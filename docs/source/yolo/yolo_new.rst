.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Eseguire YOLO su Raspberry Pi
===============================================================

YOLO (You Only Look Once) è un rivoluzionario algoritmo di rilevamento oggetti caratterizzato da velocità e precisione. Trasforma il rilevamento oggetti in un problema di regressione, prevedendo tutte le categorie e le posizioni degli oggetti in un'immagine attraverso un unico passaggio in avanti della rete neurale.

Immaginalo come un sistema di visione che può "vedere tutto a colpo d'occhio." Che si tratti di videosorveglianza, guida autonoma o controllo qualità industriale, YOLO è presente ovunque sia necessario il rilevamento oggetti in tempo reale.

.. image:: img/yolo_new.png

Figura: YOLOv8n eseguito in tempo reale su Raspberry Pi. Gli oggetti nel flusso della fotocamera vengono rilevati e annotati con precisione, con le classi rilevate e i punteggi di confidenza visualizzati a sinistra. Questa immagine mostra il modello che identifica con successo oggetti come una persona, una sedia e una TV.

Principi Fondamentali
------------------------------------------

A differenza dei metodi precedenti a due stadi (come R-CNN) che "prima trovano le regioni candidate e poi le identificano," YOLO adotta un approccio fondamentalmente diverso:

* **Framework Unificato**: Divide l'immagine in una griglia (ad esempio, la griglia originale 7x7).

* **Predizione a Griglia**: Ogni cella della griglia è responsabile della predizione degli oggetti il cui centro cade all'interno di quella cella. Ogni cella prevede multipli bounding box (inclusi posizione e dimensione) insieme ai loro punteggi di confidenza, e prevede anche le probabilità delle classi degli oggetti.

* **Completamento a Stadio Unico**: Classificazione e localizzazione sono realizzate simultaneamente all'interno della stessa rete neurale, ottenendo veramente "you only look once," superando così significativamente i metodi precedenti in velocità.


Esecuzione del Codice
------------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_test.py

Il codice scaricherà automaticamente un modello (circa 6MB) e lo eseguirà sulla fotocamera. I risultati verranno visualizzati in una finestra con il titolo "YOLOv8".

(il primo avvio scaricherà automaticamente un modello di circa 6MB):

.. code-block:: python

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")  # nano model

   # initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLO start, Press 'q' to exit...")

   try:
      while True:
         # capture frame
         frame = picam2.capture_array()

         # run YOLO and set imgsz=320
         results = model(frame, imgsz=320)

         # draw results
         annotated = results[0].plot()

         # show results
         cv2.imshow("YOLO on Raspberry Pi", annotated)

         # press 'q' to exit
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("exit")



Risoluzione dei Problemi
-------------------------

D: Se si incontra l'errore Numpy.dtype size changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Degradare la versione di Numpy:

.. code-block:: bash

   # If version is 2.x, downgrade to 1.x
   pip3 install "numpy<2.0" --break-system-packages --force-reinstall

D: Se si incontra l'errore di libreria mancante ``libopenblas.so.0``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installare la libreria OpenBLAS:

.. code-block:: bash

   sudo apt install libopenblas-dev

D: Se la fotocamera non può essere aperta
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Controllare la connessione della fotocamera e assicurarsi che sia abilitata:

.. code-block:: bash

   sudo raspi-config
   # Select Interface Options -> Camera -> Enable

D: Se si incontrano errori di memoria insufficiente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aumentare lo spazio di swap:

.. code-block:: bash

   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Modify CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon

Metodi di Ottimizzazione delle Prestazioni
--------------------------------------------------------

Eseguire YOLO su un Raspberry Pi (anche 4B/5) può essere impegnativo. Ecco diversi metodi di ottimizzazione collaudati:

1. **Regolare la Risoluzione di Inferenza YOLO**: Il codice sopra utilizza già imgsz=320, che è un'impostazione equilibrata. Valori regolabili:

   * ``imgsz=224`` - Risoluzione più bassa, velocità massima
   * ``imgsz=320`` - Scelta standard
   * ``imgsz=416`` - Precisione più alta, velocità inferiore
   * ``imgsz=640`` - Precisione massima, molto lento su Raspberry Pi

2. **Scegliere il Modello Giusto**:

   * ``yolov8n.pt`` (6MB) - Più veloce, adatto per rilevamento in tempo reale
   * ``yolov8s.pt`` (22MB) - Leggermente più lento ma più accurato
   * ``yolov8m.pt`` (49MB) - Più lento, maggiore precisione
   * ``yolov8l/x.pt`` - Generalmente inutilizzabile su Raspberry Pi
   * Puoi anche usare il tuo modello addestrato, ad esempio ``"/home/pi/my_model.pt"``. Tratteremo come addestrare modelli personalizzati nei capitoli successivi.

3. **Limitare le Classi di Rilevamento**: Se si rilevano solo oggetti specifici (ad esempio, solo persone), modificare il codice:

.. code-block:: python

   results = model(frame, classes=[0], imgsz=320)  # 0 is the class ID for person

ID delle classi comuni:

   * 0 - person
   * 1 - bicycle
   * 2 - car
   * 3 - motorcycle
   * 5 - bus
   * 7 - truck

4. **Utilizzare Varianti di Modello Leggere**:

.. code-block:: python

   # Use pruned version of YOLOv8n (if available)
   model = YOLO("yolov8n.pt")

   # Or use TensorRT acceleration (requires additional configuration)
   # model = YOLO("yolov8n.pt")
   # model.export(format="engine")  # Export as TensorRT engine

5. **Ridurre l'Elaborazione dei Fotogrammi**: Se non è necessaria la visualizzazione in tempo reale di tutti i fotogrammi, elaborarli in modo intermittente:

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()

       # Process every 3rd frame
       if frame_count % 3 == 0:
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           cv2.imshow("YOLO on Raspberry Pi", annotated)

       frame_count += 1

       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

6. **Utilizzare il Multi-threading**: Separare l'acquisizione della fotocamera e l'inferenza YOLO in thread diversi:

.. code-block:: python

   import threading
   import queue

   frame_queue = queue.Queue(maxsize=2)
   result_queue = queue.Queue(maxsize=2)

   def capture_frames():
       while True:
           frame = picam2.capture_array()
           if frame_queue.full():
               frame_queue.get()
           frame_queue.put(frame)

   def process_frames():
       while True:
           frame = frame_queue.get()
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           if result_queue.full():
               result_queue.get()
           result_queue.put(annotated)

   # Start threads
   threading.Thread(target=capture_frames, daemon=True).start()
   threading.Thread(target=process_frames, daemon=True).start()

   while True:
       if not result_queue.empty():
           cv2.imshow("YOLO on Raspberry Pi", result_queue.get())
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

Utilizzo Avanzato
--------------------------------

Utilizzare File Video come Input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")
   cap = cv2.VideoCapture("input_video.mp4")

   while cap.isOpened():
       ret, frame = cap.read()
       if not ret:
           break

       results = model(frame, imgsz=320)
       annotated = results[0].plot()
       cv2.imshow("YOLO Detection", annotated)

       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   cap.release()
   cv2.destroyAllWindows()

Riepilogo
------------------

Attraverso questo tutorial, hai imparato:

* Come configurare l'ambiente YOLO su Raspberry Pi
* Come eseguire il rilevamento oggetti in tempo reale utilizzando la fotocamera
* Come risolvere problemi comuni di installazione e runtime
* Vari metodi per ottimizzare le prestazioni di rilevamento

La potenza di YOLO risiede nella sua semplicità ed efficienza, consentendo prestazioni di rilevamento oggetti rispettabili anche su dispositivi embedded come il Raspberry Pi. Continuando a esplorare, puoi costruire varie applicazioni interessanti come sorveglianza intelligente, tracciamento oggetti e conteggio persone.
