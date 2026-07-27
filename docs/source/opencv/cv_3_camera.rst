.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Captura de Cámara en Tiempo Real
================================================================

En los capítulos anteriores, aprendimos cómo leer y reproducir archivos de video locales.
En este capítulo, iremos un paso más allá usando la **cámara Raspberry Pi** para la captura de video en tiempo real y aplicando la **conversión de espacio de color** con OpenCV.


1. Objetivos del Proyecto
--------------------------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

- Usar **Picamera2** para capturar fotogramas de cámara en tiempo real
- Convertir la salida de la cámara del formato BGRA a BGR
- Usar OpenCV para la vista previa en tiempo real
- Comprender las características y casos de uso de diferentes espacios de color

.. image:: img/opencv_camera.png
   :alt: Ilustración de vista previa de cámara en tiempo real
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
      python3 cv_3_camera.py

#. Cuando ejecutes el programa, aparecerán dos ventanas de OpenCV:

   * **BGR Frame** – muestra la imagen de la cámara en color en vivo
   * **GRAY Frame** – muestra la versión en escala de grises de la misma imagen

   Puedes salir del programa de dos maneras:

   * Presionar la tecla **q** en el teclado
   * Cerrar cualquiera de las ventanas haciendo clic en el botón de cerrar (X)

   Después de salir, la cámara deja de transmitir y todas las ventanas de OpenCV se cierran.

3. Código de Ejemplo
-------------------------------

A continuación se muestra el ejemplo completo de Python para este capítulo (``cv_3_camera.py``):

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. Explicación del Código
-------------------

#. Importar las bibliotecas necesarias:

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2 captura fotogramas de la cámara Raspberry Pi, y OpenCV se usa para la conversión y visualización de imágenes.

#. Crear un objeto Picamera2 y configurar la cámara:

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   Esto inicia la cámara a 640x480.
   ``XRGB8888`` es un formato de 4 canales, por lo que cada fotograma capturado es similar a BGRA.

#. Capturar un fotograma como array NumPy:

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   Cada bucle lee un fotograma de la cámara.

#. Convertir el fotograma para su visualización:

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr`` se usa para la visualización de color normal.
   - ``frame_gray`` es una versión en escala de grises del mismo fotograma.

#. Mostrar los fotogramas en dos ventanas:

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   Esto abre dos ventanas de OpenCV: una muestra el fotograma en color y la otra muestra el fotograma en escala de grises.

#. Condiciones de salida (presionar ``q`` o cerrar una ventana):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - Presiona ``q`` para salir.
   - Cerrar cualquiera de las ventanas también detendrá el programa de forma segura.

#. Limitar FPS para reducir el uso de CPU:

   .. code-block:: python

      time.sleep(1 / 30)

   Esto añade un pequeño retardo para que el bucle se ejecute a aproximadamente 30 FPS, lo que puede reducir la carga de CPU en Raspberry Pi.

#. Detener la cámara y cerrar las ventanas de OpenCV:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Esto libera la cámara y cierra todas las ventanas de OpenCV antes de que el programa finalice.

5. La Importancia de la Conversión del Espacio de Color
-------------------------------------------------------------------

El formato de imagen sin procesar que sale de la cámara puede no coincidir siempre con el formato que OpenCV requiere para el procesamiento.
En este ejemplo, Picamera2 genera imágenes en formato **XRGB8888 (BGRA)**, mientras que OpenCV utiliza principalmente el formato **BGR**.

Por lo tanto, necesitamos convertir la imagen de la siguiente manera:

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

Esto asegura que la imagen esté organizada en el orden de canales BGR estándar utilizado por OpenCV, lo que permite que se muestre y procese correctamente.

Luego podemos convertir la imagen BGR a escala de grises para su posterior procesamiento:

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

Esto nos permite transformar las imágenes capturadas por la cámara a un formato adecuado para los flujos de trabajo de procesamiento de imágenes de OpenCV.

**Espacios de color comunes y casos de uso**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Espacio de Color
     - Características
     - Casos de uso típicos
   * - **BGR**
     - Formato predeterminado de OpenCV
     - Visualización de imágenes, procesamiento básico, detección de bordes
   * - **RGB**
     - Intuitivo para la percepción humana
     - Visualización, entrada de imágenes para aprendizaje profundo
   * - **GRAY**
     - Imagen en escala de grises de un solo canal
     - Detección de objetos, detección de bordes, optimización del rendimiento
   * - **HSV**
     - Separa el color del brillo
     - Detección de color, seguimiento de objetos, segmentación
   * - **YCrCb**
     - Separa la luminancia de la crominancia
     - Detección de rostros, compresión de video, robustez ante iluminación

Por ejemplo, **HSV** suele ser mejor para la **detección de color y el seguimiento de objetos**,
mientras que **YCrCb** es más robusto en el **reconocimiento facial** o **escenas con iluminación variable**.

6. Extensiones y Práctica
-------------------------------------------

- Intenta convertir de BGR a GRAY o HSV y observa los resultados.

  Por ejemplo, usa:

  - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
  - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
  - y otros

- Prueba diferentes resoluciones (por ejemplo, 1280x720) y observa el efecto en la latencia y la tasa de fotogramas.
- Combina este código con el ejemplo de reproducción de video anterior para implementar el cambio entre una transmisión de cámara y una fuente de video.
