#!/usr/bin/env python3
import os, time, pwd
from picamera2 import Picamera2, Preview
from fusion_hat.user_button import UserButton

u = os.getenv("SUDO_USER")
home = pwd.getpwnam(u).pw_dir if u else os.path.expanduser("~")
os.makedirs(f"{home}/Pictures", exist_ok=True)
photo = f"{home}/Pictures/my_photo.jpg"

camera = Picamera2()
camera.configure(camera.create_preview_configuration())

def shot():
    camera.capture_file(photo)
    print(f"Saved: {photo}")

UserButton().set_on_click(shot)

# Start preview only when a GUI display is available
preview_started = False
if os.getenv("DISPLAY"):
    try:
        camera.start_preview(Preview.QT)
        preview_started = True
    except Exception as e:
        print(f"Preview disabled: {e}")

camera.start()
print("Press USR to take photo. Ctrl+C to exit.")
try:
    while True: time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    try: camera.stop()
    except: pass
    if preview_started:
        try: camera.stop_preview()
        except: pass
    try: camera.close()
    except: pass


