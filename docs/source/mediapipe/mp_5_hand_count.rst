.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. Conteggio dei Gesti della Mano
==============================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

Nella sezione precedente, abbiamo implementato il rilevamento
delle mani in tempo reale e la visualizzazione dei landmark.

Questa sezione estende tale funzionalita utilizzando
le posizioni dei landmark delle dita per contare il numero
di dita alzate (0–5).

Analizzando le posizioni relative delle punte delle dita
e delle loro corrispondenti articolazioni, possiamo determinare
se ogni dito e esteso.

.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

Il programma segue questi passaggi:

1. Inizializza il modello MediaPipe Hands.
2. Acquisisce i fotogrammi video dalla fotocamera del Raspberry Pi.
3. Rileva 21 landmark della mano in tempo reale.
4. Confronta le coordinate della punta delle dita con le loro articolazioni prossimali.
5. Determina se ogni dito e esteso.
6. Conta il numero di dita alzate.
7. Visualizza il risultato sul fotogramma video.

Questo metodo e:

- Leggero ed efficiente
- Adatto per Raspberry Pi
- Una base per il controllo gestuale e i sistemi interattivi

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. Dopo aver eseguito il programma, si apre una finestra intitolata "Show Video" che mostra il flusso video in diretta.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Quando una mano appare davanti alla fotocamera:

   - MediaPipe rileva la mano in tempo reale.
   - 21 punti landmark e linee di connessione vengono disegnati sulla mano.
   - Il programma analizza le posizioni della punta delle dita e delle articolazioni.
   - Viene calcolato il numero di dita alzate (0–5).

   Il conteggio delle dita rilevato viene visualizzato nell'angolo superiore sinistro
   dello schermo come:

      Fingers: X

   Mentre estendi o pieghi le dita, il numero si aggiorna
   istantaneamente in tempo reale.

   Se non viene rilevata alcuna mano, viene mostrato solo il normale flusso video
   senza conteggio delle dita.

   Premi ``q`` per uscire dal programma.
   La fotocamera si ferma e la finestra OpenCV si chiude automaticamente.



-----------------------------
4. Codice Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2 
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections on the frame
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
               )


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

In ogni iterazione del ciclo, determina se ciascuno dei 5 dita e esteso e conta il numero di dita estese. Per esempio:

- ✊ Tutte le dita chiuse → Conteggio 0
- ☝️ Indice esteso → Conteggio 1
- ✌️ Indice + Medio estesi → Conteggio 2
- 🖐️ Tutte e cinque le dita aperte → Conteggio 5

--------------------------------------------------------------
5. Logica di Rilevamento ed Estensioni
--------------------------------------------------------------

MediaPipe Hands restituisce 21 landmark.
Usiamo le posizioni della punta delle dita e delle articolazioni per determinare
se ogni dito e esteso.

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → Indici della punta delle dita
  (Pollice=4, Indice=8, Medio=12, Anulare=16, Mignolo=20)

- ``finger_dips`` → Articolazioni prossimali corrispondenti
  (Pollice=2, Indice=6, Medio=10, Anulare=14, Mignolo=18)

------------------------------------------------------------

Logica di conteggio delle dita:

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

Spiegazione della logica:

- **Pollice** → Confronta ``tip.x`` e ``dip.x`` (per la mano destra).
- **Altre dita** → Confronta ``tip.y`` e ``dip.y``.
- Se la punta del dito e sopra (o verso l'esterno rispetto) l'articolazione,
  il dito e considerato esteso.
- Ogni condizione soddisfatta aumenta il conteggio di ``+1``.

------------------------------------------------------------

Suggerimenti per l'estensione:

- Per supportare sia la mano sinistra che quella destra,
  usa ``hands_detected.multi_handedness`` per determinare il tipo di mano,
  e inverti il confronto sull'asse x del pollice di conseguenza.

- Questa logica puo essere estesa per implementare:

  - Riconoscimento del gesto OK
  - Rilevamento del pollice in su
  - Interazione sasso-carta-forbice
  - Controlli personalizzati basati sui gesti

------------------------------------------------------------
6. Risoluzione dei Problemi
------------------------------------------------------------

- Rilevamento del pollice impreciso

  Il rilevamento del pollice potrebbe essere impreciso perche la logica differisce per la mano sinistra e destra. Il confronto orizzontale utilizzato per il pollice dipende dall'orientamento della mano.

  Usa ``multi_handedness`` per determinare se la mano rilevata e sinistra o destra, e regola la logica di rilevamento del pollice di conseguenza.

- Rilevamento instabile

  Se il conteggio delle dita appare instabile, l'illuminazione potrebbe essere insufficiente o lo sfondo potrebbe essere disordinato.

  Migliora le condizioni di illuminazione e usa uno sfondo semplice per aumentare la stabilita del rilevamento.

- Latenza elevata

  Se la risposta e lenta, la risoluzione potrebbe essere troppo alta o la CPU potrebbe essere sovraccarica.

  Riduci la risoluzione (per esempio, 320×240) e chiudi i processi di background non necessari. Puoi anche semplificare la logica di conteggio delle dita se necessario.


-----------------------------
7. Riepilogo
-----------------------------

- Utilizzando MediaPipe Hands, possiamo implementare rapidamente il **riconoscimento dei gesti in tempo reale**.
- Questa sezione ha implementato il **conteggio dei gesti numerici** basato sulle posizioni della punta delle dita, gettando le basi per il riconoscimento personalizzato dei gesti.
- Adattandosi per le mani sinistra/destra ed espandendo le regole di giudizio, si possono ottenere scenari interattivi piu complessi.