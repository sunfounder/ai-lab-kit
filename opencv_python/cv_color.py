from picamera2 import Picamera2, Preview
import cv2
import numpy as np


picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"}  
)
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start()

print("Streaming... press 'q' to quit")


LOWER_RED1 = np.array([0,   100, 80])
UPPER_RED1 = np.array([10,  255, 255])
LOWER_RED2 = np.array([170, 100, 80])
UPPER_RED2 = np.array([180, 255, 255])

KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
MIN_AREA = 800   

while True:
    # Capture camera frame-by-frame as BGR
    frame_bgra = picam2.capture_array()
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Use inRange to get mask
    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask = cv2.bitwise_or(mask1, mask2)

    # cv2.imshow("inrange mask", mask)

    # Morphological operations
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)


    # cv2.imshow("morph mask", mask)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        
        cv2.rectangle(frame_bgr, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame_bgr, f"red {int(area)}", (x, y-6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("red-mask", mask)
    cv2.imshow("cv2.imshow", frame_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
