#!/usr/bin/env python3
from fusion_hat.servo import Servo   # Import Servo class
from time import sleep               # Import sleep for delays

# Initialize servo on channel 0
servo = Servo(0)

try:
    while True:
        # Sweep from -90° to +90° in steps of 10°
        for angle in range(-90, 91, 10):
            servo.angle(angle)
            sleep(0.1)   # Smooth movement delay

        # Sweep back from +90° to -90° in steps of 10°
        for angle in range(90, -91, -10):
            servo.angle(angle)
            sleep(0.1)

except KeyboardInterrupt:
    # Stop the program safely when Ctrl+C is pressed
    servo.angle(0)        # Return servo to center position
    sleep(0.1)
