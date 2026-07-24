.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Mostrare un'Immagine
=======================

In questo capitolo, esploreremo un semplice esempio per aiutarti a sperimentare rapidamente l’uso base di OpenCV: **leggere e visualizzare un’immagine**.

Nella cartella del progetto di esempio, abbiamo gia’ preparato una foto di esempio chiamata ``my_photo.jpg``.
Puoi anche usare l’esempio :ref:`py_photograph` per scattare una foto e salvarla nella cartella corrente.


1. Panoramica del Progetto
--------------------------

In questa sezione, realizzeremo i seguenti compiti:

- Usare ``cv2.imread`` per leggere un'immagine locale
- Usare ``cv2.imshow`` per visualizzare l'immagine
- Usare ``cv2.waitKey`` per controllare il comportamento della finestra
- Usare ``cv2.destroyAllWindows`` per chiudere la finestra

Dopo aver eseguito con successo questo codice, una finestra dell'immagine apparira' sullo schermo.

.. image:: img/opencv_imshow.png
   :alt: Anteprima del risultato
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
      python3 cv_1_imgshow.py

#. Dopo aver eseguito lo script, OpenCV apre una finestra intitolata ``Picture`` e visualizza l'immagine caricata da ``my_photo.jpg``.

   La finestra rimarra' aperta fino a quando l'utente non chiude il programma.

   Per uscire dal programma, puoi:

   * Premere **q** sulla tastiera
   * Chiudere la finestra facendo clic sul pulsante di chiusura

   Una volta chiusa la finestra, tutte le risorse di OpenCV vengono rilasciate e il programma termina.

3. Codice Completo
------------------

.. code-block:: python

   # Python code to read and display an image using OpenCV
   import cv2
   from pathlib import Path

   # Get the directory of the current Python file
   BASE_DIR = Path(__file__).resolve().parent

   # Read image from disk
   # cv2.imread loads the image as a NumPy array
   img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

   # Create a GUI window to display the image
   # First parameter: window title
   # Second parameter: image array
   cv2.imshow("Picture", img)

   # Keep the window open until the user closes it or presses 'q'
   # cv2.waitKey only listens for keyboard events, not the close button
   # Therefore, we use a loop to detect both window close and key press
   while True:
      # Check if the window has been closed
      if cv2.getWindowProperty("Picture", cv2.WND_PROP_VISIBLE) < 1:
         break

      # Wait for 1 ms and check for key press
      # Press 'q' to exit the program
      if cv2.waitKey(1) & 0xFF == ord("q"):
         break

   # Destroy all OpenCV windows and release memory
   cv2.destroyAllWindows()

4. Spiegazione del Codice
-------------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``

  Legge l'immagine chiamata ``my_photo.jpg`` e la carica in modalita' colore.

- ``cv2.imshow(“Picture”, img)``

  Crea una finestra intitolata “Picture” e visualizza l'immagine.

- ``cv2.waitKey(0)``

  Quando il parametro e' ``0``, il programma attendera' indefinitamente fino a quando non si chiude la finestra o si preme un tasto.

- ``cv2.getWindowProperty()``

  Ottiene un valore di proprieta' della finestra specificata (ad esempio, se la finestra e' ancora visibile).


- ``cv2.destroyAllWindows()``

  Chiude tutte le finestre di OpenCV e rilascia le risorse.

5. Ulteriori Esercizi
---------------------

- Prova a cambiare il titolo della finestra in ``imshow`` impostandolo a “My First OpenCV Window”.
- Sostituisci l'immagine con una diversa e osserva il risultato.
- Modifica il parametro di ``waitKey`` a `3000` in modo che il programma chiuda automaticamente la finestra dopo 3 secondi.
