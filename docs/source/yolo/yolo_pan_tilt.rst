.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Seguir Objetos con Pan-Tilt
==============================================================


En los tutoriales anteriores, aprendimos como usar YOLO para la deteccion de objetos en Raspberry Pi. Sin embargo, la deteccion es solo el primer paso—si quieres que la camara realmente "siga" al objetivo, necesitas combinar la deteccion con control mecanico.

Este tutorial te guiara en la construccion de un **Sistema de Seguimiento de Objetos YOLO** que logra lo siguiente:

* Deteccion en tiempo real de objetos especificos usando YOLO
* Calculo automatico de la desviacion de posicion del objetivo en el encuadre
* Camara con pan-tilt controlada por servos para mantener el objetivo centrado en el encuadre
* Soporte para guardar fotogramas actuales con la tecla ESPACIO para recopilacion de conjuntos de datos

Aqui seguimos el objetivo de nuestro modelo personalizado entrenado en el tutorial anterior—el mio es un muneco de nieve. Tambien puedes elegir otros modelos (como yolov8n) para seguir otros objetivos (como personas, autos, etc.).

.. image:: img/yolo_track.png

Figura: Sistema de seguimiento de objetos YOLO en accion. Cuando el objetivo se mueve, el pan-tilt de la camara lo sigue automaticamente, manteniendo el objetivo cerca de la mira amarilla en el centro del encuadre. El cuadro delimitador verde marca el objetivo detectado.

**Escenarios de Aplicacion**:

* Vigilancia inteligente: Seguir automaticamente objetivos sospechosos
* Acompanante de mascotas: Deja que la camara siga los movimientos de tu mascota
* Videoconferencias: Mantener automaticamente a los oradores centrados en el encuadre
* Recopilacion de datos: Capturar automaticamente imagenes de objetivos desde multiples angulos

Configuracion del Hardware
---------------------------------------

Para usar este proyecto, necesitas ensamblar el pan-tilt siguiendo las instrucciones en :ref:`assemble_fusion_hat_pan_tilt`.

.. image:: ../quick_start/img/gimbal_assemble.png


Ejecutar el Codigo
----------------------------------------

1. **Modificar parametros de configuracion**

   .. code-block:: bash

      cd ~/ai-lab-kit/yolo
      nano yolo_tracking.py

   Cambia la variable ``TARGET`` al principio del codigo al objeto que deseas seguir:

   .. code-block:: python

      TARGET = "person"     # Seguir a una persona
      # or
      TARGET = "snowman"    # Seguir un muneco de nieve

2. **Preparar el archivo del modelo**

   * Usa un modelo preentrenado: ``model = YOLO("yolov8n.pt")``
   * Usa un modelo personalizado: ``model = YOLO("snowman.pt")``

3. **Guardar y ejecutar el codigo**

   .. code-block:: bash

      python3 yolo_tracking.py

4. **Instrucciones de operacion**

   * Despues de iniciar el programa, la camara comienza a funcionar automaticamente
   * Cuando se detecta un objetivo, los servos giran automaticamente para mantener el objetivo centrado en el encuadre
   * Presiona ``ESPACIO`` para guardar el fotograma actual (para recopilar datos de entrenamiento)
   * Presiona ``ESC`` para salir del programa

Codigo
-----------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480         # Camera resolution
   CX, CY = W // 2, H // 2 # Center coordinates
   CONFIDENCE = 0.3        # Detection confidence threshold
   DEADZONE = 50           # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

   print(f"=== YOLO Tracking System ===")
   print(f"Target: {TARGET}")
   print(f"Confidence threshold: {CONFIDENCE}")
   print(f"Deadzone: {DEADZONE} pixels")

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

   # -------------------- Camera Initialization --------------------
   print("Initializing camera...")
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (W, H)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()
   time.sleep(2)

   print("\n=== System Ready ===")
   print("Controls:")
   print("  SPACE - Capture image (for dataset)")
   print("  ESC   - Exit")
   print("  (Auto-tracks object when detected)")
   print("==========================\n")

   # -------------------- Tracking Variables --------------------
   pan_pos = 0    # Current pan angle (-90 to 90)
   tilt_pos = 0   # Current tilt angle (-45 to 45)
   capture_count = 0

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

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

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

         # Draw deadzone rectangle (visual reference)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")


Explicacion del Codigo
------------------------------

Aqui esta el codigo completo de seguimiento de objetos YOLO. Analizaremos su principio de funcionamiento seccion por seccion.

**1. Importar Librerias y Parametros de Configuracion**

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480             # Camera resolution
   CX, CY = W // 2, H // 2     # Center coordinates
   CONFIDENCE = 0.3            # Detection confidence threshold
   DEADZONE = 50               # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

Parametros de configuracion:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Parametro
     - Descripcion
     - Valor Recomendado
   * - ``TARGET``
     - Nombre del objeto a seguir
     - "person", "snowman", "cup"
   * - ``W, H``
     - Resolucion de la camara
     - 640x480 (rendimiento equilibrado)
   * - ``DEADZONE``
     - Rango de zona muerta (pixeles)
     - 50-100, evita vibraciones frecuentes
   * - ``CONFIDENCE``
     - Umbral de confianza de deteccion
     - 0.3-0.5
   * - ``SAVE_DIR``
     - Directorio de guardado de imagenes
     - captured_images

**2. Inicializar Servos**

.. code-block:: python

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

Rangos de angulo del servo:

* Servo Pan (horizontal): -90° a 90°, 0° es el centro
* Servo Tilt (vertical): -45° a 45°, 0° es el centro

**3. Cargar Modelo YOLO**

.. code-block:: python

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

Recomendaciones de seleccion de modelo:

* Usa tu propio modelo entrenado: ``"snowman.pt"``, ``"my_pet.pt"``
* Usa modelo preentrenado: ``"yolov8n.pt"`` (puede detectar 80 objetos comunes)

**4. Logica de Deteccion y Seguimiento de Objetos**

.. code-block:: python

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

Explicacion de la logica de seguimiento:

* **Mecanismo de zona muerta**: Cuando el objetivo esta dentro de la zona muerta cerca del centro del encuadre, los servos no se mueven, evitando vibraciones frecuentes
* **Determinacion de direccion**: Si el objetivo esta a la izquierda del centro, gira a la derecha; si esta a la derecha del centro, gira a la izquierda
* **Identificacion del objetivo**: Encuentra el objeto a seguir comparando nombres de clases

**5. Bucle Principal**

.. code-block:: python

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

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

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair and deadzone
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")

Optimizacion de Rendimiento
-----------------------------------------

Al ejecutar el sistema de seguimiento en Raspberry Pi, las siguientes optimizaciones pueden ayudar:

1. **Reducir la frecuencia de deteccion**: Detectar cada 2-3 fotogramas, reutilizar los resultados de deteccion para otros fotogramas

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       if frame_count % 3 == 0:
           results = model.predict(frame, imgsz=320)
       frame_count += 1

2. **Reducir la region de deteccion**: Detectar solo en areas donde es probable que aparezca el objetivo

3. **Usar modelos mas pequenos**: ``yolov8n.pt`` es la mejor opcion

4. **Ajustar el rango de zona muerta**: Aumentar ``DEADZONE`` reduce el movimiento frecuente de los servos

Preguntas Frecuentes
---------------------------------

**P: ¿Que hago si los servos no se mueven?**

* Verifica si los servos estan correctamente conectados
* Verifica que la libreria fusion_hat este instalada correctamente

**P: ¿Que hago si la respuesta del seguimiento es demasiado lenta?**

* Reduce la resolucion de la camara (por ejemplo, 320x240)
* Reduce la resolucion de deteccion ``imgsz``
* Aumenta el rango de zona muerta para reducir el movimiento de los servos

**P: ¿Que hago si la deteccion del objetivo es inestable?**

* Ajusta el umbral ``CONFIDENCE`` (valores mas bajos detectan mas pero aumentan los falsos positivos)
* Asegura una iluminacion adecuada
* Usa un modelo entrenado personalizado para una mejor especificidad

**P: ¿Como ajustar la sensibilidad del servo?**

Modifica el valor de paso en la funcion ``simple_track``:

.. code-block:: python

   # Increase step size for faster servo movement
   pan_move = 2  # Originally 1
   tilt_move = 2

**P: ¿Puedo seguir multiples objetivos?**

Modifica la funcion ``find_target_detection`` para devolver el objetivo mas cercano o de mayor confianza, o implementa funcionalidad de cambio entre multiples objetivos.

Funciones Extendidas
-----------------------------------

**1. Agregar Control PID** (seguimiento mas suave)

.. code-block:: python

   # Simplified PID controller example
   pan_error = CX - obj_x
   pan_output = pan_error * 0.05  # Proportional control
   pan_pos += int(pan_output)

**2. Registrar Automaticamente la Trayectoria de Seguimiento**

.. code-block:: python

   # Record target position history
   trajectory = []
   trajectory.append((obj_x, obj_y))

**3. Enviar Notificaciones Cuando se Detecte un Objetivo**

.. code-block:: python

   if obj_x is not None:
       # Send email or push notification
       pass

**4. Integracion de Reconocimiento Facial**

Combinalo con librerias de reconocimiento facial para seguir solo a individuos especificos.

Resumen
---------------------

A traves de este tutorial, has aprendido:

* Como combinar la deteccion de objetos YOLO con el control de servos
* Como implementar un sistema de seguimiento automatico basado en vision
* Como usar mecanismos de zona muerta para evitar vibraciones
* Como recopilar datos de entrenamiento durante el seguimiento

Este sistema se puede aplicar ampliamente en escenarios como vigilancia inteligente, fotografia automatizada y vision robotica. A medida que los modelos YOLO continuan evolucionando, puedes construir sistemas de seguimiento aun mas inteligentes, como ajustar automaticamente el zoom segun el tamano del objetivo, o predecir el movimiento del objetivo basandose en trayectorias de movimiento.
