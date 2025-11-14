
import cv2

# --- Utility: empty callback for trackbars ---
def _noop(x):
    pass

# Get path of the video
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / 'sample4.mp4')

# Read video
cap = cv2.VideoCapture(video_path)

if cap.isOpened() == False:
    print("Error opening video stream or file")

# Create OpenCV windows
cv2.namedWindow("cv2.imshow")         # original view
cv2.namedWindow("Canny Edges")        # edge view

# Create trackbars to tune Canny thresholds in real time
# Typical ranges: low (0-255), high (0-255); start with common defaults
cv2.createTrackbar("low_th",  "Canny Edges", 50, 255, _noop)
cv2.createTrackbar("high_th", "Canny Edges", 150, 255, _noop)

print("Streaming... press 'q' to quit")
try:
    while True:
        start_time = cv2.getTickCount()
        ret, frame = cap.read()
        
        # If video ends, restart from beginning
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Resize frame for better display
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)


        # --- Canny edge detection pipeline ---
        # 1) Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 2) Optional denoising to reduce false edges
        #    Gaussian blur helps Canny be less sensitive to noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Read current thresholds from trackbars
        low_th  = cv2.getTrackbarPos("low_th",  "Canny Edges")
        high_th = cv2.getTrackbarPos("high_th", "Canny Edges")

        # Ensure high threshold is at least low threshold + 1 to avoid errors
        if high_th <= low_th:
            high_th = low_th + 1
            cv2.setTrackbarPos("high_th", "Canny Edges", high_th)

        # 3) Run Canny
        edges = cv2.Canny(blurred, threshold1=low_th, threshold2=high_th, L2gradient=True)

        # Show original and edges
        cv2.imshow("cv2.imshow", frame)
        cv2.imshow("Canny Edges", edges)

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
            
finally:
    # Release video capture object
    cap.release()
    cv2.destroyAllWindows()
