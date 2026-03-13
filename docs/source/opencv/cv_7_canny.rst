.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

7. Canny-Kantenerkennung
=========================================

In diesem Kapitel erfassen wir Echtzeitvideo mit Raspberry Pi + Picamera2 und führen eine Kantenerkennung mit dem **Canny-Algorithmus** von OpenCV durch.  
Die Kantenerkennung ist ein grundlegender Bestandteil der Computer Vision, und der Canny-Algorithmus gilt als eine der stabilsten und rauschresistentesten Methoden.

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_7.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Was macht der Canny-Algorithmus?
--------------------------------------------------

In Bildern entsprechen **Kanten** normalerweise Stellen mit starken Intensitätsänderungen (Graustufen), zum Beispiel:

- Objektumrisse
- Grenzen zwischen hellen und dunklen Bereichen
- Strukturelle Kantenlinien

Das Ziel der Canny-Kantenerkennung ist:

- **Kanteninformationen präzise zu extrahieren**, während unnötige Störungen reduziert werden;
- eine zuverlässige Grundlage für nachfolgende Verfahren wie **Konturerkennung**, **Objektsegmentierung** und **geometrische Erkennung** (z. B. Kreise, Rechtecke) zu schaffen;
- in der Robotikvision wird sie häufig für **Pfaderkennung** und **Hinderniserkennung** verwendet.

.. image:: img/opencv_canny.png
   :alt: Illustration der Canny-Kantenerkennung
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
      python3 cv_7_canny.py

   .. tip::
   
      Zusätzlich stellen wir ``cv_7_canny_video.py`` zur Verarbeitung von Videodateien sowie ``cv_7_canny_conbine.py`` bereit, um Echtzeitaufnahme und Video in einer kombinierten Ansicht zu verarbeiten.

#. Wenn Sie das Programm ausführen, erscheinen zwei OpenCV-Fenster:

   * **Camera** – zeigt das Live-Kamerabild  
   * **Canny Edges** – zeigt die in Echtzeit erkannten Kanten  
   
   Sie können die Schwellenwerte der Kantenerkennung mithilfe der Trackbars anpassen.  
   Drücken Sie **q** oder schließen Sie ein Fenster, um das Programm zu beenden.

3. Vollständiger Code
---------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2

   # Empty callback function for trackbars (required by OpenCV API)
   def _noop(x):
      pass

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()

   # Create a preview configuration:
   # size: resolution of the camera image
   # format: XRGB8888 (4-channel image, similar to BGRA)
   picam2.configure(
      picam2.create_preview_configuration(
         main={"size": (640, 480), "format": "XRGB8888"}
      )
   )

   # Start the camera
   picam2.start()

   # -----------------------------
   # Create OpenCV windows
   # -----------------------------
   WIN_CAM = "Camera"        # window for original image
   WIN_EDGE = "Canny Edges"  # window for edge detection result

   cv2.namedWindow(WIN_CAM)
   cv2.namedWindow(WIN_EDGE)

   # -----------------------------
   # Create trackbars to tune Canny thresholds
   # -----------------------------
   # low_th: lower threshold for Canny
   # high_th: higher threshold for Canny
   cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
   cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   print("Press 'q' to exit")

   # -----------------------------
   # Main loop
   # -----------------------------
   while True:
      # Capture one frame from the camera (BGRA format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for OpenCV processing
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame to grayscale
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

      # Apply Gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Read current threshold values from trackbars
      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      # Ensure high_th is always larger than low_th
      if high_th <= low_th:
         high_th = low_th + 1
         cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

      # Perform Canny edge detection
      edges = cv2.Canny(blurred, low_th, high_th)

      # Show original camera image
      cv2.imshow(WIN_CAM, frame_bgr)

      # Show edge detection result
      cv2.imshow(WIN_EDGE, edges)

      # Process GUI events and keyboard input
      key = cv2.waitKey(1) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
         break

   # -----------------------------
   # Cleanup
   # -----------------------------
   picam2.stop()             # Stop the camera
   cv2.destroyAllWindows()   # Close all OpenCV windows

4. Code-Erklärung
---------------------------------
#. Eine Callback-Funktion für die Trackbars definieren:

   .. code-block:: python

      def _noop(x):
          pass

   OpenCV-Trackbars benötigen eine Callback-Funktion.  
   Da wir darin nichts ausführen müssen, genügt eine leere Funktion.

#. Picamera2 initialisieren und das Vorschauformat festlegen:

   .. code-block:: python

      picam2 = Picamera2()
      picam2.configure(
          picam2.create_preview_configuration(
              main={"size": (640, 480), "format": "XRGB8888"}
          )
      )
      picam2.start()

   Dadurch wird die Raspberry-Pi-Kamera mit einer Auflösung von 640×480 gestartet.  
   ``XRGB8888`` ist ein 4-Kanal-Format, sodass die Frames BGRA-ähnlich sind.

#. Zwei OpenCV-Fenster erstellen:

   .. code-block:: python

      WIN_CAM = "Camera"
      WIN_EDGE = "Canny Edges"

      cv2.namedWindow(WIN_CAM)
      cv2.namedWindow(WIN_EDGE)

   Ein Fenster zeigt das originale Kamerabild, das andere das Ergebnis der Canny-Kantenerkennung.

#. Trackbars erstellen, um die Canny-Schwellenwerte in Echtzeit anzupassen:

   .. code-block:: python

      cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
      cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   - ``low_th``: unterer Schwellenwert für Canny.
   - ``high_th``: oberer Schwellenwert für Canny.
   
   Sie können diese Schieberegler verschieben, um die Empfindlichkeit der Kantenerkennung zu ändern.

#. Ein Frame erfassen und für die OpenCV-Verarbeitung konvertieren:

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Die Kamera gibt ein 4-Kanal-Bild aus, daher konvertieren wir es in das Standard-3-Kanal-BGR-Format.

#. In Graustufen konvertieren und das Bild weichzeichnen:

   .. code-block:: python

      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

   - Canny arbeitet mit Graustufenbildern.
   - Die Gaußsche Unschärfe reduziert Rauschen und verhindert zu viele falsche Kanten.

#. Trackbar-Werte lesen und gültig halten:

   .. code-block:: python

      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      if high_th <= low_th:
          high_th = low_th + 1
          cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

   Canny erwartet, dass ``high_th`` größer als ``low_th`` ist.  
   Dieser Codeblock korrigiert die Werte automatisch, wenn sie zu nah beieinander liegen.

#. Canny-Kantenerkennung ausführen:

   .. code-block:: python

      edges = cv2.Canny(blurred, low_th, high_th)

   Canny hebt starke Kanten im Bild hervor.  
   Niedrigere Schwellenwerte erkennen meist mehr Kanten, aber auch mehr Rauschen.

#. Beide Fenster anzeigen:

   .. code-block:: python

      cv2.imshow(WIN_CAM, frame_bgr)
      cv2.imshow(WIN_EDGE, edges)

   Das linke Fenster zeigt das Live-Kamerabild, das andere die erkannten Kanten.

#. Abbruchbedingungen (``q`` drücken oder Fenster schließen):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
          break

   Dadurch können Einsteiger das Programm auf zwei Arten beenden: über die Tastatur oder durch Schließen des Fensters.

#. Aufräumen:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Beenden Sie immer den Kamerastream und schließen Sie alle OpenCV-Fenster, um Ressourcen freizugeben.

5. Warum ist Canny nützlich?
--------------------------------------------

Die Ausgabe von Canny eignet sich sehr gut für weitere Computer-Vision-Aufgaben:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Anwendung
     - Beschreibung
   * - Konturerkennung
     - Verwenden Sie ``cv2.findContours`` auf dem Canny-Ergebnis, um Objektformen zu erhalten
   * - Objektsegmentierung
     - Verwenden Sie Kanten als Grundlage, um Zielobjekte vom Hintergrund zu trennen
   * - Formerkennung
     - Kombination mit Hough-Transformationen zur Erkennung von Kreisen, Linien usw.
   * - Roboternavigation
     - Erkennung von Boden, Straßen oder Hindernisumrissen zur Unterstützung der Planung
   * - OCR / Ziel-Lokalisierung
     - Textbereiche, QR-Codes und Marker besitzen oft klare Kantenstrukturen

Canny ist nicht nur „optisch beeindruckend“, sondern der **Einstiegspunkt** für viele weiterführende Computer-Vision-Pipelines.

6. Tipps zur Auswahl der Schwellenwerte
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30 30 70
   
   * - Szenario
     - low_th
     - high_th
     - Hinweise
   * - Stabile Innenbeleuchtung
     - 50
     - 150
     - Allgemeiner Fall, stabile Ergebnisse
   * - Starkes Licht & hoher Kontrast
     - 100
     - 200
     - Schwellenwerte erhöhen, um falsche Kanten zu reduzieren
   * - Schwaches Licht, viel Rauschen
     - 30
     - 100
     - Niedrigere Schwellenwerte, um mehr Details zu erhalten
   * - Sehr unscharfe Kanten
     - 20
     - 80
     - Schwellenwerte weiter senken, um die Kantenerkennung empfindlicher zu machen

Verwenden Sie die Trackbars, um schnell einen geeigneten Bereich einzustellen, und übernehmen Sie die Werte anschließend fest in Ihr Programm.


7. Erweiterte Übungen
---------------------

- Verwenden Sie ``cv2.findContours`` auf dem Canny-Ergebnis, um Objektkonturen zu zeichnen.  
- Ändern Sie die Größe des Gauß-Kernels und beobachten Sie, wie sich die Genauigkeit der Kantenerkennung verändert.  
- Testen Sie verschiedene Schwellenwerte bei schwacher und starker Beleuchtung, um den Effekt der Doppel-Schwellenwerte zu verstehen.  
- Nutzen Sie die Kantenkarte zur Formerkennung mit ``cv2.HoughLines`` (Linien) oder ``cv2.HoughCircles`` (Kreise).
