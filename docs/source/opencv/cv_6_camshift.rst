.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. Tracciamento Oggetti con CAMShift
=====================================

Nel capitolo precedente, abbiamo imparato l’algoritmo MeanShift, che puo’ tracciare continuamente un bersaglio in un video basandosi sul suo istogramma colore.
In questa sezione, introduciamo **CAMShift (Continuously Adaptive Mean Shift)**,
che estende MeanShift **adattando automaticamente la dimensione e l’orientamento della finestra**, rendendolo piu’ pratico per applicazioni reali.
Inoltre, in questo esempio tracceremo un bersaglio **basandoci sulla luminosita’ piuttosto che sul colore**, anch’esso molto comune nella pratica.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. Caratteristiche dell'Algoritmo
---------------------------------

**MeanShift** puo' solo tracciare la posizione del bersaglio e utilizza una finestra di dimensione fissa.
**CAMShift** traccia la posizione **e** regola automaticamente dimensione e angolo della finestra.

Ad esempio, quando il bersaglio si avvicina alla fotocamera, il riquadro di tracciamento cresce; quando si allontana, si riduce; quando ruota, il riquadro ruota di conseguenza.

.. image:: img/opencv_camshift.png
   :alt: Illustrazione del tracciamento CAMShift
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
      python3 cv_6_camshift.py

#. Quando esegui il programma, apparir'a una finestra OpenCV chiamata **CAMShift Tracker** che inizier'a a riprodurre il file video *sample3.mp4*.

   Il programma traccia il gatto nero utilizzando l'algoritmo CAMShift (Continuously Adaptive Mean Shift).

   Un rettangolo ruotato verde verr'a disegnato attorno all'oggetto tracciato.
   Mentre il gatto si muove o cambia dimensione e orientamento, la finestra di tracciamento adatter'a automaticamente posizione, dimensione e angolo.

   Puoi uscire dal programma in due modi:

   * Premere il tasto **q** sulla tastiera
   * Chiudere la finestra facendo clic sul pulsante di chiusura (X)

   Dopo l'uscita, la riproduzione video si ferma e tutte le finestre OpenCV vengono chiuse.

3. Codice Completo
------------------

Apri ``cv_6_camshift.py`` per visualizzare il codice completo.

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Spiegazione del Codice
-------------------------

#. Aprire il file video e leggere il primo frame:

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift necessita di un frame iniziale per imparare cosa tracciare.

#. Impostare la finestra di tracciamento iniziale (ROI):

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   Questo rettangolo dovrebbe coprire l'oggetto bersaglio nel primo frame.
   CAMShift aggiorner'a automaticamente questa finestra durante il tracciamento.

#. Convertire il primo frame in HSV ed estrarre la ROI:

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV e' comodo per il tracciamento perche' puoi scegliere canali specifici (come V per la luminosita').

#. Costruire una maschera per un oggetto scuro (valori V bassi):

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   Questo mantiene solo i pixel “scuri” nella ROI.
   Per oggetti neri/scuri, la luminosita' (V) e' solitamente la caratteristica piu' utile.

#. Calcolare e normalizzare un istogramma del canale V:

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - Il canale ``2`` corrisponde al canale **V (Value/luminosita')** in HSV.
   - L'istogramma descrive quanto “scuro/luminoso” e' la ROI del bersaglio.
   - La normalizzazione rende il tracciamento piu' stabile.

#. Impostare i criteri di terminazione per CAMShift:

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift smette di aggiornarsi quando raggiunge 10 iterazioni o il movimento e' inferiore a 1 pixel.

#. Set playback speed using FPS:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Questo imposta un ritardo in modo che il video venga riprodotto vicino ai suoi FPS originali.

#. Creare una mappa di probabilita' usando la back projection (canale V):

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   La back projection evidenzia i pixel nel frame i cui valori V corrispondono all'istogramma ROI.
   Valori piu' luminosi in ``back_proj`` significano “piu' probabilmente il bersaglio”.

#. Tracciare usando CAMShift e aggiornare la finestra:

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift e' basato su MeanShift, ma puo' anche adattare la **dimensione e la rotazione** della finestra di tracciamento.

   - ``track_window`` viene aggiornato ogni frame.
   - ``rot_rect`` contiene un rettangolo ruotato (centro, dimensione, angolo).

#. Disegnare il riquadro di tracciamento ruotato:

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   Questo converte il rettangolo ruotato in quattro punti d'angolo e lo disegna sul frame.

#. Condizioni di uscita (tastiera + chiusura finestra):

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   Premi ``q`` per uscire o chiudi la finestra per fermarti in modo sicuro.

#. Rilasciare le risorse:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Rilascia sempre il file video e chiudi le finestre alla fine.


5. CAMShift vs MeanShift
------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Caratteristica
     - MeanShift
     - CAMShift
   * - Dimensione finestra
     - Fissa
     - Adattiva
   * - Angolo
     - Non supportato
     - Supporta la rotazione
   * - Precisione tracciamento
     - Moderata
     - Piu' alta, piu' adattiva
   * - Applicazioni
     - Bersagli statici
     - Movimento complesso, bersagli rotanti

CAMShift e' un miglioramento rispetto a MeanShift,
gestisce meglio la deformazione, la rotazione e i cambiamenti di distanza del bersaglio, risultando ideale per scenari reali.

6. Estensioni ed Esercizi
-------------------------

- Regola le soglie ``inRange`` per tracciare bersagli verdi o blu
- Combina con l'input della fotocamera in tempo reale per costruire un sistema di tracciamento basato sul colore


7. Avanzato: Selezione Interattiva ROI e Regolazione Automatica delle Soglie HSV
---------------------------------------------------------------------------------

Come nella sezione precedente, questo progetto puo' anche utilizzare l'interazione con il mouse per selezionare la ROI e regolare automaticamente le soglie HSV.

Esegui ``cv_6_camshift_auto.py`` per il codice modificato.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

Quando esegui il programma, il primo frame del video verr'a visualizzato e ti verr'a chiesto di selezionare una Regione di Interesse (ROI) con il mouse.

Trascina il mouse per disegnare un rettangolo attorno all'oggetto bersaglio, poi premi **Enter** o **Space** per confermare la selezione.
Premi **Esc** per annullare la selezione.

Dopo aver selezionato la ROI, apparir'a una finestra chiamata **CAMShift Tracker**.
L'oggetto selezionato verr'a tracciato con un rettangolo ruotato verde, e la finestra di tracciamento adatter'a automaticamente posizione, dimensione e orientamento man mano che l'oggetto si muove.

Per fermare il programma:

* Premi il tasto **q** sulla tastiera
* Oppure chiudi la finestra usando il pulsante di chiusura (X)

Dopo l'uscita, la riproduzione video si ferma e tutte le finestre OpenCV vengono chiuse.


.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

   ...

