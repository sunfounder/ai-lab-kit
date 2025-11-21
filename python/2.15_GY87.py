#!/usr/bin/env python3
"""
Read data from all three sensors on the GY-87 module:
- BMP180: temperature, pressure, altitude
- MPU6050: temperature, accelerometer, gyroscope
- QMC5883L (via Magnetometer): compass heading

Gracefully exits when Ctrl+C is pressed.
"""

from smbus2 import SMBus
from time import sleep
import math

# Import Fusion HAT sensor modules
from fusion_hat.modules import bmp180, MPU6050
from fusion_hat.modules.magnetometer import Magnetometer


def main():
    # --- Initialize BMP180 (pressure / temperature / altitude) ---
    bus = SMBus(1)  # I2C bus 1 on Raspberry Pi
    bmp_sensor = bmp180.BMP180(bus, oversampling=3)

    # --- Initialize MPU6050 (accelerometer / gyroscope / temperature) ---
    mpu = MPU6050()

    # --- Initialize Magnetometer (QMC5883L / others auto-detected) ---
    mag = Magnetometer()

    # TODO: replace these with your own calibration values
    # from the QMC5883L calibration script.
    mag_offsets = (0.0, 0.0, 0.0)   # (OFFSET_X, OFFSET_Y, OFFSET_Z)
    mag_scales  = (1.0, 1.0, 1.0)   # (SCALE_X,  SCALE_Y,  SCALE_Z)

    print("Starting combined GY-87 sensor readout...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # ---------- BMP180 readings ----------
            temp_bmp, pressure, altitude = bmp_sensor.read()

            # ---------- MPU6050 readings ----------
            temp_mpu = mpu.get_temp()
            acc_x, acc_y, acc_z = mpu.get_accel_data()
            gyro_x, gyro_y, gyro_z = mpu.get_gyro_data()

            # ---------- Magnetometer / heading ----------
            mag_data = mag.read()
            if mag_data is not None:
                mx_raw, my_raw, mz_raw = mag_data

                # Apply hard-iron and soft-iron calibration
                mx = (mx_raw - mag_offsets[0]) * mag_scales[0]
                my = (my_raw - mag_offsets[1]) * mag_scales[1]
                mz = (mz_raw - mag_offsets[2]) * mag_scales[2]

                # Heading in degrees (0–360)
                heading = math.degrees(math.atan2(my, mx))
                if heading < 0:
                    heading += 360.0
            else:
                mx = my = mz = 0.0
                heading = float("nan")

            # ---------- Print all readings ----------
            print(
                f"BMP180: Temp={temp_bmp:6.2f} °C"
                f" | Pressure={pressure:10.2f} Pa"
                f" | Alt={altitude:7.2f} m"
            )
            print(
                f"MPU6050: Temp={temp_mpu:6.2f} °C"
                f" | ACC=({acc_x:7.4f}g, {acc_y:7.4f}g, {acc_z:7.4f}g)"
                f" | GYRO=({gyro_x:7.2f}dps, {gyro_y:7.2f}dps, {gyro_z:7.2f}dps)"
            )
            print(
                f"Magnetometer: mx={mx:7.4f} G, my={my:7.4f} G, mz={mz:7.4f} G"
                f" | Heading={heading:6.2f}°"
            )
            print("-" * 80)

            sleep(0.5)

    except KeyboardInterrupt:
        print("\nExiting combined GY-87 sensor program...")


if __name__ == "__main__":
    main()
