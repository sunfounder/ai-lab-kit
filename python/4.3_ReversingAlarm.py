#!/usr/bin/env python3

import time
from fusion_hat.modules import Ultrasonic, Buzzer
from fusion_hat.pin import Pin

# Ultrasonic sensor: Trig -> GPIO 27, Echo -> GPIO 22
sensor = Ultrasonic(trig=Pin(27), echo=Pin(22))

# Buzzer connected to GPIO 17
buzzer = Buzzer(Pin(17))

def get_distance():
    """
    Read distance from ultrasonic sensor and print it.
    Returns distance in centimeters.
    """
    dis = sensor.read()
    print(f"Distance: {dis:.2f} cm")
    return dis


def beep(times, on_time, off_time):
    """
    Make the buzzer beep with given timing.
    """
    for _ in range(times):
        buzzer.on()
        time.sleep(on_time)
        buzzer.off()
        time.sleep(off_time)


def loop():
    """
    Continuously measure distance and control buzzer frequency.
    """
    while True:
        dis = get_distance()

        if dis >= 50:
            # Far distance: buzzer silent
            time.sleep(0.5)

        elif 20 < dis < 50:
            # Medium distance: slow beeping
            beep(times=2, on_time=0.05, off_time=0.2)

        else:
            # Close distance (<= 20 cm): fast beeping
            beep(times=5, on_time=0.05, off_time=0.05)

        time.sleep(0.3)  # Measurement interval


try:
    loop()
except KeyboardInterrupt:
    buzzer.off()
    print("\nProgram stopped, buzzer turned off.")
