import streamlit as st
import os
import sys

# Thêm path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.animal_engine import AnimalEngine
from src.utils.audio_helper import AudioRecorder

# Khởi tạo engine (cache để không load lại mỗi lần)
@st.cache_resource
def get_animal_engine():
    model_path = "models/My_AST_Model_96acc-20251227T152517Z-1-001/My_AST_Model_96acc"
    return AnimalEngine(model_path=model_path)

def _translate_label(label):
    """Chuyển đổi label tiếng Anh sang tiếng Việt."""
    translations = {
        "dog": "Chó",
        "cat": "Mèo",
        "sheep": "Cừu",
        "cow": "Bò",
        "pig": "Lợn",
        "hen": "Gà mái",
        "rooster": "Gà trống",
        "frog": "Ếch",
        "crow": "Quạ",
        "chirping_birds": "Chim hót",
        "crickets": "Dế",
        "insects": "Côn trùng",
        "vacuum_cleaner": "Máy hút bụi",
        "thunderstorm": "Sấm sét",
        "airplane": "Máy bay",
        "train": "Tàu hỏa",
        "car_horn": "Còi xe",
        "rain": "Mưa",
        "wind": "Gió",
        "footsteps": "Tiếng bước chân",
        "laughing": "Tiếng cười",
        "crying_baby": "Trẻ em khóc",
        "coughing": "Ho",
        "sneezing": "Hắt hơi",
        "snoring": "Ngáy",
        "breathing": "Thở",
        "clock_tick": "Tiếng đồng hồ",
        "clock_alarm": "Báo thức",
        "door_wood_knock": "Gõ cửa",
        "door_wood_creaks": "Cửa kêu cót két",
        "can_opening": "Mở lon",
        "washing_machine": "Máy giặt",
        "toilet_flush": "Xả nước toilet",
        "brushing_teeth": "Đánh răng",
        "drinking_sipping": "Uống nước",
        "keyboard_typing": "Gõ bàn phím",
        "mouse_click": "Click chuột",
        "fireworks": "Pháo hoa",
        "chainsaw": "Cưa máy",
        "helicopter": "Trực thăng",
        "engine": "Động cơ",
        "siren": "Còi báo động",
        "church_bells": "Chuông nhà thờ",
        "clapping": "Vỗ tay",
        "glass_breaking": "Vỡ kính",
        "hand_saw": "Cưa tay",
        "crackling_fire": "Lửa cháy",
        "pouring_water": "Đổ nước",
        "water_drops": "Giọt nước",
        "sea_waves": "Sóng biển",
    }
    return translations.get(label.lower(), label.replace("_", " ").title())

def show():
    st.title("🐾 Nhận diện âm thanh động vật")
    st.markdown("---")
    
    # Khởi tạo engine
    engine = get_animal_engine()
    
    # File output
    output_file = "recordings/animal_input.wav"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Khởi tạo recorder
    if 'animal_recorder' not in st.session_state:
        st.session_state.animal_recorder = AudioRecorder(filename=output_file)
        st.session_state.animal_recording = False
        st.session_state.animal_uploaded_file = None
    
    recorder = st.session_state.animal_recorder
    
    # Phần 1: Chọn nguồn âm thanh
    st.subheader("📹 Bước 1: Chọn nguồn âm thanh")
    st.info("💡 Ghi âm hoặc upload file âm thanh để nhận diện")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎤 Ghi âm")
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            if st.button("▶️ Bắt đầu", key="animal_start", use_container_width=True, type="primary"):
                try:
                    recorder.start_recording()
                    st.session_state.animal_recording = True
                    st.success("Đang ghi âm...")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        with col1_2:
            if st.button("⏹️ Dừng", key="animal_stop", use_container_width=True, disabled=not st.session_state.get('animal_recording', False)):
                try:
                    recorder.stop_recording()
                    st.session_state.animal_recording = False
                    st.success("Đã ghi xong!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        with col1_3:
            if st.button("🔊 Nghe", key="animal_play", use_container_width=True, disabled=not os.path.exists(output_file)):
                try:
                    recorder.play_recording()
                    st.success("Đã phát xong!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
        
        if st.session_state.get('animal_recording', False):
            st.info("🔴 Đang ghi âm...")
        elif os.path.exists(output_file):
            st.success("✅ Đã có file ghi âm")
    
    with col2:
        st.markdown("#### 📁 Upload file")
        uploaded_file = st.file_uploader(
            "Chọn file âm thanh",
            type=['wav', 'mp3', 'flac', 'ogg', 'm4a'],
            key="animal_upload"
        )
        
        if uploaded_file is not None:
            # Lưu file tạm
            temp_path = f"recordings/temp_{uploaded_file.name}"
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.animal_uploaded_file = temp_path
            st.success(f"✅ Đã tải: {uploaded_file.name}")
        else:
            st.session_state.animal_uploaded_file = None
    
    st.markdown("---")
    
    # Phần 2: Nhận diện
    st.subheader("🤖 Bước 2: Nhận diện")
    
    if st.button("🔍 NHẬN DIỆN ÂM THANH", use_container_width=True, type="primary"):
        # Xác định file nào sẽ được sử dụng (ưu tiên file upload)
        audio_file = None
        
        if st.session_state.get('animal_uploaded_file') and os.path.exists(st.session_state.animal_uploaded_file):
            audio_file = st.session_state.animal_uploaded_file
        elif os.path.exists(output_file):
            audio_file = output_file
        else:
            st.warning("Vui lòng ghi âm hoặc upload file âm thanh trước!")
        
        if audio_file:
            with st.spinner("Đang phân tích âm thanh..."):
                try:
                    result = engine.predict(audio_file, top_k=5)
                    st.session_state.animal_result = result
                except Exception as e:
                    st.error(f"Lỗi xử lý: {e}")
                    st.session_state.animal_result = None
    
    st.markdown("---")
    
    # Phần 3: Kết quả
    st.subheader("📊 Kết quả nhận diện")
    
    if 'animal_result' in st.session_state and st.session_state.animal_result:
        result = st.session_state.animal_result
        
        if not result.get("success", False):
            error_msg = result.get("error", "Có lỗi xảy ra")
            st.error(f"❌ Lỗi: {error_msg}")
        else:
            # Kết quả chính
            top_result = result.get("top_result")
            if top_result:
                label = top_result["label"]
                confidence = top_result["confidence"]
                label_vn = _translate_label(label)
                is_animal = result.get("is_animal", False)
                prefix = "[Động vật]" if is_animal else "[Âm thanh]"
                
                st.markdown(f"### {prefix} {label_vn}")
                st.markdown(f"**Độ tin cậy:** {confidence}")
            
            # Top K results
            st.markdown("#### Top 5 kết quả:")
            top_k = result.get("top_k", [])
            
            if top_k:
                for i, item in enumerate(top_k, 1):
                    label = item["label"]
                    label_vn = _translate_label(label)
                    confidence = item["confidence"]
                    is_animal = engine._is_animal_label(label)
                    prefix = "[Động vật]" if is_animal else "[Âm thanh]"
                    
                    with st.expander(f"{i}. {prefix} {label_vn} ({label})"):
                        st.write(f"**Độ tin cậy:** {confidence}")
    else:
        st.info("Chưa có kết quả. Hãy ghi âm/upload file và nhấn nút nhận diện.")

