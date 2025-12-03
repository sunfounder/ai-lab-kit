.. _mp_hand_count:

5. Hand Gesture Counting
==============================================

In the previous section, we implemented **real-time detection and landmark drawing** for both hands.
This section will further introduce how to use **finger landmark positions** to implement a simple and efficient function:

**Count the number of raised fingers** to achieve hand gesture number recognition (0~5).

.. image:: img/mp_hand_count.png
   :align: center

**Objective：**

- Use MediaPipe Hands to detect 21 landmarks.
- Analyze the positional relationship between the thumb and other fingers to determine if fingers are extended.
- Count the number of extended fingers and display it in real-time.

**Approach：**

1. Initialize the MediaPipe Hands model.
2. Capture camera video stream and perform hand landmark detection.
3. Use coordinates of finger tips and proximal joints for logical judgment.
4. Count the number of raised fingers and draw it on the frame.
5. Achieve real-time number gesture recognition effect.

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

   sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

-----------------------------
2. Code Example
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2 
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

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


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

In each loop iteration, it determines whether each of the 5 fingers is extended and counts the number of extended fingers. For example:

- ✊ All fingers closed → Count 0
- ☝️ Index finger extended → Count 1
- ✌️ Index + Middle fingers → Count 2
- 🖐️ All five fingers open → Count 5

--------------------------------------------------------------
3. Detection Logic Explanation
--------------------------------------------------------------

MediaPipe Hands returns 21 landmarks.
We primarily use the following two sets to determine if fingers are extended:

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips``: Fingertip positions (Thumb=4, Index=8, Middle=12, Ring=16, Pinky=20)
- ``finger_dips``: Corresponding proximal joints (Thumb=2, Index=6, Middle=10, Ring=14, Pinky=18)

The judgment rules are as follows:

.. code:: python

   # Count the number of fingers raised (right hand)
   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check if thumb is up
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
         finger_count += 1

   # Check if the other fingers are up
   for i in range(1, 5):
         if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
            finger_count += 1

   # Display the number of fingers raised
   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

- **Thumb**: Check if ``tip.x`` is greater than ``dip.x`` (for right hand).
- **Other four fingers**: Check if ``tip.y`` is less than ``dip.y``.
  - If the tip is higher than the dip, the finger is considered extended.

Each condition met increases the count by ``+1``.

-----------------------------
4. Advanced Tips
-----------------------------

- To support both left and right hands:
  - Use ``hands_detected.multi_handedness`` to determine left/right hand.
  - Adjust the x-axis judgment direction for the thumb accordingly.

- Can be extended to include:
  - 🆗 OK gesture recognition
  - 👍 Thumbs up recognition
  - ✊✋✌ Game interactions

-----------------------------------------------------
5. Common Issues and Troubleshooting
-----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Cause
     - Solution
   * - Thumb detection inaccurate
     - Different directions for left/right hands
     - Use ``multi_handedness`` to determine left/right and adjust logic
   * - Unstable detection
     - Insufficient lighting, cluttered background
     - Improve lighting or change background
   * - High latency
     - Resolution too high or CPU overloaded
     - Reduce resolution or optimize algorithm

-----------------------------
6.  Summary
-----------------------------

- Using MediaPipe Hands, we can quickly implement **real-time gesture recognition**.
- This section implemented **number gesture counting** based on fingertip positions, laying the foundation for custom gesture recognition.
- By adapting for left/right hands and expanding judgment rules, more complex interactive scenarios can be achieved.