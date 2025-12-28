import streamlit as st
import os
import sys

# Thêm path để import các module
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.stt_engine import STTEngine
from src.utils.audio_helper import AudioRecorder

# Khởi tạo engine (cache để không load lại mỗi lần)
@st.cache_resource
def get_stt_engine():
    model_path = "models/speech_to_text/speech-to-text-vn/whisper-vivos-final"
    return STTEngine(model_path=model_path)

def show():
    st.title("CHUYỂN ĐỔI GIỌNG NÓI SANG VĂN BẢN")
    st.markdown("---")
    
    # Khởi tạo engine
    engine = get_stt_engine()
    
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
    
    st.markdown("---")
    
    # Nút chuyển đổi
    if st.button("🔄 Chuyển đổi sang Văn bản", use_container_width=True, type="primary"):
        if not os.path.exists(output_file):
            st.warning("Vui lòng ghi âm trước!")
        else:
            with st.spinner("Đang phân tích âm thanh, vui lòng đợi..."):
                try:
                    result_text = engine.predict(output_file)
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

