#!/usr/bin/env python3
"""
Magnetometer Calibration Tool
Supports: QMC5883L / QMC5883P / QMC6310 / HMC5883L

Rotate the GY-87 module slowly in all directions to collect
raw magnetic field extremes for offset & scale calibration.
"""

import time
import math
from fusion_hat.modules.magnetometer import Magnetometer

CALIB_TIME = 20   # Duration of sample collection (seconds)


def main():
    # Auto-detect magnetometer on I2C bus
    mag = Magnetometer()
    mag_type = mag.get_type()

    if not mag_type:
        print("❌ No magnetometer detected. Check wiring or I2C settings.")
        return

    print(f"✅ Magnetometer detected: {mag_type}")
    print("\n==================== Calibration Instructions ====================")
    print(" Slowly rotate the sensor in ALL directions for 20 seconds.")
    print(" Try to draw a large 3D sphere.\n")
    print(" Calibration starts in 3 seconds...\n")
    time.sleep(3)

    # Initialize min/max capture variables
    x_min, x_max =  9999.0, -9999.0
    y_min, y_max =  9999.0, -9999.0
    z_min, z_max =  9999.0, -9999.0

    print("▶ Collecting samples... KEEP ROTATING!\n")
    start = time.time()

    try:
        while time.time() - start < CALIB_TIME:
            data = mag.read()
            if data is None:
                continue  # Skip if sensor failed to read

            x, y, z = data

            # Update min/max ranges
            x_min, x_max = min(x_min, x), max(x_max, x)
            y_min, y_max = min(y_min, y), max(y_max, y)
            z_min, z_max = min(z_min, z), max(z_max, z)

            # Live feedback
            print(
                f"X[{x_min:+.4f},{x_max:+.4f}]  "
                f"Y[{y_min:+.4f},{y_max:+.4f}]  "
                f"Z[{z_min:+.4f},{z_max:+.4f}] ",
                end="\r"
            )
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n\n⚠ Calibration interrupted\n")
        return

    print("\n\n==================== Calibration Complete ====================\n")

    # Hard-iron offsets (center of ellipsoid)
    offset_x = (x_max + x_min) / 2
    offset_y = (y_max + y_min) / 2
    offset_z = (z_max + z_min) / 2

    # Soft-iron scaling factors (normalize ellipsoid → sphere)
    scale_x = (x_max - x_min) / 2
    scale_y = (y_max - y_min) / 2
    scale_z = (z_max - z_min) / 2

    avg = (scale_x + scale_y + scale_z) / 3  # average radius

    # Convert to scale multipliers
    scale_x = avg / scale_x if scale_x != 0 else 1.0
    scale_y = avg / scale_y if scale_y != 0 else 1.0
    scale_z = avg / scale_z if scale_z != 0 else 1.0

    # Output calibration results
    print("Paste the following into your project:\n")
    print(f"mag_offsets = ({offset_x:.6f}, {offset_y:.6f}, {offset_z:.6f})")
    print(f"mag_scales  = ({scale_x:.6f}, {scale_y:.6f}, {scale_z:.6f})\n")

    print("🎉 Calibration done.\n")


if __name__ == "__main__":
    main()
