.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. Stima della Posizione Umana
================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

Dopo l'implementazione del riconoscimento di mani e gesti,
questo capitolo introduce **MediaPipe Pose** —
un modulo leggero ma potente per la stima della posizione umana in tempo reale.

Usando MediaPipe Pose, possiamo rilevare **33 landmark del corpo**
in tempo reale e disegnare lo scheletro completo sul flusso video.

.. image:: img/mp_pose.png
   :width: 400
   :align: center

This module can be used for:

- Riconoscimento delle azioni
- Correzione della postura
- Monitoraggio del fitness
- Analisi del movimento

------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

Il programma esegue i seguenti passaggi:

1. Inizializza il modello MediaPipe Pose
   (configura la complessita del modello e la segmentazione opzionale).
2. Acquisisce i fotogrammi video usando ``Picamera2``.
3. Converte i fotogrammi in formato RGB (richiesto da MediaPipe).
4. Esegue il modello Pose per ottenere 33 punti chiave del corpo.
5. Disegna i punti chiave e le connessioni dello scheletro usando OpenCV.
6. Visualizza il flusso video annotato in tempo reale.

Questo capitolo getta le basi per attivita piu avanzate di
interazione uomo-macchina e analisi del movimento del corpo.


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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   Se desideri utilizzare MediaPipe Pose con un video registrato, puoi eseguire il seguente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. Dopo aver eseguito il programma, si apre una finestra intitolata "Show Video" che mostra il flusso video in diretta.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
         
   Quando una persona appare davanti alla fotocamera:

   - MediaPipe Pose rileva 33 landmark del corpo in tempo reale.
   - Viene disegnato uno scheletro completo sul fotogramma video.
   - Le articolazioni chiave come spalle, gomiti, polsi, fianchi, ginocchia e caviglie sono collegate con linee.

   Mentre la persona si muove:

   - I punti chiave dello scheletro seguono il movimento del corpo in modo fluido.
   - Lo scheletro si aggiorna continuamente in tempo reale.

   Se la segmentazione dello sfondo e abilitata (``enable_segmentation=True``),
   il modello calcola internamente una maschera di segmentazione, anche se in questo esempio
   viene visualizzato solo lo scheletro.

   Se nessuna persona viene rilevata, il programma mostra semplicemente il normale flusso video senza annotazioni.

   Premi ``q`` per uscire dal programma.
   La fotocamera si ferma e la finestra OpenCV si chiude automaticamente.

-----------------------------
4. Codice Completo
-----------------------------

Ecco un programma di base per il rilevamento della posizione umana:

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

Dopo aver eseguito il programma, il flusso video mostrera uno scheletro umano in tempo reale, includendo:

- 33 punti chiave
- Linee di connessione dello scheletro
- Lo scheletro segue il movimento quando la persona si muove

-----------------------------
5. Spiegazione del Codice
-----------------------------

**1. Importare le Librerie**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  Controlla la fotocamera del Raspberry Pi, basata su libcamera.

* **cv2 (OpenCV)**
  Utilizzato per la conversione dello spazio colore (BGR↔RGB), finestre di visualizzazione, disegno di grafica.

* **mediapipe.python.solutions.pose**
  Il **modello Pose** di MediaPipe, che puo rilevare **33 punti chiave del corpo completo** (testa, spalle, gomiti, ginocchia, ecc.), e puo restituire maschere di segmentazione (umano vs. sfondo).

* **drawing_utils / drawing_styles**
  Strumenti di disegno integrati di MediaPipe e definizioni di stile, utilizzati per disegnare punti chiave e linee dello scheletro.

**2. Inizializzare il Modello Pose**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Modalita video continua
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False``: Indica che l'input e un flusso video continuo, non una singola immagine. Tiene traccia dopo il rilevamento iniziale per maggiore velocita. Di solito impostato su False.

* ``model_complexity=1``: Complessita del modello, 0=leggero, 1=medio, 2=alta precisione (piu lento). Imposta a 1 o 2 se le prestazioni del Raspberry Pi lo consentono.

* ``enable_segmentation=True``: Restituisce la maschera di segmentazione umana, puo distinguere la persona in primo piano dallo sfondo. Quando True, abilita effetti come la sostituzione dello sfondo, il chroma key. Questo utilizzo sara spiegato nella documentazione successiva: :ref:`mp_pose_segmentation`

MediaPipe Pose restituisce una struttura di risultati che include:

* ``pose_landmarks``: 33 punti chiave;
* ``pose_world_landmarks``: Coordinate 3D del mondo;
* ``segmentation_mask``: Mappa di segmentazione umana.

**3. Aprire la Fotocamera**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

* Crea l'oggetto fotocamera ``Picamera2()``
* Imposta la risoluzione **640x480**, formato pixel ``"XRGB8888"`` (BGRA a 4 canali).
  Questo formato ha la migliore compatibilita con OpenCV, eliminando i passaggi di decodifica.
* Avvia la fotocamera.

Opzionale:
``picam2.start_preview(Preview.QTGL)`` puo visualizzare la finestra del flusso video direttamente sulla GPU; commentato qui, si usa invece ``imshow()`` di OpenCV.

**4. Ciclo Principale: Elaborare Ogni Fotogramma**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Acquisisce un fotogramma dalla fotocamera (formato BGRA)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. Acquisisce il fotogramma corrente. Picamera2 restituisce immagini in formato **BGRA** (Blue Green Red + Alpha) per impostazione predefinita.
2. Converte in **BGR** per la successiva elaborazione OpenCV.

.. code-block:: python

   # Converti in RGB per MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

I modelli MediaPipe **devono usare RGB**.

* Chiama ``pose.process()`` per il rilevamento dei punti chiave.
* ``results`` e un oggetto complesso che puo contenere:

  * ``results.pose_landmarks``: Punti chiave (33 punti)
  * ``results.pose_world_landmarks``: Coordinate 3D
  * ``results.segmentation_mask``: Maschera di segmentazione

.. code-block:: python

   # Converti nuovamente in BGR per la visualizzazione con OpenCV
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

Converte nuovamente perche ``imshow()`` di OpenCV richiede l'ordine BGR.

**5. Disegnare i Punti Chiave della Pose**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

Se viene rilevato un corpo umano:

* ``results.pose_landmarks``: Contiene ``(x, y, z, visibility)`` per ogni punto chiave.

  * ``x, y``: Coordinate normalizzate (0~1)
  * ``z``: Profondita relativa
  * ``visibility``: Confidenza del punto chiave (0~1)

* Spiegazione dei parametri ``draw_landmarks``:

   * ``frame``: Immagine su cui disegnare (formato BGR)
   * ``results.pose_landmarks``: Punti chiave umani per il fotogramma corrente
   * ``mp_pose.POSE_CONNECTIONS``: Regole di connessione (quali punti collegare con linee)
   * ``landmark_drawing_spec``: Stile di disegno dei punti
   * ``connection_drawing_spec``: Stile di disegno delle linee (puo essere omesso, usa lo stile predefinito del sistema)

Effetto: Disegna lo scheletro (connessioni per testa, braccia, gambe) e i punti chiave (posizioni delle articolazioni) sull'immagine.

**6. Visualizzare il Fotogramma e Logica di Uscita**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

Visualizza ogni fotogramma nella finestra ``"Show Video"``.
Esce dal ciclo quando viene premuto il tasto 'q'.

**7. Rilasciare le Risorse**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Ferma l'anteprima, rilascia la fotocamera, chiude tutte le finestre OpenCV.

-----------------------------
6. Introduzione al Modello Pose
-----------------------------

Il modulo MediaPipe Pose restituisce **33 punti chiave**, coprendo aree come testa, torso, braccia e gambe:

.. list-table::
   :header-rows: 1

   * - Parte del Corpo
     - Indice
   * - Naso
     - 0
   * - Spalla Sinistra/Destra
     - 11 / 12
   * - Gomito Sinistro/Destro
     - 13 / 14
   * - Polso Sinistro/Destro
     - 15 / 16
   * - Anca Sinistra/Destra
     - 23 / 24
   * - Ginocchio Sinistro/Destro
     - 25 / 26
   * - Caviglia Sinistra/Destra
     - 27 / 28
   * - Indice del Piede Sinistro/Destro
     - 31 / 32

Questi punti possono essere utilizzati per **giudizio della postura**, **conteggio delle azioni** (es., squat, flessioni, rilevamento di pose yoga), ecc.

-----------------------------
7. Prestazioni e Regolazione
-----------------------------

.. list-table::
   :header-rows: 1

   * - Elemento
     - Impatto
     - Suggerimento di Ottimizzazione
   * - Risoluzione
     - Risoluzione piu alta aumenta la precisione ma anche la latenza
     - Usa 640x480 per bilanciare prestazioni e velocita
   * - model_complexity
     - Migliora la precisione del riconoscimento ma rallenta il calcolo
     - Raccomandato 1~2 per Raspberry Pi
   * - Segmentazione
     - Aumenta il carico GPU/CPU
     - Raccomandato disabilitare se la sostituzione dello sfondo non e necessaria

------------------------------------------------------------
8. Risoluzione dei Problemi
------------------------------------------------------------

- Nessun umano rilevato

  Se il programma viene eseguito ma nessuna persona viene rilevata, assicurati che l'intero corpo sia all'interno del fotogramma della fotocamera. Evita la retroilluminazione intensa e migliora le condizioni di illuminazione. Mantieni una distanza di circa 1–2 metri dalla fotocamera per risultati ottimali.

- Video lento o in ritardo

  Se il frame rate e basso, prova a ridurre la risoluzione a 640×480 o inferiore. Imposta ``model_complexity = 1`` per migliori prestazioni. Disabilita la segmentazione se non e necessaria e chiudi altri programmi in background per liberare risorse di sistema.

- Errore di segmentazione (segmentation fault)

  La maggior parte degli errori di segmentazione sono causati da una mancata corrispondenza tra l'architettura del sistema e la wheel di MediaPipe installata.

  Controlla l'architettura del tuo sistema:

  .. code-block:: bash

     uname -m

  L'output dovrebbe essere ``aarch64``.

  Se vedi ``armv7l`` o ``armhf``, stai usando Raspberry Pi OS a 32 bit, che non e compatibile con la wheel ufficiale di MediaPipe.

  Puoi anche verificare in Python:

  .. code-block:: python

     import platform
     print(platform.machine())

  Il risultato deve essere anche ``aarch64``.

- Uso aarch64 ma ho ancora un segmentation fault

  Questo puo accadere se alcuni kernel TensorFlow Lite XNNPACK non sono completamente compatibili con la tua build di MediaPipe.

  Soluzioni possibili:

  - Usa ``model_complexity = 1`` (raccomandato in questo tutorial).
  - Assicurati che MediaPipe sia installato nell'ambiente virtuale corretto.
  - Installa una wheel ottimizzata per Raspberry Pi come ``mediapipe-bin`` (versione PINTO0309).

- ``model_complexity = 2`` si blocca ma ``1`` funziona

  La complessita 2 carica un modello piu grande che potrebbe attivare ottimizzazioni CPU avanzate. Su Raspberry Pi, alcuni kernel TensorFlow Lite ottimizzati potrebbero non essere completamente supportati. La complessita 1 evita quei kernel ed e generalmente piu stabile e veloce su Raspberry Pi.



-----------------------------
9. Riepilogo
-----------------------------

- Questo capitolo ha implementato il **rilevamento dello scheletro umano in tempo reale** basato su MediaPipe Pose;
- Pose fornisce 33 punti chiave, utilizzabili in campi come fitness, analisi della postura, riconoscimento delle azioni;
- Regolando risoluzione e complessita del modello, si puo ottenere un funzionamento fluido su Raspberry Pi;
- Basandoci su questi punti chiave, possiamo successivamente sviluppare:

  - Riconoscimento delle azioni (es., "alzare la mano", "accovacciarsi")
  - Valutazione della postura (es., "La postura da seduti e corretta?")
  - Controllo interattivo umano.