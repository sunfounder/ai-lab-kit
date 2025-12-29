#!/usr/bin/env python3
"""
Record video using the Fusion HAT+ USR button and Picamera2.

- Shows a live preview window.
- First USR button press: start recording.
- Second USR button press: stop recording.
- Videos are saved as ~/Videos/video_YYYYMMDD_HHMMSS.mp4
- Press Ctrl+C to exit.
"""

import os
import time
import threading
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from fusion_hat.user_button import UserButton  # Fusion HAT+ USR button

# Resolve the correct user's home directory (works even when using sudo)
REAL_USER = os.getenv("SUDO_USER") or os.getlogin()
USER_HOME = f"/home/{REAL_USER}"
VIDEOS_DIR = os.path.join(USER_HOME, "Videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

# Initialize camera and configure for video + preview
camera = Picamera2()
video_config = camera.create_video_configuration(
    main={"size": (800, 600)},
    controls={"FrameRate": 30},
    buffer_count=12,
)
camera.configure(video_config)

# Encoder for H.264 video
encoder = H264Encoder(bitrate=10_000_000)

# Recording state
record_lock = threading.Lock()
is_recording = False
current_output = None  # Keep a reference so it isn't garbage-collected

def make_output():
    """Create a new output file in ~/Videos with a timestamped name."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(VIDEOS_DIR, f"video_{timestamp}.mp4")
    return filepath, FfmpegOutput(filepath)

def toggle_recording():
    """
    Called when the USR button is pressed.
    First press: start recording.
    Second press: stop recording.
    """
    global is_recording, current_output

    with record_lock:
        if not is_recording:
            filepath, output = make_output()
            current_output = output
            print(f"\nStart recording: {filepath}")
            camera.start_recording(encoder, output)
            is_recording = True
        else:
            print("\nStop recording.")
            camera.stop_recording()
            is_recording = False
            current_output = None

def main():
    # Set up the USR button
    btn = UserButton()
    btn.set_on_click(toggle_recording)

    # Start preview and camera pipeline
    camera.start_preview(Preview.QT)
    camera.start()

    print("Video preview is running.")
    print("Press the Fusion HAT+ USR button to START/STOP recording.")
    print(f"Videos will be saved in: {VIDEOS_DIR}")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            time.sleep(0.1)  # Keep program alive
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        # If still recording, stop cleanly
        with record_lock:
            if is_recording:
                print("Stopping recording before exit...")
                camera.stop_recording()
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    main()
