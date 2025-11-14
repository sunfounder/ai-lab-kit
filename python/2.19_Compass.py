# from fusion_hat.modules import MPU6050
from fusion_hat.modules import Compass 
import time

com = Compass()


while True:
   x, y, z, angle = com.read()
   print("x: %d, y: %d, z: %d, angle: %d")
   time.sleep(0.1)
   