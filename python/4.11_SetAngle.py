#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fusion_hat.adc import ADC
from fusion_hat.servo import Servo
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board, time

# ==== OLED setup ====
WIDTH, HEIGHT = 128, 64
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# Framebuffer for drawing
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def text_size(font, text):
    l, t, r, b = font.getbbox(text)
    return (r - l, b - t)

# ==== Servo & potentiometer ====
servo = Servo('P0')   # servo on port P0
pot   = ADC('A0')     # potentiometer on A0 (0..4095)

def linear_map(x, in_min, in_max, out_min, out_max):
    """Map x from one range to another."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# ---- bar layout (centered pointer, zero at screen center) ----
BAR_TOP     = 40              # y of the bar
BAR_HEIGHT  = 10
BAR_MARGINX = 6
BAR_WIDTH   = WIDTH - BAR_MARGINX * 2
BAR_CENTERX = BAR_MARGINX + BAR_WIDTH // 2

def draw_bar(angle_deg):
    """
    Draw a centered horizontal bar with a moving pointer.
    -90° maps to the far left, +90° to the far right.
    0° is at the bar center.
    """
    # Clear screen
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Title
    title = "Servo Angle"
    tw, th = text_size(font, title)
    draw.text(((WIDTH - tw) // 2, 4), title, font=font, fill=255)

    # Numeric angle
    txt = f"{angle_deg:>4} deg"
    nw, nh = text_size(font, txt)
    draw.text(((WIDTH - nw) // 2, 20), txt, font=font, fill=255)

    # Static bar background
    draw.rectangle(
        (BAR_MARGINX, BAR_TOP, BAR_MARGINX + BAR_WIDTH - 1, BAR_TOP + BAR_HEIGHT),
        outline=255, fill=0
    )

    # Ticks: left (-90), center (0), right (+90)
    for x in (BAR_MARGINX, BAR_CENTERX, BAR_MARGINX + BAR_WIDTH - 1):
        draw.line((x, BAR_TOP - 3, x, BAR_TOP + BAR_HEIGHT + 3), fill=255)

    # Map angle (-90..90) to bar position
    pos = int(linear_map(angle_deg, -90, 90, BAR_MARGINX, BAR_MARGINX + BAR_WIDTH - 1))

    # Pointer: a solid vertical line
    draw.line((pos, BAR_TOP - 2, pos, BAR_TOP + BAR_HEIGHT + 2), fill=255)

    # Optional: filled segment from center to pointer (visualize direction)
    if pos >= BAR_CENTERX:
        draw.rectangle((BAR_CENTERX, BAR_TOP + 1, pos, BAR_TOP + BAR_HEIGHT - 1), outline=0, fill=255)
    else:
        draw.rectangle((pos, BAR_TOP + 1, BAR_CENTERX, BAR_TOP + BAR_HEIGHT - 1), outline=0, fill=255)

try:
    while True:
        # Read potentiometer (0..4095) and map to angle (-90..90)
        raw = pot.read()
        angle = int(linear_map(raw, 0, 4095, -90, 90))

        # Drive servo
        servo.angle(angle)

        # Draw UI and push to OLED
        draw_bar(angle)
        oled.image(image)
        oled.show()

        # Optional: print for debugging
        # print(f"pot={raw:4d} -> angle={angle:4d} deg")

        time.sleep(0.05)  # ~20 FPS

except KeyboardInterrupt:
    # Graceful cleanup
    servo.angle(0)
    oled.fill(0)
    oled.show()
    print("\nExited.")
