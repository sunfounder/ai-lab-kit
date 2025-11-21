#!/usr/bin/env python3
"""
Read temperature, pressure, and altitude
from the BMP180 sensor on the GY-87 module.
Gracefully exits when Ctrl+C is pressed.
"""

# Import SMBus for I2C communication
from smbus2 import SMBus

# Import the BMP180 module from Fusion HAT
from fusion_hat.modules import bmp180

# Import sleep for timing delays
from time import sleep


def main():
    # Create an I2C bus object
    # SMBus(1) corresponds to I2C bus 1 on Raspberry Pi
    bus = SMBus(1)

    # Initialize the BMP180 sensor
    # Oversampling=3 gives highest accuracy (slower sampling)
    sensor = bmp180.BMP180(bus, oversampling=3)

    try:
        # Continuous loop to read and print sensor values
        while True:
            # Read temperature (°C), pressure (Pa), altitude (m)
            temp, pressure, altitude = sensor.read()

            # Print formatted readings to the terminal
            print(
                f"Temp: {temp:6.2f} °C",
                f" | Pressure: {pressure:10.2f} Pa",
                f" | Altitude: {altitude:7.2f} m"
            )

            # Delay between readings
            sleep(0.5)

    except KeyboardInterrupt:
        # Handles CTRL+C interruption safely
        print("\nExiting program...")


# Standard Python entry point check
if __name__ == "__main__":
    main()
