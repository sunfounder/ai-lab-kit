.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. Detección de Rostros
===========================

Esta sección presenta cómo usar el módulo **MediaPipe Face Mesh** en una **Raspberry Pi** para la detección de rostros en tiempo real y el dibujo de mallas de puntos de referencia faciales.

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe es un framework de pipelines de aprendizaje automático multiplataforma desarrollado por Google, que admite el procesamiento en tiempo real de flujos de video e imágenes. El módulo Face Mesh es un modelo proporcionado por MediaPipe para la detección de rostros y el seguimiento de puntos de referencia en tiempo real, que se puede utilizar para construir varias aplicaciones de reconocimiento facial e interacción.

En comparación con la detección Haar de OpenCV, MediaPipe utiliza un modelo de aprendizaje profundo para la detección, ofreciendo:

- Mayor precisión
- Mejor robustez frente a la iluminación y los ángulos
- Soporta el seguimiento de puntos de referencia faciales (468 puntos)
- Integración perfecta con OpenCV, permitiendo dibujar los resultados de detección directamente en los flujos de video.

------------------------
1. Ejecutar el Código
------------------------

.. important::


   Antes de comenzar, asegúrate de:

   * Tener el soporte para cámara ensamblado
   * Poder acceder al escritorio de Raspberry Pi
   * Tener el paquete de código instalado
   * Tener Fusion HAT+ instalado y configurado
   * Tener OpenCV instalado

   Para obtener instrucciones detalladas, consulta :ref:`opencv_install`.

#. Abre la terminal e ingresa el siguiente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. Después de ejecutar el script, OpenCV abre una ventana titulada "Show Video" y muestra el flujo de video en vivo capturado desde la cámara Raspberry Pi.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   * Si aparece un rostro frente a la cámara, el programa lo detecta y dibuja una malla detallada de puntos de referencia faciales en el rostro en tiempo real. La malla sigue los movimientos faciales suavemente a medida que la persona se mueve, parpadea o cambia de expresión.
   * Si no se detecta ningún rostro, la ventana continúa mostrando la transmisión normal de la cámara sin puntos de referencia.

   El flujo de video se ejecuta continuamente hasta que el usuario cierra el programa.
   Para salir del programa, presiona q en el teclado.
   La cámara se detendrá y todos los recursos de OpenCV se liberarán automáticamente.

------------------------
2. Código de Ejemplo
------------------------

El código completo se muestra a continuación:

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

Después de ejecutar el programa, verás la transmisión de la cámara en vivo, y se dibujará automáticamente una malla facial cuando se detecte un rostro.

-----------------------------
3. Explicación de Pasos Clave
-----------------------------

#. Importar bibliotecas

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   Estas bibliotecas se utilizan para:

   - Controlar la cámara Raspberry Pi
   - Procesar y mostrar imágenes
   - Detectar puntos de referencia faciales

#. Inicializar FaceMesh

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   Esto crea el modelo de detección facial.
   Rastrea un rostro continuamente en modo video.

#. Iniciar la cámara

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   La cámara comienza a transmitir a una resolución de 640x480.

#. Capturar fotogramas en un bucle

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Cada bucle captura un fotograma y convierte el formato para OpenCV.

#. Detectar puntos de referencia faciales

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   El fotograma se convierte a RGB.
   MediaPipe analiza la imagen y detecta los puntos de referencia faciales.

#. Dibujar la malla facial

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   Si se detecta un rostro, se dibuja una malla sobre él.

#. Mostrar el resultado y salir

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   Presiona ``q`` para detener el programa.
   La cámara se cerrará automáticamente.

---------------------------------------------
4. Problemas Comunes y Solución de Problemas
---------------------------------------------

* La cámara no se puede abrir

  * Asegúrate de que el cable de la cámara CSI esté insertado correctamente
  * Habilita la interfaz de la cámara:

    ``sudo raspi-config`` → Interface Options → Camera

  * Reinicia la Raspberry Pi después de habilitarla

* El programa se inicia lentamente

  La primera ejecución carga el modelo MediaPipe, lo que puede tardar unos segundos.
  Esto es normal. Las ejecuciones posteriores serán más rápidas.

* Detección inestable / Retraso

  * Reduce la resolución de la cámara (por ejemplo, 320x240)
  * Desactiva ``refine_landmarks`` para reducir el uso de CPU
  * Cierra otros programas en ejecución

* No module named ``mediapipe``

  Instala MediaPipe:

  .. code-block:: bash

     pip install mediapipe

  Asegúrate de estar usando un sistema Raspberry Pi OS de 64 bits.

-----------------------------
5. Resumen
-----------------------------

- MediaPipe FaceMesh utiliza un modelo de aprendizaje profundo para lograr una detección facial de alta precisión en Raspberry Pi
- Se integra muy estrechamente con OpenCV
- Adecuado para escenarios como reconocimiento de expresiones, seguimiento de avatares, aplicaciones de RA
- Más robusto y fácil de extender en comparación con las características Haar tradicionales

La siguiente sección presentará **cómo usar los puntos de referencia de Face Mesh** para el análisis de características faciales simples y la interacción.
