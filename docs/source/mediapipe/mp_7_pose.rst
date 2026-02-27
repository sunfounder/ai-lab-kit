.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. Human Pose Estimation
================================

------------------------------------------------------------
1. Overview
------------------------------------------------------------

Following the implementation of hand and gesture recognition,
this chapter introduces **MediaPipe Pose** —
a lightweight yet powerful real-time human pose estimation module.

Using MediaPipe Pose, we can detect **33 body landmarks**
in real time and draw the full-body skeleton on the video feed.

.. image:: img/mp_pose.png
   :width: 400
   :align: center

This module can be used for:

- Action recognition
- Posture correction
- Fitness monitoring
- Motion analysis

------------------------------------------------------------
2. How It Works
------------------------------------------------------------

The program performs the following steps:

1. Initialize the MediaPipe Pose model
   (configure model complexity and optional segmentation).
2. Capture video frames using ``Picamera2``.
3. Convert frames to RGB format (required by MediaPipe).
4. Run the Pose model to obtain 33 body keypoints.
5. Draw keypoints and skeleton connections using OpenCV.
6. Display the annotated video stream in real time.

This chapter lays the foundation for more advanced
human–computer interaction and body motion analysis tasks.


------------------------
3. Run the Code
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   If you want to use MediaPipe Pose with a recorded video, you can run the following command:

   .. code-block:: bash
   
      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. After running the program, a window titled "Show Video" opens and displays the live camera feed.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
         
   When a person appears in front of the camera:
   
   - MediaPipe Pose detects 33 body landmarks in real time.
   - A full-body skeleton is drawn on the video frame.
   - Key joints such as shoulders, elbows, wrists, hips, knees, and ankles are connected with lines.
   
   As the person moves:
   
   - The skeletal keypoints follow the body motion smoothly.
   - The skeleton updates continuously in real time.
   
   If background segmentation is enabled (``enable_segmentation=True``),
   the model internally computes a segmentation mask, although in this example
   only the skeleton is displayed.
   
   If no person is detected, the program simply shows the normal camera feed without annotations.
   
   Press ``q`` to exit the program.
   The camera stops and the OpenCV window closes automatically.

-----------------------------
4. Complete Code
-----------------------------

Here is a basic human pose detection program:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
       static_image_mode=False,  # False for processing video streams
       model_complexity=2,       # 0~2, higher is more accurate
       enable_segmentation=True, # Enable background segmentation (optional)
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Pose detection
      results = pose.process(frame_rgb)

      # Convert RGB back to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If human body is detected, draw skeleton
      if results.pose_landmarks:
         drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After running the program, the camera feed will display a real-time human skeleton, including:

- 33 keypoints
- Skeleton connection lines
- Skeleton follows movement when the person moves

-----------------------------
5. Code Explanation
-----------------------------

**1. Import Libraries**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  Controls the Raspberry Pi camera, based on libcamera.

* **cv2 (OpenCV)**
  Used for image color space conversion (BGR↔RGB), display windows, drawing graphics.

* **mediapipe.python.solutions.pose**
  MediaPipe's **Pose model**, which can detect **33 full-body keypoints** (head, shoulders, elbows, knees, etc.), and can return segmentation masks (human vs. background).

* **drawing_utils / drawing_styles**
  MediaPipe's built-in drawing tools and style definitions, used for drawing keypoints and skeleton lines.

**2. Initialize Pose Model**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Continuous video mode
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False``: Indicates the input is a continuous video stream, not a single image. Tracks after initial detection for faster speed. Usually set to False.

* ``model_complexity=1``: Model complexity, 0=light, 1=medium, 2=high accuracy (slower). Set to 1 or 2 if Raspberry Pi performance allows.

* ``enable_segmentation=True``: Outputs human segmentation mask, can distinguish foreground person from background. When True, enables effects like background replacement, chroma keying. This usage will be explained in subsequent documentation: :ref:`mp_pose_segmentation`

MediaPipe Pose returns a result structure including:

* ``pose_landmarks``: 33 keypoints;
* ``pose_world_landmarks``: 3D world coordinates;
* ``segmentation_mask``: Human segmentation map.

**3. Open Camera**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

* Create camera object ``Picamera2()``
* Set resolution **640x480**, pixel format ``"XRGB8888"`` (4-channel BGRA).
  This format has the best compatibility with OpenCV, eliminating decoding steps.
* Start the camera.

Optional:
``picam2.start_preview(Preview.QTGL)`` can display the video stream window directly on the GPU; commented out here, using OpenCV's ``imshow()`` instead.

**4. Main Loop: Process Each Frame**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Capture a frame from the camera (BGRA format)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. Capture the current frame. Picamera2 returns images in **BGRA** (Blue Green Red + Alpha) format by default.
2. Convert to **BGR** for subsequent OpenCV processing.

.. code-block:: python

   # Convert to RGB for MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

MediaPipe models **must use RGB**.

* Call ``pose.process()`` for keypoint detection.
* ``results`` is a complex object that may contain:

  * ``results.pose_landmarks``: Keypoints (33 points)
  * ``results.pose_world_landmarks``: 3D coordinates
  * ``results.segmentation_mask``: Segmentation mask

.. code-block:: python

   # Convert back to BGR for OpenCV display
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

Convert back because OpenCV's ``imshow()`` requires BGR order.

**5. Draw Pose Keypoints**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

If a human body is detected:

* ``results.pose_landmarks``: Contains ``(x, y, z, visibility)`` for each keypoint.

  * ``x, y``: Normalized coordinates (0~1)
  * ``z``: Relative depth
  * ``visibility``: Keypoint confidence (0~1)

* ``draw_landmarks`` parameter explanation:

   * ``frame``: Image to draw on (BGR format)
   * ``results.pose_landmarks``: Human keypoints for the current frame
   * ``mp_pose.POSE_CONNECTIONS``: Connection rules (which points to connect with lines)
   * ``landmark_drawing_spec``: Point drawing style
   * ``connection_drawing_spec``: Line drawing style (can be omitted, uses system default style)

Effect: Draws the skeleton (connections for head, arms, legs) and keypoints (joint positions) on the image.

**6. Display Frame & Exit Logic**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

Display each frame in the ``"Show Video"`` window.
Exit the loop when the 'q' key is pressed.

**7. Release Resources**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Stop preview, release camera, close all OpenCV windows.

-----------------------------
6. Pose Model Introduction
-----------------------------

The MediaPipe Pose module returns **33 keypoints**, covering areas like the head, torso, arms, and legs:

.. list-table::
   :header-rows: 1

   * - Body Part
     - Index
   * - Nose
     - 0
   * - Left/Right Shoulder
     - 11 / 12
   * - Left/Right Elbow
     - 13 / 14
   * - Left/Right Wrist
     - 15 / 16
   * - Left/Right Hip
     - 23 / 24
   * - Left/Right Knee
     - 25 / 26
   * - Left/Right Ankle
     - 27 / 28
   * - Left/Right Foot Index
     - 31 / 32

These points can be used for **posture judgment**, **action counting** (e.g., squats, push-ups, yoga pose detection), etc.

-----------------------------
7. Performance and Tuning
-----------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Impact
     - Optimization Suggestion
   * - Resolution
     - Higher resolution increases accuracy but also latency
     - Use 640x480 to balance performance and speed
   * - model_complexity
     - Improves recognition accuracy but slows computation
     - Recommended 1~2 for Raspberry Pi
   * - segmentation
     - Increases GPU/CPU load
     - Recommended to disable if background replacement is not needed

------------------------------------------------------------
8. Troubleshooting
------------------------------------------------------------

- No human detected

  If the program runs but no person is detected, make sure the entire body is inside the camera frame. Avoid strong backlight and improve lighting conditions. Keep a distance of about 1–2 meters from the camera for best results.

- Video is slow or lagging

  If the frame rate is low, try reducing the resolution to 640×480 or lower. Set ``model_complexity = 1`` for better performance. Disable segmentation if it is not required, and close other background programs to free system resources.

- Segmentation fault occurs

  Most segmentation faults are caused by a mismatch between the system architecture and the installed MediaPipe wheel.

  Check your system architecture:

  .. code-block:: bash

     uname -m

  The output should be ``aarch64``.

  If you see ``armv7l`` or ``armhf``, you are using 32-bit Raspberry Pi OS, which is not compatible with the official MediaPipe wheel.

  You can also verify in Python:

  .. code-block:: python

     import platform
     print(platform.machine())

  The result must also be ``aarch64``.

- Using aarch64 but still getting segmentation fault

  This may happen if some TensorFlow Lite XNNPACK kernels are not fully compatible with your MediaPipe build.

  Possible solutions:

  - Use ``model_complexity = 1`` (recommended in this tutorial).
  - Make sure MediaPipe is installed in the correct virtual environment.
  - Install a Raspberry Pi–optimized wheel such as ``mediapipe-bin`` (PINTO0309 version).

- ``model_complexity = 2`` crashes but ``1`` works

  Complexity 2 loads a larger model that may trigger advanced CPU optimizations. On Raspberry Pi, some optimized TensorFlow Lite kernels may not be fully supported. Complexity 1 avoids those kernels and is generally more stable and faster on Raspberry Pi.



-----------------------------
9. Summary
-----------------------------

- This chapter implemented **real-time human skeleton detection** based on MediaPipe Pose;
- Pose provides 33 keypoints, usable in fields like fitness, posture analysis, action recognition;
- By adjusting resolution and model complexity, smooth operation can be achieved on Raspberry Pi;
- Based on these keypoints, we can subsequently develop:

  - Action recognition (e.g., "raising hand", "squatting")
  - Posture assessment (e.g., "Is sitting posture correct?")
  - Human interactive control.