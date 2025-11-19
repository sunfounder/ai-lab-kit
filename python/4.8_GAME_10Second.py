#!/usr/bin/env python3

# Import Pin control, modes, and pull-up/down definitions
from fusion_hat.pin import Pin, Mode, Pull
# Import time for delays
import time
# Import threading to use Timer for repeated callbacks
import threading

# Initialize the button connected to GPIO 22, set as input with pull-down resistor
sensorPin = Pin(22, mode=Mode.IN, pull=Pull.DOWN)

# Define GPIO pins for the 74HC595 shift register
SDI = Pin(17, mode=Mode.OUT)    # Serial Data Input
RCLK = Pin(4, mode=Mode.OUT)    # Register Clock (latch)
SRCLK = Pin(27, mode=Mode.OUT)  # Shift Register Clock

# Define GPIO pins controlling digit selection on the 4-digit 7-segment display
placePin = [Pin(pin, mode=Mode.OUT) for pin in (23, 24, 25, 12)]

# Define the segment encoding for digits 0–9 (common cathode)
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)

# Counter value, timer object, and game state variable
counter = 0
timer1 = None
gameState = 0

def clearDisplay():
    """Clear all segments by shifting out 'all off' bits to the 74HC595."""
    for _ in range(8):
        SDI.on()      # Send high bits (turned off segments)
        SRCLK.on()    # Pulse shift clock
        SRCLK.off()
    RCLK.on()         # Latch the data
    RCLK.off()

def hc595_shift(data):
    """Shift out one byte to the 74HC595 to control segment lighting."""
    for i in range(8):
        SDI.value(0x80 & (data << i))  # Output next bit
        SRCLK.on()                     # Clock pulse
        SRCLK.off()
    RCLK.on()                          # Latch data to output
    RCLK.off()

def pickDigit(digit):
    """Enable one of the 4 digits on the display by activating its control pin."""
    for pin in placePin:
        pin.off()          # Disable all digits
    placePin[digit].on()   # Enable selected digit

def display():
    """Render the current 4-digit counter value onto the 7-segment display."""
    global counter

    # Units digit
    clearDisplay()
    pickDigit(3)
    hc595_shift(number[counter % 10])

    # Tens digit
    clearDisplay()
    pickDigit(2)
    hc595_shift(number[counter % 100 // 10])

    # Hundreds digit (minus 0x80 to enable decimal point if needed)
    clearDisplay()
    pickDigit(1)
    hc595_shift(number[counter % 1000 // 100] - 0x80)

    # Thousands digit
    clearDisplay()
    pickDigit(0)
    hc595_shift(number[counter % 10000 // 1000])

def stateChange():
    """Handle button-triggered mode changes: start or stop the timer."""
    global gameState, counter, timer1

    # When gameState = 0 → Reset counter and start timer
    if gameState == 0:
        counter = 0           # Reset counter
        time.sleep(1)         # Small delay before start
        timer()               # Start counting

    # When gameState = 1 → Stop the timer
    elif gameState == 1 and timer1 is not None:
        timer1.cancel()       # Stop Timer thread
        time.sleep(1)

    # Toggle between state 0 and 1
    gameState = (gameState + 1) % 2

def loop():
    """Main loop: refresh the display and detect button presses."""
    global counter
    currentState = 0
    lastState = 0

    while True:
        display()                     # Continuously update display
        currentState = sensorPin.value()   # Read button state
        # Detect falling edge: button released → pressed transition
        if (currentState == 0) and (lastState == 1):
            stateChange()             # Trigger state change
        lastState = currentState      # Save state for edge detection

def timer():
    """Timer callback: increments counter every 0.01 seconds using threading.Timer."""
    global counter, timer1
    timer1 = threading.Timer(0.01, timer)  # Create next timer event
    timer1.start()                         # Start timer loop
    counter += 1                           # Increase counter value

try:
    loop()                                 # Run main loop
except KeyboardInterrupt:
    if timer1:
        timer1.cancel()                    # Cleanly stop timer on exit
