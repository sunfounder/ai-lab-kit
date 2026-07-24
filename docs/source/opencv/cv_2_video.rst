.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. Riprodurre un Video
======================

In questo capitolo, imparerai come leggere e riprodurre flussi video in OpenCV e come controllare la velocita’ di riproduzione calcolando il tempo di elaborazione dei frame.



1. Panoramica del Progetto
--------------------------

In questa sezione, raggiungeremo i seguenti obiettivi:

- Usare ``cv2.VideoCapture`` per aprire un file video
- Leggere e visualizzare il video frame per frame
- Riavviare automaticamente il video dopo la sua conclusione
- Controllare il frame rate di riproduzione usando calcoli del tempo di elaborazione
- Premere il tasto ``q`` per uscire dalla riproduzione

.. image:: img/opencv_video.png
   :alt: Illustrazione dell'interfaccia di riproduzione video
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
      python3 cv_2_video.py

#. Dopo aver eseguito lo script, OpenCV apre una finestra intitolata **Video** e visualizza i frame video in tempo reale.

   Se il video raggiunge la fine, si riavvia automaticamente dall'inizio.

   Per fermare il programma, puoi:

   * Premere **q** sulla tastiera per uscire dalla riproduzione
   * Chiudere la finestra facendo clic sul pulsante di chiusura

   Una volta chiusa la finestra, tutte le risorse di OpenCV vengono rilasciate e il programma termina.


3. Codice Completo
------------------

.. code-block:: python

  import cv2

  # Open the video file
  cap = cv2.VideoCapture("sample2.mp4")

  while True:
      # Read one frame from the video
      ret, frame = cap.read()

      # If the video ends, restart from the beginning
      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

      # Resize the frame for better display performance
      frame = cv2.resize(frame, (640, 480))

      # Display the frame in a window named "Video"
      cv2.imshow("Video", frame)

      # Wait 30 ms between frames (~30 FPS)
      # This also processes GUI events (keyboard and window events)
      key = cv2.waitKey(30) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
          break

      # Exit if the user closes the window (click the close button)
      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

  # Release the video capture object
  cap.release()

  # Close all OpenCV windows
  cv2.destroyAllWindows()


4. Spiegazione del Codice
-------------------------

#. Aprire il file video:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Questo apre il file video e crea un oggetto ``VideoCapture`` per la lettura dei frame.

#. Leggere un frame dal video:

   .. code-block:: python

      ret, frame = cap.read()

   - ``ret`` e' ``True`` se un frame viene letto correttamente.
   - ``ret`` diventa ``False`` quando il video termina o la lettura fallisce.
   - ``frame`` sono i dati dell'immagine (un array NumPy).

#. Loop the video when it ends:

   .. code-block:: python

      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

   Quando il video termina, questo reimposta la posizione di riproduzione al primo frame in modo che il video possa riavviarsi.

#. Resize the frame:

   .. code-block:: python

      frame = cv2.resize(frame, (640, 480))

   Questo ridimensiona ogni frame a 640×480 per una visualizzazione piu' fluida e un minore utilizzo della CPU su Raspberry Pi.

#. Visualizzare il frame:

   .. code-block:: python

      cv2.imshow("Video", frame)

   Questo visualizza il frame corrente in una finestra chiamata ``Video``.

#. Controllare la velocita' di riproduzione e leggere l'input da tastiera:

   .. code-block:: python

      key = cv2.waitKey(30) & 0xFF

   Questo attende circa 30 ms tra i frame (circa 30 FPS) e processa gli eventi GUI.

#. Uscire premendo ``q``:

   .. code-block:: python

      if key == ord("q"):
          break

   Premi ``q`` per fermare il programma.

#. Uscire quando la finestra viene chiusa:

   .. code-block:: python

      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

   Questo controlla se la finestra e' ancora visibile.
   Se l'utente chiude la finestra, il programma termina in modo sicuro.

#. Rilasciare l'oggetto di acquisizione video:

   .. code-block:: python

      cap.release()

   Questo rilascia la risorsa del file video.

#. Chiudere tutte le finestre di OpenCV:

   .. code-block:: python

      cv2.destroyAllWindows()

   Questo chiude tutte le finestre di OpenCV e rilascia le risorse GUI.


5. Ulteriori Esercizi
---------------------

- Prova a cambiare la dimensione della finestra per vedere come influisce sulla nitidezza dell'immagine.
- Sostituisci il file video con uno diverso per testare la compatibilita'.
- Stampa il tempo di elaborazione per frame per comprendere meglio la relazione tra FPS e ritardo di riproduzione.
