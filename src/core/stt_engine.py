import os
import torch
import librosa
import numpy as np
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration

class STTEngine:
    def __init__(self, model_path="models/speech_to_text/speech-to-text-vn/whisper-vivos-final"):
        """
        Khởi tạo model Whisper STT.
        :param model_path: Đường dẫn đến thư mục chứa model đã tải về từ Drive.
        """
        self.model_path = model_path
        self.transcriber = None
        
        if torch.cuda.is_available():
            self.device_str = "cuda" # Dùng cho model.to()
            self.device_id = 0       # Dùng cho pipeline()
            print("--- Đang khởi tạo STT Engine trên GPU (NVIDIA) ---")
        else:
            self.device_str = "cpu"  # Dùng cho model.to()
            self.device_id = -1      # Dùng cho pipeline()
            print("--- Đang khởi tạo STT Engine trên CPU ---")
        self._load_model()

    def _load_model(self):
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Không tìm thấy thư mục model tại: {self.model_path}")

            print(f"Đang load model từ: {self.model_path}")

            # Load model thủ công để kiểm soát tốt hơn
            # Bước 1: Load Processor
            self.processor = WhisperProcessor.from_pretrained(self.model_path)
            
            # Bước 2: Load Model và chuyển sang thiết bị (SỬA LỖI TẠI ĐÂY)
            # Dùng self.device_str ("cpu" hoặc "cuda") thay vì số -1
            self.model = WhisperForConditionalGeneration.from_pretrained(self.model_path).to(self.device_str)
            
            # Bước 3: Tạo pipeline
            self.transcriber = pipeline(
                "automatic-speech-recognition",
                model=self.model,
                tokenizer=self.processor.tokenizer,
                feature_extractor=self.processor.feature_extractor,
                device=self.device_id # Pipeline thì vẫn dùng số (-1 hoặc 0)
            )
            
            print("Model STT đã sẵn sàng!")
            
        except Exception as e:
            print(f"Lỗi load model STT: {e}")
            self.transcriber = None

    def predict(self, audio_path):
        """
        Nhận diện văn bản từ file âm thanh.
        :param audio_path: Đường dẫn file âm thanh (.wav, .mp3)
        :return: Chuỗi văn bản kết quả
        """
        if self.transcriber is None:
            return "Lỗi: Model chưa được khởi tạo thành công."

        if not os.path.exists(audio_path):
            return "Lỗi: Không tìm thấy file âm thanh."

        try:
            print(f"Đang xử lý file: {audio_path}")
            
            # --- BƯỚC XỬ LÝ ÂM THANH (Giống code Colab của bạn) ---
            # Load file và ép về 16kHz (yêu cầu của Whisper)
            audio_array, sampling_rate = librosa.load(audio_path, sr=16000)

            # --- BƯỚC DỰ ĐOÁN ---
            # generate_kwargs={"language": "vietnamese"} giúp AI định hướng tốt hơn
            result = self.transcriber(
                audio_array, 
                generate_kwargs={"language": "vietnamese"}
            )
            
            text = result["text"]
            return text

        except Exception as e:
            print(f"Lỗi dự đoán: {e}")
            return f"Có lỗi xảy ra khi xử lý: {str(e)}"

# Đoạn code dưới đây chỉ chạy khi bạn test file này trực tiếp
if __name__ == "__main__":
    # Test thử
    # Bạn nhớ sửa đường dẫn này trỏ đúng folder model bạn tải về
    engine = STTEngine(model_path="../../models/stt_vn/whisper-vivos-final") 
    
    # Test với 1 file mẫu
    test_audio = "../../recordings/test.wav"
    if os.path.exists(test_audio):
        print("Kết quả:", engine.predict(test_audio))