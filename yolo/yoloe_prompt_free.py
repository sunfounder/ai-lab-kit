
from ultralytics import YOLO 
from picamera2 import Picamera2
import cv2

# prompt-free mode
model = YOLO("yoloe-11s-seg-pf.pt")  # pf = prompt-free

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("Prompt-free mode: detecting everything automatically...")
print("Press 'q' to exit")

while True:
   frame = picam2.capture_array()
   results = model.predict(frame, imgsz=320)
   annotated = results[0].plot()
   cv2.imshow("YOLOE Prompt-Free", annotated)
   
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
picam2.stop()