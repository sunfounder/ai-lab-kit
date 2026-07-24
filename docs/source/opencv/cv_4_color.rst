.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. Rilevamento del Colore
=========================

Il rilevamento del colore e' una delle funzioni piu' fondamentali e pratiche della computer vision.
In questo capitolo, utilizzeremo codice e spiegazioni passo-passo per **rilevare oggetti rossi usando lo spazio colore HSV** e **disegnare rettangoli delimitatore** intorno ad essi.

Questo costituisce la base per tecniche di tracciamento oggetti piu' avanzate (es. CAMShift).

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Obiettivo e Approccio
------------------------

- Usare **Picamera2** per acquisire frame dalla fotocamera in tempo reale
- Convertire l'immagine dallo spazio colore BGR a HSV
- Usare ``cv2.inRange`` per estrarre le regioni rosse
- Usare il filtraggio morfologico per rimuovere il rumore
- Usare ``cv2.findContours`` per trovare i contorni degli oggetti rossi
- Disegnare rettangoli delimitatore attorno alle regioni rosse rilevate

.. image:: img/color_detection.png
   :alt: Illustrazione dell'anteprima del rilevamento colore
   :align: center

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
      python3 cv_4_color.py

#. Quando esegui il programma, appariranno due finestre OpenCV sullo schermo:

   * **Red Detection** – mostra l'immagine in diretta dalla fotocamera con rettangoli verdi attorno agli oggetti rossi rilevati
   * **Red Mask** – mostra l'immagine della maschera binaria utilizzata per il rilevamento del colore rosso

   Il programma acquisisce continuamente frame dalla fotocamera Raspberry Pi e rileva le regioni rosse in tempo reale.
   Se viene rilevato un oggetto rosso, un rettangolo verde e il valore dell'area verranno visualizzati sull'immagine a colori.

   Puoi uscire dal programma in due modi:

   * Premere il tasto **q** sulla tastiera
   * Chiudere una qualsiasi finestra OpenCV facendo clic sul pulsante di chiusura (X)

   Dopo l'uscita, la fotocamera smette di trasmettere e tutte le finestre OpenCV vengono chiuse.

3. Codice Completo
------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. Spiegazione del Codice
-------------------------

#. Inizializzare Picamera2 e avviare lo streaming:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   Questo configura la fotocamera a 640×480 e avvia lo stream di anteprima.
   ``XRGB8888`` e' un formato a 4 canali, quindi i frame catturati sono di tipo BGRA.

#. Convertire il frame catturato in un formato che OpenCV utilizza comunemente:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2 restituisce un'immagine a 4 canali, quindi la convertiamo in BGR standard a 3 canali per l'elaborazione.

#. Usare lo spazio colore HSV per un rilevamento colore robusto:

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV separa il colore (Hue) dalla luminosita', rendendo il rilevamento colore piu' stabile in diverse condizioni di illuminazione.

#. Definire due intervalli HSV per il rosso:

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   Il rosso “si avvolge” attorno alla scala Hue in OpenCV HSV (vicino a 0 e vicino a 180), quindi due intervalli vengono combinati per coprire tutte le sfumature di rosso.

#. Pulire la maschera con la morfologia (ridurre il rumore e riempire i buchi):

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** rimuove piccoli punti rumorosi.
   - **CLOSE** riempie piccoli buchi all'interno delle regioni rosse rilevate.

#. Trovare le regioni rosse e filtrare le piccole macchie:

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   I contorni vengono rilevati dalla maschera binaria.
   ``MIN_AREA`` ignora le piccole regioni rosse per ridurre i falsi positivi.

#. Disegnare rettangoli delimitatore ed etichette sull'immagine risultato:

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   Questo mostra dove OpenCV ha trovato oggetti rossi e stampa l'area della macchia rilevata come riferimento.

#. Visualizzare sia il risultato che la maschera:

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   La **finestra del risultato** mostra la vista della fotocamera con i riquadri, mentre la **finestra della maschera** mostra l'immagine binaria solo rossa.

#. Condizioni di uscita (tastiera + chiusura finestra):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   Premi ``q`` per uscire o chiudi una qualsiasi finestra per uscire in modo sicuro.

#. Pulizia:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Ferma sempre la fotocamera e chiudi le finestre OpenCV per rilasciare le risorse.


5. Suggerimenti per la Regolazione dei Parametri
------------------------------------------------

- ``LOWER_RED1 / UPPER_RED1``: regola questo intervallo per rilevare altri colori.
  Ad esempio, verde ≈ ``[35, 50, 50]`` a ``[85, 255, 255]``.

- ``KERNEL``: kernel piu' grandi forniscono un filtraggio piu' forte ma potrebbero rimuovere oggetti piccoli.

- ``MIN_AREA``: aumentare questo valore filtra i contorni piccoli e rumorosi; diminuirlo rende il rilevamento piu' sensibile.

.. note::
   Puoi iniziare visualizzando solo la ``mask`` e regolando le soglie fino a quando la regione target appare chiara, poi procedere con il resto del processo.




6. Estensioni ed Esercizi
-------------------------

- Modifica la soglia HSV per rilevare altri colori (es. blu o verde).
- Sperimenta con diversi parametri morfologici in sfondi piu' complessi.
