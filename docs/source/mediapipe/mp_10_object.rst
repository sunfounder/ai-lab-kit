.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_object:


10. Objekterkennung
=================================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

Neben spezialisierten Modellen für Gesicht, Hände und Pose
stellt MediaPipe auch einen allgemeinen **Object Detector**
auf Basis von TensorFlow Lite bereit.

Dieses Kapitel zeigt, wie das Modell
``efficientdet_lite0.tflite`` auf dem Raspberry Pi
für Echtzeit-Objekterkennung verwendet wird und wie die Ergebnisse
im Kamerabild visualisiert werden.

.. image:: img/mp_object.png
   :width: 500
   :align: center

Dieses Modul kann verwendet werden für:

- Echtzeit-Demonstrationen zur Objekterkennung
- Wahrnehmungssysteme für Smart Home / Robotik
- Einfache Sicherheitsüberwachung
- Embedded-Vision-Projekte


------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Das Programm führt die folgenden Schritte aus:

1. Initialisierung des MediaPipe Tasks **ObjectDetector**
   und Laden des Modells ``efficientdet_lite0.tflite``.
2. Erfassen von Frames aus dem Picamera2-Videostream.
3. Konvertieren jedes Frames in ein MediaPipe-``mp.Image``-Objekt.
4. Aufruf von ``detect_for_video`` zur Echtzeit-Objekterkennung.
5. Zeichnen von Bounding-Boxen und Labels mit OpenCV.
6. Begrenzung der Anzahl angezeigter Erkennungen, um eine übersichtliche Darstellung
   und stabile Leistung auf dem Raspberry Pi zu gewährleisten.

-----------------------------
3. Modellvorbereitung
-----------------------------

Dieses Beispiel verwendet das Modell **EfficientDet Lite0**
im TensorFlow-Lite-Format (TFLite).

EfficientDet Lite0 ist leichtgewichtig und für
Embedded-Geräte wie den Raspberry Pi optimiert.
Es bietet ein gutes Gleichgewicht zwischen Geschwindigkeit und Genauigkeit.

Die Datei ``efficientdet_lite0.tflite`` ist im Projektverzeichnis enthalten
und kann direkt verwendet werden.

* `Official model download page <https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector#efficientdet-lite0_model_recommended>`_

Wenn eine höhere Genauigkeit erforderlich ist und die Hardwareleistung ausreicht,
können Sie stattdessen verwenden:

- EfficientDet Lite1
- EfficientDet Lite2

Sie können das Modell auch durch ein eigenes,
selbst trainiertes TFLite-Objekterkennungsmodell ersetzen,
solange es den Formatanforderungen des
MediaPipe Tasks Object Detector entspricht.


------------------------
4. Code ausführen
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_object.py


#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel "Show Video" und zeigt den Live-Kamerastream an.

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_10.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Für jedes Videoframe wird das Object-Detector-Modell (``efficientdet_lite0.tflite``) in Echtzeit ausgeführt und sucht nach erkennbaren Objekten in der Szene.
   
   Wenn Objekte erkannt werden:
   
   - Um jedes Objekt wird eine rechteckige Bounding-Box gezeichnet.
   - Über der Box wird ein Label mit Konfidenzwert im Format ``name: score`` angezeigt (z. B. ``person: 0.87``).
   - Es werden nur Erkennungen oberhalb von ``SCORE_THRESHOLD`` (Standard 0.5) angezeigt.
   - Um die Darstellung übersichtlich zu halten und die Leistung zu sichern, werden pro Frame höchstens ``MAX_DRAW`` Erkennungen (Standard 20) gezeichnet.
   
   Wenn sich das Kamerabild verändert, werden Bounding-Boxen und Labels kontinuierlich in Echtzeit aktualisiert.
   
   Drücken Sie ``q``, um das Programm zu beenden.  
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.

-----------------------------
5. Vollständiger Code
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

Nach dem Ausführen des Skripts zeigt der Kamerastream:

- Bounding-Boxen um erkannte Objekte
- Klassifizierungslabels und Konfidenzwerte
- Echtzeit-Erkennung (auf dem Raspberry Pi etwa 10~20 FPS)

-----------------------------
6. Code-Erklärung
-----------------------------

**Konfiguration**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20

- ``SCORE_THRESHOLD`` steuert die minimale Konfidenz, ab der Erkennungen angezeigt werden (wird innerhalb der Tasks-Runtime angewendet).
- ``MAX_DRAW`` ist eine UI-Hilfseinstellung, um zu begrenzen, wie viele Boxen pro Frame gezeichnet werden.

**Importe**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2, numpy as np, time
   from pathlib import Path
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

- ``mediapipe.tasks.python.vision`` enthält die **ObjectDetector**-Tasks-API.
- Für Fensteranzeige und Zeichnen wird weiterhin klassisches OpenCV verwendet.

**Visualisierungs-Hilfsfunktion**

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

- Hält die Hauptschleife übersichtlich.
- Vermeidet die Verwendung nicht vorhandener „visualize“-Hilfsfunktionen; arbeitet direkt mit den Tasks-Ausgaben.

**ObjectDetector erstellen**

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

- ``RunningMode.VIDEO`` ist für Videostreams optimiert und **erfordert Zeitstempel**.
- Die Tasks-Runtime übernimmt intern Bildskalierung und Normalisierung.

**Kameraeinrichtung (Streaming-Quelle)**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

- 640×480 bietet ein gutes Verhältnis zwischen Bildrate und Genauigkeit auf dem Raspberry Pi.
- Picamera2 liefert BGRA (``XRGB8888``); wir konvertieren anschließend nach BGR/RGB.

**Erkennung pro Frame**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr,  cv2.COLOR_BGR2RGB)

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

   ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp
   detection_result = detector.detect_for_video(mp_image, ts_ms)

- MediaPipe erwartet **RGB-Bilddaten**.
- Der Zeitstempel muss **bei jedem Frame ansteigen**; für dieses Beispiel reicht ``time.time()*1000`` aus.

**Darstellung und Anzeige**

.. code-block:: python

   annotated = visualize(frame_bgr, detection_result)
   cv2.imshow("Show Video", annotated)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

- Die Hilfsfunktion gibt ein BGR-Bild zurück, das direkt mit OpenCV angezeigt werden kann.
- Drücken Sie ``q``, um die Schleife zu beenden.

**Aufräumen**

.. code-block:: python

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Geben Sie immer die Kamera frei und schließen Sie alle Fenster, um zu verhindern, dass das Gerät blockiert wird.

------------------------------------------------------
7. Leistung und Anwendungen
------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Optimierungsrichtung
     - Wirkung
     - Empfehlung
   * - Auflösung
     - Höhere Auflösung liefert klarere Bilder, aber geringere Geschwindigkeit
     - 640x480 ist ausreichend
   * - Modellauswahl
     - Lite0 ~ Lite2
     - Lite0 ist schneller, Lite2 ist genauer
   * - Mehrfachobjekt-Darstellung
     - Zu viele Objekte erhöhen die Latenz
     - ``MAX_DRAW`` zur Begrenzung verwenden

------------------------------------------------------
8. Fehlerbehebung
------------------------------------------------------

- Keine Erkennungsergebnisse

  Wenn nichts erkannt wird, ist möglicherweise die Konfidenzschwelle zu hoch.

  Versuchen Sie, ``SCORE_THRESHOLD`` zu reduzieren (z. B. von 0.5 auf 0.3) und testen Sie erneut.

- Niedrige Bildrate

  Wenn das Video langsam wirkt, sind möglicherweise das Modell oder die Auflösung zu anspruchsvoll für den Raspberry Pi.

  Verwenden Sie ein leichteres Modell (``efficientdet_lite0.tflite``) und reduzieren Sie die Auflösung (z. B. 640×480 oder 320×240). Auch das Schließen anderer Hintergrundprozesse kann die Leistung verbessern.

- Verschobene Erkennungsboxen

  Wenn Bounding-Boxen verschoben erscheinen oder außerhalb des Bildes liegen, liegt dies meist an Problemen bei der Koordinatenumrechnung.

  Stellen Sie sicher, dass die Bounding-Box-Koordinaten auf die Bildgrenzen begrenzt werden. In diesem Beispiel werden ``x1, y1, x2, y2`` bereits entsprechend begrenzt, um Zeichnungsfehler zu vermeiden.

- Unübersichtliche Erkennungsergebnisse

  Wenn zu viele Objekte erkannt werden und der Bildschirm überladen wirkt, wird die Darstellung schwer lesbar.

  Begrenzen Sie die Anzahl der gezeichneten Erkennungen mit ``MAX_DRAW`` (z. B. 10–20), um die Visualisierung klar und stabil zu halten.

-----------------------------
9. Zusammenfassung
-----------------------------

- In diesem Kapitel wurde eine allgemeine Objekterkennung auf Basis von MediaPipe Tasks implementiert;
- Das EfficientDet-Lite0-Modell bietet ein ausgewogenes Verhältnis zwischen Genauigkeit und Leistung;
- Die Methode zur Visualisierung von Erkennungsergebnissen wurde erläutert;
- Kann auf eigene Modelle erweitert werden (z. B. für Obst-, Fahrzeug- oder Gefahrgut-Erkennungsszenarien).