"""
Utility để vẽ waveform của audio file sử dụng WaveSurfer.js

KIẾN TRÚC:
-----------
Python (Streamlit Backend)
   └── Ghi / đọc audio (soundfile, sounddevice)
        ↓
   └── Encode base64
        ↓
Frontend (WaveSurfer.js - JavaScript)
   └── Hiển thị waveform + phát audio đồng bộ

LƯU Ý:
- WaveSurfer.js là thư viện JavaScript, KHÔNG phải Python
- Phải nhúng qua HTML + JS trong Streamlit
- Streamlit hỗ trợ sẵn bằng: st.components.v1.html(...)
- Không cần server riêng, không cần React/Vue, không cần build frontend
"""
import base64
import os


def get_wavesurfer_html(audio_path, wave_color='#1e90ff', progress_color='#0066cc', height=120, bar_width=2):
    """
    Tạo HTML với WaveSurfer.js để hiển thị waveform tương tác.
    
    :param audio_path: Đường dẫn đến file audio
    :param wave_color: Màu của sóng âm
    :param progress_color: Màu của thanh progress
    :param height: Chiều cao của waveform
    :param bar_width: Độ rộng của thanh sóng
    :return: HTML string để hiển thị trong Streamlit
    """
    try:
        if not os.path.exists(audio_path):
            return f'<div style="padding: 20px; text-align: center; color: red;">File không tồn tại: {audio_path}</div>'
        
        # Đọc file audio và encode base64
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        
        audio_b64 = base64.b64encode(audio_bytes).decode()
        
        # Xác định MIME type dựa trên extension
        ext = os.path.splitext(audio_path)[1].lower()
        mime_types = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.m4a': 'audio/mp4'
        }
        mime_type = mime_types.get(ext, 'audio/wav')
        
        # Tạo unique ID để tránh conflict khi có nhiều waveform
        import hashlib
        waveform_id = hashlib.md5(audio_path.encode()).hexdigest()[:8]
        
        html = f"""
        <script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
        
        <div style="margin: 10px 0;">
            <div id="waveform-{waveform_id}" style="margin-bottom: 10px;"></div>
            <div style="text-align: center;">
                <button id="play-pause-{waveform_id}" style="padding: 8px 20px; margin: 0 5px; background: #1e90ff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ▶️ Play
                </button>
                <button id="stop-{waveform_id}" style="padding: 8px 20px; margin: 0 5px; background: #666; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ⏹️ Stop
                </button>
                <span id="time-{waveform_id}" style="margin-left: 15px; color: #666; font-size: 14px;">0:00 / 0:00</span>
            </div>
        </div>
        
        <script>
        (function() {{
            var wavesurfer = WaveSurfer.create({{
                container: '#waveform-{waveform_id}',
                waveColor: '{wave_color}',
                progressColor: '{progress_color}',
                cursorColor: '#333',
                barWidth: {bar_width},
                barRadius: 3,
                height: {height},
                normalize: true,
                backend: 'WebAudio',
                mediaControls: false
            }});
            
            wavesurfer.load("data:{mime_type};base64,{audio_b64}");
            
            var playPauseBtn = document.getElementById('play-pause-{waveform_id}');
            var stopBtn = document.getElementById('stop-{waveform_id}');
            var timeDisplay = document.getElementById('time-{waveform_id}');
            
            function formatTime(seconds) {{
                var mins = Math.floor(seconds / 60);
                var secs = Math.floor(seconds % 60);
                return mins + ':' + (secs < 10 ? '0' : '') + secs;
            }}
            
            wavesurfer.on('ready', function() {{
                var duration = wavesurfer.getDuration();
                timeDisplay.textContent = '0:00 / ' + formatTime(duration);
            }});
            
            wavesurfer.on('play', function() {{
                playPauseBtn.textContent = '⏸️ Pause';
            }});
            
            wavesurfer.on('pause', function() {{
                playPauseBtn.textContent = '▶️ Play';
            }});
            
            wavesurfer.on('finish', function() {{
                playPauseBtn.textContent = '▶️ Play';
            }});
            
            wavesurfer.on('timeupdate', function() {{
                var current = wavesurfer.getCurrentTime();
                var duration = wavesurfer.getDuration();
                timeDisplay.textContent = formatTime(current) + ' / ' + formatTime(duration);
            }});
            
            playPauseBtn.addEventListener('click', function() {{
                wavesurfer.playPause();
            }});
            
            stopBtn.addEventListener('click', function() {{
                wavesurfer.stop();
                playPauseBtn.textContent = '▶️ Play';
            }});
        }})();
        </script>
        """
        
        return html
    
    except Exception as e:
        return f'<div style="padding: 20px; text-align: center; color: red;">Lỗi khi tải waveform: {str(e)}</div>'


def get_wavesurfer_comparison_html(audio_path1, audio_path2, title1="Audio gốc", title2="Audio đã xử lý", 
                                   wave_color1='#ff7f0e', progress_color1='#cc6600',
                                   wave_color2='#2ca02c', progress_color2='#1e7e1e', height=100):
    """
    Tạo HTML với 2 WaveSurfer để so sánh 2 file audio.
    
    :param audio_path1: Đường dẫn đến file audio đầu tiên
    :param audio_path2: Đường dẫn đến file audio thứ hai
    :param title1: Tiêu đề cho audio đầu tiên
    :param title2: Tiêu đề cho audio thứ hai
    :param wave_color1: Màu sóng cho audio 1
    :param progress_color1: Màu progress cho audio 1
    :param wave_color2: Màu sóng cho audio 2
    :param progress_color2: Màu progress cho audio 2
    :param height: Chiều cao của mỗi waveform
    :return: HTML string
    """
    try:
        import hashlib
        id1 = hashlib.md5(audio_path1.encode()).hexdigest()[:8]
        id2 = hashlib.md5(audio_path2.encode()).hexdigest()[:8]
        
        # Đọc và encode cả 2 file
        with open(audio_path1, "rb") as f:
            audio1_b64 = base64.b64encode(f.read()).decode()
        with open(audio_path2, "rb") as f:
            audio2_b64 = base64.b64encode(f.read()).decode()
        
        ext1 = os.path.splitext(audio_path1)[1].lower()
        ext2 = os.path.splitext(audio_path2)[1].lower()
        mime_types = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.m4a': 'audio/mp4'
        }
        mime1 = mime_types.get(ext1, 'audio/wav')
        mime2 = mime_types.get(ext2, 'audio/wav')
        
        html = f"""
        <script src="https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.min.js"></script>
        
        <div style="margin: 20px 0;">
            <h4 style="margin: 10px 0; color: #333;">{title1}</h4>
            <div id="waveform-{id1}" style="margin-bottom: 10px;"></div>
            <div style="text-align: center; margin-bottom: 20px;">
                <button id="play-pause-{id1}" style="padding: 8px 20px; margin: 0 5px; background: {wave_color1}; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ▶️ Play
                </button>
                <button id="stop-{id1}" style="padding: 8px 20px; margin: 0 5px; background: #666; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ⏹️ Stop
                </button>
                <span id="time-{id1}" style="margin-left: 15px; color: #666; font-size: 14px;">0:00 / 0:00</span>
            </div>
            
            <h4 style="margin: 10px 0; color: #333;">{title2}</h4>
            <div id="waveform-{id2}" style="margin-bottom: 10px;"></div>
            <div style="text-align: center;">
                <button id="play-pause-{id2}" style="padding: 8px 20px; margin: 0 5px; background: {wave_color2}; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ▶️ Play
                </button>
                <button id="stop-{id2}" style="padding: 8px 20px; margin: 0 5px; background: #666; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    ⏹️ Stop
                </button>
                <span id="time-{id2}" style="margin-left: 15px; color: #666; font-size: 14px;">0:00 / 0:00</span>
            </div>
        </div>
        
        <script>
        (function() {{
            function formatTime(seconds) {{
                var mins = Math.floor(seconds / 60);
                var secs = Math.floor(seconds % 60);
                return mins + ':' + (secs < 10 ? '0' : '') + secs;
            }}
            
            // Waveform 1
            var wavesurfer1 = WaveSurfer.create({{
                container: '#waveform-{id1}',
                waveColor: '{wave_color1}',
                progressColor: '{progress_color1}',
                cursorColor: '#333',
                barWidth: 2,
                barRadius: 3,
                height: {height},
                normalize: true
            }});
            
            wavesurfer1.load("data:{mime1};base64,{audio1_b64}");
            
            wavesurfer1.on('ready', function() {{
                var duration = wavesurfer1.getDuration();
                document.getElementById('time-{id1}').textContent = '0:00 / ' + formatTime(duration);
            }});
            
            wavesurfer1.on('play', function() {{
                document.getElementById('play-pause-{id1}').textContent = '⏸️ Pause';
            }});
            
            wavesurfer1.on('pause', function() {{
                document.getElementById('play-pause-{id1}').textContent = '▶️ Play';
            }});
            
            wavesurfer1.on('timeupdate', function() {{
                var current = wavesurfer1.getCurrentTime();
                var duration = wavesurfer1.getDuration();
                document.getElementById('time-{id1}').textContent = formatTime(current) + ' / ' + formatTime(duration);
            }});
            
            document.getElementById('play-pause-{id1}').addEventListener('click', function() {{
                wavesurfer1.playPause();
            }});
            
            document.getElementById('stop-{id1}').addEventListener('click', function() {{
                wavesurfer1.stop();
                document.getElementById('play-pause-{id1}').textContent = '▶️ Play';
            }});
            
            // Waveform 2
            var wavesurfer2 = WaveSurfer.create({{
                container: '#waveform-{id2}',
                waveColor: '{wave_color2}',
                progressColor: '{progress_color2}',
                cursorColor: '#333',
                barWidth: 2,
                barRadius: 3,
                height: {height},
                normalize: true
            }});
            
            wavesurfer2.load("data:{mime2};base64,{audio2_b64}");
            
            wavesurfer2.on('ready', function() {{
                var duration = wavesurfer2.getDuration();
                document.getElementById('time-{id2}').textContent = '0:00 / ' + formatTime(duration);
            }});
            
            wavesurfer2.on('play', function() {{
                document.getElementById('play-pause-{id2}').textContent = '⏸️ Pause';
            }});
            
            wavesurfer2.on('pause', function() {{
                document.getElementById('play-pause-{id2}').textContent = '▶️ Play';
            }});
            
            wavesurfer2.on('timeupdate', function() {{
                var current = wavesurfer2.getCurrentTime();
                var duration = wavesurfer2.getDuration();
                document.getElementById('time-{id2}').textContent = formatTime(current) + ' / ' + formatTime(duration);
            }});
            
            document.getElementById('play-pause-{id2}').addEventListener('click', function() {{
                wavesurfer2.playPause();
            }});
            
            document.getElementById('stop-{id2}').addEventListener('click', function() {{
                wavesurfer2.stop();
                document.getElementById('play-pause-{id2}').textContent = '▶️ Play';
            }});
        }})();
        </script>
        """
        
        return html
    
    except Exception as e:
        return f'<div style="padding: 20px; text-align: center; color: red;">Lỗi khi tải waveform: {str(e)}</div>'

