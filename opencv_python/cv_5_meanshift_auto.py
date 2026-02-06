# Python program to demonstrate MeanShift tracking with ROI selection
import numpy as np
import cv2
from pathlib import Path

# -----------------------------
# Load video
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / "sample2.mp4")

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise RuntimeError("Error opening video file")

# Read the first frame (for ROI selection and building the target model)
ret, frame0 = cap.read()
if not ret:
    raise RuntimeError("Cannot read the first frame from the video")

# -----------------------------
# Select ROI with mouse
# Press Enter/Space to confirm, press Esc to cancel
# -----------------------------
roi_box = cv2.selectROI("Select ROI", frame0, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Select ROI")

x, y, w, h = map(int, roi_box)
if w == 0 or h == 0:
    cap.release()
    cv2.destroyAllWindows()
    raise RuntimeError("ROI selection cancelled or invalid")

track_window = (x, y, w, h)

# -----------------------------
# Build target model from ROI (Hue histogram)
# 1) Convert first frame to HSV
# 2) Estimate HSV bounds from ROI percentiles
# 3) Build mask ONLY inside ROI
# 4) Compute ROI histogram on Hue channel
# -----------------------------
hsv0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2HSV)
roi_hsv = hsv0[y:y + h, x:x + w]

h_roi = roi_hsv[:, :, 0]
s_roi = roi_hsv[:, :, 1]
v_roi = roi_hsv[:, :, 2]

# Robust range from percentiles (ignore outliers)
h_low, h_high = np.percentile(h_roi, [5, 95])
s_low, s_high = np.percentile(s_roi, [5, 95])
v_low, v_high = np.percentile(v_roi, [5, 95])

# Add padding so the range is not too tight
pad_h, pad_s, pad_v = 10, 20, 20

lower = np.array([
    max(int(h_low) - pad_h, 0),
    max(int(s_low) - pad_s, 0),
    max(int(v_low) - pad_v, 0)
], dtype=np.uint8)

upper = np.array([
    min(int(h_high) + pad_h, 180),
    min(int(s_high) + pad_s, 255),
    min(int(v_high) + pad_v, 255)
], dtype=np.uint8)

# Mask ONLY the ROI (do not mask the whole frame)
roi_mask = cv2.inRange(roi_hsv, lower, upper)

# Histogram on Hue channel (0..180)
roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Termination criteria: max 15 iterations or move by at least 2 pixels
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

# FPS delay (fallback if unavailable)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1e-3:
    fps = 30.0
expected_delay_ms = int(1000 / fps)

WIN = "MeanShift Tracker"
print("Tracking... press 'q' to quit")

# -----------------------------
# Main loop
# -----------------------------
while True:
    start_tick = cv2.getTickCount()
    ret, frame = cap.read()

    # Loop video
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Back projection (Hue channel, range 0..180)
    bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

    # Optional: smooth probability map to reduce noise
    bp = cv2.GaussianBlur(bp, (5, 5), 0)

    # Apply MeanShift to update tracking window
    _, track_window = cv2.meanShift(bp, track_window, term_crit)

    # Draw tracking window
    x, y, w, h = track_window
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, "MeanShift Tracker", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow(WIN, frame)

    # Correct processing time in milliseconds
    process_time_ms = (cv2.getTickCount() - start_tick) * 1000 / cv2.getTickFrequency()
    delay_ms = max(1, int(expected_delay_ms - process_time_ms))

    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

    # Exit if the user closes the window (click X)
    if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
