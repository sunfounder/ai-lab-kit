.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

9. Seguimiento de Objetos Rojos con Cámara Pan-Tilt
====================================================

El seguimiento de objetos combinado con control mecánico forma la base de muchas aplicaciones de robótica y visión artificial.
En este capítulo, crearemos un sistema que **detecta objetos rojos en tiempo real y controla servos pan-tilt** para mantener el objeto centrado en la vista de la cámara.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_9.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Esto extiende la detección básica de color a un sistema de seguimiento activo que puede seguir objetos en movimiento de forma autónoma.

.. image:: img/color_track.png
   :alt: Vista general del sistema de seguimiento con cámara pan-tilt
   :align: center


1. Objetivo y Enfoque
-------------------------

- Usar **Picamera2** para capturar fotogramas de video en tiempo real
- Detectar objetos rojos usando el **espacio de color HSV** y filtrado morfológico
- Implementar un algoritmo de **seguimiento simple de 4 direcciones** basado en la posición del objeto
- Controlar los **servos pan y tilt** para mantener el objeto centrado
- Mostrar **información de depuración en tiempo real** y estado del seguimiento
- Proporcionar **parámetros ajustables** para afinar el comportamiento del seguimiento


2. Ejecutar el Código
--------------------

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
        python3 cv_9_track_color.py

3. Resultado de la Ejecución
---------------------------------

Cuando se ejecute correctamente, deberías ver:

**1. Ventana de OpenCV:**

- "Red Object Tracking": Muestra la transmisión de la cámara con superposición de seguimiento

**2. Elementos visuales en la ventana de seguimiento:**

- Cruz amarilla en el centro del fotograma
- Rectángulo azul que muestra la zona muerta (zona sin movimiento)
- Círculo rojo que marca el centro del objeto detectado
- Línea verde que conecta el objeto con el centro del fotograma
- Superposición de información en tiempo real:

  - Coordenadas de posición del objeto
  - Ángulos actuales del servo
  - Modo de seguimiento (Simple 4-Direcciones)
  - Paso de movimiento y configuración de zona muerta

**3. Salida en consola:**

- FPS (fotogramas por segundo)
- Posiciones actuales del servo
- Estado de detección del objeto
- Ajustes del paso de movimiento

**4. Comportamiento del servo:**

- Los servos se moverán en pasos fijos para mantener los objetos rojos centrados
- Sin movimiento cuando el objeto está dentro de la zona muerta
- Los servos vuelven a la posición central cuando se presiona la tecla 'r'


**Controles:**

- Presiona **'q'** para salir del programa
- Presiona **'r'** para restablecer los servos a la posición central
- Presiona **'+'** para aumentar la velocidad de movimiento
- Presiona **'-'** para disminuir la velocidad de movimiento

4. Código Completo
-------------------------------

A continuación se muestra el programa Python completo para el seguimiento de objetos rojos:

.. code-block:: python

   #!/usr/bin/env python3
   """
   Red Object Tracking with Pan-Tilt Camera
   """

   import cv2
   import numpy as np
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2

   # ========== SERVO SETTINGS ==========
   # Servo channels
   PAN_CHANNEL = 2    # Horizontal servo
   TILT_CHANNEL = 3   # Vertical servo

   # Servo angle limits (adjust according to your hardware)
   PAN_MIN = -90      # Maximum left rotation
   PAN_MAX = 90       # Maximum right rotation
   TILT_MIN = -45     # Maximum down rotation
   TILT_MAX = 45      # Maximum up rotation

   # Initial position (center)
   PAN_CENTER = 0
   TILT_CENTER = 0

   # ========== CAMERA SETTINGS ==========
   FRAME_WIDTH = 640
   FRAME_HEIGHT = 480
   CENTER_X = FRAME_WIDTH // 2
   CENTER_Y = FRAME_HEIGHT // 2

   # ========== COLOR DETECTION SETTINGS ==========
   # Red color range in HSV (two ranges for red)
   LOWER_RED1 = np.array([0, 100, 80])     # Lower range for red
   UPPER_RED1 = np.array([10, 255, 255])   # Upper range for red
   LOWER_RED2 = np.array([170, 100, 80])   # Lower range for red (wrap-around)
   UPPER_RED2 = np.array([180, 255, 255])  # Upper range for red (wrap-around)

   # Morphology kernel for noise removal
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

   # Minimum contour area to consider (adjust based on object size)
   MIN_CONTOUR_AREA = 500

   # ========== TRACKING SETTINGS ==========
   # Deadzone around center (pixels) - no movement inside this zone
   DEADZONE_X = 50    # Horizontal deadzone
   DEADZONE_Y = 50    # Vertical deadzone

   # Movement step size in degrees (how much to move each frame)
   MOVE_STEP = 2      # Degrees to move per adjustment

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Red Object Tracking System...")

   # Initialize servos
   print("Setting up servos...")
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center the servos initially
   print("Centering servos...")
   pan_servo.angle(PAN_CENTER)
   tilt_servo.angle(TILT_CENTER)
   time.sleep(1)  # Wait for servos to move to center

   # Current servo positions
   current_pan = PAN_CENTER
   current_tilt = TILT_CENTER

   # Initialize camera
   print("Setting up camera...")
   picam2 = Picamera2()

   # Configure camera for OpenCV
   config = picam2.create_preview_configuration(
       main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "XRGB8888"}
   )
   picam2.configure(config)
   picam2.start()

   print("Camera started. Looking for red objects...")
   print("Press 'q' to quit the program")
   print("-" * 50)

   def simple_tracking(x, y):
       """
       Simple 4-direction tracking algorithm
       Args:
           x: Object x-coordinate (None if not found)
           y: Object y-coordinate (None if not found)
       Returns:
           pan_move, tilt_move: Degrees to move each servo (+/-)
       """
       # If no object detected, don't move
       if x is None or y is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Check if object is left of center (outside deadzone)
       if x < CENTER_X - DEADZONE_X:
           # Object is left, move camera right (positive pan)
           pan_move = MOVE_STEP
       # Check if object is right of center (outside deadzone)
       elif x > CENTER_X + DEADZONE_X:
           # Object is right, move camera left (negative pan)
           pan_move = -MOVE_STEP

       # Check if object is above center (outside deadzone)
       if y < CENTER_Y - DEADZONE_Y:
           # Object is up, move camera down (negative tilt)
           tilt_move = -MOVE_STEP
       # Check if object is below center (outside deadzone)
       elif y > CENTER_Y + DEADZONE_Y:
           # Object is down, move camera up (positive tilt)
           tilt_move = MOVE_STEP

       return pan_move, tilt_move

   def update_servo_position(pan_move, tilt_move):
       """
       Update servo positions with limits checking
       Args:
           pan_move: Degrees to move pan servo (+/-)
           tilt_move: Degrees to move tilt servo (+/-)
       Returns:
           current_pan, current_tilt: New servo positions
       """
       global current_pan, current_tilt

       # Calculate new positions
       new_pan = current_pan + pan_move
       new_tilt = current_tilt + tilt_move

       # Apply angle limits to prevent hardware damage
       new_pan = max(min(new_pan, PAN_MAX), PAN_MIN)
       new_tilt = max(min(new_tilt, TILT_MAX), TILT_MIN)

       # Move servos only if position changed
       if new_pan != current_pan:
           pan_servo.angle(new_pan)
           current_pan = new_pan

       if new_tilt != current_tilt:
           tilt_servo.angle(new_tilt)
           current_tilt = new_tilt

       return current_pan, current_tilt

   def find_red_object(frame):
       """
       Detect red object in frame using HSV color space
       Args:
           frame: Input BGR image frame
       Returns:
           center_x, center_y: Coordinates of largest red object, or (None, None)
           mask: Binary mask showing detected red areas
       """
       # Convert BGR to HSV color space (better for color detection)
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

       # Create masks for red color (red wraps around 0 in HSV)
       mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)   # Lower red range
       mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)   # Upper red range
       mask = cv2.bitwise_or(mask1, mask2)                # Combine both ranges

       # Apply morphological operations to clean up noise
       mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
       mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

       # Find contours in the mask
       contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

       # Return if no contours found
       if not contours:
           return None, None, mask

       # Find the largest contour (assume it's our target)
       largest_contour = max(contours, key=cv2.contourArea)
       area = cv2.contourArea(largest_contour)

       # Filter by minimum area to ignore small noise
       if area < MIN_CONTOUR_AREA:
           return None, None, mask

       # Calculate center of the contour using image moments
       M = cv2.moments(largest_contour)
       if M["m00"] == 0:  # Prevent division by zero
           return None, None, mask

       center_x = int(M["m10"] / M["m00"])
       center_y = int(M["m01"] / M["m00"])

       return center_x, center_y, mask

   def draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle):
       """
       Draw debugging information on the frame for visualization
       Args:
           frame: Frame to draw on
           object_x, object_y: Object coordinates
           mask: Detection mask
           pan_angle, tilt_angle: Current servo angles
       Returns:
           frame: Frame with debug drawings
       """
       # Draw center crosshair
       cv2.line(frame, (CENTER_X - 20, CENTER_Y), (CENTER_X + 20, CENTER_Y), (0, 255, 255), 2)
       cv2.line(frame, (CENTER_X, CENTER_Y - 20), (CENTER_X, CENTER_Y + 20), (0, 255, 255), 2)
       cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (0, 255, 255), -1)

       # Draw deadzone rectangle
       cv2.rectangle(frame,
                    (CENTER_X - DEADZONE_X, CENTER_Y - DEADZONE_Y),
                    (CENTER_X + DEADZONE_X, CENTER_Y + DEADZONE_Y),
                    (255, 255, 0), 1)

       # Draw object center if detected
       if object_x is not None and object_y is not None:
           cv2.circle(frame, (object_x, object_y), 10, (0, 0, 255), -1)
           cv2.line(frame, (CENTER_X, CENTER_Y), (object_x, object_y), (0, 255, 0), 2)

           # Display position information
           pos_text = f"Position: ({object_x}, {object_y})"
           cv2.putText(frame, pos_text, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

       # Display servo angles
       angle_text = f"Pan: {pan_angle:+03.0f}, Tilt: {tilt_angle:+03.0f}"
       cv2.putText(frame, angle_text, (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

       # Display tracking mode
       cv2.putText(frame, "Mode: Simple 4-Direction", (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Display movement step
       step_text = f"Step: {MOVE_STEP}, Deadzone: {DEADZONE_X}px"
       cv2.putText(frame, step_text, (10, 120),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Draw quit instruction
       cv2.putText(frame, "Press 'q' to quit, 'r' to reset", (10, FRAME_HEIGHT - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

       return frame

   def cleanup():
       """
       Clean up resources before exiting
       """
       print("\nCleaning up...")

       # Center servos before stopping
       print("Centering servos...")
       pan_servo.angle(PAN_CENTER)
       tilt_servo.angle(TILT_CENTER)
       time.sleep(0.5)

       # Stop camera
       print("Stopping camera...")
       picam2.stop()

       # Close OpenCV windows
       cv2.destroyAllWindows()
       print("System shutdown complete.")

   # ========== MAIN LOOP ==========
   def main():
       """
       Main tracking loop
       """
       frame_count = 0
       start_time = time.time()
       global MOVE_STEP
       global current_pan, current_tilt
       try:
           while True:
               # Capture frame from camera
               frame_bgra = picam2.capture_array()
               frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

               # Find red object in frame
               obj_x, obj_y, mask = find_red_object(frame_bgr)

               # Use simple tracking algorithm to determine movement
               pan_move, tilt_move = simple_tracking(obj_x, obj_y)

               # Update servo positions
               pan_angle, tilt_angle = update_servo_position(pan_move, tilt_move)

               # Draw debugging information
               frame_display = draw_debug_info(frame_bgr, obj_x, obj_y, mask, pan_angle, tilt_angle)

               # Display frames
               cv2.imshow("Red Object Tracking", frame_display)

               # Calculate and display FPS every 30 frames
               frame_count += 1
               if frame_count % 30 == 0:
                   elapsed_time = time.time() - start_time
                   fps = frame_count / elapsed_time
                   print(f"FPS: {fps:.1f} | Pan: {pan_angle:+03.0f}° | Tilt: {tilt_angle:+03.0f}° | "
                         f"Object: {'Found' if obj_x else 'Not found'}")

               # Check for user input
               key = cv2.waitKey(1) & 0xFF
               if key == ord('q'):
                   print("\nQuit command received.")
                   break
               elif key == ord('r'):
                   # Reset to center position
                   print("Resetting to center...")
                   pan_servo.angle(PAN_CENTER)
                   tilt_servo.angle(TILT_CENTER)
                   current_pan = PAN_CENTER
                   current_tilt = TILT_CENTER
                   time.sleep(0.5)
               elif key == ord('+'):
                   # Increase movement speed
                   MOVE_STEP = min(MOVE_STEP + 0.5, 5)
                   print(f"Movement step increased to {MOVE_STEP}°")
               elif key == ord('-'):
                   # Decrease movement speed
                   MOVE_STEP = max(MOVE_STEP - 0.5, 0.5)
                   print(f"Movement step decreased to {MOVE_STEP}°")

       except KeyboardInterrupt:
           print("\nProgram interrupted.")

       finally:
           cleanup()

   # ========== PROGRAM START ==========
   if __name__ == "__main__":
       print("=" * 60)
       print("RED OBJECT TRACKING WITH PAN-TILT CAMERA")
       print("=" * 60)
       print("System will:")
       print("1. Detect red objects using OpenCV")
       print("2. Move servos in 4 directions to keep object centered")
       print("3. Display tracking information")
       print("\nControls:")
       print("  Press 'q' to quit")
       print("  Press 'r' to reset servos to center")
       print("  Press '+' to increase movement speed")
       print("  Press '-' to decrease movement speed")
       print("\nTracking Logic:")
       print(f"  Deadzone: {DEADZONE_X}px around center (no movement)")
       print(f"  Movement: {MOVE_STEP}° per adjustment")
       print("  Left object → Move right (+pan)")
       print("  Right object → Move left (-pan)")
       print("  Up object → Move down (-tilt)")
       print("  Down object → Move up (+tilt)")
       print("=" * 60)

       main()


5. Explicación del Código
----------------------------------

#. ``simple_tracking(x, y)``

   Esta función decide cómo deben moverse los servos según la posición del objeto detectado.

   - Si no se detecta ningún objeto (``x`` o ``y`` es ``None``), devuelve ``(0, 0)`` (sin movimiento).
   - Si el objeto está fuera de la zona muerta, devuelve un pequeño paso de movimiento:

     - Objeto a la izquierda  → ``pan_move = +MOVE_STEP``
     - Objeto a la derecha → ``pan_move = -MOVE_STEP``
     - Objeto arriba    → ``tilt_move = -MOVE_STEP``
     - Objeto abajo  → ``tilt_move = +MOVE_STEP``

   La zona muerta evita que la cámara vibre cuando el objeto ya está cerca del centro.

#. ``update_servo_position(pan_move, tilt_move)``

   Esta función actualiza los ángulos de los servos pan/tilt de forma segura.

   - Añade el paso de movimiento a los ángulos actuales del servo.
   - Limita los ángulos a límites seguros (``PAN_MIN/PAN_MAX`` y ``TILT_MIN/TILT_MAX``).
   - Envía comandos al servo solo cuando el ángulo realmente cambia.

   Esto protege el hardware contra la sobre-rotación.

#. ``find_red_object(frame)``

   Esta función detecta el objeto rojo más grande en el fotograma de la cámara.

   Pasos principales:

   - Convierte el fotograma de BGR a HSV.
   - Crea una máscara binaria para píxeles rojos usando dos rangos HSV.
   - Limpia la máscara usando morfología (OPEN + CLOSE).
   - Encuentra contornos y selecciona el más grande.
   - Filtra las manchas pequeñas usando ``MIN_CONTOUR_AREA``.
   - Usa momentos de imagen para calcular el centro del objeto.

   Devuelve:

   - ``center_x, center_y``: la posición central del objeto (o ``None, None``)
   - ``mask``: la máscara binaria que muestra las áreas rojas

#. ``draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle)``

   Esta función dibuja información útil de seguimiento en el fotograma de video, incluyendo:

   - Cruz central
   - Rectángulo de zona muerta
   - Posición del objeto detectado
   - Ángulos del servo (pan y tilt)
   - Modo de seguimiento y tamaño del paso
   - Instrucciones de teclas

   Esto facilita ver cómo funciona el rastreador.

#. ``cleanup()``

   Esta función apaga el sistema de forma segura antes de salir.

   - Mueve los servos de vuelta a la posición central.
   - Detiene la cámara.
   - Cierra todas las ventanas de OpenCV.

   Esto evita que la cámara quede en una posición extraña.

#. ``main()``

   Este es el bucle principal de seguimiento.

   Cada iteración hace:

   - Capturar un fotograma de la cámara.
   - Detectar el objeto rojo.
   - Decidir cómo mover los servos.
   - Actualizar los ángulos del servo.
   - Dibujar información de depuración.
   - Mostrar la ventana de resultados.

   También admite controles en tiempo de ejecución:

   - ``q`` para salir
   - ``r`` para restablecer servos
   - ``+`` / ``-`` para ajustar la velocidad de seguimiento

   El programa siempre llama a ``cleanup()`` en el bloque ``finally`` para garantizar un apagado seguro.


6. Parámetros Clave y Ajuste
----------------------------

#. Parámetros de Detección de Color

   .. code-block:: python

      # HSV thresholds for red detection
      LOWER_RED1 = np.array([0, 100, 80])     # [Hue, Saturation, Value]
      UPPER_RED1 = np.array([10, 255, 255])
      LOWER_RED2 = np.array([170, 100, 80])
      UPPER_RED2 = np.array([180, 255, 255])

      # Minimum object size
      MIN_CONTOUR_AREA = 500

   Consejos de ajuste:

   - Ajusta los valores de Tono para diferentes colores
   - Aumenta los mínimos de Saturación/Valor en entornos brillantes
   - Ajusta ``MIN_CONTOUR_AREA`` según el tamaño esperado del objeto

#. Parámetros de Seguimiento

   .. code-block:: python

      # Deadzone size (pixels)
      DEADZONE_X = 50    # Larger = less jitter, but less precision
      DEADZONE_Y = 50

      # Movement step size (degrees)
      MOVE_STEP = 2      # Larger = faster tracking, but may overshoot

   Consejos de ajuste:

   - Comienza con una zona muerta más grande (50-100px) para una operación estable
   - Ajusta MOVE_STEP según los requisitos de seguimiento (0.5-5°)
   - Usa las teclas '+' y '-' para ajustar la velocidad durante la ejecución

#. Parámetros del Servo

   .. code-block:: python

      # Servo limits (calibrate for your hardware)
      PAN_MIN = -90   # Maximum left
      PAN_MAX = 90    # Maximum right
      TILT_MIN = -45  # Maximum down
      TILT_MAX = 45   # Maximum up

   .. note:: Calibra estos valores para tu hardware específico para evitar daños.


7. Problemas Comunes y Solución de Problemas
------------------------------------

* El Servo No Se Mueve

  - **Causa**: Objeto dentro de la zona muerta o MIN_CONTOUR_AREA demasiado alto
  - **Solución**: Verifica la posición del objeto, reduce MIN_CONTOUR_AREA o disminuye la zona muerta

* Movimiento del Servo Demasiado Lento

  - **Causa**: MOVE_STEP demasiado pequeño
  - **Solución**: Presiona la tecla '+' para aumentar la velocidad de movimiento

* Movimiento del Servo Demasiado Brusco

  - **Causa**: MOVE_STEP demasiado grande
  - **Solución**: Presiona la tecla '-' para disminuir la velocidad de movimiento

* Detección Falsa de Objetos

  - **Causa**: Umbrales HSV demasiado amplios o problemas de iluminación
  - **Solución**: Ajusta los rangos HSV, mejora la iluminación, aumenta MIN_CONTOUR_AREA

* Bajo FPS (Por Debajo de 10 FPS)

  - **Causa**: Sobrecarga de procesamiento o configuración de la cámara
  - **Solución**: Reduce la resolución del fotograma, simplifica el dibujo de depuración

8. Extensiones y Funciones Avanzadas
------------------------------------

#. Seguimiento de Múltiples Objetos

   .. code-block:: python

      # Instead of taking the largest contour:
      for contour in contours:
          if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
              # Track multiple objects

#. Retorno al Control Proporcional

   .. code-block:: python

      # Re-implement proportional control if desired
      KP_PAN = 0.3
      pan_move = -x_error * KP_PAN / CENTER_X

#. Ajuste de Velocidad Basado en el Tamaño del Objeto

   .. code-block:: python

      # Adjust movement speed based on object size
      object_size = cv2.contourArea(largest_contour)
      if object_size > 1000:  # Large object
          adjusted_step = MOVE_STEP * 0.5  # Move slower
      else:  # Small object
          adjusted_step = MOVE_STEP * 1.5  # Move faster

#. Registro y Grabación de Datos

   .. code-block:: python

      # Record tracking data for analysis
      with open('tracking_log.csv', 'a') as f:
          f.write(f"{time.time()},{obj_x},{obj_y},{pan_angle},{tilt_angle}\n")

#. Transmisión en Red

   .. code-block:: python

      # Stream video over network
      import socket
      # Add network streaming code


9. Resultados del Aprendizaje
---------------------

Después de completar este proyecto, deberías entender:

1. **Visión Artificial**: Detección de color en tiempo real y seguimiento de objetos
2. **Sistemas de Control**: Implementación de algoritmo de seguimiento simple de 4 direcciones
3. **Integración de Hardware**: Interfaz de cámaras y servos con Raspberry Pi
4. **Control Interactivo**: Ajuste de parámetros en tiempo real durante la operación
5. **Diseño de Sistemas**: Arquitectura simplificada de sistema de seguimiento

Este proyecto proporciona una base para aplicaciones más avanzadas como seguimiento facial, navegación autónoma y sistemas de automatización industrial. El enfoque simplificado de 4 direcciones facilita su comprensión y modificación para diferentes aplicaciones.
