
#!/usr/bin/env python3
"""
YOLO-based Object Tracking for Raspberry Pi
Tracks a specific object (e.g., person) using YOLO and controls servos
Press SPACE to capture images for dataset, ESC to exit
"""

from picamera2 import Picamera2
from ultralytics import YOLO
from fusion_hat.servo import Servo
import cv2
import time
import os

# -------------------- Configuration --------------------
TARGET = "your_object"      # Object to track (class name)
W, H = 640, 480         # Camera resolution
CX, CY = W // 2, H // 2 # Center coordinates
CONFIDENCE = 0.3        # Detection confidence threshold
DEADZONE = 50           # Pixels from center before moving
SAVE_DIR = "captured_images"  # Dataset save directory

# Create save directory
os.makedirs(SAVE_DIR, exist_ok=True)

print(f"=== YOLO Tracking System ===")
print(f"Target: {TARGET}")
print(f"Confidence threshold: {CONFIDENCE}")
print(f"Deadzone: {DEADZONE} pixels")

# -------------------- Servo Initialization --------------------
print("Initializing servos...")
pan = Servo(2)    # Channel 2 for pan (horizontal)
tilt = Servo(3)   # Channel 3 for tilt (vertical)
pan.angle(0)      # Center position
tilt.angle(0)     # Center position
time.sleep(1)

# -------------------- YOLO Model Loading --------------------
print("Loading YOLO model...")
# Use YOLOv8n for best performance on Raspberry Pi
model = YOLO("your_model.pt")
print("Model loaded successfully")

# -------------------- Camera Initialization --------------------
print("Initializing camera...")
picam2 = Picamera2()
picam2.preview_configuration.main.size = (W, H)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)

print("\n=== System Ready ===")
print("Controls:")
print("  SPACE - Capture image (for dataset)")
print("  ESC   - Exit")
print("  (Auto-tracks object when detected)")
print("==========================\n")

# -------------------- Tracking Variables --------------------
pan_pos = 0    # Current pan angle (-90 to 90)
tilt_pos = 0   # Current tilt angle (-45 to 45)
capture_count = 0

def simple_track(x, y):
   """
   Simple 4-direction tracking with deadzone
   Returns: (pan_move, tilt_move) where:
      pan_move: -1 (left), 0 (stop), 1 (right)
      tilt_move: -1 (down), 0 (stop), 1 (up)
   """
   if x is None or y is None:
      return 0, 0
   
   pan_move = 0
   tilt_move = 0
   
   # Horizontal movement (pan)
   if x < CX - DEADZONE:
      pan_move = 1           # Move right
   elif x > CX + DEADZONE:
      pan_move = -1          # Move left
   
   # Vertical movement (tilt)
   if y < CY - DEADZONE:
      tilt_move = -1         # Move down
   elif y > CY + DEADZONE:
      tilt_move = 1          # Move up
   
   return pan_move, tilt_move

def find_target_detection(results, target_name):
   """
   Search YOLO detection results for target object
   Returns: (x_center, y_center, confidence) or (None, None, None)
   """
   if len(results[0].boxes) == 0:
      return None, None, None
   
   for box in results[0].boxes:
      class_id = int(box.cls[0])
      class_name = model.names[class_id]
      confidence = float(box.conf[0])
      
      # Case-insensitive partial match
      if target_name.lower() in class_name.lower():
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)
            return x_center, y_center, confidence
   
   return None, None, None

# -------------------- Main Tracking Loop --------------------
try:
   while True:
      # Capture frame
      frame = picam2.capture_array()
      
      # Run YOLO detection
      results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)
      
      # Find target object
      obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)
      
      # Process tracking if object found
      if obj_x is not None:
            pan_move, tilt_move = simple_track(obj_x, obj_y)
            pan_pos += pan_move
            tilt_pos += tilt_move
            
            # Limit servo angles to safe ranges
            pan_pos = max(-90, min(90, pan_pos))
            tilt_pos = max(-45, min(45, tilt_pos))
            
            # Send commands to servos
            pan.angle(pan_pos)
            tilt.angle(tilt_pos)
            
            # Draw detection box
            cv2.rectangle(frame, (obj_x - 30, obj_y - 30), 
                        (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
            cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)
            
            status = f"{TARGET} detected: {obj_conf:.2f}"
            color = (0, 255, 0)
      else:
            status = f"No {TARGET} detected"
            color = (0, 0, 255)
      
      # Draw center crosshair
      cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
      cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
      
      # Draw deadzone rectangle (visual reference)
      cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                     (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)
      
      # Display status information
      cv2.putText(frame, status, (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
      cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                  (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
      cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
      cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
      
      # Show video window
      cv2.imshow(f"YOLO Tracking - {TARGET}", frame)
      
      # Handle key presses
      key = cv2.waitKey(1) & 0xFF
      
      if key == 32:  # SPACE key - capture image
            filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured: {filename}")
            capture_count += 1
            
            # Flash effect
            flash = frame.copy()
            flash[:] = (255, 255, 255)
            cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
            cv2.waitKey(50)
            
      elif key == 27:  # ESC key - exit
            print(f"\nExiting. Total captured: {capture_count} images")
            break

finally:
   # -------------------- Cleanup --------------------
   print("Cleaning up...")
   pan.angle(0)      # Return to center
   tilt.angle(0)     # Return to center
   time.sleep(0.5)
   cv2.destroyAllWindows()
   picam2.stop()
   print("Tracking stopped. Servos centered.")