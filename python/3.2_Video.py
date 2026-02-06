import os
import time
import pwd
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from fusion_hat.user_button import UserButton

# ----- Paths (works correctly even when using sudo) -----
sudo_user = os.getenv("SUDO_USER")
home = pwd.getpwnam(sudo_user).pw_dir if sudo_user else os.path.expanduser("~")
videos_dir = os.path.join(home, "Videos")
os.makedirs(videos_dir, exist_ok=True)

# ----- Camera / encoder -----
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (800, 600)}, controls={"FrameRate": 30}))
encoder = H264Encoder(bitrate=10_000_000)

is_recording = False
output = None
preview_started = False

def start_recording():
    """Start recording to a timestamped MP4 file."""
    global is_recording, output
    ts = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join(videos_dir, f"video_{ts}.mp4")
    output = FfmpegOutput(path)  # keep a reference while recording
    camera.start_recording(encoder, output)
    is_recording = True
    print(f"\nStart recording: {path}")

def stop_recording():
    """Stop recording safely."""
    global is_recording, output
    camera.stop_recording()
    is_recording = False
    output = None
    print("\nStop recording.")

def toggle():
    """USR button callback: toggle start/stop."""
    if not is_recording:
        start_recording()
    else:
        stop_recording()

# ----- Button -----
UserButton().set_on_click(toggle)

# ----- Preview (only if a GUI display is available) -----
if os.getenv("DISPLAY"):
    try:
        camera.start_preview(Preview.QT)
        preview_started = True
    except Exception:
        preview_started = False  # continue without preview

# ----- Run -----
camera.start()
print("Press USR to START/STOP recording. Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    # Stop recording if still active
    if is_recording:
        try:
            camera.stop_recording()
        except Exception:
            pass
        
    # Stop preview only if it was started
    if preview_started:
        try:
            camera.stop_preview()
        except Exception:
            pass
    try:
        camera.stop()
    except Exception:
        pass
    try:
        camera.close()
    except Exception:
        pass
