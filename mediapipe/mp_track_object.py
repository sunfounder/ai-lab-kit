#!/usr/bin/env python3

import cv2
import time
from fusion_hat.servo import Servo
from picamera2 import Picamera2
from pathlib import Path

# MediaPipe imports
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Settings
TARGET = "banana"
W, H = 640, 480
CX, CY = W//2, H//2

# Initialize
print(f"Tracking: {TARGET}")

# Servos
pan = Servo(2)
tilt = Servo(3)
pan.angle(0)
tilt.angle(0)
time.sleep(1)

# Camera
cam = Picamera2()
cam.configure(cam.create_preview_configuration(
    main={"size": (W, H), "format": "XRGB8888"}
))
cam.start()
time.sleep(2)

# Load MediaPipe model
model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")

# Create detector
options = vision.ObjectDetectorOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    score_threshold=0.3,
    running_mode=vision.RunningMode.VIDEO
)

detector = vision.ObjectDetector.create_from_options(options)

print("Ready. Press 'q' to quit")

# Simple tracking function
def simple_track(x, y):
    """Basic 4-direction tracking"""
    if x is None:
        return 0, 0
    
    pan_move = 0
    tilt_move = 0
    
    # Left/right
    if x < CX - 50:
        pan_move = 1
    elif x > CX + 50:
        pan_move = -1
    
    # Up/down  
    if y < CY - 50:
        tilt_move = -1
    elif y > CY + 50:
        tilt_move = 1
    
    return pan_move, tilt_move

# Main loop
pan_pos = 0
tilt_pos = 0

try:
    while True:
        # Get frame
        frame = cam.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        
        # Convert to RGB for MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        # Detect objects
        detections = detector.detect_for_video(mp_image, int(time.time() * 1000))
        
        # Find target
        obj_x = obj_y = None
        for detection in detections.detections:
            for category in detection.categories:
                if TARGET.lower() in str(category.category_name).lower():
                    bbox = detection.bounding_box
                    obj_x = bbox.origin_x + bbox.width // 2
                    obj_y = bbox.origin_y + bbox.height // 2
                    break
        
        # Track if object found
        if obj_x:
            pan_move, tilt_move = simple_track(obj_x, obj_y)
            pan_pos += pan_move
            tilt_pos += tilt_move
            
            # Limit angles
            pan_pos = max(-90, min(90, pan_pos))
            tilt_pos = max(-45, min(45, tilt_pos))
            
            # Move servos
            pan.angle(pan_pos)
            tilt.angle(tilt_pos)
            
            # Draw box
            cv2.rectangle(frame, 
                         (obj_x-30, obj_y-30), 
                         (obj_x+30, obj_y+30), 
                         (0,255,0), 2)
            status = f"Tracking {TARGET}"
            color = (0,255,0)
        else:
            status = f"No {TARGET}"
            color = (0,0,255)
        
        # Draw center cross
        cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
        cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)
        
        # Draw info
        cv2.putText(frame, status, (10,30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}", 
                   (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
        cv2.putText(frame, "Press 'q' to quit", (10,90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        
        # Show frame
        cv2.imshow(f"Track: {TARGET}", frame)
        
        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup
    pan.angle(0)
    tilt.angle(0)
    time.sleep(0.5)
    cam.stop()
    cv2.destroyAllWindows()
    print("Done")