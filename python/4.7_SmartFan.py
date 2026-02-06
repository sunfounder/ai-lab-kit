#!/usr/bin/env python3

from fusion_hat.motor import Motor
from fusion_hat.pin import Pin, Mode, Pull
from fusion_hat.adc import ADC
from time import sleep, time
import math

BtnPin = Pin(22, mode=Mode.IN, pull=Pull.DOWN)
motor = Motor("M0")
thermistor = ADC("A3")

level = 0
currentTemp = None
markTemp = None

PRINT_INTERVAL = 1.0
_last_print = 0.0

button_event = False  # flag: button was pressed

def temperature(samples=5, delay=0.01):
    """Read thermistor multiple times and return averaged Celsius (float) or None."""
    vals = []
    for _ in range(samples):
        analogVal = thermistor.read()
        Vr = 3.3 * float(analogVal) / 4095.0
        if (3.3 - Vr) <= 0.1:
            return None
        Rt = 10000.0 * Vr / (3.3 - Vr)
        tempK = 1.0 / (((math.log(Rt / 10000.0)) / 3950.0) + (1.0 / (273.15 + 25.0)))
        vals.append(tempK - 273.15)
        sleep(delay)
    return sum(vals) / len(vals)

def motor_run(lv):
    lv = max(0, min(4, lv))
    motor.power(0 if lv == 0 else lv * 25)
    return lv

def changeLevel():
    """Button press: cycle level 0~4 and set a flag for main loop to print."""
    global level, button_event
    level = (level + 1) % 5
    button_event = True

BtnPin.when_activated = changeLevel

def main():
    global level, currentTemp, markTemp, _last_print, button_event

    markTemp = temperature()
    while True:
        currentTemp = temperature()
        if currentTemp is None:
            print("Sensor read failed. Please check the sensor.")
            sleep(0.5)
            continue

        # Handle button event in main loop (stable timing)
        if button_event:
            button_event = False
            markTemp = currentTemp
            print(f"[Button] Level -> {level} | Temp: {currentTemp:.2f} °C | Mark: {markTemp:.2f} °C")

        # Periodic temperature print
        now = time()
        if now - _last_print >= PRINT_INTERVAL:
            if markTemp is None:
                markTemp = currentTemp
            print(f"Temp: {currentTemp:.2f} °C | Mark: {markTemp:.2f} °C | Level: {level}")
            _last_print = now

        # Auto adjust level based on ±5°C
        if markTemp is None:
            markTemp = currentTemp

        if level != 0:
            diff = currentTemp - markTemp
            if diff <= -5:
                level = max(0, level - 1)
                markTemp = currentTemp
                print(f"[Auto] Temp down -> Level {level} (Temp: {currentTemp:.2f} °C)")
            elif diff >= 5:
                level = min(4, level + 1)
                markTemp = currentTemp
                print(f"[Auto] Temp up   -> Level {level} (Temp: {currentTemp:.2f} °C)")

        level = motor_run(level)
        sleep(0.5)

try:
    main()
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    motor.stop()
    sleep(0.1)
