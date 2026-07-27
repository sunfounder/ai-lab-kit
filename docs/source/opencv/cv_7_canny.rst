.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

7. Detección de Bordes Canny
=========================================

En este capítulo, capturaremos video en tiempo real usando Raspberry Pi + Picamera2 y realizaremos detección de bordes con el **algoritmo Canny** de OpenCV.
La detección de bordes es una parte fundamental de la visión artificial, y el algoritmo Canny es ampliamente reconocido como uno de los métodos más estables y robustos frente al ruido.

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_7.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. ¿Qué Hace el Algoritmo Canny?
--------------------------------------------------

En las imágenes, los **bordes** generalmente corresponden a ubicaciones con cambios fuertes de intensidad (escala de grises), como:

- Contornos de objetos
- Límites entre regiones claras y oscuras
- Líneas de borde estructurales

El propósito de la detección de bordes Canny es:

- **Extraer información de bordes con precisión** mientras se reduce la interferencia innecesaria;
- Proporcionar una base fiable para la posterior **detección de contornos**, **segmentación de objetos** y **reconocimiento geométrico** (por ejemplo, círculos, rectángulos);
- En visión robótica, se usa a menudo para **detección de caminos** y **reconocimiento de obstáculos**.

.. image:: img/opencv_canny.png
   :alt: Ilustración de la detección de bordes Canny
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
      python3 cv_7_canny.py

   .. tip::

      También proporcionamos ``cv_7_canny_video.py`` para procesar archivos de video, y ``cv_7_canny_conbine.py`` para combinar la captura en tiempo real con video (vista combinada).

#. Cuando ejecutes el programa, aparecerán dos ventanas de OpenCV:

   * **Camera** – muestra la imagen de la cámara en vivo
   * **Canny Edges** – muestra los bordes detectados en tiempo real

   Puedes ajustar los umbrales de detección de bordes usando las barras deslizantes.
   Presiona **q** o cierra cualquier ventana para salir del programa.

3. Código Completo
---------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2

   # Empty callback function for trackbars (required by OpenCV API)
   def _noop(x):
      pass

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()

   # Create a preview configuration:
   # size: resolution of the camera image
   # format: XRGB8888 (4-channel image, similar to BGRA)
   picam2.configure(
      picam2.create_preview_configuration(
         main={"size": (640, 480), "format": "XRGB8888"}
      )
   )

   # Start the camera
   picam2.start()

   # -----------------------------
   # Create OpenCV windows
   # -----------------------------
   WIN_CAM = "Camera"        # window for original image
   WIN_EDGE = "Canny Edges"  # window for edge detection result

   cv2.namedWindow(WIN_CAM)
   cv2.namedWindow(WIN_EDGE)

   # -----------------------------
   # Create trackbars to tune Canny thresholds
   # -----------------------------
   # low_th: lower threshold for Canny
   # high_th: higher threshold for Canny
   cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
   cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   print("Press 'q' to exit")

   # -----------------------------
   # Main loop
   # -----------------------------
   while True:
      # Capture one frame from the camera (BGRA format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for OpenCV processing
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame to grayscale
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

      # Apply Gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Read current threshold values from trackbars
      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      # Ensure high_th is always larger than low_th
      if high_th <= low_th:
         high_th = low_th + 1
         cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

      # Perform Canny edge detection
      edges = cv2.Canny(blurred, low_th, high_th)

      # Show original camera image
      cv2.imshow(WIN_CAM, frame_bgr)

      # Show edge detection result
      cv2.imshow(WIN_EDGE, edges)

      # Process GUI events and keyboard input
      key = cv2.waitKey(1) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
         break

   # -----------------------------
   # Cleanup
   # -----------------------------
   picam2.stop()             # Stop the camera
   cv2.destroyAllWindows()   # Close all OpenCV windows

4. Explicación del Código
---------------------------------
#. Definir una función de callback para las barras deslizantes:

   .. code-block:: python

      def _noop(x):
          pass

   Las barras deslizantes de OpenCV requieren una función de callback.
   No necesitamos hacer nada dentro de ella, por lo que una función vacía es suficiente.

#. Inicializar Picamera2 y establecer el formato de vista previa:

   .. code-block:: python

      picam2 = Picamera2()
      picam2.configure(
          picam2.create_preview_configuration(
              main={"size": (640, 480), "format": "XRGB8888"}
          )
      )
      picam2.start()

   Esto inicia la cámara Raspberry Pi a 640x480.
   ``XRGB8888`` es un formato de 4 canales, por lo que los fotogramas son similares a BGRA.

#. Crear dos ventanas de OpenCV:

   .. code-block:: python

      WIN_CAM = "Camera"
      WIN_EDGE = "Canny Edges"

      cv2.namedWindow(WIN_CAM)
      cv2.namedWindow(WIN_EDGE)

   Una ventana muestra la imagen original de la cámara, y la otra muestra el resultado de bordes Canny.

#. Crear barras deslizantes para ajustar los umbrales de Canny en tiempo real:

   .. code-block:: python

      cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
      cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   - ``low_th``: umbral inferior para Canny.
   - ``high_th``: umbral superior para Canny.

   Puedes arrastrar estos controles para cambiar la sensibilidad de la detección de bordes.

#. Capturar un fotograma y convertirlo para procesamiento con OpenCV:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   La salida de la cámara es de 4 canales, por lo que la convertimos a BGR estándar de 3 canales.

#. Convertir a escala de grises y desenfocar la imagen:

   .. code-block:: python

      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

   - Canny funciona en imágenes en escala de grises.
   - El desenfoque Gaussiano reduce el ruido, lo que ayuda a evitar detectar demasiados bordes falsos.

#. Leer los valores de las barras deslizantes y mantenerlos válidos:

   .. code-block:: python

      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      if high_th <= low_th:
          high_th = low_th + 1
          cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

   Canny espera que ``high_th`` sea mayor que ``low_th``.
   Este bloque corrige automáticamente los valores si el usuario los acerca demasiado.

#. Ejecutar la detección de bordes Canny:

   .. code-block:: python

      edges = cv2.Canny(blurred, low_th, high_th)

   Canny resalta los bordes fuertes en la imagen.
   Los umbrales más bajos generalmente detectan más bordes, pero también más ruido.

#. Mostrar ambas ventanas:

   .. code-block:: python

      cv2.imshow(WIN_CAM, frame_bgr)
      cv2.imshow(WIN_EDGE, edges)

   La ventana izquierda muestra la transmisión de la cámara en vivo, y la otra muestra los bordes detectados.

#. Condiciones de salida (presionar ``q`` o cerrar la ventana):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
          break

   Esto permite a los principiantes detener el programa de dos maneras: teclado o cerrando la ventana.

#. Limpieza:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Siempre detén la cámara y cierra todas las ventanas de OpenCV para liberar recursos.

5. ¿Por Qué es Útil Canny?
--------------------------

La salida de Canny es muy adecuada para tareas de visión posteriores:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Aplicación
     - Descripción
   * - Detección de contornos
     - Usa ``cv2.findContours`` en la salida de Canny para obtener formas de objetos
   * - Segmentación de objetos
     - Usa los bordes como base para separar el objetivo del fondo
   * - Reconocimiento de formas
     - Combina con transformadas de Hough para detectar círculos, líneas, etc.
   * - Navegación robótica
     - Detecta suelo, carreteras, contornos de obstáculos para ayudar a la planificación
   * - OCR / Localización de objetivos
     - Las regiones de texto, códigos QR y marcadores a menudo tienen características de borde claras

Canny no es solo "de apariencia interesante", es el **punto de entrada** a un proceso de CV más amplio.


6. Consejos para la Selección de Umbrales
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30 30 70

   * - Escenario
     - low_th
     - high_th
     - Notas
   * - Iluminación interior estable
     - 50
     - 150
     - Caso general, resultados estables
   * - Iluminación fuerte y alto contraste
     - 100
     - 200
     - Aumentar umbrales para reducir bordes falsos
   * - Poca luz, con ruido
     - 30
     - 100
     - Umbrales más bajos para mantener más detalles
   * - Bordes muy borrosos
     - 20
     - 80
     - Umbrales más bajos para hacer los bordes más sensibles

Usa las barras deslizantes para ajustar rápidamente un rango apropiado, luego codifícalo en tu programa.


7. Ejercicios Extendidos
---------------------

- Usa ``cv2.findContours`` en la salida de Canny para dibujar los límites de los objetos.
- Cambia el tamaño del kernel Gaussiano y observa cómo cambia la precisión de los bordes.
- Prueba diferentes umbrales en condiciones de poca/mucha luz para entender los efectos del doble umbral.
- Usa el mapa de bordes para la detección de formas con ``cv2.HoughLines`` (líneas) o ``cv2.HoughCircles`` (círculos).
