#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode, Pull

# Initialize PIR motion sensor on GPIO 22 (input with pull-down)
pir = Pin(22, mode=Mode.IN, pull=Pull.DOWN)

# Define GPIO pins for the 74HC595 shift register
SDI = Pin(17, mode=Mode.OUT)   # Serial Data Input
RCLK = Pin(4, mode=Mode.OUT)   # Register Clock (latch)
SRCLK = Pin(27, mode=Mode.OUT) # Shift Register Clock

# Define GPIO pins used to select one of the 4 digits on the 7-segment display
placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]

# Segment code table for digits 0–9 (common-cathode 7-segment display)
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

# Counter to display the number of detections
counter = 0

def clearDisplay():
    """Clear the 7-segment display by shifting out 'all off' bits."""
    for _ in range(8):
        SDI.high()     # Send a high bit
        SRCLK.high()   # Clock it in
        SRCLK.low()
    RCLK.high()        # Latch output
    RCLK.low()

def hc595_shift(data):
    """Shift a full byte of data into the 74HC595 to control the segments."""
    for i in range(8):
        SDI.value(0x80 & (data << i))  # Output next bit of the data
        SRCLK.high()                   # Pulse shift clock
        SRCLK.low()
    RCLK.high()                        # Latch data to display
    RCLK.low()

def pickDigit(digit):
    """Enable one specific digit (0–3) on the multiplexed display."""
    for pin in placePin:
        pin.low()                      # Disable all digits
    placePin[digit].high()             # Activate the selected digit

def display():
    """Display the current 4-digit counter value on the 7-segment display."""
    global counter

    # Display ones place
    clearDisplay()
    pickDigit(3)
    hc595_shift(number[counter % 10])

    # Display tens place
    clearDisplay()
    pickDigit(2)
    hc595_shift(number[counter % 100 // 10])

    # Display hundreds place
    clearDisplay()
    pickDigit(1)
    hc595_shift(number[counter % 1000 // 100])

    # Display thousands place
    clearDisplay()
    pickDigit(0)
    hc595_shift(number[counter % 10000 // 1000])

def loop():
    """Main loop: continuously update display and detect PIR motion transitions."""
    global counter
    currentState = 0
    lastState = 0

    while True:
        display()                                      # Refresh 7-segment display
        currentState = 1 if pir.value() == 1 else 0    # Read PIR output

        # Detect rising edge: motion detected now, but not in last cycle
        if currentState == 1 and lastState == 0:
            counter += 1                               # Increase the count

        lastState = currentState                        # Save state for next loop

try:
    loop()                                             # Start main loop
except KeyboardInterrupt:
    # Clean up GPIO pins when exiting
    SDI.low()
    SRCLK.low()
    RCLK.low()
    pass
