.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. Tracciamento Oggetti con MeanShift
======================================

MeanShift e’ un classico algoritmo di tracciamento oggetti basato su istogrammi.
In questa lezione, non solo implementeremo un esempio completo di **tracciamento MeanShift**, ma spiegheremo anche **perche’** ogni passo viene eseguito e **cosa succede dietro le quinte**.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. Cos'e' MeanShift?
--------------------

MeanShift sposta iterativamente una finestra secondo la densita’ di probabilita’ per **trovare la posizione piu’ probabile del bersaglio**.

In parole semplici:
Prima si fornisce all’algoritmo una “regione bersaglio iniziale”. Esso calcola le caratteristiche cromatiche di questa regione (es. l’istogramma colore del bersaglio), e poi in ogni frame successivo trova l’area piu’ simile a quel colore e sposta il rettangolo li’.

Questo processo non si basa sul deep learning e non richiede pre-addestramento: e’ molto leggero.

.. image:: img/opencv_meanshift.png
   :alt: Tracciamento MeanShift
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
      python3 cv_5_meanshift.py

#. Quando esegui il programma, apparir'a una finestra OpenCV chiamata **MeanShift Tracker** che inizier'a a riprodurre il file video ``sample2.mp4``.

   Un rettangolo verde verr'a disegnato attorno all'oggetto bersaglio e aggiornato in tempo reale utilizzando l'algoritmo di tracciamento MeanShift.

   La finestra di tracciamento si sposter'a mentre l'oggetto si muove nel video.

   Puoi uscire dal programma in due modi:

   * Premere il tasto **q** sulla tastiera
   * Chiudere la finestra facendo clic sul pulsante di chiusura (X)

   Dopo l'uscita, la riproduzione video si ferma e tutte le finestre OpenCV vengono chiuse.

3. Codice Completo
------------------

Di seguito e' lo script completo di tracciamento MeanShift (``cv_5_meanshift.py``):

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Spiegazione
--------------

#. Aprire il file video:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Questo crea un oggetto di acquisizione video in modo che OpenCV possa leggere i frame dal file.

#. Leggere il primo frame e assicurarsi che funzioni:

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   Il tracciamento MeanShift necessita di un frame iniziale per imparare cosa tracciare.

#. Impostare la finestra di tracciamento iniziale (l'oggetto che si desidera tracciare):

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   Questo rettangolo e' la posizione iniziale del bersaglio (ROI).
   Di solito si regolano questi valori per corrispondere all'oggetto nel primo frame.

#. Convert the first frame to HSV and extract the ROI:

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV e' comunemente usato per il tracciamento perche' il canale Hue descrive il colore in modo piu' consistente di RGB/BGR.

#. Build a mask to ignore weak/invalid pixels in the ROI:

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   Questo filtra i pixel con saturazione/valore molto bassi (spesso ombre o rumore), migliorando la stabilita' del tracciamento.

#. Calcolare e normalizzare l’istogramma ROI (canale Hue):

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - L’istogramma descrive la distribuzione del colore del bersaglio (Hue).
   - La normalizzazione rende la scala dell’istogramma consistente tra diverse condizioni di illuminazione o dimensioni ROI.

#. Definire i criteri di terminazione per MeanShift:

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift si fermer' a quando:
   - raggiunge 15 iterazioni, oppure
   - il movimento della finestra e' inferiore a 2 pixel.

#. Set a playback delay based on the video FPS:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Questo mantiene la riproduzione vicina alla velocita' video originale.
   Se gli FPS non possono essere letti, viene utilizzato il valore predefinito di 30 FPS.

#. Convertire ogni frame in HSV (per il tracciamento):

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   Il tracciamento viene eseguito in HSV in modo da poter confrontare l’istogramma Hue del bersaglio.

#. Back projection (trovare dove probabilmente si trova il colore del bersaglio):

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   La back projection produce una mappa di probabilita': le aree luminose hanno maggiori probabilita' di corrispondere all'istogramma ROI.

#. Aggiornare la finestra di tracciamento usando MeanShift:

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift sposta la finestra di tracciamento verso l'area a piu' alta densita' nella mappa di probabilita', aggiornando la posizione del bersaglio frame per frame.

#. Disegnare il risultato del tracciamento:

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   Questo disegna il rettangolo di tracciamento corrente sul frame video.

#. Visualizzare la finestra e le condizioni di uscita:

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - Premi ``q`` per uscire.
   - Chiudere la finestra permette anche di uscire in modo sicuro.

#. Rilasciare le risorse:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Rilascia sempre il video e chiudi le finestre per liberare le risorse di sistema.

5. MeanShift vs CAMShift
------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Caratteristica
     - MeanShift
     - CAMShift
   * - Dimensione finestra
     - Fissa
     - Auto-aggiustamento (si adatta alla scala del bersaglio)
   * - Bersaglio rotante
     - Non supportato
     - Supportato
   * - Scenari adatti
     - Dimensione bersaglio relativamente stabile
     - Il bersaglio puo' scalare/ruotare
   * - Applicazioni
     - Tracciamento semplice, palle, marcatori
     - Tracciamento pratico, sorveglianza, riconoscimento


6. Avanzato: Selezionare ROI con il Mouse
-----------------------------------------

In precedenza, abbiamo usato valori fissi:

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

E’ semplice ma non flessibile.
Se cambi video o il bersaglio inizia altrove, dovresti modificare il codice.

OpenCV fornisce ``cv2.selectROI`` in modo da poter **selezionare la regione bersaglio interattivamente sul primo frame** con il mouse, e il programma otterr’a ``(x, y, w, h)`` automaticamente.

**Codice di inizializzazione modificato**

Esegui ``cv_5_meanshift_auto.py`` per il codice modificato.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

Quando esegui il programma, il primo frame del video verr’a visualizzato e ti verr’a chiesto di selezionare una Regione di Interesse (ROI) usando il mouse.

Trascina il mouse per disegnare un rettangolo attorno all’oggetto bersaglio, poi premi **Enter** o **Space** per confermare la selezione.
Premi **Esc** per annullare la selezione.

Dopo aver confermato la ROI, apparir’a una finestra chiamata **MeanShift Tracker**.
L’oggetto selezionato verr’a tracciato con un rettangolo verde, e il riquadro si sposter’a mentre l’oggetto si muove nel video.

Per fermare il programma:

* Premi il tasto **q** sulla tastiera
* Oppure chiudi la finestra usando il pulsante di chiusura (X)

Dopo l’uscita, la riproduzione video si ferma e tutte le finestre OpenCV vengono chiuse.

.. image:: img/opencv_meanshift_mouse.png
   :alt: Finestra interattiva di selezione ROI
   :align: center

**Note**

``cv2.selectROI’’ e’ il selettore ROI interattivo integrato di OpenCV, ideale per l’inizializzazione manuale.
Restituisce ``(x, y, w, h)``, che e’ completamente compatibile con ``track_window``, quindi non e’ necessario modificare la logica principale di CAMShift/MeanShift.
Questo permette di riutilizzare lo stesso programma su diversi video e bersagli.


7. Avanzato II: Calcolare Dinamicamente le Soglie HSV per la ROI
----------------------------------------------------------------

Il file originale ``cv_5_meanshift.py`` utilizza soglie HSV impostate manualmente, adatte quando il colore del bersaglio e’ fisso e l’illuminazione e’ stabile.


.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

Se l’illuminazione varia significativamente o il colore del bersaglio non e’ fisso, i limiti ``inRange`` hard-coded potrebbero non essere ottimali.
Un approccio piu’ intelligente e’ **calcolare automaticamente i limiti HSV inferiore/superiore dalla ROI selezionata**.

**Esempio: Calcolo automatico delle soglie HSV**

Esegui ``cv_5_meanshift_auto.py`` per il codice modificato.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

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


Quando si selezionano bersagli molto scuri o molto luminosi, non e' piu' necessario modificare manualmente le soglie; si adatta anche rapidamente a diverse condizioni di illuminazione e colori.

.. note::

   - ``np.percentile`` (5%–95%) taglia gli estremi (bordi, ombre, luci, ecc.) all'interno della ROI, migliorando la robustezza.
   - ``pad_h``, ``pad_s``, ``pad_v`` forniscono tolleranza in modo che lievi variazioni di colore siano ancora catturate.
   - ``lower`` e ``upper`` sono i limiti HSV dinamici usati direttamente con ``cv2.inRange``.


**Riepilogo**

- Usa ``cv2.selectROI`` per un'inizializzazione flessibile del bersaglio.
- Usa ``np.percentile`` per calcolare automaticamente i limiti HSV per l'adattabilita'.
- Combinato con ``cv2.inRange`` e CAMShift/MeanShift, questo approccio rimane stabile in condizioni di illuminazione difficili e variazioni del bersaglio.
