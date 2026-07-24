.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

9. Tracciamento di Oggetti Rossi con Fotocamera Pan-Tilt
=========================================================

Il tracciamento di oggetti combinato con il controllo meccanico costituisce la base di molte applicazioni robotiche e di computer vision.
In questo capitolo, creeremo un sistema che **rileva oggetti rossi in tempo reale e controlla i servo pan-tilt** per mantenere l'oggetto centrato nella vista della fotocamera.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_9.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Questo estende il rilevamento colore di base in un sistema di tracciamento attivo che puo' seguire oggetti in movimento in modo autonomo.

.. image:: img/color_track.png
   :alt: Panoramica del sistema di tracciamento con fotocamera pan-tilt
   :align: center


1. Obiettivo e Approccio
------------------------

- Usare **Picamera2** per acquisire frame video in tempo reale
- Rilevare oggetti rossi usando lo **spazio colore HSV** e il filtraggio morfologico
- Implementare un algoritmo di **tracciamento semplice a 4 direzioni** basato sulla posizione dell'oggetto
- Controllare i **servo pan e tilt** per mantenere l'oggetto centrato
- Visualizzare **informazioni di debug in tempo reale** e stato del tracciamento
- Fornire **parametri regolabili** per ottimizzare il comportamento di tracciamento


2. Eseguire il Codice
---------------------

.. important::

   Prima di iniziare, assicurati:

   * Il pan-tilt sia assemblato
   * Di poter accedere al desktop di Raspberry Pi
   * Il pacchetto di codice sia installato
   * Fusion HAT+ sia installato e configurato
   * OpenCV sia installato

   Per istruzioni dettagliate, consulta :ref:`opencv_install`.

#. Apri il terminale e inserisci il seguente comando:

   .. code-block:: bash

        cd ~/ai-lab-kit/opencv_python
        python3 cv_9_track_color.py

3. Risultato dell'Esecuzione
----------------------------

Quando viene eseguito con successo, dovresti vedere:

**1. Finestra OpenCV:**

- "Red Object Tracking": Mostra il feed della fotocamera con overlay di tracciamento

**2. Elementi visivi nella finestra di tracciamento:**

- Mirino giallo al centro del frame
- Rettangolo blu che mostra la zona morta (zona di non movimento)
- Cerchio rosso che segna il centro dell'oggetto rilevato
- Linea verde che collega l'oggetto al centro del frame
- Overlay informativo in tempo reale:

  - Coordinate della posizione dell'oggetto
  - Angoli attuali dei servo
  - Modalita' di tracciamento (Simple 4-Direction)
  - Passo di movimento e impostazioni della zona morta

**3. Output della console:**

- FPS (frame al secondo)
- Posizioni correnti dei servo
- Stato del rilevamento oggetti
- Regolazioni del passo di movimento

**4. Comportamento dei servo:**

- I servo si muoveranno a passi fissi per mantenere gli oggetti rossi centrati
- Nessun movimento quando l'oggetto e' all'interno della zona morta
- I servo tornano alla posizione centrale quando viene premuto il tasto 'r'


**Controlli:**

- Premi **'q'** per uscire dal programma
- Premi **'r'** per resettare i servo alla posizione centrale
- Premi **'+'** per aumentare la velocita' di movimento
- Premi **'-'** per diminuire la velocita' di movimento

4. Codice Completo
------------------

Di seguito e' il programma Python completo per il tracciamento di oggetti rossi:

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


5. Spiegazione del Codice
-------------------------

#. ``simple_tracking(x, y)``

   Questa funzione decide come i servo dovrebbero muoversi in base alla posizione dell'oggetto rilevato.

   - Se nessun oggetto viene rilevato (``x`` o ``y`` e' ``None``), restituisce ``(0, 0)`` (nessun movimento).
   - Se l'oggetto e' fuori dalla zona morta, restituisce un piccolo passo di movimento:

     - Oggetto a sinistra → ``pan_move = +MOVE_STEP``
     - Oggetto a destra → ``pan_move = -MOVE_STEP``
     - Oggetto in alto → ``tilt_move = -MOVE_STEP``
     - Oggetto in basso → ``tilt_move = +MOVE_STEP``

   La zona morta impedisce alla fotocamera di tremare quando l'oggetto e' gia' vicino al centro.

#. ``update_servo_position(pan_move, tilt_move)``

   Questa funzione aggiorna in modo sicuro gli angoli dei servo pan/tilt.

   - Aggiunge il passo di movimento agli angoli correnti dei servo.
   - Blocca gli angoli entro i limiti di sicurezza (``PAN_MIN/PAN_MAX`` e ``TILT_MIN/TILT_MAX``).
   - Invia comandi ai servo solo quando l'angolo cambia effettivamente.

   Questo protegge l'hardware dalla rotazione eccessiva.

#. ``find_red_object(frame)``

   Questa funzione rileva l'oggetto rosso piu' grande nel frame della fotocamera.

   Passaggi principali:

   - Converte il frame da BGR a HSV.
   - Crea una maschera binaria per i pixel rossi usando due intervalli HSV.
   - Pulisce la maschera usando la morfologia (OPEN + CLOSE).
   - Trova i contorni e seleziona il piu' grande.
   - Filtra le piccole macchie usando ``MIN_CONTOUR_AREA``.
   - Usa i momenti dell'immagine per calcolare il centro dell'oggetto.

   Restituisce:

   - ``center_x, center_y``: la posizione del centro dell'oggetto (o ``None, None``)
   - ``mask``: la maschera binaria che mostra le aree rosse

#. ``draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle)``

   Questa funzione disegna informazioni utili di tracciamento sul frame video, includendo:

   - Mirino centrale
   - Rettangolo della zona morta
   - Posizione dell'oggetto rilevato
   - Angoli dei servo (pan e tilt)
   - Modalita' di tracciamento e dimensione del passo
   - Istruzioni dei tasti

   Questo rende facile vedere come funziona il tracciatore.

#. ``cleanup()``

   Questa funzione spegne in modo sicuro il sistema prima di uscire.

   - Riporta i servo alla posizione centrale.
   - Ferma la fotocamera.
   - Chiude tutte le finestre OpenCV.

   Questo impedisce che la fotocamera venga lasciata in una posizione anomala.

#. ``main()``

   Questo e' il ciclo principale di tracciamento.

   Ogni iterazione fa:

   - Acquisisce un frame dalla fotocamera.
   - Rileva l'oggetto rosso.
   - Decide come muovere i servo.
   - Aggiorna gli angoli dei servo.
   - Disegna le informazioni di debug.
   - Visualizza la finestra del risultato.

   Supporta anche controlli in esecuzione:

   - ``q`` per uscire
   - ``r`` per resettare i servo
   - ``+`` / ``-`` per regolare la velocita' di tracciamento

   Il programma chiama sempre ``cleanup()`` nel blocco ``finally`` per garantire un arresto sicuro.


6. Parametri Chiave e Regolazione
---------------------------------

#. Parametri di Rilevamento Colore

   .. code-block:: python

      # HSV thresholds for red detection
      LOWER_RED1 = np.array([0, 100, 80])     # [Hue, Saturation, Value]
      UPPER_RED1 = np.array([10, 255, 255])
      LOWER_RED2 = np.array([170, 100, 80])
      UPPER_RED2 = np.array([180, 255, 255])

      # Minimum object size
      MIN_CONTOUR_AREA = 500

   Suggerimenti per la regolazione:

   - Regola i valori di Hue per colori diversi
   - Aumenta i minimi di Saturazione/Valore in ambienti luminosi
   - Regola ``MIN_CONTOUR_AREA`` in base alla dimensione prevista dell'oggetto

#. Parametri di Tracciamento

   .. code-block:: python

      # Deadzone size (pixels)
      DEADZONE_X = 50    # Larger = less jitter, but less precision
      DEADZONE_Y = 50

      # Movement step size (degrees)
      MOVE_STEP = 2      # Larger = faster tracking, but may overshoot

   Suggerimenti per la regolazione:

   - Inizia con una zona morta piu' grande (50-100px) per un funzionamento stabile
   - Regola MOVE_STEP in base ai requisiti di tracciamento (0.5-5°)
   - Usa i tasti '+' e '-' per regolare la velocita' durante l'esecuzione

#. Parametri dei Servo

   .. code-block:: python

      # Servo limits (calibrate for your hardware)
      PAN_MIN = -90   # Maximum left
      PAN_MAX = 90    # Maximum right
      TILT_MIN = -45  # Maximum down
      TILT_MAX = 45   # Maximum up

   .. note:: Calibra questi valori per il tuo hardware specifico per prevenire danni.


7. Problemi Comuni e Risoluzione dei Problemi
---------------------------------------------

* Servo che non si Muove

  - **Causa**: Oggetto nella zona morta o MIN_CONTOUR_AREA troppo alto
  - **Soluzione**: Controlla la posizione dell'oggetto, riduci MIN_CONTOUR_AREA o diminuisci la zona morta

* Movimento del Servo Troppo Lento

  - **Causa**: MOVE_STEP troppo piccolo
  - **Soluzione**: Premi il tasto '+' per aumentare la velocita' di movimento

* Movimento del Servo Troppo Nervoso

  - **Causa**: MOVE_STEP troppo grande
  - **Soluzione**: Premi il tasto '-' per diminuire la velocita' di movimento

* Rilevamento Falso Oggetto

  - **Causa**: Soglie HSV troppo ampie o problemi di illuminazione
  - **Soluzione**: Regola gli intervalli HSV, migliora l'illuminazione, aumenta MIN_CONTOUR_AREA

* FPS Bassi (Sotto 10 FPS)

  - **Causa**: Sovraccarico di elaborazione o impostazioni della fotocamera
  - **Soluzione**: Riduci la risoluzione del frame, semplifica il disegno di debug

8. Estensioni e Funzionalita' Avanzate
---------------------------------------

#. Tracciamento Multiplo di Oggetti

   .. code-block:: python

      # Instead of taking the largest contour:
      for contour in contours:
          if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
              # Track multiple objects

#. Ritorno al Controllo Proporzionale

   .. code-block:: python

      # Re-implement proportional control if desired
      KP_PAN = 0.3
      pan_move = -x_error * KP_PAN / CENTER_X

#. Regolazione della Velocita' in Base alla Dimensione dell'Oggetto

   .. code-block:: python

      # Adjust movement speed based on object size
      object_size = cv2.contourArea(largest_contour)
      if object_size > 1000:  # Large object
          adjusted_step = MOVE_STEP * 0.5  # Move slower
      else:  # Small object
          adjusted_step = MOVE_STEP * 1.5  # Move faster

#. Registrazione e Acquisizione Dati

   .. code-block:: python

      # Record tracking data for analysis
      with open('tracking_log.csv', 'a') as f:
          f.write(f"{time.time()},{obj_x},{obj_y},{pan_angle},{tilt_angle}\n")

#. Streaming in Rete

   .. code-block:: python

      # Stream video over network
      import socket
      # Add network streaming code


9. Risultati di Apprendimento
-----------------------------

Dopo aver completato questo progetto, dovresti comprendere:

1. **Computer Vision**: Rilevamento colore in tempo reale e tracciamento oggetti
2. **Sistemi di Controllo**: Implementazione di un algoritmo di tracciamento semplice a 4 direzioni
3. **Integrazione Hardware**: Interfacciamento di fotocamere e servo con Raspberry Pi
4. **Controllo Interattivo**: Regolazione dei parametri in tempo reale durante il funzionamento
5. **Progettazione di Sistema**: Architettura semplificata del sistema di tracciamento

Questo progetto fornisce una base per applicazioni piu' avanzate come il tracciamento facciale, la navigazione autonoma e i sistemi di automazione industriale. L'approccio semplificato a 4 direzioni rende piu' facile comprendere e modificare per diverse applicazioni.