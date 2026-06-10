"""
MediaPipe Hand Detection + TTS Demo
====================================
Detects fingers via webcam in real time. Press the 't' key to speak the
current finger count using TTS.

Usage:
    python mp_hand_count_tts.py

Controls:
    't'  - speak the detected finger count via TTS
    'q'  - quit
"""

from picamera2 import Picamera2
import cv2
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
from fusion_hat.tts import Espeak
import time


# ======================== Init TTS ========================
tts = Espeak()
tts.set_amp(200)       # volume 0-200, default 100
tts.set_speed(150)     # speed 80-260, default 150
tts.set_pitch(80)      # pitch 0-99, default 80

# ======================== Init MediaPipe Hands ========================
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)

# ======================== Init Camera ========================
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"},
)
picam2.configure(config)
picam2.start()

# ======================== Constants ========================
# Finger tip and dip landmark indices
FINGER_TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
FINGER_DIPS = [2, 6, 10, 14, 18]   # corresponding middle joints

# Minimum interval (seconds) between TTS triggers to avoid spamming
DEBOUNCE_INTERVAL = 1.5

print("=" * 55)
print("  MediaPipe Hand Count + TTS")
print("  Press 't' to speak count | 'q' to quit")
print("=" * 55)

# ======================== Main Loop ========================
last_tts_time = 0          # timestamp of last TTS trigger
tts_triggered = False      # whether TTS was just fired (for visual flash)
tts_flash_until = 0        # how long the flash should last

while True:
    # ---- 1. Capture frame ----
    frame_bgra = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # ---- 2. Convert to RGB for MediaPipe ----
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    hands_detected = hands.process(frame_rgb)

    # ---- 3. Convert back to BGR for OpenCV display ----
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # ---- 4. Count fingers (right hand only) ----
    total_fingers = 0

    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            # Draw hand skeleton
            drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )

            landmarks = hand_landmarks.landmark
            finger_count = 0

            # Thumb: extended when x_tip > x_dip (right hand)
            if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
                finger_count += 1

            # Other four fingers: tip is above dip when extended (smaller y)
            for i in range(1, 5):
                if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
                    finger_count += 1

            total_fingers += finger_count

    # ---- 5. Display finger count on screen ----
    display_text = f"Fingers: {total_fingers}"
    cv2.putText(frame, display_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

    # ---- 6. Key handling ----
    key = cv2.waitKey(1) & 0xff

    # 't' key: trigger TTS (with debounce)
    if key == ord('t'):
        now = time.time()
        if now - last_tts_time > DEBOUNCE_INTERVAL:
            last_tts_time = now
            tts_triggered = True
            tts_flash_until = now + 1.0  # flash for 1 second

            if total_fingers == 0:
                message = "no fingers detected"
            elif total_fingers == 1:
                message = "one finger detected"
            else:
                message = f"{total_fingers} fingers detected"

            print(f"[TTS] {message}")
            tts.say(message)

    # 'q' key: quit
    if key == ord('q'):
        break

    # ---- 7. Visual feedback while speaking (green border flash) ----
    if tts_triggered and time.time() < tts_flash_until:
        h, w = frame.shape[:2]
        thickness = 8
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 255, 0), thickness)
        cv2.putText(frame, "Speaking...", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    else:
        tts_triggered = False

    # ---- 8. Show controls hint at bottom ----
    cv2.putText(frame, "Press 't' to speak count | 'q' to quit",
                (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    # ---- 9. Show frame ----
    cv2.imshow("MediaPipe Hand Count + TTS", frame)

# ======================== Cleanup ========================
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
print("Exited.")
