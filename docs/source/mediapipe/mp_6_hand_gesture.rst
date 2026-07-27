.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_gesture:


6. Reconocedor de Gestos de Mano
==================================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En el capítulo anterior, usamos MediaPipe Hands
para obtener 21 puntos de referencia de la mano y visualizar el esqueleto de la mano.

Este capítulo presenta **MediaPipe Tasks – Gesture Recognizer**,
que puede generar directamente etiquetas de gestos semánticos como:

- ``Thumb_Up``
- ``Open_Palm``
- ``Victory``
- ``Closed_Fist``

Combinando:

- ``Picamera2`` para captura de video
- ``MediaPipe Hands`` para visualización de puntos de referencia
- ``Gesture Recognizer`` para clasificación

podemos lograr el reconocimiento de gestos en tiempo real
con renderizado del esqueleto y visualización de etiquetas.

.. image:: img/mp_hang_gesture.png
   :alt: Gesture Recognizer
   :align: center


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El programa realiza los siguientes pasos:

1. Capturar fotogramas de video usando ``Picamera2``.
2. (Opcional) Usar ``MediaPipe Hands`` para dibujar puntos de referencia.
3. Usar **MediaPipe Tasks – Gesture Recognizer** en modo ``VIDEO``.
4. Para cada mano detectada, obtener:

   - Lista de categorías de gestos (etiqueta + confianza)
   - Lateralidad (Izquierda / Derecha)
   - Puntos de referencia normalizados

5. Seleccionar el gesto superior y dibujar
   "etiqueta + puntuación de confianza"
   sobre la mano correspondiente.

.. note::

   Este capítulo usa la API de **Tasks de MediaPipe (0.10+)**.


------------------------------------------------------------
3. Modelo
------------------------------------------------------------

Gesture Recognizer requiere un archivo de modelo:

``gesture_recognizer.task``

El archivo de modelo ya está incluido en el directorio de ejemplo.
Usa la versión proporcionada.

El modelo integrado admite las siguientes etiquetas de gestos:

- 0 → ``Unknown``
- 1 → ``Closed_Fist``
- 2 → ``Open_Palm``
- 3 → ``Pointing_Up``
- 4 → ``Thumb_Down``
- 5 → ``Thumb_Up``
- 6 → ``Victory``
- 7 → ``ILoveYou``

------------------------
4. Ejecutar el Código
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_gesture.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_6.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparecen una o dos manos frente a la cámara, el programa:

   - Detecta y dibuja los 21 puntos de referencia de la mano y las líneas de conexión (esqueleto de la mano) en tiempo real.
   - Ejecuta el modelo Gesture Recognizer en cada fotograma para clasificar el gesto.

   Si se reconoce un gesto con una puntuación superior a ``SCORE_THRESHOLD`` (por defecto 0.5), el programa muestra una etiqueta cerca de la mano correspondiente, incluyendo:

   - Lateralidad (Izquierda/Derecha)
   - Nombre del gesto (por ejemplo, ``Thumb_Up``, ``Open_Palm``, ``Victory``)
   - Puntuación de confianza (por ejemplo, ``0.87``)

   También se dibuja un rectángulo delgado alrededor del área de la mano para que la ubicación de la etiqueta sea más clara.

   A medida que cambias las poses de la mano, la etiqueta del gesto y la puntuación se actualizan continuamente en tiempo real.

   Si no se detecta ninguna mano, o la confianza del gesto está por debajo del umbral, solo se muestra el esqueleto de la mano (o la transmisión de la cámara sin procesar) sin etiquetas de gesto.

   Presiona ``q`` para salir del programa. La cámara se detiene y la ventana de OpenCV se cierra automáticamente.


-----------------------------
5. Código Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Import MediaPipe Tasks (Gesture Recognizer)
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   from pathlib import Path

   # --------------------- Settings ---------------------
   BASE_DIR = Path(__file__).resolve().parent
   GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")  # Path to the gesture model
   SCORE_THRESHOLD = 0.5                           # Show gestures above this score
   # ---------------------------------------------------

   # Initialize the Hands model (kept for landmark drawing)
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

   # Initialize Gesture Recognizer (VIDEO mode for streaming)
   BaseOptions = python.BaseOptions
   GestureRecognizerOptions = vision.GestureRecognizerOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=GESTURE_MODEL_PATH)
   gr_options = GestureRecognizerOptions(
       base_options=base_options,
       running_mode=RunningMode.VIDEO
   )
   recognizer = vision.GestureRecognizer.create_from_options(gr_options)

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # (Optional) helper to draw a label near a hand bounding box computed from landmarks
   def draw_gesture_label(frame_bgr, norm_landmarks, text, color=(0, 175, 255)):
       """
       norm_landmarks: list of 21 normalized landmarks (x,y in [0,1]).
       We compute a tight bbox to place the gesture text.
       """
       if not norm_landmarks:
           return
       h, w = frame_bgr.shape[:2]
       xs = [int(lm.x * w) for lm in norm_landmarks]
       ys = [int(lm.y * h) for lm in norm_landmarks]
       x1, y1 = max(0, min(xs)), max(0, min(ys))
       x2, y2 = min(w-1, max(xs)), min(h-1, max(ys))
       cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)
       (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
       y_text = max(0, y1 - th - 6)
       cv2.rectangle(frame_bgr, (x1, y_text), (x1 + tw + 6, y_text + th + 6), color, -1)
       cv2.putText(frame_bgr, text, (x1 + 3, y_text + th + 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert the frame from BGR to RGB (required by MediaPipe)
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # ---- A) Run legacy Hands (for landmark drawing you already have) ----
       hands_detected = hands.process(frame_rgb)

       # ---- B) Run Gesture Recognizer (direct gesture labels) ----
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
       ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
       gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

       # Convert the frame back from RGB to BGR (required by OpenCV)
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

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

       # ---- C) Overlay gesture names on top of each detected hand ----
       if gesture_result and getattr(gesture_result, "gestures", None):
           for i, gesture_list in enumerate(gesture_result.gestures):
               if not gesture_list:
                   continue
               top = gesture_list[0]
               label = top.category_name  # e.g., "Thumb_Up"
               score = top.score or 0.0
               if score < SCORE_THRESHOLD:
                   continue

               hand_label = ""
               if gesture_result.handedness and i < len(gesture_result.handedness):
                   if gesture_result.handedness[i]:
                       hand_label = gesture_result.handedness[i][0].category_name or ""

               text = f"{hand_label} {label} ({score:.2f})".strip()

               hand_lms = None
               if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
                   hand_lms = gesture_result.hand_landmarks[i]

               if hand_lms:
                   draw_gesture_label(frame, hand_lms, text)
               else:
                   cv2.putText(frame, text, (20, 40 + 30*i),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

       # Display the frame with annotations
       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   # Release the camera
   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutar el script, la ventana mostrará el esqueleto de la mano (opcional) y los cuadros de texto de gestos. Cuando se reconozca un gesto que coincida con las categorías del modelo, se mostrará sobre el cuadro delimitador de la mano correspondiente:

- Mano izquierda/derecha (lateralidad)
- Nombre del gesto (ej., ``Thumb_Up``)
- Puntuación de confianza (0~1)

-----------------------------
6. Explicación del Código
-----------------------------

Este ejemplo combina dos partes:

- **Hands (Solutions API)**: se usa para dibujar el esqueleto de la mano (21 puntos de referencia + conexiones).
- **Gesture Recognizer (Tasks API)**: se usa para predecir una etiqueta de gesto como ``Thumb_Up`` o ``Open_Palm``.

**Flujo de alto nivel**

#. Inicializar Hands para el dibujo de puntos de referencia (opcional pero útil para la visualización).
#. Cargar el modelo Gesture Recognizer (``gesture_recognizer.task``) y habilitar el modo ``VIDEO``.
#. Iniciar la cámara y procesar fotogramas en un bucle:

   - Convertir el fotograma a RGB (MediaPipe requiere RGB).
   - Ejecutar Hands para dibujar el esqueleto.
   - Ejecutar Gesture Recognizer para obtener ``etiqueta + puntuación`` para cada mano.
   - Dibujar la etiqueta cerca de la mano correspondiente.

#. Presiona ``q`` para salir y liberar recursos.

**Puntos clave a entender**

- Archivo del modelo

  Gesture Recognizer requiere ``gesture_recognizer.task``. Asegúrate de que el archivo del modelo esté colocado en la misma carpeta que el script (o actualiza la ruta).

- El modo VIDEO requiere marcas de tiempo

  ``recognize_for_video()`` necesita una marca de tiempo en milisegundos que aumente continuamente. En este ejemplo, la generamos usando el tiempo de tick de OpenCV.

- Mostrar etiquetas con un umbral de confianza

  Solo se muestran los gestos con puntuación >= ``SCORE_THRESHOLD``. Esto evita mostrar predicciones inestables.

-----------------------------
7. Parámetros y Ajuste
-----------------------------

.. list-table::
   :header-rows: 1

   * - Parámetro
     - Descripción
     - Sugerencia
   * - ``SCORE_THRESHOLD``
     - Los gestos por debajo de esta puntuación se ignoran
     - Aumentar para reducir falsos positivos; disminuir para mejorar el recall
   * - ``max_num_hands``
     - Número de manos a detectar simultáneamente
     - 2 es suficiente para la mayoría de los escenarios
   * - ``running_mode=VIDEO``
     - Modo de flujo de video, requiere marca de tiempo
     - Mantener (el reconocimiento en streaming es más estable)
   * - Resolución
     - Afecta la velocidad y la precisión
     - Se recomienda 640x480 o menos en Raspberry Pi para mejores FPS

-------------------------------------------------------
8. Solución de Problemas
-------------------------------------------------------

- ``FileNotFoundError: gesture_recognizer.task``

  Esto generalmente significa que la ruta del archivo del modelo es incorrecta.
  Asegúrate de que el archivo del modelo esté colocado en el mismo directorio que el script,
  o actualiza ``GESTURE_MODEL_PATH`` en consecuencia.

- ``ImportError: cannot import name 'vision'``

  Este error indica que la versión de MediaPipe está desactualizada.
  Actualiza MediaPipe a la versión 0.10 o posterior usando:

  ``pip install --upgrade mediapipe``

- La categoría reconocida difiere de la esperada

  El conjunto de categorías del modelo puede diferir, o las condiciones de iluminación pueden afectar el reconocimiento.
  Intenta mejorar la iluminación, simplificar el fondo,
  o cambiar a una versión diferente del modelo.

- Baja tasa de fotogramas

  El rendimiento de Raspberry Pi puede ser limitado.
  Reduce la resolución, desactiva el dibujo del esqueleto,
  o cierra procesos de fondo innecesarios.

-----------------------------
9. Resumen
-----------------------------

- **Gesture Recognizer** permite el reconocimiento de gestos semánticos en tiempo real en Raspberry Pi;
- Combinado con el renderizado del esqueleto de **Hands**, es intuitivo y fácil de depurar;
- Ajustando umbrales y resolución, se puede lograr un equilibrio entre "estabilidad / velocidad";
- Posibilidades futuras:

  - Mapear diferentes gestos a comandos específicos (accesos directos, control GPIO, etc.);
  - Entrenar modelos de gestos personalizados para escenarios específicos.
