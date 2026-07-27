.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. Contador de Sentadillas
==========================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En el capítulo anterior, implementamos la estimación básica de la pose humana.
Este capítulo se basa en esa base para implementar un simple
**Contador de Sentadillas** usando MediaPipe Pose.

Este es un ejemplo práctico que combina:

- Detección de pose
- Reconocimiento de acciones
- Conteo en tiempo real

Se puede usar en sistemas inteligentes de fitness,
asistentes de entrenamiento en casa o aplicaciones de análisis de movimiento.

.. image:: img/mp_pose_s2.png
   :alt: Ejemplo de conteo de sentadillas
   :align: center


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El contador de sentadillas se implementa usando la siguiente lógica:

1. Usar MediaPipe Pose para detectar 33 puntos clave corporales.
2. Seleccionar articulaciones clave (Hombro, Cadera, Tobillo).
3. Usar las coordenadas y normalizadas para estimar la altura de la cadera.
4. Definir umbrales superior e inferior (por ejemplo, 0.55 y 0.45).
5. Usar una máquina de estados simple para detectar la transición:
   "de pie → en cuclillas → de pie".
6. Aumentar el contador cuando se completa un ciclo completo de sentadilla.
7. Mostrar el conteo de sentadillas y el valor actual de cadera en la pantalla.

.. note::

   - Este ejemplo no utiliza el cálculo del ángulo de la articulación.
   - Se basa en coordenadas normalizadas para reducir el cálculo.
   - El método es ligero y adecuado para Raspberry Pi.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_8.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando una persona está de pie frente a la cámara:

   - MediaPipe Pose detecta 33 puntos de referencia corporales en tiempo real.
   - Se dibuja un esqueleto corporal completo en la pantalla.
   - El sistema calcula continuamente la posición relativa de la cadera (HipRel).

   A medida que realizas sentadillas:

   - Cuando te agachas y tu cadera supera el umbral inferior (DOWN_TH),
     el sistema marca que estás en la posición "abajo".
   - Cuando te levantas y la cadera supera el umbral superior (UP_TH),
     el contador de sentadillas aumenta en 1.

   La pantalla muestra:

   - ``Squats: N`` — el número total de sentadillas completadas.
   - ``HipRel: value`` — la posición normalizada actual de la cadera utilizada para la detección.

   El contador solo aumenta después de un ciclo de movimiento completo
   (de pie → sentadilla → de pie), evitando el conteo duplicado.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.


-----------------------------
4. Código Completo
-----------------------------

Aquí está la implementación completa del contador de sentadillas:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutar el script, el sistema:

- Detectará el esqueleto humano;
- Calculará la posición relativa de la cadera;
- Contará +1 cuando se complete un ciclo completo desde "agacharse" hasta "levantarse";
- Mostrará **Squats: N** y el valor actual de HipRel en la pantalla en tiempo real.

-----------------------------------------------
5. Coordenadas y Diseño de Estados
-----------------------------------------------

Usamos los siguientes 6 puntos clave (3 a cada lado):

.. list-table::
   :header-rows: 1

   * - Punto Clave
     - Índice
     - Descripción
   * - Hombro
     - 11 (Izquierdo) / 12 (Derecho)
     - Referencia superior
   * - Cadera
     - 23 (Izquierda) / 24 (Derecha)
     - Centro para calcular la posición de sentadilla
   * - Tobillo
     - 27 (Izquierdo) / 28 (Derecho)
     - Referencia inferior

.. image:: img/mp_pose_s1.png
   :alt: Puntos clave de MediaPipe Pose
   :align: center

**Valor de cadera relativa (Hip Relative)** fórmula de cálculo:

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- Un hip_rel más grande significa más cerca del suelo (es decir, agachándose).
- Un hip_rel más pequeño significa estar de pie erguido.

Definimos dos umbrales:

- **DOWN_TH = 0.55**: Se considera que se está entrando en la posición baja de la sentadilla
- **UP_TH = 0.45**: Se considera que se ha vuelto a la posición de pie

Usa una máquina de estados simple para un conteo fiable:

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
6. Ajuste de Parámetros y Optimización
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Parámetro
     - Descripción
     - Sugerencia de ajuste
   * - DOWN_TH
     - Umbral de acción de sentadilla
     - Valor más alto requiere una sentadilla más profunda para contar
   * - UP_TH
     - Umbral de acción de levantarse
     - Valor más bajo requiere estar más erguido
   * - model_complexity
     - Complejidad del modelo Pose
     - Usa 1 para mayor velocidad
   * - Resolución
     - Afecta la tasa de fotogramas y la precisión
     - Recomendado 640×480

.. tip::
   Para personas de diferentes alturas, se pueden usar umbrales adaptativos o calibración personalizada para un conteo más preciso.

---------------------------------------------------------
7. Solución de Problemas
---------------------------------------------------------

- Conteo inexacto

  Si el conteo de sentadillas no es preciso, los valores de umbral pueden no coincidir con la posición de tu cuerpo o el ángulo de la cámara.

  Intenta imprimir ``hip_rel`` en tiempo real y ajusta ``DOWN_TH`` y ``UP_TH`` en consecuencia.
  También asegúrate de que tu forma de sentadilla sea consistente y claramente visible.

- Persona no detectada

  Si el cuerpo no se detecta, mejora las condiciones de iluminación y evita fondos complejos.

  Asegúrate de estar completamente dentro del fotograma y mirando directamente a la cámara.

- Alta latencia

  Si la respuesta del video es lenta, reduce ``model_complexity`` a 1 y baja la resolución de la cámara (por ejemplo, 640×480 o 320×240).

  Cierra programas de fondo innecesarios para mejorar el rendimiento.

-----------------------------
8. Resumen
-----------------------------

- Implementado un **contador de sentadillas en tiempo real** usando puntos clave de Pose + máquina de estados;
- Sin necesidad de cálculos de ángulos complejos, alta eficiencia operativa;
- Adecuado para Raspberry Pi u otras aplicaciones de dispositivos periféricos;
- Posibles extensiones futuras:

  - Detección de flexiones/abdominales
  - Registro y visualización de datos
  - Guía de ritmo automática y retroalimentación de entrenamiento
