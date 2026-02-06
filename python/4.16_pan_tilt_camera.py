#!/usr/bin/env python3
import os, time
from picamera2 import Picamera2, Preview
from fusion_hat.adc import ADC
from fusion_hat.pin import Pin, Mode, Pull
from fusion_hat.servo import Servo

# Servo channels for pan (horizontal) and tilt (vertical)
PAN_CHANNEL, TILT_CHANNEL = 2, 3

# Joystick ADC pins (X/Y axis) and button pin
X_PIN, Y_PIN = "A1", "A0"
BTN_PIN = 17

# Angle limits to protect servos
PAN_MIN, PAN_MAX = -90, 90
TILT_MIN, TILT_MAX = -45, 45

# Deadzone ignores small joystick movement
DEADZONE = 15
MOVE_SPEED = 3
LOOP_DELAY = 0.05

# Photo save directory (works with sudo)
REAL_USER = os.getenv("SUDO_USER") or os.getlogin()
PHOTO_DIR = os.path.join(f"/home/{REAL_USER}", "Pictures", "camera_pan_tilt")
os.makedirs(PHOTO_DIR, exist_ok=True)

# Initialize servos
pan_servo = Servo(PAN_CHANNEL)
tilt_servo = Servo(TILT_CHANNEL)

# Initialize joystick and button (active-low)
x_adc = ADC(X_PIN)
y_adc = ADC(Y_PIN)
joystick_button = Pin(BTN_PIN, mode=Mode.IN, pull=Pull.UP)  # pressed -> 0

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (1280, 720)}))

preview_started = False
photo_count = 1
current_pan = 0
current_tilt = 0
last_button_state = 1  # Used for edge detection

def clamp(v, vmin, vmax):
    # Limit value to a safe range
    return max(vmin, min(vmax, v))

def map_value(value, in_min, in_max, out_min, out_max):
    # Map ADC value to a new range
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def apply_deadzone(v, dz):
    # Ignore small joystick movement
    return 0 if (-dz < v < dz) else v

def read_joystick():
    # Read joystick X/Y position
    x = map_value(x_adc.read(), 0, 4095, -100, 100)
    y = map_value(y_adc.read(), 0, 4095, -100, 100)
    return x, y

def check_button_press():
    # Detect button press (HIGH -> LOW)
    global last_button_state
    current_state = joystick_button.value()
    if last_button_state == 1 and current_state == 0:
        last_button_state = current_state
        return True
    last_button_state = current_state
    return False

def take_photo():
    # Capture and save one photo
    global photo_count
    filename = f"photo_{photo_count:03d}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)
    camera.capture_file(filepath)
    print("Saved:", filepath)
    photo_count += 1

def start_preview_if_available():
    # Start camera preview only if a display is available
    global preview_started
    preview_started = False
    if os.getenv("DISPLAY"):
        try:
            camera.start_preview(Preview.QT)
            preview_started = True
        except Exception:
            preview_started = False

def cleanup():
    # Safely stop camera and release resources
    try:
        camera.stop()
    except Exception:
        pass
    if preview_started:
        try:
            camera.stop_preview()
        except Exception:
            pass
    try:
        camera.close()
    except Exception:
        pass

def main():
    global current_pan, current_tilt

    start_preview_if_available()
    camera.start()

    # Center camera at startup
    pan_servo.angle(0)
    tilt_servo.angle(0)

    try:
        while True:
            # Read joystick and move camera
            x, y = read_joystick()
            x = apply_deadzone(x, DEADZONE)
            y = apply_deadzone(y, DEADZONE)

            new_pan = current_pan + (MOVE_SPEED if x > DEADZONE else -MOVE_SPEED if x < -DEADZONE else 0)
            new_tilt = current_tilt + (MOVE_SPEED if y > DEADZONE else -MOVE_SPEED if y < -DEADZONE else 0)

            new_pan = clamp(new_pan, PAN_MIN, PAN_MAX)
            new_tilt = clamp(new_tilt, TILT_MIN, TILT_MAX)

            if new_pan != current_pan:
                current_pan = new_pan
                pan_servo.angle(current_pan)

            if new_tilt != current_tilt:
                current_tilt = new_tilt
                tilt_servo.angle(current_tilt)

            # Take photo when button is pressed
            if check_button_press():
                take_photo()

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()
