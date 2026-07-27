.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. Pantalla Verde
=========================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

Este capítulo utiliza la capacidad de **segmentación de personas** de
MediaPipe Pose para implementar un simple **efecto de pantalla verde**.

Al separar a la persona del fondo,
podemos reemplazar el fondo original con un color verde sólido.
Esto permite:

- Aplicaciones de fondo virtual
- Composición de croma clave (OBS / NLE)
- Efectos de transmisión en vivo
- Reemplazo de escenas estilo RA

.. image:: img/mp_pose_green.png
   :align: center


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El efecto de pantalla verde se implementa usando los siguientes pasos:

1. Inicializar el modelo Pose con ``enable_segmentation=True``.
2. Para cada fotograma, obtener ``results.segmentation_mask``.
3. La máscara es un mapa de probabilidad de un solo canal (rango 0–1).
4. Aplicar un umbral (por ejemplo, 0.5) para separar el primer plano del fondo.
5. Reemplazar los píxeles de fondo con verde sólido.
6. Opcionalmente, aplicar desenfoque o filtrado morfológico para suavizar los bordes.

Este método es ligero y se ejecuta en tiempo real en Raspberry Pi,
proporcionando un ejemplo práctico de segmentación humana.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

   Si deseas usar MediaPipe Pose con un video grabado, puedes ejecutar el siguiente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_9.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Aparece una barra deslizante llamada ``Mask`` en la misma ventana. Controla el umbral de segmentación (0–100), con el valor predeterminado establecido en 50 (0.5).

   Cuando aparece una persona frente a la cámara:

   - MediaPipe Pose genera un ``segmentation_mask`` para cada fotograma.
   - Los píxeles con valores de máscara por encima del umbral se tratan como primer plano (persona).
   - Todos los demás píxeles se reemplazan con un fondo verde sólido (efecto de pantalla verde).

   A medida que mueves la barra deslizante ``Mask``:

   - Aumentar el umbral mantiene solo el área de primer plano más confiable (menos fuga de fondo, pero puede cortar algunas partes del cuerpo).
   - Disminuir el umbral incluye más píxeles como primer plano (silueta más completa, pero puede incluir ruido de fondo).

   Si no hay máscara de segmentación disponible, el programa simplemente muestra la transmisión normal de la cámara sin reemplazo de fondo.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.

-----------------------------
4. Código Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: empty callback for trackbars ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutar el script, la persona (primer plano) se conserva y el fondo se reemplaza con verde sólido.
Se puede usar directamente para la composición posterior con **Chroma Key** en OBS, Premiere, DaVinci Resolve, etc.

-------------------------------------
5. Explicación de Puntos Clave
-------------------------------------

``segmentation_mask`` es una **imagen flotante de un solo canal** (rango 0~1) con el mismo tamaño que el fotograma de entrada:

- Valor **cercano a 1**: Alta probabilidad de ser **primer plano (persona)**;
- Valor **cercano a 0**: Alta probabilidad de ser **fondo**.

El enfoque habitual es establecer un umbral **T** (por ejemplo, 0.5) y crear una máscara de condición:

.. code-block:: python

   condition = (mask > T)[..., None]

Aquí configuramos una barra deslizante para ajustar el umbral en tiempo real:

.. code-block:: python

   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

Luego podemos usar ``np.where(condition, frame, background)`` para reemplazar el fondo; aquí lo reemplazamos con verde:

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
6. Optimización del Efecto y los Bordes
----------------------------------------------------

La binarización directa puede causar bordes dentados o pequeños agujeros alrededor del cabello y los bordes de la ropa.
Un **postprocesamiento ligero** puede mejorar los bordes:

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **Rango de valor T recomendado 0.3~0.7**: Se puede reducir apropiadamente en entornos oscuros/modelos conservadores; se puede aumentar con más ruido.
   - No hagas el kernel de desenfoque demasiado grande, de lo contrario el límite de la persona "filtrará verde".

----------------------------------------------------
7. Usar Fondo Personalizado (Imagen/Video)
----------------------------------------------------

Reemplazar el verde sólido con una imagen de fondo personalizada:

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

O usar otro video como fondo (leer el siguiente fotograma ``bg_frame``, redimensionar a las mismas dimensiones, luego reemplazar).

----------------------------------------------------
8. Equilibrio entre Rendimiento y Calidad
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Elemento
     - Impacto
     - Sugerencia
   * - Resolución
     - Mayor resolución da bordes más finos pero velocidad más lenta
     - Comienza con 640×480; aumenta si se necesita una imagen más clara
   * - model_complexity
     - Mayor es más preciso pero más lento
     - Recomendado 1~2 en Raspberry Pi
   * - Fuerza del postprocesamiento
     - Demasiado desenfoque/morfología puede "tragar bordes/filtrar verde"
     - Kernel pequeño + pocas iteraciones, observa el efecto de borde

------------------------------------------------------------
9. Solución de Problemas
------------------------------------------------------------

- Bordes dentados o costuras visibles alrededor de la persona

  Esto suele ocurrir porque la máscara se aplica con un umbral duro, lo que crea límites abruptos.

  Intenta ajustar el umbral usando la barra deslizante ``Mask``. Para bordes más suaves, aplica un pequeño desenfoque a la máscara de segmentación o usa una operación de cierre morfológico simple antes de la composición.

- Faltan partes de la persona

  Si partes del cuerpo se recortan, la iluminación puede ser demasiado débil, o el color de la ropa puede fusionarse con el fondo.

  Mejora la iluminación, ajusta el umbral e intenta usar un fondo más simple con mayor contraste contra el sujeto.

- Baja tasa de fotogramas

  Si el video se siente lento, la resolución puede ser demasiado alta o el modelo demasiado complejo.

  Reduce la resolución de la cámara (por ejemplo, 640×480 o 320×240) y mantén ``model_complexity`` en 1 para un mejor rendimiento.

- El verde se derrama sobre el sujeto

  Si el fondo verde aparece en el sujeto, el límite de segmentación puede ser inexacto, o el color del sujeto puede causar confusión visual.

  Intenta cambiar a un color de reemplazo diferente (azul o gris), o reemplaza el fondo con una imagen en lugar de un color sólido para un resultado más natural.


-----------------------------
10. Resumen
-----------------------------

- Usando ``segmentation_mask``, podemos lograr rápidamente "recorte de persona + reemplazo de fondo";
- Obtén bordes más naturales a través de umbrales y postprocesamiento ligero;
- Adecuado para fondos virtuales, composición de transmisiones en vivo, enseñanza remota, etc.;
- Los siguientes pasos podrían combinar el **esqueleto de pose** y la **segmentación** para efectos más interactivos (por ejemplo, reemplazar solo el fondo, no reemplazar el esqueleto superpuesto en primer plano).
