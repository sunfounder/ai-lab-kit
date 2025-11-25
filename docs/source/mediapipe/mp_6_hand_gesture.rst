.. _mp_hand_gesture:


6. Hand Gesture Recognizer
==================================================

In the previous chapter, we used MediaPipe Hands to obtain 21 hand landmarks and visualized the skeleton.
This chapter further introduces **MediaPipe Tasks' Gesture Recognizer model** to achieve **direct output of semantic gesture labels** (such as "Thumb_Up", "Open_Palm", etc.), and overlays the display with the landmark rendering from Hands.

.. image:: img/mp_hang_gesture.png
   :alt: Gesture Recognizer
   :align: center

**Objective：**

- On the Raspberry Pi, combine ``Picamera2`` + ``MediaPipe Hands`` + ``Gesture Recognizer`` model to achieve **real-time gesture classification**;
- Output gesture category and confidence for each hand in the video stream;
- Overlay the skeleton and gesture text for clear teaching/demonstration effects.

**Approach：**

1. Use **Picamera2** to capture video frames;
2. Use **MediaPipe Hands** for landmark drawing (optional);
3. Use **MediaPipe Tasks: Gesture Recognizer** in **VIDEO** mode for gesture recognition on each frame;
4. Obtain for each hand: candidate gesture list (category + confidence), normalized hand landmarks, handedness (left/right);
5. Draw the top-1 gesture as a "label + score" above the bounding box of the corresponding hand.

.. note::

   - This chapter uses the Tasks API from **MediaPipe 0.10+**.
   - Gesture Recognizer requires a model file (``gesture_recognizer.task``); we have placed it in the example code directory, please use it directly.

------------------------
1. Run the Code
------------------------

Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).
4. You have installed the **mediapipe** environment (see :ref:`mediapipe_install`).

Open the terminal in VNC and enter the following command:

.. code-block:: bash

   sudo ~/mediapipe_env/bin/python3 ~/ai-lab-kit/mediapipe/mp_hand_gesture.py

-----------------------------
2. Code Example
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Import MediaPipe Tasks (Gesture Recognizer)
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   from pathlib import Path

   # --------------------- Settings ---------------------
   BASE_DIR = Path(__file__).resolve().parent
   GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")  # Path to the gesture model
   SCORE_THRESHOLD = 0.5                           # Show gestures above this score
   # ---------------------------------------------------

   # Initialize the Hands model (kept for landmark drawing)
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
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
   picam2.start()

   print("Streaming... press 'q' to quit")

   # (Optional) helper to draw a label near a hand bounding box computed from landmarks
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
       x1, y1 = max(0, min(xs)), max(0, min(ys))
       x2, y2 = min(w-1, max(xs)), min(h-1, max(ys))
       cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)
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
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
       ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
       gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

       # Convert the frame back from RGB to BGR (required by OpenCV)
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # If hands are detected, draw landmarks and connections on the frame
       if hands_detected.multi_hand_landmarks:
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

       # ---- C) Overlay gesture names on top of each detected hand ----
       if gesture_result and getattr(gesture_result, "gestures", None):
           for i, gesture_list in enumerate(gesture_result.gestures):
               if not gesture_list:
                   continue
               top = gesture_list[0]
               label = top.category_name  # e.g., "Thumb_Up"
               score = top.score or 0.0
               if score < SCORE_THRESHOLD:
                   continue

               hand_label = ""
               if gesture_result.handedness and i < len(gesture_result.handedness):
                   if gesture_result.handedness[i]:
                       hand_label = gesture_result.handedness[i][0].category_name or ""

               text = f"{hand_label} {label} ({score:.2f})".strip()

               hand_lms = None
               if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
                   hand_lms = gesture_result.hand_landmarks[i]

               if hand_lms:
                   draw_gesture_label(frame, hand_lms, text)
               else:
                   cv2.putText(frame, text, (20, 40 + 30*i),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

       # Display the frame with annotations
       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   # Release the camera
   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

After running the script, the window will display the hand skeleton (optional) and gesture text boxes. When a gesture matching the model's categories is recognized, it will display above the corresponding hand's bounding box:

- Left/Right hand (handedness)
- Gesture name (e.g., ``Thumb_Up``)
- Confidence score (0~1)

-----------------------------
3. Code Explanation
-----------------------------

**High-level flow:**

#. Initialize MediaPipe **Hands** for landmark drawing (solutions API).
#. Initialize MediaPipe **GestureRecognizer** in ``VIDEO`` mode (Tasks API).
#. Open camera with **Picamera2** and stream frames.
#. For each frame:

   - Convert BGRA → BGR → RGB.
   - Run ``Hands.process()`` to get landmarks → draw skeleton.
   - Wrap the RGB frame into ``mp.Image`` and call
     ``recognizer.recognize_for_video(image, timestamp_ms)``.
   - For each detected hand, overlay the **gesture label** and **score** near the hand bbox.
   - Show the annotated frame.

#. Clean up camera and window resources on exit.

**Modules and Imports**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # MediaPipe Tasks (Gesture Recognizer)
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   from pathlib import Path

- ``mediapipe.python.solutions`` provides the classic *solutions* (e.g., Hands, Pose).
- ``mediapipe.tasks.python.vision`` provides the **Tasks** API with ready-to-use detectors/recognizers.

**Settings**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")
   SCORE_THRESHOLD = 0.5

- ``GESTURE_MODEL_PATH``: Path to the gesture model file. In this example, we use the ``gesture_recognizer.task`` model. It is a pre-trained model for recognizing gestures. We place the model file in the same directory as the script and use the ``Path`` module to get its path.
- ``SCORE_THRESHOLD``: Minimum confidence score to display a gesture label.

**Initialization**

1. Hands (Solutions API)

.. code-block:: python

   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

- ``static_image_mode=False``: Optimized for video streams.
- ``max_num_hands``: Up to two hands.
- ``min_detection_confidence``: Filter out low-confidence detections.

2. Gesture Recognizer (Tasks API)

.. code-block:: python

   BaseOptions = python.BaseOptions
   GestureRecognizerOptions = vision.GestureRecognizerOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=GESTURE_MODEL_PATH)
   gr_options = GestureRecognizerOptions(
       base_options=base_options,
       running_mode=RunningMode.VIDEO
   )
   recognizer = vision.GestureRecognizer.create_from_options(gr_options)

- ``RunningMode.VIDEO``: Streaming mode that **requires** a monotonically increasing timestamp.
- The recognizer returns gesture categories per detected hand, along with handedness and landmarks.

**Camera Setup (Picamera2)**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

- The stream is configured to 640×480 to balance **speed** and **accuracy**.
- Picamera2 returns BGRA frames; we will convert to BGR and RGB as needed.

**Per-Frame Processing**

1. Color Conversion

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

- MediaPipe expects **RGB** input.
- We keep a **BGR** copy (``frame``) for drawing and display.

2. Hands Landmarks (Drawing)

.. code-block:: python

   hands_detected = hands.process(frame_rgb)

   if hands_detected.multi_hand_landmarks:
       for hand_landmarks in hands_detected.multi_hand_landmarks:
           drawing.draw_landmarks(
               frame,
               hand_landmarks,
               mp_hands.HAND_CONNECTIONS,
               drawing_styles.get_default_hand_landmarks_style(),
               drawing_styles.get_default_hand_connections_style(),
           )

- ``Hands.process`` returns 21 landmarks per hand.
- ``draw_landmarks`` draws the canonical hand skeleton.

3. Gesture Recognition (Tasks API)

.. code-block:: python

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
   ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
   gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

- ``recognize_for_video`` needs a **timestamp in ms**; use OpenCV tick clock for a monotonic source.
- The result includes:

  - ``gestures``: list of per-hand gesture lists (top-1 used)
  - ``hand_landmarks``: 21 normalized landmarks per detected hand
  - ``handedness``: classification like ``Left`` or ``Right``

4. Overlay Gesture Labels

Helper to place text near the hand bbox

.. code-block:: python

   def draw_gesture_label(frame_bgr, norm_landmarks, text, color=(0, 175, 255)):
       """
       Compute a tight bounding box from normalized landmarks, draw it, and
       put the gesture label above the box.
       """
       if not norm_landmarks:
           return
       h, w = frame_bgr.shape[:2]
       xs = [int(lm.x * w) for lm in norm_landmarks]
       ys = [int(lm.y * h) for lm in norm_landmarks]
       x1, y1 = max(0, min(xs)), max(0, min(ys))
       x2, y2 = min(w-1, max(xs)), min(h-1, max(ys))
       cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)
       (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
       y_text = max(0, y1 - th - 6)
       cv2.rectangle(frame_bgr, (x1, y_text), (x1 + tw + 6, y_text + th + 6), color, -1)
       cv2.putText(frame_bgr, text, (x1 + 3, y_text + th + 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)

Using the helper with recognizer output

.. code-block:: python

   if gesture_result and getattr(gesture_result, "gestures", None):
       for i, gesture_list in enumerate(gesture_result.gestures):
           if not gesture_list:
               continue
           top = gesture_list[0]
           label = top.category_name
           score = top.score or 0.0
           if score < SCORE_THRESHOLD:
               continue

           hand_label = ""
           if gesture_result.handedness and i < len(gesture_result.handedness):
               if gesture_result.handedness[i]:
                   hand_label = gesture_result.handedness[i][0].category_name or ""

           text = f"{hand_label} {label} ({score:.2f})".strip()

           hand_lms = None
           if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
               hand_lms = gesture_result.hand_landmarks[i]

           if hand_lms:
               draw_gesture_label(frame, hand_lms, text)
           else:
               cv2.putText(frame, text, (20, 40 + 30*i),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

- We display the **top-1** gesture per hand if its score ≥ ``SCORE_THRESHOLD``.
- The label includes handedness (``Left``/``Right``) when available.

**Display and Exit**

.. code-block:: python

   cv2.imshow("Show Video", frame)
   if cv2.waitKey(1) & 0xff == ord('q'):
       break

   # Cleanup
   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()

- The loop runs until you press ``q``.
- Always release the camera and destroy windows when finishing.

-----------------------------
4. Parameters and Tuning
-----------------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Suggestion
   * - ``SCORE_THRESHOLD``
     - Gestures below this score are ignored
     - Increase to reduce false positives; decrease to improve recall
   * - ``max_num_hands``
     - Number of hands to detect simultaneously
     - 2 is sufficient for most scenarios
   * - ``running_mode=VIDEO``
     - Video stream mode, requires timestamp
     - Keep using (streaming recognition is more stable)
   * - Resolution
     - Affects speed and accuracy
     - Recommended 640×480 or lower on Raspberry Pi for better FPS

-------------------------------------------------------
5. Common Issues and Troubleshooting
-------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Possible Cause
     - Solution
   * - ``FileNotFoundError: gesture_recognizer.task``
     - Incorrect model file path
     - Place model in the same directory as the script per "Model Download & Placement", or correct ``GESTURE_MODEL_PATH``
   * - ``ImportError: cannot import name 'vision' from mediapipe.tasks.python``
     - Old MediaPipe version
     - `pip install --upgrade mediapipe` to version 0.10+
   * - Recognized category differs from expectation
     - Different model category set / lighting effects
     - Change model version, improve lighting, or simplify background
   * - Low frame rate
     - Limited Raspberry Pi computing power
     - Reduce resolution, disable skeleton drawing, use lightweight system environment

-----------------------------
6. ✅ Summary
-----------------------------

- **Gesture Recognizer** enables real-time semantic gesture recognition on Raspberry Pi;
- Combined with **Hands** skeleton rendering, it's both intuitive and easy to debug;
- By adjusting thresholds and resolution, a balance between "stability / speed" can be achieved;
- Future possibilities:

  - Map different gestures to specific commands (shortcuts, GPIO control, etc.);
  - Train custom gesture models for specific scenarios.