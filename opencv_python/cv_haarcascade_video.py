# Python program to demonstrate
# meanshift 


import numpy as np
import cv2


# Get path of the video
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / 'sample5.mp4')

# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
face_cascade = cv2.CascadeClassifier(str(BASE_DIR /'haarcascade_frontalface_default.xml'))

# Trained XML file for detecting eyes
eye_cascade = cv2.CascadeClassifier(str(BASE_DIR /'haarcascade_eye.xml'))


# Read video
cap = cv2.VideoCapture(video_path)

if cap.isOpened() == False:
    print("Error opening video stream or file")
 
# Retrieve the first frame from the video
ret, frame = cap.read()

 
while(True):
    start_time = cv2.getTickCount()
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        continue

    # convert to gray scale of each frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detects faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # To draw a rectangle in a face
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detects eyes of different sizes in the input image
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # To draw a rectangle in eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)

    # Display an image in a window
    cv2.imshow('Haarcascade',frame)

    # Calculate delay to maintain desired FPS
    expected_delay = max(1, int(1000 / cap.get(cv2.CAP_PROP_FPS)))
    process_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    delay = int(expected_delay - process_time)
    
    # Ensure delay is non-negative
    delay = max(0, delay)
    
    # Wait for the next frame
    k = cv2.waitKey(delay) & 0xff
    if k == ord('q'):
        break
        
# release cap object
cap.release()

# destroy all opened windows
cv2.destroyAllWindows()
