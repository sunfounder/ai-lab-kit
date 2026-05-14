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
markTemp = None

last_button_state = 0
last_press_time = 0
_last_print = 0.0

DEBOUNCE_TIME = 0.3
PRINT_INTERVAL = 1.0
MANUAL_HOLD_TIME = 2.0
TEMP_THRESHOLD = 5.0


def temperature(samples=5, delay=0.01):
    """Read thermistor temperature and return average Celsius value."""

    vals = []

    for _ in range(samples):
        analogVal = thermistor.read()
        Vr = 3.3 * float(analogVal) / 4095.0

        if Vr <= 0 or (3.3 - Vr) <= 0.1:
            sleep(delay)
            continue

        Rt = 10000.0 * Vr / (3.3 - Vr)

        if Rt <= 0:
            sleep(delay)
            continue

        tempK = 1.0 / (
            ((math.log(Rt / 10000.0)) / 3950.0)
            + (1.0 / (273.15 + 25.0))
        )

        vals.append(tempK - 273.15)
        sleep(delay)

    if not vals:
        return None

    return sum(vals) / len(vals)


def motor_run(lv):
    """Set motor power according to level."""

    lv = max(0, min(4, lv))
    power_table = [0, 25, 50, 75, 100]
    motor.power(power_table[lv])

    return lv


def read_button():
    """Read current button state."""

    try:
        return BtnPin.value()
    except TypeError:
        return BtnPin.value


def main():
    """Main loop for button control and temperature auto adjustment."""

    global level, markTemp, last_button_state, last_press_time, _last_print

    while markTemp is None:
        markTemp = temperature()
        sleep(0.1)

    while True:
        now = time()

        button_state = read_button()

        if button_state == 1 and last_button_state == 0:
            if now - last_press_time >= DEBOUNCE_TIME:
                old = level
                level = (level + 1) % 5
                last_press_time = now

                currentTemp = temperature()
                if currentTemp is not None:
                    markTemp = currentTemp

                level = motor_run(level)

                print(
                    f"[Button] {old} -> {level} | "
                    f"Power: {0 if level == 0 else level * 25}%"
                )

        last_button_state = button_state

        currentTemp = temperature()

        if currentTemp is None:
            print("Sensor read failed.")
            sleep(0.5)
            continue

        auto_allowed = (now - last_press_time) >= MANUAL_HOLD_TIME

        if auto_allowed and level != 0:
            diff = currentTemp - markTemp

            if diff >= TEMP_THRESHOLD:
                level = min(4, level + 1)
                markTemp = currentTemp
                level = motor_run(level)
                print(f"[Auto] Temp up -> Level {level}")

            elif diff <= -TEMP_THRESHOLD:
                level = max(0, level - 1)
                markTemp = currentTemp
                level = motor_run(level)
                print(f"[Auto] Temp down -> Level {level}")

        if now - _last_print >= PRINT_INTERVAL:
            print(
                f"Temp: {currentTemp:.2f} C | "
                f"Mark: {markTemp:.2f} C | "
                f"Level: {level}"
            )
            _last_print = now

        level = motor_run(level)

        sleep(0.05)


try:
    main()

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    motor.stop()
    sleep(0.1)