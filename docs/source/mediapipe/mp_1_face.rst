.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. Rilevamento Facciale
===========================

Questa sezione introduce come utilizzare il modulo **MediaPipe Face Mesh** su un **Raspberry Pi** per il rilevamento facciale in tempo reale e il disegno della mesh dei landmark facciali.

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe e un framework di pipeline di machine learning cross-platform sviluppato da Google, che supporta l'elaborazione in tempo reale di flussi video e immagini. Il modulo Face Mesh e un modello fornito da MediaPipe per il rilevamento facciale in tempo reale e il tracciamento dei landmark, che puo essere utilizzato per creare varie applicazioni di riconoscimento facciale e interazione.

Rispetto al rilevamento Haar di OpenCV, MediaPipe utilizza un modello di deep learning per il rilevamento, offrendo:

-  Maggiore precisione
-  Migliore robustezza all'illuminazione e agli angoli
-  Supporto per il tracciamento dei landmark facciali (468 punti)
-  Integrazione perfetta con OpenCV, consentendo di disegnare direttamente i risultati del rilevamento sui flussi video.

------------------------
1. Eseguire il Codice
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
   
      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. Dopo aver eseguito lo script, OpenCV apre una finestra intitolata “Show Video” e mostra il flusso video in diretta catturato dalla fotocamera del Raspberry Pi.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   * Se un volto appare davanti alla fotocamera, il programma lo rileva e disegna una mesh dettagliata dei landmark facciali in tempo reale. The mesh tracks facial movements smoothly as the person moves, blinks, or changes expressions.
   * Se non viene rilevato alcun volto, la finestra continua a mostrare il normale flusso video senza landmark.
   
   Il flusso video continua a essere eseguito fino a quando l'utente non esce dal programma.
   Per uscire dal programma, premi q sulla tastiera.
   La fotocamera si fermera e tutte le risorse di OpenCV verranno rilasciate automaticamente.

------------------------
2. Codice di Esempio
------------------------

Il codice completo e mostrato di seguito:

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the mp_face_mesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,          # Set to False for video streams
       max_num_faces=1,                  # Maximum number of faces to detect
       refine_landmarks=True,           # Whether to refine landmarks
       min_detection_confidence=0.5     # Detection confidence threshold
   )

   # Open Raspberry Pi camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 → BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert BGR to RGB (MediaPipe requires RGB)
       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # Face detection and landmark tracking
       results = face.process(frame)

       # Convert RGB back to BGR (for OpenCV display)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       # Draw detected facial landmarks
       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Dopo aver eseguito il programma, vedrai il flusso video in diretta e una mesh facciale verra automaticamente disegnata quando viene rilevato un volto.

-----------------------------
3. Spiegazione dei Passaggi Chiave
-----------------------------

#. Importare le librerie

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   Queste librerie vengono utilizzate per:

   - Controllare la fotocamera del Raspberry Pi
   - Elaborare e visualizzare le immagini
   - Rilevare i landmark facciali

#. Inizializzare FaceMesh

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   Questo crea il modello di rilevamento facciale.
   Tiene traccia di un volto in modo continuo in modalita video.

#. Avviare la fotocamera

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   La fotocamera inizia lo streaming alla risoluzione 640×480.

#. Acquisire i fotogrammi in un ciclo

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Ogni ciclo acquisisce un fotogramma e converte il formato per OpenCV.

#. Rilevare i landmark facciali

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   Il fotogramma viene convertito in RGB.
   MediaPipe analizza l'immagine e rileva i landmark facciali.

#. Disegnare la mesh facciale

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   Se viene rilevato un volto, viene disegnata una mesh su di esso.

#. Visualizzare il risultato e uscire

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   Premi ``q`` per fermare il programma.
   La fotocamera si chiudera automaticamente.

---------------------------------------------
4. Problemi Comuni e Risoluzione dei Problemi
---------------------------------------------

* La fotocamera non si apre

  * Assicurati che il cavo della fotocamera CSI sia inserito correttamente
  * Abilita l'interfaccia della fotocamera:

    ``sudo raspi-config`` → Interface Options → Camera

  * Riavvia il Raspberry Pi dopo l'abilitazione

* Il programma si avvia lentamente

  La prima esecuzione carica il modello MediaPipe, il che potrebbe richiedere alcuni secondi.
  Questo e normale. Le esecuzioni successive saranno piu veloci.

* Rilevamento instabile / Ritardo

  * Riduci la risoluzione della fotocamera (es. 320×240)
  * Disabilita ``refine_landmarks`` per ridurre l'uso della CPU
  * Chiudi altri programmi in esecuzione

* Nessun modulo ``mediapipe``

  Installa MediaPipe:

  .. code-block:: bash

     pip install mediapipe

  Assicurati di utilizzare un sistema Raspberry Pi OS a 64 bit.

-----------------------------
5. Riepilogo
-----------------------------

- MediaPipe FaceMesh utilizza un modello di deep learning per ottenere un rilevamento facciale di alta precisione su Raspberry Pi
- Si integra molto strettamente con OpenCV
- Adatto a scenari come il riconoscimento delle espressioni, il tracciamento degli avatar, le applicazioni AR
- Piu robusto e facile da estendere rispetto alle tradizionali feature Haar

La prossima sezione introdurra ulteriormente **come utilizzare i landmark di Face Mesh** per l'analisi semplice delle caratteristiche facciali e l'interazione.