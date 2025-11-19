# from fusion_hat.modules import MPU6050
from fusion_hat.modules import Compass 
import time

com = Compass()

compass_offsets = (-123.52, 88.14, 30.77)
compass_scales  = (1.0921, 0.9746, 1.0154)

while True:
    x, y, z, _ = com.read()

    x = (x - compass_offsets[0]) * compass_scales[0]
    y = (y - compass_offsets[1]) * compass_scales[1]
    z = (z - compass_offsets[2]) * compass_scales[2]

    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360

    print("Corrected heading:", angle)
    time.sleep(0.1)
