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
    # Thêm class để nhận diện trang giới thiệu
    st.markdown('<div class="intro-page">', unsafe_allow_html=True)
    
    html_code = """
    <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 0; padding-top: 0;">
        <h2 style="color: #FFFFFF; margin: 0; padding: 0;">BÁO CÁO CUỐI KỲ</h2>
        <h1 style="color: #FFFFFF; margin: 0; padding: 0;">MÔN XỬ LÝ TIẾNG NÓI</h1>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    page_bg = """
    <style>
    .members {
        padding: 1em;
        background-color: transparent;
        border-radius: 8px;
        text-align: center;
        font-size: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .members h3 {
        font-size: 26px;
        color: #FFFFFF;
    }
    .member-item {
        margin-bottom: 0.5em;
        color: #FFFFFF;
        font-size: 22px;
    }
    .description {
        padding: 1em;
        background-color: transparent;
        text-align: center;
        color: #FFFFFF;
        font-size: 18px;
        line-height: 1.8;
    }
    .description h3 {
        color: #FFFFFF;
        font-size: 24px;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    .description ul {
        text-align: left;
        display: inline-block;
        color: #FFFFFF;
    }
    .description li {
        margin-bottom: 0.5em;
        color: #FFFFFF;
    }
    .features-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 10px 0;
        margin-top: 0;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        color: #FFFFFF;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.5);
    }
    .feature-card h4 {
        color: #FFFFFF;
        font-size: 20px;
        margin: 0 0 15px 0;
        font-weight: bold;
    }
    .feature-card p {
        color: #FFFFFF;
        font-size: 16px;
        margin: 0;
        line-height: 1.6;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="members" style="margin-top: 5px;">
            <h3>Thành viên:</h3>
            <div class="member-item">
                <strong>Speech Processing Team</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="text-align: center; margin: 10px 0 20px 0;">
            <h3 style="color: #FFFFFF; font-size: 28px; margin-bottom: 15px;">CÁC CHỨC NĂNG</h3>
        </div>
        <div class="features-container">
            <div class="feature-card">
                <h4>🎤 Chuyển đổi giọng nói sang văn bản</h4>
                <p>Ghi âm và chuyển đổi giọng nói tiếng Việt thành văn bản sử dụng mô hình Whisper</p>
            </div>
            <div class="feature-card">
                <h4>🔇 Lọc nhiễu âm thanh</h4>
                <p>Sử dụng mô hình Deep Learning (CNN + LSTM) để loại bỏ nhiễu và cải thiện chất lượng âm thanh</p>
            </div>
            <div class="feature-card">
                <h4>🐾 Nhận diện Âm thanh Động vật</h4>
                <p>Sử dụng mô hình AST với độ chính xác 96% để nhận diện tiếng kêu động vật và các loại âm thanh khác</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    logo = "https://itute.github.io/img/logo/logo.png"
    st.image(logo, width=128)

    st.markdown("### Speech Processing")
    if st.button("GIỚI THIỆU"):
        st.query_params.clear()
        st.query_params.update({"menu": "GioiThieu"})
    if st.button("CHUYỂN ĐỔI GIỌNG NÓI"):
        st.query_params.clear()
        st.query_params.update({"menu": "STT"})
    if st.button("LỌC NHIỄU"):
        st.query_params.clear()
        st.query_params.update({"menu": "Denoise"})
    if st.button("NHẬN DIỆN ĐỘNG VẬT"):
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

/* Nền đen cho sidebar */
section[data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Style cho nút trong sidebar - màu xanh ngọc dương */
section[data-testid="stSidebar"] button[data-testid="stBaseButton"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
section[data-testid="stSidebar"] button {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    background-color: #00CED1 !important;
    background: #00CED1 !important;
    border: 1px solid #00CED1 !important;
    padding: 10px 0 !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    color: #ffffff !important;
    transition: all 0.3s ease !important;
    box-sizing: border-box !important;
    margin: 5px 0 !important;
    display: block !important;
    position: relative !important;
    z-index: 100 !important;
    pointer-events: auto !important;
    cursor: pointer !important;
}

section[data-testid="stSidebar"] button[data-testid="stBaseButton"]:hover,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover,
section[data-testid="stSidebar"] button:hover {
    background-color: #20B2AA !important;
    background: #20B2AA !important;
    border-color: #20B2AA !important;
    transform: scale(1.05) !important;
    box-shadow: 0 4px 8px rgba(0, 206, 209, 0.4) !important;
    cursor: pointer !important;
}

/* Override tất cả button trong sidebar với màu xanh ngọc dương */
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-secondary"] {
    background-color: #00CED1 !important;
    background: #00CED1 !important;
    border-color: #00CED1 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #20B2AA !important;
    background: #20B2AA !important;
    border-color: #20B2AA !important;
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

/* Nền xám trắng cho vùng nội dung bên trong - chỉ khi không phải trang giới thiệu */
div[data-testid="stMainBlockContainer"]:not(:has(.intro-page)):not(:has(h2[style*="BÁO CÁO"])) {
    background: rgba(245, 245, 250, 0.95) !important;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

/* Bỏ nền xám cho trang giới thiệu và đẩy lên cao */
div[data-testid="stMainBlockContainer"]:has(.intro-page),
div[data-testid="stMainBlockContainer"]:has(h2[style*="BÁO CÁO"]) {
    background: transparent !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* Đẩy nội dung trang giới thiệu lên cao */
.intro-page {
    background: transparent !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Giảm margin của các phần tử đầu tiên trong trang giới thiệu */
.intro-page > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Đảm bảo tất cả nội dung trong trang giới thiệu không có nền */
.intro-page {
    background: transparent !important;
}

/* Làm text trong phần kết quả đậm hơn */
textarea[data-testid="stTextArea"] {
    color: #1a1a1a !important;
    font-weight: 500 !important;
    font-size: 16px !important;
}

/* Làm text trong textarea đậm hơn */
div[data-testid="stTextArea"] textarea {
    color: #1a1a1a !important;
    font-weight: 500 !important;
    font-size: 16px !important;
}

/* Làm label "Văn bản đã chuyển đổi" đậm hơn */
div[data-testid="stTextArea"] label {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* Làm subheader "Kết quả nhận diện" đậm hơn */
h3[data-testid="stHeader"] {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

/* Làm tất cả text trong phần kết quả đậm hơn */
div[data-testid="stTextArea"] * {
    color: #1a1a1a !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)
