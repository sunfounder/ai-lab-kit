#!/usr/bin/env python3
"""
Take photos using the Fusion HAT+ USR button and Picamera2.

- Shows a live preview window.
- Each press of the USR button captures a new image.
- Images are saved in ~/Pictures/photo_XXX.jpg with automatic numbering.
- Press Ctrl+C to exit.
"""

import os
import time
import threading
from picamera2 import Picamera2, Preview
from fusion_hat.user_button import UserButton   # Fusion HAT+ USR button

# Resolve the correct user's home directory
# Works correctly even when running with sudo
REAL_USER = os.getenv("SUDO_USER") or os.getlogin()
USER_HOME = f"/home/{REAL_USER}"
PICTURES_DIR = os.path.join(USER_HOME, "Pictures")
os.makedirs(PICTURES_DIR, exist_ok=True)

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (800, 600)}))

# Global photo counter with thread safety
photo_index = 1
photo_lock = threading.Lock()

# Button event handler
def take_photo():
    """
    Called automatically whenever the USR button is clicked.
    Captures a photo and saves it with an incrementing filename.
    """
    global photo_index
    with photo_lock:
        filepath = os.path.join(PICTURES_DIR, f"photo_{photo_index:03d}.jpg")
        print(f"\nCapturing: {filepath}")
        camera.capture_file(filepath)
        print("Saved.")
        photo_index += 1

# Main program logic
def main():
    # Start button listener
    btn = UserButton()
    btn.set_on_click(take_photo)

    # Start preview
    camera.start_preview(Preview.QT)
    camera.start()

    print("Camera preview is running.")
    print("Press the Fusion HAT+ USR button to take a photo.")
    print(f"Photos will be saved to: {PICTURES_DIR}")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            time.sleep(0.1)  # Keep program alive
    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    main()
