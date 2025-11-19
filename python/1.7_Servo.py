from fusion_hat.servo import Servo   # Import the Servo class for controlling servos
from time import sleep               # Import sleep for timing delays

servo = Servo(0)                     # Create a Servo object on channel 0

while True:                          # Loop forever
    # Sweep from -90° to +90° in steps of 10°
    for i in range(-90, 91, 10):
        servo.angle(i)               # Set servo to angle i
        sleep(0.1)                   # Small delay for smooth movement

    # Sweep back from +90° to -90° in steps of -10°
    for i in range(90, -91, -10):
        servo.angle(i)               # Set servo to angle i
        sleep(0.1)                   # Small delay for smooth movement
