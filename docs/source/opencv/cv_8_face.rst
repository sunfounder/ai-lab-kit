.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

8. Gesichts- und Augenerkennung
=========================================

In diesem Kapitel verwenden wir die Raspberry-Pi-Kamera mit Picamera2, um Video aufzunehmen, und nutzen die Haar-Feature-Klassifikatoren von OpenCV für die **Echtzeit-Erkennung von Gesichtern und Augen**.  
Dieser Ansatz ist leichtgewichtig und sehr praktisch – ideal für Einsteigerprojekte auf dem Raspberry Pi.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_8.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Haar-Features und Erkennungsprinzip
-----------------------------------------

1. Wesen der Haar-Features

Haar-Features sind eine klassische Methode zur Objekterkennung. Sie kodieren **Helligkeitsunterschiede innerhalb von Bildregionen**, um zu bestimmen, ob eine Region wahrscheinlich ein Gesicht, Augen usw. enthält.

Typische Beispiele für Haar-Features:

- Augenbereiche sind meist dunkler als die Stirn darüber  
- Die Helligkeit ist auf beiden Seiten des Nasenrückens symmetrisch  
- Der Bereich unter dem Mund zeigt häufig ein deutliches Kantenmuster

.. image:: img/opencv_haar_f.png
   :alt: Illustration der Haar-Features
   :align: center

OpenCV benötigt vortrainierte Haar-Klassifikatoren (``.xml``-Dateien). Diese sind bereits im Beispielverzeichnis enthalten – Sie müssen sie nur laden und verwenden.

2. Erkennungspipeline

   1. Laden des trainierten Haar-Modells mit ``CascadeClassifier``  
   2. Umwandeln des Echtzeitvideos in Graustufen (für höhere Effizienz)  
   3. Verwenden von ``detectMultiScale`` zur Erkennung von Gesichts- und Augenbereichen  
   4. Zeichnen von Rechtecken um die erkannten Zielobjekte

.. image:: img/opencv_haar_show.png
   :alt: Illustration der Erkennungspipeline
   :align: center


2. Code ausführen
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

      cd ~/ai-lab-kit/opencv_python
      python3 cv_8_haarcascade.py

   .. tip::
      
      Zusätzlich stellen wir ``cv_8_haarcascade_video.py`` bereit, um Gesichter und Augen aus einer Videodatei zu erkennen.

#. Wenn Sie das Programm ausführen, erscheint ein Fenster mit dem Namen **Raspberry Pi Camera - Face Detection** und zeigt das Live-Kamerabild der Raspberry-Pi-Kamera an.

   Erkannte Gesichter im Videostream werden mit **gelben Rechtecken** markiert, und jedes erkannte Gesicht wird beschriftet (Face 1, Face 2, ...).  
   Innerhalb jeder erkannten Gesichtsregion erkennt das Programm außerdem Augen und markiert diese mit **orangefarbenen Rechtecken**.
   
   Die Erkennung funktioniert in Echtzeit, und die Rechtecke bewegen sich mit, wenn sich eine Person vor der Kamera bewegt.
   
   So beenden Sie das Programm:
   
   * Drücken Sie die **q**-Taste auf der Tastatur  
   * Oder schließen Sie das Anzeigefenster über die Schaltfläche zum Schließen (X)  
   
   Nach dem Beenden stoppt die Kamera und alle OpenCV-Fenster werden geschlossen.


3. Vollständiger Code
--------------------------------

.. code-block:: python

   # Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
   import cv2
   from picamera2 import Picamera2
   from pathlib import Path

   # -----------------------------
   # Load Haar cascade classifiers
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent

   face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
   eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   # Check if cascade files are loaded correctly
   if face_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
   if eye_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   # -----------------------------
   # Initialize Picamera2
   # -----------------------------
   picam2 = Picamera2()

   # Video configuration (resolution can be adjusted)
   config = picam2.create_video_configuration(main={"size": (640, 480)})
   picam2.configure(config)
   picam2.start()

   WIN = "Raspberry Pi Camera - Face Detection"
   print("Camera started. Press 'q' to quit.")

   try:
      while True:
         # Capture a frame (Picamera2 typically provides RGB)
         frame_rgb = picam2.capture_array()

         # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
         gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

         # Improve contrast to make detection more stable under different lighting
         gray = cv2.equalizeHist(gray)

         # Detect faces
         faces = face_cascade.detectMultiScale(
               gray,
               scaleFactor=1.2,
               minNeighbors=5,
               minSize=(60, 60)
         )

         # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
         frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

         # Draw face and eye results
         for i, (x, y, w, h) in enumerate(faces, start=1):
               # Draw face rectangle + label
               cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
               cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

               # ROI for eye detection (search eyes only inside the detected face area)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = frame_bgr[y:y + h, x:x + w]

               eyes = eye_cascade.detectMultiScale(
                  roi_gray,
                  scaleFactor=1.2,
                  minNeighbors=8,
                  minSize=(20, 20)
               )

               # Draw up to 2 eyes (typical for a face)
               for (ex, ey, ew, eh) in eyes[:2]:
                  cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

         # Show the frame
         cv2.imshow(WIN, frame_bgr)

         # Handle keyboard input
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
               break

         # Exit if the user closes the window (click X)
         if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
               break

   finally:
      picam2.stop()
      cv2.destroyAllWindows()
      print("Camera stopped.")

4. Code-Erklärung
----------------------

#. Erforderliche Bibliotheken importieren:

   .. code-block:: python

      import cv2
      from picamera2 import Picamera2
      from pathlib import Path

   OpenCV wird für die Erkennung und das Zeichnen verwendet, Picamera2 dient zum Erfassen von Frames von der Raspberry-Pi-Kamera.

#. Verzeichnis des aktuellen Skripts ermitteln:

   .. code-block:: python

      BASE_DIR = Path(__file__).resolve().parent

   Dadurch können die Cascade-XML-Dateien aus demselben Ordner wie das Python-Skript geladen werden.

#. Haar-Cascade-Klassifikatoren laden (Gesicht und Augen):

   .. code-block:: python

      face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
      eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   Haar-Cascades sind vortrainierte Modelle, die Gesichter und Augen erkennen können.

#. Prüfen, ob die Cascade-Dateien korrekt geladen wurden:

   .. code-block:: python

      if face_cascade.empty():
          raise FileNotFoundError("haarcascade_frontalface_default.xml konnte nicht geladen werden")
      if eye_cascade.empty():
          raise FileNotFoundError("haarcascade_eye.xml konnte nicht geladen werden")

   Wenn der Dateipfad falsch ist oder die Datei fehlt, ist ``CascadeClassifier`` leer.  
   Diese Prüfungen helfen, das Problem frühzeitig zu erkennen.

#. Kamera initialisieren und Auflösung festlegen:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_video_configuration(main={"size": (640, 480)})
      picam2.configure(config)
      picam2.start()

   Dadurch wird die Kamera im Videomodus mit 640×480 gestartet.

#. Frames kontinuierlich erfassen:

   .. code-block:: python

      frame_rgb = picam2.capture_array()

   In jeder Schleife wird ein Frame erfasst. Picamera2 gibt Frames normalerweise im RGB-Format zurück.

#. In Graustufen umwandeln (schneller für die Erkennung):

   .. code-block:: python

      gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

   Die Gesichts-/Augenerkennung arbeitet mit Graustufenbildern und läuft schneller als mit Farbbildern.

#. Kontrast verbessern für stabilere Erkennung:

   .. code-block:: python

      gray = cv2.equalizeHist(gray)

   Histogrammangleichung kann die Erkennung unter unterschiedlichen Lichtbedingungen verbessern.

#. Gesichter im Frame erkennen:

   .. code-block:: python

      faces = face_cascade.detectMultiScale(
          gray,
          scaleFactor=1.2,
          minNeighbors=5,
          minSize=(60, 60)
      )

   Dies gibt eine Liste von Rechtecken ``(x, y, w, h)`` für alle erkannten Gesichter zurück.

   - ``scaleFactor`` steuert die Skalierungsschritte des Bildes (kleiner = genauer, aber langsamer).
   - ``minNeighbors`` reduziert Fehl-Erkennungen (höher = strenger).
   - ``minSize`` ignoriert sehr kleine Erkennungen.

#. RGB in BGR konvertieren für Zeichnen und Anzeige:

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

   Die Zeichenfunktionen von OpenCV und ``imshow`` erwarten BGR für Farbbilder.

#. Gesichtsrechtecke und Beschriftungen zeichnen:

   .. code-block:: python

      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
      cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   Dadurch wird um jedes erkannte Gesicht ein Rechteck gezeichnet und eine Beschriftung wie „Face 1“ hinzugefügt.

#. Augen innerhalb jedes Gesichts erkennen (ROI):

   .. code-block:: python

      roi_gray = gray[y:y + h, x:x + w]
      roi_color = frame_bgr[y:y + h, x:x + w]

      eyes = eye_cascade.detectMultiScale(
          roi_gray,
          scaleFactor=1.2,
          minNeighbors=8,
          minSize=(20, 20)
      )

   ROI bedeutet „Region of Interest“. Wenn Augen nur innerhalb des Gesichtsbereichs erkannt werden, ist das schneller und reduziert Fehl-Erkennungen.

#. Bis zu zwei Augen zeichnen:

   .. code-block:: python

      for (ex, ey, ew, eh) in eyes[:2]:
          cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

   Dadurch werden Rechtecke um die ersten zwei erkannten Augen gezeichnet.

#. Ergebnis anzeigen und Beenden behandeln:

   .. code-block:: python

      cv2.imshow(WIN, frame_bgr)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
          break

   Drücken Sie ``q`` zum Beenden oder schließen Sie das Fenster, um sicher zu beenden.

#. Aufräumen (wird immer ausgeführt):

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Die Kamera wird gestoppt und alle OpenCV-Fenster werden geschlossen, auch wenn ein Fehler auftritt.


5. Vor- und Nachteile der Haar-Erkennung
-----------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspekt
     - Vorteile
     - Nachteile
   * - Geschwindigkeit
     - Sehr schnell; geeignet für Raspberry Pi
     - -
   * - Genauigkeit
     - Funktioniert gut bei frontalen Gesichtern
     - Empfindlich gegenüber Rotation und Profilansichten
   * - Beleuchtung
     - Gut bei gleichmäßiger Beleuchtung
     - Leistung sinkt bei zu heller/dunkler Umgebung
   * - Modell
     - Kleine Modellgröße; leicht zu deployen
     - Weniger genau als Deep-Learning-Methoden

Da Haar-Features leichtgewichtig und schnell sind, sind sie auf Embedded-Geräten weiterhin sehr praktisch.


6. Häufige Verbesserungen
------------------------------------

1. **Vorverarbeitung der Beleuchtung**: Histogrammangleichung oder CLAHE vor der Erkennung anwenden, um die Leistung bei schwachem Licht zu verbessern.  
2. **Erkennung aus mehreren Winkeln**: Sowohl Front- als auch Profil-Gesichtsklassifikatoren laden, um mehr Posen zu erkennen.  
3. **Mehr Gesichtsmerkmale**: Haar-Klassifikatoren für Augen/Mund/Nase hinzufügen, um die Erkennung zu erweitern.  
4. **DNN statt Haar verwenden**: OpenCV DNN + ResNet/MobileNet kann eine höhere Genauigkeit liefern (benötigt jedoch mehr Rechenleistung).


7. Erweiterte Übungen
---------------------

- Verwenden Sie ``cv2.equalizeHist`` auf dem Graustufenbild, um die Erkennung bei schwachem Licht zu verbessern.  
- Fügen Sie Haar-Klassifikatoren für Mund oder Nase hinzu, um weitere Gesichtsmerkmale zu erkennen.  
- Zeichnen Sie den Erkennungsprozess mit ``cv2.VideoWriter`` auf.  
- Kombinieren Sie das Programm mit GPIO-Ausgabe für ein Raspberry-Pi-Projekt: „LED einschalten, wenn ein Gesicht erkannt wird“.  
