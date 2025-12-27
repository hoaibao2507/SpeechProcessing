import threading
import queue
import os
import sounddevice as sd
import soundfile as sf

class AudioRecorder:
    def __init__(self, filename="recording.wav", samplerate=48000, channels=2):
        self.filename = filename
        self.samplerate = samplerate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = False
        self.file_exists = False
        self.thread = None

    # Callback nhận dữ liệu từ microphone (chạy ngầm)
    def _callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        self.q.put(indata.copy())

    # Hàm thực thi ghi âm trong luồng riêng
    def _record_thread(self):
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            
            with sf.SoundFile(self.filename, mode='w',
                              samplerate=self.samplerate,
                              channels=self.channels) as file:
                with sd.InputStream(samplerate=self.samplerate,
                                    channels=self.channels,
                                    callback=self._callback):
                    while self.recording:
                        data = self.q.get()
                        if data is None:
                            break
                        file.write(data)
            self.file_exists = True
        except Exception as e:
            print(f"Lỗi ghi âm: {e}")

    def start_recording(self):
        if self.recording:
            return False
        
        self.recording = True
        # Xóa queue cũ nếu có
        with self.q.mutex:
            self.q.queue.clear()
            
        self.thread = threading.Thread(target=self._record_thread, daemon=True)
        self.thread.start()
        return True

    def stop_recording(self):
        if not self.recording:
            return False
        
        self.recording = False
        self.q.put(None) # Tín hiệu dừng vòng lặp
        if self.thread:
            self.thread.join() # Đợi luồng kết thúc
        return True

    def play_recording(self):
        if not os.path.exists(self.filename):
            raise FileNotFoundError("Chưa có file ghi âm nào.")
        
        data, fs = sf.read(self.filename, dtype='float32')
        sd.play(data, fs)
        sd.wait()