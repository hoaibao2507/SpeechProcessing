import os
import torch
import librosa
import json
import numpy as np
from transformers import AutoProcessor, ASTForAudioClassification

class AnimalEngine:
    def __init__(self, model_path="models/My_AST_Model_96acc-20251227T152517Z-1-001/My_AST_Model_96acc"):
        """
        Khởi tạo model AST (Audio Spectrogram Transformer) để nhận diện âm thanh động vật.
        :param model_path: Đường dẫn đến thư mục chứa model AST
        """
        self.model_path = model_path
        self.model = None
        self.processor = None
        self.label_map = None
        
        # Chọn thiết bị (GPU ưu tiên)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("--- Đang khởi tạo Animal Engine trên GPU (NVIDIA) ---")
        else:
            self.device = torch.device("cpu")
            print("--- Đang khởi tạo Animal Engine trên CPU ---")
        
        self._load_model()

    def _load_model(self):
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Không tìm thấy thư mục model tại: {self.model_path}")

            print(f"Đang load model AST từ: {self.model_path}")

            # Load processor
            self.processor = AutoProcessor.from_pretrained(self.model_path)
            
            # Load model
            self.model = ASTForAudioClassification.from_pretrained(self.model_path)
            self.model.to(self.device)
            self.model.eval()
            
            # Load label map
            label_map_path = os.path.join(self.model_path, "label_map.json")
            if os.path.exists(label_map_path):
                with open(label_map_path, 'r', encoding='utf-8') as f:
                    self.label_map = json.load(f)
            else:
                # Fallback: sử dụng id2label từ config
                if hasattr(self.model.config, 'id2label'):
                    self.label_map = {"id2label": {str(k): v for k, v in self.model.config.id2label.items()}}
                else:
                    print("Cảnh báo: Không tìm thấy label_map.json")
                    self.label_map = None
            
            print("Model Animal Recognition đã sẵn sàng!")
            
        except Exception as e:
            print(f"Lỗi load model Animal: {e}")
            import traceback
            traceback.print_exc()
            self.model = None

    def predict(self, audio_path, top_k=5):
        """
        Nhận diện loại âm thanh từ file audio.
        :param audio_path: Đường dẫn file âm thanh (.wav, .mp3)
        :param top_k: Số lượng kết quả top để trả về (mặc định 5)
        :return: Dictionary chứa kết quả nhận diện
        """
        if self.model is None or self.processor is None:
            return {
                "success": False,
                "error": "Model chưa được khởi tạo thành công."
            }

        if not os.path.exists(audio_path):
            return {
                "success": False,
                "error": "Không tìm thấy file âm thanh."
            }

        try:
            print(f"Đang xử lý file: {audio_path}")
            
            # Load audio file (AST thường yêu cầu 16kHz)
            audio_array, sampling_rate = librosa.load(audio_path, sr=16000)
            
            # Preprocess audio
            inputs = self.processor(audio_array, sampling_rate=sampling_rate, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Lấy top-k predictions
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            top_probs, top_indices = torch.topk(probabilities, k=min(top_k, probabilities.size(1)), dim=-1)
            
            # Chuyển đổi kết quả
            results = []
            for i in range(top_probs.size(1)):
                idx = top_indices[0][i].item()
                prob = top_probs[0][i].item()
                
                # Lấy label từ label_map hoặc config
                if self.label_map and "id2label" in self.label_map:
                    label = self.label_map["id2label"].get(str(idx), f"class_{idx}")
                elif hasattr(self.model.config, 'id2label'):
                    label = self.model.config.id2label.get(idx, f"class_{idx}")
                else:
                    label = f"class_{idx}"
                
                results.append({
                    "label": label,
                    "probability": prob,
                    "confidence": f"{prob * 100:.2f}%"
                })
            
            # Tìm kết quả có confidence cao nhất
            top_result = results[0] if results else None
            
            return {
                "success": True,
                "top_result": top_result,
                "top_k": results,
                "is_animal": self._is_animal_label(top_result["label"]) if top_result else False
            }

        except Exception as e:
            print(f"Lỗi dự đoán: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Có lỗi xảy ra khi xử lý: {str(e)}"
            }

    def _is_animal_label(self, label):
        """
        Kiểm tra xem label có phải là động vật không.
        """
        animal_labels = [
            "dog", "cat", "sheep", "cow", "pig", "hen", "rooster", 
            "frog", "crow", "chirping_birds", "crickets", "insects"
        ]
        return label.lower() in animal_labels

