.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. Green-Screen
====================================

------------------------------------------------------------
1. Überblick
------------------------------------------------------------

In diesem Kapitel wird die **Personensegmentierung** von
MediaPipe Pose verwendet, um einen einfachen **Green-Screen-Effekt**
zu realisieren.

Durch die Trennung der Person vom Hintergrund
kann der ursprüngliche Hintergrund durch eine einfarbig grüne Fläche ersetzt werden.
Dadurch lassen sich folgende Anwendungen umsetzen:

- Virtuelle Hintergründe
- Chroma-Key-Komposition (OBS / NLE)
- Effekte für Live-Streaming
- AR-ähnlicher Szenenersatz

.. image:: img/mp_pose_green.png
   :align: center


------------------------------------------------------------
2. Funktionsweise
------------------------------------------------------------

Der Green-Screen-Effekt wird mit den folgenden Schritten umgesetzt:

1. Initialisieren des Pose-Modells mit ``enable_segmentation=True``.
2. Für jedes Frame wird ``results.segmentation_mask`` abgerufen.
3. Die Maske ist eine einkanalige Wahrscheinlichkeitskarte (Bereich 0–1).
4. Ein Schwellenwert (z. B. 0.5) trennt Vordergrund und Hintergrund.
5. Hintergrundpixel werden durch eine einfarbig grüne Fläche ersetzt.
6. Optional können Weichzeichnen oder morphologische Filter angewendet werden, um die Kanten zu glätten.

Diese Methode ist leichtgewichtig und läuft in Echtzeit auf dem Raspberry Pi
und dient gleichzeitig als praktisches Beispiel für Personensegmentierung.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

   Wenn Sie MediaPipe Pose mit einem aufgezeichneten Video verwenden möchten, können Sie folgenden Befehl ausführen:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

#. Nach dem Start des Programms öffnet sich ein Fenster mit dem Titel "Show Video" und zeigt den Live-Kamerastream an.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_9.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   Im selben Fenster erscheint ein Trackbar-Regler mit dem Namen ``Mask``. Er steuert den Segmentierungsschwellenwert (0–100), der Standardwert ist 50 (0.5).

   Wenn eine Person vor der Kamera erscheint:

   - MediaPipe Pose erzeugt für jedes Frame eine ``segmentation_mask``.
   - Pixel mit Maskenwerten über dem Schwellenwert werden als Vordergrund (Person) behandelt.
   - Alle anderen Pixel werden durch einen einfarbig grünen Hintergrund ersetzt (Green-Screen-Effekt).

   Wenn Sie den ``Mask``-Regler bewegen:

   - Ein höherer Schwellenwert behält nur den sichersten Vordergrundbereich (weniger Hintergrunddurchsickern, aber eventuell abgeschnittene Körperteile).
   - Ein niedrigerer Schwellenwert nimmt mehr Pixel als Vordergrund auf (vollständigere Silhouette, aber möglicherweise mehr Hintergrundrauschen).

   Wenn keine Segmentierungsmaske verfügbar ist, zeigt das Programm lediglich den normalen Kamerastream ohne Hintergrundersatz an.

   Drücken Sie ``q``, um das Programm zu beenden.  
   Die Kamera stoppt und das OpenCV-Fenster wird automatisch geschlossen.

-----------------------------
4. Vollständiger Code
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: empty callback for trackbars ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Nach dem Ausführen des Skripts bleibt die Person (Vordergrund) erhalten, während der Hintergrund durch eine einfarbig grüne Fläche ersetzt wird.
Dies kann direkt für nachfolgendes Keying mit **Chroma Key** in OBS, Premiere, DaVinci Resolve usw. verwendet werden.

-------------------------------------
5. Erklärung der wichtigsten Punkte
-------------------------------------

``segmentation_mask`` ist ein **einkanaliges Float-Bild** (Bereich 0~1) mit derselben Größe wie das Eingabebild:

- Wert **nahe 1**: Hohe Wahrscheinlichkeit für **Vordergrund (Person)**;
- Wert **nahe 0**: Hohe Wahrscheinlichkeit für **Hintergrund**.

Üblicherweise wird ein Schwellenwert **T** (z. B. 0.5) festgelegt und eine Bedingungsmaske erstellt:

.. code-block:: python

   condition = (mask > T)[..., None]

Hier richten wir einen Trackbar-Regler ein, um den Schwellenwert in Echtzeit anzupassen:

.. code-block:: python

   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

Anschließend können wir ``np.where(condition, frame, background)`` verwenden, um den Hintergrund zu ersetzen; hier ersetzen wir ihn durch Grün:

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
6. Effekt und Kantenoptimierung
----------------------------------------------------

Eine direkte Binärschwellwertbildung kann gezackte Kanten oder kleine Löcher an Haar- und Kleidungskanten verursachen.
**Leichte Nachbearbeitung** kann die Kanten verbessern:

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **Empfohlener T-Wertbereich 0.3~0.7**: In dunklen Umgebungen oder bei konservativen Modellen kann der Wert etwas gesenkt werden; bei stärkerem Rauschen kann er erhöht werden.
   - Der Unschärfekernel sollte nicht zu groß sein, da sonst die Personenkontur „grün auslaufen“ kann.

--------------------------------------------------------

7. Verwendung eines benutzerdefinierten Hintergrunds (Bild/Video)
-------------------------------------------------------------------------

Ersetzen Sie das einfarbige Grün durch ein eigenes Hintergrundbild:

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

Oder verwenden Sie ein anderes Video als Hintergrund (lesen Sie das nächste Frame ``bg_frame``, passen Sie die Größe an und ersetzen Sie es entsprechend).

----------------------------------------------------
8. Balance zwischen Leistung und Qualität
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Element
     - Auswirkung
     - Empfehlung
   * - Auflösung
     - Höhere Auflösung liefert feinere Kanten, aber geringere Geschwindigkeit
     - Beginnen Sie mit 640×480; erhöhen Sie bei Bedarf für klarere Bilder
   * - model_complexity
     - Höher bedeutet präzisere Erkennung, aber geringere Geschwindigkeit
     - Für Raspberry Pi wird 1~2 empfohlen
   * - Stärke der Nachbearbeitung
     - Zu viel Blur/Morphologie kann Kanten „verschlucken“ oder Grün durchscheinen lassen
     - Kleiner Kernel + wenige Iterationen, Kantenwirkung beobachten

------------------------------------------------------------
9. Fehlerbehebung
------------------------------------------------------------

- Gezackte Kanten oder sichtbare Übergänge um die Person

  Dies passiert meist, wenn die Maske mit einem harten Schwellenwert angewendet wird, wodurch scharfe Kanten entstehen.
  
  Passen Sie den Schwellenwert mit dem ``Mask``-Regler an. Für weichere Kanten können Sie die Segmentierungsmaske leicht weichzeichnen oder eine einfache morphologische Closing-Operation vor der Komposition anwenden.

- Fehlende Teile der Person

  Wenn Teile des Körpers fehlen, kann die Beleuchtung zu schwach sein oder die Kleidung farblich mit dem Hintergrund verschmelzen.
  
  Verbessern Sie die Beleuchtung, passen Sie den Schwellenwert an und verwenden Sie möglichst einen einfachen Hintergrund mit starkem Kontrast zur Person.

- Niedrige Bildrate

  Wenn das Video langsam wirkt, ist möglicherweise die Auflösung zu hoch oder das Modell zu komplex.
  
  Reduzieren Sie die Kameraauflösung (z. B. 640×480 oder 320×240) und setzen Sie ``model_complexity`` auf 1 für bessere Leistung.

- Grüner Hintergrund überlappt mit der Person

  Wenn der grüne Hintergrund auf die Person übergreift, kann die Segmentierungsgrenze ungenau sein oder die Farbe der Person zu Verwechslungen führen.
  
  Versuchen Sie eine andere Ersatzfarbe (z. B. Blau oder Grau) oder ersetzen Sie den Hintergrund durch ein Bild statt durch eine einfarbige Fläche, um ein natürlicheres Ergebnis zu erzielen.


-----------------------------
10. Zusammenfassung
-----------------------------

- Mit ``segmentation_mask`` lässt sich schnell ein „Personenfreistellen + Hintergrundersatz“ realisieren;
- Natürlichere Kanten können durch geeignete Schwellenwerte und leichte Nachbearbeitung erreicht werden;
- Geeignet für virtuelle Hintergründe, Live-Streaming-Keying, Fernunterricht usw.;
- Als nächster Schritt können **Pose-Skelett** und **Segmentierung** kombiniert werden, um interaktivere Effekte zu erzeugen (z. B. Hintergrund ersetzen, aber das Skelett weiterhin im Vordergrund anzeigen).