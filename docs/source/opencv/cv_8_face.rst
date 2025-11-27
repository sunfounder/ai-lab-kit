8. Face and Eye Detection
=========================================

In this chapter, we will use the Raspberry Pi’s Picamera2 to capture video and apply OpenCV’s Haar feature classifiers for **real-time face and eye detection**.  
This approach is lightweight and highly practical—great for beginners deploying on a Raspberry Pi.

1. Haar Features and Detection Principles
-----------------------------------------

1. Essence of Haar Features

Haar features are a classic method for object detection. They encode **patterns of brightness differences** within image regions to determine whether a region likely contains a face, eyes, and so on.

Typical Haar feature examples:

- Eye regions are usually darker than the forehead above  
- Brightness is symmetric on both sides of the nose bridge  
- The area below the mouth often shows a clear edge pattern

.. image:: img/opencv_haar_f.png
   :alt: Illustration of Haar features
   :align: center

OpenCV requires pre-trained Haar classifiers (``.xml`` files). They are already included in the example directory—just load and use them.

2. Detection Pipeline

   1. Load the trained Haar model using ``CascadeClassifier``  
   2. Convert the real-time video to grayscale (to improve efficiency)  
   3. Use ``detectMultiScale`` to detect face/eye regions  
   4. Draw rectangles around detected targets

.. image:: img/opencv_haar_show.png
   :alt: Detection pipeline illustration
   :align: center


2. Run the Code
------------------------



Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).

Open the terminal in VNC and enter the following command:



.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_haarcascade.py


.. tip::
   
   We also provide ``cv_haarcascade_video.py`` for detecting faces and eyes from a video file.


3. Complete Code
----------------


.. code-block:: python

   # Python program to demonstrate face and eye detection using Raspberry Pi Camera
   import numpy as np
   import cv2
   from picamera2 import Picamera2

   # 1. Trained XML classifiers for face and eye detection
   face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

   # 2. Initialize Picamera2
   picam2 = Picamera2()

   # Configure camera for video capture
   config = picam2.create_video_configuration(
      main={"size": (640, 480)},  # Adjust resolution as needed
   )
   picam2.configure(config)

   # Start camera
   picam2.start()

   print("Camera started. Press 'q' to quit.")

   while True:
      start_time = cv2.getTickCount()
      
      # 3. Capture frame from Pi Camera
      frame = picam2.capture_array()
      
      # 4. Convert RGB (PiCamera) to BGR (OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
      
      # 5. Convert to grayscale for detection
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
      # 6. Detect faces of different sizes in the input image
      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
      
      face_count = 0
      eye_count = 0
      
      for (x, y, w, h) in faces:
         face_count += 1
         # Draw a rectangle around the face
         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
         
         # Add face label
         cv2.putText(frame, f'Face {face_count}', (x, y-10), 
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
         
         roi_gray = gray[y:y + h, x:x + w]
         roi_color = frame[y:y + h, x:x + w]
         
         # 8. Detect eyes in the face region
         eyes = eye_cascade.detectMultiScale(roi_gray)
         
         # Draw rectangles around eyes
         for (ex, ey, ew, eh) in eyes:
               eye_count += 1
               cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)
      
      # 9. Display the frame
      cv2.imshow('Raspberry Pi Camera - Face Detection', frame)
      
      # Wait for key press
      k = cv2.waitKey(1) & 0xff
      if k == ord('q'):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()
   print("Camera stopped.")

4. Results
-------------------

- Place ``haarcascade_frontalface_default.xml`` and ``haarcascade_eye.xml`` in the code directory or provide correct paths.
- Ensure the Raspberry Pi camera (Picamera2) works properly.
- Press ``q`` to exit.
- Best results under good lighting.




5. Code Explanation
----------------------

1. Load Haar Classifiers

.. code-block:: python

   face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

- These two XML files are OpenCV’s official pre-trained Haar models for faces and eyes.
- After loading with ``CascadeClassifier``, you can directly call ``detectMultiScale`` to perform detection.

..  Common models:
..
..   - ``haarcascade_frontalface_default.xml`` → frontal face detection
..   - ``haarcascade_eye.xml`` → eye detection
..   - ``haarcascade_profileface.xml`` → profile (side) face detection
..
..  You can find them under OpenCV’s ``data/haarcascades`` directory.

2. Convert to Grayscale

.. code-block:: python

   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

Haar features focus on brightness patterns rather than color.  
Grayscale conversion:

- Reduces computation cost  
- Suppresses noise and improves detection accuracy

3. Face Detection

.. code-block:: python

   faces = face_cascade.detectMultiScale(gray, 1.3, 5)

- ``1.3``: image pyramid scale factor. Larger → faster but slightly less precise.  
- ``5``: minimum neighbors for a detection. Larger → fewer false positives but may miss some faces.

``detectMultiScale`` returns rectangles for all detected faces as ``(x, y, w, h)``.

4. Draw Face Bounding Boxes

.. code-block:: python

   cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)

- Draw rectangles on the frame to visualize detections.
- Use different colors for different detections:

  - Blue/yellowish box → face  
  - Orange box → eyes

5. Eye Detection (ROI)

.. code-block:: python

   eyes = eye_cascade.detectMultiScale(roi_gray)

- Detect eyes **within** the detected face region to reduce false positives drastically.
- The result returns ``(ex, ey, ew, eh)``, which you can draw via ``cv2.rectangle``.

6. Display Results

.. code-block:: python

   cv2.imshow('Raspberry Pi Camera - Face Detection', frame)

- The frame displays face and eye bounding boxes in real time.
- Press ``q`` to exit.


6. Pros and Cons of Haar Detection
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Advantages
     - Disadvantages
   * - Speed
     - Very fast; suitable for Raspberry Pi
     - -
   * - Accuracy
     - Works well for frontal faces
     - Sensitive to rotation and profile views
   * - Lighting
     - Good under even lighting
     - Performance drops if too bright/dark
   * - Model
     - Small model size; easy to deploy
     - Less accurate than deep learning methods

Because it’s lightweight and fast, Haar features are still very practical on embedded devices.


7. Common Improvements
----------------------

1. **Lighting Preprocessing**: Apply histogram equalization or CLAHE before detection to improve performance in low light.  
2. **Multi-Angle Detection**: Load both frontal and profile face classifiers to detect more poses.  
3. **More Facial Features**: Add Haar classifiers for eyes/mouth/nose to enrich detection.  
4. **Use DNN Instead of Haar**: OpenCV DNN + ResNet/MobileNet can yield higher accuracy (but require more compute).



8. Extended Exercises
---------------------

- Use ``cv2.equalizeHist`` on the grayscale image to enhance low-light detection.  
- Add mouth or nose Haar classifiers to detect more facial features.  
- Record the detection process with ``cv2.VideoWriter``.  
- Combine with GPIO output to make a Raspberry Pi project: “turn on LED when a face is detected.”
