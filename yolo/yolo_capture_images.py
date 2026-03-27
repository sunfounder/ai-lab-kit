
#!/usr/bin/env python3
"""
Simple camera capture script for Raspberry Pi
Press SPACE to capture, ESC to exit
Images saved to ./captured_images/
"""

from picamera2 import Picamera2
import cv2
import os
import time

# Create save directory
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# Wait for camera to warm up
time.sleep(1)

print("=== Camera Capture Tool ===")
print(f"Images will be saved to: {save_dir}")
print("Controls:")
print("  SPACE - Capture image")
print("  ESC   - Exit")
print("==========================")

count = 0

try:
   while True:
      # Capture frame
      frame = picam2.capture_array()

      # Display frame with instructions
      display = frame.copy()
      cv2.putText(display, f"Captured: {count} images", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
      cv2.putText(display, "Press SPACE to capture, ESC to exit", (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
      
      cv2.imshow("Camera Capture", display)
      
      # Wait for key press
      key = cv2.waitKey(1) & 0xFF
      
      if key == 32:  # SPACE key
            # Save image
            filename = f"{save_dir}/img_{count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured: {filename}")
            count += 1
            
            # Optional: flash effect
            flash = frame.copy()
            flash[:] = (255, 255, 255)
            cv2.imshow("Camera Capture", flash)
            cv2.waitKey(50)
            
      elif key == 27:  # ESC key
            print(f"\nExiting. Total captured: {count} images")
            break

finally:
   cv2.destroyAllWindows()
   picam2.stop()
   print("Camera stopped")