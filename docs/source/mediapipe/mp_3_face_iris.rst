.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. Contornos Faciales y Detección del Iris
=================================================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En las secciones anteriores, implementamos la detección básica de malla facial
y el reconocimiento simple de emociones.

Esta sección se centra en los métodos de conexión de características detalladas
proporcionados por MediaPipe FaceMesh:

- ``FACEMESH_CONTOURS`` — Dibuja las líneas de contorno facial
  (bordes del rostro y límites exteriores de características)

- ``FACEMESH_IRISES`` — Dibuja las regiones del iris de ambos ojos

Al dibujar solo contornos y regiones del iris, la visualización se vuelve
más limpia y ligera. Esto es útil para:

- Extracción de características faciales
- Seguimiento ocular
- Seguimiento pupilar
- Interacción por mirada

.. image:: img/mp_face_iris.png
   :align: center

------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El programa realiza los siguientes pasos:

1. Inicializar el modelo MediaPipe FaceMesh.
2. Capturar fotogramas de video de la cámara Raspberry Pi.
3. Convertir la imagen al formato RGB (requerido por MediaPipe).
4. Dibujar las líneas de contorno facial usando ``FACEMESH_CONTOURS``.
5. Dibujar los puntos de referencia del iris usando ``FACEMESH_IRISES``.
6. Mostrar solo las áreas clave para una visualización más clara.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

#. Después de ejecutar el programa, se abre una ventana de video titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_3.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparece un rostro frente a la cámara:

   - MediaPipe detecta puntos de referencia faciales en tiempo real.
   - Solo se dibujan las líneas de contorno facial (contorno del rostro, cejas, labios, etc.).
   - Las regiones del iris de ambos ojos se resaltan con conexiones de puntos circulares.

   A diferencia de la malla facial completa, la pantalla muestra solo los contornos clave y las características del iris, haciendo la visualización más limpia y menos abarrotada.

   A medida que el usuario mueve la cabeza o los ojos:

   - Las líneas de contorno siguen el rostro suavemente.
   - Los puntos de referencia del iris siguen el movimiento ocular en tiempo real.

   Si no se detecta ningún rostro, la ventana continúa mostrando la transmisión normal de la cámara sin anotaciones.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.

-----------------------------
4. Código Completo
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

Después de ejecutar el programa, solo se mostrarán en la pantalla los contornos faciales y las regiones del iris de ambos ojos.

-----------------------------
5. Explicación de Pasos Clave
-----------------------------

El código en esta sección es casi el mismo que el de
:ref:`mp_face`.

La diferencia principal es el método de dibujo utilizado
dentro del bucle principal. La función ``draw_landmarks()``
se llama dos veces:

- Una vez con ``FACEMESH_CONTOURS``
- Una vez con ``FACEMESH_IRISES``

Puedes comentar cualquiera de los bloques de dibujo
para observar la diferencia en el efecto visual.

------------------------------------------------------------

``FACEMESH_CONTOURS``

- Un conjunto de conexiones proporcionado por MediaPipe.
- Dibuja principalmente:

  - Contorno facial externo
  - Bordes de los ojos
  - Contorno de la nariz
  - Contornos de los labios

Este método produce una visualización simplificada,
facilitando la observación de los cambios en el contorno facial.

------------------------------------------------------------

``FACEMESH_IRISES``

- Dibuja las regiones del iris de ambos ojos.
- Incluye puntos clave del iris y líneas de conexión circular.
- Útil para:

  - Seguimiento ocular
  - Seguimiento pupilar
  - Detección de mirada

------------------------------------------------------------

``landmark_drawing_spec=None``

- Desactiva el dibujo de puntos de referencia individuales.
- Solo se muestran las líneas de conexión,
  resultando en un efecto visual más limpio.

Si deseas mostrar tanto puntos como líneas,
define un ``DrawingSpec`` personalizado.

------------------------------------------------------------

``drawing_styles.get_default_face_mesh_contours_style()``

- Devuelve el estilo de dibujo de contorno predeterminado.

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- Devuelve el estilo de línea de conexión del iris predeterminado.


------------------------------------------------------------
6. Solución de Problemas
------------------------------------------------------------

- Iris no detectado

  Si el iris no se detecta, la iluminación puede ser insuficiente,
  el rostro puede estar demasiado lejos de la cámara,
  o ``refine_landmarks`` puede no estar habilitado.

  Mejora la iluminación, acércate a la cámara,
  y asegúrate de que ``refine_landmarks=True`` esté configurado
  al inicializar FaceMesh.

- Líneas de contorno temblorosas

  Si las líneas de contorno parecen inestables,
  la confianza de detección puede ser demasiado baja,
  o la iluminación y el movimiento de la cabeza pueden estar afectando el seguimiento.

  Intenta aumentar ``min_detection_confidence``,
  mejorar la iluminación y mantener los movimientos de cabeza más lentos y suaves.

- Alta latencia

  Si la respuesta del video se siente lenta,
  la resolución puede ser demasiado alta
  o ``refine_landmarks`` puede estar consumiendo recursos adicionales.

  Reduce la resolución (por ejemplo, 320x240),
  o desactiva ``refine_landmarks`` si no se necesita la detección del iris.

-----------------------------
7. Resumen
-----------------------------

- ``FACEMESH_CONTOURS`` y ``FACEMESH_IRISES`` son dos métodos de conexión importantes proporcionados por MediaPipe.
- En comparación con el dibujo de malla completa, son más ligeros e intuitivos, adecuados para escenarios de interacción práctica.
- El siguiente capítulo presentará cómo usar estas características para el seguimiento de la mirada y la detección de parpadeos.
