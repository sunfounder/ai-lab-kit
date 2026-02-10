.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. CAMShift Object Tracking
==============================

In the previous chapter, we learned the MeanShift algorithm, which can continuously track a target in a video based on its color histogram.  
In this section, we introduce **CAMShift (Continuously Adaptive Mean Shift)**,  
which extends MeanShift by **automatically adapting the window size and orientation**, making it more practical for real-world applications.  
Additionally, in this example we’ll track a target **based on brightness rather than color**, which is also very common in practice.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. Algorithm Features
---------------------

**MeanShift** can only track target position and uses a fixed-size window.  
**CAMShift** tracks position **and** automatically adjusts window size and angle.

For example, when the target approaches the camera, the tracking box grows; when the target moves away, it shrinks; when the target rotates, the box rotates accordingly.

.. image:: img/opencv_camshift.png
   :alt: CAMShift tracking illustration
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
      python3 cv_6_camshift.py

#. When you run the program, an OpenCV window named **CAMShift Tracker** will appear and start playing the video file *sample3.mp4*.  

   The program tracks the black cat using the CAMShift (Continuously Adaptive Mean Shift) algorithm.

   A green rotated bounding box will be drawn around the tracked object.  
   As the cat moves or changes its size and orientation, the tracking window will automatically adapt its position, size, and angle.

   You can exit the program in two ways:

   * Press the **q** key on the keyboard  
   * Close the window by clicking the close button (X)  

   After exiting, the video playback stops and all OpenCV windows are closed.

3. Complete Code
---------------------

Open ``cv_6_camshift.py`` to view the full code.

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Code Explanation
---------------------------

#. Open the video file and read the first frame:

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift needs an initial frame to learn what to track.

#. Set the initial tracking window (ROI):

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   This rectangle should cover the target object in the first frame.  
   CAMShift will update this window automatically during tracking.

#. Convert the first frame to HSV and extract the ROI:

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV is convenient for tracking because you can choose specific channels (like V for brightness).

#. Build a mask for a dark object (low V values):

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   This keeps only “dark” pixels in the ROI.  
   For black/dark objects, brightness (V) is usually the most useful feature.

#. Compute and normalize a histogram of the V channel:

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - Channel ``2`` means the **V (Value/brightness)** channel in HSV.
   - The histogram describes how “dark/bright” the target ROI is.
   - Normalization makes tracking more stable.

#. Set the termination criteria for CAMShift:

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift stops updating when it reaches 10 iterations or the movement is smaller than 1 pixel.

#. Set playback speed using FPS:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   This sets a delay so the video plays close to its original FPS.

#. Create a probability map using back projection (V channel):

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   Back projection highlights pixels in the frame whose V values match the ROI histogram.  
   Brighter values in ``back_proj`` mean “more likely to be the target”.

#. Track using CAMShift and update the window:

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift is based on MeanShift, but it can also adapt the **size and rotation** of the tracking window.

   - ``track_window`` is updated each frame.
   - ``rot_rect`` contains a rotated rectangle (center, size, angle).

#. Draw the rotated tracking box:

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   This converts the rotated rectangle into four corner points and draws it on the frame.

#. Exit conditions (keyboard + window close):

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   Press ``q`` to quit, or close the window to stop safely.

#. Release resources:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Always release the video file and close windows at the end.


5. CAMShift vs. MeanShift
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - MeanShift
     - CAMShift
   * - Window size
     - Fixed
     - Adaptive
   * - Angle
     - Not supported
     - Supports rotation
   * - Tracking accuracy
     - Moderate
     - Higher, more adaptive
   * - Applications
     - Static targets
     - Complex motion, rotating targets

CAMShift is an upgrade over MeanShift,  
better handling target deformation, rotation, and distance changes—well-suited for real-world scenarios.

6. Extensions and Practice
-------------------------------------------

- Adjust the ``inRange`` thresholds to track green or blue targets  
- Combine with live camera input to build a real-time color-based tracking system


7. Advanced: Interactive ROI Selection and Auto-Adjusting HSV Thresholds
-------------------------------------------------------------------------

As in the previous section, this project can also use mouse interaction to select the ROI and automatically adjust HSV thresholds.

Run ``cv_6_camshift_auto.py`` for the modified code.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

When you run the program, the first frame of the video will be displayed, and you will be asked to select a Region of Interest (ROI) with the mouse.

Drag the mouse to draw a rectangle around the target object, then press **Enter** or **Space** to confirm the selection.  
Press **Esc** to cancel the selection.

After selecting the ROI, a window named **CAMShift Tracker** will appear.  
The selected object will be tracked with a green rotated rectangle, and the tracking window will automatically adapt its position, size, and orientation as the object moves.

To stop the program:

* Press the **q** key on the keyboard  
* Or close the display window using the close button (X)  

After exiting, the video playback stops and all OpenCV windows are closed.


.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

   ...

