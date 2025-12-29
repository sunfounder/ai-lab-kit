#!/usr/bin/env python3
"""
Pan-Tilt Camera Control System
Control camera direction with joystick, take photos with joystick button
Simple version for beginners
"""

import os
import time
from fusion_hat.adc import ADC
from fusion_hat.pin import Pin, Mode, Pull
from fusion_hat.servo import Servo
from picamera2 import Picamera2, Preview

# ========== HARDWARE SETTINGS ==========
# Servo channels for pan (horizontal) and tilt (vertical)
PAN_CHANNEL = 2
TILT_CHANNEL = 3

# Joystick ADC pins
X_PIN = 'A1'  # Horizontal control
Y_PIN = 'A0'  # Vertical control

# Joystick button pin
BTN_PIN = 17

# ========== CONTROL SETTINGS ==========
# Angle limits for safety
PAN_MIN = -90    # Leftmost position
PAN_MAX = 90     # Rightmost position
TILT_MIN = -45   # Downward limit
TILT_MAX = 45    # Upward limit

# Joystick deadzone (ignore small movements)
DEADZONE = 15

# Movement speed (degrees per update)
MOVE_SPEED = 3

# ========== CAMERA SETTINGS ==========
# Photo save location
REAL_USER = os.getenv("SUDO_USER") or os.getlogin()
USER_HOME = f"/home/{REAL_USER}"
PHOTO_DIR = os.path.join(USER_HOME, "Pictures", "camera_pan_tilt")
os.makedirs(PHOTO_DIR, exist_ok=True)

# ========== INITIALIZE HARDWARE ==========
print("Initializing Pan-Tilt Camera System...")

# Initialize servos
print("Setting up servos...")
pan_servo = Servo(PAN_CHANNEL)   # Horizontal rotation servo
tilt_servo = Servo(TILT_CHANNEL) # Vertical rotation servo

# Initialize joystick
print("Setting up joystick...")
joystick_button = Pin(BTN_PIN, mode=Mode.IN, pull=Pull.UP)
x_adc = ADC(X_PIN)
y_adc = ADC(Y_PIN)

# Initialize camera
print("Setting up camera...")
camera = Picamera2()
# Configure camera for preview
camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
camera.configure(camera_config)

# ========== GLOBAL VARIABLES ==========
# Current camera angles
current_pan = 0    # Horizontal angle (-90 to 90)
current_tilt = 0   # Vertical angle (-45 to 45)

# Photo counter
photo_count = 1

# Program running flag
running = True

# Previous button state (for detecting button press)
last_button_state = 1  # 1 = not pressed, 0 = pressed

# ========== HELPER FUNCTIONS ==========
def map_value(value, in_min, in_max, out_min, out_max):
    """
    Convert value from one range to another
    Example: map 0-4095 to -100 to 100
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def read_joystick():
    """
    Read joystick position
    Returns: x_value (-100 to 100), y_value (-100 to 100)
    """
    # Read ADC values (0 to 4095)
    x_raw = x_adc.read()
    y_raw = y_adc.read()
    
    # Convert to -100 to 100 range
    x_value = map_value(x_raw, 0, 4095, -100, 100)
    y_value = map_value(y_raw, 0, 4095, -100, 100)
    
    return x_value, y_value

def apply_deadzone(value, deadzone):
    """
    Ignore small joystick movements to prevent drifting
    """
    if -deadzone < value < deadzone:
        return 0
    return value

def move_camera(x_value, y_value):
    """
    Move camera based on joystick position
    """
    global current_pan, current_tilt
    
    # Apply deadzone to ignore small movements
    x_value = apply_deadzone(x_value, DEADZONE)
    y_value = apply_deadzone(y_value, DEADZONE)
    
    # Calculate new angles
    new_pan = current_pan
    new_tilt = current_tilt
    
    # Move left or right (pan)
    if x_value < -DEADZONE:      # Left
        new_pan = current_pan - MOVE_SPEED
    elif x_value > DEADZONE:     # Right
        new_pan = current_pan + MOVE_SPEED
    
    # Move up or down (tilt)
    if y_value < -DEADZONE:      # Down
        new_tilt = current_tilt - MOVE_SPEED
    elif y_value > DEADZONE:     # Up
        new_tilt = current_tilt + MOVE_SPEED
    
    # Check angle limits for pan
    if new_pan < PAN_MIN:
        new_pan = PAN_MIN
    elif new_pan > PAN_MAX:
        new_pan = PAN_MAX
    
    # Check angle limits for tilt
    if new_tilt < TILT_MIN:
        new_tilt = TILT_MIN
    elif new_tilt > TILT_MAX:
        new_tilt = TILT_MAX
    
    # Move servos only if angle changed
    if new_pan != current_pan:
        pan_servo.angle(new_pan)
        current_pan = new_pan
        print(f"Pan: {current_pan} degrees", end="  ")
    
    if new_tilt != current_tilt:
        tilt_servo.angle(new_tilt)
        current_tilt = new_tilt
        print(f"Tilt: {current_tilt} degrees", end="  ")
    
    # Print new line if something moved
    if new_pan != current_pan or new_tilt != current_tilt:
        print()

def check_button_press():
    """
    Check if joystick button is pressed
    Returns: True if button was just pressed
    """
    global last_button_state
    
    current_state = joystick_button.value()
    
    # Button is pressed when it goes from 1 to 0
    if last_button_state == 1 and current_state == 0:
        last_button_state = current_state
        return True
    
    last_button_state = current_state
    return False

def take_photo():
    """
    Capture and save a photo
    """
    global photo_count
    
    # Create filename with angle information
    filename = f"photo_{photo_count:03d}_pan{current_pan:+03d}_tilt{current_tilt:+03d}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)
    
    print(f"\nTaking photo #{photo_count}...")
    print(f"   Camera angles: Pan={current_pan} degrees, Tilt={current_tilt} degrees")
    print(f"   Saving to: {filepath}")
    
    try:
        # Capture photo
        camera.capture_file(filepath)
        print("Photo saved successfully!")
        
        # Simple visual feedback
        print("Photo captured!")
        
        # Increment photo counter
        photo_count += 1
        
    except Exception as e:
        print(f"Error taking photo: {e}")

def reset_camera():
    """
    Reset camera to center position
    """
    global current_pan, current_tilt
    
    print("\nResetting camera to center position...")
    
    current_pan = 0
    current_tilt = 0
    
    pan_servo.angle(current_pan)
    tilt_servo.angle(current_tilt)
    
    print(f"Camera centered: Pan={current_pan} degrees, Tilt={current_tilt} degrees")

def print_instructions():
    """
    Display control instructions
    """
    print("\n" + "="*60)
    print("PAN-TILT CAMERA CONTROL SYSTEM")
    print("="*60)
    print("CONTROLS:")
    print("  Joystick LEFT/RIGHT  -> Move camera horizontally (Pan)")
    print("  Joystick UP/DOWN     -> Move camera vertically (Tilt)")
    print("  Joystick BUTTON      -> Take a photo")
    print("\nINFORMATION:")
    print(f"  Photos saved to: {PHOTO_DIR}")
    print(f"  Pan range: {PAN_MIN} to {PAN_MAX} degrees")
    print(f"  Tilt range: {TILT_MIN} to {TILT_MAX} degrees")
    print("\nPress Ctrl+C to exit the program")
    print("="*60 + "\n")

def cleanup():
    """
    Clean up resources before exiting
    """
    global running
    
    print("\nShutting down system...")
    running = False
    
    # Reset servos to center
    print("Centering servos...")
    pan_servo.angle(0)
    tilt_servo.angle(0)
    time.sleep(0.5)
    
    # Stop camera
    print("Stopping camera...")
    camera.stop_preview()
    camera.close()
    
    print("System shutdown complete!")
    print(f"Total photos taken: {photo_count-1}")

# ========== MAIN PROGRAM ==========
def main():
    """
    Main program loop
    """
    global running
    
    # Start camera preview
    print("Starting camera preview...")
    camera.start_preview(Preview.QT)
    camera.start()
    
    # Reset camera to center
    reset_camera()
    
    # Show instructions
    print_instructions()
    
    print("System ready! Start controlling the camera...\n")
    
    # Main control loop
    try:
        while running:
            # Read joystick position
            x_val, y_val = read_joystick()
            
            # Move camera based on joystick
            move_camera(x_val, y_val)
            
            # Check if joystick button is pressed
            if check_button_press():
                take_photo()
            
            # Small delay to prevent CPU overload
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    
    finally:
        # Clean up before exiting
        cleanup()

# ========== PROGRAM START ==========
if __name__ == "__main__":
    print("Starting Pan-Tilt Camera Control System")
    print("==========================================")
    main()