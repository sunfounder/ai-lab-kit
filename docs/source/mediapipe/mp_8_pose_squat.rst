.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. Kniebeugen-Zähler
==========================================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

Im vorherigen Kapitel haben wir die grundlegende menschliche Posenschätzung implementiert.
Dieses Kapitel baut darauf auf und zeigt die Umsetzung eines einfachen
**Kniebeugen-Zählers** mit MediaPipe Pose.

Dies ist ein praxisnahes Beispiel für die Kombination aus:

- Pose-Erkennung
- Bewegungserkennung
- Echtzeit-Zählung

Es kann in intelligenten Fitnesssystemen,
Heimtrainings-Assistenten oder Anwendungen zur Bewegungsanalyse eingesetzt werden.

.. image:: img/mp_pose_s2.png
   :alt: Squat Count Example
   :align: center


------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Der Kniebeugen-Zähler wird mit der folgenden Logik implementiert:

1. MediaPipe Pose wird verwendet, um 33 Körper-Schlüsselpunkte zu erkennen.
2. Wichtige Gelenke werden ausgewählt (Schulter, Hüfte, Knöchel).
3. Die normalisierten y-Koordinaten werden verwendet, um die Hüfthöhe abzuschätzen.
4. Obere und untere Schwellenwerte werden definiert (z. B. 0.55 und 0.45).
5. Eine einfache Zustandsmaschine erkennt den Übergang:
   „stehen → Kniebeuge → stehen“.
6. Der Zähler wird erhöht, wenn ein vollständiger Kniebeugen-Zyklus abgeschlossen ist.
7. Die Anzahl der Kniebeugen und der aktuelle Hüftwert werden auf dem Bildschirm angezeigt.

.. note::

   - In diesem Beispiel wird keine Gelenkwinkelberechnung verwendet.
   - Es basiert auf normalisierten Koordinaten, um den Rechenaufwand zu verringern.
   - Die Methode ist leichtgewichtig und für den Raspberry Pi geeignet.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel "Show Video" und zeigt den Live-Kamerastream an.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_8.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Wenn eine Person vor der Kamera steht:

   - MediaPipe Pose erkennt in Echtzeit 33 Körper-Landmarks.
   - Ein vollständiges Körperskelett wird auf dem Bildschirm dargestellt.
   - Das System berechnet fortlaufend die relative Hüftposition (HipRel).

   Während Sie Kniebeugen ausführen:

   - Wenn Sie nach unten gehen und Ihre Hüfte den unteren Schwellenwert (DOWN_TH) unterschreitet,
     markiert das System, dass Sie sich in der „unteren“ Position befinden.
   - Wenn Sie sich wieder aufrichten und die Hüfte den oberen Schwellenwert (UP_TH) überschreitet,
     erhöht sich der Kniebeugen-Zähler um 1.

   Auf dem Bildschirm werden folgende Informationen angezeigt:

   - ``Squats: N`` — die Gesamtzahl der abgeschlossenen Kniebeugen.
   - ``HipRel: value`` — die aktuell normalisierte Hüftposition, die für die Erkennung verwendet wird.

   Der Zähler wird nur nach einem vollständigen Bewegungszyklus erhöht
   (stehen → Kniebeuge → stehen), wodurch doppelte Zählungen verhindert werden.

   Drücken Sie ``q``, um das Programm zu beenden.
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.


-----------------------------
4. Vollständiger Code
-----------------------------

Hier ist die vollständige Implementierung des Kniebeugen-Zählers:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Nach dem Ausführen des Skripts wird das System:

- das menschliche Skelett erkennen;
- die relative Hüftposition berechnen;
- den Zähler um +1 erhöhen, wenn ein vollständiger Zyklus von „in die Hocke gehen“ zu „aufstehen“ abgeschlossen ist;
- **Squats: N** sowie den aktuellen HipRel-Wert in Echtzeit auf dem Bildschirm anzeigen.

-----------------------------------------------
5. Koordinaten- und Zustandsdesign
-----------------------------------------------

Wir verwenden die folgenden 6 Schlüsselpunkte (je 3 auf jeder Seite):

.. list-table::
   :header-rows: 1

   * - Schlüsselpunkt
     - Index
     - Beschreibung
   * - Schulter
     - 11 (Links) / 12 (Rechts)
     - Oberer Referenzpunkt
   * - Hüfte
     - 23 (Links) / 24 (Rechts)
     - Kernpunkt zur Berechnung der Kniebeugenposition
   * - Knöchel
     - 27 (Links) / 28 (Rechts)
     - Unterer Referenzpunkt

.. image:: img/mp_pose_s1.png
   :alt: MediaPipe Pose Keypoints
   :align: center

Berechnungsformel für den **Hip Relative**-Wert:

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- Ein größerer hip_rel-Wert bedeutet, dass sich die Hüfte näher am Boden befindet (d. h. in der Hocke).
- Ein kleinerer hip_rel-Wert bedeutet, dass die Person aufrecht steht.

Wir definieren zwei Schwellenwerte:

- **DOWN_TH = 0.55**: Wird als Erreichen der unteren Position der Kniebeuge betrachtet
- **UP_TH = 0.45**: Wird als Rückkehr in die aufrechte Position betrachtet

Eine einfache Zustandsmaschine wird für eine zuverlässige Zählung verwendet:

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
6. Parameteranpassung und Optimierung
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Beschreibung
     - Anpassungsempfehlung
   * - DOWN_TH
     - Schwellenwert für die Kniebeugenbewegung
     - Ein höherer Wert erfordert eine tiefere Kniebeuge, um gezählt zu werden
   * - UP_TH
     - Schwellenwert für das Aufstehen
     - Ein niedrigerer Wert erfordert eine aufrechtere Körperhaltung
   * - model_complexity
     - Komplexität des Pose-Modells
     - Verwenden Sie 1 für höhere Geschwindigkeit
   * - Resolution
     - Beeinflusst Bildrate und Genauigkeit
     - Empfohlen: 640×480

.. tip::
   Für Personen unterschiedlicher Körpergröße können adaptive Schwellenwerte oder eine persönliche Kalibrierung verwendet werden, um eine genauere Zählung zu erreichen.

---------------------------------------------------------
5. Fehlerbehebung
---------------------------------------------------------

- Ungenaue Zählung

  Wenn die Anzahl der Kniebeugen nicht korrekt ist, passen die Schwellenwerte möglicherweise nicht zu Ihrer Körperhaltung oder zum Kamerawinkel.
  
  Geben Sie ``hip_rel`` in Echtzeit aus und passen Sie ``DOWN_TH`` und ``UP_TH`` entsprechend an.
  Achten Sie außerdem darauf, dass Ihre Kniebeugenbewegung klar und konsistent ausgeführt wird.

- Person wird nicht erkannt

  Wenn der Körper nicht erkannt wird, verbessern Sie die Lichtverhältnisse und vermeiden Sie komplexe Hintergründe.
  
  Stellen Sie sicher, dass Sie vollständig im Bild stehen und direkt zur Kamera ausgerichtet sind.

- Hohe Latenz

  Wenn die Videoreaktion langsam ist, reduzieren Sie ``model_complexity`` auf 1 und verringern Sie die Kameraauflösung (z. B. 640×480 oder 320×240).
  
  Schließen Sie unnötige Hintergrundprogramme, um die Leistung zu verbessern.

-----------------------------
6.  Zusammenfassung
-----------------------------

- In diesem Abschnitt wurde ein **Echtzeit-Kniebeugen-Zähler** auf Basis von Pose-Schlüsselpunkten und einer Zustandsmaschine implementiert;
- Es sind keine komplexen Winkelberechnungen erforderlich, wodurch eine hohe Ausführungseffizienz erreicht wird;
- Geeignet für Anwendungen auf Raspberry Pi oder anderen Edge-Geräten;
- Mögliche zukünftige Erweiterungen:

  - Liegestütz-/Sit-up-Erkennung
  - Datenerfassung und Visualisierung
  - Automatische Rhythmusführung und Trainingsfeedback