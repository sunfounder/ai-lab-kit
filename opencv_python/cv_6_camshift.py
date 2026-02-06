# Python program to demonstrate CAMShift (tracking a dark object)
import numpy as np
import cv2

# Read video


cap = cv2.VideoCapture("sample3.mp4")

# Retrieve the first frame from the video
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cannot read the video file.")

# Set the initial region for tracking window (x, y, width, height)
x, y, w, h = 100, 200, 40, 40
track_window = (x, y, w, h)

# Convert first frame to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Extract ROI (only the target area) in HSV
hsv_roi = hsv[y:y+h, x:x+w]

# For tracking a black object, we keep dark pixels (low V) inside ROI
# V channel is hsv[..., 2], so we build a mask based on V <= 80
roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

# Build histogram on V channel (channel index 2) within ROI
# Use 256 bins for V (0~256) to match back projection range
roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Termination criteria for CAMShift
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# FPS delay (fallback if FPS is unavailable)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1e-3:
    fps = 30.0
delay_ms = int(1000 / fps)

WINDOW_NAME = "CAMShift Tracker"

while True:
    ret, frame = cap.read()

    # If video ends, restart from beginning
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Back projection on V channel using ROI histogram (range 0~256)
    back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

    # Apply CAMShift
    rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

    # Draw rotated rectangle
    pts = cv2.boxPoints(rot_rect).astype(np.int32)
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

    cv2.putText(frame, "CAMShift Tracker", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(WINDOW_NAME, frame)

    # Keyboard + GUI events
    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

    # Exit if user closes the window (click X)
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
