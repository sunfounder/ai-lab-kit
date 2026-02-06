# Import Picamera2 for Raspberry Pi Camera
from picamera2 import Picamera2
import cv2
import time

# Create a Picamera2 object
picam2 = Picamera2()

# Create a camera configuration
# XRGB8888 is a 4-channel format (similar to BGRA)
# size sets the resolution of the camera frame
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}
)

# Apply the configuration to the camera
picam2.configure(config)

# Start the camera
picam2.start()

print("Streaming... press 'q' to quit")

# Window names
WINDOW_BGR = "BGR Frame"
WINDOW_GRAY = "GRAY Frame"

while True:
    # Capture one frame as a NumPy array (BGRA-like format)
    frame_bgra = picam2.capture_array()

    # Convert BGRA to BGR for normal color display
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert BGRA directly to grayscale
    frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

    # Display the color and grayscale frames
    cv2.imshow(WINDOW_BGR, frame_bgr)
    cv2.imshow(WINDOW_GRAY, frame_gray)

    # Process GUI events and check keyboard input
    # Press 'q' to exit the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Exit if the user closes any OpenCV window
    if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
        cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
        break

    # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
    time.sleep(1 / 30)

# Stop the camera
picam2.stop()

# Close all OpenCV windows
cv2.destroyAllWindows()
