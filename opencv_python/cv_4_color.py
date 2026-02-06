from picamera2 import Picamera2
import cv2
import numpy as np
import time

# -----------------------------
# Camera setup
# -----------------------------
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
)
picam2.configure(config)
picam2.start()

print("Streaming... press 'q' to quit")

# -----------------------------
# Red color range in HSV
# (Red wraps around 0/180 in HSV, so we use two ranges)
# -----------------------------
LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

# Morphology settings
KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
MIN_AREA = 800  # ignore small blobs

# Window names
WIN_RESULT = "Red Detection"
WIN_MASK = "Red Mask"

# Optional: limit FPS to reduce CPU usage (set to None to disable)
TARGET_FPS = 30
FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

while True:
    loop_start = time.perf_counter()

    # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
    frame_bgra = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Create red mask using two HSV ranges
    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Morphological operations: remove noise + fill holes
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes for valid red regions
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame_bgr,
            f"red area={int(area)}",
            (x, max(0, y - 6)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA
        )

    # Show both windows
    cv2.imshow(WIN_RESULT, frame_bgr)
    cv2.imshow(WIN_MASK, mask)

    # Process GUI events + keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # Exit if the user closes any window (click X)
    if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
        cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
        break

# Cleanup
picam2.stop()
cv2.destroyAllWindows()
