.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. Video abspielen
=======================================

In diesem Kapitel lernen Sie, wie Sie Videostreams in OpenCV einlesen und abspielen und wie Sie die Wiedergabegeschwindigkeit durch Berechnung der Frame-Verarbeitungszeit steuern können.



1. Projektübersicht
-------------------

In diesem Abschnitt erreichen wir folgende Ziele:

- Verwenden von ``cv2.VideoCapture``, um eine Videodatei zu öffnen
- Lesen und Anzeigen des Videos Frame für Frame
- Automatisches Neustarten des Videos nach dem Ende
- Steuerung der Wiedergabebildrate durch Berechnung der Verarbeitungszeit
- Drücken der Taste ``q``, um die Wiedergabe zu beenden

.. image:: img/opencv_video.png
   :alt: Darstellung der Video-Wiedergabeoberfläche
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
      python3 cv_2_video.py

#. Nach dem Start des Skripts öffnet OpenCV ein Fenster mit dem Titel **Video** und zeigt die Videoframes in Echtzeit an.  

   Wenn das Video das Ende erreicht, startet es automatisch wieder vom Anfang.
   
   Um das Programm zu beenden, können Sie:
   
   * **q** auf der Tastatur drücken, um die Wiedergabe zu beenden  
   * das Fenster über die Schaltfläche zum Schließen schließen  

   Sobald das Fenster geschlossen wird, werden alle OpenCV-Ressourcen freigegeben und das Programm beendet.


3. Vollständiger Code
------------------------------

.. code-block:: python

  import cv2

  # Open the video file
  cap = cv2.VideoCapture("sample2.mp4")

  while True:
      # Read one frame from the video
      ret, frame = cap.read()

      # If the video ends, restart from the beginning
      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

      # Resize the frame for better display performance
      frame = cv2.resize(frame, (640, 480))

      # Display the frame in a window named "Video"
      cv2.imshow("Video", frame)

      # Wait 30 ms between frames (~30 FPS)
      # This also processes GUI events (keyboard and window events)
      key = cv2.waitKey(30) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
          break

      # Exit if the user closes the window (click the close button)
      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

  # Release the video capture object
  cap.release()

  # Close all OpenCV windows
  cv2.destroyAllWindows()


4. Code-Erklärung
-----------------------

#. Videodatei öffnen:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Dies öffnet die Videodatei und erstellt ein ``VideoCapture``-Objekt zum Lesen der Frames.

#. Einen Frame aus dem Video lesen:

   .. code-block:: python

      ret, frame = cap.read()

   - ``ret`` ist ``True``, wenn ein Frame erfolgreich gelesen wurde.
   - ``ret`` wird ``False``, wenn das Video endet oder das Lesen fehlschlägt.
   - ``frame`` enthält die Bilddaten (ein NumPy-Array).

#. Video neu starten, wenn es endet:

   .. code-block:: python

      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

   Wenn das Video endet, wird hier die Wiedergabeposition auf den ersten Frame zurückgesetzt, sodass das Video erneut gestartet wird.

#. Frame skalieren:

   .. code-block:: python

      frame = cv2.resize(frame, (640, 480))

   Dadurch wird jeder Frame auf 640×480 skaliert, was eine flüssigere Anzeige und geringere CPU-Auslastung auf dem Raspberry Pi ermöglicht.

#. Frame anzeigen:

   .. code-block:: python

      cv2.imshow("Video", frame)

   Dies zeigt den aktuellen Frame in einem Fenster mit dem Namen ``Video`` an.

#. Wiedergabegeschwindigkeit steuern und Tastatureingaben verarbeiten:

   .. code-block:: python

      key = cv2.waitKey(30) & 0xFF

   Dadurch wartet das Programm etwa 30 ms zwischen zwei Frames (ca. 30 FPS) und verarbeitet gleichzeitig GUI-Ereignisse.

#. Mit ``q`` beenden:

   .. code-block:: python

      if key == ord("q"):
          break

   Drücken Sie ``q``, um das Programm zu stoppen.

#. Programm beenden, wenn das Fenster geschlossen wird:

   .. code-block:: python

      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

   Dadurch wird überprüft, ob das Fenster noch sichtbar ist.  
   Wenn der Benutzer das Fenster schließt, beendet das Programm sicher die Ausführung.

#. VideoCapture-Objekt freigeben:

   .. code-block:: python

      cap.release()

   Dadurch wird die Videodatei-Ressource freigegeben.

#. Alle OpenCV-Fenster schließen:

   .. code-block:: python

      cv2.destroyAllWindows()

   Dadurch werden alle OpenCV-Fenster geschlossen und die GUI-Ressourcen freigegeben.


5. Weitere Übungen
-------------------

- Versuchen Sie, die Fenstergröße zu ändern, um zu sehen, wie sich dies auf die Bildklarheit auswirkt.  
- Ersetzen Sie die Videodatei durch andere Dateien, um die Kompatibilität zu testen.  
- Geben Sie die Verarbeitungszeit pro Frame aus, um die Beziehung zwischen FPS und Wiedergabeverzögerung besser zu verstehen.