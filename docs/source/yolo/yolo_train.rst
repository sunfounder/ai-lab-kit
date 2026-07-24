.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Addestrare il Tuo Modello YOLO Personalizzato
======================================================

Addestrare il proprio modello YOLO implica essenzialmente far apprendere all'algoritmo di deep learning come identificare oggetti specifici dai dati delle immagini che fornisci. Questo processo può essere paragonato all'insegnare a un bambino a riconoscere qualcosa di nuovo: gli mostri numerose immagini di esempio da diverse angolazioni e ambienti, dicendogli "questo è l'oggetto bersaglio." Dopo sufficienti esempi, può identificare accuratamente quell'oggetto in nuove immagini.

Per YOLO, il processo di addestramento funziona così:

1. **Preparazione dei Dati**: Raccogliere immagini contenenti gli oggetti bersaglio e annotare la posizione e la categoria di ciascun oggetto
2. **Apprendimento del Modello**: L'algoritmo apprende automaticamente i pattern caratteristici degli oggetti analizzando questi dati annotati
3. **Generazione dei Pesi**: Dopo il completamento dell'addestramento, genera un file modello (file .pt) contenente la conoscenza appresa
4. **Applicazione di Inferenza**: Distribuire questo modello sul Raspberry Pi per il rilevamento su nuove immagini

Grazie al transfer learning, non è necessario addestrare da zero. La piattaforma Ultralytics fornisce modelli di base pre-addestrati (come YOLOv8n) che sono stati addestrati su milioni di immagini. Dobbiamo solo "fare fine-tuning" di questi modelli con un piccolo numero di immagini proprie per creare modelli personalizzati efficaci.



----------------------------------------------------------

Acquisire Foto
------------------------------

Poiché il nostro progetto YOLO è basato su Raspberry Pi, utilizzeremo la fotocamera del Raspberry Pi per acquisire foto. Per risultati migliori, abbiamo anche utilizzato telefoni cellulari per acquisire alcune foto e aumentare la diversità dei dati.

**Suggerimenti per l'Acquisizione Foto**

* **Chiarezza**: Acquisire gli oggetti nel modo più chiaro possibile, evitando sfocature
* **Diversità**: Acquisire foto da diverse angolazioni (frontale, laterale, dall'alto, ecc.) e in diverse condizioni di illuminazione (luce intensa, scarsa illuminazione, controluce, ecc.)
* **Variazione dello Sfondo**: Provare ad acquisire immagini su sfondi diversi per aiutare il modello ad apprendere le caratteristiche essenziali degli oggetti piuttosto che degli sfondi
* **Evitare Sovrapposizioni**: Puoi acquisire più oggetti simultaneamente, ma evita sovrapposizioni significative tra gli oggetti
* **Quantità Raccomandata**: Puntare ad almeno 50-100 foto per categoria; più immagini producono risultati migliori

**Quale Oggetto Dovresti Usare?**

Puoi scegliere qualsiasi oggetto ti interessi per addestrare, come: una bambola, una tazza, una sedia, o persino il tuo animale domestico. Questo tutorial utilizza un pupazzo di neve giocattolo come esempio; sostituiscilo semplicemente con il tuo oggetto bersaglio.

.. image:: img/ultralytics_a1_capture_photo.png

**Acquisire Foto con la Fotocamera del Raspberry Pi**

Ecco il codice per acquisire foto utilizzando la fotocamera del Raspberry Pi:

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_capture_images.py

.. code-block:: python

   #!/usr/bin/env python3
   """
   Simple camera capture script for Raspberry Pi
   Press SPACE to capture, ESC to exit
   Images saved to ./captured_images/
   """

   from picamera2 import Picamera2
   import cv2
   import os
   import time

   # Create save directory
   save_dir = "captured_images"
   os.makedirs(save_dir, exist_ok=True)

   # Initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   # Wait for camera to warm up
   time.sleep(1)

   print("=== Camera Capture Tool ===")
   print(f"Images will be saved to: {save_dir}")
   print("Controls:")
   print("  SPACE - Capture image")
   print("  ESC   - Exit")
   print("==========================")

   count = 0

   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()
         
         # Display frame with instructions
         display = frame.copy()
         cv2.putText(display, f"Captured: {count} images", (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
         cv2.putText(display, "Press SPACE to capture, ESC to exit", (10, 60),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         cv2.imshow("Camera Capture", display)
         
         # Wait for key press
         key = cv2.waitKey(1) & 0xFF
         
         if key == 32:  # SPACE key
               # Save image
               filename = f"{save_dir}/img_{count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               count += 1
               
               # Optional: flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow("Camera Capture", flash)
               cv2.waitKey(50)
               
         elif key == 27:  # ESC key
               print(f"\nExiting. Total captured: {count} images")
               break

   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("Camera stopped")

**Trasferire le Immagini al Tuo Computer**

Dopo l'acquisizione, usa :ref:`filezilla` per scaricare le immagini dal Raspberry Pi al tuo computer:

1. Controllare l'indirizzo IP sul tuo Raspberry Pi: ``hostname -I``
2. Connettersi al Raspberry Pi in FileZilla (username: pi, password: la tua password)
3. Navigare alla directory ``~/ai-lab-kit/yolo/captured_images/``
4. Scaricare tutte le immagini sul tuo computer


----------------------------------------------------------


Addestrare il Modello
-------------------------------------------------

Utilizzeremo la piattaforma online `Ultralytics Platform <https://platform.ultralytics.com/>`_. Questa piattaforma fornisce servizi di addestramento modelli convenienti senza la necessità di configurare ambienti di addestramento complessi.

**Registrazione e Login**

1. Fare clic su **Get started** nell'angolo in alto a destra per accedere alla pagina di registrazione e completare la procedura di iscrizione.

.. image:: img/ultralytics_1_signup.png

**Creare un Dataset**

2. Dopo la registrazione, verrai portato alla homepage. Fare clic su **New Dataset** per creare un nuovo dataset.

.. image:: img/ultralytics_3_new_dataset.png

3. Apparirà una finestra. Qui puoi caricare le foto appena acquisite con il tuo Raspberry Pi e inserire un **Nome per il dataset**. Quindi fare clic su **Create & upload**.

.. image:: img/ultralytics_4_create_dataset.png

4. Ora entrerai nell'interfaccia del dataset, dove puoi vedere tutte le immagini caricate.

.. image:: img/ultralytics_5_dataset.png

**Annotare le Immagini**

5. Aprire ogni foto per annotarla. Usare il pulsante **+Add Class** a destra per aggiungere categorie. Aggiungere il nome della categoria appropriato in base all'oggetto che si desidera identificare (ad esempio: se ti stai addestrando a riconoscere una tazza, aggiungi "cup"; se ti stai addestrando a riconoscere un animale domestico, aggiungi "pet").

   **Suggerimenti per l'Annotazione**:
   - Usare il mouse per disegnare bounding box attorno agli oggetti, mantenendoli il più vicino possibile ai bordi degli oggetti
   - Assicurarsi che ogni oggetto sia annotato correttamente
   - Se un'immagine non contiene oggetti bersaglio, non è necessaria alcuna annotazione

.. image:: img/ultralytics_6_train2.png

6. Ripetere i passaggi precedenti fino a quando tutte le foto sono annotate. Controllare che le annotazioni su ogni immagine siano accurate.

.. image:: img/ultralytics_7_train3.png

**Creare un Modello di Addestramento**

7. Fare clic su **Models**, quindi su **New Model**.

.. image:: img/ultralytics_8_new_model.png

8. Nella finestra pop-up, selezionare **YOLOv8n** o **YOLO11n** come **Modello Base**. Queste sono versioni nano adatte per Raspberry Pi, offrendo dimensioni ridotte e alta velocità.

.. image:: img/ultralytics_9_new_model1.png

9. Configurare i parametri di addestramento:

   - **Image size**: Selezionare **320** (questa è la dimensione dell'immagine che il Raspberry Pi può elaborare efficientemente)
   - **Epochs**: Mantenere il valore predefinito (tipicamente 50-100 epoche)
   - **GPU Type**: Nessun requisito specifico, ma diversi tipi di GPU influenzano la velocità e il costo di addestramento

   **Nota**: I nuovi account Ultralytics ricevono $5 in crediti gratuiti; addestrare un modello piccolo costa tipicamente solo pochi centesimi, usa secondo necessità.

.. image:: img/ultralytics_9_new_model2.png

10. Fare clic su **Start Training**. Attendere un periodo (di solito 10-30 minuti, a seconda del volume di dati e della GPU), e il modello completerà l'addestramento.

    Durante l'addestramento, puoi vedere metriche in tempo reale:

    - **box_loss**: Perdita della bounding box; valori più piccoli sono migliori
    - **cls_loss**: Perdita di classificazione; valori più piccoli sono migliori
    - **mAP**: Precisione Media Media (Mean Average Precision); valori più alti sono migliori (intervallo 0-1)

**Scaricare e Distribuire**

11. Dopo il completamento dell'addestramento, fare clic su **Download PyTorch Model** per scaricare il modello addestrato (sarà un file .pt).

.. image:: img/ultralytics_10_download_model.png

12. Dopo il download, utilizzare FileZilla per trasferirlo sul tuo Raspberry Pi (si consiglia di posizionarlo nella directory ``~/ai-lab-kit/yolo/``).

**Eseguire il Modello Personalizzato**

Dopo aver posizionato il modello sul tuo Raspberry Pi, devi modificare il percorso del modello nel codice di esempio. Ecco un esempio di esecuzione completo

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   nano yolo_custom.py

sostituisci il nome del file del modello con il tuo file scaricato:

.. code-block:: python
   :emphasize-lines: 6

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("your_model.pt")  # Replace with your model filename

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

**Verificare i Risultati**

13. Eseguire il codice di esempio per osservare le prestazioni del modello YOLO sul tuo Raspberry Pi:

    .. code-block:: bash

       python3 yolo_custom.py

    Se tutto funziona correttamente, dovresti vedere il tuo oggetto bersaglio addestrato inquadrato da un bounding box nel flusso della fotocamera, con il nome della categoria e il punteggio di confidenza visualizzati.

.. image:: img/ultralytics_a2_yolo_find.png


Congratulazioni! Hai addestrato con successo il tuo modello YOLO personalizzato e lo hai distribuito sul Raspberry Pi.

----------------------------------------------------------

Suggerimenti e Raccomandazioni per l'Addestramento
--------------------------------------------------

**Migliorare le Prestazioni del Modello**

* **Aumentare il Volume di Dati**: Puntare ad almeno 50-100 immagini per categoria
* **Data Augmentation**: Variare proattivamente angolazioni, distanze e illuminazione durante l'acquisizione
* **Campioni Negativi**: Includere alcune immagini senza oggetti bersaglio per aiutare a ridurre i falsi positivi
* **Dataset Bilanciato**: Se si identificano più categorie, assicurarsi che ciascuna categoria abbia un numero simile di immagini



Domande Comuni
-------------------------


**D: Cosa fare se i risultati del rilevamento del modello sono insoddisfacenti?**

- Controllare la precisione delle annotazioni
- Aumentare il numero di immagini di addestramento
- Provare modelli più grandi (come YOLOv8s) o più epoche di addestramento
- Acquisire più immagini da scenari diversi

**D: Quanto tempo richiede l'addestramento?**

- Con circa 50 immagini e YOLOv8n, l'addestramento richiede tipicamente 10-20 minuti
- La piattaforma si regola automaticamente in base alla GPU selezionata

**D: Posso addestrare localmente?**

Sì, ma dovrai configurare l'ambiente Python e i driver GPU. Per i principianti, si consiglia la piattaforma Ultralytics per validare rapidamente le idee.


