from picamera2 import Picamera2, Preview
import cv2

# --- Utility: empty callback for trackbars ---
def _noop(x):
    pass

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}  # XRGB8888 -> BGRA frames
)
picam2.configure(config)

# Start preview from Picamera2 (optional GUI preview)
# picam2.start_preview(Preview.QTGL)
picam2.start()

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
        # Capture frame as BGRA due to XRGB8888 format
        frame_bgra = picam2.capture_array()
        # Convert BGRA -> BGR for OpenCV processing
        frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

        # --- Canny edge detection pipeline ---
        # 1) Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
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
        cv2.imshow("cv2.imshow", frame_bgr)
        cv2.imshow("Canny Edges", edges)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Always clean up devices and windows
    picam2.stop_preview()
    picam2.stop()
    cv2.destroyAllWindows()
