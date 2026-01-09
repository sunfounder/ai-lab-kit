.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. Squat Counter
==========================================

In the previous chapter, we implemented basic human pose estimation. This chapter will utilize the **keypoints detected by Pose** to implement a **Squat Counter**.
This is a typical example of "action recognition + counting" applications, usable in smart fitness systems.

.. image:: img/mp_pose_s2.png
   :alt: Squat Count Example
   :align: center

**Objective：**

- Use MediaPipe Pose to recognize human keypoints;
- Detect hip position in real-time to determine if a squat action is completed;
- Use a state machine and thresholds to avoid duplicate counting;
- Overlay results in real-time on the camera feed.

**Approach：**

1. Use MediaPipe Pose to detect 33 human body keypoints.
2. Select the y-coordinates of Shoulder, Hip, and Ankle to calculate the relative height of the hip.
3. Set upper and lower thresholds (e.g., 0.55 and 0.45) to count via "squat down - stand up" state changes.
4. Draw the squat count and current hip value on the screen.

.. note::
   - This example does not use angle detection but calculates using normalized coordinates, avoiding computational complexity;
   - Suitable for real-time operation on lightweight devices like Raspberry Pi.

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

   sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

-----------------------------
2. Code Implementation
-----------------------------

Here is the complete squat counter implementation:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After executing the script, the system will:

- Detect the human skeleton;
- Calculate the relative hip position;
- Count +1 when a complete cycle from "squat down" to "stand up" is finished;
- Display **Squats: N** and the current HipRel value on the screen in real-time.

-----------------------------------------------
3. Coordinate and State Design
-----------------------------------------------

We use the following 6 keypoints (3 on each side):

.. list-table::
   :header-rows: 1

   * - Keypoint
     - Index
     - Description
   * - Shoulder
     - 11 (Left) / 12 (Right)
     - Upper reference
   * - Hip
     - 23 (Left) / 24 (Right)
     - Core for calculating squat position
   * - Ankle
     - 27 (Left) / 28 (Right)
     - Lower reference

.. image:: img/mp_pose_s1.png
   :alt: MediaPipe Pose Keypoints
   :align: center

**Hip Relative** value calculation formula:

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- Larger hip_rel means closer to the ground (i.e., squatting down).
- Smaller hip_rel means standing upright.

We define two thresholds:

- **DOWN_TH = 0.55**: Considered entering the bottom of the squat
- **UP_TH = 0.45**: Considered returning to standing

Use a simple state machine for reliable counting:

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
4. Parameter Tuning and Optimization
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Adjustment Suggestion
   * - DOWN_TH
     - Squat action threshold
     - Higher value requires deeper squat to count
   * - UP_TH
     - Stand up action threshold
     - Lower value requires standing more upright
   * - model_complexity
     - Pose model complexity
     - Use 1 for faster speed
   * - Resolution
     - Affects frame rate and accuracy
     - Recommended 640×480

.. tip::
   For people of different heights, adaptive thresholds or personalized calibration can be used for more accurate counting.

---------------------------------------------------------
5. Common Issues and Troubleshooting
---------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Cause
     - Solution
   * - Inaccurate counting
     - Incorrect thresholds / Improper form
     - Adjust thresholds by printing hip_rel in real-time
   * - Person not detected
     - Lighting or complex background
     - Ensure frontal standing, clean background
   * - High latency
     - High model complexity
     - Adjust model_complexity=1 or reduce resolution

-----------------------------
6.  Summary
-----------------------------

- Implemented a **real-time squat counter** using Pose keypoints + state machine;
- No complex angle calculations required, high operational efficiency;
- Suitable for Raspberry Pi or other edge device applications;
- Future extensions possible:

  - Push-up/Sit-up detection
  - Data recording and visualization
  - Automatic rhythm guidance and training feedback