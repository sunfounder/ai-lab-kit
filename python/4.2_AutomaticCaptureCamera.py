#!/usr/bin/env python3

import os
import time
import threading
from picamera2 import Picamera2, Preview
from fusion_hat.pin import Pin, Mode, Pull

# Resolve the correct user's home directory (works with sudo)
REAL_USER = os.getenv("SUDO_USER") or os.getlogin()
USER_HOME = f"/home/{REAL_USER}"
PICTURES_DIR = os.path.join(USER_HOME, "Pictures")
os.makedirs(PICTURES_DIR, exist_ok=True)

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (800, 600)}))

# Photo counter with thread safety
photo_index = 1
photo_lock = threading.Lock()

# Track whether preview was started successfully
preview_started = False

# Initialize PIR sensor (GPIO 17)
pir = Pin(17, mode=Mode.IN, pull=Pull.DOWN)

def take_photo():
   """Capture one photo and increment the index."""
   global photo_index
   with photo_lock:
      filepath = os.path.join(PICTURES_DIR, f"photo_{photo_index:03d}.jpg")
      print(f"\nMotion detected! Capturing: {filepath}")
      camera.capture_file(filepath)
      print("Saved.")
      photo_index += 1

def main():
   global preview_started

   # Start preview only when a GUI display is available
   preview_started = False
   if os.getenv("DISPLAY"):
      try:
         camera.start_preview(Preview.QT)
         preview_started = True
      except Exception as e:
         print(f"Preview start failed (continue without preview): {e}")
   else:
      print("No DISPLAY detected (running headless without preview).")

   camera.start()

   print("Camera is running.")
   print("PIR sensor monitoring on GPIO 17.")
   print(f"Photos will be saved to: {PICTURES_DIR}")
   print("Press Ctrl+C to exit.\n")

   try:
      while True:
         if pir.value():        # PIR detects motion (HIGH)
            take_photo()        # Take one photo
            time.sleep(2)       # Delay to avoid repeated shots

         time.sleep(0.1)

   except KeyboardInterrupt:
      print("\nExiting...")

   finally:
      try:
         camera.stop()
      except Exception:
         pass

      if preview_started:
         try:
            camera.stop_preview()
         except Exception:
            pass

      try:
         camera.close()
      except Exception:
         pass

if __name__ == "__main__":
   main()
