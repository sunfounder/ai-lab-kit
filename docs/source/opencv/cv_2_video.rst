.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. Reproducir Video
========================================

En este capítulo, aprenderás cómo leer y reproducir flujos de video en OpenCV, y cómo controlar la velocidad de reproducción calculando el tiempo de procesamiento de fotogramas.



1. Resumen del Proyecto
-----------------------

En esta sección, lograremos los siguientes objetivos:

- Usar ``cv2.VideoCapture`` para abrir un archivo de video
- Leer y mostrar video fotograma por fotograma
- Reiniciar automáticamente el video después de que termine
- Controlar la tasa de fotogramas de reproducción usando cálculos de tiempo de procesamiento
- Presionar la tecla ``q`` para salir de la reproducción

.. image:: img/opencv_video.png
   :alt: Ilustración de la interfaz de reproducción de video
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
      python3 cv_2_video.py

#. Después de ejecutar el script, OpenCV abre una ventana titulada **Video** y muestra los fotogramas del video en tiempo real.

   Si el video llega al final, se reiniciará automáticamente desde el principio.

   Para detener el programa, puedes:

   * Presionar **q** en el teclado para salir de la reproducción
   * Cerrar la ventana haciendo clic en el botón de cerrar

   Una vez que la ventana se cierra, todos los recursos de OpenCV se liberan y el programa finaliza.


3. Código Completo
------------------------------

.. code-block:: python

  import cv2

  # Open the video file
  cap = cv2.VideoCapture("sample2.mp4")

  while True:
      # Read one frame from the video
      ret, frame = cap.read()

      # If the video ends, restart from the beginning
      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

      # Resize the frame for better display performance
      frame = cv2.resize(frame, (640, 480))

      # Display the frame in a window named "Video"
      cv2.imshow("Video", frame)

      # Wait 30 ms between frames (~30 FPS)
      # This also processes GUI events (keyboard and window events)
      key = cv2.waitKey(30) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
          break

      # Exit if the user closes the window (click the close button)
      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

  # Release the video capture object
  cap.release()

  # Close all OpenCV windows
  cv2.destroyAllWindows()


4. Explicación del Código
-----------------------

#. Abrir el archivo de video:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Esto abre el archivo de video y crea un objeto ``VideoCapture`` para leer fotogramas.

#. Leer un fotograma del video:

   .. code-block:: python

      ret, frame = cap.read()

   - ``ret`` es ``True`` si el fotograma se lee correctamente.
   - ``ret`` se vuelve ``False`` cuando el video termina o la lectura falla.
   - ``frame`` son los datos de la imagen (un array NumPy).

#. Repetir el video cuando termina:

   .. code-block:: python

      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

   Cuando el video termina, esto restablece la posición de reproducción al primer fotograma para que el video pueda reiniciarse.

#. Redimensionar el fotograma:

   .. code-block:: python

      frame = cv2.resize(frame, (640, 480))

   Esto redimensiona cada fotograma a 640x480 para una visualización más fluida y menor uso de CPU en Raspberry Pi.

#. Mostrar el fotograma:

   .. code-block:: python

      cv2.imshow("Video", frame)

   Esto muestra el fotograma actual en una ventana llamada ``Video``.

#. Controlar la velocidad de reproducción y leer la entrada del teclado:

   .. code-block:: python

      key = cv2.waitKey(30) & 0xFF

   Esto espera aproximadamente 30 ms entre fotogramas (alrededor de 30 FPS) y procesa eventos GUI.

#. Salir presionando ``q``:

   .. code-block:: python

      if key == ord("q"):
          break

   Presiona ``q`` para detener el programa.

#. Salir cuando se cierra la ventana:

   .. code-block:: python

      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

   Esto verifica si la ventana sigue siendo visible.
   Si el usuario cierra la ventana, el programa sale de forma segura.

#. Liberar el objeto de captura de video:

   .. code-block:: python

      cap.release()

   Esto libera el recurso del archivo de video.

#. Cerrar todas las ventanas de OpenCV:

   .. code-block:: python

      cv2.destroyAllWindows()

   Esto cierra todas las ventanas de OpenCV y libera los recursos GUI.


5. Práctica Adicional
----------------------

- Intenta cambiar el tamaño de la ventana para ver cómo afecta la claridad de la imagen.
- Reemplaza el archivo de video con diferentes para probar la compatibilidad.
- Imprime el tiempo de procesamiento por fotograma para entender mejor la relación entre FPS y el retardo de reproducción.
