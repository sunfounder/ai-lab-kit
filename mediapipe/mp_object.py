# STEP 1: Import the necessary modules.
from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import time
from pathlib import Path

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -------------------- Paths & basic settings --------------------
BASE_DIR = Path(__file__).resolve().parent
TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")  # or 'efficientdet.tflite'
SCORE_THRESHOLD = 0.5
MAX_DRAW = 20  # keep the screen clean

# -------------------- Helper: visualization --------------------
def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
    """
    Draw bounding boxes and category labels on a BGR image.
    Compatible with MediaPipe Tasks ObjectDetector's detection_result.
    """
    img = bgr_image.copy()
    h, w = img.shape[:2]

    drawn = 0
    for det in detection_result.detections:
        bbox = det.bounding_box  # (origin_x, origin_y, width, height) in pixels
        x1 = int(bbox.origin_x)
        y1 = int(bbox.origin_y)
        x2 = int(bbox.origin_x + bbox.width)
        y2 = int(bbox.origin_y + bbox.height)

        # Sanity clamp
        x1 = max(0, min(x1, w - 1))
        y1 = max(0, min(y1, h - 1))
        x2 = max(0, min(x2, w - 1))
        y2 = max(0, min(y2, h - 1))

        # Pick top-1 category
        if det.categories:
            c = det.categories[0]
            name = c.category_name if c.category_name else "object"
            score = c.score if c.score is not None else 0.0
            caption = f"{name}: {score:.2f}"
        else:
            caption = "object"

        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)

        # Caption background + text
        (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
        cv2.putText(img, caption, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

        drawn += 1
        if drawn >= MAX_DRAW:
            break

    return img

# ======================= VIDEO PIPELINE =======================
# We mirror the "STEP" structure from the reference and adapt it to streaming.

# STEP 2: Create an ObjectDetector object.
BaseOptions = python.BaseOptions
ObjectDetectorOptions = vision.ObjectDetectorOptions
RunningMode = vision.RunningMode

base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
options = ObjectDetectorOptions(
    base_options=base_options,
    score_threshold=SCORE_THRESHOLD,
    running_mode=RunningMode.VIDEO,  # VIDEO mode for streaming input
)
detector = vision.ObjectDetector.create_from_options(options)

# STEP 3: (Streaming) Prepare the camera as the input "image" source.
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XRGB8888"},
)
picam2.configure(config)
# picam2.start_preview(Preview.QTGL)
picam2.start()

print("Streaming... press 'q' to quit")

while True:
    # Capture BGRA from Picamera2 and convert to BGR
    frame_bgra = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert to RGB and wrap as mp.Image (MediaPipe expects RGB)
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    # STEP 4: Detect objects in the input image (streaming = detect_for_video).
    ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp in ms
    detection_result = detector.detect_for_video(mp_image, ts_ms)

    # STEP 5: Process/visualize the detection result on the current frame.
    annotated = visualize(frame_bgr, detection_result)

    # Display
    cv2.imshow("Show Video", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
try:
    picam2.stop_preview()
except Exception:
    pass
picam2.stop()
cv2.destroyAllWindows()