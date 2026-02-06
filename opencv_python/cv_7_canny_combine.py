from picamera2 import Picamera2, Preview
import cv2

# Empty callback function for trackbars (required by OpenCV API)
def _noop(x):
    pass

# -----------------------------
# Camera setup
# -----------------------------
picam2 = Picamera2()

# Create camera configuration
# size   : camera resolution
# format : XRGB8888 (4-channel image format, similar to BGRA)
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}
)
picam2.configure(config)

# Optional: Picamera2 preview window (can be disabled for OpenCV demos)
# This preview uses GPU and may conflict with OpenCV windows
# picam2.start_preview(Preview.QTGL)

# Start the camera
picam2.start()

# -----------------------------
# Create OpenCV window
# -----------------------------
WIN = "Camera with Canny Overlay"
cv2.namedWindow(WIN)

# Create trackbars to adjust Canny thresholds in real time
# low_th  : lower threshold for Canny edge detection
# high_th : higher threshold for Canny edge detection
cv2.createTrackbar("low_th",  WIN, 50, 255, _noop)
cv2.createTrackbar("high_th", WIN, 150, 255, _noop)

print("Streaming... press 'q' to quit")

try:
    # -----------------------------
    # Main loop
    # -----------------------------
    while True:
        # Capture one frame from the camera (BGRA format)
        frame_bgra = picam2.capture_array()

        # Convert BGRA to BGR for OpenCV processing
        frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

        # Convert the image to grayscale (Canny works on single-channel images)
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise and false edges
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Read threshold values from trackbars
        low_th  = cv2.getTrackbarPos("low_th",  WIN)
        high_th = cv2.getTrackbarPos("high_th", WIN)

        # Ensure high_th is always greater than low_th
        # Prevent invalid threshold settings
        if high_th <= low_th:
            high_th = min(255, low_th + 1)
            cv2.setTrackbarPos("high_th", WIN, high_th)

        # Perform Canny edge detection
        edges = cv2.Canny(blurred, threshold1=low_th, threshold2=high_th, L2gradient=True)

        # Convert edges to 3-channel image for overlay display
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Overlay edges on the original image
        # addWeighted blends original image and edge map
        overlay = cv2.addWeighted(frame_bgr, 0.8, edges_bgr, 0.8, 0)

        # Display the overlay result
        cv2.imshow(WIN, overlay)

        # Process GUI events and keyboard input
        key = cv2.waitKey(1) & 0xFF

        # Press 'q' to exit the program
        if key == ord("q"):
            break

        # Exit if the user closes the window (click the close button)
        if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    # -----------------------------
    # Cleanup resources
    # -----------------------------
    picam2.stop()            # Stop the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows
