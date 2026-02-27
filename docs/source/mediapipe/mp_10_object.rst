.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_object:


10. Object Detection
=================================

------------------------------------------------------------
1. Overview
------------------------------------------------------------

In addition to specialized models for face, hands, and pose,
MediaPipe also provides a general-purpose **Object Detector**
based on TensorFlow Lite.

This chapter demonstrates how to use the
``efficientdet_lite0.tflite`` model on Raspberry Pi
to perform real-time object detection and visualize results
on the camera feed.

.. image:: img/mp_object.png
   :width: 500
   :align: center

This module can be used for:

- Real-time object recognition demos
- Smart home / robotics perception
- Simple safety monitoring
- Embedded vision projects


------------------------------------------------------------
2. How It Works
------------------------------------------------------------

The program performs the following steps:

1. Initialize the MediaPipe Tasks **ObjectDetector**
   and load the ``efficientdet_lite0.tflite`` model.
2. Capture frames from the Picamera2 video stream.
3. Convert each frame to a MediaPipe ``mp.Image`` object.
4. Call ``detect_for_video`` to run real-time object detection.
5. Draw bounding boxes and labels using OpenCV.
6. Limit the number of displayed detections to keep the output clear
   and maintain stable performance on Raspberry Pi.

-----------------------------
3. Model Preparation
-----------------------------

This example uses the **EfficientDet Lite0** model
in TensorFlow Lite (TFLite) format.

EfficientDet Lite0 is lightweight and optimized for
embedded devices such as Raspberry Pi.
It provides a good balance between speed and accuracy.

The file ``efficientdet_lite0.tflite`` is included in the project directory
and can be used directly.

* `Official model download page <https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector#efficientdet-lite0_model_recommended>`_

If higher accuracy is required and hardware performance allows,
you may switch to:

- EfficientDet Lite1
- EfficientDet Lite2

You can also replace the model with your own self-trained
TFLite object detection model, as long as it follows
MediaPipe Tasks Object Detector format requirements.


------------------------
4. Run the Code
------------------------

.. important::


   Before you start, make sure:

   * The pan-tilt is assembled
   * You can access the Raspberry Pi desktop
   * The code package is installed
   * Fusion HAT+ is installed and configured
   * OpenCV is installed

   For detailed instructions, see :ref:`opencv_install`.

#. Open the terminal and enter the following command:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_object.py


#. After running the program, a window titled "Show Video" opens and displays the live camera feed.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_10.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   For each video frame, the Object Detector model (``efficientdet_lite0.tflite``) runs in real time and searches for recognizable objects in the scene.
   
   When objects are detected:
   
   - A rectangular bounding box is drawn around each object.
   - A label and confidence score are shown above the box in the format ``name: score`` (for example, ``person: 0.87``).
   - Only detections above ``SCORE_THRESHOLD`` (default 0.5) are displayed.
   - To keep the display clear and maintain performance, the program draws up to ``MAX_DRAW`` detections (default 20) per frame.
   
   As the camera view changes, the bounding boxes and labels update continuously in real time.
   
   Press ``q`` to exit the program.  
   The camera stops and the OpenCV window closes automatically.

-----------------------------
5. Complete Code
-----------------------------

.. code-block:: python

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
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")  # Model path
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20  # Limit the number of drawn detections

   # -------------------- Helper: visualization --------------------
   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       img = bgr_image.copy()
       h, w = img.shape[:2]
       drawn = 0

       for det in detection_result.detections:
           bbox = det.bounding_box
           x1 = max(0, min(int(bbox.origin_x), w - 1))
           y1 = max(0, min(int(bbox.origin_y), h - 1))
           x2 = max(0, min(int(bbox.origin_x + bbox.width), w - 1))
           y2 = max(0, min(int(bbox.origin_y + bbox.height), h - 1))

           # top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw bounding box
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break
       return img

   # STEP 2: Initialize the detector
   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,
   )
   detector = vision.ObjectDetector.create_from_options(options)

   # STEP 3: Camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()
   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert to RGB and wrap as mp.Image
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

       # STEP 4: Detect
       ts_ms = int(time.time() * 1000)
       detection_result = detector.detect_for_video(mp_image, ts_ms)

       # STEP 5: Visualize
       annotated = visualize(frame_bgr, detection_result)

       cv2.imshow("Show Video", annotated)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

After running the script, the camera feed will display:

- Bounding boxes around detected objects
- Classification labels and confidence scores
- Real-time detection (can achieve about 10~20 FPS on Raspberry Pi)

-----------------------------
6. Code Explanation
-----------------------------

**Configuration**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20

- ``SCORE_THRESHOLD`` controls the minimum confidence to display detections (applied inside the Tasks runtime).
- ``MAX_DRAW`` is a UI convenience to limit how many boxes we render per frame.

**Imports**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2, numpy as np, time
   from pathlib import Path
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

- ``mediapipe.tasks.python.vision`` hosts the **ObjectDetector** Tasks API.
- We still use classic OpenCV for windowing and drawing.

**Visualization Helper**

.. code-block:: python

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
           x1 = int(bbox.origin_x); y1 = int(bbox.origin_y)
           x2 = int(bbox.origin_x + bbox.width); y2 = int(bbox.origin_y + bbox.height)

           # Clamp to frame bounds (defensive)
           x1 = max(0, min(x1, w - 1)); y1 = max(0, min(y1, h - 1))
           x2 = max(0, min(x2, w - 1)); y2 = max(0, min(y2, h - 1))

           # Top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw rectangle and caption
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break

       return img

- Keeps the main loop clean.
- Avoids relying on non-existent "visualize" utilities; it works directly with Tasks outputs.

**Create the ObjectDetector**

.. code-block:: python

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

- ``RunningMode.VIDEO`` is optimized for streams and **requires timestamps**.
- The Tasks runtime internally handles image resizing/normalization for you.

**Camera Setup (Streaming Source)**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

- 640×480 is a good trade-off between FPS and accuracy on Raspberry Pi.
- Picamera2 returns BGRA (``XRGB8888``); we'll convert to BGR/RGB.

**Per-Frame Detection**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr,  cv2.COLOR_BGR2RGB)

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

   ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp
   detection_result = detector.detect_for_video(mp_image, ts_ms)

- MediaPipe expects **RGB** buffers.
- The timestamp must **increase every frame**; using ``time.time()*1000`` is sufficient for this demo.

**Render and Display**

.. code-block:: python

   annotated = visualize(frame_bgr, detection_result)
   cv2.imshow("Show Video", annotated)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

- The helper returns a BGR image ready for OpenCV display.
- Press ``q`` to exit the loop.

**Cleanup**

.. code-block:: python

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Always release the camera and destroy windows to avoid locking the device.

------------------------------------------------------
7. Performance and Applications
------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Optimization Direction
     - Effect
     - Suggestion
   * - Resolution
     - Higher resolution gives clearer image but slower speed
     - 640x480 is sufficient
   * - Model Selection
     - Lite0 ~ Lite2
     - Lite0 is faster, Lite2 is more accurate
   * - Multi-object Drawing
     - Too many objects cause latency
     - Use ``MAX_DRAW`` to limit

------------------------------------------------------
8. Troubleshooting
------------------------------------------------------

- No detection results

  If nothing is detected, the confidence threshold may be too high.

  Try lowering ``SCORE_THRESHOLD`` (for example, from 0.5 to 0.3) and test again.

- Low frame rate

  If the video feels slow, the model or resolution may be too heavy for the Raspberry Pi.

  Use a lighter model (``efficientdet_lite0.tflite``) and reduce the resolution (for example, 640×480 or 320×240). Closing other background processes can also improve performance.

- Detection box offset

  If bounding boxes look shifted or go out of frame, it is usually caused by coordinate conversion issues.

  Make sure bounding box coordinates are clamped to the image boundaries. This example already clamps ``x1, y1, x2, y2`` to prevent out-of-range drawing.

- Detection looks chaotic

  If too many objects are detected and the screen becomes cluttered, it may be hard to read the results.

  Limit the number of drawn detections using ``MAX_DRAW`` (for example, 10–20) to keep the visualization clear and stable.

-----------------------------
9. Summary
-----------------------------

- This chapter implemented general-purpose object detection based on MediaPipe Tasks;
- Used the EfficientDet Lite0 model, balancing accuracy and performance;
- Mastered the method for visualizing detection results;
- Can be extended to custom models (e.g., fruit, vehicle, hazardous item detection scenarios).