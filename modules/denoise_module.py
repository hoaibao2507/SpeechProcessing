import streamlit as st
import os
import sys
import sounddevice as sd
import soundfile as sf

# Thêm path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.denoise_engine import DenoiseEngine
from src.utils.audio_helper import AudioRecorder
from src.utils.audio_visualizer import get_wavesurfer_html, get_wavesurfer_comparison_html
import streamlit.components.v1 as components

# Khởi tạo engine (cache để không load lại mỗi lần)
@st.cache_resource
def get_denoise_engine():
    model_path = "models/denoiser/model_SE_v1.pth"
    return DenoiseEngine(model_path=model_path)

def show():
    st.title("🔇 Lọc nhiễu âm thanh")
    st.markdown("---")
    
    # Khởi tạo engine
    engine = get_denoise_engine()
    
    # Đường dẫn file
    input_file = "recordings/denoise_input.wav"
    output_file = "recordings/denoise_output.wav"
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    
    # Khởi tạo recorder
    if 'denoise_recorder' not in st.session_state:
        st.session_state.denoise_recorder = AudioRecorder(filename=input_file)
        st.session_state.denoise_recording = False
        st.session_state.denoise_success = False
    
    recorder = st.session_state.denoise_recorder
    
    # Phần 1: Ghi âm
    st.subheader("📹 Bước 1: Ghi âm (Môi trường ồn)")
    st.info("💡 Hãy bật quạt hoặc tạo tiếng ồn nền, sau đó ghi âm câu nói.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Bắt đầu Ghi âm", key="denoise_start", use_container_width=True, type="primary"):
            try:
                recorder.start_recording()
                st.session_state.denoise_recording = True
                st.success("Đang ghi âm...")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    with col2:
        if st.button("⏹️ Dừng", key="denoise_stop", use_container_width=True, disabled=not st.session_state.get('denoise_recording', False)):
            try:
                recorder.stop_recording()
                st.session_state.denoise_recording = False
                st.success("Đã ghi xong!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    with col3:
        if st.button("🔊 Nghe lại", key="denoise_play", use_container_width=True, disabled=not os.path.exists(input_file)):
            try:
                recorder.play_recording()
                st.success("Đã phát xong!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
    
    # Hiển thị trạng thái
    if st.session_state.get('denoise_recording', False):
        st.info("🔴 Đang ghi âm...")
    elif os.path.exists(input_file):
        st.success("✅ Đã có file ghi âm")
        
        # Hiển thị waveform của file gốc với WaveSurfer
        st.subheader("📊 Sóng âm - File gốc")
        try:
            html = get_wavesurfer_html(input_file, wave_color='#ff7f0e', progress_color='#cc6600', height=100)
            components.html(html, height=180)
        except Exception as e:
            st.warning(f"Không thể hiển thị waveform: {e}")
    
    st.markdown("---")
    
    # Phần 2: Xử lý
    st.subheader("🤖 Bước 2: Xử lý khử nhiễu")
    
    if st.button("🚀 CHẠY KHỬ NHIỄU (AI)", use_container_width=True, type="primary"):
        if not os.path.exists(input_file):
            st.warning("Vui lòng ghi âm ở Bước 1 trước!")
        else:
            with st.spinner("AI đang tách tiếng ồn... (Vui lòng đợi)"):
                try:
                    success, message = engine.process_audio(input_file, output_file)
                    if success:
                        st.session_state.denoise_success = True
                        st.success(f"✅ {message}")
                    else:
                        st.session_state.denoise_success = False
                        st.error(f"❌ {message}")
                except Exception as e:
                    st.error(f"Lỗi xử lý: {e}")
                    st.session_state.denoise_success = False
    
    st.markdown("---")
    
    # Phần 3: Kết quả
    st.subheader("🎵 Bước 3: Kết quả sau xử lý")
    
    if st.session_state.get('denoise_success', False) and os.path.exists(output_file):
        st.success("✅ Đã lọc xong! Hãy nghe thử bên dưới.")
        
        # Hiển thị waveform so sánh với WaveSurfer
        st.subheader("📊 So sánh sóng âm")
        try:
            html = get_wavesurfer_comparison_html(
                input_file, 
                output_file,
                title1="Audio gốc (có nhiễu)",
                title2="Audio đã lọc nhiễu",
                wave_color1='#ff7f0e',
                progress_color1='#cc6600',
                wave_color2='#2ca02c',
                progress_color2='#1e7e1e',
                height=100
            )
            components.html(html, height=500)
        except Exception as e:
            st.warning(f"Không thể hiển thị waveform: {e}")
        
        if st.button("🔊 Nghe giọng đã lọc nhiễu", use_container_width=True, type="primary"):
            try:
                data, fs = sf.read(output_file)
                sd.play(data, fs)
                sd.wait()
                st.success("Đã phát xong!")
            except Exception as e:
                st.error(f"Lỗi phát âm thanh: {e}")
    else:
        st.info("Chưa có kết quả. Hãy ghi âm và chạy khử nhiễu.")

