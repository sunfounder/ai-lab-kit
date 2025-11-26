#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MPU6050(GY87) + SSD1306 OLED
Gravity-referenced cube with one filled face and user-selectable X/Y flip.
- Accelerometer-only tilt (roll/pitch) relative to an initial baseline
- Orthographic projection (no perspective distortion)
- Front face is filled for orientation feedback
- Two flags at top let you flip X(Y) directions to match your physical setup
"""

import time
import math
from fusion_hat.modules import MPU6050
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board

# ========== User-configurable axis flip ==========
# Flip X/Y to match your physical mounting and perceived motion on the OLED.
# If motion looks reversed on a given axis, set that axis to True.
FLIP_X = False   # True = invert roll direction on display; False = normal
FLIP_Y = False   # True = invert pitch direction on display; False = normal

# ========== OLED setup ==========
WIDTH, HEIGHT = 128, 64
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# Framebuffer
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# ========== IMU ==========
mpu = MPU6050()
# If your driver exposes range setters, you can uncomment:
# mpu.set_accel_range(MPU6050.ACCEL_RANGE_2G)

# ========== Cube model ==========
CUBE_SIZE = 9  # smaller cube for 128x64 OLED

VERTS = [
    (-1, -1, -1), (+1, -1, -1), (+1, +1, -1), (-1, +1, -1),
    (-1, -1, +1), (+1, -1, +1), (+1, +1, +1), (-1, +1, +1),
]
EDGES = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]
FRONT_FACE = [4,5,6,7]  # +Z face gets filled

# ========== Projection (orthographic) ==========
def project_point(p, scale=CUBE_SIZE, cx=WIDTH//2, cy=HEIGHT//2):
    """
    Orthographic projection. We flip the screen Y here so that positive 3D Y
    appears upward on the OLED (more intuitive for tilt).
    """
    x, y, _z = p
    return int(cx + scale * x), int(cy - scale * y)

# ========== Math / orientation helpers ==========
def ema(prev, new, alpha):
    """Exponential smoothing to reduce jitter."""
    return alpha * new + (1.0 - alpha) * prev

def rotate_point(p, roll, pitch, yaw=0.0):
    """Rotate p=(x,y,z) by Rx(roll)*Ry(pitch)*Rz(yaw). Yaw fixed to 0 for gravity-only."""
    x, y, z = p
    # Rx
    cr, sr = math.cos(roll), math.sin(roll)
    y, z = (y*cr - z*sr), (y*sr + z*cr)
    # Ry
    cp, sp = math.cos(pitch), math.sin(pitch)
    x, z = (x*cp + z*sp), (-x*sp + z*cp)
    # Rz (kept for completeness)
    if yaw:
        cz, sz = math.cos(yaw), math.sin(yaw)
        x, y = (x*cz - y*sz), (x*sz + y*cz)
    return (x, y, z)

def accel_to_rp(ax, ay, az):
    """
    Convert accelerometer (g) to roll/pitch in radians (gravity-referenced).
    roll  = rotation around X (right-hand rule)
    pitch = rotation around Y
    """
    g = math.sqrt(ax*ax + ay*ay + az*az) + 1e-9
    axn, ayn, azn = ax / g, ay / g, az / g
    roll  = math.atan2(ayn, azn)
    pitch = math.atan2(-axn, math.sqrt(ayn*ayn + azn*azn))
    return roll, pitch

def draw_cube(roll, pitch, yaw=0.0, annotate=True):
    """Render the cube with one filled face."""
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    rverts = [rotate_point(v, roll, pitch, yaw) for v in VERTS]
    pts = [project_point(v) for v in rverts]

    # Filled front face
    face_xy = [pts[i] for i in FRONT_FACE]
    draw.polygon(face_xy, outline=255, fill=255)

    # Wireframe edges
    for a, b in EDGES:
        x0, y0 = pts[a]
        x1, y1 = pts[b]
        draw.line((x0, y0, x1, y1), fill=255)

    if annotate:
        rdeg = math.degrees(roll)
        pdeg = math.degrees(pitch)
        draw.text((2, 2), f"R:{rdeg:+.0f}  P:{pdeg:+.0f}", font=font, fill=255)
        # draw.text((2, 12), "Yaw: n/a (gravity only)", font=font, fill=255)

# ========== Baseline & smoothing ==========
baseline_set = False
roll0 = pitch0 = 0.0

ROLL_EMA  = 0.20
PITCH_EMA = 0.20
roll_disp = pitch_disp = 0.0

try:
    while True:
        # Read accelerometer (in g)
        ax, ay, az = mpu.get_accel_data()

        # Absolute roll/pitch from gravity
        roll_abs, pitch_abs = accel_to_rp(ax, ay, az)

        # First reading defines baseline (0°,0°)
        if not baseline_set:
            roll0, pitch0 = roll_abs, pitch_abs
            baseline_set = True

        # Relative orientation
        roll_rel  = roll_abs  - roll0
        pitch_rel = pitch_abs - pitch0

        # Apply user flips to match perceived direction on OLED
        if FLIP_X:
            roll_rel = -roll_rel
        if FLIP_Y:
            pitch_rel = -pitch_rel

        # Smooth
        roll_disp  = ema(roll_disp,  roll_rel,  ROLL_EMA)
        pitch_disp = ema(pitch_disp, pitch_rel, PITCH_EMA)

        # Render (yaw fixed to 0 in gravity-only mode)
        draw_cube(roll_disp, pitch_disp, yaw=0.0, annotate=True)

        # Show on OLED
        oled.image(image)
        oled.show()

        time.sleep(0.02)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("\nExited.")
