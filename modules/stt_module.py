import streamlit as st
import os
import sys

# Thêm path để import các module
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.stt_engine import STTEngine
from src.utils.audio_helper import AudioRecorder
from src.utils.audio_visualizer import get_wavesurfer_html
import streamlit.components.v1 as components

# Khởi tạo engine cho tiếng Việt (cache để không load lại mỗi lần)
@st.cache_resource
def get_stt_engine_vn():
    model_path = "models/speech_to_text/speech-to-text-vn/whisper-vivos-final"
    return STTEngine(model_path=model_path)

# Khởi tạo engine cho tiếng Anh (cache để không load lại mỗi lần)
@st.cache_resource
def get_stt_engine_en():
    # Sử dụng model mới đã fine-tune cho tiếng Anh (checkpoint-300 là checkpoint cuối cùng)
    model_path = "models/whisper-finetuned-20251228T043928Z-1-004/whisper-finetuned/checkpoint-300"
    # Nếu model mới không có đầy đủ file, fallback về model base Whisper
    if not os.path.exists(model_path):
        # Có thể dùng model Whisper base nếu cần
        model_path = "openai/whisper-base"  # Hoặc model khác
    return STTEngine(model_path=model_path)

def show():
    st.title("🗣️ CHUYỂN ĐỔI GIỌNG NÓI SANG VĂN BẢN")
    st.markdown("---")
    
    # Chọn ngôn ngữ
    language = st.selectbox(
        "Chọn ngôn ngữ:",
        ["Tiếng Việt", "Tiếng Anh"],
        index=0
    )
    
    # Khởi tạo engine dựa trên ngôn ngữ đã chọn
    # Lưu vào session state để đảm bảo dùng đúng engine
    if language == "Tiếng Việt":
        engine = get_stt_engine_vn()
        lang_code = "vi"  # Mã ngôn ngữ ISO 639-1 cho tiếng Việt
        st.session_state.stt_language = "vi"
        st.session_state.stt_engine_type = "vn"
    else:
        engine = get_stt_engine_en()
        lang_code = "en"  # Mã ngôn ngữ ISO 639-1 cho tiếng Anh
        st.session_state.stt_language = "en"
        st.session_state.stt_engine_type = "en"
    
    # File output
    output_file = "recordings/stt_input.wav"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Khởi tạo recorder
    if 'stt_recorder' not in st.session_state:
        st.session_state.stt_recorder = AudioRecorder(filename=output_file)
        st.session_state.stt_recording = False
        st.session_state.stt_uploaded_file = None
    
    recorder = st.session_state.stt_recorder
    
    # Phần chọn nguồn âm thanh
    st.subheader("📹 Chọn nguồn âm thanh")
    st.info("💡 Ghi âm hoặc upload file âm thanh để chuyển đổi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎤 Ghi âm")
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            if st.button("▶️ Bắt đầu", key="stt_start", use_container_width=True, type="primary"):
                try:
                    recorder.start_recording()
                    st.session_state.stt_recording = True
                    st.success("Đang ghi âm...")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        with col1_2:
            if st.button("⏹️ Dừng", key="stt_stop", use_container_width=True, disabled=not st.session_state.get('stt_recording', False)):
                try:
                    recorder.stop_recording()
                    st.session_state.stt_recording = False
                    st.success("Đã ghi xong!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        with col1_3:
            if st.button("🔊 Nghe", key="stt_play", use_container_width=True, disabled=not os.path.exists(output_file)):
                try:
                    recorder.play_recording()
                    st.success("Đã phát xong!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        if st.session_state.get('stt_recording', False):
            st.info("🔴 Đang ghi âm...")
        elif os.path.exists(output_file):
            st.success("✅ Đã có file ghi âm")
    
    with col2:
        st.markdown("#### 📁 Upload file")
        uploaded_file = st.file_uploader(
            "Chọn file âm thanh",
            type=['wav', 'mp3', 'flac', 'ogg', 'm4a'],
            key="stt_upload"
        )
        
        if uploaded_file is not None:
            # Lưu file tạm
            temp_path = f"recordings/temp_{uploaded_file.name}"
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.stt_uploaded_file = temp_path
            st.success(f"✅ Đã tải: {uploaded_file.name}")
        else:
            st.session_state.stt_uploaded_file = None
    
    # Hiển thị waveform nếu có file audio
    audio_file_to_show = None
    if st.session_state.get('stt_uploaded_file') and os.path.exists(st.session_state.stt_uploaded_file):
        audio_file_to_show = st.session_state.stt_uploaded_file
    elif os.path.exists(output_file):
        audio_file_to_show = output_file
    
    if audio_file_to_show:
        st.subheader("📊 Sóng âm")
        try:
            html = get_wavesurfer_html(audio_file_to_show, wave_color='#1e90ff', progress_color='#0066cc', height=120)
            components.html(html, height=200)
        except Exception as e:
            st.warning(f"Không thể hiển thị waveform: {e}")
    
    st.markdown("---")
    
    # Nút chuyển đổi
    if st.button("🔄 Chuyển đổi sang Văn bản", use_container_width=True, type="primary"):
        # Xác định file nào sẽ được sử dụng (ưu tiên file upload)
        audio_file = None
        
        if st.session_state.get('stt_uploaded_file') and os.path.exists(st.session_state.stt_uploaded_file):
            audio_file = st.session_state.stt_uploaded_file
        elif os.path.exists(output_file):
            audio_file = output_file
        else:
            st.warning("Vui lòng ghi âm hoặc upload file âm thanh trước!")
        
        if audio_file:
            with st.spinner("Đang phân tích âm thanh, vui lòng đợi..."):
                try:
                    result_text = engine.predict(audio_file, language=lang_code)
                    st.session_state.stt_result = result_text
                except Exception as e:
                    st.error(f"Lỗi xử lý: {e}")
                    st.session_state.stt_result = None
    
    # Hiển thị kết quả
    st.markdown("---")
    st.subheader("📝 Kết quả nhận diện")
    
    if 'stt_result' in st.session_state and st.session_state.stt_result:
        st.text_area(
            "Văn bản đã chuyển đổi:",
            value=st.session_state.stt_result,
            height=200,
            disabled=True
        )
    else:
        st.info("Chưa có kết quả. Hãy ghi âm và nhấn nút chuyển đổi.")

