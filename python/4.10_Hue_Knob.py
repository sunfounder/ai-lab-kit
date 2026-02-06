#!/usr/bin/env python3
import time
import colorsys
import board
import neopixel_spi as neopixel
from fusion_hat.pin import Pin, Mode, Pull

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
# Rotary Encoder (polling, stable)
# ---------------------------
CLK_PIN = 17
DT_PIN  = 4
SW_PIN  = 27

clk = Pin(CLK_PIN, mode=Mode.IN, pull=Pull.UP)
dt  = Pin(DT_PIN,  mode=Mode.IN, pull=Pull.UP)
sw  = Pin(SW_PIN,  mode=Mode.IN, pull=Pull.UP)  # button active LOW

# How many "detents" (clicks) to complete a full hue cycle (0~360).
# Bigger value = finer control.
DETENTS_PER_CYCLE = 120

# Many encoders generate 2 transitions per detent (sometimes 4).
# If your counting feels too fast/too slow, try 2 or 4.
TRANSITIONS_PER_DETENT = 2

raw = 0
last_clk = clk.value()
last_detent = None
last_hue_idx = None

def hue_to_rgb(h: float):
    """h in [0.0, 1.0] -> (R, G, B) 0..255"""
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def apply_color_from_detent(detent: int):
    """Update LED color only when detent changes."""
    global last_hue_idx

    hue_idx = detent % DETENTS_PER_CYCLE
    if hue_idx == last_hue_idx:
        return

    last_hue_idx = hue_idx
    hue = hue_idx / DETENTS_PER_CYCLE
    color = hue_to_rgb(hue)

    strip.fill(color)
    strip.show()

    # Print compact info (optional)
    print(f"\rHue: {int(hue * 360):3d}°  Detent: {detent:6d}  RGB: {color}   ", end="", flush=True)

def reset_all():
    """Reset counter and hue to 0."""
    global raw, last_detent, last_hue_idx
    raw = 0
    last_detent = 0
    last_hue_idx = None
    apply_color_from_detent(0)

# Initialize to 0°
reset_all()
print("\nRotate to change hue. Press button to reset. CTRL+C to exit.")

try:
    while True:
        c = clk.value()
        if c != last_clk:
            # Direction: DT != CLK means one direction, else the other
            raw += 1 if dt.value() != c else -1

            detent = raw // TRANSITIONS_PER_DETENT
            if detent != last_detent:
                last_detent = detent
                apply_color_from_detent(detent)

            last_clk = c

        # Button reset (active LOW)
        if sw.value() == 0:
            reset_all()
            # debounce + wait release
            time.sleep(0.05)
            while sw.value() == 0:
                time.sleep(0.01)

        time.sleep(0.001)

except KeyboardInterrupt:
    pass
finally:
    strip.fill(0)
    strip.show()
    print("\nExited and cleared LEDs.")
