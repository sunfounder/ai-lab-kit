.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. Hand-Gestenzählung
==============================================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

Im vorherigen Abschnitt haben wir die Echtzeit-Handerkennung
und die Visualisierung von Landmarks implementiert.

Dieser Abschnitt erweitert diese Funktionalität, indem
die Positionen der Finger-Landmarks verwendet werden,
um die Anzahl der erhobenen Finger (0–5) zu zählen.

Durch die Analyse der relativen Positionen der Fingerspitzen
und ihrer entsprechenden Gelenke lässt sich bestimmen,
ob ein Finger ausgestreckt ist.

.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Das Programm führt die folgenden Schritte aus:

1. Initialisierung des MediaPipe-Hands-Modells.
2. Erfassung von Videoframes mit der Raspberry-Pi-Kamera.
3. Echtzeit-Erkennung von 21 Hand-Landmarks.
4. Vergleich der Koordinaten der Fingerspitzen mit ihren proximalen Gelenken.
5. Bestimmung, ob jeder Finger ausgestreckt ist.
6. Zählen der erhobenen Finger.
7. Anzeige des Ergebnisses im Videobild.

Diese Methode ist:

- Leichtgewichtig und effizient
- Geeignet für den Raspberry Pi
- Eine Grundlage für Gestensteuerung und interaktive Systeme

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel "Show Video" und zeigt den Live-Kamerastream an.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Wenn eine Hand vor der Kamera erscheint:

   - MediaPipe erkennt die Hand in Echtzeit.
   - 21 Landmark-Punkte und Verbindungslinien werden auf der Hand gezeichnet.
   - Das Programm analysiert die Positionen der Fingerspitzen und Gelenke.
   - Die Anzahl der erhobenen Finger (0–5) wird berechnet.

   Die erkannte Fingeranzahl wird in der linken oberen Ecke
   des Bildschirms angezeigt als:

      Fingers: X

   Wenn Sie Ihre Finger strecken oder beugen, wird die Zahl
   sofort in Echtzeit aktualisiert.

   Wenn keine Hand erkannt wird, wird nur der normale Kamerastream
   ohne Fingerzählung angezeigt.

   Drücken Sie ``q``, um das Programm zu beenden.
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.



-----------------------------
4. Vollständiger Code
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2 
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections on the frame
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
               )


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

In jeder Schleifeniteration wird bestimmt, ob jeder der 5 Finger ausgestreckt ist, und die Anzahl der ausgestreckten Finger wird gezählt. Zum Beispiel:

- ✊ Alle Finger geschlossen → Anzahl 0
- ☝️ Zeigefinger ausgestreckt → Anzahl 1
- ✌️ Zeige- + Mittelfinger → Anzahl 2
- 🖐️ Alle fünf Finger geöffnet → Anzahl 5

--------------------------------------------------------------
5. Erkennungslogik und Erweiterungen
--------------------------------------------------------------

MediaPipe Hands gibt 21 Landmarks zurück.
Wir verwenden die Positionen der Fingerspitzen und Gelenke, um zu bestimmen,
ob jeder Finger ausgestreckt ist.

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → Indizes der Fingerspitzen  
  (Daumen=4, Zeigefinger=8, Mittelfinger=12, Ringfinger=16, kleiner Finger=20)

- ``finger_dips`` → Entsprechende proximale Gelenke  
  (Daumen=2, Zeigefinger=6, Mittelfinger=10, Ringfinger=14, kleiner Finger=18)

------------------------------------------------------------

Logik zur Fingerzählung:

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

Erklärung der Logik:

- **Daumen** → Vergleich von ``tip.x`` und ``dip.x`` (für die rechte Hand).
- **Andere Finger** → Vergleich von ``tip.y`` und ``dip.y``.
- Wenn sich die Fingerspitze oberhalb des Gelenks befindet
  (oder beim Daumen weiter nach außen),
  wird der Finger als ausgestreckt betrachtet.
- Jede erfüllte Bedingung erhöht den Zähler um ``+1``.

------------------------------------------------------------

Tipps zur Erweiterung:

- Um sowohl linke als auch rechte Hände zu unterstützen,
  verwenden Sie ``hands_detected.multi_handedness``, um den Handtyp zu bestimmen,
  und kehren Sie den Vergleich der x-Achse für den Daumen entsprechend um.

- Diese Logik kann erweitert werden, um Folgendes zu implementieren:

  - Erkennung der OK-Geste
  - Erkennung von Daumen hoch
  - Stein-Schere-Papier-Interaktion
  - Benutzerdefinierte gestenbasierte Steuerungen

------------------------------------------------------------
6. Fehlerbehebung
------------------------------------------------------------

- Daumenerkennung ungenau

  Die Daumenerkennung kann ungenau sein, weil sich die Logik für linke und rechte Hände unterscheidet. Der horizontale Vergleich für den Daumen hängt von der Handausrichtung ab.

  Verwenden Sie ``multi_handedness``, um festzustellen, ob die erkannte Hand links oder rechts ist, und passen Sie die Logik zur Daumenerkennung entsprechend an.

- Instabile Erkennung

  Wenn die Fingerzählung instabil erscheint, kann dies an unzureichender Beleuchtung oder einem unruhigen Hintergrund liegen.

  Verbessern Sie die Lichtverhältnisse und verwenden Sie einen einfachen Hintergrund, um die Erkennungsstabilität zu erhöhen.

- Hohe Latenz

  Wenn die Reaktion langsam wirkt, ist möglicherweise die Auflösung zu hoch oder die CPU überlastet.

  Reduzieren Sie die Auflösung (z. B. 320×240) und schließen Sie unnötige Hintergrundprozesse. Bei Bedarf können Sie auch die Logik zur Fingerzählung vereinfachen.


-----------------------------
7. Zusammenfassung
-----------------------------

- Mit MediaPipe Hands lässt sich **Echtzeit-Gestenerkennung** schnell umsetzen.
- In diesem Abschnitt wurde **die Zählung von Zahlengesten** auf Basis der Fingerspitzenpositionen implementiert und damit die Grundlage für benutzerdefinierte Gestenerkennung geschaffen.
- Durch die Anpassung an linke und rechte Hände sowie die Erweiterung der Erkennungsregeln lassen sich komplexere interaktive Szenarien realisieren.