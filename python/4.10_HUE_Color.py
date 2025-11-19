#!/usr/bin/env python3
import time
import colorsys
import board
import neopixel_spi as neopixel
from fusion_hat import Rotary_Encoder, Pin
from signal import pause

# ---------------------------
# NeoPixel (SPI) setup
# ---------------------------
LED_COUNT = 12
PIXEL_ORDER = neopixel.GRB

spi = board.SPI()
strip = neopixel.NeoPixel_SPI(
    spi,
    LED_COUNT,
    pixel_order=PIXEL_ORDER,
    auto_write=False,
)
time.sleep(0.01)
strip.fill(0)
strip.show()

# ---------------------------
# Rotary Encoder + Button
# ---------------------------
# CLK -> GPIO17, DT -> GPIO4, SW -> GPIO27 (pull-up)
encoder = Rotary_Encoder(clk=17, dt=4)
sw = Pin(27, Pin.IN, pull=Pin.PULL_UP)

# You can tweak how many encoder steps you want per full hue cycle.
# If your encoder has 24 'detents', 24 or 48 feel good.
STEPS_PER_CYCLE = 120  # higher = finer control

_last_hue_idx = 0

def hue_to_rgb(h: float):
    """h in [0.0, 1.0] -> (R, G, B) 0..255"""
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def apply_color_from_steps(steps: int):
    global _last_hue_idx
    # Map steps to [0..STEPS_PER_CYCLE-1]
    hue_idx = steps % STEPS_PER_CYCLE
    if hue_idx == _last_hue_idx:
        return  # no visual update needed
    _last_hue_idx = hue_idx

    hue = hue_idx / STEPS_PER_CYCLE  # 0.0..1.0
    color = hue_to_rgb(hue)

    strip.fill(color)
    strip.show()
    print(f"Hue: {int(hue * 360)}°, Steps: {steps}, Color: {color}")

def rotary_change():
    apply_color_from_steps(encoder.steps())

def reset_counter():
    encoder.reset()
    apply_color_from_steps(0)
    print("Counter reset (Hue -> 0°)")

# Event bindings
encoder.when_rotated = rotary_change
sw.when_activated = reset_counter

# Initialize to 0°
apply_color_from_steps(0)

print("Rotate to change hue. Press button to reset. CTRL+C to exit.")
try:
    pause()
except KeyboardInterrupt:
    pass
finally:
    # Turn off LEDs on exit
    strip.fill(0)
    strip.show()
    print("Exited and cleared LEDs.")
