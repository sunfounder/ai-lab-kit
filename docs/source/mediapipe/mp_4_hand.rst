.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. Handerkennung
===============================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

Im vorherigen Abschnitt haben wir mit MediaPipe
Gesichtserkennung und Landmark-Tracking implementiert.

Dieser Abschnitt stellt **MediaPipe Hands** vor —
ein leichtgewichtiges und stabiles Modul zur Echtzeit-Erkennung
von Hand-Landmarks.

Mit diesem Modul können wir:

- Bis zu zwei Hände gleichzeitig erkennen
- 21 Landmark-Punkte pro Hand identifizieren
- Hand-Skelettverbindungen in Echtzeit visualisieren

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Das Programm führt die folgenden Schritte aus:

1. Initialisierung des MediaPipe-Hands-Modells.
2. Erfassung von Frames mit der Raspberry-Pi-Kamera.
3. Konvertierung des Bildes in das RGB-Format (erforderlich für MediaPipe).
4. Erkennung von Hand-Landmarks mit dem Hands-Modul.
5. Zeichnen der 21 Landmark-Punkte und ihrer Verbindungslinien.
6. Anzeige des annotierten Videostreams in Echtzeit.

Dieses Modul bildet die Grundlage für:

- Gestenerkennung
- Fingerzählen
- Interaktive Steuerungssysteme
- Berührungslose Mensch–Computer-Interaktion

------------------------
3. Code ausführen
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel „Show Video“ und zeigt den Live-Kamerastream an.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
   
   Wenn eine oder zwei Hände vor der Kamera erscheinen:
   
   - MediaPipe erkennt jede Hand in Echtzeit.
   - Auf jeder Hand werden 21 Landmark-Punkte identifiziert.
   - Die Landmark-Punkte werden durch Linien verbunden und bilden ein Hand-Skelett.
   
   Wenn zwei Hände sichtbar sind, werden beide Hände gleichzeitig
   verfolgt und annotiert.
   
   Wenn der Benutzer seine Hände oder Finger bewegt:
   
   - folgen die Landmark-Punkte der Bewegung flüssig.
   - aktualisiert sich das Hand-Skelett in Echtzeit.
   
   Wenn keine Hand erkannt wird, zeigt das Programm lediglich
   den normalen Kamerastream ohne Markierungen an.
   
   Drücken Sie ``q``, um das Programm zu beenden.
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.

-----------------------------
4. Vollständiger Code
-----------------------------

Der vollständige Beispielcode lautet wie folgt:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Nach dem Ausführen des Codes sehen Sie im Kamerastream:

- Wenn eine oder zwei Hände erkannt werden, werden angezeigt:

  - 21 Hand-Landmarks
  - Ein blaues Verbindungsskelett
- Wenn sich die Hand bewegt, verfolgt die Erkennung die Bewegung in Echtzeit.

--------------------------------------------------------
5. Beschreibung der MediaPipe-Hands-Landmarks
--------------------------------------------------------

MediaPipe Hands liefert **21 Landmarks** für jede Hand, darunter Positionen wie Handgelenk, Handfläche und Fingerspitzen.

Häufig verwendete Landmarks sind:

.. list-table::
   :header-rows: 1

   * - Index
     - Name
     - Position
   * - 0
     - WRIST
     - Handgelenk
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - Spitzen der jeweiligen Finger
   * - 5~17
     - Joints
     - Mittlere Gelenke der jeweiligen Finger
   * - 9
     - PALM_CENTER (ungefähr)
     - Bereich der Handfläche

.. image:: img/mp_hand_point.png
  :width: 400
  :alt: MediaPipe Hands Landmarks Illustration
  :align: center

.. note::
   Diese Koordinaten sind **normalisierte Koordinaten** und können anhand der Bildauflösung in tatsächliche Pixelpositionen umgerechnet werden.
   Sie können zur Berechnung von Winkeln und Abständen verwendet werden und ermöglichen dadurch Gestenerkennung.

------------------------------------------------------------
6. Fehlerbehebung
------------------------------------------------------------

- Instabile Handerkennung

  Die Handerkennung kann instabil werden, wenn die Beleuchtung zu schwach ist, der Hintergrund unruhig ist oder sich die Hand zu schnell bewegt.
  
  Versuchen Sie, die Beleuchtung zu verbessern, einen einfachen Hintergrund zu verwenden und Ihre Hände langsamer und gleichmäßiger zu bewegen.

- Keine Hand erkannt

  Wenn keine Hand erkannt wird, ist möglicherweise der Kamerawinkel ungeeignet, die Hand befindet sich zu weit von der Kamera entfernt oder die Auflösung ist zu niedrig.
  
  Passen Sie die Kameraposition an, bewegen Sie sich näher zur Kamera und stellen Sie sicher, dass die Auflösung mindestens 640×480 beträgt.

- Hohe Latenz

  Wenn die Videoreaktion langsam wirkt, könnte der Raspberry Pi stark ausgelastet sein oder die Auflösung zu hoch eingestellt sein.
  
  Reduzieren Sie die Auflösung (z. B. 320×240) und schließen Sie unnötige Hintergrundprozesse.


-----------------------------
7.  Zusammenfassung
-----------------------------

- MediaPipe Hands ermöglicht eine stabile **Echtzeit-Handerkennung** auf dem Raspberry Pi.
- Stellt 21 Landmarks pro Hand bereit, geeignet für:

  - Gestenerkennung
  - Virtuelle Steuerung
  - Interaktive UI-Steuerung
  
- Anschließend werden wir **benutzerdefinierte Gestenerkennung** auf Basis dieser Landmarks implementieren.