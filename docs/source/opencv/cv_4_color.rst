.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. Farberkennung
===========================================

Farberkennung ist eine der grundlegendsten und zugleich praktischsten Funktionen der Computer Vision.  
In diesem Kapitel verwenden wir schrittweise erklärten Code, um **rote Objekte im HSV-Farbraum zu erkennen** und **Begrenzungsrahmen** um diese zu zeichnen.

Dies bildet die Grundlage für weiterführende Objektverfolgungstechniken (z. B. CAMShift).

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Ziel und Vorgehensweise
--------------------------------------------

- Verwenden von **Picamera2**, um Kameraframes in Echtzeit aufzunehmen  
- Umwandeln des Bildes vom BGR- in den HSV-Farbraum  
- Verwenden von ``cv2.inRange``, um rote Bereiche zu extrahieren  
- Verwenden morphologischer Filter, um Rauschen zu entfernen  
- Verwenden von ``cv2.findContours``, um die Konturen roter Objekte zu finden  
- Zeichnen von Begrenzungsrahmen um die erkannten roten Bereiche

.. image:: img/color_detection.png
   :alt: Vorschau der Farberkennung
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
      python3 cv_4_color.py

#. Wenn Sie das Programm ausführen, erscheinen zwei OpenCV-Fenster auf dem Bildschirm:

   * **Red Detection** – zeigt das Live-Kamerabild mit grünen Begrenzungsrahmen um erkannte rote Objekte  
   * **Red Mask** – zeigt das binäre Maskenbild, das für die Farberkennung verwendet wird  

   Das Programm erfasst kontinuierlich Frames von der Raspberry-Pi-Kamera und erkennt rote Bereiche in Echtzeit.  
   Wenn ein rotes Objekt erkannt wird, erscheinen auf dem Farbbild ein grünes Rechteck sowie der Flächenwert.

   Sie können das Programm auf zwei Arten beenden:

   * Drücken Sie die **q**-Taste auf der Tastatur  
   * Schließen Sie eines der OpenCV-Fenster über die Schaltfläche zum Schließen (X)  

   Nach dem Beenden stoppt die Kameraübertragung und alle OpenCV-Fenster werden geschlossen.

3. Vollständiger Code
------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. Code-Erklärung
--------------------------------

#. Picamera2 initialisieren und den Stream starten:

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   Dadurch wird die Kamera auf 640×480 konfiguriert und der Vorschaustream gestartet.  
   ``XRGB8888`` ist ein 4-Kanal-Format, daher sind die aufgenommenen Frames BGRA-ähnlich.

#. Das aufgenommene Frame in ein von OpenCV üblich verwendetes Format konvertieren:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2 liefert hier ein 4-Kanal-Bild zurück, deshalb wandeln wir es zur Verarbeitung in das standardmäßige 3-Kanal-BGR-Format um.

#. Den HSV-Farbraum für robuste Farberkennung verwenden:

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV trennt Farbe (Hue) von Helligkeit, wodurch die Farberkennung bei unterschiedlichen Lichtverhältnissen stabiler wird.

#. Zwei HSV-Bereiche für Rot definieren:

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   Rot „überlappt“ in der Hue-Skala von OpenCV-HSV (nahe 0 und nahe 180), daher werden zwei Bereiche kombiniert, um alle Rottöne abzudecken.

#. Die Maske mit Morphologie bereinigen (Rauschen reduzieren und Löcher füllen):

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** entfernt kleine störende Punkte.
   - **CLOSE** füllt kleine Löcher innerhalb der erkannten roten Bereiche.

#. Rote Bereiche finden und kleine Fragmente herausfiltern:

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   Die Konturen werden aus der binären Maske erkannt.  
   ``MIN_AREA`` ignoriert kleine rote Bereiche, um Fehldetektionen zu reduzieren.

#. Begrenzungsrahmen und Beschriftungen in das Ergebnisbild zeichnen:

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   Dadurch wird angezeigt, wo OpenCV rote Objekte gefunden hat, und die erkannte Flächengröße wird zur Referenz eingeblendet.

#. Sowohl das Ergebnis als auch die Maske anzeigen:

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   Das **Ergebnisfenster** zeigt das Kamerabild mit Rahmen, und das **Maskenfenster** zeigt das binäre Bild nur der roten Bereiche.

#. Abbruchbedingungen (Tastatur + Fensterschließen):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   Drücken Sie ``q``, um das Programm zu beenden, oder schließen Sie eines der Fenster für einen sicheren Abbruch.

#. Aufräumen:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Stoppen Sie immer die Kamera und schließen Sie die OpenCV-Fenster, um Ressourcen freizugeben.


5. Tipps zur Parameteranpassung
---------------------------------------------

- ``LOWER_RED1 / UPPER_RED1``: Passen Sie diesen Bereich an, um andere Farben zu erkennen.  
  Zum Beispiel Grün ≈ ``[35, 50, 50]`` bis ``[85, 255, 255]``.

- ``KERNEL``: Größere Kernel bewirken eine stärkere Filterung, können aber kleine Objekte entfernen.

- ``MIN_AREA``: Ein höherer Wert filtert kleine störende Konturen heraus; ein niedrigerer Wert macht die Erkennung empfindlicher.

.. note::
   Sie können zunächst nur die ``mask`` anzeigen und die Schwellenwerte so lange anpassen, bis der Zielbereich klar aussieht, und erst danach mit dem restlichen Ablauf fortfahren.




6. Erweiterungen und Übungen
----------------------------------------

- Ändern Sie den HSV-Schwellenwert, um andere Farben zu erkennen (z. B. Blau oder Grün).  
- Experimentieren Sie mit unterschiedlichen morphologischen Parametern in komplexeren Hintergründen.  