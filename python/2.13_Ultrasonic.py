# Import Ultrasonic and Pin class
from fusion_hat.modules import Ultrasonic
from fusion_hat.pin import Pin
from time import sleep

# Create Ultrasonic object
sensor = Ultrasonic(Pin(27), Pin(22))

try:
    # Main loop to continuously measure and report distance
    while True:
        dis = sensor.read() # Measure distance in centimeters
        print('Distance: {:.2f} cm'.format(dis))  # Print the distance with two decimal precision
        sleep(0.3)  # Wait for 0.3 seconds before the next measurement

except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C) to gracefully exit the loop
    pass