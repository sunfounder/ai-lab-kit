#!/usr/bin/env python3
"""
Homework Grading Demo with Pan-Tilt Camera
Press User Button to take photo, LLM grades, servo nods or shakes
"""

import time
from fusion_hat.llm import OpenAI
from fusion_hat.servo import Servo
from fusion_hat.user_button import UserButton
from picamera2 import Picamera2, Preview

# ========== LLM SETTINGS ==========
# Create a secret.py file with: OPENAI_API_KEY = "your-api-key-here"
try:
    from secret import OPENAI_API_KEY
except ImportError:
    print("ERROR: Please create a secret.py file with your OpenAI API key")
    print("Example content: OPENAI_API_KEY = 'sk-...'")
    exit()

# LLM instructions for grading
INSTRUCTIONS = """You are a homework grading assistant.
When you see a photo of a homework question with an answer, 
determine if the answer is correct or incorrect.

Respond with ONLY ONE WORD:
- If the answer is CORRECT, respond: "CORRECT"
- If the answer is INCORRECT, respond: "INCORRECT"

Do not provide any other text, explanations, or justifications.
Only respond with "CORRECT" or "INCORRECT"."""

# Initialize LLM
llm = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o"
)

# Set LLM settings
llm.set_max_messages(5)
llm.set_instructions(INSTRUCTIONS)

# ========== HARDWARE SETTINGS ==========
PAN_CHANNEL = 2      # Horizontal servo for shaking head
TILT_CHANNEL = 3     # Vertical servo for nodding head

# Servo center positions
TILT_CENTER = 0      # Looking straight ahead
PAN_CENTER = 0       # Center position

# ========== INITIALIZE HARDWARE ==========
print("Initializing Homework Grading Demo...")
print("-" * 50)

# Initialize servos
pan_servo = Servo(PAN_CHANNEL)
tilt_servo = Servo(TILT_CHANNEL)

# Center servos
tilt_servo.angle(TILT_CENTER)
pan_servo.angle(PAN_CENTER)
time.sleep(1)
print("Servos ready")

# Initialize camera
camera = Picamera2()
camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
camera.configure(camera_config)
camera.start_preview(Preview.QT)
camera.start()
time.sleep(2)
print("Camera ready")

# Initialize user button
user_button = UserButton()
print("User button ready")
print("-" * 50)

# ========== SERVO MOVEMENT FUNCTIONS ==========
def nod_head():
    """
    Nodding head movement for "correct"
    """
    # Look down
    tilt_servo.angle(15)
    time.sleep(0.2)
    # Look up
    tilt_servo.angle(-10)
    time.sleep(0.2)
    # Return to center
    tilt_servo.angle(TILT_CENTER)

def shake_head():
    """
    Shaking head movement for "incorrect"
    """
    # Look left
    pan_servo.angle(-20)
    time.sleep(0.15)
    # Look right
    pan_servo.angle(20)
    time.sleep(0.15)
    # Look left again
    pan_servo.angle(-15)
    time.sleep(0.15)
    # Return to center
    pan_servo.angle(PAN_CENTER)

# ========== GRADING FUNCTION ==========
def grade_homework():
    """
    Main grading function: take photo, send to LLM, move servo
    """
    print("\nTaking photo...")
    
    # Capture image
    img_path = './homework.jpg'
    camera.capture_file(img_path)
    print("Photo captured")
    
    # Send to LLM for grading
    print("Sending to AI for grading...")
    
    prompt = "Look at this homework question and answer. Is the answer correct? Respond with only one word: 'CORRECT' or 'INCORRECT'."
    
    response = llm.prompt(prompt, image_path=img_path)
    response_text = response.strip().upper()
    
    print(f"AI response: {response_text}")
    
    # Move servo based on response
    if "INCORRECT" in response_text:
        print("Answer is incorrect - shaking head")
        shake_head()
    elif "CORRECT" in response_text:
        print("Answer is correct - nodding head")
        nod_head()
    else:
        print(f"Unexpected response: {response_text}")

# ========== BUTTON CALLBACK ==========
def on_button_click():
    """
    Called when user button is pressed
    """
    print("\n" + "=" * 50)
    print("Button pressed - Starting grading process")
    grade_homework()
    print("=" * 50)

# ========== MAIN DEMO ==========
def main():
    """
    Main demo function
    """
    print("\nHOMEWORK GRADING DEMO")
    print("=" * 50)
    print("Instructions:")
    print("1. Place a homework question under the camera")
    print("2. Make sure the question AND answer are visible")
    print("3. Press the User Button (USR) on Fusion HAT to grade")
    print("4. The camera will take a photo")
    print("5. AI will grade the answer")
    print("6. Servo will nod (correct) or shake (incorrect)")
    print("=" * 50)
    print("\nWaiting for button press...")
    
    # Set button callback
    user_button.set_on_click(on_button_click)
    
    # Keep program running
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDemo stopped by user")

# ========== CLEANUP ==========
def cleanup():
    """
    Clean up resources
    """
    print("\nCleaning up...")
    
    # Return servos to center
    tilt_servo.angle(TILT_CENTER)
    pan_servo.angle(PAN_CENTER)
    
    # Stop camera
    camera.stop()
    
    print("Demo ended")

# ========== RUN DEMO ==========
if __name__ == "__main__":
    try:
        main()
    finally:
        cleanup()