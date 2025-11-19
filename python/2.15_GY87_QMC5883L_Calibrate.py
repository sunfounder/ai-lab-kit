#!/usr/bin/env python3
from fusion_hat.modules import Compass
import time
import math

com = Compass()

print("\n==================== QMC5883L Calibration Tool ====================")
print("Rotate your GY-87 module slowly in ALL directions for 15 seconds.")
print("Try to draw a big 3D sphere motion: roll, pitch, yaw.\n")
print("Calibration starting in 3 seconds...\n")
time.sleep(3)

# Initialize min/max
x_min, x_max = 9999, -9999
y_min, y_max = 9999, -9999
z_min, z_max = 9999, -9999

start_time = time.time()
CALIBRATION_DURATION = 15  # seconds

print("Calibrating... KEEP ROTATING the sensor!\n")

while time.time() - start_time < CALIBRATION_DURATION:
    x, y, z, _ = com.read()

    # Track min/max for each axis
    x_min = min(x_min, x)
    x_max = max(x_max, x)

    y_min = min(y_min, y)
    y_max = max(y_max, y)

    z_min = min(z_min, z)
    z_max = max(z_max, z)

    print(f"X[{x_min},{x_max}] Y[{y_min},{y_max}] Z[{z_min},{z_max}] ", end="\r")
    time.sleep(0.05)

print("\n\n==================== Calibration Complete ====================")

# Calculate OFFSETS (Hard iron correction)
offset_x = (x_max + x_min) / 2
offset_y = (y_max + y_min) / 2
offset_z = (z_max + z_min) / 2

# Calculate SCALES (Soft iron correction)
scale_x = (x_max - x_min) / 2
scale_y = (y_max - y_min) / 2
scale_z = (z_max - z_min) / 2

avg_scale = (scale_x + scale_y + scale_z) / 3

scale_x = avg_scale / scale_x
scale_y = avg_scale / scale_y
scale_z = avg_scale / scale_z

print("\nCopy these lines into your project:\n")

print(f"compass_offsets = ({offset_x:.2f}, {offset_y:.2f}, {offset_z:.2f})")
print(f"compass_scales  = ({scale_x:.4f}, {scale_y:.4f}, {scale_z:.4f})")

print("\nExample usage in your main program:")
print("""
x, y, z, angle = com.read()

# Apply calibration
x = (x - compass_offsets[0]) * compass_scales[0]
y = (y - compass_offsets[1]) * compass_scales[1]
z = (z - compass_offsets[2]) * compass_scales[2]

# Compute corrected heading
heading = math.degrees(math.atan2(y, x))
if heading < 0:
    heading += 360
print("Heading:", heading)
""")

print("\nDone.\n")
