.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_auto_tts:

13. TTS Automatico Senza Contatto — Diffusione Vocale a Mani Libere
==================================================================

-----------------------------------------------------------------
1. Panoramica
-----------------------------------------------------------------

In :ref:`mp_hand_count_tts` (Sezione 12), abbiamo costruito un programma
di conteggio dei gesti della mano in cui l'utente preme il tasto ``t`` per attivare
una diffusione vocale TTS.

In questa sezione, facciamo il passo successivo: **rimuovere completamente la tastiera.**
Il sistema ora rileva *automaticamente* quando tieni fermo un gesto della mano
e pronuncia il conteggio delle dita — niente tasti, niente pulsanti,
completamente senza contatto.

.. image:: img/mp_hand_count.png
   :align: center

Questa lezione introduce un **modello a macchina a stati** per l'interazione
senza contatto — una tecnica che puoi applicare a progetti di accessibilita,
installazioni a mani libere e qualsiasi scenario in cui l'input da tastiera
non e pratico.

Alla fine di questa lezione, saprai come:

- Progettare una macchina a stati per il tracciamento della presenza della mano
- Rilevare la *stabilita* del gesto su piu fotogrammi
- Usare un cancello di durata di mantenimento per evitare falsi trigger
- Rilevare automaticamente quando una mano entra o esce dal fotogramma
- Fornire feedback visivo a piu stadi (inattivo → rilevato → stabile → in parlato)
- Visualizzare una barra di progresso per il conto alla rovescia della durata di mantenimento


-----------------------------------------------------------------
2. Come Funziona
-----------------------------------------------------------------

Il programma sostituisce il trigger da tastiera con un **trigger automatico
basato sulla stabilita**. Ecco il pipeline:

1. Inizializza **MediaPipe Hands** per il rilevamento delle mani in tempo reale.
2. Inizializza il **motore TTS Fusion HAT+** (Espeak).
3. Acquisisce i fotogrammi video e rileva le dita (come prima).
4. Inserisce il conteggio delle dita in un **rilevatore di stabilita** — una finestra
   scorrevole che controlla se il conteggio e rimasto lo stesso
   attraverso piu fotogrammi consecutivi.
5. Una volta che il conteggio e confermato stabile, avvia un **timer di durata di mantenimento**.
6. Se l'utente mantiene lo stesso gesto per 2.5 secondi, il TTS si attiva
   automaticamente.
7. Se la mano lascia il fotogramma, il sistema dice "hand left the frame"
   dopo un breve ritardo.
8. Una **barra di progresso** e un **bordo multicolore** mostrano lo stato
   corrente a colpo d'occhio.

The key design idea is:

    *The user's steady hand replaces the keyboard —*
    the system watches for *intent* (holding still) rather than
    reacting to every fleeting gesture.

This makes the project fully hands-free and accessible — ideal for
assistive technology, interactive exhibits, or situations where
the user cannot reach a keyboard.


-----------------------------------------------------------------
3. Concetti di Progettazione Chiave
-----------------------------------------------------------------

Aggiungere il TSS ad attivazione automatica richiede una gestione dello stato
piu sofisticata rispetto alla versione con pressione del tasto. Esaminiamo ogni
nuovo concetto.

--------------------------------------------------
3.1 Macchina a Stati per il Tracciamento della Mano
--------------------------------------------------

Il programma traccia la presenza della mano come uno **stato**, non solo un
valore per fotogramma. Una classe ``HandTrackingState`` incapsula
tutte le variabili di stato:

.. code-block:: python

    class HandTrackingState:
        def __init__(self):
            self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
            self.current_fingers = 0
            self.stable_fingers = -1
            self.stable_start_time = 0
            self.is_stable = False
            self.hand_present = False
            self.hand_absent_start_time = 0
            self.last_tts_time = 0
            self.last_tts_message = ""
            self.last_no_hand_tts_time = 0

    state = HandTrackingState()

Raggruppando tutte le variabili di tracciamento in un unico oggetto, il codice
rimane organizzato anche quando la logica diventa piu complessa.

La macchina a stati transita attraverso queste fasi:

- **Nessuna mano** — bordo grigio, stato inattivo
- **Mano rilevata, non ancora stabile** — bordo ciano, prompt "tieni la mano ferma"
- **Stabile, in mantenimento** — bordo verde si riempie, barra di progresso animata
- **In parlato** — flash verde brillante, etichetta "SPEAKING..."

--------------------------------------------------
3.2 Rilevamento della Stabilita
--------------------------------------------------

Un conteggio delle dita su un singolo fotogramma e inaffidabile — il numero puo
fluttuare a causa del rumore della fotocamera o di un leggero movimento della mano. Per evitare
falsi trigger, usiamo una **finestra scorrevole** dei conteggi recenti:

.. code-block:: python

    from collections import deque

    FRAME_HISTORY_SIZE = 10
    STABLE_FRAMES_REQUIRED = 5

    state.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)

    def update_stability(new_count):
        state.finger_history.append(new_count)

        if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
            recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
            if all(c == new_count for c in recent_counts):
                # Gesture is stable!
                state.is_stable = True
                state.stable_start_time = time.time()
                state.current_fingers = new_count
                return True

        state.current_fingers = new_count
        return False

Il gesto e considerato **stabile** solo quando gli ultimi 5 fotogrammi
riportano tutti lo stesso conteggio delle dita. Questo filtra le fluttuazioni
momentanee e garantisce che il sistema parli solo quando l'utente sta
intenzionalmente mantenendo un gesto.

--------------------------------------------------
3.3 Auto-Trigger con Durata di Mantenimento
--------------------------------------------------

La stabilita da sola non basta — l'utente deve *mantenere* il gesto
abbastanza a lungo per dimostrare l'intenzione:

.. code-block:: python

    HOLD_DURATION_REQUIRED = 2.5    # seconds
    MIN_TTS_INTERVAL = 4.0          # seconds between auto triggers

    def should_trigger_tts():
        now = time.time()

        # Minimum interval between TTS triggers
        if now - state.last_tts_time < MIN_TTS_INTERVAL:
            return False

        # Hand must be present and stable
        if not state.hand_present or not state.is_stable:
            return False

        # Must have been stable for the required hold duration
        hold_time = now - state.stable_start_time
        if hold_time < HOLD_DURATION_REQUIRED:
            return False

        # Don't repeat the same count too quickly
        if state.stable_fingers == state.current_fingers:
            if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
                return False

        return True

Tre cancelli proteggono dai falsi trigger:

1. **Intervallo minimo** — almeno 4 secondi tra due eventi TTS qualsiasi.
2. **Durata di mantenimento** — il gesto deve essere tenuto fermo per 2.5 secondi.
3. **Protezione ripetizioni** — lo stesso conteggio non verra pronunciato di nuovo per 8 secondi.

--------------------------------------------------
3.4 Rilevamento dell'Uscita della Mano
--------------------------------------------------

Quando l'utente rimuove la mano dalla fotocamera, il sistema
se ne accorge e pronuncia una notifica:

.. code-block:: python

    HAND_EXIT_DELAY = 4.0  # seconds after hand leaves

    # When hand just left:
    if state.hand_present:
        state.hand_present = False
        state.is_stable = False
        state.stable_fingers = -1
        state.finger_history.clear()

        if now - state.last_tts_time >= MIN_TTS_INTERVAL:
            tts.say("hand left the frame")

Il messaggio di uscita viene attivato solo se e passato abbastanza tempo
dall'ultimo evento TTS — impedendo che interrompa un
annuncio del conteggio delle dita.

--------------------------------------------------
3.5 Costruzione del Messaggio
--------------------------------------------------

La costruzione del messaggio e identica alla versione con pressione del tasto:

.. code-block:: python

    if count == 0:
        message = "no fingers detected"
    elif count == 1:
        message = "one finger detected"
    else:
        message = f"{count} fingers detected"

.. note::

   Unlike the key-press version which sums fingers across both hands,
   this version uses ``max(total_fingers, finger_count)`` to pick
   the hand with the most visible fingers. This produces more
   reliable results when both hands are in frame.

--------------------------------------------------
3.6 Feedback Visivo a Piu Stadi
--------------------------------------------------

Invece di un singolo flash verde, questa versione fornisce un
**bordo continuo con codice colore** che riflette lo stato corrente:

.. code-block:: python

    COLOR_IDLE     = (128, 128, 128)   # gray   — no hand
    COLOR_DETECTED = (255, 255, 0)     # cyan   — hand seen, not yet stable
    COLOR_STABLE   = (0, 255, 0)       # green  — gesture stable, holding
    COLOR_SPEAKING = (0, 255, 0)       # bright green — TTS in progress

The border color transitions smoothly from cyan to green as the
hold duration progresses, giving the user real-time feedback on
how close they are to triggering TTS.

**Barra di progresso**: Una piccola barra nell'angolo in alto a destra si riempie
da sinistra a destra mentre la durata di mantenimento conta. Quando raggiunge il 100%,
il TTS si attiva. Questo da all'utente un chiaro conto alla rovescia visivo.

**Testo di stato**: Una riga di stato sotto il conteggio delle dita mostra la
fase corrente:

- ``"Status: No hand detected"``
- ``"Status: Detecting... keep hand still"``
- ``"Status: Hold gesture (1.3s to speak)"``
- ``"Status: Ready to speak!"``


-----------------------------------------------------------------
4. Eseguire il Codice
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts_without_tap.py

#. Dopo aver eseguito il programma:

   - Si apre una finestra intitolata "MediaPipe Hand Detection + AUTO TTS (Touchless Mode)",
     che mostra il flusso video in diretta.
   - Tieni la mano davanti alla fotocamera — il conteggio delle dita appare
     nell'angolo superiore sinistro.
   - *Tieni la mano ferma* — osserva il bordo cambiare da grigio
     a ciano a verde, e la barra di progresso riempirsi.
   - Dopo 2.5 secondi di mantenimento dello stesso gesto, il sistema
     pronuncia automaticamente il conteggio delle dita.
   - Rimuovi la mano dalla fotocamera — dopo un momento, il sistema
     dice "hand left the frame."

   .. hint::

      Try showing different numbers of fingers and holding each
      one steady for a few seconds. You should hear each count
      spoken automatically. Notice how the border color and
      progress bar guide you through the process.

   Press ``q`` to exit the program.


--------------------------------------------------
5. Codice Completo
--------------------------------------------------

.. code-block:: python

   """
   MediaPipe Hand Detection + Auto TTS (Touchless Mode)
   ====================================================
   Detects fingers via webcam in real time. Automatically speaks the finger count
   when a stable hand gesture is maintained for a certain duration.

   No keyboard input required for triggering TTS.

   Usage:
       python mp_hand_count_auto_tts.py

   Controls:
       'q'  - quit
   """

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   from fusion_hat.tts import Espeak
   import time
   from collections import deque


   # ======================== Init TTS ========================
   tts = Espeak()
   tts.set_amp(200)       # volume 0-200, default 100
   tts.set_speed(150)     # speed 80-260, default 150
   tts.set_pitch(80)      # pitch 0-99, default 80

   # ======================== Init MediaPipe Hands ========================
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5,
       min_tracking_confidence=0.5
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

   # Auto TTS parameters
   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable before speaking
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves before saying "hand left"
   NO_HAND_COOLDOWN = 5.0          # seconds without hand before suppressing "no hand" repeats

   # Frame processing
   FRAME_HISTORY_SIZE = 10         # for stability detection

   # Border colors (BGR)
   COLOR_IDLE = (128, 128, 128)    # gray
   COLOR_DETECTED = (255, 255, 0)  # cyan
   COLOR_STABLE = (0, 255, 0)      # green
   COLOR_SPEAKING = (0, 255, 0)    # bright green

   print("=" * 60)
   print("  MediaPipe Hand Detection + AUTO TTS (Touchless Mode)")
   print("  No keyboard needed - just show a stable hand gesture")
   print("  Press 'q' to quit")
   print("=" * 60)

   # ======================== State Management ========================
   class HandTrackingState:
       def __init__(self):
           self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
           self.current_fingers = 0
           self.stable_fingers = -1
           self.stable_start_time = 0
           self.is_stable = False
           self.hand_present = False
           self.hand_absent_start_time = 0
           self.last_tts_time = 0
           self.last_tts_message = ""
           self.last_no_hand_tts_time = 0

   state = HandTrackingState()

   def get_finger_count(hand_landmarks):
       """Count fingers for a single hand (right hand logic)"""
       landmarks = hand_landmarks.landmark
       finger_count = 0

       # Thumb: extended when x_tip > x_dip (right hand)
       if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
           finger_count += 1

       # Other four fingers: tip is above dip when extended (smaller y)
       for i in range(1, 5):
           if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
               finger_count += 1

       return finger_count

   def update_stability(new_count):
       """Update stability state based on finger count history"""
       state.finger_history.append(new_count)

       if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
           recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
           if all(c == new_count for c in recent_counts):
               if not state.is_stable or state.current_fingers != new_count:
                   state.is_stable = True
                   state.stable_start_time = time.time()
                   state.current_fingers = new_count
                   return True
       else:
           state.is_stable = False

       state.current_fingers = new_count
       return False

   def should_trigger_tts():
       """Check if conditions are met for auto TTS"""
       now = time.time()

       if now - state.last_tts_time < MIN_TTS_INTERVAL:
           return False

       if not state.hand_present or not state.is_stable:
           return False

       hold_time = now - state.stable_start_time
       if hold_time < HOLD_DURATION_REQUIRED:
           return False

       if state.stable_fingers == state.current_fingers:
           if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
               return False

       return True

   def trigger_tts():
       """Execute TTS for current finger count"""
       now = time.time()
       count = state.current_fingers

       if count == 0:
           message = "no fingers detected"
       elif count == 1:
           message = "one finger detected"
       else:
           message = f"{count} fingers detected"

       if message == state.last_tts_message and now - state.last_tts_time < 3.0:
           return False

       print(f"[TTS] {message} (held for {HOLD_DURATION_REQUIRED}s)")
       tts.say(message)

       state.last_tts_time = now
       state.last_tts_message = message
       state.stable_fingers = count

       return True

   def trigger_hand_exit_tts():
       """Say hand has left the frame"""
       now = time.time()
       if now - state.last_tts_time >= MIN_TTS_INTERVAL:
           print("[TTS] hand left the frame")
           tts.say("hand left the frame")
           state.last_tts_time = now
           state.last_tts_message = "hand left"

   def get_border_color():
       """Determine border color based on current state"""
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

   # ======================== Main Loop ========================
   frame_count = 0
   speaking_flash_until = 0

   while True:
       # ---- 1. Capture frame ----
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # ---- 2. Convert to RGB for MediaPipe ----
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       # ---- 3. Convert back to BGR for OpenCV display ----
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # ---- 4. Detect hands and count fingers ----
       total_fingers = 0
       has_hand = False

       if hands_detected.multi_hand_landmarks:
           has_hand = True
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

               finger_count = get_finger_count(hand_landmarks)
               total_fingers = max(total_fingers, finger_count)

       # ---- 5. Update state machine ----
       now = time.time()

       if has_hand:
           if not state.hand_present:
               state.hand_present = True
               state.is_stable = False
               state.finger_history.clear()
               print("[INFO] Hand detected")
           state.hand_absent_start_time = now
       else:
           if state.hand_present:
               state.hand_present = False
               state.is_stable = False
               state.stable_fingers = -1
               state.finger_history.clear()
               if now - state.last_tts_time >= MIN_TTS_INTERVAL:
                   trigger_hand_exit_tts()

       if has_hand:
           update_stability(total_fingers)

           if should_trigger_tts():
               if trigger_tts():
                   speaking_flash_until = now + 0.8
                   state.speaking_until = speaking_flash_until

       # ---- 6. Display information on screen ----
       display_text = f"Fingers: {total_fingers}"
       cv2.putText(frame, display_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

       if not has_hand:
           status_text = "Status: No hand detected"
           status_color = (128, 128, 128)
       elif state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               remaining = HOLD_DURATION_REQUIRED - (now - state.stable_start_time)
               status_text = f"Status: Hold gesture ({remaining:.1f}s to speak)"
               status_color = (255, 255, 0)
           else:
               status_text = "Status: Ready to speak!"
               status_color = (0, 255, 0)
       else:
           status_text = "Status: Detecting... keep hand still"
           status_color = (0, 200, 200)

       cv2.putText(frame, status_text, (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

       cv2.putText(frame, "Keep gesture still to auto-speak | 'q' to quit",
                   (10, frame.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

       # ---- 7. Visual border feedback ----
       h, w = frame.shape[:2]
       thickness = 6

       if now < speaking_flash_until:
           border_color = (0, 255, 0)
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)
           cv2.putText(frame, "SPEAKING...", (w - 180, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
       else:
           border_color = get_border_color()
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)

       # ---- 8. Progress bar for hold duration ----
       if has_hand and state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           bar_width = int(w * 0.4)
           bar_height = 8
           bar_x = w - bar_width - 10
           bar_y = 10
           filled_width = int(bar_width * hold_progress)

           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                        (60, 60, 60), -1)
           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                        (0, 255, 0), -1)

       # ---- 9. Key handling ----
       key = cv2.waitKey(1) & 0xff

       if key == ord('q'):
           break

       # ---- 10. Show frame ----
       cv2.imshow("MediaPipe Hand Detection + AUTO TTS (Touchless Mode)", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")


--------------------------------------------------
6. Spiegazione del Codice
--------------------------------------------------

Esaminiamo il codice sezione per sezione, concentrandoci su
cosa e nuovo rispetto alla versione con pressione del tasto di
:ref:`mp_hand_count_tts`.

--------------------------------------------------
6.1 Importazioni e Nuove Dipendenze
--------------------------------------------------

.. code-block:: python

   from collections import deque
   import time

L'aggiunta chiave e ``deque`` — una coda a doppia estremita del
modulo ``collections`` di Python. Fornisce una finestra scorrevole
di dimensione fissa per il rilevamento della stabilita: quando fai ``append``
a un ``deque(maxlen=N)``, gli elementi vecchi vengono automaticamente
eliminati, mantenendo solo gli N valori piu recenti.

Questo e perfetto per tracciare gli ultimi 5-10 conteggi delle dita
senza gestione manuale delle liste.

--------------------------------------------------
6.2 Costanti e Configurazione
--------------------------------------------------

.. code-block:: python

   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves
   NO_HAND_COOLDOWN = 5.0          # seconds before suppressing repeats
   FRAME_HISTORY_SIZE = 10         # for stability detection

   COLOR_IDLE     = (128, 128, 128)   # gray
   COLOR_DETECTED = (255, 255, 0)     # cyan
   COLOR_STABLE   = (0, 255, 0)       # green
   COLOR_SPEAKING = (0, 255, 0)       # bright green

Tutti i parametri di temporizzazione e comportamento sono dichiarati come costanti
nominate all'inizio del file. Questo rende il programma facile da regolare —
vuoi un tempo di mantenimento piu lungo? Cambia ``HOLD_DURATION_REQUIRED``.
Vuoi annunci meno frequenti? Aumenta ``MIN_TTS_INTERVAL``.

I quattro colori del bordo definiscono un linguaggio visivo:

- **Grigio** — inattivo, nessuna mano nel fotogramma
- **Ciano** — mano rilevata, ma non ancora stabile
- **Verde** — gesto stabile e in mantenimento
- **Verde brillante** — attualmente in parlato

--------------------------------------------------
6.3 Classe HandTrackingState
--------------------------------------------------

.. code-block:: python

   class HandTrackingState:
       def __init__(self):
           self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
           self.current_fingers = 0
           self.stable_fingers = -1
           self.stable_start_time = 0
           self.is_stable = False
           self.hand_present = False
           self.hand_absent_start_time = 0
           self.last_tts_time = 0
           self.last_tts_message = ""
           self.last_no_hand_tts_time = 0

   state = HandTrackingState()

Questa classe raggruppa tutte le variabili di tracciamento in un unico oggetto.
Ogni variabile ha un ruolo specifico:

- ``finger_history`` — finestra scorrevole dei conteggi recenti delle dita
  (usata dal rilevatore di stabilita)
- ``current_fingers`` — il conteggio delle dita per il fotogramma corrente
- ``stable_fingers`` — l'ultimo conteggio stabile confermato che e stato pronunciato
- ``stable_start_time`` — quando e iniziato l'attuale periodo stabile
- ``is_stable`` — se il gesto e attualmente confermato stabile
- ``hand_present`` — se una mano e attualmente nel fotogramma
- ``hand_absent_start_time`` — quando la mano ha lasciato il fotogramma l'ultima volta
- ``last_tts_time`` — timestamp dell'ultimo evento TTS
- ``last_tts_message`` — l'ultimo messaggio pronunciato (per evitare ripetizioni)
- ``last_no_hand_tts_time`` — timestamp dell'ultimo annuncio "nessuna mano"

Una singola istanza ``state`` viene creata globalmente, quindi tutte le funzioni
helper possono leggerla e modificarla senza passare parametri.

--------------------------------------------------
6.4 Funzione di Rilevamento della Stabilita
--------------------------------------------------

.. code-block:: python

   def update_stability(new_count):
       state.finger_history.append(new_count)

       if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
           recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
           if all(c == new_count for c in recent_counts):
               if not state.is_stable or state.current_fingers != new_count:
                   state.is_stable = True
                   state.stable_start_time = time.time()
                   state.current_fingers = new_count
                   return True
       else:
           state.is_stable = False

       state.current_fingers = new_count
       return False

Questa funzione e il cuore del sistema senza contatto. Ecco come funziona:

1. **Aggiunge** il nuovo conteggio delle dita alla finestra scorrevole.
2. **Controlla** se abbiamo abbastanza fotogrammi (almeno 5).
3. **Confronta** gli ultimi 5 fotogrammi — se corrispondono tutti al conteggio
   corrente, il gesto e stabile.
4. **Registra** il momento in cui e iniziata la stabilita (``stable_start_time``)
   — questo viene usato dal timer di durata di mantenimento.
5. **Restituisce** ``True`` sul fotogramma in cui la stabilita viene confermata
   per la prima volta, ``False`` altrimenti.

L'espressione ``all(c == new_count for c in recent_counts)`` e
elegante: controlla che *ogni* valore nella finestra corrisponda al
conteggio corrente. Se anche un solo fotogramma differisce, la stabilita e interrotta.

--------------------------------------------------
6.5 Logica di Attivazione Automatica del TTS
--------------------------------------------------

.. code-block:: python

   def should_trigger_tts():
       now = time.time()

       if now - state.last_tts_time < MIN_TTS_INTERVAL:
           return False
       if not state.hand_present or not state.is_stable:
           return False
       hold_time = now - state.stable_start_time
       if hold_time < HOLD_DURATION_REQUIRED:
           return False
       if state.stable_fingers == state.current_fingers:
           if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
               return False
       return True

Questa funzione funge da **cancello** — tutte le condizioni devono essere soddisfatte
prima che il TTS possa attivarsi:

1. **Minimum interval**: at least 4 seconds since the last TTS.
2. **Hand present and stable**: the gesture must be confirmed stable.
3. **Hold duration**: the user must have held the gesture for
   at least 2.5 seconds.
4. **Repeat guard**: the same finger count won't be spoken again
   for 8 seconds (2× the minimum interval).

.. tip::

   The hold duration creates a clear *intent signal* — momentary
   gestures are ignored, but a deliberate hold triggers speech.
   This is the key difference from the key-press approach: the
   user's *patience* replaces the button press.

--------------------------------------------------
6.6 Rilevamento dell'Uscita della Mano
--------------------------------------------------

.. code-block:: python

   # In the main loop:
   if has_hand:
       if not state.hand_present:
           # Hand just entered
           state.hand_present = True
           state.is_stable = False
           state.finger_history.clear()
           print("[INFO] Hand detected")
       state.hand_absent_start_time = now
   else:
       if state.hand_present:
           # Hand just left
           state.hand_present = False
           state.is_stable = False
           state.stable_fingers = -1
           state.finger_history.clear()
           if now - state.last_tts_time >= MIN_TTS_INTERVAL:
               trigger_hand_exit_tts()

Quando la mano entra o esce dal fotogramma, lo stato viene resettato:

- La stabilita viene cancellata (``is_stable = False``)
- La cronologia delle dita viene cancellata (``history.clear()``)
- Se la mano e appena uscita, ed e passato abbastanza tempo
  dall'ultimo TTS, il sistema dice "hand left the frame"

Resettare la stabilita all'entrata e all'uscita impedisce che lo stato
obsoleto venga trasportato tra le apparizioni della mano.

--------------------------------------------------
6.7 Bordo Multicolore e Barra di Progresso
--------------------------------------------------

.. code-block:: python

   def get_border_color():
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               # Smooth blend from cyan to green
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

Il colore del bordo non e solo decorativo — e un indicatore
di stato in tempo reale:

- **Nessuna mano** → bordo grigio
- **Mano rilevata, non stabile** → bordo ciano
- **Stabile, in mantenimento** → gradiente fluido da ciano a verde
  mentre la durata di mantenimento progredisce
- **Mantenimento completato / in parlato** → bordo verde brillante

The **progress bar** works alongside the border:

.. code-block:: python

   if has_hand and state.is_stable:
       hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
       bar_width = int(w * 0.4)
       bar_height = 8
       bar_x = w - bar_width - 10
       bar_y = 10
       filled_width = int(bar_width * hold_progress)

       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                    (60, 60, 60), -1)  # background
       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                    (0, 255, 0), -1)   # fill

A dark gray bar (40% of frame width) sits in the top-right corner.
A green fill sweeps across it as the hold time progresses.
When the bar is full, TTS fires.

Together, the border color and progress bar give the user
continuous feedback — they always know exactly how close they
are to triggering speech.


-----------------------------------------------------------------
7. Idee di Estensione
-----------------------------------------------------------------

The touchless auto-TTS pattern opens up many possibilities:

- **Assistive communication** — Map specific gestures to
  pre-recorded phrases. Hold up 1 finger for "yes", 2 for "no",
  3 for "help". The system speaks the phrase automatically.

- **Hands-free presentation control** — Hold a gesture to
  advance slides or trigger sound effects during a talk.

- **Interactive museum exhibit** — Visitors hold up fingers
  to hear facts about numbered exhibits. No touching required.

- **GPIO button integration** — Add a physical button via
  ``fusion_hat`` GPIO that enables/disables auto-TTS mode,
  giving the user manual control over when the system listens.

- **Multi-gesture vocabulary** — Extend the stability detector
  to recognize a sequence of gestures (e.g., 1 finger → 2 fingers
  → 3 fingers) as a "command code" that triggers different actions.

- **Combine with Face Detection** — Auto-announce when a face
  enters or leaves the frame: "Person detected" / "Person left."


-----------------------------------------------------------------
8. Risoluzione dei Problemi
-----------------------------------------------------------------

- **TTS fires too frequently or on unstable gestures**

  Increase ``STABLE_FRAMES_REQUIRED`` (e.g., from 5 to 8) to
  require more frames of consistency before confirming stability.

  Increase ``HOLD_DURATION_REQUIRED`` (e.g., from 2.5 to 3.5)
  to require a longer hold before speaking.

- **TTS never fires, even when holding steady**

  Make sure your hand is well-lit and clearly visible to the
  camera. Check that ``min_detection_confidence`` is not set
  too high (0.5 is a good default).

  Verify that the status text on screen shows "Ready to speak!"
  — if it stays at "Detecting..." or the progress bar never
  fills, the stability detector may not be confirming.

- **"Hand left the frame" spoken at wrong times**

  The exit message respects ``MIN_TTS_INTERVAL`` — it won't
  fire if a finger-count announcement just happened. If you
  want it to always speak, remove the ``MIN_TTS_INTERVAL``
  check from ``trigger_hand_exit_tts()``.

- **Progress bar not appearing**

  The progress bar only appears when ``has_hand`` is ``True``
  **and** ``state.is_stable`` is ``True``. If either condition
  is false, the bar is hidden. Check the status text to
  determine which condition is failing.

- **Border color doesn't change**

  Verify that ``get_border_color()`` is being called on every
  frame and that the ``state.hand_present`` and ``state.is_stable``
  flags are being updated correctly in the main loop.


-----------------------------------------------------------------
9. Riepilogo
-----------------------------------------------------------------

- Questa lezione ha dimostrato come **rimuovere il trigger da tastiera**
  e costruire un sistema TTS completamente automatico senza contatto.
- Il progetto utilizza una **macchina a stati** (classe ``HandTrackingState``)
  per tracciare la presenza della mano, la stabilita del gesto e la temporizzazione del TTS.
- **Modelli di progettazione chiave** trattati:

  - **Rilevamento della stabilita** — finestra scorrevole dei conteggi delle dita
    per confermare che l'utente sta tenendo fermo un gesto
  - **Cancello di durata di mantenimento** — richiedere 2.5 secondi di stabilita
    prima di attivare il TTS, sostituendo la pressione del tasto con l'*intenzione*
  - **Rilevamento automatico dell'uscita** — pronuncia "hand left the frame"
    quando la mano scompare
  - **Feedback visivo a piu stadi** — bordo con codice colore
    (grigio → ciano → verde) piu una barra di progresso per lo stato
    in tempo reale
  - **Reset dello stato all'entrata/uscita della mano** — cancellare la cronologia e
    la stabilita per evitare che dati obsoleti vengano trasportati

- Questi modelli sono **indipendenti dal progetto** — puoi applicare
  l'approccio macchina a stati + rilevamento di stabilita a qualsiasi progetto
  di visione artificiale che necessiti di interazione senza contatto.
- Combinare il TTS automatico con il riconoscimento dei gesti apre la porta
  a tecnologie assistive, sistemi di controllo a mani libere e
  installazioni interattive.
