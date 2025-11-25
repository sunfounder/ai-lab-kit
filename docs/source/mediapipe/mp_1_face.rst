.. _mp_face:

1. Face Detection
===========================

This section introduces how to use the **MediaPipe Face Mesh** module on a **Raspberry Pi** for real-time face detection and facial landmark mesh drawing.

.. image:: img/mp_face_mesh_demo.png
   :alt: MediaPipe FaceMesh
   :align: center

MediaPipe is a cross-platform machine learning pipeline framework developed by Google, supporting real-time processing of video streams and images. The Face Mesh module is a model provided by MediaPipe for real-time face detection and landmark tracking, which can be used to build various facial recognition and interaction applications.

Compared to OpenCV's Haar detection, MediaPipe uses a deep learning model for detection, offering:

- ✅ Higher accuracy
- ✅ Better robustness to lighting and angles
- ✅ Supports facial landmark tracking (468 points)
- ✅ Seamless integration with OpenCV, allowing direct drawing of detection results on video streams.

------------------------
1. Run the Code
------------------------

Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).
4. You have installed the **mediapipe** environment (see :ref:`mediapipe_install`).

Open the terminal in VNC and enter the following command:

.. code-block:: bash

   sudo ~/mediapipe_env/bin/python3 ~/ai-lab-kit/mediapipe/mp_face.py

-----------------------------
2. Code Example
-----------------------------

The complete code is shown below:

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the mp_face_mesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,          # Set to False for video streams
       max_num_faces=1,                  # Maximum number of faces to detect
       refine_landmarks=True,           # Whether to refine landmarks
       min_detection_confidence=0.5     # Detection confidence threshold
   )

   # Open Raspberry Pi camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 → BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert BGR to RGB (MediaPipe requires RGB)
       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # Face detection and landmark tracking
       results = face.process(frame)

       # Convert RGB back to BGR (for OpenCV display)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       # Draw detected facial landmarks
       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After running the program, you will see the live camera feed, and a facial mesh will be automatically drawn when a face is detected.

-----------------------------
3. Key Steps Explanation
-----------------------------

**Import Libraries**

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

Picamera2 (``from picamera2 import Picamera2``): The official upper-level interface for libcamera on Raspberry Pi. It is used to open the camera, set resolution/pixel format, and capture frames.

OpenCV (``import cv2``): A common computer vision library. It handles color space conversion (BGR↔RGB), display windows (imshow), drawing graphics/text, etc.

MediaPipe Face Mesh (``mp_face_mesh``): The face mesh module in Google's real-time ML framework. It returns 468 (or 478, depending on refine_landmarks) stable 2D keypoints on a face. It can detect/track facial landmarks. It is also fast, robust, and adaptable to lighting/angles.

``drawing_utils`` / ``drawing_styles``: MediaPipe's built-in drawing tools and style presets, used to draw landmarks and connections (mesh) onto the image, with aesthetically pleasing and consistent results.

**Initialize FaceMesh Model**

.. code-block:: python

   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

- ``static_image_mode``: False for continuous video streams; True for single image detection (photos).
- ``max_num_faces``: Maximum number of faces to detect.
- ``refine_landmarks``: Enable refined landmarks (e.g., pupil positions). More accurate, slightly slower; recommended for fine-grained analysis (expression, gaze).
- ``min_detection_confidence``: Detection confidence threshold. 0.5 means only detections with confidence greater than 50% are considered valid.
- ``min_tracking_confidence``: Threshold for the tracking phase; can be lowered appropriately if tracking is unstable. (Not used here)

**Camera Configuration**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

- ``Picamera2``: Raspberry Pi camera module.
- ``create_preview_configuration``: Create camera preview configuration.

   - ``size``: Resolution, width × height. 640×480 offers a good balance between speed and accuracy on Raspberry Pi; can be reduced to 320×240 for smoother performance or increased to 1280×720 for more detail (may drop frames).
   - ``format``: Pixel format, XRGB8888 represents 8-bit 4-channel (BGRA), compatible with OpenCV.
- ``configure``: Configure the camera.
- ``start``: Start the camera.

**Capture Camera Frame**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

Picamera2 outputs in **XRGB8888** format, which needs to be converted to BGR for use with OpenCV.

**RGB Conversion and Model Inference**

.. code-block:: python

   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = face.process(frame)

- MediaPipe FaceMesh requires the input image to be in RGB format.
- ``face.process(frame)`` performs face detection/landmark inference. Returns ``results``, containing:

   - ``multi_face_landmarks``: Landmarks for each face (landmark[x].x / y / z are normalized coordinates, 0~1)
   - Other internal intermediate results (not typically used directly)

**Draw Detection Results**

.. code-block:: python

   if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
         drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
            connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
         )

- ``results.multi_face_landmarks``: Each detected face corresponds to a set of landmarks (typically 468 points, plus finer points like iris if refine_landmarks=True). The ``for`` loop is used because multiple faces might be detected and need to be drawn individually.

- ``drawing.draw_landmarks``: Draws the 468 facial landmarks:

   - ``image=frame``: The image to draw on, i.e., the input image.
   - ``landmark_list=face_landmarks``: The landmarks to draw.
   - ``connections``: Which connection lines to draw.

      - ``FACEMESH_TESSELATION``: Represents the facial triangular mesh connection lines, effect looks like a layer of triangles over the face.
      - ``FACEMESH_CONTOURS``: Cleaner, only draws facial contours/facial feature boundaries (recommended for demos/explanations).
      - ``FACEMESH_IRISES``: Only draws the irises.

      .. note:: The use of FACEMESH_CONTOURS and FACEMESH_IRISES will be fully explained in subsequent sections, please refer to :ref:`mp_face_iris`.

   - ``landmark_drawing_spec``: Customize the style of the **points**, such as color, thickness, etc.

      - To avoid drawing points, set to ``None``.
      - ``DrawingSpec``: Customizes the style of points and lines. Can be used for both ``landmark_drawing_spec`` and ``connection_drawing_spec``. It can set the following parameters:

         - ``thickness`` is the edge line width of the point.
         - ``circle_radius`` is the point radius.
         - ``color`` is the color, e.g., ``(0, 255, 0)`` for green.
         - ``circle_color`` is the inner color of the point, e.g., ``(0, 255, 0)`` for green.
         - ``alpha`` is the transparency, ranging from 0 to 1.

   - ``connection_drawing_spec``: Customize the style of the connection **lines**, such as color, thickness, etc.

      - To avoid drawing lines, pass ``None``.
      - ``DrawingSpec``: Customizes the style of points and lines. Refer to ``landmark_drawing_spec``.
      - Here, ``get_default_face_mesh_tesselation_style()`` is used directly, which means using the default style (color, transparency, line width are all pre-configured).

   - ``interpolation_steps``: Interpolation steps for smoothing connection lines. Default is 1, meaning no interpolation. Higher steps make lines smoother but increase computation.
   - ``visibility_threshold``: Visibility threshold for filtering out invisible landmarks. Default is 0.5, meaning only landmarks with visibility >= 0.5 are drawn.

---------------------------------------------
4. Common Issues and Troubleshooting
---------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Cause
     - Solution
   * - Camera cannot open
     - CSI interface not enabled / Picamera2 configuration error
     - Check ``sudo raspi-config`` → Interface Options → Camera
   * - Program starts slowly
     - First-time model loading, initialization is slow
     - Wait a few seconds; subsequent runs will be faster
   * - Unstable detection / Lagging
     - Limited Raspberry Pi performance
     - Reduce resolution (e.g., 320×240), or turn off `refine_landmarks`
   * - "No module named mediapipe"
     - mediapipe not installed or Python version incompatible
     - Use ``pip install mediapipe`` and confirm Python is 64-bit

-----------------------------
5. ✅ Summary
-----------------------------

- MediaPipe FaceMesh uses a deep learning model to achieve high-precision face detection on Raspberry Pi
- Integrates very closely with OpenCV
- Suitable for scenarios like expression recognition, avatar tracking, AR applications
- More robust and easier to extend compared to traditional Haar features

The next section will further introduce **how to use Face Mesh landmarks** for simple facial feature analysis and interaction.