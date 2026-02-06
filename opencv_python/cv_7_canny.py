from picamera2 import Picamera2
import cv2

# Empty callback function for trackbars (required by OpenCV API)
def _noop(x):
    pass

# -----------------------------
# Camera setup
# -----------------------------
picam2 = Picamera2()

# Create a preview configuration:
# size: resolution of the camera image
# format: XRGB8888 (4-channel image, similar to BGRA)
picam2.configure(
    picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "XRGB8888"}
    )
)

# Start the camera
picam2.start()

# -----------------------------
# Create OpenCV windows
# -----------------------------
WIN_CAM = "Camera"        # window for original image
WIN_EDGE = "Canny Edges"  # window for edge detection result

cv2.namedWindow(WIN_CAM)
cv2.namedWindow(WIN_EDGE)

# -----------------------------
# Create trackbars to tune Canny thresholds
# -----------------------------
# low_th: lower threshold for Canny
# high_th: higher threshold for Canny
cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

print("Press 'q' to exit")

# -----------------------------
# Main loop
# -----------------------------
while True:
    # Capture one frame from the camera (BGRA format)
    frame_bgra = picam2.capture_array()

    # Convert BGRA to BGR for OpenCV processing
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Read current threshold values from trackbars
    low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
    high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

    # Ensure high_th is always larger than low_th
    if high_th <= low_th:
        high_th = low_th + 1
        cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, low_th, high_th)

    # Show original camera image
    cv2.imshow(WIN_CAM, frame_bgr)

    # Show edge detection result
    cv2.imshow(WIN_EDGE, edges)

    # Process GUI events and keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Press 'q' to exit the program
    if key == ord("q"):
        break

    # Exit if the user closes any OpenCV window
    if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
        cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
        break

# -----------------------------
# Cleanup
# -----------------------------
picam2.stop()             # Stop the camera
cv2.destroyAllWindows()   # Close all OpenCV windows
