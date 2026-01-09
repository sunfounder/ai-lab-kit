.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. Facial Contours and Iris Detection
=================================================================

In the previous sections, we implemented basic face mesh detection and simple emotion recognition based on landmarks.
This section will further explain **the more detailed feature connection methods provided by MediaPipe FaceMesh**:

- ``FACEMESH_CONTOURS`` — Facial contour lines (face edges, outer contours of facial features)
- ``FACEMESH_IRISES`` — Iris (eyeball) region detection and drawing

By drawing only the contours and iris features, we can achieve a cleaner and more lightweight visual effect, facilitating subsequent tasks like facial feature extraction and eye movement interaction.

.. image:: img/mp_face_iris.png
   :align: center

**Objective：**

- Use the FaceMesh module to draw only **facial contours and iris regions**, facilitating facial feature analysis and eye tracking.
- Improve drawing efficiency and reduce annotation redundancy.
- Lay the foundation for advanced tasks like "pupil tracking" and "gaze point detection".

**Approach：**

1. Initialize the MediaPipe FaceMesh model.
2. Capture camera video frames and convert them to MediaPipe-compatible RGB format.
3. Draw the outer facial contour lines using ``FACEMESH_CONTOURS``.
4. Draw the iris regions of both eyes using ``FACEMESH_IRISES``.
5. Display only key areas for cleaner and clearer annotations.

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

   sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

-----------------------------
2. Code Example
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize FaceMesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Enable if hardware preview is needed
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      if results.multi_face_landmarks:
         for face_landmarks in results.multi_face_landmarks:
            # Draw facial contours
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_CONTOURS,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            # Draw iris features
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

After running the program, only facial contours and iris regions of both eyes will be displayed on the screen.

-----------------------------
3. Key Steps Explanation
-----------------------------

The code in this section is basically the same as the code in :ref:`mp_face`. The main difference lies in the choice of drawing method. Here we can see that in the main loop, we call the ``draw_landmarks`` function twice, drawing FACEMESH_CONTOURS and FACEMESH_IRISES respectively. You can comment out one of them to see how the effect differs.

``FACEMESH_CONTOURS``

- This is a connection method provided by MediaPipe
- Mainly draws:

  - Outer facial contour
  - Edges of facial features like eyes, nose, lips
- Suitable for simplified visualization of face detection results, making it easier to observe contour changes.

``FACEMESH_IRISES``

- Specifically draws the iris regions of both eyes.
- Includes keypoints and connection lines for left and right eye irises.
- Can be used for subsequent tasks like eye tracking and gaze detection.

``landmark_drawing_spec = None``

- Disables drawing individual points, keeping only connection lines for a cleaner effect.
- If you need to display both points and lines, you can define a ``DrawingSpec``.

``drawing_styles.get_default_face_mesh_contours_style()``

- Gets the default contour drawing style.

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- Gets the default iris connection line drawing style.

--------------------------------------------------
4. Advantages and Application Scenarios
--------------------------------------------------

- **Lightweight Drawing** — Lower rendering burden compared to the full FaceMesh grid.
- **More Focused Features** — Facilitates facial feature localization and iris tracking.
- **High Extensibility** — Can be directly integrated with gaze estimation algorithms or other interaction modules.

**Application Examples:**

- Intelligent interaction systems
- Gaze tracking and eye-controlled interaction
- Expression and pose estimation
- Virtual avatar facial driving

-----------------------------------------------------
5. Common Issues and Troubleshooting
-----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Cause
     - Solution
   * - Iris not detected
     - Insufficient light or face too far
     - Increase lighting or move closer to camera
   * - Contour lines jittery
     - Low detection confidence
     - Increase min_detection_confidence
   * - High latency
     - High resolution or refine_landmarks consuming resources
     - Reduce resolution or turn off refine_landmarks

-----------------------------
6.  Summary
-----------------------------

- ``FACEMESH_CONTOURS`` and ``FACEMESH_IRISES`` are two important connection methods provided by MediaPipe.
- Compared to full mesh drawing, they are more lightweight and intuitive, suitable for practical interaction scenarios.
- The next chapter will introduce how to use these features for gaze tracking and blink detection.