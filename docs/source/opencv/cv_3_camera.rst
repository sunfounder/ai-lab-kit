.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Echtzeit-Kameraaufnahme
================================================================

In den vorherigen Kapiteln haben wir gelernt, wie man lokale Videodateien liest und abspielt.  
In diesem Kapitel gehen wir einen Schritt weiter und verwenden die **Raspberry-Pi-Kamera** für die Echtzeit-Videoaufnahme sowie **Farbraumkonvertierungen** mit OpenCV.


1. Projektziele
--------------------------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

- Verwenden von **Picamera2**, um Kameraframes in Echtzeit aufzunehmen  
- Umwandeln der Kameraausgabe vom BGRA-Format in das BGR-Format  
- Verwenden von OpenCV für die Echtzeitvorschau  
- Verständnis der Eigenschaften und Einsatzbereiche verschiedener Farbräume

.. image:: img/opencv_camera.png
   :alt: Darstellung der Echtzeit-Kameravorschau
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
      python3 cv_3_camera.py

#. Wenn Sie das Programm ausführen, erscheinen zwei OpenCV-Fenster:

   * **BGR Frame** – zeigt das Live-Kamerabild in Farbe  
   * **GRAY Frame** – zeigt die Graustufenversion desselben Bildes  
   
   Sie können das Programm auf zwei Arten beenden:
   
   * Drücken Sie die **q**-Taste auf der Tastatur  
   * Schließen Sie eines der Fenster über die Schaltfläche zum Schließen (X)  
   
   Nach dem Beenden stoppt die Kameraübertragung und alle OpenCV-Fenster werden geschlossen.

3. Beispielcode
-------------------------------

Unten finden Sie das vollständige Python-Beispiel für dieses Kapitel (``cv_3_camera.py``):

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. Code-Erklärung
-------------------

#. Erforderliche Bibliotheken importieren:

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2 erfasst Frames von der Raspberry-Pi-Kamera, und OpenCV wird für Bildkonvertierung und Anzeige verwendet.

#. Ein Picamera2-Objekt erstellen und die Kamera konfigurieren:

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   Dadurch wird die Kamera mit einer Auflösung von 640×480 gestartet.  
   ``XRGB8888`` ist ein 4-Kanal-Format, sodass jedes aufgenommene Frame BGRA-ähnlich ist.

#. Ein Frame als NumPy-Array erfassen:

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   In jeder Schleife wird ein Frame von der Kamera gelesen.

#. Das Frame für die Anzeige konvertieren:

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr`` wird für die normale Farbdarstellung verwendet.
   - ``frame_gray`` ist eine Graustufenversion desselben Frames.

#. Frames in zwei Fenstern anzeigen:

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   Dadurch werden zwei OpenCV-Fenster geöffnet: eines zeigt das Farbbild, das andere die Graustufenversion.

#. Abbruchbedingungen (``q`` drücken oder Fenster schließen):

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - Drücken Sie ``q``, um das Programm zu beenden.
   - Das Schließen eines der Fenster beendet das Programm ebenfalls sicher.

#. FPS begrenzen, um die CPU-Auslastung zu reduzieren:

   .. code-block:: python

      time.sleep(1 / 30)

   Dadurch wird eine kleine Verzögerung hinzugefügt, sodass die Schleife mit etwa 30 FPS läuft, was die CPU-Belastung auf dem Raspberry Pi reduzieren kann.

#. Kamera stoppen und OpenCV-Fenster schließen:

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Dadurch wird die Kamera freigegeben und alle OpenCV-Fenster werden geschlossen, bevor das Programm beendet wird.

5. Die Bedeutung der Farbraumkonvertierung
-------------------------------------------------------------------

Das von der Kamera ausgegebene Rohbildformat entspricht nicht immer dem Format, das OpenCV für die Verarbeitung benötigt.  
In diesem Beispiel gibt Picamera2 Bilder im **XRGB8888 (BGRA)**-Format aus, während OpenCV hauptsächlich das **BGR**-Format verwendet.

Daher müssen wir das Bild wie folgt konvertieren:

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

Dadurch wird sichergestellt, dass das Bild in der von OpenCV verwendeten Standardreihenfolge der BGR-Kanäle vorliegt und korrekt angezeigt sowie verarbeitet werden kann.

Anschließend können wir das BGR-Bild zur weiteren Verarbeitung in ein Graustufenbild umwandeln:

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

Dadurch lassen sich kamerabasierte Bilder in ein Format umwandeln, das sich für OpenCV-Bildverarbeitungsabläufe eignet.

**Gängige Farbräume und ihre Anwendungsfälle**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Farbraum
     - Eigenschaften
     - Typische Anwendungsfälle
   * - **BGR**
     - Standardformat von OpenCV
     - Bildanzeige, grundlegende Verarbeitung, Kantenerkennung
   * - **RGB**
     - Für Menschen intuitiver
     - Visualisierung, Eingabe für Deep-Learning-Modelle
   * - **GRAY**
     - Einkanal-Graustufenbild
     - Objekterkennung, Kantenerkennung, Leistungsoptimierung
   * - **HSV**
     - Trennt Farbe und Helligkeit
     - Farberkennung, Objektverfolgung, Segmentierung
   * - **YCrCb**
     - Trennt Luminanz und Chrominanz
     - Gesichtserkennung, Videokompression, Robustheit gegenüber Beleuchtung

Zum Beispiel eignet sich **HSV** häufig besser für **Farberkennung und Objektverfolgung**,  
während **YCrCb** robuster für **Gesichtserkennung** oder Szenen mit wechselnden Lichtverhältnissen ist.

6. Erweiterungen und Übungen
-------------------------------------------

- Versuchen Sie, das Bild von BGR nach GRAY oder HSV zu konvertieren und beobachten Sie die Ergebnisse.

   Verwenden Sie zum Beispiel:

   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
   - und weitere

- Testen Sie verschiedene Auflösungen (z. B. 1280×720) und beobachten Sie die Auswirkungen auf Latenz und Bildrate.  
- Kombinieren Sie diesen Code mit dem vorherigen Video-Wiedergabebeispiel, um zwischen einem Kamerastream und einer Videodatei umzuschalten.