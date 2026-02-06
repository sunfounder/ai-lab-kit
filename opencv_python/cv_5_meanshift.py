import numpy as np
import cv2

cap = cv2.VideoCapture("sample2.mp4")

# Read the first frame
ret, frame = cap.read()
if not ret:
    raise RuntimeError("Cannot read the video file.")

# Initial tracking window (x, y, w, h)
x, y, w, h = 80, 100, 80, 80
track_window = (x, y, w, h)

# Convert the first frame to HSV
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Extract ROI in HSV (ONLY the selected area)
roi_hsv = hsv_frame[y:y+h, x:x+w]

# Create a mask for ROI (filter out low saturation/value pixels)
roi_mask = cv2.inRange(
    roi_hsv,
    np.array((0, 61, 33), dtype=np.uint8),
    np.array((180, 255, 255), dtype=np.uint8)
)

# Compute histogram of ROI (Hue channel)
roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

# Normalize histogram for better tracking
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Termination criteria: max 15 iterations or move by at least 2 pixels
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

# FPS settings (fallback if FPS is unavailable)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1e-3:
    fps = 30.0
delay_ms = int(1000 / fps)

WINDOW_NAME = "MeanShift Tracker"

while True:
    ret, frame = cap.read()

    # Loop video
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Back projection: probability map of where the ROI histogram appears in the frame
    bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

    # Apply meanShift to update tracking window
    _, track_window = cv2.meanShift(bp, track_window, termination)

    # Draw tracking window
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, "MeanShift Tracker", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(WINDOW_NAME, frame)

    # Handle keyboard input and GUI events
    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

    # Exit if window is closed
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
