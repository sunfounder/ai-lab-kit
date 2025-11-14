# Python program to demonstrate
# meanshift 


import numpy as np
import cv2
 
# Get path of the video
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / 'sample2.mp4')

# read video
cap = cv2.VideoCapture(video_path)
 
# Retrieve the first frame from the video
ret, frame = cap.read()

##### Select the region of interest (ROI) with mouse####
# Press Enter or Space to confirm the selection
# Press Esc to exit the selection
roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select ROI")
x, y, w, h = map(int,roi_box)
track_window = (x, y, w, h)


# converting BGR to HSV format
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# apply mask on the HSV frame
# mask = cv2.inRange(hsv, np.array((0., 61., 33.)), np.array((180., 255., 255.)))

#### automatically select the HSV of the ROI####
h_roi = hsv[y:y+h, x:x+w, 0]
s_roi = hsv[y:y+h, x:x+w, 1]
v_roi = hsv[y:y+h, x:x+w, 2]

h_low,  h_high  = np.percentile(h_roi, [5, 95])
s_low,  s_high  = np.percentile(s_roi, [5, 95])
v_low,  v_med   = np.percentile(v_roi, [5, 95])

pad_h, pad_s, pad_v = 10, 20, 20
lower = np.array([max(h_low - pad_h, 0),
                  max(s_low - pad_s, 0),
                  max(v_low - pad_v, 0)], dtype=np.uint8)
upper = np.array([min(h_high + pad_h, 180),
                  min(s_high + pad_s, 255),
                  min(v_med  + pad_v,  255)], dtype=np.uint8)

# create a mask for the selected region
mask = cv2.inRange(hsv, lower, upper)


# get histogram for hsv channel
roi = cv2.calcHist([hsv], [0], mask, [180], [0, 180])

# normalize the retrieved values
cv2.normalize(roi, roi, 0, 255, cv2.NORM_MINMAX)
 
# termination criteria, either 15 
# iteration or by at least 2 pt
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2 )
 
while(True):
    start_time = cv2.getTickCount()
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        continue

    # convert BGR to HSV format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    bp = cv2.calcBackProject([hsv], [0], roi, [0, 180], 1)
 
    # applying meanshift to get the new region
    ret, track_window = cv2.meanShift(bp, track_window, termination)
 
    # Draw track window on the frame
    x, y, w, h = track_window
    frame = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
    
    # Display tracking information
    cv2.putText(frame, 'MeanShift Tracker', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # show results
    cv2.imshow('MeanShift Tracker', frame)
 
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
