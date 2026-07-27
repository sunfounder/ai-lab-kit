.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. Detección de Color
===========================================

La detección de color es una de las funciones más fundamentales y prácticas en la visión artificial.
En este capítulo, utilizaremos código y explicaciones paso a paso para **detectar objetos rojos usando el espacio de color HSV** y **dibujar rectángulos delimitadores** alrededor de ellos.

Esto sienta las bases para técnicas de seguimiento de objetos más avanzadas (por ejemplo, CAMShift).

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Objetivo y Enfoque
--------------------------------------------

- Usar **Picamera2** para capturar fotogramas de cámara en tiempo real
- Convertir la imagen de BGR al espacio de color HSV
- Usar ``cv2.inRange`` para extraer las regiones rojas
- Usar filtrado morfológico para eliminar el ruido
- Usar ``cv2.findContours`` para encontrar contornos de objetos rojos
- Dibujar rectángulos delimitadores alrededor de las regiones rojas detectadas

.. image:: img/color_detection.png
   :alt: Ilustración de vista previa de detección de color
   :align: center

2. Ejecutar el Código
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

      cd ~/ai-lab-kit/opencv_python
      python3 cv_4_color.py

#. Cuando ejecutes el programa, aparecerán dos ventanas de OpenCV en la pantalla:

   * **Red Detection** – muestra la imagen de la cámara en vivo con rectángulos verdes alrededor de los objetos rojos detectados
   * **Red Mask** – muestra la imagen de máscara binaria utilizada para la detección de color rojo

   El programa captura fotogramas continuamente de la cámara Raspberry Pi y detecta regiones rojas en tiempo real.
   Si se detecta un objeto rojo, se mostrarán un rectángulo verde y el valor del área en la imagen en color.

   Puedes salir del programa de dos maneras:

   * Presionar la tecla **q** en el teclado
   * Cerrar cualquiera de las ventanas de OpenCV haciendo clic en el botón de cerrar (X)

   Después de salir, la cámara deja de transmitir y todas las ventanas de OpenCV se cierran.

3. Código Completo
------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. Explicación del Código
--------------------------------

#. Inicializar Picamera2 y comenzar la transmisión:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   Esto configura la cámara a 640x480 e inicia la transmisión de vista previa.
   ``XRGB8888`` es un formato de 4 canales, por lo que los fotogramas capturados son similares a BGRA.

#. Convertir el fotograma capturado a un formato que OpenCV usa comúnmente:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2 devuelve aquí una imagen de 4 canales, por lo que la convertimos a BGR estándar de 3 canales para su procesamiento.

#. Usar el espacio de color HSV para una detección de color robusta:

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV separa el color (Tono) del brillo, lo que hace que la detección de color sea más estable bajo diferentes condiciones de iluminación.

#. Definir dos rangos HSV para el rojo:

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   El rojo "se envuelve" alrededor de la escala de Tono en HSV de OpenCV (cerca de 0 y cerca de 180), por lo que se combinan dos rangos para cubrir todos los rojos.

#. Limpiar la máscara con morfología (reducir ruido y rellenar agujeros):

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** elimina pequeños puntos ruidosos.
   - **CLOSE** rellena pequeños agujeros dentro de las regiones rojas detectadas.

#. Encontrar regiones rojas y filtrar manchas pequeñas:

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   Los contornos se detectan a partir de la máscara binaria.
   ``MIN_AREA`` ignora las regiones rojas pequeñas para reducir las falsas detecciones.

#. Dibujar rectángulos delimitadores y etiquetas en la imagen de resultado:

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   Esto muestra dónde encontró OpenCV los objetos rojos e imprime el área de la mancha detectada como referencia.

#. Mostrar tanto el resultado como la máscara:

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   La **ventana de resultado** muestra la vista de la cámara con los rectángulos, y la **ventana de máscara** muestra la imagen binaria solo roja.

#. Condiciones de salida (teclado + cierre de ventana):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   Presiona ``q`` para salir, o cierra cualquiera de las ventanas para salir de forma segura.

#. Limpieza:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Siempre detén la cámara y cierra las ventanas de OpenCV para liberar recursos.


5. Consejos para el Ajuste de Parámetros
-----------------------------

- ``LOWER_RED1 / UPPER_RED1``: ajusta este rango para detectar otros colores.
  Por ejemplo, verde ≈ ``[35, 50, 50]`` a ``[85, 255, 255]``.

- ``KERNEL``: kernels más grandes proporcionan un filtrado más fuerte pero pueden eliminar objetos pequeños.

- ``MIN_AREA``: aumentar este valor filtra los contornos ruidosos pequeños; disminuirlo hace que la detección sea más sensible.

.. note::
   Puedes comenzar mostrando solo la ``mask`` y ajustando los umbrales hasta que la región objetivo se vea clara, luego continuar con el resto del proceso.



6. Extensiones y Práctica
--------------------------

- Modifica el umbral HSV para detectar otros colores (por ejemplo, azul o verde).
- Experimenta con diferentes parámetros morfológicos en fondos más complejos.
