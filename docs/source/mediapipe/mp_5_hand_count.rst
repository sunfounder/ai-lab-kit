.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. Conteo de Gestos de Mano
==============================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En la sección anterior, implementamos la detección de manos
en tiempo real y la visualización de puntos de referencia.

Esta sección extiende esa funcionalidad usando
las posiciones de los puntos de referencia de los dedos para contar el
número de dedos levantados (0–5).

Analizando las posiciones relativas de las puntas de los dedos
y sus articulaciones correspondientes, podemos determinar
si cada dedo está extendido.

.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El programa sigue estos pasos:

1. Inicializar el modelo MediaPipe Hands.
2. Capturar fotogramas de video de la cámara Raspberry Pi.
3. Detectar 21 puntos de referencia de manos en tiempo real.
4. Comparar las coordenadas de las puntas de los dedos con sus articulaciones proximales.
5. Determinar si cada dedo está extendido.
6. Contar el número de dedos levantados.
7. Mostrar el resultado en el fotograma de video.

Este método es:

- Ligero y eficiente
- Adecuado para Raspberry Pi
- Una base para el control por gestos y sistemas interactivos

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparece una mano frente a la cámara:

   - MediaPipe detecta la mano en tiempo real.
   - Se dibujan 21 puntos de referencia y líneas de conexión en la mano.
   - El programa analiza las posiciones de las puntas de los dedos y las articulaciones.
   - Se calcula el número de dedos levantados (0–5).

   El conteo de dedos detectado se muestra en la esquina superior izquierda
   de la pantalla como:

      Fingers: X

   A medida que extiendes o doblas los dedos, el número se actualiza
   instantáneamente en tiempo real.

   Si no se detecta ninguna mano, solo se muestra
   la transmisión normal de la cámara sin conteo de dedos.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.



-----------------------------
4. Código Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

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

               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

En cada iteración del bucle, determina si cada uno de los 5 dedos está extendido y cuenta el número de dedos extendidos. Por ejemplo:

- ✊ Todos los dedos cerrados → Conteo 0
- ☝️ Dedo índice extendido → Conteo 1
- ✌️ Índice + Medio → Conteo 2
- 🖐️ Los cinco dedos abiertos → Conteo 5

--------------------------------------------------------------
5. Lógica de Detección y Extensiones
--------------------------------------------------------------

MediaPipe Hands devuelve 21 puntos de referencia.
Usamos las posiciones de las puntas de los dedos y las articulaciones para determinar si
cada dedo está extendido.

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → Índices de las puntas de los dedos
  (Pulgar=4, Índice=8, Medio=12, Anular=16, Meñique=20)

- ``finger_dips`` → Articulaciones proximales correspondientes
  (Pulgar=2, Índice=6, Medio=10, Anular=14, Meñique=18)

------------------------------------------------------------

Lógica de conteo de dedos:

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

Explicación de la lógica:

- **Pulgar** → Comparar ``tip.x`` y ``dip.x`` (para la mano derecha).
- **Otros dedos** → Comparar ``tip.y`` y ``dip.y``.
- Si la punta del dedo está arriba (o hacia afuera) de la articulación,
  el dedo se considera extendido.
- Cada condición satisfecha aumenta el conteo en ``+1``.

------------------------------------------------------------

Consejos de extensión:

- Para admitir ambas manos (izquierda y derecha),
  usa ``hands_detected.multi_handedness`` para determinar el tipo de mano,
  e invierte la comparación del eje x del pulgar en consecuencia.

- Esta lógica se puede extender para implementar:

  - Reconocimiento de gesto OK
  - Detección de pulgar arriba
  - Interacción de piedra–papel–tijeras
  - Controles personalizados basados en gestos

------------------------------------------------------------
6. Solución de Problemas
------------------------------------------------------------

- Detección del pulgar imprecisa

  La detección del pulgar puede ser imprecisa porque la lógica difiere para manos izquierda y derecha. La comparación horizontal utilizada para el pulgar depende de la orientación de la mano.

  Usa ``multi_handedness`` para determinar si la mano detectada es izquierda o derecha y ajusta la lógica de detección del pulgar en consecuencia.

- Detección inestable

  Si el conteo de dedos parece inestable, la iluminación puede ser insuficiente o el fondo puede estar desordenado.

  Mejora las condiciones de iluminación y usa un fondo simple para aumentar la estabilidad de la detección.

- Alta latencia

  Si la respuesta se siente lenta, la resolución puede ser demasiado alta o la CPU puede estar sobrecargada.

  Reduce la resolución (por ejemplo, 320x240) y cierra procesos de fondo innecesarios. También puedes simplificar la lógica de conteo de dedos si es necesario.


-----------------------------
7. Resumen
-----------------------------

- Usando MediaPipe Hands, podemos implementar rápidamente el **reconocimiento de gestos en tiempo real**.
- Esta sección implementó el **conteo de gestos numéricos** basado en las posiciones de las puntas de los dedos, sentando las bases para el reconocimiento de gestos personalizado.
- Adaptándose para manos izquierda/derecha y expandiendo las reglas de juicio, se pueden lograr escenarios interactivos más complejos.
