# SpeechProcessing
Đồ án cuối kỳ môn Xử lý tiếng nói

## 📋 Mô tả
Ứng dụng xử lý tiếng nói với giao diện đồ họa (GUI) được xây dựng bằng Python và Tkinter. Dự án cung cấp các chức năng chính: chuyển đổi giọng nói sang văn bản (Speech-to-Text) và lọc nhiễu âm thanh (Audio Denoising).

## ✨ Các chức năng

### 1. Chuyển đổi giọng nói sang văn bản (Speech-to-Text)
- Ghi âm giọng nói trực tiếp từ microphone
- Chuyển đổi giọng nói tiếng Việt thành văn bản
- Sử dụng mô hình Whisper đã được fine-tune cho tiếng Việt
- Hỗ trợ GPU (CUDA) để tăng tốc xử lý

### 2. Lọc nhiễu âm thanh (Audio Denoising)
- Ghi âm trong môi trường có nhiễu
- Sử dụng mô hình Deep Learning (CNN + LSTM) để loại bỏ nhiễu
- Nghe lại âm thanh đã được xử lý
- Cải thiện chất lượng âm thanh bằng AI

### 3. Nhận diện Âm thanh Động vật (Animal Recognition)
- Ghi âm tiếng kêu của động vật hoặc các loại âm thanh khác
- Sử dụng mô hình AST (Audio Spectrogram Transformer) với độ chính xác 96%
- Hiển thị kết quả nhận diện với độ tin cậy (confidence)
- Hiển thị top 5 kết quả có khả năng nhất
- Nhận diện được nhiều loại động vật: chó, mèo, gà, bò, lợn, cừu, ếch, quạ, chim, dế, côn trùng
- Cũng có thể nhận diện các âm thanh khác: máy bay, tàu hỏa, mưa, gió, v.v.

## 🛠️ Yêu cầu hệ thống

### Phần mềm
- Python 3.7 trở lên
- PyTorch (hỗ trợ CUDA nếu có GPU NVIDIA)
- Các thư viện Python (xem phần Cài đặt)

### Phần cứng (khuyến nghị)
- Microphone để ghi âm
- GPU NVIDIA (tùy chọn, để tăng tốc xử lý)
- RAM: Tối thiểu 4GB (khuyến nghị 8GB trở lên)

## 📦 Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd SpeechProcessing
```

### 2. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt các thư viện cần thiết
```bash
pip install torch torchvision torchaudio
pip install transformers
pip install librosa
pip install soundfile
pip install sounddevice
pip install numpy
```

Hoặc tạo file `requirements.txt` và cài đặt:
```bash
pip install -r requirements.txt
```

### 4. Tải các mô hình
Dự án yêu cầu các mô hình sau:

#### Mô hình Speech-to-Text:
- Đường dẫn: `models/speech_to_text/speech-to-text-vn/whisper-vivos-final`
- Mô hình Whisper đã được fine-tune cho tiếng Việt
- **Lưu ý**: Đường dẫn này phải chứa trực tiếp các file model (config.json, model.safetensors, tokenizer.json, v.v.)

#### Mô hình Denoising:
- Đường dẫn: `models/denoiser/model_SE_v1.pth`
- Mô hình Speech Enhancement (CNN + LSTM)

#### Mô hình Nhận diện Động vật (Animal Recognition):
- Đường dẫn: `models/My_AST_Model_96acc-20251227T152517Z-1-001/My_AST_Model_96acc`
- Mô hình AST (Audio Spectrogram Transformer) với độ chính xác 96%
- Nhận diện 50 loại âm thanh bao gồm: chó, mèo, gà, bò, lợn, cừu, ếch, quạ, chim, dế, côn trùng và nhiều âm thanh khác
- **Lưu ý**: Đường dẫn này phải chứa trực tiếp các file model (config.json, model.safetensors, label_map.json, v.v.)

**Lưu ý**: Bạn cần tải các mô hình này và đặt vào đúng thư mục như trên.

## 🚀 Cách chạy dự án

### Chạy ứng dụng chính
```bash
python main.py
```

Ứng dụng sẽ mở cửa sổ GUI với các tab chức năng.

### Cấu trúc thư mục
```
SpeechProcessing/
├── main.py                 # File chạy chính
├── src/
│   ├── core/              # Các engine xử lý
│   │   ├── stt_engine.py  # Engine chuyển đổi giọng nói
│   │   ├── denoise_engine.py  # Engine lọc nhiễu
│   │   └── animal_engine.py   # Engine nhận diện động vật
│   ├── ui/                # Giao diện người dùng
│   │   ├── main_window.py # Cửa sổ chính
│   │   ├── tabs/          # Các tab chức năng
│   │   └── widgets/       # Các widget tái sử dụng
│   └── utils/             # Tiện ích hỗ trợ
│       └── audio_helper.py # Helper ghi âm
├── models/                # Thư mục chứa các mô hình
│   ├── speech_to_text/
│   ├── denoiser/
│   └── My_AST_Model_96acc-20251227T152517Z-1-001/  # Model nhận diện động vật
└── recordings/            # Thư mục lưu file ghi âm
```

## 📖 Hướng dẫn sử dụng

### Chuyển đổi giọng nói sang văn bản
1. Mở tab "Chuyển đổi giọng nói sang văn bản"
2. Nhấn nút "Bắt đầu Ghi âm"
3. Nói vào microphone
4. Nhấn "Dừng" khi hoàn tất
5. Nhấn "Chuyển đổi sang Văn bản" để xem kết quả

### Lọc nhiễu âm thanh
1. Mở tab "Lọc nhiễu"
2. Tạo môi trường có nhiễu (bật quạt, TV, v.v.)
3. Nhấn "Bắt đầu Ghi âm" và nói
4. Nhấn "Dừng" khi hoàn tất
5. Nhấn "CHẠY KHỬ NHIỄU (AI)" để xử lý
6. Nhấn "Nghe giọng đã lọc nhiễu" để kiểm tra kết quả

### Nhận diện âm thanh động vật
1. Mở tab "Nhận diện Chó/Mèo"
2. Nhấn "Bắt đầu Ghi âm"
3. Ghi âm tiếng kêu của động vật (chó, mèo, gà, v.v.) hoặc các âm thanh khác
4. Nhấn "Dừng" khi hoàn tất
5. Nhấn "NHẬN DIỆN ÂM THANH" để xem kết quả
6. Xem kết quả chính và top 5 kết quả có khả năng nhất

## 🔧 Cấu hình

### Thay đổi đường dẫn mô hình
Nếu bạn đặt mô hình ở vị trí khác, chỉnh sửa trong `src/ui/main_window.py`:
```python
self.stt_engine = STTEngine(model_path="models/speech_to_text/speech-to-text-vn/whisper-vivos-final")
self.denoise_engine = DenoiseEngine(model_path="models/denoiser/model_SE_v1.pth")
```

### Thay đổi thiết bị xử lý
- Ứng dụng tự động phát hiện GPU nếu có
- Nếu không có GPU, sẽ tự động chuyển sang CPU
- Xem log trong console để biết thiết bị đang sử dụng

## ⚠️ Lưu ý
- Đảm bảo microphone hoạt động bình thường
- File ghi âm được lưu trong thư mục `recordings/`
- Quá trình xử lý có thể mất vài giây, vui lòng đợi
- Mô hình Whisper yêu cầu âm thanh ở tần số 16kHz

## 👥 Tác giả
Đồ án cuối kỳ môn Xử lý tiếng nói

## 📝 License
[MIT License hoặc license của bạn]