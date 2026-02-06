#!/usr/bin/env python3
from time import sleep
from fusion_hat.motor import Motor

# Motor on port M0, reverse direction if needed
motor = Motor("M0", is_reversed=True)

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

except KeyboardInterrupt:
    # Ctrl + C to stop
    print("\nStopped by user.")

finally:
    # Always stop the motor safely
    motor.stop()
    sleep(0.1)
