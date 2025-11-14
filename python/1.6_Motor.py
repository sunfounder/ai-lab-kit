#!/usr/bin/env python3
from time import sleep
from fusion_hat.motor import Motor


motor = Motor('M0',is_reversed=True)

try:
    while True:
        motor.power(0)
        sleep(0.5)
        motor.power(-50)
        sleep(1)
        motor.power(0)
        sleep(0.5)
        motor.power(75)
        sleep(1)
finally:
    motor.stop()
    sleep(.1)
