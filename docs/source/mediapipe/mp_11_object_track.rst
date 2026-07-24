.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. Tracciamento Oggetti con Fotocamera Pan-Tilt
=================================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

In questo capitolo, estendiamo il rilevamento oggetti di MediaPipe
per costruire un semplice **sistema di tracciamento oggetti**
utilizzando una piattaforma pan-tilt con servo.

Il sistema rileva un oggetto target specificato
(per esempio, una "banana")
e regola automaticamente due servo
per mantenere l'oggetto centrato nella visuale della fotocamera.

.. image:: img/mp_object_track.png
   :width: 500
   :align: center

This project combines:

- Rilevamento oggetti in tempo reale
- Controllo dei servo motori
- Logica di tracciamento proporzionale
- Sovrapposizione di feedback visivo

Dimostra come la visione artificiale puo guidare direttamente
l'hardware fisico in tempo reale.


------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

Il sistema di tracciamento segue questi passaggi:

1. Inizializza i servo pan e tilt alla posizione centrale.
2. Configura la fotocamera del Raspberry Pi per lo streaming video.
3. Carica il modello EfficientDet Lite0 per il rilevamento oggetti.
4. Rileva gli oggetti in ogni fotogramma usando MediaPipe Tasks.
5. Identifica l'oggetto target (es., "banana").
6. Calcola l'offset dell'oggetto rispetto al centro del fotogramma.
7. Regola gli angoli dei servo usando il controllo proporzionale.
8. Visualizza guide di tracciamento e stato sullo schermo.

Questo esempio mostra come il feedback basato sulla visione
possa essere utilizzato per controllare dinamicamente il movimento hardware.

------------------------
3. Eseguire il Codice
------------------------

.. important::


   Before you start, make sure:

   * The pan-tilt is assembled
   * You can access the Raspberry Pi desktop
   * The code package is installed
   * Fusion HAT+ is installed and configured
   * OpenCV is installed

   For detailed instructions, see :ref:`opencv_install`.

#. Apri il terminale e inserisci il seguente comando:

   .. code-block:: bash

       sudo python3 ~/ai-lab-kit/mediapipe/mp_track_object.py

#. Dopo aver eseguito il programma, si apre la finestra della fotocamera e inizia il rilevamento oggetti in tempo reale.

   .. raw:: html
   
         <video width="300" loop muted controls>
             <source src="../_static/video/object_tracking.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
   
   Il sistema cerca l'oggetto target specificato (default: ``banana``).
   Un mirino giallo viene visualizzato al centro dello schermo come punto di riferimento.

   Quando l'oggetto target appare nel fotogramma:

   - MediaPipe rileva l'oggetto usando il modello EfficientDet Lite0.
   - Viene calcolato il centro del riquadro di delimitazione rilevato.
   - Se l'oggetto e fuori dalla zona morta centrale, i servo pan e tilt si muovono passo dopo passo.
   - La fotocamera ruota fisicamente per mantenere l'oggetto vicino al centro del fotogramma.
   - Un riquadro di tracciamento verde viene disegnato intorno all'oggetto.
   - Lo schermo mostra:

     - ``Tracking banana`` (stato)
     - Angoli attuali dei servo (Pan / Tilt)

   Quando l'oggetto non viene rilevato:

   - I servo smettono di muoversi.
   - Il testo di stato cambia in ``No banana found`` (visualizzato in rosso).

   La logica di tracciamento usa un semplice controllo deadzone a 4 direzioni:
   i servo si muovono solo quando l'oggetto e sufficientemente lontano dal centro,
   prevenendo vibrazioni.

   Premi ``q`` per fermare il programma.

   All'uscita:

   - Entrambi i servo tornano alla posizione centrale.
   - La fotocamera si ferma.
   - La finestra di visualizzazione si chiude.
   - Viene stampato un messaggio: ``Tracking stopped. Servos centered.``

-----------------------------
4. Codice Completo
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
5. Spiegazione del Codice
-----------------------------

**Sezione di Configurazione**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET``: Categoria dell'oggetto da tracciare (deve essere nelle classi del dataset COCO);
- ``W, H``: Risoluzione della fotocamera - bilanciata tra velocita e dettaglio;
- ``CX, CY``: Coordinate del centro del fotogramma per il riferimento di tracciamento;
- ``SCORE_THRESHOLD``: Confidenza minima per un rilevamento valido;
- ``DEADZONE``: Distanza dal centro prima che inizi il movimento del servo (riduce le vibrazioni).

**Inizializzazione dei Servo**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` e ``Servo(3)`` corrispondono ai canali su Fusion HAT;
- ``.angle(0)`` centra i servo nella posizione a 0°;
- ``time.sleep(1)`` garantisce che i servo raggiungano la posizione prima di continuare.

**Configurazione della Fotocamera**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- Utilizza la libreria Picamera2 per la moderna API della fotocamera;
- Il formato ``XRGB8888`` fornisce canali colore a 8 bit;
- ``time.sleep(2)`` permette al sensore della fotocamera di stabilizzarsi.

**Rilevatore MediaPipe**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- Carica il modello EfficientDet Lite0 dalla stessa directory;
- ``RunningMode.VIDEO`` ottimizzato per l'elaborazione continua dei fotogrammi;
- ``detect_for_video()`` richiede un timestamp per ogni fotogramma.

**Funzione di Tracciamento**

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

- Controllo proporzionale semplice (non un vero PID);
- La zona morta previene le vibrazioni del servo da piccoli movimenti;
- Restituisce valori di movimento di -1, 0 o 1 per ogni asse.

**Elaborazione del Ciclo Principale**

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

1. Converte il fotogramma in formato immagine MediaPipe;
2. Esegue il rilevamento oggetti con il timestamp corrente;
3. Cerca tra i rilevamenti l'oggetto target (senza distinzione maiuscole/minuscole);
4. Calcola le coordinate del centro dell'oggetto.

**Logica di Controllo dei Servo**

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

1. Ottiene i comandi di movimento dalla funzione di tracciamento;
2. Aggiorna gli accumulatori di posizione;
3. Limita le posizioni ai limiti meccanici;
4. Invia i nuovi angoli ai servo.

**Feedback Visivo**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)
   
   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)
   
   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- Riquadro verde: Oggetto attualmente tracciato;
- Mirino giallo: Riferimento del centro del fotogramma;
- Testo di stato: Stato del tracciamento e angoli dei servo.

**Routine di Pulizia**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- Riporta i servo alla posizione centrale;
- Ferma l'acquisizione della fotocamera;
- Chiude le finestre OpenCV;
- Viene eseguito anche se si verifica un errore (``try...finally``).

------------------------------------------------------
6. Opzioni di Configurazione
------------------------------------------------------

**Cambiare l'Oggetto Target**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**Regolare i Parametri di Tracciamento**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive

   # Faster, more responsive tracking
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**Limiti di Escursione dei Servo**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**Ottimizzazione delle Prestazioni**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing

   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. Considerazioni sulle Prestazioni
------------------------------------------------------

.. list-table:: Fattori di Prestazione
   :header-rows: 1

   * - Fattore
     - Effetto sulle Prestazioni
     - Raccomandazione
   * - Risoluzione della Fotocamera
     - Piu alta = rilevamento piu lento
     - 640x480 buon equilibrio
   * - Soglia di Rilevamento
     - Piu bassa = piu rilevamenti ma piu falsi positivi
     - 0.3-0.5 ottimale
   * - Dimensione Zona Morta
     - Piu grande = piu fluido ma meno reattivo
     - 40-60 pixel
   * - Velocita del Servo
     - Piu veloce = piu reattivo ma potrebbe superare il target
     - Considerare il controllo dell'accelerazione
   * - Dimensione del Modello
     - Lite0 piu veloce, Lite2 piu preciso
     - Lite0 per tracciamento in tempo reale

**Prestazioni Previste:**

- **Raspberry Pi 4:** 8-15 FPS con 640x480
- **Latenza di Rilevamento:** 100-200ms
- **Tempo di Risposta del Servo:** 50-100ms per grado
- **Latenza Totale del Sistema:** 200-400ms

------------------------------------------------------
8. Guida alla Risoluzione dei Problemi
------------------------------------------------------

.. list-table:: Problemi Comuni e Soluzioni
   :header-rows: 1

   * - Problema
     - Causa Possibile
     - Soluzione
   * - Nessun rilevamento oggetti
     - Oggetto non nelle classi COCO
     - Usa nomi di oggetti supportati
   * - Movimento servo a scatti
     - Zona morta troppo piccola
     - Aumenta DEADZONE a 60-80
   * - Superamento del target del servo
     - Passo di movimento troppo grande
     - Cambia pan_move da 1 a 0.5
   * - Basso frame rate
     - Risoluzione troppo alta
     - Riduci a 320x240
   * - Fotocamera non funziona
     - Fotocamera non abilitata
     - Esegui ``sudo raspi-config``
   * - I servo non si muovono
     - Cablaggio o alimentazione errati
     - Controlla connessioni e alimentazione
   * - Oggetto perso frequentemente
     - Soglia troppo alta
     - Riduci SCORE_THRESHOLD a 0.2
   * - Direzione di tracciamento errata
     - Orientamento del servo invertito
     - Inverti i segni di pan_move

**Suggerimenti per il Debug:**

1. **Testare i servo separatamente:**

   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **Verificare il rilevamento oggetti:**

   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **Controllare le coordinate dell'oggetto:**

   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **Monitorare il frame rate:**

   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. Modifiche Avanzate
------------------------------------------------------

**1. Implementazione del Controllo PID**

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

**2. Tracciamento di Oggetti Multipli**

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

**3. Velocita Proporzionale alla Distanza**

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

**4. Memoria dell'Oggetto (Tracciamento Inerziale)**

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
10. Applicazioni ed Estensioni
------------------------------------------------------

**Applicazioni Educative:**

- Principi di robotica e automazione
- Fondamenti di visione artificiale
- Sistemi di controllo (P vs PID)
- Progettazione di sistemi in tempo reale

**Applicazioni Pratiche:**

- Auto-tracciamento per telecamere di sicurezza
- Automazione della fotocamera per videoconferenze
- Osservazione della fauna selvatica
- Tecnologia assistiva per il tracciamento

**Progetti di Estensione:**

1. **Interfaccia Web:** Controllo remoto tramite browser
2. **Posizioni Preimpostate:** Salva/carica posizioni di tracciamento comuni
3. **Apprendimento Oggetti:** Addestra su oggetti personalizzati
4. **Multi-telecamera:** Coordina piu unita di tracciamento
5. **Integrazione Cloud:** Carica dati di tracciamento per l'analisi
6. **Feedback Audio:** Annuncia lo stato del tracciamento
7. **Controllo Gestuale:** Usa i gesti delle mani per controllare il tracciamento

-----------------------------
11. Sicurezza e Buone Pratiche
------------------------------

1. **Sicurezza Meccanica:**

   - Fissare tutte le parti mobili
   - Utilizzare la gestione dei cavi
   - Evitare punti di pizzicamento
   - Impostare limiti di angolo ragionevoli

2. **Sicurezza Elettrica:**

   - Utilizzare alimentazione esterna per i servo
   - Garantire una corretta messa a terra
   - Evitare il sovraccarico dell'alimentazione
   - Utilizzare cavi di sezione appropriata

3. **Sicurezza Software:**

   - Includere sempre il centraggio dei servo all'uscita
   - Implementare un meccanismo di arresto di emergenza
   - Registrare gli errori per il debug
   - Validare input e limiti

4. **Sicurezza Operativa:**

   - Tenersi lontani dal meccanismo in movimento
   - Monitorare il surriscaldamento
   - Controlli di manutenzione regolari
   - Avere capacita di override manuale

-----------------------------
12. Riepilogo
-----------------------------

Questo capitolo ha dimostrato un sistema completo di tracciamento oggetti utilizzando:

1. **MediaPipe Tasks** per il rilevamento oggetti affidabile
2. **Servo pan-tilt** per il tracciamento fisico
3. **Controllo proporzionale semplice** per la logica di movimento
4. **OpenCV** per feedback visivo e visualizzazione

Il sistema fornisce una base per applicazioni di tracciamento piu avanzate e dimostra concetti chiave nella visione artificiale in tempo reale, nei sistemi di controllo e nella programmazione Python embedded.

Modificando l'oggetto target, regolando i parametri ed estendendo la logica di controllo, questo sistema puo essere adattato per varie applicazioni, dalle dimostrazioni educative alle soluzioni di automazione pratica.

**Prossimi Passi:**

- Implementare il controllo PID per un tracciamento piu fluido
- Aggiungere memoria dell'oggetto per la gestione dell'occlusione temporanea
- Creare un'interfaccia web per il monitoraggio remoto
- Integrare con sistemi di automazione domestica
- Addestrare modelli di rilevamento oggetti personalizzati
