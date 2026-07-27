.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_emotion:

2. Detección de Emociones
==========================================

-----------------------------
1. Descripción General
-----------------------------

En esta sección, extendemos la detección de Face Mesh para realizar
un reconocimiento básico de emociones.

En lugar de usar modelos de aprendizaje profundo, este método utiliza
la geometría de los puntos de referencia faciales (proporciones de ojos y boca) para clasificar
expresiones en tiempo real.

.. image:: img/mp_face_emotion_happy.png
   :align: center

Emociones reconocibles:

- 😮 Sorprendido
- 😀 Feliz
- 😢 Triste
- 😠 Enojado
- 😐 Neutral

-----------------------------
2. Cómo Funciona
-----------------------------

El programa sigue estos pasos:

1. Usar ``Picamera2`` + ``MediaPipe FaceMesh`` para obtener 468 puntos de referencia.
2. Seleccionar puntos característicos clave alrededor de los ojos y la boca.
3. Calcular proporciones normalizadas:

   - Apertura del ojo
   - Anchura de la boca
   - Apertura de la boca

4. Comparar los valores con umbrales preestablecidos.
5. Mostrar la emoción detectada usando OpenCV.

Ventajas de este enfoque:

- Rápido y ligero (adecuado para Raspberry Pi)
- No requiere red neuronal
- Fácil de ajustar los umbrales

------------------------
3. Ejecutar el Código
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

        sudo python3 ~/ai-lab-kit/mediapipe/mp_face_emotion.py

#. Después de ejecutar el programa, se abre una ventana de video y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_2.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparece un rostro frente a la cámara, el sistema:

   - Detecta 468 puntos de referencia faciales en tiempo real
   - Calcula las proporciones de apertura de ojos y boca
   - Clasifica la expresión facial actual

   La etiqueta de emoción detectada (como ``Happy``, ``Surprised``, ``Sad``, ``Angry`` o ``Neutral``) se muestra en la pantalla de video.

   A medida que el usuario cambia las expresiones faciales, la etiqueta de emoción se actualiza instantáneamente.

   Si no se detecta ningún rostro, el programa continúa mostrando la transmisión normal de la cámara sin una etiqueta de emoción.

   Presiona ``q`` para salir del programa. La cámara se detendrá y la ventana de OpenCV se cerrará automáticamente.


-----------------------------
4. Código Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   import numpy as np

   # --------- Emotion judgment auxiliary function ---------
   def euclidean(p1, p2):
       return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

   def classify_emotion(landmarks):
       """
       landmarks: results.multi_face_landmarks[0].landmark (length ~468)
       Returns (label, details_dict)
       """
       # Keypoint Index (MediaPipe 468 points)
       L_EYE_TOP, L_EYE_BOT = 159, 145
       R_EYE_TOP, R_EYE_BOT = 386, 374
       L_EYE_CENTER, R_EYE_CENTER = 33, 263
       MOUTH_LEFT, MOUTH_RIGHT = 61, 291
       LIP_UP, LIP_DOWN = 13, 14

       # Normalization scale: distance between left and right eye centers
       io = euclidean(landmarks[L_EYE_CENTER], landmarks[R_EYE_CENTER])
       if io < 1e-6:
           return "Neutral", {}

       mouth_width = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT]) / io
       mouth_open  = euclidean(landmarks[LIP_UP], landmarks[LIP_DOWN]) / io
       eye_open_L  = euclidean(landmarks[L_EYE_TOP], landmarks[L_EYE_BOT]) / io
       eye_open_R  = euclidean(landmarks[R_EYE_TOP], landmarks[R_EYE_BOT]) / io
       eye_open    = 0.5 * (eye_open_L + eye_open_R)

       # --------- Simple threshold rules (adjustable) ---------
       if mouth_open > 0.08 and eye_open > 0.055:
           label = "Surprised"
       elif mouth_width > 0.48 and mouth_open > 0.035:
           label = "Happy"
       elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
           label = "Sad"
       elif mouth_open < 0.02 and eye_open < 0.028:
           label = "Angry"
       else:
           label = "Neutral"

       details = {
           "mouth_width": round(mouth_width, 3),
           "mouth_open": round(mouth_open, 3),
           "eye_open": round(eye_open, 3),
       }
       return label, details

   # Initialize FaceMesh
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
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

               # --------- Emotion detection ---------
               label, metrics = classify_emotion(face_landmarks.landmark)

               # Draw emotion label on the frame
               cv2.putText(frame, f"Emotion: {label}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

               # Debug information
               dbg = f"mw:{metrics.get('mouth_width',0)} mo:{metrics.get('mouth_open',0)} eo:{metrics.get('eye_open',0)}"
               cv2.putText(frame, dbg, (20, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutarlo, la categoría de emoción reconocida se mostrará en tiempo real en la transmisión de la cámara, junto con información de depuración que incluye anchura de boca, apertura de boca, apertura de ojos, etc.

-----------------------------
5. Explicación de Pasos Clave
-----------------------------

#. Seleccionar puntos clave

   .. code-block:: python

      # Keypoint Index (MediaPipe 468 points)
      L_EYE_TOP, L_EYE_BOT = 159, 145
      R_EYE_TOP, R_EYE_BOT = 386, 374
      L_EYE_CENTER, R_EYE_CENTER = 33, 263
      MOUTH_LEFT, MOUTH_RIGHT = 61, 291
      LIP_UP, LIP_DOWN = 13, 14

   Estos índices corresponden a:

   - 159, 145 → Bordes superior e inferior del ojo izquierdo
   - 386, 374 → Bordes superior e inferior del ojo derecho
   - 33, 263 → Centros de los ojos (usados para normalización)
   - 61, 291 → Comisuras de la boca
   - 13, 14 → Puntos medios del labio superior e inferior

   .. image:: img/mp_face_point.jpg
      :align: center

#. Normalizar distancias

   Para reducir la influencia de la distancia de la cámara,
   se usa la distancia entre los dos centros de los ojos
   como escala de normalización.

   .. code-block:: python

      def euclidean(p1, p2):
          return np.linalg.norm(
              np.array([p1.x, p1.y]) -
              np.array([p2.x, p2.y])
          )

      io = euclidean(
          landmarks[L_EYE_CENTER],
          landmarks[R_EYE_CENTER]
      )

#. Calcular características geométricas

   .. code-block:: python

      mouth_width = euclidean(
          landmarks[MOUTH_LEFT],
          landmarks[MOUTH_RIGHT]
      ) / io

      mouth_open = euclidean(
          landmarks[LIP_UP],
          landmarks[LIP_DOWN]
      ) / io

      eye_open_L = euclidean(
          landmarks[L_EYE_TOP],
          landmarks[L_EYE_BOT]
      ) / io

      eye_open_R = euclidean(
          landmarks[R_EYE_TOP],
          landmarks[R_EYE_BOT]
      ) / io

      eye_open = 0.5 * (eye_open_L + eye_open_R)

   Características calculadas:

   - ``mouth_width`` → Anchura horizontal de la boca
   - ``mouth_open`` → Apertura vertical de la boca
   - ``eye_open`` → Apertura promedio del ojo

#. Clasificar la emoción usando umbrales

   .. code-block:: python

      if mouth_open > 0.08 and eye_open > 0.055:
          label = "Surprised"
      elif mouth_width > 0.48 and mouth_open > 0.035:
          label = "Happy"
      elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
          label = "Sad"
      elif mouth_open < 0.02 and eye_open < 0.028:
          label = "Angry"
      else:
          label = "Neutral"

   Reglas de emoción (umbrales empíricos):

   - Sorprendido → Boca y ojos muy abiertos
   - Feliz → Boca ancha, ojos normales
   - Triste / Enojado → Boca y ojos casi cerrados
   - Neutral → No coincide con otras condiciones

-----------------------------------------------------
6. Ajuste de Umbrales y Robustez
-----------------------------------------------------

- Los umbrales como ``0.08``, ``0.035``, ``0.018`` se basan en valores empíricos a una resolución de 640x480.
- Si la cámara está más cerca o la resolución es diferente, ajusta los umbrales usando la información de depuración (mw/mo/eo).
- La lógica de juicio de emociones se puede modificar para ser más compleja o usar modelos entrenados para mayor precisión, como calcular la posición relativa de las comisuras de la boca, la forma de la boca y otras características.

------------------------------------------------------------
7. Solución de Problemas
------------------------------------------------------------

- El reconocimiento de emociones no es sensible

  Los umbrales pueden no coincidir con la distancia actual de la cámara.
  Ajusta los valores de ``mouth_open`` y ``eye_open``.

- Latencia de detección

  La resolución puede ser demasiado alta.
  Reduce la resolución o desactiva ``refine_landmarks``.

- No se puede reconocer la emoción

  La iluminación puede ser insuficiente o el ángulo del rostro estar inclinado.
  Mejora la iluminación y mira directamente a la cámara.

-----------------------------
8. Resumen
-----------------------------

- Este capítulo implementó el reconocimiento ligero de emociones basado en **características geométricas + puntos de referencia de FaceMesh**.
- Ofrece ventajas de **alto rendimiento en tiempo real** y **umbrales ajustables**.
- Puede usarse en proyectos como arte interactivo, HCI, detección de estado en aula/reuniones.
