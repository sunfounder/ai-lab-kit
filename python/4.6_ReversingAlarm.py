#!/usr/bin/env python3

import time
from fusion_hat.modules import Ultrasonic, Buzzer
from fusion_hat.pin import Pin

# Trigger pin is connected to GPIO 27, Echo pin to GPIO 22
sensor = Ultrasonic(trig=Pin(27), echo=Pin(22))

# Initialize the buzzer connected to GPIO pin 17
buzzer = Buzzer(Pin(17))


def distance():
    # Calculate and return the distance measured by the sensor
    dis = sensor.read() # Convert distance to centimeters
    print('Distance: {:.2f} cm'.format(dis))  # Print distance with two decimal places
    time.sleep(0.3)  # Wait for 0.3 seconds before next measurement
    return dis

def loop():
    # Continuously measure distance and update buzzer
    while True:
        dis = distance()  # Get the current distance

        # Adjust buzzer frequency based on distance
        if dis >= 50:
            time.sleep(0.5)
        elif 20 < dis < 50:
            # Medium distance: medium buzzer frequency
            for _ in range(2):
                buzzer.on()
                time.sleep(0.05)
                buzzer.off()
                time.sleep(0.2)
        elif dis <= 20:
            # Close distance: high buzzer frequency
            for _ in range(5):
                buzzer.on()
                time.sleep(0.05)
                buzzer.off()
                time.sleep(0.05)

try:
    loop()      # Start the measurement loop
except KeyboardInterrupt:
    # Turn off buzzer (e.g., Ctrl+C)
    buzzer.off()
