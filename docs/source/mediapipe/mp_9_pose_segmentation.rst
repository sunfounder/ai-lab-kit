.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. Schermo Verde
====================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

Questo capitolo utilizza la capacita di **segmentazione della persona** di
MediaPipe Pose per implementare un semplice **effetto schermo verde**.

Separando la persona dallo sfondo,
possiamo sostituire lo sfondo originale con un colore verde uniforme.
Questo consente:

- Applicazioni con sfondo virtuale
- Compositing chroma key (OBS / NLE)
- Effetti per live streaming
- Sostituzione della scena in stile AR

.. image:: img/mp_pose_green.png
   :align: center


------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

L'effetto schermo verde e implementato usando i seguenti passaggi:

1. Inizializza il modello Pose con ``enable_segmentation=True``.
2. Per ogni fotogramma, ottieni ``results.segmentation_mask``.
3. La maschera e una mappa di probabilita a canale singolo (intervallo 0–1).
4. Applica una soglia (es., 0.5) per separare primo piano e sfondo.
5. Sostituisci i pixel dello sfondo con verde uniforme.
6. Opzionalmente applica sfocatura o filtraggio morfologico per ammorbidire i bordi.

Questo metodo e leggero e funziona in tempo reale su Raspberry Pi,
fornendo al contempo un esempio pratico di segmentazione umana.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

   Se desideri utilizzare MediaPipe Pose con un video registrato, puoi eseguire il seguente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

#. Dopo aver eseguito il programma, si apre una finestra intitolata "Show Video" che mostra il flusso video in diretta.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_9.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Una barra di scorrimento chiamata ``Mask`` appare nella stessa finestra. Controlla la soglia di segmentazione (0–100), con il valore predefinito impostato a 50 (0.5).

   Quando una persona appare davanti alla fotocamera:

   - MediaPipe Pose genera una ``segmentation_mask`` per ogni fotogramma.
   - I pixel con valori della maschera superiori alla soglia vengono trattati come primo piano (persona).
   - Tutti gli altri pixel vengono sostituiti con uno sfondo verde uniforme (effetto schermo verde).

   Mentre muovi la barra di scorrimento ``Mask``:

   - Aumentare la soglia mantiene solo l'area di primo piano piu sicura (meno perdita di sfondo, ma potrebbe tagliare alcune parti del corpo).
   - Diminuire la soglia include piu pixel come primo piano (sagoma piu completa, ma potrebbe includere rumore dello sfondo).

   Se non e disponibile alcuna maschera di segmentazione, il programma mostra semplicemente il normale flusso video senza sostituzione dello sfondo.

   Premi ``q`` per uscire dal programma.
   La fotocamera si ferma e la finestra OpenCV si chiude automaticamente.

-----------------------------
4. Codice Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: callback vuoto per le barre di scorrimento ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Crea una barra di scorrimento per la soglia, valore predefinito 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Dopo aver eseguito lo script, la persona (primo piano) viene preservata e lo sfondo viene sostituito con verde uniforme.
Puo essere utilizzato direttamente per il successivo keying con **Chroma Key** in OBS, Premiere, DaVinci Resolve, ecc.

-------------------------------------
5. Spiegazione dei Punti Chiave
-------------------------------------

``segmentation_mask`` e una **immagine float a canale singolo** (intervallo 0~1) con la stessa dimensione del fotogramma di input:

- Valore **vicino a 1**: Alta probabilita di essere **primo piano (persona)**;
- Valore **vicino a 0**: Alta probabilita di essere **sfondo**.

L'approccio usuale e impostare una soglia **T** (es., 0.5) e creare una maschera di condizione:

.. code-block:: python

   condition = (mask > T)[..., None]

Qui impostiamo una barra di scorrimento per regolare la soglia in tempo reale:

.. code-block:: python

   # Crea una barra di scorrimento per la soglia, valore predefinito 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

Poi possiamo usare ``np.where(condition, frame, background)`` per sostituire lo sfondo; qui lo sostituiamo con il verde:

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
6. Ottimizzazione dell'Effetto e dei Bordi
----------------------------------------------------

La binarizzazione diretta puo causare bordi frastagliati o piccoli fori intorno ai capelli e ai bordi dei vestiti.
**Una leggera post-elaborazione** puo migliorare i bordi:

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **Intervallo T consigliato 0.3~0.7**: Puo essere opportunamente abbassato in ambienti bui/modelli conservativi; puo essere aumentato con piu rumore.
   - Non rendere il kernel di sfocatura troppo grande, altrimenti il confine della persona "perdera verde".

----------------------------------------------------
7. Utilizzo di Sfondi Personalizzati (Immagine/Video)
----------------------------------------------------

Sostituisci il verde uniforme con un'immagine di sfondo personalizzata:

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

Oppure usa un altro video come sfondo (leggi il fotogramma successivo ``bg_frame``, ridimensionalo alle stesse dimensioni, poi sostituisci).

----------------------------------------------------
8. Bilanciamento tra Prestazioni e Qualita
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Elemento
     - Impatto
     - Suggerimento
   * - Risoluzione
     - Risoluzione piu alta da bordi piu fini ma velocita ridotta
     - Inizia con 640×480; aumenta se serve un'immagine piu chiara
   * - model_complexity
     - Piu alto e piu preciso ma piu lento
     - Raccomandato 1~2 su Raspberry Pi
   * - Forza della post-elaborazione
     - Troppa sfocatura/morfologia puo "inghiottire i bordi/perdere verde"
     - Kernel piccolo + poche iterazioni, osserva l'effetto sui bordi

------------------------------------------------------------
9. Risoluzione dei Problemi
------------------------------------------------------------

- Bordi frastagliati o cuciture visibili intorno alla persona

  Questo di solito accade perche la maschera viene applicata con una soglia rigida, che crea confini netti.

  Prova a regolare la soglia usando la barra di scorrimento ``Mask``. Per bordi piu morbidi, applica una piccola sfocatura alla maschera di segmentazione o usa una semplice operazione di chiusura morfologica prima del compositing.

- Parti mancanti della persona

  Se parti del corpo vengono tagliate, l'illuminazione potrebbe essere troppo debole o il colore dei vestiti potrebbe confondersi con lo sfondo.

  Migliora l'illuminazione, regola la soglia e prova a usare uno sfondo piu semplice con maggiore contrasto rispetto al soggetto.

- Basso frame rate

  Se il video e lento, la risoluzione potrebbe essere troppo alta o il modello troppo complesso.

  Riduci la risoluzione della fotocamera (per esempio, 640×480 o 320×240) e mantieni ``model_complexity`` a 1 per migliori prestazioni.

- Il verde si riversa sul soggetto

  Se lo sfondo verde appare sul soggetto, il confine di segmentazione potrebbe essere impreciso o il colore del soggetto potrebbe causare confusione visiva.

  Prova a passare a un colore di sostituzione diverso (blu o grigio), o sostituisci lo sfondo con un'immagine invece di un colore uniforme per un risultato piu naturale.


-----------------------------
10. Riepilogo
-----------------------------

- Usando ``segmentation_mask``, possiamo ottenere rapidamente "ritaglio della persona + sostituzione dello sfondo";
- Ottieni bordi piu naturali attraverso soglie e post-elaborazione leggera;
- Adatto per sfondi virtuali, keying per live streaming, insegnamento a distanza, ecc.;
- I prossimi passi potrebbero combinare **scheletro della posa** e **segmentazione** per effetti piu interattivi (es., sostituire solo lo sfondo, non sostituire la sovrapposizione dello scheletro in primo piano).