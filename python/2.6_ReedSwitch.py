#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode, Pull
from time import sleep  # Import sleep for delay

# Initialize reed switch (Button) on GPIO pin 17
reed = Pin(17, mode=Mode.IN, pull=Pull.DOWN)

# Initialize LED1 connected to GPIO pin 22
led1 = Pin(22,mode=Mode.OUT)
# Initialize LED2 connected to GPIO pin 27
led2 = Pin(27,mode=Mode.OUT)

try:
      # Continuously monitor the state of the reed switch and control LEDs accordingly
      while True:
         if reed.value() == 1:  # Check if the reed switch is activated
            led1.off()  # Turn off LED1
            led2.on()   # Turn on LED2
         else:  # If the sensor is not activated
            led1.on()   # Turn on LED1
            led2.off()  # Turn off LED2

except KeyboardInterrupt:
      # Handle a keyboard interrupt (Ctrl+C) for a clean exit from the loop
      pass
