import os
import torch
import torch.nn as nn
import librosa
import soundfile as sf
import numpy as np

# ==========================================
# 1. ĐỊNH NGHĨA KIẾN TRÚC MÔ HÌNH (CODE CỦA BẠN)
# ==========================================
class SpeechEnhancer(nn.Module):
    def __init__(self):
        super(SpeechEnhancer, self).__init__()
        # Encoder: Giảm chiều Frequency từ 256 -> 128 -> 64 -> 32
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3,3), stride=(2,1), padding=(1,1)),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=(3,3), stride=(2,1), padding=(1,1)),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=(3,3), stride=(2,1), padding=(1,1)),
            nn.ReLU()
        )
        # LSTM: 64 channels * 32 bins = 2048
        self.lstm = nn.LSTM(input_size=2048, hidden_size=512, num_layers=2, batch_first=True)
        self.fc = nn.Linear(512, 2048)

        # Decoder: Khôi phục chiều Frequency 32 -> 64 -> 128 -> 256
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=(3,3), stride=(2,1), padding=(1,1), output_padding=(1,0)),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, kernel_size=(3,3), stride=(2,1), padding=(1,1), output_padding=(1,0)),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, kernel_size=(3,3), stride=(2,1), padding=(1,1), output_padding=(1,0))
        )

    def forward(self, x):
        # x: [Batch, 1, Freq(256), Time]
        b, c, f, t = x.size()
        
        # Encoder
        x = self.encoder(x)
        b_n, c_n, f_n, t_n = x.size()
        
        # LSTM
        x = x.permute(0, 3, 1, 2).contiguous() # [Batch, Time, 64, 32]
        x = x.view(b_n, t_n, -1)              # [Batch, Time, 2048]
        x, _ = self.lstm(x)
        x = self.fc(x)
        
        # Decoder
        x = x.view(b_n, t_n, c_n, f_n)
        x = x.permute(0, 2, 3, 1).contiguous()
        x = self.decoder(x)
        
        # Fix kích thước để đảm bảo đầu ra đúng 256 freq và time gốc
        if x.size(2) != f or x.size(3) != t:
            x = nn.functional.interpolate(x, size=(f, t))
        return x

# ==========================================
# 2. CLASS ENGINE XỬ LÝ CHÍNH
# ==========================================
class DenoiseEngine:
    def __init__(self, model_path="models/denoiser/model_SE_v1.pth"):
        self.model_path = model_path
        self.model = None
        
        # Chọn thiết bị (GPU ưu tiên)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"--- Khởi tạo Denoise Engine trên {self.device} ---")

        self._load_model()

    def _load_model(self):
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Không tìm thấy model tại: {self.model_path}")

            print("Đang load model khử nhiễu...")
            
            # Khởi tạo model từ class của bạn
            self.model = SpeechEnhancer()
            
            # Load trọng số (Weights)
            state_dict = torch.load(self.model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            
            print("Model Lọc nhiễu đã sẵn sàng!")

        except Exception as e:
            print(f"Lỗi load model Denoise: {e}")
            import traceback
            traceback.print_exc()

    def process_audio(self, input_path, output_path):
        """
        Quy trình: Load Wav -> STFT (Spectrogram) -> Model -> iSTFT (Wav) -> Save
        """
        if self.model is None:
            return False, "Model chưa được load."

        try:
            print(f"Đang xử lý file: {input_path}")
            
            # 1. Load Audio (Mặc định 16k cho các bài toán Speech)
            audio, sr = librosa.load(input_path, sr=16000)
            
            # 2. Tạo Spectrogram (STFT)
            # n_fft=512 -> tạo ra 257 bins tần số (512/2 + 1)
            stft = librosa.stft(audio, n_fft=512, hop_length=256)
            magnitude = np.abs(stft)  # Lấy biên độ (Dùng cho model)
            phase = np.angle(stft)    # Lấy pha (Giữ lại để tái tạo âm thanh)

            # 3. Chuẩn bị dữ liệu cho Model
            # Model yêu cầu Freq = 256, nhưng stft có 257 -> Cắt bỏ 1 dòng cuối
            mag_input = magnitude[:256, :] 
            
            # Chuyển sang Tensor [Batch, Channel, Freq, Time]
            # Thêm 1 chiều Batch và 1 chiều Channel -> [1, 1, 256, Time]
            inputs = torch.tensor(mag_input).unsqueeze(0).unsqueeze(0).float().to(self.device)

            # 4. Chạy Model (Inference)
            with torch.no_grad():
                outputs = self.model(inputs)

            # 5. Hậu xử lý (Post-process)
            # Lấy kết quả ra khỏi GPU và chuyển về numpy
            cleaned_mag = outputs.squeeze().cpu().numpy() # [256, Time]
            
            # Pad lại dòng tần số thứ 257 (thường là 0 hoặc copy dòng cuối) để iSTFT hoạt động
            # Chúng ta tạo mảng zeros [1, Time] và nối vào đuôi
            pad_row = np.zeros((1, cleaned_mag.shape[1]))
            cleaned_mag = np.vstack((cleaned_mag, pad_row))

            # 6. Tái tạo âm thanh (Reconstruct)
            # Kết hợp biên độ đã lọc (cleaned_mag) với pha gốc (phase) - Đây là kỹ thuật phổ biến
            cleaned_stft = cleaned_mag * np.exp(1j * phase)
            
            # Biến đổi ngược (iSTFT)
            cleaned_audio = librosa.istft(cleaned_stft, hop_length=256)

            # 7. Lưu file
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            sf.write(output_path, cleaned_audio, sr)
            
            return True, "Đã lọc nhiễu thành công!"

        except Exception as e:
            print(f"Lỗi xử lý: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)