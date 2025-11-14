from picamera2 import Picamera2, Preview
import cv2

picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"} ,
)

picam2.configure(config)
#picam2.start_preview(Preview.QTGL)
picam2.start()

print("Streaming... press 'q' to quit")
while True:
    frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
    frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    cv2.imshow("BGR Frame", frame_bgr)
    cv2.imshow("GRAY Frame", frame_gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
