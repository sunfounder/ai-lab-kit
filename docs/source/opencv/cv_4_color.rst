.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. Color Detection
===========================================

Color detection is one of the most fundamental and practical functions in computer vision.  
In this chapter, we will use step-by-step code and explanations to **detect red objects using the HSV color space** and **draw bounding boxes** around them.

This forms the foundation for more advanced object tracking techniques (e.g., CAMShift).

1. Objective and Approach
--------------------------------------------

- Use **Picamera2** to capture real-time camera frames  
- Convert the image from BGR to HSV color space  
- Use ``cv2.inRange`` to extract the red regions  
- Use morphological filtering to remove noise  
- Use ``cv2.findContours`` to find red object contours  
- Draw bounding boxes around the detected red regions

.. image:: img/color_detection.png
   :alt: Color detection preview illustration
   :align: center

2. Run the Code
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

      cd ~/ai-lab-kit/opencv_python
      python3 cv_4_color.py

#. When you run the program, two OpenCV windows will appear on the screen:

   * **Red Detection** – shows the live camera image with green bounding boxes around detected red objects  
   * **Red Mask** – shows the binary mask image used for red color detection  

   The program continuously captures frames from the Raspberry Pi camera and detects red regions in real time.  
   If a red object is detected, a green rectangle and the area value will be displayed on the color image.

   You can exit the program in two ways:

   * Press the **q** key on the keyboard  
   * Close any of the OpenCV windows by clicking the close button (X)  

   After exiting, the camera stops streaming and all OpenCV windows are closed.

3. Complete Code
------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. Code Explanation
--------------------------------

#. Initialize Picamera2 and start streaming:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   This configures the camera at 640×480 and starts the preview stream.  
   ``XRGB8888`` is a 4-channel format, so the captured frames are BGRA-like.

#. Convert the captured frame to a format OpenCV commonly uses:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2 returns a 4-channel image here, so we convert it to standard 3-channel BGR for processing.

#. Use HSV color space for robust color detection:

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV separates color (Hue) from brightness, which makes color detection more stable under different lighting.

#. Define two HSV ranges for red:

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   Red “wraps around” the Hue scale in OpenCV HSV (near 0 and near 180), so two ranges are combined to cover all reds.

#. Clean the mask with morphology (reduce noise and fill holes):

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** removes small noisy dots.
   - **CLOSE** fills small holes inside the detected red regions.

#. Find red regions and filter small blobs:

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   Contours are detected from the binary mask.  
   ``MIN_AREA`` ignores small red regions to reduce false detections.

#. Draw bounding boxes and labels on the result image:

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   This shows where OpenCV found red objects, and prints the detected blob area for reference.

#. Display both the result and the mask:

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   The **result window** shows the camera view with boxes, and the **mask window** shows the red-only binary image.

#. Exit conditions (keyboard + window close):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   Press ``q`` to quit, or close either window to exit safely.

#. Cleanup:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Always stop the camera and close OpenCV windows to release resources.


5. Parameter Tuning Tips
-----------------------------

- ``LOWER_RED1 / UPPER_RED1``: adjust this range to detect other colors.  
  For example, green ≈ ``[35, 50, 50]`` to ``[85, 255, 255]``.

- ``KERNEL``: larger kernels give stronger filtering but may remove small objects.

- ``MIN_AREA``: increasing this value filters out small noisy contours; decreasing it makes detection more sensitive.

.. note::
   You can start by only displaying the ``mask`` and tuning the thresholds until the target region looks clear, then proceed with the rest of the pipeline.




6. Extensions and Practice
--------------------------

- Modify the HSV threshold to detect other colors (e.g., blue or green).  
- Experiment with different morphological parameters in more complex backgrounds.  
