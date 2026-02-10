.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. Green Screen
====================================

This chapter utilizes the **person segmentation** feature of MediaPipe Pose to achieve **person cutout** + **background replacement with green** (green screen).
This separates the subject from the background, facilitating subsequent tasks like virtual backgrounds, chroma key compositing, live streaming effects, etc.

.. image:: img/mp_pose_green.png
   :align: center

**Objective：**

- Use MediaPipe Pose's ``segmentation_mask`` to separate the person from the background;
- Replace the background with solid green (Chroma Key green screen) for later keying in NLE/OBS;
- Provide threshold tuning and edge smoothing suggestions for cleaner cutout effects.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Media_9.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

**Approach：**

1. Initialize the Pose model with ``enable_segmentation=True``;
2. Obtain ``results.segmentation_mask`` per frame (single-channel probability map, range 0~1);
3. Binarize the probability map using a threshold (e.g., 0.5) to get foreground/background regions;
4. Replace the background with solid green (or other colors/images/video frames);
5. (Optional) Apply blur/morphological processing to the mask to improve edges.

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

   sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

If you want to use MediaPipe Pose with a recorded video, you can run the following command:

.. code-block:: bash

   sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

-----------------------------
2. Code Example
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: empty callback for trackbars ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After running the script, the person (foreground) is preserved, and the background is replaced with solid green.
It can be directly used for subsequent keying with **Chroma Key** in OBS, Premiere, DaVinci Resolve, etc.

-------------------------------------
3. Key Points Explanation
-------------------------------------

``segmentation_mask`` is a **single-channel float image** (range 0~1) with the same size as the input frame:

- Value **close to 1**: High probability of being **foreground (person)**;
- Value **close to 0**: High probability of being **background**.

The usual approach is to set a threshold **T** (e.g., 0.5) and create a condition mask:

.. code-block:: python

   condition = (mask > T)[..., None]

Here we set up a trackbar to adjust the threshold in real-time:

.. code-block:: python

   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

Then we can use ``np.where(condition, frame, background)`` to replace the background; here we replace it with green:

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
4. Effect and Edge Optimization
----------------------------------------------------

Direct binarization can cause jagged edges or small holes around hair and clothing edges.
**Light post-processing** can improve edges:

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **Recommended T value range 0.3~0.7**: Can be appropriately lowered in dark environments/conservative models; can be raised with more noise.
   - Don't make the blur kernel too large, otherwise the person's boundary will "leak green".

----------------------------------------------------
5. Using Custom Background (Image/Video)
----------------------------------------------------

Replace solid green with a custom background image:

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

Or use another video as the background (read the next frame ``bg_frame``, resize to the same dimensions, then replace).

----------------------------------------------------
6. Performance and Quality Balance
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Impact
     - Suggestion
   * - Resolution
     - Higher resolution gives finer edges but slower speed
     - Start with 640×480; increase if clearer image needed
   * - model_complexity
     - Higher is more precise but slower
     - Recommended 1~2 on Raspberry Pi
   * - Post-processing strength
     - Too much blur/morphology can "swallow edges/leak green"
     - Small kernel + few iterations, observe edge effect

----------------------------------------------------
7. Common Issues and Troubleshooting
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Possible Cause
     - Solution
   * - Jagged edges/visible seams on person's boundary
     - Caused by direct hard thresholding
     - Lower or raise threshold; add slight blur/closing operation
   * - Missing parts of the person
     - Weak lighting/clothing color similar to background
     - Add fill light; adjust threshold; change background
   * - Low frame rate
     - Resolution too high/model too complex
     - Reduce resolution; lower ``model_complexity``
   * - Green spills onto the subject
     - Green screen replacement conflicts with subject color
     - Use blue/gray background, or change background image

-----------------------------
8.  Summary
-----------------------------

- Using ``segmentation_mask``, we can quickly achieve "person cutout + background replacement";
- Obtain more natural edges through thresholds and lightweight post-processing;
- Suitable for virtual backgrounds, live streaming keying, remote teaching, etc.;
- Next steps could combine **pose skeleton** and **segmentation** for more interactive effects (e.g., only replace background, don't replace foreground overlay skeleton).