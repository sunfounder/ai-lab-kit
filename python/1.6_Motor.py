#!/usr/bin/env python3
# Import sleep function to pause execution
from time import sleep
# Import Motor class from the fusion_hat.motor module
from fusion_hat.motor import Motor

# Create a Motor object for motor port 'M0'
# is_reversed=True means the motor direction is inverted
motor = Motor('M0', is_reversed=True)

try:
    # Loop forever
    while True:
        motor.power(0)       # Stop the motor
        sleep(0.5)           # Wait 0.5 seconds
        
        motor.power(-50)     # Run the motor at -50% power
        sleep(1)             # Run for 1 second
        
        motor.power(0)       # Stop again
        sleep(0.5)           # Wait 0.5 seconds
        
        motor.power(75)      # Run the motor at 75% power
        sleep(1)             # Run for 1 second

finally:
    motor.stop()             # Ensure the motor is stopped on exit
    sleep(.1)                # Short delay for safety
