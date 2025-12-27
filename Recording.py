import tkinter as tk
from tkinter import messagebox as msb
import threading
import queue
import os
import sounddevice as sd
import soundfile as sf

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Recording")
        self.geometry("700x350")

        # Attributes
        self.q = queue.Queue()
        self.recording = False
        self.thread = None
        self.file_exists = False
        self.filename = "recording.wav"
        self.samplerate = 48000
        self.channels = 2

        # Build UI
        self._build_ui()

    def _build_ui(self):
        cvs_figure = tk.Canvas(self, width=600, height=300, relief=tk.SUNKEN, border=1)
        lblf_upper = tk.LabelFrame(self)
        lblf_lower = tk.LabelFrame(self)

        # Control buttons
        self.btn_start = tk.Button(lblf_upper, text="Record", width=8, command=self.start_recording)
        self.btn_stop = tk.Button(lblf_upper, text="Stop", width=8, command=self.stop_recording, state=tk.DISABLED)
        self.btn_play = tk.Button(lblf_upper, text="Play", width=8, command=self.play_recording)

        self.btn_start.grid(row=0, padx=5, pady=5)
        self.btn_stop.grid(row=1, padx=5, pady=5)
        self.btn_play.grid(row=2, padx=5, pady=5)

        # Navigation buttons (for UI only)
        btn_view = tk.Button(lblf_lower, text="View", width=8, command=lambda: msb.showinfo("Info", "View clicked"))
        btn_next = tk.Button(lblf_lower, text="Next", width=8, command=lambda: msb.showinfo("Info", "Next clicked"))
        btn_prev = tk.Button(lblf_lower, text="Prev", width=8, command=lambda: msb.showinfo("Info", "Prev clicked"))

        btn_view.grid(row=0, padx=5, pady=5)
        btn_next.grid(row=1, padx=5, pady=5)
        btn_prev.grid(row=2, padx=5, pady=5)

        cvs_figure.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
        lblf_upper.grid(row=0, column=1, padx=5, pady=6, sticky=tk.N)
        lblf_lower.grid(row=1, column=1, padx=5, pady=6, sticky=tk.S)

    # Callback receives data from microphone
    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    # Thread for recording
    def _record(self):
        try:
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
            self.after(0, lambda: msb.showerror("Error", f"Recording error:\n{e}"))
        finally:
            self.after(0, self._on_recording_finished)

    # Start recording
    def start_recording(self):
        if self.recording:
            msb.showwarning("Warning", "Recording is already in progress!")
            return

        try:
            msb.showinfo("Recording", "Recording started...")
            self.recording = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self._record, daemon=True)
            self.thread.start()
        except Exception as e:
            msb.showerror("Error", f"Failed to start recording:\n{e}")

    # Stop recording
    def stop_recording(self):
        if not self.recording:
            return

        self.recording = False
        self.q.put(None)
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def _on_recording_finished(self):
        msb.showinfo("Done", "Recording finished. You can now play the file.")

    # Play recorded file
    def play_recording(self):
        if not os.path.exists(self.filename):
            msb.showwarning("No file", "No recording found to play.")
            return
        try:
            data, fs = sf.read(self.filename, dtype='float32')
            sd.play(data, fs)
            sd.wait()
            msb.showinfo("Playback", "Playback finished.")
        except Exception as e:
            msb.showerror("Error", f"Playback error:\n{e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
