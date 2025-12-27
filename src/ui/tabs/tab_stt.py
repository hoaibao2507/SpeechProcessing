import tkinter as tk
import threading
from src.ui.widgets.recorder_widget import RecorderWidget

class STTTab(tk.Frame):
    def __init__(self, parent, engine):
        """
        :param parent: Tab cha (Notebook)
        :param engine: Instance của STTEngine
        """
        super().__init__(parent)
        self.engine = engine
        self.output_file = "recordings/stt_input.wav"
        
        self._setup_ui()

    def _setup_ui(self):
        # 1. Tiêu đề
        lbl_intro = tk.Label(self, text="Ghi âm và chuyển thành văn bản", font=("Arial", 12, "bold"))
        lbl_intro.pack(pady=10)
        
        # 2. Widget Ghi âm
        self.recorder = RecorderWidget(self, output_file=self.output_file)
        self.recorder.pack(pady=10)

        # 3. Nút Chuyển đổi
        self.btn_convert = tk.Button(self, text="⬇ Chuyển đổi sang Văn bản ⬇", 
                                     font=("Arial", 10), bg="#cceeff",
                                     command=self.on_stt_convert)
        self.btn_convert.pack(pady=10)

        # 4. Hiển thị kết quả
        lbl_res = tk.Label(self, text="Kết quả nhận diện:")
        lbl_res.pack(anchor="w", padx=20)
        
        self.txt_result = tk.Text(self, height=8, width=70, font=("Consolas", 10))
        self.txt_result.pack(pady=5, padx=20)

    def on_stt_convert(self):
        self.btn_convert.config(state=tk.DISABLED, text="Đang xử lý...")
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, "⏳ Đang phân tích âm thanh, vui lòng đợi...\n")
        
        threading.Thread(target=self._run_stt_thread).start()

    def _run_stt_thread(self):
        result_text = self.engine.predict(self.output_file)
        self.after(0, lambda: self._update_ui_result(result_text))

    def _update_ui_result(self, text):
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, text)
        self.btn_convert.config(state=tk.NORMAL, text="⬇ Chuyển đổi sang Văn bản ⬇")