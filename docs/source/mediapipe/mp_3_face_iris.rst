.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. Contorni Facciali e Rilevamento dell'Iride
=================================================================

------------------------------------------------------------
1. Panoramica
------------------------------------------------------------

Nelle sezioni precedenti, abbiamo implementato il rilevamento di base della mesh facciale
e il semplice riconoscimento delle emozioni.

Questa sezione si concentra sui metodi di connessione delle caratteristiche dettagliate
forniti da MediaPipe FaceMesh:

- ``FACEMESH_CONTOURS`` — Disegna le linee del contorno facciale
  (bordi del viso e confini esterni delle caratteristiche)

- ``FACEMESH_IRISES`` — Disegna le regioni dell'iride di entrambi gli occhi

Disegnando solo contorni e regioni dell'iride, la visualizzazione diventa
piu pulita e leggera. Questo e utile per:

- Estrazione di caratteristiche facciali
- Eye tracking
- Tracciamento della pupilla
- Interazione tramite sguardo

.. image:: img/mp_face_iris.png
   :align: center

------------------------------------------------------------
2. Come Funziona
------------------------------------------------------------

Il programma esegue i seguenti passaggi:

1. Inizializza il modello MediaPipe FaceMesh.
2. Acquisisce i fotogrammi video dalla fotocamera del Raspberry Pi.
3. Converte l'immagine in formato RGB (richiesto da MediaPipe).
4. Disegna le linee del contorno facciale usando ``FACEMESH_CONTOURS``.
5. Disegna i landmark dell'iride usando ``FACEMESH_IRISES``.
6. Visualizza solo le aree chiave per una visualizzazione piu chiara.

------------------------
3. Eseguire il Codice
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

#. Dopo aver eseguito il programma, si apre una finestra video intitolata "Show Video" che mostra il flusso video in diretta.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_3.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
         
   Quando un volto appare davanti alla fotocamera:

   - MediaPipe rileva i landmark facciali in tempo reale.
   - Vengono disegnate solo le linee del contorno facciale (profilo del viso, sopracciglia, labbra, ecc.).
   - Le regioni dell'iride di entrambi gli occhi sono evidenziate con connessioni circolari dei landmark.

   A differenza della mesh facciale completa, lo schermo mostra solo i contorni chiave e le caratteristiche dell'iride, rendendo la visualizzazione piu pulita e meno affollata.

   Mentre l'utente muove la testa o gli occhi:

   - Le linee del contorno seguono il volto in modo fluido.
   - I landmark dell'iride tracciano il movimento degli occhi in tempo reale.

   Se non viene rilevato alcun volto, la finestra continua a mostrare il normale flusso video senza annotazioni.

   Premi ``q`` per uscire dal programma.
   La fotocamera si ferma e la finestra OpenCV si chiude automaticamente.

-----------------------------
4. Codice Completo
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize FaceMesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Enable if hardware preview is needed
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      if results.multi_face_landmarks:
         for face_landmarks in results.multi_face_landmarks:
            # Draw facial contours
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_CONTOURS,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            # Draw iris features
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Dopo aver eseguito il programma, sullo schermo verranno visualizzati solo i contorni facciali e le regioni dell'iride di entrambi gli occhi.

-----------------------------
5. Spiegazione dei Passaggi Chiave
-----------------------------

Il codice in questa sezione e quasi lo stesso di
:ref:`mp_face`.

La differenza principale e il metodo di disegno utilizzato
all'interno del ciclo principale. La funzione ``draw_landmarks()``
viene chiamata due volte:

- Una volta con ``FACEMESH_CONTOURS``
- Una volta con ``FACEMESH_IRISES``

Puoi commentare uno dei due blocchi di disegno
per osservare la differenza nell'effetto visivo.

------------------------------------------------------------

``FACEMESH_CONTOURS``

- Un insieme di connessioni fornito da MediaPipe.
- Disegna principalmente:

  - Contorno facciale esterno
  - Bordi degli occhi
  - Profilo del naso
  - Contorni delle labbra

Questo metodo produce una visualizzazione semplificata,
rendendo piu facile osservare i cambiamenti del contorno facciale.

------------------------------------------------------------

``FACEMESH_IRISES``

- Disegna le regioni dell'iride di entrambi gli occhi.
- Include i punti chiave dell'iride e le linee di connessione circolari.
- Utile per:

  - Eye tracking
  - Tracciamento della pupilla
  - Rilevamento dello sguardo

------------------------------------------------------------

``landmark_drawing_spec=None``

- Disabilita il disegno dei singoli punti landmark.
- Vengono visualizzate solo le linee di connessione,
  ottenendo un effetto visivo piu pulito.

Se desideri visualizzare sia punti che linee,
definisci un ``DrawingSpec`` personalizzato.

------------------------------------------------------------

``drawing_styles.get_default_face_mesh_contours_style()``

- Restituisce lo stile di disegno predefinito per i contorni.

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- Restituisce lo stile predefinito per le linee di connessione dell'iride.


------------------------------------------------------------
6. Risoluzione dei Problemi
------------------------------------------------------------

- Iride non rilevata

  Se l'iride non viene rilevata, l'illuminazione potrebbe essere insufficiente,
  il volto potrebbe essere troppo lontano dalla fotocamera,
  o ``refine_landmarks`` potrebbe non essere abilitato.

  Migliora l'illuminazione, avvicinati alla fotocamera,
  e assicurati che ``refine_landmarks=True`` sia impostato
  durante l'inizializzazione di FaceMesh.

- Linee di contorno instabili

  Se le linee del contorno appaiono instabili,
  la confidenza di rilevamento potrebbe essere troppo bassa,
  o l'illuminazione e il movimento della testa potrebbero influenzare il tracciamento.

  Prova ad aumentare ``min_detection_confidence``,
  migliorare l'illuminazione e mantenere i movimenti della testa piu lenti e fluidi.

- Latenza elevata

  Se la risposta video e lenta,
  la risoluzione potrebbe essere troppo alta
  o ``refine_landmarks`` potrebbe consumare risorse aggiuntive.

  Riduci la risoluzione (per esempio, 320×240),
  o disabilita ``refine_landmarks`` se il rilevamento dell'iride non e necessario.
  
-----------------------------
7. Riepilogo
-----------------------------

- ``FACEMESH_CONTOURS`` e ``FACEMESH_IRISES`` sono due importanti metodi di connessione forniti da MediaPipe.
- Rispetto al disegno della mesh completa, sono piu leggeri e intuitivi, adatti per scenari di interazione pratica.
- Il prossimo capitolo introdurra come utilizzare queste funzionalita per il tracciamento dello sguardo e il rilevamento dei battiti di ciglia.