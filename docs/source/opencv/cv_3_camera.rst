.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Acquisizione Fotocamera in Tempo Reale
==========================================

Nei capitoli precedenti, abbiamo imparato come leggere e riprodurre file video locali.
In questo capitolo, faremo un passo avanti utilizzando la **fotocamera Raspberry Pi** per l'acquisizione video in tempo reale e applicheremo la **conversione dello spazio colore** con OpenCV.


1. Obiettivi del Progetto
-------------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

- Usare **Picamera2** per acquisire frame dalla fotocamera in tempo reale
- Convertire l'output della fotocamera dal formato BGRA al formato BGR
- Usare OpenCV per l'anteprima in tempo reale
- Comprendere le caratteristiche e i casi d'uso dei diversi spazi colore

.. image:: img/opencv_camera.png
   :alt: Illustrazione dell'anteprima della fotocamera in tempo reale
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
      python3 cv_3_camera.py

#. Quando esegui il programma, appariranno due finestre OpenCV:

   * **BGR Frame** – mostra l'immagine a colori in diretta dalla fotocamera
   * **GRAY Frame** – mostra la versione in scala di grigi della stessa immagine

   Puoi uscire dal programma in due modi:

   * Premere il tasto **q** sulla tastiera
   * Chiudere una qualsiasi finestra facendo clic sul pulsante di chiusura (X)

   Dopo l'uscita, la fotocamera smette di trasmettere e tutte le finestre OpenCV vengono chiuse.

3. Codice di Esempio
--------------------

Di seguito e' l'esempio Python completo per questo capitolo (``cv_3_camera.py``):

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. Spiegazione del Codice
-------------------------

#. Importare le librerie necessarie:

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2 cattura i frame dalla fotocamera Raspberry Pi, mentre OpenCV viene utilizzato per la conversione e la visualizzazione delle immagini.

#. Creare un oggetto Picamera2 e configurare la fotocamera:

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   Questo avvia la fotocamera a 640×480.
   ``XRGB8888`` e' un formato a 4 canali, quindi ogni frame catturato e' di tipo BGRA.

#. Acquisire un frame come array NumPy:

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   Ogni ciclo legge un frame dalla fotocamera.

#. Convertire il frame per la visualizzazione:

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr`` viene utilizzato per la visualizzazione a colori normale.
   - ``frame_gray`` e' una versione in scala di grigi dello stesso frame.

#. Display the frames in two windows:

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   Questo apre due finestre OpenCV: una mostra il frame a colori, l'altra mostra il frame in scala di grigi.

#. Exit conditions (press ``q`` or close a window):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - Premi ``q`` per uscire.
   - Chiudere una qualsiasi finestra fermera' il programma in modo sicuro.

#. Limitare gli FPS per ridurre l'uso della CPU:

   .. code-block:: python

      time.sleep(1 / 30)

   Questo aggiunge un piccolo ritardo in modo che il ciclo venga eseguito a circa 30 FPS, riducendo il carico della CPU su Raspberry Pi.

#. Fermare la fotocamera e chiudere le finestre OpenCV:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Questo rilascia la fotocamera e chiude tutte le finestre OpenCV prima che il programma termini.

5. L'Importanza della Conversione dello Spazio Colore
=====================================================

Il formato immagine grezzo in uscita dalla fotocamera potrebbe non corrispondere sempre al formato richiesto da OpenCV per l'elaborazione.
In questo esempio, Picamera2 produce immagini in formato **XRGB8888 (BGRA)**, mentre OpenCV utilizza principalmente il formato **BGR**.

Pertanto, dobbiamo convertire l'immagine come segue:

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

Questo garantisce che l'immagine sia organizzata nell'ordine standard dei canali BGR utilizzato da OpenCV, consentendone la corretta visualizzazione ed elaborazione.

Possiamo quindi convertire l'immagine BGR in scala di grigi per ulteriori elaborazioni:

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

Questo ci permette di trasformare le immagini catturate dalla fotocamera in un formato adatto ai flussi di lavoro di elaborazione immagini di OpenCV.

**Spazi Colore Comuni e Casi d'Uso**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Spazio Colore
     - Caratteristiche
     - Casi d'Uso Tipici
   * - **BGR**
     - Formato predefinito di OpenCV
     - Visualizzazione immagini, elaborazione di base, rilevamento bordi
   * - **RGB**
     - Intuitivo per la percezione umana
     - Visualizzazione, input immagini per deep learning
   * - **GRAY**
     - Immagine in scala di grigi a canale singolo
     - Rilevamento oggetti, rilevamento bordi, ottimizzazione prestazioni
   * - **HSV**
     - Separa colore e luminosita'
     - Rilevamento colore, tracciamento oggetti, segmentazione
   * - **YCrCb**
     - Separa luminanza e crominanza
     - Rilevamento volti, compressione video, robustezza all'illuminazione

Ad esempio, **HSV** e' spesso migliore per il **rilevamento colore e il tracciamento oggetti**,
mentre **YCrCb** e' piu' robusto nel **riconoscimento facciale** o in **scene con illuminazione variabile**.

6. Estensioni ed Esercizi
=========================

- Prova a convertire da BGR a GRAY o HSV e osserva i risultati.

   Ad esempio, usa:

   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
   - e altri

- Prova diverse risoluzioni (es. 1280×720) e osserva l'effetto sulla latenza e sul frame rate.
- Combina questo codice con l'esempio precedente di riproduzione video per implementare il passaggio tra un flusso della fotocamera e una sorgente video.
