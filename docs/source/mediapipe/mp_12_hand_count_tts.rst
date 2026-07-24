.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_tts:

12. Aggiungere la Diffusione Vocale TTS ai Progetti MediaPipe
============================================================

-----------------------------------------------------------------
1. Panoramica
-----------------------------------------------------------------

In :ref:`mp_hand_count` (Sezione 5), abbiamo costruito un programma
di conteggio dei gesti della mano che mostra il numero di dita alzate sullo schermo.

In questa sezione, faremo un passo avanti:
**aggiungeremo la diffusione vocale Text-to-Speech (TTS)**
in modo che il Raspberry Pi possa *parlare* ad alta voce il conteggio delle dita rilevato —
rendendo il progetto piu interattivo e accessibile.

.. image:: img/mp_hand_count.png
   :align: center

Questa lezione non riguarda solo il conteggio delle dita —
insegna un **modello generale** per aggiungere TTS a *qualsiasi*
progetto MediaPipe o OpenCV.

Alla fine di questa lezione, saprai come:

- Inizializzare e configurare il motore TTS di Fusion HAT+
- Attivare il TTS con la pressione di un tasto con protezione debounce
- Aggiungere feedback visivo mentre il sistema parla
- Applicare questo modello ai tuoi progetti di visione artificiale


-----------------------------------------------------------------
2. Come Funziona
-----------------------------------------------------------------

Il programma si basa sul pipeline di conteggio delle mani e aggiunge un livello TTS
che viene attivato dalla pressione di un tasto:

1. Inizializza **MediaPipe Hands** per il rilevamento delle mani in tempo reale.
2. Inizializza il **motore TTS Fusion HAT+** (Espeak).
3. Acquisisce i fotogrammi video e rileva le dita (come prima).
4. Attende che l'utente prema il tasto ``t``.
5. Alla pressione del tasto, converte il conteggio corrente delle dita in un messaggio parlato.
6. Usa la **logica debounce** per prevenire attivazioni rapide ripetute.
7. Mostra un **flash visivo** sullo schermo mentre il TTS parla.
8. Il parlato viene riprodotto attraverso l'altoparlante di Fusion HAT+.

L'idea chiave del progetto e:

    *Il TTS viene aggiunto come livello non bloccante —*
    il rilevamento viene eseguito continuamente e il parlato viene attivato solo
    quando l'utente lo richiede.

Questo modello mantiene fluido il pipeline video aggiungendo
l'output vocale su richiesta.


-----------------------------------------------------------------
3. Il Modulo TTS di Fusion HAT+
-----------------------------------------------------------------

La libreria ``fusion_hat`` fornisce un'interfaccia semplice e unificata
per diversi motori TTS. In questo progetto, usiamo **Espeak** —
un motore offline leggero che funziona bene su Raspberry Pi.

**Utilizzo di base:**

.. code-block:: python

    from fusion_hat.tts import Espeak

    # Create TTS instance
    tts = Espeak()

    # Configure voice
    tts.set_amp(200)       # volume: 0-200 (default 100)
    tts.set_speed(150)     # speed: 80-260 (default 150)
    tts.set_pitch(80)      # pitch: 0-99 (default 80)

    # Speak
    tts.say("Hello!")

Tre parametri ti permettono di personalizzare la voce:

- **amp** (ampiezza) — controlla il volume. Piu alto = piu forte.
- **speed** — velocita di eloquio in parole al minuto. 150 e normale.
- **pitch** — tono della voce. 80 e il default; valori piu bassi suonano piu gravi.

.. note::

   Fusion HAT+ supporta anche **Piper** (neurale, offline)
   e **OpenAI TTS** (online, voci naturali).
   Vedi :ref:`tts_piper_openai` per opzioni piu avanzate.


-----------------------------------------------------------------
4. Progettazione Chiave: Aggiungere TTS a un Ciclo Video
-----------------------------------------------------------------

Quando si aggiunge TTS a un pipeline video in tempo reale, ci sono alcune
importanti considerazioni di progettazione. Esaminiamole una per una.

--------------------------------------------------
4.1 Attivazione tramite Pressione di un Tasto
--------------------------------------------------

Invece di parlare ad ogni fotogramma (che sarebbe caotico),
usiamo un tasto della tastiera come trigger:

.. code-block:: python

    key = cv2.waitKey(1) & 0xff
    if key == ord('t'):
        tts.say(message)

Il tasto ``t`` e stato scelto perche e facile da ricordare
(*t* per *talk*). Puoi usare qualsiasi tasto — ``space`` per
controllo a mani libere, o un pulsante GPIO per input fisico.

--------------------------------------------------
4.2 Protezione Debounce
--------------------------------------------------

Senza protezione, tenere premuto il tasto ``t`` attiverrebbe
il TTS decine di volte al secondo, sovrapponendo il parlato e
rendendolo incomprensibile.

**Soluzione: debounce basato sul tempo.**

.. code-block:: python

    DEBOUNCE_INTERVAL = 1.5  # seconds
    last_tts_time = 0

    # In the loop:
    if key == ord('t'):
        now = time.time()
        if now - last_tts_time > DEBOUNCE_INTERVAL:
            last_tts_time = now
            tts.say(message)

Dopo ogni attivazione TTS, ulteriori attivazioni vengono ignorate
per 1.5 secondi. Questo da al parlato abbastanza tempo per terminare
prima che inizi il successivo.

--------------------------------------------------
4.3 Costruzione del Messaggio
--------------------------------------------------

Il conteggio delle dita (un intero) deve essere convertito in
una frase dal suono naturale:

.. code-block:: python

    if total_fingers == 0:
        message = "no fingers detected"
    elif total_fingers == 1:
        message = "one finger detected"
    else:
        message = f"{total_fingers} fingers detected"

Usare ``"one"`` invece di ``"1"`` garantisce che Espeak lo pronunci
naturalmente. Per numeri maggiori di uno, la forma numerica
funziona bene con Espeak.

--------------------------------------------------
4.4 Feedback Visivo (Flash del Bordo Verde)
--------------------------------------------------

Mentre il sistema parla, aggiungiamo un indicatore visivo
in modo che l'utente sappia che il parlato e in corso:

.. code-block:: python

    tts_flash_until = now + 1.0   # flash for 1 second

    # Later in the loop:
    if tts_triggered and time.time() < tts_flash_until:
        cv2.rectangle(frame, (0, 0), (w-1, h-1), (0, 255, 0), 8)
        cv2.putText(frame, "Speaking...", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

Un **bordo verde** appare intorno al fotogramma e un'etichetta
**"Speaking..."** viene mostrata. Entrambi scompaiono automaticamente
dopo 1 secondo.

Questo ciclo di feedback e importante perche:

- Il TTS richiede un momento per completarsi — l'utente deve sapere
  che il sistema ha ricevuto il suo comando.
- Il bordo scompare quando finito, quindi non interferisce
  con l'uso normale.


-----------------------------------------------------------------
5. Eseguire il Codice
-----------------------------------------------------------------

.. important::

   Before you start, make sure:

   * The Fusion HAT+ is assembled and the speaker is connected
   * You can access the Raspberry Pi desktop
   * The code package is installed
   * MediaPipe and OpenCV are installed

   For detailed instructions, see :ref:`mediapipe_install` and :ref:`opencv_install`.

#. Apri il terminale e inserisci il seguente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts.py

#. Dopo aver eseguito il programma:

   - Si apre una finestra intitolata "MediaPipe Hand Count + TTS",
     che mostra il flusso video in diretta.
   - Tieni la mano davanti alla fotocamera — il conteggio delle dita appare
     nell'angolo superiore sinistro.
   - *Premi il tasto* ``t`` — il sistema pronuncia il conteggio
     corrente delle dita attraverso l'altoparlante di Fusion HAT+.
   - Un bordo verde lampeggia sullo schermo mentre parla.

   .. hint::

      Prova a mostrare diversi numeri di dita e premi ``t``
      ogni volta. Dovresti sentire: "one finger detected",
      "three fingers detected", ecc.

   Premi ``q`` per uscire dal programma.


--------------------------------------------------
6. Codice Completo
--------------------------------------------------

.. code-block:: python

   """
   MediaPipe Hand Detection + TTS Demo
   ====================================
   Detects fingers via webcam in real time. Press the 't' key to speak the
   current finger count using TTS.

   Usage:
       python mp_hand_count_tts.py

   Controls:
       't'  - speak the detected finger count via TTS
       'q'  - quit
   """

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   from fusion_hat.tts import Espeak
   import time


   # ======================== Init TTS ========================
   tts = Espeak()
   tts.set_amp(200)       # volume 0-200, default 100
   tts.set_speed(150)     # speed 80-260, default 150
   tts.set_pitch(80)      # pitch 0-99, default 80

   # ======================== Init MediaPipe Hands ========================
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

   # ======================== Init Camera ========================
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   # ======================== Constants ========================
   # Finger tip and dip landmark indices
   FINGER_TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
   FINGER_DIPS = [2, 6, 10, 14, 18]   # corresponding middle joints

   # Minimum interval (seconds) between TTS triggers to avoid spamming
   DEBOUNCE_INTERVAL = 1.5

   print("=" * 55)
   print("  MediaPipe Hand Count + TTS")
   print("  Press 't' to speak count | 'q' to quit")
   print("=" * 55)

   # ======================== Main Loop ========================
   last_tts_time = 0          # timestamp of last TTS trigger
   tts_triggered = False      # whether TTS was just fired (for visual flash)
   tts_flash_until = 0        # how long the flash should last

   while True:
       # ---- 1. Capture frame ----
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # ---- 2. Convert to RGB for MediaPipe ----
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       # ---- 3. Convert back to BGR for OpenCV display ----
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # ---- 4. Count fingers (right hand only) ----
       total_fingers = 0

       if hands_detected.multi_hand_landmarks:
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               # Draw hand skeleton
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Thumb: extended when x_tip > x_dip (right hand)
               if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
                   finger_count += 1

               # Other four fingers: tip is above dip when extended (smaller y)
               for i in range(1, 5):
                   if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
                       finger_count += 1

               total_fingers += finger_count

       # ---- 5. Display finger count on screen ----
       display_text = f"Fingers: {total_fingers}"
       cv2.putText(frame, display_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

       # ---- 6. Key handling ----
       key = cv2.waitKey(1) & 0xff

       # 't' key: trigger TTS (with debounce)
       if key == ord('t'):
           now = time.time()
           if now - last_tts_time > DEBOUNCE_INTERVAL:
               last_tts_time = now
               tts_triggered = True
               tts_flash_until = now + 1.0  # flash for 1 second

               if total_fingers == 0:
                   message = "no fingers detected"
               elif total_fingers == 1:
                   message = "one finger detected"
               else:
                   message = f"{total_fingers} fingers detected"

               print(f"[TTS] {message}")
               tts.say(message)

       # 'q' key: quit
       if key == ord('q'):
           break

       # ---- 7. Visual feedback while speaking (green border flash) ----
       if tts_triggered and time.time() < tts_flash_until:
           h, w = frame.shape[:2]
           thickness = 8
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 255, 0), thickness)
           cv2.putText(frame, "Speaking...", (10, 75),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
       else:
           tts_triggered = False

       # ---- 8. Show controls hint at bottom ----
       cv2.putText(frame, "Press 't' to speak count | 'q' to quit",
                   (10, frame.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

       # ---- 9. Show frame ----
       cv2.imshow("MediaPipe Hand Count + TTS", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")


--------------------------------------------------
7. Spiegazione del Codice
--------------------------------------------------

Esaminiamo il codice sezione per sezione, concentrandoci su
cosa e nuovo rispetto al programma di conteggio delle dita di base.

--------------------------------------------------
7.1 Importazioni e Inizializzazione
--------------------------------------------------

.. code-block:: python

   from fusion_hat.tts import Espeak
   import time

   tts = Espeak()
   tts.set_amp(200)
   tts.set_speed(150)
   tts.set_pitch(80)

Due nuove importazioni e un blocco di inizializzazione TTS sono le prime
aggiunte. ``Espeak()`` crea il motore TTS, e le tre
chiamate ``set_*`` configurano la voce.

``import time`` e necessario per la temporizzazione del debounce.

--------------------------------------------------
7.2 Costanti Debounce e Variabili di Stato
--------------------------------------------------

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5

   last_tts_time = 0
   tts_triggered = False
   tts_flash_until = 0

Vengono introdotte quattro nuove variabili:

- ``DEBOUNCE_INTERVAL`` — previene lo spam del TTS (secondi).
- ``last_tts_time`` — registra quando il TTS e stato attivato l'ultima volta.
- ``tts_triggered`` — flag per l'effetto flash visivo.
- ``tts_flash_until`` — timestamp di quando il flash dovrebbe terminare.

--------------------------------------------------
7.3 Gestione dei Tasti con Debounce
--------------------------------------------------

.. code-block:: python

   key = cv2.waitKey(1) & 0xff

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           tts_triggered = True
           tts_flash_until = now + 1.0

           if total_fingers == 0:
               message = "no fingers detected"
           elif total_fingers == 1:
               message = "one finger detected"
           else:
               message = f"{total_fingers} fingers detected"

           tts.say(message)

Questa e l'aggiunta TTS principale. Analizziamola:

1. **Rilevamento del tasto** — ``ord('t')`` controlla se ``t`` e stato premuto.

2. **Cancello debounce** — ``time.time() - last_tts_time > DEBOUNCE_INTERVAL``
   garantisce che siano passati almeno 1.5 secondi dall'ultima attivazione.
   Se non e passato abbastanza tempo, la pressione del tasto viene ignorata.

3. **Aggiornamento dello stato** — Quando il cancello viene superato, registriamo
   l'ora corrente e impostiamo il timer del flash.

4. **Costruzione del messaggio** — Il conteggio delle dita viene convertito in
   una frase leggibile.

5. **Parlato** — ``tts.say(message)`` invia il testo all'altoparlante.

.. note::

   ``tts.say()`` is **non-blocking** — the program continues
   processing video frames while speech plays in the background.

--------------------------------------------------
7.4 Feedback Visivo
--------------------------------------------------

.. code-block:: python

   if tts_triggered and time.time() < tts_flash_until:
       h, w = frame.shape[:2]
       thickness = 8
       cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 255, 0), thickness)
       cv2.putText(frame, "Speaking...", (10, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
   else:
       tts_triggered = False

- A green border (8 pixels thick) is drawn around the entire frame.
- A yellow "Speaking..." label appears below the finger count.
- Both persist for 1 second, then disappear automatically.
- When the flash timer expires, ``tts_triggered`` resets to ``False``,
  ready for the next trigger.

Questo modello e riutilizzabile — puoi aggiungere lo stesso feedback
a qualsiasi progetto che attiva il TTS.


-----------------------------------------------------------------
8. Idee di Estensione: Applicare Questo Modello ad Altri Progetti
-----------------------------------------------------------------

Il modello di integrazione TTS che hai imparato qui e **generico**.
Puoi aggiungere la diffusione vocale a qualsiasi progetto MediaPipe, OpenCV o YOLO
seguendo questi passaggi:

**Passo 1: Importare e inizializzare il TTS**

.. code-block:: python

   from fusion_hat.tts import Espeak
   tts = Espeak()
   tts.set_amp(200)

**Passo 2: Aggiungere variabili debounce (prima del ciclo)**

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5
   last_tts_time = 0

**Passo 3: Aggiungere TTS attivato da tasto (dentro il ciclo)**

.. code-block:: python

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           # Build your message from detection results
           tts.say(your_message)

Ecco alcune idee per applicare questo modello:

- **MediaPipe Face Detection** (:ref:`mp_face`)
  → "Face detected at center of frame"

- **MediaPipe Pose** (:ref:`mp_pose`)
  → "Both arms raised" or "Squat detected — good form!"

- **OpenCV Color Tracking** (:ref:`play_with_opencv`)
  → "Red object moving left" or "Target locked"

- **YOLO Object Detection** (:ref:`play_with_yolo`)
  → "Person detected" or "Two cars in view"

- **Hardware Integration**
  → Replace the ``t`` key with a GPIO button press via
  ``fusion_hat`` for a completely hands-free experience.


-----------------------------------------------------------------
9. Risoluzione dei Problemi
-----------------------------------------------------------------

- **Nessun suono dall'altoparlante**

  Assicurati che l'altoparlante di Fusion HAT+ sia collegato correttamente e
  che il volume non sia in muto. Prova a eseguire un semplice test TTS:

  .. code-block:: bash

     sudo python3 -c "from fusion_hat.tts import Espeak; Espeak().say('test')"

  Se senti "test", il motore TTS funziona.

- **Il TTS si attiva troppe volte quando si tiene premuto il tasto**

  Aumenta ``DEBOUNCE_INTERVAL`` a un valore piu grande,
  per esempio ``2.0`` o ``2.5`` secondi.

  Se vuoi solo una singola attivazione per pressione del tasto
  (nessuna ripetizione quando tenuto premuto), traccia lo stato del tasto tra i fotogrammi
  e attiva solo sul *fronte di salita* (transizione del tasto da
  non premuto a premuto).

- **Il parlato e troppo veloce o poco chiaro**

  Abbassa la velocita: ``tts.set_speed(120)``.

  Regola il tono per chiarezza: ``tts.set_pitch(70)``.

- **Il parlato si sovrappone al parlato precedente**

  Espeak su Fusion HAT+ mette in coda il parlato per impostazione predefinita.
  Se vuoi cancellare il parlato in corso prima di iniziarne uno nuovo,
  puoi aggiungere un piccolo ritardo o usare un motore TTS diverso.

- **Il flash visivo non appare**

  Controlla che ``tts_triggered`` sia impostato su ``True`` all'interno del
  blocco debounce e che ``tts_flash_until`` sia impostato su
  ``time.time() + 1.0``.


-----------------------------------------------------------------
10. Riepilogo
-----------------------------------------------------------------

- Questa lezione ha dimostrato come **aggiungere la diffusione vocale TTS**
  a un progetto di visione artificiale MediaPipe.
- Il motore ``Espeak`` di Fusion HAT+ fornisce una soluzione TTS semplice
  e offline su Raspberry Pi.
- **Modelli di progettazione chiave** trattati:

  - Attivazione del TTS tramite pressione di un tasto (non ad ogni fotogramma)
  - **Protezione debounce** per prevenire la sovrapposizione del parlato
  - **Feedback visivo** (flash del bordo verde) per la consapevolezza dell'utente
  - Conversione dei risultati del rilevamento in messaggi vocali naturali

- Questi modelli sono **indipendenti dal progetto** — puoi applicarli
  a qualsiasi progetto OpenCV, MediaPipe o YOLO per aggiungere output vocale.
- Aggiungere la voce rende i tuoi progetti piu accessibili e
  a mani libere, aprendo la porta ad applicazioni di tecnologia assistiva
  e installazioni interattive.
