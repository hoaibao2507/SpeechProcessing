import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
from src.ui.widgets.recorder_widget import RecorderWidget

class AnimalTab(tk.Frame):
    def __init__(self, parent, engine):
        """
        :param parent: Tab cha (Notebook)
        :param engine: Instance của AnimalEngine
        """
        super().__init__(parent)
        self.engine = engine
        self.output_file = "recordings/animal_input.wav"
        self.uploaded_file = None  # File được upload
        
        self._setup_ui()

    def _setup_ui(self):
        # 1. Tiêu đề
        lbl_intro = tk.Label(self, text="Nhận diện âm thanh động vật và các loại âm thanh", 
                            font=("Arial", 12, "bold"))
        lbl_intro.pack(pady=10)
        
        lbl_hint = tk.Label(self, text="Ghi âm hoặc upload file âm thanh để nhận diện", 
                          fg="gray", font=("Arial", 9))
        lbl_hint.pack(pady=5)
        
        # 2. Frame chứa 2 phương thức: Ghi âm và Upload file
        frame_input = tk.LabelFrame(self, text="Bước 1: Chọn nguồn âm thanh", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_input.pack(pady=10, padx=10, fill="x")
        
        # Tạo 2 cột
        frame_left = tk.Frame(frame_input)
        frame_left.pack(side=tk.LEFT, fill="both", expand=True, padx=5)
        
        frame_right = tk.Frame(frame_input)
        frame_right.pack(side=tk.RIGHT, fill="both", expand=True, padx=5)
        
        # Cột trái: Ghi âm
        lbl_record = tk.Label(frame_left, text="Ghi âm", font=("Arial", 9, "bold"))
        lbl_record.pack(pady=5)
        self.recorder = RecorderWidget(frame_left, output_file=self.output_file)
        self.recorder.pack()
        
        # Cột phải: Upload file
        lbl_upload = tk.Label(frame_right, text="Upload file", font=("Arial", 9, "bold"))
        lbl_upload.pack(pady=5)
        
        btn_frame = tk.Frame(frame_right)
        btn_frame.pack(pady=5)
        
        self.btn_upload = tk.Button(btn_frame, text="Chọn file", 
                                    font=("Arial", 9), bg="#e0e0e0",
                                    command=self.on_upload_file)
        self.btn_upload.pack(side=tk.LEFT, padx=2)
        
        self.btn_clear = tk.Button(btn_frame, text="Xóa", 
                                   font=("Arial", 9), bg="#ffcccc",
                                   command=self.on_clear_file, state=tk.DISABLED)
        self.btn_clear.pack(side=tk.LEFT, padx=2)
        
        self.lbl_file_name = tk.Label(frame_right, text="Chưa chọn file", 
                                      fg="gray", font=("Arial", 8), wraplength=200)
        self.lbl_file_name.pack(pady=5)

        # 3. Nút Nhận diện
        self.btn_recognize = tk.Button(self, text="NHẬN DIỆN ÂM THANH", 
                                      font=("Arial", 11, "bold"), bg="#ffcc80", fg="black",
                                      height=2,
                                      command=self.on_recognize)
        self.btn_recognize.pack(pady=15, fill="x", padx=50)

        # 4. Hiển thị kết quả
        frame_result = tk.LabelFrame(self, text="Kết quả nhận diện", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame_result.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Kết quả chính
        self.lbl_main_result = tk.Label(frame_result, text="Chưa có kết quả", 
                                        font=("Arial", 14, "bold"), fg="blue")
        self.lbl_main_result.pack(pady=10)
        
        # Confidence
        self.lbl_confidence = tk.Label(frame_result, text="", font=("Arial", 11), fg="green")
        self.lbl_confidence.pack(pady=5)
        
        # Top K results
        lbl_topk = tk.Label(frame_result, text="Top 5 kết quả:", font=("Arial", 10, "bold"))
        lbl_topk.pack(anchor="w", padx=10, pady=(15, 5))
        
        # Frame chứa Text và Scrollbar
        text_frame = tk.Frame(frame_result)
        text_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Scrollbar cho Text widget
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.txt_topk = tk.Text(text_frame, height=8, width=60, font=("Consolas", 9),
                                yscrollcommand=scrollbar.set)
        self.txt_topk.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.txt_topk.yview)

    def on_upload_file(self):
        """Mở dialog để chọn file âm thanh"""
        file_path = filedialog.askopenfilename(
            title="Chọn file âm thanh",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.uploaded_file = file_path
            file_name = os.path.basename(file_path)
            self.lbl_file_name.config(text=f"[OK] {file_name}", fg="green")
            self.btn_clear.config(state=tk.NORMAL)
            messagebox.showinfo("Thành công", f"Đã chọn file: {file_name}")

    def on_clear_file(self):
        """Xóa file đã upload"""
        self.uploaded_file = None
        self.lbl_file_name.config(text="Chưa chọn file", fg="gray")
        self.btn_clear.config(state=tk.DISABLED)

    def on_recognize(self):
        # Xác định file nào sẽ được sử dụng (ưu tiên file upload)
        audio_file = None
        
        if self.uploaded_file and os.path.exists(self.uploaded_file):
            audio_file = self.uploaded_file
        elif os.path.exists(self.output_file):
            audio_file = self.output_file
        else:
            messagebox.showwarning("Thiếu file", "Vui lòng ghi âm hoặc upload file âm thanh trước!")
            return
        
        # Khóa nút và cập nhật UI
        self.btn_recognize.config(state=tk.DISABLED, text="Đang nhận diện...")
        self.lbl_main_result.config(text="Đang phân tích âm thanh...", fg="orange")
        self.lbl_confidence.config(text="")
        self.txt_topk.delete("1.0", tk.END)
        self.txt_topk.insert(tk.END, "Đang xử lý...\n")
        
        # Chạy trong thread riêng
        threading.Thread(target=self._run_recognize_thread, args=(audio_file,)).start()

    def _run_recognize_thread(self, audio_file):
        # Gọi Engine để nhận diện
        result = self.engine.predict(audio_file, top_k=5)
        
        # Cập nhật UI sau khi xong
        self.after(0, lambda: self._update_ui_result(result))

    def _update_ui_result(self, result):
        # Mở lại nút
        self.btn_recognize.config(state=tk.NORMAL, text="NHẬN DIỆN ÂM THANH")
        
        if not result.get("success", False):
            error_msg = result.get("error", "Có lỗi xảy ra")
            self.lbl_main_result.config(text=f"Lỗi: {error_msg}", fg="red")
            self.lbl_confidence.config(text="")
            self.txt_topk.delete("1.0", tk.END)
            messagebox.showerror("Lỗi", error_msg)
            return
        
        # Hiển thị kết quả chính
        top_result = result.get("top_result")
        if top_result:
            label = top_result["label"]
            confidence = top_result["confidence"]
            
            # Chuyển đổi label thành tiếng Việt (nếu là động vật)
            label_vn = self._translate_label(label)
            
            # Kiểm tra xem có phải động vật không
            is_animal = result.get("is_animal", False)
            prefix = "[Động vật]" if is_animal else "[Âm thanh]"
            
            self.lbl_main_result.config(
                text=f"{prefix} {label_vn}", 
                fg="green" if is_animal else "blue"
            )
            self.lbl_confidence.config(text=f"Độ tin cậy: {confidence}")
        
        # Hiển thị top K results
        top_k = result.get("top_k", [])
        self.txt_topk.delete("1.0", tk.END)
        
        if top_k:
            for i, item in enumerate(top_k, 1):
                label = item["label"]
                label_vn = self._translate_label(label)
                confidence = item["confidence"]
                is_animal = self.engine._is_animal_label(label)
                prefix = "[Động vật]" if is_animal else "[Âm thanh]"
                
                self.txt_topk.insert(tk.END, f"{i}. {prefix} {label_vn} ({label})\n")
                self.txt_topk.insert(tk.END, f"   Độ tin cậy: {confidence}\n\n")
        else:
            self.txt_topk.insert(tk.END, "Không có kết quả")

    def _translate_label(self, label):
        """
        Chuyển đổi label tiếng Anh sang tiếng Việt.
        """
        translations = {
            "dog": "Chó",
            "cat": "Mèo",
            "sheep": "Cừu",
            "cow": "Bò",
            "pig": "Lợn",
            "hen": "Gà mái",
            "rooster": "Gà trống",
            "frog": "Ếch",
            "crow": "Quạ",
            "chirping_birds": "Chim hót",
            "crickets": "Dế",
            "insects": "Côn trùng",
            "vacuum_cleaner": "Máy hút bụi",
            "thunderstorm": "Sấm sét",
            "airplane": "Máy bay",
            "train": "Tàu hỏa",
            "car_horn": "Còi xe",
            "rain": "Mưa",
            "wind": "Gió",
            "footsteps": "Tiếng bước chân",
            "laughing": "Tiếng cười",
            "crying_baby": "Trẻ em khóc",
            "coughing": "Ho",
            "sneezing": "Hắt hơi",
            "snoring": "Ngáy",
            "breathing": "Thở",
            "clock_tick": "Tiếng đồng hồ",
            "clock_alarm": "Báo thức",
            "door_wood_knock": "Gõ cửa",
            "door_wood_creaks": "Cửa kêu cót két",
            "can_opening": "Mở lon",
            "washing_machine": "Máy giặt",
            "toilet_flush": "Xả nước toilet",
            "brushing_teeth": "Đánh răng",
            "drinking_sipping": "Uống nước",
            "keyboard_typing": "Gõ bàn phím",
            "mouse_click": "Click chuột",
            "fireworks": "Pháo hoa",
            "chainsaw": "Cưa máy",
            "helicopter": "Trực thăng",
            "engine": "Động cơ",
            "siren": "Còi báo động",
            "church_bells": "Chuông nhà thờ",
            "clapping": "Vỗ tay",
            "glass_breaking": "Vỡ kính",
            "hand_saw": "Cưa tay",
            "crackling_fire": "Lửa cháy",
            "pouring_water": "Đổ nước",
            "water_drops": "Giọt nước",
            "sea_waves": "Sóng biển",
            "crickets": "Dế",
            "chirping_birds": "Chim hót",
        }
        
        # Chuyển đổi snake_case thành tiếng Việt
        return translations.get(label.lower(), label.replace("_", " ").title())

