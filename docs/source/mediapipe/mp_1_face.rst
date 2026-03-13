.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. Gesichtserkennung
===========================

In diesem Abschnitt wird gezeigt, wie das **MediaPipe Face Mesh**-Modul auf einem **Raspberry Pi** für die Echtzeit-Gesichtserkennung und das Zeichnen eines Gesichts-Landmark-Meshes verwendet wird.

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe ist ein plattformübergreifendes Framework für Machine-Learning-Pipelines, das von Google entwickelt wurde und die Echtzeitverarbeitung von Video-Streams und Bildern unterstützt. Das Face-Mesh-Modul ist ein von MediaPipe bereitgestelltes Modell für Echtzeit-Gesichtserkennung und Landmark-Tracking und kann zur Entwicklung verschiedener Anwendungen für Gesichtserkennung und Interaktion verwendet werden.

Im Vergleich zur Haar-Erkennung von OpenCV verwendet MediaPipe ein Deep-Learning-Modell zur Erkennung und bietet:

- Höhere Genauigkeit
- Bessere Robustheit gegenüber unterschiedlichen Lichtverhältnissen und Blickwinkeln
- Unterstützung für Gesichts-Landmark-Tracking (468 Punkte)
- Nahtlose Integration mit OpenCV, wodurch die Erkennungsergebnisse direkt auf dem Videostream dargestellt werden können.

------------------------
1. Code ausführen
------------------------

.. important::


   Stellen Sie vor dem Start sicher, dass:

   * das Pan-Tilt-Modul montiert ist
   * Sie Zugriff auf den Raspberry Pi Desktop haben
   * das Codepaket installiert ist
   * das Fusion HAT+ installiert und konfiguriert ist
   * OpenCV installiert ist

   Detaillierte Anweisungen finden Sie unter :ref:`opencv_install`.

#. Öffnen Sie das Terminal und geben Sie den folgenden Befehl ein:

   .. code-block:: bash
   
      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. Nach dem Start des Skripts öffnet OpenCV ein Fenster mit dem Titel „Show Video“ und zeigt den Live-Videostream der Raspberry-Pi-Kamera an.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   * Wenn ein Gesicht vor der Kamera erscheint, erkennt das Programm es und zeichnet in Echtzeit ein detailliertes Gesichts-Landmark-Mesh auf das Gesicht. Das Mesh verfolgt Gesichtsbewegungen flüssig, während sich die Person bewegt, blinzelt oder ihre Mimik verändert.
   * Wenn kein Gesicht erkannt wird, zeigt das Fenster weiterhin den normalen Kamerastream ohne Landmarken an.
   
   Der Videostream läuft kontinuierlich weiter, bis der Benutzer das Programm beendet.
   Zum Beenden drücken Sie die Taste **q** auf der Tastatur.
   Die Kamera wird gestoppt und alle OpenCV-Ressourcen werden automatisch freigegeben.

------------------------
2. Codebeispiel
------------------------

Der vollständige Code ist unten dargestellt:

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

Nach dem Ausführen des Programms sehen Sie den Live-Kamerastream, und sobald ein Gesicht erkannt wird, wird automatisch ein Gesichts-Mesh darüber gelegt.

-----------------------------

3. Erklärung der wichtigsten Schritte
-----------------------------------------------

#. Bibliotheken importieren

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   Diese Bibliotheken werden verwendet, um:

   - die Raspberry-Pi-Kamera zu steuern
   - Bilder zu verarbeiten und anzuzeigen
   - Gesichts-Landmarks zu erkennen

#. FaceMesh initialisieren

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   Dadurch wird das Gesichtserkennungsmodell erstellt.
   Es verfolgt kontinuierlich ein Gesicht im Videomodus.

#. Kamera starten

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   Die Kamera beginnt mit dem Streaming bei einer Auflösung von 640×480.

#. Frames in einer Schleife erfassen

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   In jeder Schleifeniteration wird ein Frame aufgenommen und für OpenCV in das passende Format konvertiert.

#. Gesichts-Landmarks erkennen

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   Das Frame wird in das RGB-Format konvertiert.
   MediaPipe analysiert anschließend das Bild und erkennt die Gesichts-Landmarks.

#. Gesichts-Mesh zeichnen

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   Wenn ein Gesicht erkannt wird, wird ein Mesh darüber gezeichnet.

#. Ergebnis anzeigen und Programm beenden

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   Drücken Sie ``q``, um das Programm zu beenden.
   Die Kamera wird anschließend automatisch geschlossen.

---------------------------------------------
4. Häufige Probleme und Fehlerbehebung
---------------------------------------------

* Kamera kann nicht geöffnet werden

  * Stellen Sie sicher, dass das CSI-Kamerakabel korrekt angeschlossen ist
  * Aktivieren Sie die Kameraschnittstelle:

    ``sudo raspi-config`` → Interface Options → Camera

  * Starten Sie den Raspberry Pi nach der Aktivierung neu

* Programm startet langsam

  Beim ersten Start wird das MediaPipe-Modell geladen, was einige Sekunden dauern kann.
  Das ist normal. Nachfolgende Starts erfolgen schneller.

* Instabile Erkennung / Verzögerungen

  * Reduzieren Sie die Kameraauflösung (z. B. 320×240)
  * Deaktivieren Sie ``refine_landmarks``, um die CPU-Auslastung zu reduzieren
  * Schließen Sie andere laufende Programme

* Kein Modul namens ``mediapipe``

  Installieren Sie MediaPipe:

  .. code-block:: bash

     pip install mediapipe

  Stellen Sie sicher, dass Sie ein 64-Bit-Raspberry-Pi-OS verwenden.

-----------------------------
5. Zusammenfassung
-----------------------------

- MediaPipe FaceMesh verwendet ein Deep-Learning-Modell, um hochpräzise Gesichtserkennung auf dem Raspberry Pi zu ermöglichen
- Lässt sich sehr eng mit OpenCV integrieren
- Geeignet für Szenarien wie Gesichtsausdruckserkennung, Avatar-Tracking und AR-Anwendungen
- Robuster und einfacher erweiterbar als traditionelle Haar-Feature-Methoden

Im nächsten Abschnitt wird weiter erläutert, **wie Face-Mesh-Landmarks** für einfache Gesichtsmerkmalanalysen und interaktive Anwendungen genutzt werden können.