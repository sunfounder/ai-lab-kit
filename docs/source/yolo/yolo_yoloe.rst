.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. Rilevare Qualsiasi Cosa con YOLOE
===========================================


YOLOE (You Only Look Once with Embeddings) è l'ultimo membro della famiglia YOLO, introducendo capacità di apprendimento congiunto linguaggio-visione al tradizionale YOLO. In parole semplici, YOLOE non solo può rilevare oggetti su cui è stato addestrato, ma può anche rilevare nuovi oggetti arbitrari attraverso descrizioni testuali o prompt senza riaddestramento.

Caratteristiche principali di YOLOE:

* **Rilevamento a vocabolario aperto**: Rilevare oggetti arbitrari attraverso descrizioni testuali, non limitato a categorie predefinite
* **Modalità Prompt-Free**: Rilevare automaticamente oggetti salienti nelle immagini senza alcun prompt
* **Distribuzione efficiente**: Eredita l'architettura efficiente di YOLO, funziona senza problemi su Raspberry Pi
* **Supporto multi-attività**: Supporta varie attività tra cui rilevamento oggetti e segmentazione di istanze

Questo rende YOLOE particolarmente adatto per prototipazione rapida e applicazioni che richiedono il rilevamento flessibile di vari oggetti.

Installare le Dipendenze
---------------------------------------------------

Per prima cosa, installare la libreria CLIP richiesta da YOLOE:

.. code-block:: bash

   pip3 install git+https://github.com/ultralytics/CLIP.git --break-system-packages

Modalità Prompt-Free
-----------------------------

La modalità Prompt-Free è il modo più intuitivo per utilizzare YOLOE. In questa modalità, il modello rileva automaticamente tutti gli oggetti salienti nell'immagine senza alcun prompt testuale. Si comporta in modo simile allo YOLO tradizionale ma con migliori capacità di vocabolario aperto.

.. image:: img/yolo_prompt_free1.png

Figura: Ho puntato la fotocamera verso la mia scrivania disordinata, e la modalità Prompt-Free di YOLOE ha automaticamente identificato e segmentato tutti gli oggetti salienti in vista—monitor, tastiera, bicchiere d'acqua, taccuino, mouse... Ogni oggetto è annotato con una maschera di segmentazione di colore diverso, senza richiedere alcun prompt testuale. Tutto è presentato chiaramente a colpo d'occhio.

**Come funziona**: Il modello identifica automaticamente gli oggetti in primo piano nell'immagine attraverso l'analisi delle caratteristiche visive e esegue la segmentazione. Questo approccio è adatto per sfogliare rapidamente il contenuto dell'immagine o quando non sei sicuro di quali oggetti devono essere rilevati.

Il seguente codice dimostra come eseguire YOLOE in modalità Prompt-Free su un Raspberry Pi:

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_free.py

.. code-block:: python

   from ultralytics import YOLO 
   from picamera2 import Picamera2
   import cv2

   # prompt-free mode
   model = YOLO("yoloe-11s-seg-pf.pt")  # pf = prompt-free

   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("Prompt-free mode: detecting everything automatically...")
   print("Press 'q' to exit")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, imgsz=320)
      annotated = results[0].plot()
      cv2.imshow("YOLOE Prompt-Free", annotated)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**Caratteristiche della Modalità Prompt-Free**:

* **Nessuna configurazione necessaria**: Eseguire direttamente per rilevare oggetti salienti nelle immagini
* **Segmentazione automatica**: Produce sia bounding box che maschere di segmentazione
* **Nessuna etichetta di classe**: Mostra solo le posizioni degli oggetti rilevati senza nomi di categoria
* **Casi d'uso**: Navigazione rapida, rilevamento oggetti generale, scoperta di oggetti sconosciuti

Modalità Prompt Testuale
----------------------------------

La modalità prompt testuale è dove la potenza di YOLOE brilla veramente. Attraverso descrizioni in linguaggio naturale, puoi dire al modello quali oggetti rilevare, e il modello identificherà e localizzerà questi oggetti in tempo reale.

.. image:: img/yolo_prompt_word.png

Figura: Ho tenuto un pezzo di carta metà giallo e metà bianco davanti alla fotocamera, e ho usato un prompt testuale per dire al modello di cercare "yellow paper". YOLOE ha compreso accuratamente questa descrizione, segmentando solo la metà gialla della carta e segnandola con un bounding box, ignorando completamente la porzione bianca. Questo dimostra la capacità di YOLOE di eseguire un riconoscimento oggetti fine-grained attraverso il linguaggio naturale.

**Come funziona**: Il modello codifica i prompt testuali in vettori di caratteristiche, poi li confronta con le caratteristiche dell'immagine per identificare le regioni che corrispondono meglio alle descrizioni testuali. Questo approccio ti permette di specificare dinamicamente i bersagli di rilevamento senza riaddestrare il modello.

Il seguente codice dimostra come utilizzare i prompt testuali per rilevare oggetti specifici:

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_text.py

.. code-block:: python

   from ultralytics import YOLOE
   from picamera2 import Picamera2
   import cv2

   # load YOLOE model
   model = YOLOE("yoloe-26n-seg.pt")  # nano version

   # set the classes to detect (text prompt)
   names = ["yellow paper", "red cup", "person wearing glasses"]
   model.set_classes(names, model.get_text_pe(names))

   # initialize the camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLOE running with text prompts, press 'q' to exit...")
   print(f"Detecting: {', '.join(names)}")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, conf=0.3)  # set confidence threshold to 0.3
      annotated = results[0].plot()
      cv2.imshow("YOLOE on Raspberry Pi", annotated)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**Caratteristiche della Modalità Prompt Testuale**:

* **Rilevamento dinamico**: Modificare i bersagli di rilevamento in qualsiasi momento senza riaddestramento
* **Linguaggio naturale**: Usare il linguaggio quotidiano per descrivere oggetti, come "blue car", "wooden chair"
* **Rilevamento multi-bersaglio**: Specificare più bersagli di rilevamento contemporaneamente
* **Controllo fine-grained**: Descrivere attributi come colore, materiale, forma, ecc.
* **Soglia di confidenza**: Controllare la sensibilità del rilevamento attraverso il parametro ``conf``

Utilizzo Avanzato
-------------------------------------

**Cambiare Dinamicamente i Bersagli di Rilevamento**

Puoi modificare i prompt testuali durante l'esecuzione senza riavviare il programma:

.. code-block:: python

   # Initialize model
   model = YOLOE("yoloe-26n-seg.pt")
   
   # Initial detection targets
   current_names = ["red apple"]
   model.set_classes(current_names, model.get_text_pe(current_names))
   
   while True:
      frame = picam2.capture_array()
      
      # Check if detection target needs to be switched
      key = cv2.waitKey(1) & 0xFF
      if key == ord('1'):
         current_names = ["banana"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: banana")
      elif key == ord('2'):
         current_names = ["orange"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: orange")
      
      results = model.predict(frame, conf=0.3)
      annotated = results[0].plot()
      cv2.imshow("YOLOE", annotated)
      
      if key == ord('q'):
         break

**Usare Descrizioni Testuali più Complesse**

YOLOE supporta descrizioni complesse in linguaggio naturale per una localizzazione più precisa degli oggetti:

.. code-block:: python

   # More precise description examples
   names = [
       "person wearing a red hat",
       "car with open door",
       "small dog on the left side",
       "yellow paper on the desk"
   ]
   model.set_classes(names, model.get_text_pe(names))

**Regolare i Parametri di Rilevamento**

Ottimizzazione delle prestazioni per Raspberry Pi:

.. code-block:: python

   # Performance optimization configuration
   results = model.predict(
       frame, 
       imgsz=224,        # Lower resolution for faster speed
       conf=0.4,         # Higher confidence threshold reduces false positives
       iou=0.5,          # Adjust IOU threshold
       verbose=False     # Disable verbose output
   )

Suggerimenti per l'Ottimizzazione delle Prestazioni
---------------------------------------------------

Quando si esegue YOLOE su Raspberry Pi, le seguenti ottimizzazioni possono aiutare a ottenere migliori prestazioni:

1. **Scegliere il modello giusto**:

   - ``yoloe-26n-seg.pt``: Versione nano, massima velocità
   - ``yoloe-11s-seg-pf.pt``: Versione S, maggiore precisione ma più lenta

2. **Ridurre la risoluzione di input**:

   - ``imgsz=224``: Massima velocità
   - ``imgsz=320``: Scelta equilibrata (consigliata)
   - ``imgsz=416``: Maggiore precisione

3. **Regolare la soglia di confidenza**:

   - Aumentare il parametro ``conf`` (ad esempio, a 0.5) riduce il numero di rilevamenti e migliora la velocità

4. **Ridurre le categorie di rilevamento**:

   - Nella modalità prompt testuale, limitare la lunghezza della lista ``names`` può migliorare la velocità di inferenza

FAQ
-------------------------

**D: Qual è la differenza tra YOLOE e YOLO tradizionale?**

R: Lo YOLO tradizionale può rilevare solo categorie fisse definite durante l'addestramento, mentre YOLOE può rilevare oggetti arbitrari attraverso prompt testuali senza riaddestramento.

**D: La modalità Prompt-Free rileva tutti gli oggetti?**

R: La modalità Prompt-Free rileva gli oggetti visivamente salienti nell'immagine ma non fornisce etichette di categoria, rendendola adatta per sfogliare rapidamente le scene.

**D: Il prompt testuale supporta il cinese?**

R: Si consigliano prompt in inglese per risultati migliori, poiché il modello è principalmente addestrato su dati inglesi.

**D: Qual è la velocità di esecuzione di YOLOE su Raspberry Pi?**

R: Su Raspberry Pi 5, utilizzando il modello nano con risoluzione 320, si possono ottenere prestazioni in tempo reale di 3-5 FPS.

**D: Posso usare più prompt testuali simultaneamente?**

R: Sì, è sufficiente aggiungere più descrizioni alla lista ``names``, e il modello rileverà tutti questi oggetti simultaneamente.