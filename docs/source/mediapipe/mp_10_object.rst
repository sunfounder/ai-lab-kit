.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_object:


10. Rilevamento Oggetti
=================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

Oltre ai modelli specializzati per viso, mani e posa,
MediaPipe fornisce anche un **Object Detector** generico
basato su TensorFlow Lite.

Questo capitolo dimostra come utilizzare il modello
``efficientdet_lite0.tflite`` su Raspberry Pi
per eseguire il rilevamento oggetti in tempo reale e visualizzare i risultati
sul flusso video della fotocamera.

.. image:: img/mp_object.png
   :width: 500
   :align: center

This module can be used for:

- Demo di riconoscimento oggetti in tempo reale
- Percezione per casa intelligente/robotica
- Monitoraggio di sicurezza semplice
- Progetti di visione embedded


------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

Il programma esegue i seguenti passaggi:

1. Inizializza l'**ObjectDetector** di MediaPipe Tasks
   e carica il modello ``efficientdet_lite0.tflite``.
2. Acquisisce i fotogrammi dal flusso video di Picamera2.
3. Converte ogni fotogramma in un oggetto MediaPipe ``mp.Image``.
4. Chiama ``detect_for_video`` per eseguire il rilevamento oggetti in tempo reale.
5. Disegna riquadri e etichette usando OpenCV.
6. Limita il numero di rilevamenti visualizzati per mantenere l'output chiaro
   e mantenere prestazioni stabili su Raspberry Pi.

-----------------------------
3. Preparazione del Modello
-----------------------------

Questo esempio utilizza il modello **EfficientDet Lite0**
in formato TensorFlow Lite (TFLite).

EfficientDet Lite0 e leggero e ottimizzato per
dispositivi embedded come Raspberry Pi.
Fornisce un buon equilibrio tra velocita e precisione.

Il file ``efficientdet_lite0.tflite`` e incluso nella directory del progetto
e puo essere utilizzato direttamente.

* `Pagina di download ufficiale del modello <https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector#efficientdet-lite0_model_recommended>`_

Se e richiesta una precisione maggiore e le prestazioni hardware lo consentono,
puoi passare a:

- EfficientDet Lite1
- EfficientDet Lite2

Puoi anche sostituire il modello con un tuo modello di rilevamento oggetti
TFLite auto-addestrato, purche segua
i requisiti di formato di MediaPipe Tasks Object Detector.


------------------------
4. Eseguire il Codice
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_object.py


#. Dopo aver eseguito il programma, si apre una finestra intitolata "Show Video" che mostra il flusso video in diretta.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_10.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Per ogni fotogramma video, il modello Object Detector (``efficientdet_lite0.tflite``) viene eseguito in tempo reale e cerca oggetti riconoscibili nella scena.

   Quando vengono rilevati oggetti:

   - Un riquadro di delimitazione rettangolare viene disegnato intorno a ogni oggetto.
   - Un'etichetta e un punteggio di confidenza vengono mostrati sopra il riquadro nel formato ``nome: punteggio`` (per esempio, ``person: 0.87``).
   - Vengono visualizzati solo i rilevamenti sopra ``SCORE_THRESHOLD`` (default 0.5).
   - Per mantenere lo schermo pulito e le prestazioni, il programma disegna fino a ``MAX_DRAW`` rilevamenti (default 20) per fotogramma.

   Mentre la visuale della fotocamera cambia, i riquadri e le etichette si aggiornano continuamente in tempo reale.

   Premi ``q`` per uscire dal programma.
   La fotocamera si ferma e la finestra OpenCV si chiude automaticamente.

-----------------------------
5. Codice Completo
-----------------------------

.. code-block:: python

   # STEP 1: Import the necessary modules.
   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import time
   from pathlib import Path

   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Paths & basic settings --------------------
   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")  # Model path
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20  # Limit the number of drawn detections

   # -------------------- Helper: visualization --------------------
   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       img = bgr_image.copy()
       h, w = img.shape[:2]
       drawn = 0

       for det in detection_result.detections:
           bbox = det.bounding_box
           x1 = max(0, min(int(bbox.origin_x), w - 1))
           y1 = max(0, min(int(bbox.origin_y), h - 1))
           x2 = max(0, min(int(bbox.origin_x + bbox.width), w - 1))
           y2 = max(0, min(int(bbox.origin_y + bbox.height), h - 1))

           # top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw bounding box
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break
       return img

   # STEP 2: Initialize the detector
   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,
   )
   detector = vision.ObjectDetector.create_from_options(options)

   # STEP 3: Camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()
   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert to RGB and wrap as mp.Image
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

       # STEP 4: Detect
       ts_ms = int(time.time() * 1000)
       detection_result = detector.detect_for_video(mp_image, ts_ms)

       # STEP 5: Visualize
       annotated = visualize(frame_bgr, detection_result)

       cv2.imshow("Show Video", annotated)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Dopo aver eseguito lo script, il flusso video mostrera:

- Riquadri di delimitazione intorno agli oggetti rilevati
- Etichette di classificazione e punteggi di confidenza
- Rilevamento in tempo reale (puo raggiungere circa 10~20 FPS su Raspberry Pi)

-----------------------------
6. Spiegazione del Codice
-----------------------------

**Configurazione**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20

- ``SCORE_THRESHOLD`` controlla la confidenza minima per visualizzare i rilevamenti (applicato all'interno del runtime Tasks).
- ``MAX_DRAW`` e una comodita dell'interfaccia per limitare quanti riquadri vengono renderizzati per fotogramma.

**Importazioni**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2, numpy as np, time
   from pathlib import Path
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

- ``mediapipe.tasks.python.vision`` ospita l'API Tasks **ObjectDetector**.
- Usiamo ancora la classica OpenCV per finestre e disegno.

**Helper di Visualizzazione**

.. code-block:: python

   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       """
       Draw bounding boxes and category labels on a BGR image.
       Compatible with MediaPipe Tasks ObjectDetector's detection_result.
       """
       img = bgr_image.copy()
       h, w = img.shape[:2]

       drawn = 0
       for det in detection_result.detections:
           bbox = det.bounding_box  # (origin_x, origin_y, width, height) in pixels
           x1 = int(bbox.origin_x); y1 = int(bbox.origin_y)
           x2 = int(bbox.origin_x + bbox.width); y2 = int(bbox.origin_y + bbox.height)

           # Clamp to frame bounds (defensive)
           x1 = max(0, min(x1, w - 1)); y1 = max(0, min(y1, h - 1))
           x2 = max(0, min(x2, w - 1)); y2 = max(0, min(y2, h - 1))

           # Top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw rectangle and caption
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break

       return img

- Mantiene il ciclo principale pulito.
- Evita di fare affidamento su utility "visualize" inesistenti; funziona direttamente con gli output di Tasks.

**Creare l'ObjectDetector**

.. code-block:: python

   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,  # VIDEO mode for streaming input
   )
   detector = vision.ObjectDetector.create_from_options(options)

- ``RunningMode.VIDEO`` e ottimizzato per flussi e **richiede timestamp**.
- Il runtime Tasks gestisce internamente il ridimensionamento/normalizzazione dell'immagine per te.

**Configurazione della Fotocamera (Sorgente in Streaming)**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

- 640×480 e un buon compromesso tra FPS e precisione su Raspberry Pi.
- Picamera2 restituisce BGRA (``XRGB8888``); convertiamo in BGR/RGB.

**Rilevamento per Fotogramma**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr,  cv2.COLOR_BGR2RGB)

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

   ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp
   detection_result = detector.detect_for_video(mp_image, ts_ms)

- MediaPipe si aspetta buffer **RGB**.
- Il timestamp deve **aumentare ogni fotogramma**; usare ``time.time()*1000`` e sufficiente per questa demo.

**Renderizzazione e Visualizzazione**

.. code-block:: python

   annotated = visualize(frame_bgr, detection_result)
   cv2.imshow("Show Video", annotated)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

- L'helper restituisce un'immagine BGR pronta per la visualizzazione con OpenCV.
- Premi ``q`` per uscire dal ciclo.

**Pulizia**

.. code-block:: python

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Rilascia sempre la fotocamera e distruggi le finestre per evitare di bloccare il dispositivo.

------------------------------------------------------
7. Prestazioni e Applicazioni
------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Direzione di Ottimizzazione
     - Effetto
     - Suggerimento
   * - Risoluzione
     - Risoluzione piu alta da immagine piu chiara ma velocita ridotta
     - 640x480 e sufficiente
   * - Selezione del Modello
     - Lite0 ~ Lite2
     - Lite0 e piu veloce, Lite2 e piu preciso
   * - Disegno Multi-oggetto
     - Troppi oggetti causano latenza
     - Usa ``MAX_DRAW`` per limitare

------------------------------------------------------
8. Risoluzione dei Problemi
------------------------------------------------------

- Nessun risultato di rilevamento

  Se non viene rilevato nulla, la soglia di confidenza potrebbe essere troppo alta.

  Prova ad abbassare ``SCORE_THRESHOLD`` (per esempio, da 0.5 a 0.3) e testa di nuovo.

- Basso frame rate

  Se il video e lento, il modello o la risoluzione potrebbero essere troppo pesanti per il Raspberry Pi.

  Usa un modello piu leggero (``efficientdet_lite0.tflite``) e riduci la risoluzione (per esempio, 640×480 o 320×240). Chiudere altri processi in background puo anche migliorare le prestazioni.

- Offset del riquadro di rilevamento

  Se i riquadri appaiono spostati o escono dal fotogramma, di solito e causato da problemi di conversione delle coordinate.

  Assicurati che le coordinate del riquadro siano limitate ai bordi dell'immagine. Questo esempio gia limita ``x1, y1, x2, y2`` per prevenire disegni fuori range.

- Rilevamento caotico

  Se vengono rilevati troppi oggetti e lo schermo diventa affollato, potrebbe essere difficile leggere i risultati.

  Limita il numero di rilevamenti disegnati usando ``MAX_DRAW`` (per esempio, 10–20) per mantenere la visualizzazione chiara e stabile.

-----------------------------
9. Riepilogo
-----------------------------

- Questo capitolo ha implementato il rilevamento oggetti generico basato su MediaPipe Tasks;
- Ha utilizzato il modello EfficientDet Lite0, bilanciando precisione e prestazioni;
- Ha approfondito il metodo per visualizzare i risultati del rilevamento;
- Puo essere esteso a modelli personalizzati (es., scenari di rilevamento di frutta, veicoli, oggetti pericolosi).