import tkinter as tk
from tkinter import messagebox
import threading
import os
import sounddevice as sd
import soundfile as sf
from src.ui.widgets.recorder_widget import RecorderWidget

class DenoiseTab(tk.Frame):
    def __init__(self, parent, engine):
        """
        :param parent: Tab cha (Notebook)
        :param engine: Instance của DenoiseEngine được truyền từ MainWindow
        """
        super().__init__(parent)
        self.engine = engine
        
        # Định nghĩa đường dẫn file
        # Input: File ghi âm có nhiễu
        self.input_file = "recordings/denoise_input.wav" 
        # Output: File sau khi model đã làm sạch
        self.output_file = "recordings/denoise_output.wav"

        self._setup_ui()

    def _setup_ui(self):
        # --- PHẦN 1: GHI ÂM ĐẦU VÀO ---
        frame_input = tk.LabelFrame(self, text="Bước 1: Ghi âm (Môi trường ồn)", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_input.pack(pady=10, padx=10, fill="x")
        
        lbl_hint = tk.Label(frame_input, text="Hãy bật quạt hoặc tạo tiếng ồn nền, sau đó ghi âm câu nói.", fg="gray")
        lbl_hint.pack(pady=5)

        # Sử dụng lại Widget ghi âm đã viết, lưu vào input_file
        self.recorder = RecorderWidget(frame_input, output_file=self.input_file)
        self.recorder.pack()

        # --- PHẦN 2: NÚT XỬ LÝ ---
        self.btn_process = tk.Button(self, text="CHẠY KHỬ NHIỄU (AI)", 
                                     font=("Arial", 11, "bold"), bg="#ffcc80", fg="black",
                                     height=2,
                                     command=self.on_process)
        self.btn_process.pack(pady=15, fill="x", padx=50)

        # --- PHẦN 3: KẾT QUẢ ---
        frame_output = tk.LabelFrame(self, text="Bước 2: Kết quả sau xử lý", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_output.pack(pady=10, padx=10, fill="x")

        self.lbl_status = tk.Label(frame_output, text="Trạng thái: Chưa xử lý", fg="blue", font=("Arial", 10))
        self.lbl_status.pack(pady=5)

        # Nút nghe lại file sạch
        self.btn_play_clean = tk.Button(frame_output, text="Nghe giọng đã lọc nhiễu", 
                                        font=("Arial", 10), bg="#99ff99",
                                        state=tk.DISABLED, command=self.play_output)
        self.btn_play_clean.pack(pady=10)

    def on_process(self):
        # Kiểm tra xem đã ghi âm chưa
        if not os.path.exists(self.input_file):
            messagebox.showwarning("Thiếu file", "Vui lòng ghi âm ở Bước 1 trước!")
            return

        # Khóa nút bấm để tránh bấm nhiều lần
        self.btn_process.config(state=tk.DISABLED, text="Đang xử lý... (Vui lòng đợi)")
        self.lbl_status.config(text="AI đang tách tiếng ồn...", fg="red")
        
        # Chạy xử lý trong luồng riêng (Thread) để không đơ ứng dụng
        threading.Thread(target=self._run_process_thread).start()

    def _run_process_thread(self):
        # Gọi Engine xử lý (Hàm này chạy mất vài giây)
        success, message = self.engine.process_audio(self.input_file, self.output_file)
        
        # Cập nhật giao diện sau khi xong (Dùng self.after để an toàn với Tkinter)
        self.after(0, lambda: self._on_process_finished(success, message))

    def _on_process_finished(self, success, message):
        # Mở lại nút bấm
        self.btn_process.config(state=tk.NORMAL, text="CHẠY KHỬ NHIỄU (AI)")
        
        if success:
            self.lbl_status.config(text="Đã lọc xong! Hãy nghe thử bên dưới.", fg="green")
            self.btn_play_clean.config(state=tk.NORMAL) # Mở nút nghe
            messagebox.showinfo("Thành công", message)
        else:
            self.lbl_status.config(text=f"Lỗi: {message}", fg="red")
            messagebox.showerror("Lỗi", message)

    def play_output(self):
        try:
            if not os.path.exists(self.output_file):
                messagebox.showerror("Lỗi", "Không tìm thấy file kết quả.")
                return
            
            self.lbl_status.config(text="Đang phát...", fg="green")
            self.update() # Cập nhật UI ngay
            
            # Đọc và phát file
            data, fs = sf.read(self.output_file)
            sd.play(data, fs)
            sd.wait()
            
            self.lbl_status.config(text="Đã phát xong.", fg="green")
        except Exception as e:
            messagebox.showerror("Lỗi phát âm thanh", f"{e}")