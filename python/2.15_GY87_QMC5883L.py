from fusion_hat.modules.magnetometer import Magnetometer
import math
import time

# Initialize the magnetometer (auto-detects QMC5883L / QMC5883P / HMC5883L / QMC6310)
mag = Magnetometer()

mag_offsets = (OFFSET_X, OFFSET_Y, OFFSET_Z)
mag_scales  = (SCALE_X,  SCALE_Y,  SCALE_Z)

try:
    while True:
        # Read raw magnetic field values (Gauss)
        mx, my, mz = mag.read()

        # Apply hard-iron offset and soft-iron scaling to each axis
        mx = (mx - mag_offsets[0]) * mag_scales[0]   # Corrected X
        my = (my - mag_offsets[1]) * mag_scales[1]   # Corrected Y
        mz = (mz - mag_offsets[2]) * mag_scales[2]   # Corrected Z (not used for heading)

        # Compute heading angle (atan2 gives angle from +X axis)
        heading = math.degrees(math.atan2(my, mx))

        # Convert negative angles into a 0–360° range
        if heading < 0:
            heading += 360

        # Print heading in degrees
        print(f"Heading: {heading:6.2f}°")

        # Small delay between updates
        time.sleep(0.2)

except KeyboardInterrupt:
    # Graceful exit when user presses Ctrl+C
    print("\nHeading measurement stopped by user.")
