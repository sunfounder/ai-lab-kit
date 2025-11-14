# Python program to demonstrate face and eye detection using Raspberry Pi Camera
import numpy as np
import cv2
from picamera2 import Picamera2


# Get path
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# 1. Trained XML classifiers for face and eye detection
face_cascade = cv2.CascadeClassifier(str(BASE_DIR /'haarcascade_frontalface_default.xml'))

# Trained XML file for detecting eyes
eye_cascade = cv2.CascadeClassifier(str(BASE_DIR /'haarcascade_eye.xml'))


# 2. Initialize Picamera2
picam2 = Picamera2()

# Configure camera for video capture
config = picam2.create_video_configuration(
    main={"size": (640, 480)},  # Adjust resolution as needed
)
picam2.configure(config)

# Start camera
picam2.start()

print("Camera started. Press 'q' to quit.")

while True:
    start_time = cv2.getTickCount()
    
    # 3. Capture frame from Pi Camera
    frame = picam2.capture_array()
    
    # 4. Convert BGR to RGB (OpenCV uses BGR, PiCamera captures RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # 5. Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 6. Detect faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    face_count = 0
    eye_count = 0
    
    for (x, y, w, h) in faces:
        face_count += 1
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        
        # Add face label
        cv2.putText(frame, f'Face {face_count}', (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        
        # 8. Detect eyes in the face region
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # Draw rectangles around eyes
        for (ex, ey, ew, eh) in eyes:
            eye_count += 1
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)
    
    # 9. Display the frame
    cv2.imshow('Raspberry Pi Camera - Face Detection', frame)
    
    # Wait for key press
    k = cv2.waitKey(1) & 0xff
    if k == ord('q'):
        break

# Cleanup
picam2.stop()
cv2.destroyAllWindows()
print("Camera stopped.")