#!/usr/bin/env python3
"""
Rotary Encoder (simple polling)
- 1 physical detent (click) = 1 count
- Clean output: updates on the same line (no repeated lines)
"""

from fusion_hat.pin import Pin, Mode, Pull
import time

# GPIO pins (BCM numbering)
CLK_PIN = 17
DT_PIN  = 4
SW_PIN  = 27

# Initialize pins with internal pull-ups
clk = Pin(CLK_PIN, mode=Mode.IN, pull=Pull.UP)
dt  = Pin(DT_PIN,  mode=Mode.IN, pull=Pull.UP)
sw  = Pin(SW_PIN,  mode=Mode.IN, pull=Pull.UP)  # Button is active LOW

raw = 0                 # Raw quadrature transitions
last_clk = clk.value()  # Previous CLK state
last_detent = None      # Last displayed detent value

print("Rotate the knob. Press the button to reset. CTRL + C to exit.")
try:
    while True:
        c = clk.value()
        if c != last_clk:
            # Direction: DT != CLK means one direction, else the other
            raw += 1 if dt.value() != c else -1

            # Most encoders generate 2 transitions per detent (click)
            detent = raw // 2

            # Only update output when the detent value changes
            if detent != last_detent:
                print(f"\rCounter: {detent}   ", end="", flush=True)
                last_detent = detent

            last_clk = c

        # Reset when button is pressed
        if sw.value() == 0:
            raw = 0
            detent = 0
            print("\rCounter: 0   ", end="", flush=True)
            last_detent = 0
            time.sleep(0.25)  # Button debounce

        time.sleep(0.001)  # Polling interval (1 ms)

except KeyboardInterrupt:
    print("\nExit")
