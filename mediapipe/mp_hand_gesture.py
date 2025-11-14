from picamera2 import Picamera2, Preview
import cv2 
import numpy as np
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

# import MediaPipe Tasks (Gesture Recognizer)
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from pathlib import Path

# --------------------- Settings ---------------------
BASE_DIR = Path(__file__).resolve().parent
GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")  # path to the gesture model
SCORE_THRESHOLD = 0.5                           # show gestures above this score
# ---------------------------------------------------

# Initialize the Hands model (kept for landmark drawing)
hands = mp_hands.Hands(
    static_image_mode=False,  # Set to False for processing video frames
    max_num_hands=2,          # Maximum number of hands to detect
    min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
)

# Initialize Gesture Recognizer (VIDEO mode for streaming)
BaseOptions = python.BaseOptions
GestureRecognizerOptions = vision.GestureRecognizerOptions
RunningMode = vision.RunningMode

base_options = BaseOptions(model_asset_path=GESTURE_MODEL_PATH)
gr_options = GestureRecognizerOptions(
    base_options=base_options,
    running_mode=RunningMode.VIDEO
)
recognizer = vision.GestureRecognizer.create_from_options(gr_options)

# Open the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
   main={"size": (640, 480), "format": "XRGB8888"} ,
)

picam2.configure(config)
#picam2.start_preview(Preview.QTGL) 
picam2.start()

print("Streaming... press 'q' to quit")

# (Optional) a small helper to draw a label near a hand bounding box computed from landmarks
def draw_gesture_label(frame_bgr, norm_landmarks, text, color=(0, 175, 255)):
    """
    norm_landmarks: list of 21 normalized landmarks (x,y in [0,1]).
    We compute a tight bbox to place the gesture text.
    """
    if not norm_landmarks:
        return
    h, w = frame_bgr.shape[:2]
    xs = [int(lm.x * w) for lm in norm_landmarks]
    ys = [int(lm.y * h) for lm in norm_landmarks]
    x1, y1, x2, y2 = max(0, min(xs)), max(0, min(ys)), min(w-1, max(xs)), min(h-1, max(ys))

    # draw a thin box (optional)
    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)

    # draw label above the box
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    y_text = max(0, y1 - th - 6)
    cv2.rectangle(frame_bgr, (x1, y_text), (x1 + tw + 6, y_text + th + 6), color, -1)
    cv2.putText(frame_bgr, text, (x1 + 3, y_text + th + 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)

while True:
    frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert the frame from BGR to RGB (required by MediaPipe)
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # ---- A) Run legacy Hands (for landmark drawing you already have) ----
    hands_detected = hands.process(frame_rgb)

    # ---- B) Run Gesture Recognizer (direct gesture labels) ----
    # Wrap the RGB frame as an mp.Image and call recognize_for_video with a timestamp (ms)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    # Using OpenCV tick count as a monotonic timestamp
    ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
    gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # If hands are detected, draw landmarks and connections on the frame (as before)
    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )

    # ---- C) Overlay gesture names (e.g., "Thumb_Up") on top of each detected hand ----
    # gesture_result.gestures: list of per-hand gesture lists (take top-1)
    # gesture_result.hand_landmarks: corresponding list of 21 normalized landmarks per hand
    if gesture_result and getattr(gesture_result, "gestures", None):
        for i, gesture_list in enumerate(gesture_result.gestures):
            if not gesture_list:
                continue
            top = gesture_list[0]
            label = top.category_name  # e.g., "Thumb_Up"
            score = top.score or 0.0
            if score < SCORE_THRESHOLD:
                continue

            # (optional) handedness label: "Left"/"Right"
            hand_label = ""
            if gesture_result.handedness and i < len(gesture_result.handedness):
                if gesture_result.handedness[i]:
                    hand_label = gesture_result.handedness[i][0].category_name or ""

            text = f"{hand_label} {label} ({score:.2f})".strip()

            # Find a place to draw: use the corresponding hand landmarks bounding box
            hand_lms = None
            if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
                hand_lms = gesture_result.hand_landmarks[i]

            if hand_lms:
                draw_gesture_label(frame, hand_lms, text)
            else:
                # Fallback: top-left corner if landmarks not available
                cv2.putText(frame, text, (20, 40 + 30*i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
try:
    picam2.stop_preview()
except Exception:
    pass
picam2.stop()
cv2.destroyAllWindows()
