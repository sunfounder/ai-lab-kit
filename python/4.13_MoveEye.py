#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Joystick-controlled eye on a 128x64 SSD1306 OLED.
- Joystick X/Y on ADC A0/A1 (0..4095)
- Pupil moves inside a drawn eye based on joystick deflection
- English-only comments
"""

import time
from math import sqrt
from fusion_hat.adc import ADC
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board

# ===== OLED setup =====
WIDTH, HEIGHT = 128, 64
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# Framebuffer for drawing
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# ===== Joystick (two ADC channels) =====
# Adjust channel names to your hardware if needed (e.g., 'A1','A2')
joy_x = ADC('A0')  # X axis
joy_y = ADC('A1')  # Y axis

# ===== Mapping helpers =====
def linear_map(x, in_min, in_max, out_min, out_max):
    """Map x from one range to another (float)."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(v, vmin, vmax):
    """Clamp v to [vmin, vmax]."""
    return vmax if v > vmax else vmin if v < vmin else v

# ===== Eye layout (tweak to your taste) =====
# Eye center and sizes
EYE_CX, EYE_CY = WIDTH // 2, HEIGHT // 2
EYE_W, EYE_H   = 90, 48          # outer ellipse width/height (sclera)
IRIS_R         = 10              # iris radius (white ring, optional)
PUPIL_R        = 7               # pupil radius (black)
BORDER         = 2               # outer eye border thickness in pixels

# Pupil movement limits (keep pupil inside sclera with some margin)
# We'll approximate the inside of the eye as an ellipse and limit the pupil center
PUPIL_MARGIN = PUPIL_R + 3
MAX_X = (EYE_W // 2) - PUPIL_MARGIN
MAX_Y = (EYE_H // 2) - PUPIL_MARGIN

# ===== Joystick normalization settings =====
# Joystick nominal center near 2048; define a dead zone and smoothing
ADC_MIN, ADC_MAX = 0.0, 4095.0
ADC_CENTER_X     = 2048.0
ADC_CENTER_Y     = 2048.0
DEADZONE         = 120.0     # +/- counts considered centered (no move)
SMOOTH_ALPHA     = 0.35      # EMA smoothing factor for normalized values

# State for smoothing
nx_smooth, ny_smooth = 0.0, 0.0

def read_joystick_norm():
    """
    Read joystick and produce normalized values in [-1, 1] for X and Y,
    with dead zone and smoothing. Y is inverted so up is positive.
    """
    global nx_smooth, ny_smooth

    rx = float(joy_x.read())
    ry = float(joy_y.read())

    # Raw offset from center
    dx = rx - ADC_CENTER_X
    dy = ry - ADC_CENTER_Y

    # Deadzone
    if abs(dx) < DEADZONE: dx = 0.0
    if abs(dy) < DEADZONE: dy = 0.0

    # Normalize to [-1, 1]
    # Use the larger of (center-min) / (max-center) to reduce asymmetry
    span_x_pos = ADC_MAX - ADC_CENTER_X
    span_x_neg = ADC_CENTER_X - ADC_MIN
    span_y_pos = ADC_MAX - ADC_CENTER_Y
    span_y_neg = ADC_CENTER_Y - ADC_MIN

    nx = dx / (span_x_pos if dx >= 0 else span_x_neg) if dx != 0 else 0.0
    ny = dy / (span_y_pos if dy >= 0 else span_y_neg) if dy != 0 else 0.0

    # Invert Y so pushing stick up moves pupil up
    ny = -ny

    # Clamp to [-1, 1]
    nx = clamp(nx, -1.0, 1.0)
    ny = clamp(ny, -1.0, 1.0)

    # Exponential smoothing
    nx_smooth = SMOOTH_ALPHA * nx + (1.0 - SMOOTH_ALPHA) * nx_smooth
    ny_smooth = SMOOTH_ALPHA * ny + (1.0 - SMOOTH_ALPHA) * ny_smooth

    # Re-clamp after smoothing
    nx_smooth_clamped = clamp(nx_smooth, -1.0, 1.0)
    ny_smooth_clamped = clamp(ny_smooth, -1.0, 1.0)
    return nx_smooth_clamped, ny_smooth_clamped

def pupil_target_from_norm(nx, ny):
    """
    Map normalized joystick values [-1..1] to a legal pupil center inside the eye.
    We limit by ellipse equation (x/MAX_X)^2 + (y/MAX_Y)^2 <= 1.
    If outside, project back to the ellipse boundary.
    """
    # Proposed offsets
    px = nx * MAX_X
    py = ny * MAX_Y

    # Check ellipse boundary; if outside, project back
    if (px*px) / (MAX_X*MAX_X) + (py*py) / (MAX_Y*MAX_Y) > 1.0:
        # Normalize direction to ellipse edge
        # Scale so that (px/MAX_X, py/MAX_Y) lies on unit circle
        k = 1.0 / sqrt((px*px) / (MAX_X*MAX_X) + (py*py) / (MAX_Y*MAX_Y))
        px *= k
        py *= k

    # Final pupil center
    cx = int(EYE_CX + px)
    cy = int(EYE_CY + py)
    return cx, cy

def draw_eye(cx, cy):
    """
    Draw the eye (sclera outline + filled sclera) and the pupil at (cx, cy).
    Monochrome: 1 = white (ON), 0 = black (OFF).
    """
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    # Outer eye (white sclera with border)
    # Outer ellipse
    x0 = EYE_CX - EYE_W // 2
    y0 = EYE_CY - EYE_H // 2
    x1 = EYE_CX + EYE_W // 2
    y1 = EYE_CY + EYE_H // 2

    # Border: draw multiple outlines to simulate thickness
    for t in range(BORDER):
        draw.ellipse((x0 - t, y0 - t, x1 + t, y1 + t), outline=1, fill=0)
    # Filled sclera (white)
    draw.ellipse((x0 + 1, y0 + 1, x1 - 1, y1 - 1), outline=0, fill=1)

    # Optional iris ring (white ring around pupil); comment out if undesired
    if IRIS_R > PUPIL_R:
        draw.ellipse((cx - IRIS_R, cy - IRIS_R, cx + IRIS_R, cy + IRIS_R), outline=0, fill=0)
        draw.ellipse((cx - (IRIS_R - 2), cy - (IRIS_R - 2), cx + (IRIS_R - 2), cy + (IRIS_R - 2)), outline=0, fill=1)

    # Pupil (black)
    draw.ellipse((cx - PUPIL_R, cy - PUPIL_R, cx + PUPIL_R, cy + PUPIL_R), outline=0, fill=0)

    # Optional text (for debugging)
    # txt = "X/Y"
    # tw, th = font.getsize(txt)
    # draw.text((2, 2), txt, font=font, fill=1)

def main():
    try:
        while True:
            # Read joystick → normalized [-1..1]
            nx, ny = read_joystick_norm()
            # Compute pupil center within eye bounds
            cx, cy = pupil_target_from_norm(nx, ny)
            # Draw and show
            draw_eye(cx, cy)
            oled.image(image)
            oled.show()
            time.sleep(0.02)  # ~50 FPS
    except KeyboardInterrupt:
        oled.fill(0)
        oled.show()
        print("\nExited.")

if __name__ == "__main__":
    main()
