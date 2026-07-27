.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

8. Detección de Rostros y Ojos
=========================================

En este capítulo, usaremos Picamera2 de Raspberry Pi para capturar video y aplicaremos los clasificadores de características Haar de OpenCV para la **detección de rostros y ojos en tiempo real**.
Este enfoque es ligero y muy práctico, ideal para principiantes que se inician en Raspberry Pi.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_8.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Características Haar y Principios de Detección
-----------------------------------------

1. Esencia de las Características Haar

Las características Haar son un método clásico para la detección de objetos. Codifican **patrones de diferencias de brillo** dentro de regiones de la imagen para determinar si una región probablemente contiene un rostro, ojos, etc.

Ejemplos típicos de características Haar:

- Las regiones de los ojos suelen ser más oscuras que la frente superior
- El brillo es simétrico en ambos lados del puente nasal
- El área debajo de la boca a menudo muestra un patrón de borde claro

.. image:: img/opencv_haar_f.png
   :alt: Ilustración de las características Haar
   :align: center

OpenCV requiere clasificadores Haar preentrenados (archivos ``.xml``). Ya están incluidos en el directorio de ejemplo, solo hay que cargarlos y usarlos.

2. Proceso de Detección

   1. Cargar el modelo Haar entrenado usando ``CascadeClassifier``
   2. Convertir el video en tiempo real a escala de grises (para mejorar la eficiencia)
   3. Usar ``detectMultiScale`` para detectar regiones de rostros/ojos
   4. Dibujar rectángulos alrededor de los objetivos detectados

.. image:: img/opencv_haar_show.png
   :alt: Ilustración del proceso de detección
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
      python3 cv_8_haarcascade.py

   .. tip::

      También proporcionamos ``cv_8_haarcascade_video.py`` para detectar rostros y ojos desde un archivo de video.

#. Cuando ejecutes el programa, aparecerá una ventana llamada **Raspberry Pi Camera - Face Detection** y mostrará la imagen de la cámara en vivo de la Raspberry Pi.

   Los rostros detectados en el flujo de video se resaltan con **rectángulos amarillos**, y cada rostro detectado se etiqueta (Face 1, Face 2, ...).
   Dentro de cada región facial detectada, el programa también detecta ojos y los marca con **rectángulos naranjas**.

   La detección funciona en tiempo real, y los rectángulos se moverán a medida que la persona se mueva frente a la cámara.

   Para detener el programa:

   * Presiona la tecla **q** en el teclado
   * O cierra la ventana de visualización usando el botón de cerrar (X)

   Después de salir, la cámara se detendrá y todas las ventanas de OpenCV se cerrarán.


3. Código Completo
-------------------


.. code-block:: python

   # Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
   import cv2
   from picamera2 import Picamera2
   from pathlib import Path

   # -----------------------------
   # Load Haar cascade classifiers
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent

   face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
   eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   # Check if cascade files are loaded correctly
   if face_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
   if eye_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   # -----------------------------
   # Initialize Picamera2
   # -----------------------------
   picam2 = Picamera2()

   # Video configuration (resolution can be adjusted)
   config = picam2.create_video_configuration(main={"size": (640, 480)})
   picam2.configure(config)
   picam2.start()

   WIN = "Raspberry Pi Camera - Face Detection"
   print("Camera started. Press 'q' to quit.")

   try:
      while True:
         # Capture a frame (Picamera2 typically provides RGB)
         frame_rgb = picam2.capture_array()

         # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
         gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

         # Improve contrast to make detection more stable under different lighting
         gray = cv2.equalizeHist(gray)

         # Detect faces
         faces = face_cascade.detectMultiScale(
               gray,
               scaleFactor=1.2,
               minNeighbors=5,
               minSize=(60, 60)
         )

         # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
         frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

         # Draw face and eye results
         for i, (x, y, w, h) in enumerate(faces, start=1):
               # Draw face rectangle + label
               cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
               cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

               # ROI for eye detection (search eyes only inside the detected face area)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = frame_bgr[y:y + h, x:x + w]

               eyes = eye_cascade.detectMultiScale(
                  roi_gray,
                  scaleFactor=1.2,
                  minNeighbors=8,
                  minSize=(20, 20)
               )

               # Draw up to 2 eyes (typical for a face)
               for (ex, ey, ew, eh) in eyes[:2]:
                  cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

         # Show the frame
         cv2.imshow(WIN, frame_bgr)

         # Handle keyboard input
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
               break

         # Exit if the user closes the window (click X)
         if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
               break

   finally:
      picam2.stop()
      cv2.destroyAllWindows()
      print("Camera stopped.")

4. Explicación del Código
----------------------

#. Importar las bibliotecas necesarias:

   .. code-block:: python

      import cv2
      from picamera2 import Picamera2
      from pathlib import Path

   OpenCV se usa para la detección y el dibujo, Picamera2 se usa para capturar fotogramas de la cámara Raspberry Pi.

#. Obtener el directorio del script actual:

   .. code-block:: python

      BASE_DIR = Path(__file__).resolve().parent

   Esto te permite cargar los archivos XML de los clasificadores desde la misma carpeta que el script Python.

#. Cargar los clasificadores Haar (rostro y ojos):

   .. code-block:: python

      face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
      eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   Los clasificadores Haar son modelos preentrenados que pueden detectar rostros y ojos.

#. Verificar que los archivos de los clasificadores se carguen correctamente:

   .. code-block:: python

      if face_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
      if eye_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   Si la ruta del archivo es incorrecta o el archivo falta, ``CascadeClassifier`` estará vacío.
   Estas comprobaciones te ayudan a encontrar el problema temprano.

#. Inicializar la cámara y establecer la resolución:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_video_configuration(main={"size": (640, 480)})
      picam2.configure(config)
      picam2.start()

   Esto inicia la cámara en modo video a 640x480.

#. Capturar fotogramas continuamente:

   .. code-block:: python

      frame_rgb = picam2.capture_array()

   Cada bucle captura un fotograma. Picamera2 normalmente devuelve fotogramas en formato RGB.

#. Convertir a escala de grises (más rápido para la detección):

   .. code-block:: python

      gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

   La detección de rostros/ojos funciona en imágenes en escala de grises y es más rápida que usar imágenes en color.

#. Mejorar el contraste para una detección más estable:

   .. code-block:: python

      gray = cv2.equalizeHist(gray)

   La ecualización del histograma puede mejorar los resultados de detección bajo diferentes condiciones de iluminación.

#. Detectar rostros en el fotograma:

   .. code-block:: python

      faces = face_cascade.detectMultiScale(
          gray,
          scaleFactor=1.2,
          minNeighbors=5,
          minSize=(60, 60)
      )

   Esto devuelve una lista de rectángulos ``(x, y, w, h)`` para todos los rostros detectados.

   - ``scaleFactor`` controla el paso de escala de la imagen (más pequeño puede ser más preciso pero más lento).
   - ``minNeighbors`` reduce los falsos positivos (más alto = más estricto).
   - ``minSize`` ignora las detecciones muy pequeñas.

#. Convertir RGB a BGR para dibujar y mostrar:

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

   Las funciones de dibujo de OpenCV e ``imshow`` esperan BGR para imágenes en color.

#. Dibujar rectángulos y etiquetas de rostros:

   .. code-block:: python

      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
      cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   Esto dibuja un cuadro alrededor de cada rostro detectado y añade una etiqueta como "Face 1".

#. Detectar ojos dentro de cada rostro (ROI):

   .. code-block:: python

      roi_gray = gray[y:y + h, x:x + w]
      roi_color = frame_bgr[y:y + h, x:x + w]

      eyes = eye_cascade.detectMultiScale(
          roi_gray,
          scaleFactor=1.2,
          minNeighbors=8,
          minSize=(20, 20)
      )

   ROI significa "Región de Interés". Detectar ojos solo dentro del área facial es más rápido y reduce las falsas detecciones.

#. Dibujar hasta dos ojos:

   .. code-block:: python

      for (ex, ey, ew, eh) in eyes[:2]:
          cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

   Esto dibuja rectángulos alrededor de los dos primeros ojos detectados.

#. Mostrar el resultado y manejar la salida:

   .. code-block:: python

      cv2.imshow(WIN, frame_bgr)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
          break

   Presiona ``q`` para salir, o cierra la ventana para salir de forma segura.

#. Limpieza (siempre se ejecuta):

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   La cámara se detiene y todas las ventanas de OpenCV se cierran incluso si ocurre un error.


5. Pros y Contras de la Detección Haar
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspecto
     - Ventajas
     - Desventajas
   * - Velocidad
     - Muy rápida; adecuada para Raspberry Pi
     - -
   * - Precisión
     - Funciona bien para rostros frontales
     - Sensible a la rotación y vistas de perfil
   * - Iluminación
     - Buena bajo iluminación uniforme
     - El rendimiento disminuye si es demasiado brillante/oscuro
   * - Modelo
     - Tamaño de modelo pequeño; fácil de implementar
     - Menos preciso que los métodos de aprendizaje profundo

Debido a que es ligera y rápida, las características Haar siguen siendo muy prácticas en dispositivos embebidos.


6. Mejoras Comunes
----------------------

1. **Preprocesamiento de Iluminación**: Aplica ecualización de histograma o CLAHE antes de la detección para mejorar el rendimiento con poca luz.
2. **Detección Multiángulo**: Carga clasificadores de rostros frontales y de perfil para detectar más poses.
3. **Más Características Faciales**: Añade clasificadores Haar para ojos/boca/nariz para enriquecer la detección.
4. **Usar DNN en lugar de Haar**: OpenCV DNN + ResNet/MobileNet puede ofrecer mayor precisión (pero requiere más recursos computacionales).



7. Ejercicios Extendidos
---------------------

- Usa ``cv2.equalizeHist`` en la imagen en escala de grises para mejorar la detección con poca luz.
- Añade clasificadores Haar de boca o nariz para detectar más características faciales.
- Graba el proceso de detección con ``cv2.VideoWriter``.
- Combínalo con salida GPIO para hacer un proyecto Raspberry Pi: "enciende un LED cuando se detecte un rostro".
