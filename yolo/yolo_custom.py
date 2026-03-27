
#!/usr/bin/env python3
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

model = YOLO("your_model.pt")  # Replace with your model filename

# initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("YOLO start, Press 'q' to exit...")

try:
   while True:
      # capture frame
      frame = picam2.capture_array()
      
      # run YOLO and set imgsz=320
      results = model(frame, imgsz=320)
      
      # draw results
      annotated = results[0].plot()
      
      # show results
      cv2.imshow("YOLO on Raspberry Pi", annotated)
      
      # press 'q' to exit
      if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
   cv2.destroyAllWindows()
   picam2.stop()
   print("exit")