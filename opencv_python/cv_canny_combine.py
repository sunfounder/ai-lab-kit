from picamera2 import Picamera2, Preview
import cv2

def _noop(x):
    pass

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}  # XRGB8888 -> BGRA frames
)
picam2.configure(config)

picam2.start_preview(Preview.QTGL)
picam2.start()

cv2.namedWindow("Camera with Canny Overlay")
cv2.createTrackbar("low_th",  "Camera with Canny Overlay", 50, 255, _noop)
cv2.createTrackbar("high_th", "Camera with Canny Overlay", 150, 255, _noop)

print("Streaming... press 'q' to quit")
try:
    while True:
        # Capture frame
        frame_bgra = picam2.capture_array()
        frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Read thresholds
        low_th  = cv2.getTrackbarPos("low_th",  "Camera with Canny Overlay")
        high_th = cv2.getTrackbarPos("high_th", "Camera with Canny Overlay")
        if high_th <= low_th:
            high_th = low_th + 1
            cv2.setTrackbarPos("high_th", "Camera with Canny Overlay", high_th)

        # Canny edge detection
        edges = cv2.Canny(blurred, threshold1=low_th, threshold2=high_th, L2gradient=True)

        # Convert edges to 3 channels (white edges on black background)
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Overlay: use bitwise OR (edges as white lines over original)
        overlay = cv2.addWeighted(frame_bgr, 0.8, edges_bgr, 0.8, 0)

        cv2.imshow("Camera with Canny Overlay", overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    picam2.stop_preview()
    picam2.stop()
    cv2.destroyAllWindows()
