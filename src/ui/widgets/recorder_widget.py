import tkinter as tk
from tkinter import messagebox as msb
from src.utils.audio_helper import AudioRecorder # Import logic từ bước 1

class RecorderWidget(tk.Frame):
    def __init__(self, parent, output_file="recordings/output.wav"):
        super().__init__(parent)
        
        # Khởi tạo logic ghi âm
        self.recorder = AudioRecorder(filename=output_file)
        
        # UI Components
        self.lbl_status = tk.Label(self, text="Sẵn sàng", fg="blue")
        self.lbl_status.pack(pady=5)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()

        self.btn_start = tk.Button(self.btn_frame, text="Bắt đầu Ghi âm", command=self.on_start, bg="#dddddd")
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(self.btn_frame, text="Dừng", command=self.on_stop, state=tk.DISABLED, bg="#dddddd")
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_play = tk.Button(self.btn_frame, text="Nghe lại", command=self.on_play, state=tk.NORMAL)
        self.btn_play.pack(side=tk.LEFT, padx=5)

    def on_start(self):
        try:
            self.recorder.start_recording()
            self.lbl_status.config(text="Đang ghi âm...", fg="red")
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_play.config(state=tk.DISABLED)
        except Exception as e:
            msb.showerror("Lỗi", str(e))

    def on_stop(self):
        self.recorder.stop_recording()
        self.lbl_status.config(text="Đã ghi xong", fg="green")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_play.config(state=tk.NORMAL)

    def on_play(self):
        self.lbl_status.config(text="Đang phát lại...", fg="blue")
        self.update() # Cập nhật giao diện ngay lập tức
        try:
            self.recorder.play_recording()
            self.lbl_status.config(text="Phát xong", fg="green")
        except Exception as e:
            msb.showerror("Lỗi", f"Không thể phát: {e}")
            self.lbl_status.config(text="Lỗi phát", fg="red")