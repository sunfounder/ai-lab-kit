"""
MediaPipe Hand Detection + Auto TTS (Touchless Mode)
====================================================
Detects fingers via webcam in real time. Automatically speaks the finger count
when a stable hand gesture is maintained for a certain duration.

No keyboard input required for triggering TTS.

Usage:
    python mp_hand_count_auto_tts.py

Controls:
    'q'  - quit
"""

from picamera2 import Picamera2
import cv2
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
from fusion_hat.tts import Espeak
import time
from collections import deque


# ======================== Init TTS ========================
tts = Espeak()
tts.set_amp(200)       # volume 0-200, default 100
tts.set_speed(150)     # speed 80-260, default 150
tts.set_pitch(80)      # pitch 0-99, default 80

# ======================== Init MediaPipe Hands ========================
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
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

# Auto TTS parameters
STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable before speaking
MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
HAND_EXIT_DELAY = 4.0           # seconds after hand leaves before saying "hand left"
NO_HAND_COOLDOWN = 5.0          # seconds without hand before suppressing "no hand" repeats

# Frame processing
FRAME_HISTORY_SIZE = 10         # for stability detection

# Border colors (BGR)
COLOR_IDLE = (128, 128, 128)    # gray
COLOR_DETECTED = (255, 255, 0)  # cyan
COLOR_STABLE = (0, 255, 0)      # green
COLOR_SPEAKING = (0, 255, 0)    # bright green

print("=" * 60)
print("  MediaPipe Hand Detection + AUTO TTS (Touchless Mode)")
print("  No keyboard needed - just show a stable hand gesture")
print("  Press 'q' to quit")
print("=" * 60)

# ======================== State Management ========================
class HandTrackingState:
    def __init__(self):
        self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)  # recent finger counts
        self.current_fingers = 0
        self.stable_fingers = -1           # last confirmed stable count
        self.stable_start_time = 0          # when current finger count became stable
        self.is_stable = False
        self.hand_present = False
        self.hand_absent_start_time = 0
        self.last_tts_time = 0
        self.last_tts_message = ""
        self.last_no_hand_tts_time = 0
        
state = HandTrackingState()

def get_finger_count(hand_landmarks):
    """Count fingers for a single hand (right hand logic)"""
    landmarks = hand_landmarks.landmark
    finger_count = 0
    
    # Thumb: extended when x_tip > x_dip (right hand)
    if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
        finger_count += 1
    
    # Other four fingers: tip is above dip when extended (smaller y)
    for i in range(1, 5):
        if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
            finger_count += 1
    
    return finger_count

def update_stability(new_count):
    """Update stability state based on finger count history"""
    state.finger_history.append(new_count)
    
    # Check if all recent frames have same finger count
    if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
        recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
        if all(c == new_count for c in recent_counts):
            if not state.is_stable or state.current_fingers != new_count:
                # Became stable now
                state.is_stable = True
                state.stable_start_time = time.time()
                state.current_fingers = new_count
                return True
    else:
        state.is_stable = False
    
    state.current_fingers = new_count
    return False

def should_trigger_tts():
    """Check if conditions are met for auto TTS"""
    now = time.time()
    
    # Check minimum interval between TTS
    if now - state.last_tts_time < MIN_TTS_INTERVAL:
        return False
    
    # Hand must be present and stable
    if not state.hand_present or not state.is_stable:
        return False
    
    # Must have been stable for required hold duration
    hold_time = now - state.stable_start_time
    if hold_time < HOLD_DURATION_REQUIRED:
        return False
    
    # Don't repeat same count if it just spoke
    if state.stable_fingers == state.current_fingers:
        # But allow repeat after longer interval (for re-announcement)
        if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
            return False
    
    return True

def trigger_tts():
    """Execute TTS for current finger count"""
    now = time.time()
    count = state.current_fingers
    
    if count == 0:
        message = "no fingers detected"
    elif count == 1:
        message = "one finger detected"
    else:
        message = f"{count} fingers detected"
    
    # Avoid repeating exactly the same message back-to-back
    if message == state.last_tts_message and now - state.last_tts_time < 3.0:
        return False
    
    print(f"[TTS] {message} (held for {HOLD_DURATION_REQUIRED}s)")
    tts.say(message)
    
    state.last_tts_time = now
    state.last_tts_message = message
    state.stable_fingers = count
    
    return True

def trigger_hand_exit_tts():
    """Say hand has left the frame"""
    now = time.time()
    if now - state.last_tts_time >= MIN_TTS_INTERVAL:
        print("[TTS] hand left the frame")
        tts.say("hand left the frame")
        state.last_tts_time = now
        state.last_tts_message = "hand left"

def get_border_color():
    """Determine border color based on current state"""
    now = time.time()
    
    # Speaking has priority
    if hasattr(state, 'speaking_until') and now < state.speaking_until:
        return COLOR_SPEAKING
    
    if not state.hand_present:
        return COLOR_IDLE
    
    if state.is_stable:
        hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
        if hold_progress < 1.0:
            # Mix cyan and green based on progress
            r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
            g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
            b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
            return (b, g, r)  # OpenCV uses BGR
        else:
            return COLOR_STABLE
    
    return COLOR_DETECTED

# ======================== Main Loop ========================
frame_count = 0
speaking_flash_until = 0

while True:
    # ---- 1. Capture frame ----
    frame_bgra = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
    
    # ---- 2. Convert to RGB for MediaPipe ----
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    hands_detected = hands.process(frame_rgb)
    
    # ---- 3. Convert back to BGR for OpenCV display ----
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    
    # ---- 4. Detect hands and count fingers ----
    total_fingers = 0
    has_hand = False
    
    if hands_detected.multi_hand_landmarks:
        has_hand = True
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            # Draw hand skeleton
            drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )
            
            finger_count = get_finger_count(hand_landmarks)
            total_fingers = max(total_fingers, finger_count)  # Use hand with most fingers
    
    # ---- 5. Update state machine ----
    now = time.time()
    
    # Hand presence tracking
    if has_hand:
        if not state.hand_present:
            # Hand just entered
            state.hand_present = True
            state.is_stable = False
            state.finger_history.clear()
            print("[INFO] Hand detected")
        state.hand_absent_start_time = now
    else:
        if state.hand_present:
            # Hand just left
            state.hand_present = False
            state.is_stable = False
            state.stable_fingers = -1
            state.finger_history.clear()
            # Trigger exit TTS after delay
            if now - state.last_tts_time >= MIN_TTS_INTERVAL:
                trigger_hand_exit_tts()
    
    # Update stability and check for TTS trigger
    if has_hand:
        update_stability(total_fingers)
        
        if should_trigger_tts():
            if trigger_tts():
                speaking_flash_until = now + 0.8  # flash for visual feedback
                state.speaking_until = speaking_flash_until
    
    # ---- 6. Display information on screen ----
    # Finger count
    display_text = f"Fingers: {total_fingers}"
    cv2.putText(frame, display_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
    
    # Status text
    if not has_hand:
        status_text = "Status: No hand detected"
        status_color = (128, 128, 128)
    elif state.is_stable:
        hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
        if hold_progress < 1.0:
            remaining = HOLD_DURATION_REQUIRED - (now - state.stable_start_time)
            status_text = f"Status: Hold gesture ({remaining:.1f}s to speak)"
            status_color = (255, 255, 0)
        else:
            status_text = "Status: Ready to speak!"
            status_color = (0, 255, 0)
    else:
        status_text = "Status: Detecting... keep hand still"
        status_color = (0, 200, 200)
    
    cv2.putText(frame, status_text, (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
    
    # Instructions
    cv2.putText(frame, "Keep gesture still to auto-speak | 'q' to quit",
                (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    
    # ---- 7. Visual border feedback ----
    h, w = frame.shape[:2]
    thickness = 6
    
    # Speaking flash takes priority
    if now < speaking_flash_until:
        border_color = (0, 255, 0)
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)
        cv2.putText(frame, "SPEAKING...", (w - 180, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        border_color = get_border_color()
        cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)
    
    # ---- 8. Progress bar for hold duration ----
    if has_hand and state.is_stable:
        hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
        bar_width = int(w * 0.4)
        bar_height = 8
        bar_x = w - bar_width - 10
        bar_y = 10
        filled_width = int(bar_width * hold_progress)
        
        # Background
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), 
                     (60, 60, 60), -1)
        # Fill
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height), 
                     (0, 255, 0), -1)
    
    # ---- 9. Key handling ----
    key = cv2.waitKey(1) & 0xff
    
    # 'q' key: quit
    if key == ord('q'):
        break
    
    # ---- 10. Show frame ----
    cv2.imshow("MediaPipe Hand Detection + AUTO TTS (Touchless Mode)", frame)

# ======================== Cleanup ========================
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
print("Exited.")