import streamlit as st
import sys
import os

# Thêm thư mục hiện tại vào đường dẫn tìm kiếm module để tránh lỗi ModuleNotFound
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import stt_module, denoise_module, animal_module

# Cấu hình trang
st.set_page_config(page_title="Ứng dụng xử lý tiếng nói", layout="wide")

# --- Định nghĩa các hàm trang ---
def show_intro():
    st.title("🎤 Ứng dụng Xử lý Tiếng nói")
    st.markdown("---")
    
    st.markdown("""
    ## 📋 Mô tả
    Ứng dụng xử lý tiếng nói với giao diện web được xây dựng bằng Python và Streamlit. 
    Dự án cung cấp các chức năng chính: chuyển đổi giọng nói sang văn bản (Speech-to-Text), 
    lọc nhiễu âm thanh (Audio Denoising) và nhận diện âm thanh động vật.
    
    ## ✨ Các chức năng
    
    ### 1. 🎤 Chuyển đổi giọng nói sang văn bản (Speech-to-Text)
    - Ghi âm giọng nói trực tiếp từ microphone
    - Chuyển đổi giọng nói tiếng Việt thành văn bản
    - Sử dụng mô hình Whisper đã được fine-tune cho tiếng Việt
    - Hỗ trợ GPU (CUDA) để tăng tốc xử lý
    
    ### 2. 🔇 Lọc nhiễu âm thanh (Audio Denoising)
    - Ghi âm trong môi trường có nhiễu
    - Sử dụng mô hình Deep Learning (CNN + LSTM) để loại bỏ nhiễu
    - Nghe lại âm thanh đã được xử lý
    - Cải thiện chất lượng âm thanh bằng AI
    
    ### 3. 🐾 Nhận diện Âm thanh Động vật (Animal Recognition)
    - Ghi âm tiếng kêu của động vật hoặc các loại âm thanh khác
    - Sử dụng mô hình AST (Audio Spectrogram Transformer) với độ chính xác 96%
    - Hiển thị kết quả nhận diện với độ tin cậy (confidence)
    - Hiển thị top 5 kết quả có khả năng nhất
    - Nhận diện được nhiều loại động vật: chó, mèo, gà, bò, lợn, cừu, ếch, quạ, chim, dế, côn trùng
    - Cũng có thể nhận diện các âm thanh khác: máy bay, tàu hỏa, mưa, gió, v.v.
    
    ## 🚀 Hướng dẫn sử dụng
    
    ### Chuyển đổi giọng nói sang văn bản
    1. Chọn menu "🎤 CHUYỂN ĐỔI GIỌNG NÓI" ở sidebar
    2. Nhấn nút "Bắt đầu Ghi âm"
    3. Nói vào microphone
    4. Nhấn "Dừng" khi hoàn tất
    5. Nhấn "Chuyển đổi sang Văn bản" để xem kết quả
    
    ### Lọc nhiễu âm thanh
    1. Chọn menu "🔇 LỌC NHIỄU" ở sidebar
    2. Tạo môi trường có nhiễu (bật quạt, TV, v.v.)
    3. Nhấn "Bắt đầu Ghi âm" và nói
    4. Nhấn "Dừng" khi hoàn tất
    5. Nhấn "CHẠY KHỬ NHIỄU (AI)" để xử lý
    6. Nhấn "Nghe giọng đã lọc nhiễu" để kiểm tra kết quả
    
    ### Nhận diện âm thanh động vật
    1. Chọn menu "🐾 NHẬN DIỆN ĐỘNG VẬT" ở sidebar
    2. Nhấn "Bắt đầu Ghi âm" hoặc upload file âm thanh
    3. Ghi âm tiếng kêu của động vật (chó, mèo, gà, v.v.) hoặc các âm thanh khác
    4. Nhấn "Dừng" khi hoàn tất
    5. Nhấn "NHẬN DIỆN ÂM THANH" để xem kết quả
    6. Xem kết quả chính và top 5 kết quả có khả năng nhất
    """)

# --- Sidebar ---
with st.sidebar:
    logo = "https://itute.github.io/img/logo/logo.png"
    st.image(logo, width=128)

    st.markdown("### Speech Processing")
    if st.button("⭐ GIỚI THIỆU"):
        st.query_params.clear()
        st.query_params.update({"menu": "GioiThieu"})
    if st.button("🎤 CHUYỂN ĐỔI GIỌNG NÓI"):
        st.query_params.clear()
        st.query_params.update({"menu": "STT"})
    if st.button("🔇 LỌC NHIỄU"):
        st.query_params.clear()
        st.query_params.update({"menu": "Denoise"})
    if st.button("🐾 NHẬN DIỆN ĐỘNG VẬT"):
        st.query_params.clear()
        st.query_params.update({"menu": "Animal"})

# --- Routing ---
pages = {
    "GioiThieu": show_intro,
    "STT": stt_module.show,
    "Denoise": denoise_module.show,
    "Animal": animal_module.show,
}

# Lấy route từ URL
menu = st.query_params.get("menu", "GioiThieu")

# Gọi hàm tương ứng nếu có
if menu in pages:
    pages[menu]()
else:
    st.error("Trang không tồn tại.")

# --- Giao diện nền ---
page_bg = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Open Sans', sans-serif;
    background-image: linear-gradient(
        rgba(0, 0, 0, 0.4), 
        rgba(0, 0, 0, 0.4)
    ), url("https://itute.github.io/img/hcmute_bg.jpg");
    background-size: cover;
    background-position: center;
}

[data-testid="stHeader"] {
    background: rgba(255, 255, 255, 0);
}

h1, h2, h3 {
    color: #f2f2f2;
}

/* Vô hiệu hóa resize handle của sidebar */
[data-testid="stSidebarResizeHandle"] {
    display: none !important;
    pointer-events: none !important;
}

/* Đảm bảo sidebar content có thể tương tác */
section[data-testid="stSidebar"] {
    pointer-events: auto !important;
}

section[data-testid="stSidebar"] > div {
    pointer-events: auto !important;
}

/* Style cho logo hình ảnh trong sidebar - chỉ căn giữa logo */
section[data-testid="stSidebar"] div[data-testid="stImage"],
section[data-testid="stSidebar"] [data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    justify-items: center !important;
    width: 100% !important;
    margin: 0 auto !important;
}

/* Override justify-items cho container của image logo - sử dụng anchor-center */
section[data-testid="stSidebar"] div[data-testid="stImage"] [class*="st-emotion-cache"],
section[data-testid="stSidebar"] [data-testid="stImage"] [class*="st-emotion-cache"],
section[data-testid="stSidebar"] [class*="st-emotion-cache-uwwqev"] {
    justify-items: anchor-center !important;
    width: 100% !important;
}

/* Căn giữa logo image */
section[data-testid="stSidebar"] div[data-testid="stImage"] img,
section[data-testid="stSidebar"] [data-testid="stImage"] img {
    display: block !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Style cho nút trong sidebar - sát viền và responsive */
section[data-testid="stSidebar"] button[data-testid="stBaseButton"] {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    background: linear-gradient(to right, rgba(0, 80, 200, 0.7), rgba(0, 180, 200, 0.7)) !important;
    border: 1px solid white !important;
    padding: 10px 0 !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    box-sizing: border-box !important;
    margin: 5px 0 !important;
    display: block !important;
    position: relative !important;
    z-index: 100 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
}

button[data-testid="stBaseButton"]:hover {
    background: linear-gradient(to right, rgba(0, 80, 200, 0.9), rgba(0, 180, 200, 0.9)) !important;
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

button[data-testid="stBaseButton-secondary"] {
    width: 100% !important;
}

/* Đảm bảo container của button full width */
section[data-testid="stSidebar"] [class*="element-container"],
section[data-testid="stSidebar"] [class*="block-container"] {
    width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Style cho select */
div[data-testid="stTextInput"], 
div[data-testid="stSelectbox"], 
div[data-testid="stMultiSelect"],
div[data-testid="stCheckbox"] {
    background: linear-gradient(to right, rgb(255 255 255 / 70%), rgba(0, 180, 200, 0.7));
    border: 1px solid white;
    padding: 10px;
    border-radius: 10px;
    font-size: 16px;
    color: #fff;
}

section[data-testid="stMain"] {
    background: rgba(255, 255, 255, 0.25);
    padding: 20px;
}

/* Nền xám trắng cho vùng nội dung bên trong */
div[data-testid="stMainBlockContainer"] {
    background: rgba(245, 245, 250, 0.95) !important;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
