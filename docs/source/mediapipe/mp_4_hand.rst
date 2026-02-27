.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. Hand Detection
===============================

------------------------------------------------------------
1. Overview
------------------------------------------------------------

In the previous section, we implemented face detection
and landmark tracking using MediaPipe.

This section introduces **MediaPipe Hands** —
a lightweight and stable real-time hand landmark detection module.

Using this module, we can:

- Detect up to two hands simultaneously
- Identify 21 landmarks per hand
- Visualize hand skeleton connections in real time

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. How It Works
------------------------------------------------------------

The program follows these steps:

1. Initialize the MediaPipe Hands model.
2. Capture frames from the Raspberry Pi camera.
3. Convert the image to RGB format (required by MediaPipe).
4. Detect hand landmarks using the Hands module.
5. Draw the 21 landmarks and their connection lines.
6. Display the annotated video stream in real time.

This module serves as the foundation for:

- Gesture recognition
- Finger counting
- Interactive control systems
- Touchless human–computer interaction

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. After running the program, a window titled "Show Video" opens and displays the live camera feed.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
   
   When one or two hands appear in front of the camera:
   
   - MediaPipe detects each hand in real time.
   - 21 landmark points are identified on each hand.
   - The landmarks are connected with lines to form a hand skeleton.
   
   If two hands are visible, both hands are tracked and
   annotated simultaneously.
   
   As the user moves their hands or fingers:
   
   - The landmark points follow the motion smoothly.
   - The hand skeleton updates in real time.
   
   If no hand is detected, the program simply shows
   the normal camera feed without annotations.
   
   Press ``q`` to exit the program.
   The camera stops and the OpenCV window closes automatically.

-----------------------------
4. Complete Code
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
5. MediaPipe Hands Landmarks Description
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
  :width: 400
  :alt: MediaPipe Hands Landmarks Illustration
  :align: center

.. note::
   These coordinates are **normalized coordinates** and can be converted to actual pixel positions based on the image resolution.
   They can be used to calculate angles and distances, enabling gesture recognition.

------------------------------------------------------------
6. Troubleshooting
------------------------------------------------------------

- Unstable hand detection

  Hand detection may become unstable if the lighting is too dim, the background is cluttered, or the hand moves too quickly.
  
  Try improving the lighting, using a plain background, and moving your hands more slowly and steadily.

- No hand detected

  If no hand is detected, the camera angle may be unsuitable, the hand may be too far from the camera, or the resolution may be too low.
  
  Adjust the camera position, move closer, and ensure the resolution is at least 640×480.

- High latency

  If the video response feels slow, the Raspberry Pi may be under heavy load or the resolution may be set too high.
  
  Reduce the resolution (for example, 320×240) and close unnecessary background processes.


-----------------------------
7.  Summary
-----------------------------

- MediaPipe Hands enables stable **real-time hand detection** on the Raspberry Pi.
- Provides 21 landmarks per hand, suitable for:

  - Gesture recognition
  - Virtual control
  - Interactive UI control
  
- Subsequently, we will implement **custom gesture recognition** based on these landmarks.