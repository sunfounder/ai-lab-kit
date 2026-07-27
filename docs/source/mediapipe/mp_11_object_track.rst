.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. Seguimiento de Objetos con Cámara Pan-Tilt
=================================================

------------------------------------------------------------
1. Descripción General
------------------------------------------------------------

En este capítulo, extendemos la detección de objetos de MediaPipe
para construir un **sistema de seguimiento de objetos** simple
usando una plataforma de servo pan-tilt.

El sistema detecta un objeto objetivo especificado
(por ejemplo, un "banana")
y ajusta automáticamente dos servos
para mantener el objeto centrado en la vista de la cámara.

.. image:: img/mp_object_track.png
   :width: 500
   :align: center

Este proyecto combina:

- Detección de objetos en tiempo real
- Control de motor servo
- Lógica de seguimiento proporcional
- Superposición de retroalimentación visual

Demuestra cómo la visión artificial puede controlar directamente
hardware físico en tiempo real.


------------------------------------------------------------
2. Cómo Funciona
------------------------------------------------------------

El sistema de seguimiento sigue estos pasos:

1. Inicializar los servos pan y tilt en la posición central.
2. Configurar la cámara Raspberry Pi para transmisión de video.
3. Cargar el modelo EfficientDet Lite0 para la detección de objetos.
4. Detectar objetos en cada fotograma usando MediaPipe Tasks.
5. Identificar el objeto objetivo (ej., "banana").
6. Calcular el desplazamiento del objeto relativo al centro del fotograma.
7. Ajustar los ángulos del servo usando control proporcional.
8. Mostrar guías de seguimiento y estado en la pantalla.

Este ejemplo muestra cómo la retroalimentación basada en visión
se puede usar para controlar el movimiento del hardware dinámicamente.

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

       sudo python3 ~/ai-lab-kit/mediapipe/mp_track_object.py

#. Después de ejecutar el programa, se abre la ventana de la cámara y comienza la detección de objetos en tiempo real.

   .. raw:: html

         <video width="300" loop muted controls>
             <source src="../_static/video/object_tracking.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   El sistema busca el objeto objetivo especificado (predeterminado: ``banana``).
   Se muestra una cruz amarilla en el centro de la pantalla como punto de referencia.

   Cuando el objeto objetivo aparece en el fotograma:

   - MediaPipe detecta el objeto usando el modelo EfficientDet Lite0.
   - Se calcula el centro del rectángulo delimitador detectado.
   - Si el objeto está fuera de la zona muerta central, los servos pan y tilt se mueven paso a paso.
   - La cámara rota físicamente para mantener el objeto cerca del centro del fotograma.
   - Se dibuja un cuadro de seguimiento verde alrededor del objeto.
   - La pantalla muestra:

     - ``Tracking banana`` (estado)
     - Ángulos actuales del servo (Pan / Tilt)

   Cuando el objeto no se detecta:

   - Los servos dejan de moverse.
   - El texto de estado cambia a ``No banana found`` (mostrado en rojo).

   La lógica de seguimiento usa un control de zona muerta simple de 4 direcciones:
   los servos solo se mueven cuando el objeto está suficientemente lejos del centro,
   evitando vibraciones.

   Presiona ``q`` para detener el programa.

   Al salir:

   - Ambos servos vuelven a la posición central.
   - La cámara se detiene.
   - La ventana de visualización se cierra.
   - Se imprime un mensaje: ``Tracking stopped. Servos centered.``

-----------------------------
4. Código Completo
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3

   import cv2
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2
   from pathlib import Path

   # MediaPipe imports
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Configuration --------------------
   TARGET = "banana"      # Object to track
   W, H = 640, 480           # Camera resolution
   CX, CY = W // 2, H // 2   # Center coordinates
   SCORE_THRESHOLD = 0.3     # Detection confidence threshold
   DEADZONE = 50             # Pixels from center before moving

   print(f"Tracking: {TARGET}")

   # -------------------- Servo Initialization --------------------
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)     # Allow servos to reach position

   # -------------------- Camera Initialization --------------------
   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))
   cam.start()
   time.sleep(2)     # Allow camera to stabilize

   # -------------------- MediaPipe Detector Setup --------------------
   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")

   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

   detector = vision.ObjectDetector.create_from_options(options)

   print("Ready. Press 'q' to quit")

   # -------------------- Tracking Logic --------------------
   def simple_track(x, y):
       """Basic 4-direction tracking with deadzone"""
       if x is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Left/right movement decision
       if x < CX - DEADZONE:
           pan_move = 1          # Move right
       elif x > CX + DEADZONE:
           pan_move = -1         # Move left

       # Up/down movement decision
       if y < CY - DEADZONE:
           tilt_move = -1        # Move down
       elif y > CY + DEADZONE:
           tilt_move = 1         # Move up

       return pan_move, tilt_move

   # -------------------- Main Tracking Loop --------------------
   pan_pos = 0   # Current pan angle (-90° to +90°)
   tilt_pos = 0  # Current tilt angle (-45° to +45°)

   try:
       while True:
           # Capture frame from camera
           frame = cam.capture_array()
           frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

           # Convert to RGB for MediaPipe
           rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

           # Detect objects in frame
           detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

           # Search for target object
           obj_x = obj_y = None
           for detection in detections.detections:
               for category in detection.categories:
                   # Case-insensitive search for target
                   if TARGET.lower() in str(category.category_name).lower():
                       bbox = detection.bounding_box
                       # Calculate object center
                       obj_x = bbox.origin_x + bbox.width // 2
                       obj_y = bbox.origin_y + bbox.height // 2
                       break

           # Process tracking if object found
           if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move

               # Limit servo angles to safe ranges
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))

               # Send commands to servos
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)

               # Draw tracking box around object
               cv2.rectangle(frame,
                            (obj_x - 30, obj_y - 30),
                            (obj_x + 30, obj_y + 30),
                            (0, 255, 0), 2)
               status = f"Tracking {TARGET}"
               color = (0, 255, 0)  # Green for tracking
           else:
               status = f"No {TARGET} found"
               color = (0, 0, 255)  # Red for not found

           # Draw center crosshair for reference
           cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
           cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

           # Display status information
           cv2.putText(frame, status, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
           cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                      (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
           cv2.putText(frame, "Press 'q' to quit", (10, 90),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

           # Show video window
           cv2.imshow(f"Track: {TARGET}", frame)

           # Exit on 'q' key press
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break

   finally:
       # -------------------- Cleanup --------------------
       pan.angle(0)      # Return to center
       tilt.angle(0)     # Return to center
       time.sleep(0.5)   # Allow movement
       cam.stop()        # Stop camera
       cv2.destroyAllWindows()  # Close display
       print("Tracking stopped. Servos centered.")

-----------------------------
5. Explicación del Código
-----------------------------

**Sección de Configuración**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET``: Categoría de objeto a rastrear (debe estar en las clases del conjunto de datos COCO);
- ``W, H``: Resolución de la cámara - equilibrada entre velocidad y detalle;
- ``CX, CY``: Coordenadas del centro del fotograma para referencia de seguimiento;
- ``SCORE_THRESHOLD``: Confianza mínima para una detección válida;
- ``DEADZONE``: Distancia desde el centro antes de que comience el movimiento del servo (reduce vibraciones).

**Inicialización del Servo**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` y ``Servo(3)`` corresponden a los canales en Fusion HAT;
- ``.angle(0)`` centra los servos en la posición de 0°;
- ``time.sleep(1)`` asegura que los servos lleguen a la posición antes de continuar.

**Configuración de la Cámara**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- Usa la biblioteca Picamera2 para la API moderna de cámara;
- El formato ``XRGB8888`` proporciona canales de color de 8 bits;
- ``time.sleep(2)`` permite que el sensor de la cámara se estabilice.

**Detector MediaPipe**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- Carga el modelo EfficientDet Lite0 desde el mismo directorio;
- ``RunningMode.VIDEO`` optimizado para procesamiento continuo de fotogramas;
- ``detect_for_video()`` requiere una marca de tiempo para cada fotograma.

**Función de Seguimiento**

.. code-block:: python

   def simple_track(x, y):
       if x < CX - DEADZONE:
           pan_move = 1      # Object left → move right
       elif x > CX + DEADZONE:
           pan_move = -1     # Object right → move left

       if y < CY - DEADZONE:
           tilt_move = -1    # Object up → move down
       elif y > CY + DEADZONE:
           tilt_move = 1     # Object down → move up

- Control proporcional simple (no es un PID real);
- La zona muerta evita vibraciones del servo por movimientos pequeños;
- Devuelve valores de movimiento de -1, 0 o 1 para cada eje.

**Procesamiento del Bucle Principal**

.. code-block:: python

   # Object detection
   detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

   # Find target object
   for detection in detections.detections:
       for category in detection.categories:
           if TARGET.lower() in str(category.category_name).lower():
               bbox = detection.bounding_box
               obj_x = bbox.origin_x + bbox.width // 2
               obj_y = bbox.origin_y + bbox.height // 2

1. Convertir el fotograma al formato de imagen de MediaPipe;
2. Ejecutar la detección de objetos con la marca de tiempo actual;
3. Buscar en las detecciones el objeto objetivo (sin distinción de mayúsculas/minúsculas);
4. Calcular las coordenadas del centro del objeto.

**Lógica de Control del Servo**

.. code-block:: python

   if obj_x is not None:
       pan_move, tilt_move = simple_track(obj_x, obj_y)
       pan_pos += pan_move
       tilt_pos += tilt_move

       # Enforce safe angle limits
       pan_pos = max(-90, min(90, pan_pos))
       tilt_pos = max(-45, min(45, tilt_pos))

       pan.angle(pan_pos)
       tilt.angle(tilt_pos)

1. Obtener comandos de movimiento de la función de seguimiento;
2. Actualizar los acumuladores de posición;
3. Limitar las posiciones a los límites mecánicos;
4. Enviar nuevos ángulos a los servos.

**Retroalimentación Visual**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)

   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)

   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- Cuadro verde: Objeto actualmente rastreado;
- Cruz amarilla: Referencia del centro del fotograma;
- Texto de estado: Estado del seguimiento y ángulos del servo.

**Rutina de Limpieza**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- Devuelve los servos a la posición central;
- Detiene la captura de la cámara;
- Cierra las ventanas de OpenCV;
- Se ejecuta incluso si ocurre un error (``try...finally``).

------------------------------------------------------
6. Opciones de Configuración
------------------------------------------------------

**Cambiar el Objeto Objetivo**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**Ajustar Parámetros de Seguimiento**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive

   # Faster, more responsive tracking
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**Límites de Rango del Servo**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**Ajuste de Rendimiento**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing

   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. Consideraciones de Rendimiento
------------------------------------------------------

.. list-table:: Factores de rendimiento
   :header-rows: 1

   * - Factor
     - Efecto en el rendimiento
     - Recomendación
   * - Resolución de cámara
     - Mayor = detección más lenta
     - 640x480 buen equilibrio
   * - Umbral de detección
     - Más bajo = más detecciones pero más falsos positivos
     - 0.3-0.5 óptimo
   * - Tamaño de zona muerta
     - Más grande = más suave pero menos receptivo
     - 40-60 píxeles
   * - Velocidad del servo
     - Más rápido = más receptivo pero puede sobrepasar
     - Considerar control de aceleración
   * - Tamaño del modelo
     - Lite0 más rápido, Lite2 más preciso
     - Lite0 para seguimiento en tiempo real

**Rendimiento esperado:**

- **Raspberry Pi 4:** 8-15 FPS con 640x480
- **Latencia de detección:** 100-200ms
- **Tiempo de respuesta del servo:** 50-100ms por grado
- **Latencia total del sistema:** 200-400ms

------------------------------------------------------
8. Guía de Solución de Problemas
------------------------------------------------------

.. list-table:: Problemas comunes y soluciones
   :header-rows: 1

   * - Problema
     - Causa posible
     - Solución
   * - No hay detección de objetos
     - El objeto no está en las clases COCO
     - Usa nombres de objetos compatibles
   * - Movimiento del servo brusco
     - Zona muerta demasiado pequeña
     - Aumenta DEADZONE a 60-80
   * - El servo sobrepasa
     - Paso de movimiento demasiado grande
     - Cambia pan_move de 1 a 0.5
   * - Baja tasa de fotogramas
     - Resolución demasiado alta
     - Reduce a 320x240
   * - La cámara no funciona
     - Cámara no habilitada
     - Ejecuta ``sudo raspi-config``
   * - Los servos no se mueven
     - Cableado o alimentación incorrectos
     - Verifica las conexiones y la fuente de alimentación
   * - El objeto se pierde frecuentemente
     - Umbral demasiado alto
     - Reduce SCORE_THRESHOLD a 0.2
   * - Dirección de seguimiento incorrecta
     - Orientación del servo invertida
     - Intercambia los signos de pan_move

**Consejos de depuración:**

1. **Probar servos por separado:**

   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **Verificar la detección de objetos:**

   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **Verificar las coordenadas del objeto:**

   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **Monitorear la tasa de fotogramas:**

   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. Modificaciones Avanzadas
------------------------------------------------------

**1. Implementación de Control PID**

.. code-block:: python

   class PIDController:
       def __init__(self, kp=0.1, ki=0.01, kd=0.05):
           self.kp, self.ki, self.kd = kp, ki, kd
           self.prev_error = 0
           self.integral = 0

       def update(self, error, dt=1.0):
           self.integral += error * dt
           derivative = (error - self.prev_error) / dt
           output = self.kp*error + self.ki*self.integral + self.kd*derivative
           self.prev_error = error
           return output

**2. Seguimiento de Múltiples Objetos**

.. code-block:: python

   # Track closest object
   best_dist = float('inf')
   best_obj = None
   for detection in detections.detections:
       bbox = detection.bounding_box
       obj_x = bbox.origin_x + bbox.width // 2
       obj_y = bbox.origin_y + bbox.height // 2
       dist = ((obj_x - CX)**2 + (obj_y - CY)**2)**0.5
       if dist < best_dist:
           best_dist = dist
           best_obj = (obj_x, obj_y)

**3. Velocidad Proporcional a la Distancia**

.. code-block:: python

   def adaptive_track(x, y):
       if x is None:
           return 0, 0

       # Calculate distance from center
       dx = x - CX
       dy = y - CY

       # Speed proportional to distance (with deadzone)
       pan_move = 0
       tilt_move = 0

       if abs(dx) > DEADZONE:
           pan_move = dx * 0.02  # 2% of distance per frame

       if abs(dy) > DEADZONE:
           tilt_move = dy * 0.02

       return pan_move, tilt_move

**4. Memoria de Objeto (Seguimiento Inercial)**

.. code-block:: python

   # Keep tracking briefly when object lost
   OBJECT_TIMEOUT = 10  # frames
   lost_counter = 0

   if obj_x is not None:
       last_x, last_y = obj_x, obj_y
       lost_counter = 0
   elif lost_counter < OBJECT_TIMEOUT:
       obj_x, obj_y = last_x, last_y  # Use last known position
       lost_counter += 1

------------------------------------------------------
10. Aplicaciones y Extensiones
------------------------------------------------------

**Aplicaciones educativas:**

- Principios de robótica y automatización
- Fundamentos de visión artificial
- Sistemas de control (P vs PID)
- Diseño de sistemas en tiempo real

**Aplicaciones prácticas:**

- Seguimiento automático de cámaras de seguridad
- Automatización de cámaras para videoconferencias
- Observación de vida silvestre
- Tecnología de asistencia para seguimiento

**Proyectos de extensión:**

1. **Interfaz web:** Control remoto a través del navegador
2. **Posiciones preestablecidas:** Guardar/cargar posiciones de seguimiento comunes
3. **Aprendizaje de objetos:** Entrenar en objetos personalizados
4. **Multicámara:** Coordinar múltiples unidades de seguimiento
5. **Integración en la nube:** Subir datos de seguimiento para análisis
6. **Retroalimentación de audio:** Anunciar el estado del seguimiento
7. **Control por gestos:** Usar gestos de la mano para controlar el seguimiento

-----------------------------
11. Seguridad y Buenas Prácticas
-----------------------------

1. **Seguridad mecánica:**

   - Asegura todas las partes móviles
   - Usa gestión de cables
   - Evita puntos de pellizco
   - Establece límites de ángulo razonables

2. **Seguridad eléctrica:**

   - Usa alimentación externa para los servos
   - Asegura una conexión a tierra adecuada
   - Evita sobrecargar la fuente de alimentación
   - Usa cables de calibre apropiado

3. **Seguridad del software:**

   - Incluye siempre el centrado del servo al salir
   - Implementa un mecanismo de parada de emergencia
   - Registra errores para depuración
   - Valida entradas y límites

4. **Seguridad operativa:**

   - Mantente alejado del mecanismo en movimiento
   - Monitorea el sobrecalentamiento
   - Revisiones de mantenimiento regulares
   - Ten capacidad de anulación manual

-----------------------------
12. Resumen
-----------------------------

Este capítulo demostró un sistema completo de seguimiento de objetos usando:

1. **MediaPipe Tasks** para una detección de objetos fiable
2. **Servos pan-tilt** para seguimiento físico
3. **Control proporcional simple** para la lógica de movimiento
4. **OpenCV** para retroalimentación visual y visualización

El sistema proporciona una base para aplicaciones de seguimiento más avanzadas y demuestra conceptos clave en visión artificial en tiempo real, sistemas de control y programación Python embebida.

Modificando el objeto objetivo, ajustando parámetros y extendiendo la lógica de control, este sistema se puede adaptar para varias aplicaciones, desde demostraciones educativas hasta soluciones prácticas de automatización.

**Próximos pasos:**

- Implementar control PID para un seguimiento más suave
- Añadir memoria de objeto para manejar occlusiones temporales
- Crear interfaz web para monitoreo remoto
- Integrar con sistemas de automatización del hogar
- Entrenar modelos personalizados de detección de objetos
