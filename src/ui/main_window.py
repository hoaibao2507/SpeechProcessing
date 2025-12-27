import tkinter as tk
from tkinter import ttk
import threading
from src.core.stt_engine import STTEngine
from src.core.denoise_engine import DenoiseEngine
from src.ui.tabs.tab_stt import STTTab        
from src.ui.tabs.tab_denoise import DenoiseTab

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đồ án Xử lý Tiếng nói")
        self.geometry("800x650") # Tăng chiều cao một chút để đủ chỗ hiển thị

        # --- KHỞI TẠO ENGINE (QUAN TRỌNG) ---
        # Đường dẫn trỏ đúng vào folder chứa các file model
        # models/stt_vn/speech-to-text
        print("Đang khởi tạo model...")
        self.stt_engine = STTEngine(model_path="models/speech_to_text/speech-to-text-vn/whisper-vivos-final")

        print("Đang khởi tạo Denoise Engine...")
        self.denoise_engine = DenoiseEngine(model_path="models/denoiser/model_SE_v1.pth")

        # Tạo Tab Control
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- TAB 1: Speech to Text ---
        self.tab1 = STTTab(self.notebook, engine=self.stt_engine)
        self.notebook.add(self.tab1, text='Chuyển đổi giọng nói sang văn bản')

        # --- TAB 2 & 3 ---
        self.tab2 = DenoiseTab(self.notebook, engine=self.denoise_engine)
        self.notebook.add(self.tab2, text='Lọc nhiễu')
        
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Nhận diện Chó/Mèo')

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()