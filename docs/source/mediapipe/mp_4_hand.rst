.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. Detección de Manos
===============================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En la sección anterior, implementamos la detección facial
y el seguimiento de puntos de referencia usando MediaPipe.

Esta sección presenta **MediaPipe Hands** —
un módulo de detección de puntos de referencia de manos en tiempo real, ligero y estable.

Usando este módulo, podemos:

- Detectar hasta dos manos simultáneamente
- Identificar 21 puntos de referencia por mano
- Visualizar las conexiones del esqueleto de la mano en tiempo real

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El programa sigue estos pasos:

1. Inicializar el modelo MediaPipe Hands.
2. Capturar fotogramas de la cámara Raspberry Pi.
3. Convertir la imagen al formato RGB (requerido por MediaPipe).
4. Detectar puntos de referencia de manos usando el módulo Hands.
5. Dibujar los 21 puntos de referencia y sus líneas de conexión.
6. Mostrar el flujo de video anotado en tiempo real.

Este módulo sirve como base para:

- Reconocimiento de gestos
- Conteo de dedos
- Sistemas de control interactivo
- Interacción persona-computadora sin contacto

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparecen una o dos manos frente a la cámara:

   - MediaPipe detecta cada mano en tiempo real.
   - Se identifican 21 puntos de referencia en cada mano.
   - Los puntos de referencia se conectan con líneas para formar un esqueleto de la mano.

   Si dos manos son visibles, ambas manos son rastreadas y
   anotadas simultáneamente.

   A medida que el usuario mueve las manos o los dedos:

   - Los puntos de referencia siguen el movimiento suavemente.
   - El esqueleto de la mano se actualiza en tiempo real.

   Si no se detecta ninguna mano, el programa simplemente muestra
   la transmisión normal de la cámara sin anotaciones.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.

-----------------------------
4. Código Completo
-----------------------------

El código de ejemplo completo es el siguiente:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutar el código, verás en la transmisión de la cámara:

- Si se detectan una o dos manos, se mostrarán:

  - 21 puntos de referencia de la mano
  - Esqueleto de conexión azul
- Cuando la mano se mueve, la detección la seguirá en tiempo real.

--------------------------------------------------------
5. Descripción de los Puntos de Referencia de MediaPipe Hands
--------------------------------------------------------

MediaPipe Hands devuelve **21 puntos de referencia** para cada mano, incluyendo ubicaciones como la muñeca, la palma y las puntas de los dedos.

Puntos de referencia comunes:

.. list-table::
   :header-rows: 1

   * - Índice
     - Nombre
     - Ubicación
   * - 0
     - WRIST
     - Muñeca
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - Puntas de los dedos respectivos
   * - 5~17
     - Joints
     - Articulaciones medias de los dedos respectivos
   * - 9
     - PALM_CENTER (aproximado)
     - Área de la palma

.. image:: img/mp_hand_point.png
  :width: 400
  :alt: Ilustración de los puntos de referencia de MediaPipe Hands
  :align: center

.. note::
   Estas coordenadas son **coordenadas normalizadas** y se pueden convertir a posiciones de píxeles reales según la resolución de la imagen.
   Se pueden usar para calcular ángulos y distancias, permitiendo el reconocimiento de gestos.

------------------------------------------------------------
6. Solución de Problemas
------------------------------------------------------------

- Detección de manos inestable

  La detección de manos puede volverse inestable si la iluminación es demasiado tenue, el fondo está desordenado o la mano se mueve demasiado rápido.

  Intenta mejorar la iluminación, usar un fondo simple y mover las manos más lenta y constantemente.

- No se detecta ninguna mano

  Si no se detecta ninguna mano, el ángulo de la cámara puede no ser adecuado, la mano puede estar demasiado lejos de la cámara o la resolución puede ser demasiado baja.

  Ajusta la posición de la cámara, acércate y asegúrate de que la resolución sea al menos 640x480.

- Alta latencia

  Si la respuesta del video se siente lenta, la Raspberry Pi puede estar bajo carga pesada o la resolución puede ser demasiado alta.

  Reduce la resolución (por ejemplo, 320x240) y cierra procesos de fondo innecesarios.


-----------------------------
7. Resumen
-----------------------------

- MediaPipe Hands permite la **detección de manos en tiempo real** estable en Raspberry Pi.
- Proporciona 21 puntos de referencia por mano, adecuados para:

  - Reconocimiento de gestos
  - Control virtual
  - Control de interfaz de usuario interactiva

- Posteriormente, implementaremos el **reconocimiento de gestos personalizado** basado en estos puntos de referencia.
