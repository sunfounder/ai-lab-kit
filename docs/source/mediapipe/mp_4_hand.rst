.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. Hand Detection
===============================

In the previous section, we learned how to implement face detection and tracking using MediaPipe.
This section will introduce **MediaPipe Hands** — a lightweight, stable, and practical **real-time hand landmark detection** module.
Using it, we can implement **two-hand detection** and **annotation of 21 hand landmarks** on the Raspberry Pi.

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center

**Objective：**

- Use MediaPipe Hands for real-time hand detection and landmark drawing.
- Identify and track both hands, achieving stable landmark visualization.
- Serve as a foundation for subsequent gesture recognition and interactive control.

**Approach：**

1.  Call the Hands module for detection.
2.  Draw the 21 hand landmarks and their connections.
3.  Display real-time detection results.

------------------------
1. Run the Code
------------------------

Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).
4. You have installed the **mediapipe** (see :ref:`mediapipe_install`).

Open the terminal in VNC and enter the following command:

.. code-block:: bash

   sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

-----------------------------
2. Code Example
-----------------------------

The complete example code is as follows:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After running the code, you will see in the camera feed:

- If one or two hands are detected, it will show:

  - 21 hand landmarks
  - Blue connection skeleton
- When the hand moves, the detection will track it in real-time.

--------------------------------------------------------
3. MediaPipe Hands Landmarks Description
--------------------------------------------------------

MediaPipe Hands returns **21 landmarks** for each hand, including locations like the wrist, palm, and fingertips.

Common landmarks include:

.. list-table::
   :header-rows: 1

   * - Index
     - Name
     - Location
   * - 0
     - WRIST
     - Wrist
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - Tips of respective fingers
   * - 5~17
     - Joints
     - Middle joints of respective fingers
   * - 9
     - PALM_CENTER (approximate)
     - Palm area

.. image:: img/mp_hand_point.png
  :width: 600
  :alt: MediaPipe Hands Landmarks Illustration
  :align: center

.. note::
   These coordinates are **normalized coordinates** and can be converted to actual pixel positions based on the image resolution.
   They can be used to calculate angles and distances, enabling gesture recognition.

-----------------------------------------------------
4. Common Issues and Troubleshooting
-----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Cause
     - Solution
   * - Unstable hand detection
     - Insufficient light / Complex background
     - Increase lighting or use a plain background
   * - No detection
     - Camera orientation / resolution unsuitable
     - Adjust camera position and angle
   * - High latency
     - Limited Raspberry Pi performance
     - Reduce resolution, close other processes

-----------------------------
5.  Summary
-----------------------------

- MediaPipe Hands enables stable **real-time hand detection** on the Raspberry Pi.
- Provides 21 landmarks per hand, suitable for:

  - Gesture recognition
  - Virtual control
  - Interactive UI control
  
- Subsequently, we will implement **custom gesture recognition** based on these landmarks.