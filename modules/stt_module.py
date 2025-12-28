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
    
    recorder = st.session_state.stt_recorder
    
    # Phần ghi âm
    st.subheader("📹 Ghi âm")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Bắt đầu Ghi âm", use_container_width=True, type="primary"):
            try:
                recorder.start_recording()
                st.session_state.stt_recording = True
                st.success("Đang ghi âm...")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    with col2:
        if st.button("⏹️ Dừng", use_container_width=True, disabled=not st.session_state.get('stt_recording', False)):
            try:
                recorder.stop_recording()
                st.session_state.stt_recording = False
                st.success("Đã ghi xong!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    with col3:
        if st.button("🔊 Nghe lại", use_container_width=True, disabled=not os.path.exists(output_file)):
            try:
                recorder.play_recording()
                st.success("Đã phát xong!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    # Hiển thị trạng thái
    if st.session_state.get('stt_recording', False):
        st.info("🔴 Đang ghi âm...")
    elif os.path.exists(output_file):
        st.success("✅ Đã có file ghi âm")
        
        # Hiển thị waveform với WaveSurfer
        st.subheader("📊 Sóng âm")
        try:
            html = get_wavesurfer_html(output_file, wave_color='#1e90ff', progress_color='#0066cc', height=120)
            components.html(html, height=200)
        except Exception as e:
            st.warning(f"Không thể hiển thị waveform: {e}")
    
    st.markdown("---")
    
    # Nút chuyển đổi
    if st.button("🔄 Chuyển đổi sang Văn bản", use_container_width=True, type="primary"):
        if not os.path.exists(output_file):
            st.warning("Vui lòng ghi âm trước!")
        else:
            with st.spinner("Đang phân tích âm thanh, vui lòng đợi..."):
                try:
                    result_text = engine.predict(output_file, language=lang_code)
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

