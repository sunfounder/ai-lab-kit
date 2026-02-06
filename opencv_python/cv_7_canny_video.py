import cv2
from pathlib import Path

# --- Utility: empty callback for trackbars ---
def _noop(x):
    pass

# Get path of the video
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / "sample4.mp4")

# Read video
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise RuntimeError("Error opening video file")

# FPS fallback
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 1e-3:
    fps = 30.0
expected_delay = int(1000 / fps)

# Create OpenCV windows
WIN_CAM = "Camera"
WIN_EDGE = "Canny Edges"
cv2.namedWindow(WIN_CAM)
cv2.namedWindow(WIN_EDGE)

# Create trackbars
cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

print("Streaming... press 'q' to quit")

try:
    while True:
        start_time = cv2.getTickCount()
        ret, frame = cap.read()

        # Loop video
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Resize for display
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

        # Convert to gray and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Read trackbar values
        low_th  = cv2.getTrackbarPos("low_th", WIN_EDGE)
        high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

        if high_th <= low_th:
            high_th = low_th + 1
            cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

        # Canny
        edges = cv2.Canny(blurred, low_th, high_th, L2gradient=True)

        # Show windows
        cv2.imshow(WIN_CAM, frame)
        cv2.imshow(WIN_EDGE, edges)

        # Correct processing time in ms
        process_time = (cv2.getTickCount() - start_time) * 1000 / cv2.getTickFrequency()
        delay = max(1, int(expected_delay - process_time))

        # Keyboard
        k = cv2.waitKey(delay) & 0xFF
        if k == ord("q"):
            break

        # Exit if window closed
        if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
            cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
