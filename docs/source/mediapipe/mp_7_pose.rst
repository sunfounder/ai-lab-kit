.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. Menschliche Posenschätzung
================================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

Nach der Implementierung von Hand- und Gestenerkennung
stellt dieses Kapitel **MediaPipe Pose** vor —
ein leichtgewichtiges, aber leistungsstarkes Modul zur Echtzeit-Schätzung menschlicher Körperposen.

Mit MediaPipe Pose können wir **33 Körper-Landmarks**
in Echtzeit erkennen und ein vollständiges Körperskelett
im Videostream darstellen.

.. image:: img/mp_pose.png
   :width: 400
   :align: center

Dieses Modul kann verwendet werden für:

- Aktionserkennung
- Haltungskorrektur
- Fitnessüberwachung
- Bewegungsanalyse

------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Das Programm führt die folgenden Schritte aus:

1. Initialisierung des MediaPipe-Pose-Modells
   (Konfiguration der Modellkomplexität und optionaler Segmentierung).
2. Erfassen von Videoframes mit ``Picamera2``.
3. Konvertieren der Frames in das RGB-Format (erforderlich für MediaPipe).
4. Ausführen des Pose-Modells, um 33 Körper-Schlüsselpunkte zu erhalten.
5. Zeichnen der Schlüsselpunkte und Skelettverbindungen mit OpenCV.
6. Anzeige des annotierten Videostreams in Echtzeit.

Dieses Kapitel bildet die Grundlage für fortgeschrittene
Mensch–Computer-Interaktion und Analyse von Körperbewegungen.


------------------------
3. Code ausführen
------------------------

.. important::


   Stellen Sie vor dem Start sicher, dass:

   * das Pan-Tilt-Modul montiert ist
   * Sie Zugriff auf den Raspberry-Pi-Desktop haben
   * das Codepaket installiert ist
   * das Fusion HAT+ installiert und konfiguriert ist
   * OpenCV installiert ist

   Detaillierte Anweisungen finden Sie unter :ref:`opencv_install`.

#. Öffnen Sie das Terminal und geben Sie den folgenden Befehl ein:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   Wenn Sie MediaPipe Pose mit einem aufgezeichneten Video verwenden möchten, können Sie folgenden Befehl ausführen:

   .. code-block:: bash
   
      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel "Show Video" und zeigt den Live-Kamerastream an.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
         
   Wenn eine Person vor der Kamera erscheint:
   
   - MediaPipe Pose erkennt in Echtzeit 33 Körper-Landmarks.
   - Ein vollständiges Körperskelett wird im Videobild dargestellt.
   - Wichtige Gelenke wie Schultern, Ellbogen, Handgelenke, Hüften, Knie und Knöchel werden durch Linien verbunden.
   
   Während sich die Person bewegt:
   
   - folgen die Skelett-Schlüsselpunkte den Körperbewegungen flüssig.
   - aktualisiert sich das Skelett kontinuierlich in Echtzeit.
   
   Wenn Hintergrundsegmentierung aktiviert ist (``enable_segmentation=True``),
   berechnet das Modell intern eine Segmentierungsmaske, obwohl in diesem Beispiel
   nur das Skelett angezeigt wird.
   
   Wenn keine Person erkannt wird, zeigt das Programm lediglich den normalen Kamerastream ohne Markierungen an.
   
   Drücken Sie ``q``, um das Programm zu beenden.
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.

-----------------------------
4. Vollständiger Code
-----------------------------

Hier ist ein einfaches Programm zur Erkennung menschlicher Körperposen:

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
       static_image_mode=False,  # False for processing video streams
       model_complexity=2,       # 0~2, higher is more accurate
       enable_segmentation=True, # Enable background segmentation (optional)
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Pose detection
      results = pose.process(frame_rgb)

      # Convert RGB back to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If human body is detected, draw skeleton
      if results.pose_landmarks:
         drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Nach dem Ausführen des Programms zeigt der Kamerastream ein Echtzeit-Skelett des menschlichen Körpers an, einschließlich:

- 33 Schlüsselpunkte
- Skelett-Verbindungslinien
- Das Skelett folgt den Bewegungen, wenn sich die Person bewegt

-----------------------------
5. Code-Erklärung
-----------------------------

**1. Bibliotheken importieren**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  Steuert die Raspberry-Pi-Kamera und basiert auf libcamera.

* **cv2 (OpenCV)**
  Wird für Farbkonvertierung (BGR↔RGB), Anzeige von Fenstern und Zeichnen von Grafiken verwendet.

* **mediapipe.python.solutions.pose**
  Das **Pose-Modell** von MediaPipe, das **33 Ganzkörper-Schlüsselpunkte** erkennen kann (Kopf, Schultern, Ellbogen, Knie usw.) und außerdem Segmentierungsmasken (Person vs. Hintergrund) zurückgeben kann.

* **drawing_utils / drawing_styles**
  Integrierte Zeichenwerkzeuge und Stildefinitionen von MediaPipe, die zum Zeichnen von Schlüsselpunkten und Skelettlinien verwendet werden.

**2. Pose-Modell initialisieren**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Continuous video mode
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False``: Gibt an, dass die Eingabe ein kontinuierlicher Videostream und kein Einzelbild ist. Nach der ersten Erkennung wird Tracking verwendet, was schneller ist. In der Regel auf False gesetzt.

* ``model_complexity=1``: Modellkomplexität, 0=leicht, 1=mittel, 2=hohe Genauigkeit (langsamer). Setzen Sie 1 oder 2, wenn die Leistung des Raspberry Pi ausreichend ist.

* ``enable_segmentation=True``: Gibt eine Segmentierungsmaske für die Person aus und kann Vordergrund (Person) vom Hintergrund unterscheiden. Wenn True, können Effekte wie Hintergrundersetzung oder Chroma-Key umgesetzt werden. Diese Verwendung wird in der folgenden Dokumentation erklärt: :ref:`mp_pose_segmentation`

MediaPipe Pose gibt eine Ergebnisstruktur zurück, die Folgendes enthält:

* ``pose_landmarks``: 33 Schlüsselpunkte;
* ``pose_world_landmarks``: 3D-Weltkoordinaten;
* ``segmentation_mask``: Segmentierungskarte der Person.

**3. Kamera öffnen**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

* Kameraobjekt ``Picamera2()`` erstellen
* Auflösung auf **640x480** setzen, Pixelformat ``"XRGB8888"`` (4-Kanal BGRA).
  Dieses Format hat die beste Kompatibilität mit OpenCV und vermeidet zusätzliche Dekodierungsschritte.
* Kamera starten.

Optional:
``picam2.start_preview(Preview.QTGL)`` kann den Videostream direkt über die GPU anzeigen; hier auskommentiert und stattdessen wird OpenCVs ``imshow()`` verwendet.

**4. Hauptschleife: Verarbeitung jedes Frames**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Capture a frame from the camera (BGRA format)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. Das aktuelle Frame erfassen. Picamera2 gibt Bilder standardmäßig im **BGRA**-Format (Blue, Green, Red + Alpha) zurück.
2. In **BGR** konvertieren für die weitere Verarbeitung mit OpenCV.

.. code-block:: python

   # Convert to RGB for MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

MediaPipe-Modelle **müssen RGB verwenden**.

* Aufruf von ``pose.process()`` zur Erkennung der Schlüsselpunkte.
* ``results`` ist ein komplexes Objekt, das enthalten kann:

  * ``results.pose_landmarks``: Schlüsselpunkte (33 Punkte)
  * ``results.pose_world_landmarks``: 3D-Koordinaten
  * ``results.segmentation_mask``: Segmentierungsmaske

.. code-block:: python

   # Convert back to BGR for OpenCV display
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

Zurückkonvertieren, da OpenCVs ``imshow()`` das BGR-Format benötigt.

**5. Pose-Schlüsselpunkte zeichnen**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

Wenn ein menschlicher Körper erkannt wird:

* ``results.pose_landmarks`` enthält ``(x, y, z, visibility)`` für jeden Schlüsselpunkt.

  * ``x, y``: Normalisierte Koordinaten (0~1)
  * ``z``: Relative Tiefe
  * ``visibility``: Sichtbarkeitskonfidenz des Schlüsselpunktes (0~1)

* Erklärung der ``draw_landmarks``-Parameter:

   * ``frame``: Bild, auf dem gezeichnet wird (BGR-Format)
   * ``results.pose_landmarks``: Menschliche Schlüsselpunkte des aktuellen Frames
   * ``mp_pose.POSE_CONNECTIONS``: Verbindungsregeln (welche Punkte mit Linien verbunden werden)
   * ``landmark_drawing_spec``: Zeichenstil für Punkte
   * ``connection_drawing_spec``: Zeichenstil für Linien (optional, verwendet standardmäßig den Systemstil)

Effekt: Zeichnet das Körperskelett (Verbindungen für Kopf, Arme und Beine) sowie die Schlüsselpunkte (Gelenkpositionen) auf das Bild.

**6. Frame anzeigen & Exit-Logik**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

Jedes Frame wird im Fenster ``"Show Video"`` angezeigt.
Die Schleife wird beendet, wenn die Taste ``q`` gedrückt wird.

**7. Ressourcen freigeben**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Vorschau stoppen, Kamera freigeben und alle OpenCV-Fenster schließen.

-----------------------------

6. Einführung in das Pose-Modell
----------------------------------------------

Das MediaPipe-Pose-Modul liefert **33 Schlüsselpunkte**, die Bereiche wie Kopf, Rumpf, Arme und Beine abdecken:

.. list-table::
   :header-rows: 1

   * - Körperteil
     - Index
   * - Nose
     - 0
   * - Left/Right Shoulder
     - 11 / 12
   * - Left/Right Elbow
     - 13 / 14
   * - Left/Right Wrist
     - 15 / 16
   * - Left/Right Hip
     - 23 / 24
   * - Left/Right Knee
     - 25 / 26
   * - Left/Right Ankle
     - 27 / 28
   * - Left/Right Foot Index
     - 31 / 32

Diese Punkte können für **Haltungsbewertung**, **Bewegungszählung** (z. B. Kniebeugen, Liegestütze, Yoga-Posenerkennung) usw. verwendet werden.

-----------------------------
7. Leistung und Optimierung
-----------------------------

.. list-table::
   :header-rows: 1

   * - Element
     - Auswirkung
     - Optimierungsvorschlag
   * - Auflösung
     - Höhere Auflösung erhöht die Genauigkeit, aber auch die Latenz
     - Verwenden Sie 640x480, um Leistung und Geschwindigkeit auszubalancieren
   * - model_complexity
     - Verbessert die Erkennungsgenauigkeit, verlangsamt jedoch die Berechnung
     - Für Raspberry Pi wird 1~2 empfohlen
   * - segmentation
     - Erhöht die GPU/CPU-Last
     - Empfohlen zu deaktivieren, wenn kein Hintergrundersatz benötigt wird

------------------------------------------------------------
8. Fehlerbehebung
------------------------------------------------------------

- Keine Person erkannt

  Wenn das Programm läuft, aber keine Person erkannt wird, stellen Sie sicher, dass sich der gesamte Körper im Kamerabild befindet. Vermeiden Sie starkes Gegenlicht und verbessern Sie die Beleuchtung. Halten Sie einen Abstand von etwa 1–2 Metern zur Kamera ein, um optimale Ergebnisse zu erzielen.

- Video ist langsam oder ruckelt

  Wenn die Bildrate niedrig ist, reduzieren Sie die Auflösung auf 640×480 oder niedriger. Setzen Sie ``model_complexity = 1`` für eine bessere Leistung. Deaktivieren Sie die Segmentierung, wenn sie nicht benötigt wird, und schließen Sie andere Hintergrundprogramme, um Systemressourcen freizugeben.

- Segmentation Fault tritt auf

  Die meisten Segmentation Faults werden durch eine Nichtübereinstimmung zwischen der Systemarchitektur und dem installierten MediaPipe-Wheel verursacht.

  Überprüfen Sie Ihre Systemarchitektur:

  .. code-block:: bash

     uname -m

  Die Ausgabe sollte ``aarch64`` sein.

  Wenn ``armv7l`` oder ``armhf`` angezeigt wird, verwenden Sie ein 32-Bit-Raspberry-Pi-OS, das nicht mit dem offiziellen MediaPipe-Wheel kompatibel ist.

  Sie können dies auch in Python überprüfen:

  .. code-block:: python

     import platform
     print(platform.machine())

  Das Ergebnis muss ebenfalls ``aarch64`` sein.

- aarch64 wird verwendet, aber trotzdem tritt ein Segmentation Fault auf

  Dies kann passieren, wenn einige TensorFlow-Lite-XNNPACK-Kernel nicht vollständig mit Ihrer MediaPipe-Build kompatibel sind.

  Mögliche Lösungen:

  - Verwenden Sie ``model_complexity = 1`` (empfohlen in diesem Tutorial).
  - Stellen Sie sicher, dass MediaPipe in der richtigen virtuellen Umgebung installiert ist.
  - Installieren Sie ein für Raspberry Pi optimiertes Wheel wie ``mediapipe-bin`` (PINTO0309-Version).

- ``model_complexity = 2`` stürzt ab, aber ``1`` funktioniert

  Komplexität 2 lädt ein größeres Modell, das möglicherweise erweiterte CPU-Optimierungen auslöst. Auf dem Raspberry Pi werden einige optimierte TensorFlow-Lite-Kernel möglicherweise nicht vollständig unterstützt. Komplexität 1 vermeidet diese Kernel und ist auf dem Raspberry Pi in der Regel stabiler und schneller.



-----------------------------
9. Zusammenfassung
-----------------------------

- In diesem Kapitel wurde **Echtzeit-Erkennung menschlicher Körperskelette** auf Basis von MediaPipe Pose implementiert;
- Pose liefert 33 Schlüsselpunkte, die in Bereichen wie Fitness, Haltungsanalyse und Aktionserkennung verwendet werden können;
- Durch Anpassung von Auflösung und Modellkomplexität kann ein flüssiger Betrieb auf dem Raspberry Pi erreicht werden;
- Auf Basis dieser Schlüsselpunkte können anschließend folgende Anwendungen entwickelt werden:

  - Aktionserkennung (z. B. „Hand heben“, „Kniebeugen“)
  - Haltungsbewertung (z. B. „Ist die Sitzhaltung korrekt?“)
  - Menschliche Interaktionssteuerung.