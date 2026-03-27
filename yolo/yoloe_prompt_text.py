
from ultralytics import YOLOE
from picamera2 import Picamera2
import cv2

# load YOLOE model
model = YOLOE("yoloe-26n-seg.pt")  # nano version

# set the classes to detect (text prompt)
names = ["yellow paper", "red cup", "person wearing glasses"]
model.set_classes(names, model.get_text_pe(names))

# initialize the camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("YOLOE running with text prompts, press 'q' to exit...")
print(f"Detecting: {', '.join(names)}")

while True:
   frame = picam2.capture_array()
   results = model.predict(frame, conf=0.3)  # set confidence threshold to 0.3
   annotated = results[0].plot()
   cv2.imshow("YOLOE on Raspberry Pi", annotated)
   
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cv2.destroyAllWindows()
picam2.stop()
