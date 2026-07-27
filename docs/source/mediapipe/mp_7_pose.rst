.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. Estimación de la Pose Humana
================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

Después de implementar el reconocimiento de manos y gestos,
este capítulo presenta **MediaPipe Pose** —
un módulo de estimación de pose humana en tiempo real, ligero pero potente.

Usando MediaPipe Pose, podemos detectar **33 puntos de referencia corporales**
en tiempo real y dibujar el esqueleto completo en el flujo de video.

.. image:: img/mp_pose.png
   :width: 400
   :align: center

Este módulo se puede usar para:

- Reconocimiento de acciones
- Corrección de postura
- Monitoreo de ejercicios
- Análisis de movimiento

------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El programa realiza los siguientes pasos:

1. Inicializar el modelo MediaPipe Pose
   (configurar la complejidad del modelo y la segmentación opcional).
2. Capturar fotogramas de video usando ``Picamera2``.
3. Convertir fotogramas al formato RGB (requerido por MediaPipe).
4. Ejecutar el modelo Pose para obtener 33 puntos clave corporales.
5. Dibujar puntos clave y conexiones del esqueleto usando OpenCV.
6. Mostrar el flujo de video anotado en tiempo real.

Este capítulo sienta las bases para tareas más avanzadas
de interacción persona-computadora y análisis de movimiento corporal.


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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   Si deseas usar MediaPipe Pose con un video grabado, puedes ejecutar el siguiente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. Después de ejecutar el programa, se abre una ventana titulada "Show Video" y muestra la transmisión de la cámara en vivo.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Cuando aparece una persona frente a la cámara:

   - MediaPipe Pose detecta 33 puntos de referencia corporales en tiempo real.
   - Se dibuja un esqueleto corporal completo en el fotograma de video.
   - Las articulaciones clave como hombros, codos, muñecas, caderas, rodillas y tobillos se conectan con líneas.

   A medida que la persona se mueve:

   - Los puntos clave del esqueleto siguen el movimiento corporal suavemente.
   - El esqueleto se actualiza continuamente en tiempo real.

   Si la segmentación de fondo está habilitada (``enable_segmentation=True``),
   el modelo calcula internamente una máscara de segmentación, aunque en este ejemplo
   solo se muestra el esqueleto.

   Si no se detecta ninguna persona, el programa simplemente muestra la transmisión normal de la cámara sin anotaciones.

   Presiona ``q`` para salir del programa.
   La cámara se detiene y la ventana de OpenCV se cierra automáticamente.

-----------------------------
4. Código Completo
-----------------------------

Aquí hay un programa básico de detección de pose humana:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
       static_image_mode=False,  # False for processing video streams
       model_complexity=2,       # 0~2, higher is more accurate
       enable_segmentation=True, # Enable background segmentation (optional)
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Pose detection
      results = pose.process(frame_rgb)

      # Convert RGB back to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If human body is detected, draw skeleton
      if results.pose_landmarks:
         drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Después de ejecutar el programa, la transmisión de la cámara mostrará un esqueleto humano en tiempo real, incluyendo:

- 33 puntos clave
- Líneas de conexión del esqueleto
- El esqueleto sigue el movimiento cuando la persona se mueve

-----------------------------
5. Explicación del Código
-----------------------------

**1. Importar bibliotecas**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  Controla la cámara Raspberry Pi, basada en libcamera.

* **cv2 (OpenCV)**
  Se usa para la conversión de espacio de color de imagen (BGR↔RGB), ventanas de visualización, dibujo de gráficos.

* **mediapipe.python.solutions.pose**
  El **modelo Pose** de MediaPipe, que puede detectar **33 puntos clave de todo el cuerpo** (cabeza, hombros, codos, rodillas, etc.), y puede devolver máscaras de segmentación (persona vs. fondo).

* **drawing_utils / drawing_styles**
  Herramientas de dibujo integradas de MediaPipe y definiciones de estilo, utilizadas para dibujar puntos clave y líneas del esqueleto.

**2. Inicializar el modelo Pose**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Continuous video mode
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False``: Indica que la entrada es un flujo de video continuo, no una imagen única. Rastrea después de la detección inicial para mayor velocidad. Generalmente se establece en False.

* ``model_complexity=1``: Complejidad del modelo, 0=ligero, 1=medio, 2=alta precisión (más lento). Establece en 1 o 2 si el rendimiento de Raspberry Pi lo permite.

* ``enable_segmentation=True``: Genera una máscara de segmentación humana, puede distinguir la persona del fondo. Cuando es True, permite efectos como reemplazo de fondo, croma clave. Este uso se explicará en la documentación posterior: :ref:`mp_pose_segmentation`

MediaPipe Pose devuelve una estructura de resultados que incluye:

* ``pose_landmarks``: 33 puntos clave;
* ``pose_world_landmarks``: Coordenadas mundiales 3D;
* ``segmentation_mask``: Mapa de segmentación humana.

**3. Abrir la cámara**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

* Crear objeto de cámara ``Picamera2()``
* Establecer resolución **640x480**, formato de píxel ``"XRGB8888"`` (BGRA de 4 canales).
  Este formato tiene la mejor compatibilidad con OpenCV, eliminando pasos de decodificación.
* Iniciar la cámara.

Opcional:
``picam2.start_preview(Preview.QTGL)`` puede mostrar la ventana de flujo de video directamente en la GPU; está comentado aquí, usando ``imshow()`` de OpenCV en su lugar.

**4. Bucle principal: Procesar cada fotograma**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Capture a frame from the camera (BGRA format)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. Capturar el fotograma actual. Picamera2 devuelve imágenes en formato **BGRA** (Blue Green Red + Alpha) por defecto.
2. Convertir a **BGR** para el procesamiento posterior de OpenCV.

.. code-block:: python

   # Convert to RGB for MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

Los modelos de MediaPipe **deben usar RGB**.

* Llamar a ``pose.process()`` para la detección de puntos clave.
* ``results`` es un objeto complejo que puede contener:

  * ``results.pose_landmarks``: Puntos clave (33 puntos)
  * ``results.pose_world_landmarks``: Coordenadas 3D
  * ``results.segmentation_mask``: Máscara de segmentación

.. code-block:: python

   # Convert back to BGR for OpenCV display
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

Convertir de vuelta porque ``imshow()`` de OpenCV requiere orden BGR.

**5. Dibujar puntos clave de la pose**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

Si se detecta un cuerpo humano:

* ``results.pose_landmarks``: Contiene ``(x, y, z, visibility)`` para cada punto clave.

  * ``x, y``: Coordenadas normalizadas (0~1)
  * ``z``: Profundidad relativa
  * ``visibility``: Confianza del punto clave (0~1)

* Explicación de los parámetros de ``draw_landmarks``:

   * ``frame``: Imagen sobre la que dibujar (formato BGR)
   * ``results.pose_landmarks``: Puntos clave humanos para el fotograma actual
   * ``mp_pose.POSE_CONNECTIONS``: Reglas de conexión (qué puntos conectar con líneas)
   * ``landmark_drawing_spec``: Estilo de dibujo de puntos
   * ``connection_drawing_spec``: Estilo de dibujo de líneas (se puede omitir, usa el estilo predeterminado del sistema)

Efecto: Dibuja el esqueleto (conexiones para cabeza, brazos, piernas) y los puntos clave (posiciones de las articulaciones) en la imagen.

**6. Mostrar fotograma y lógica de salida**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

Mostrar cada fotograma en la ventana ``"Show Video"``.
Salir del bucle cuando se presiona la tecla 'q'.

**7. Liberar recursos**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Detener la vista previa, liberar la cámara, cerrar todas las ventanas de OpenCV.

-----------------------------
6. Introducción al Modelo Pose
-----------------------------

El módulo MediaPipe Pose devuelve **33 puntos clave**, cubriendo áreas como la cabeza, el torso, los brazos y las piernas:

.. list-table::
   :header-rows: 1

   * - Parte del Cuerpo
     - Índice
   * - Nariz
     - 0
   * - Hombro izquierdo/derecho
     - 11 / 12
   * - Codo izquierdo/derecho
     - 13 / 14
   * - Muñeca izquierda/derecha
     - 15 / 16
   * - Cadera izquierda/derecha
     - 23 / 24
   * - Rodilla izquierda/derecha
     - 25 / 26
   * - Tobillo izquierdo/derecho
     - 27 / 28
   * - Índice del pie izquierdo/derecho
     - 31 / 32

Estos puntos se pueden usar para **juicio de postura**, **conteo de acciones** (por ejemplo, sentadillas, flexiones, detección de postura de yoga), etc.

-----------------------------
7. Rendimiento y Ajuste
-----------------------------

.. list-table::
   :header-rows: 1

   * - Elemento
     - Impacto
     - Sugerencia de optimización
   * - Resolución
     - Mayor resolución aumenta la precisión pero también la latencia
     - Usa 640x480 para equilibrar rendimiento y velocidad
   * - model_complexity
     - Mejora la precisión del reconocimiento pero ralentiza el cálculo
     - Recomendado 1~2 para Raspberry Pi
   * - segmentation
     - Aumenta la carga de GPU/CPU
     - Recomendado desactivar si no se necesita reemplazo de fondo

------------------------------------------------------------
8. Solución de Problemas
------------------------------------------------------------

- No se detecta ninguna persona

  Si el programa se ejecuta pero no se detecta ninguna persona, asegúrate de que todo el cuerpo esté dentro del fotograma de la cámara. Evita la retroiluminación fuerte y mejora las condiciones de iluminación. Mantén una distancia de aproximadamente 1 a 2 metros de la cámara para obtener mejores resultados.

- El video es lento o se queda rezagado

  Si la tasa de fotogramas es baja, intenta reducir la resolución a 640x480 o menos. Establece ``model_complexity = 1`` para un mejor rendimiento. Desactiva la segmentación si no es necesaria y cierra otros programas de fondo para liberar recursos del sistema.

- Ocurre un error de segmentación

  La mayoría de los errores de segmentación son causados por una incompatibilidad entre la arquitectura del sistema y la rueda de MediaPipe instalada.

  Verifica la arquitectura de tu sistema:

  .. code-block:: bash

     uname -m

  La salida debe ser ``aarch64``.

  Si ves ``armv7l`` o ``armhf``, estás usando Raspberry Pi OS de 32 bits, que no es compatible con la rueda oficial de MediaPipe.

  También puedes verificar en Python:

  .. code-block:: python

     import platform
     print(platform.machine())

  El resultado también debe ser ``aarch64``.

- Usando aarch64 pero aún así ocurre un error de segmentación

  Esto puede ocurrir si algunos kernels de TensorFlow Lite XNNPACK no son completamente compatibles con tu compilación de MediaPipe.

  Posibles soluciones:

  - Usa ``model_complexity = 1`` (recomendado en este tutorial).
  - Asegúrate de que MediaPipe esté instalado en el entorno virtual correcto.
  - Instala una rueda optimizada para Raspberry Pi como ``mediapipe-bin`` (versión de PINTO0309).

- ``model_complexity = 2`` falla pero ``1`` funciona

  La complejidad 2 carga un modelo más grande que puede activar optimizaciones avanzadas de CPU. En Raspberry Pi, algunos kernels optimizados de TensorFlow Lite pueden no ser totalmente compatibles. La complejidad 1 evita esos kernels y es generalmente más estable y rápida en Raspberry Pi.



-----------------------------
9. Resumen
-----------------------------

- Este capítulo implementó la **detección de esqueleto humano en tiempo real** basada en MediaPipe Pose;
- Pose proporciona 33 puntos clave, utilizables en campos como fitness, análisis de postura, reconocimiento de acciones;
- Ajustando la resolución y la complejidad del modelo, se puede lograr un funcionamiento fluido en Raspberry Pi;
- Basándonos en estos puntos clave, podemos desarrollar posteriormente:

  - Reconocimiento de acciones (por ejemplo, "levantar la mano", "sentadilla")
  - Evaluación de postura (por ejemplo, "¿la postura al sentarse es correcta?")
  - Control interactivo humano.
