.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. YOLO auf dem Raspberry Pi ausführen
==============================================================

YOLO (You Only Look Once) ist ein revolutionärer Objekterkennungsalgorithmus, der sich durch seine Geschwindigkeit und Genauigkeit auszeichnet. Er transformiert die Objekterkennung in ein Regressionsproblem, bei dem alle Objektkategorien und -positionen in einem Bild durch einen einzigen Durchlauf eines neuronalen Netzes vorhergesagt werden.

Stellen Sie sich ein Bildverarbeitungssystem vor, das „alles auf einen Blick erfasst“. Ob in der Videoüberwachung, im autonomen Fahren oder bei der industriellen Qualitätskontrolle – überall dort, wo Echtzeit-Objekterkennung benötigt wird, ist YOLO im Einsatz.

.. image:: img/yolo_new.png

Abbildung: YOLOv8n in Echtzeit auf dem Raspberry Pi. Objekte im Kamerabild werden präzise erkannt und annotiert, wobei die erkannten Klassen und Konfidenzwerte auf der linken Seite angezeigt werden. Dieses Bild zeigt, wie das Modell erfolgreich Objekte wie eine Person, einen Stuhl und einen Fernseher identifiziert.

Kernprinzipien
------------------------------------------

Im Gegensatz zu älteren zweistufigen Methoden (wie R-CNN), die „zuerst Kandidatenregionen finden und diese dann identifizieren“, verfolgt YOLO einen grundlegend anderen Ansatz:

* **Einheitliches Framework**: Unterteilt das Bild in ein Raster (z. B. das ursprüngliche 7x7-Raster).

* **Rasterbasierte Vorhersage**: Jede Rasterzelle ist für die Vorhersage von Objekten verantwortlich, deren Mittelpunkt in diese Zelle fällt. Jede Zelle sagt mehrere Begrenzungsrahmen (einschließlich Position und Größe) zusammen mit ihren Konfidenzwerten voraus und sagt auch die Wahrscheinlichkeiten der Objektklassen voraus.

* **Ein-Stufen-Verarbeitung**: Klassifizierung und Lokalisierung werden gleichzeitig innerhalb desselben neuronalen Netzes durchgeführt, was wirklich „You Only Look Once“ ermöglicht und daher in der Geschwindigkeit früheren Methoden deutlich überlegen ist.

Ausführen des Codes
------------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_test.py

Der Code lädt automatisch ein Modell (ca. 6 MB) herunter und führt es auf der Kamera aus. Die Ergebnisse werden in einem Fenster mit dem Titel „YOLOv8“ angezeigt.

(Beim ersten Start wird automatisch ein etwa 6 MB großes Modell heruntergeladen):

.. code-block:: python

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")  # nano-Modell

   # Kamera initialisieren
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLO gestartet, drücken Sie 'q' zum Beenden...")

   try:
      while True:
         # Einzelbild erfassen
         frame = picam2.capture_array()
         
         # YOLO ausführen und imgsz=320 setzen
         results = model(frame, imgsz=320)
         
         # Ergebnisse zeichnen
         annotated = results[0].plot()
         
         # Ergebnisse anzeigen
         cv2.imshow("YOLO auf dem Raspberry Pi", annotated)
         
         # 'q' zum Beenden drücken
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("Beendet")



Fehlerbehebung
---------------

F: Fehler aufgrund einer Größenänderung von Numpy.dtype
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Numpy-Version zurücksetzen:

.. code-block:: bash

   # Wenn Version 2.x, auf 1.x zurücksetzen
   pip3 install "numpy<2.0" --break-system-packages --force-reinstall

F: Fehler wegen fehlender ``libopenblas.so.0``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die OpenBLAS-Bibliothek installieren:

.. code-block:: bash

   sudo apt install libopenblas-dev

F: Kamera kann nicht geöffnet werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kameraverbindung prüfen und sicherstellen, dass sie aktiviert ist:

.. code-block:: bash

   sudo raspi-config
   # Interface Options -> Camera -> Enable auswählen

F: Fehler aufgrund von Speichermangel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Auslagerungsspeicher (Swap) vergrößern:

.. code-block:: bash

   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # CONF_SWAPSIZE=2048 ändern
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon

Methoden zur Leistungsoptimierung
--------------------------------------------------------

Der Betrieb von YOLO auf einem Raspberry Pi (selbst 4B/5) kann anspruchsvoll sein. Hier sind mehrere bewährte Optimierungsmethoden:

1. **YOLO-Inferenzauflösung anpassen**: Der obige Code verwendet bereits imgsz=320, was eine ausgewogene Einstellung ist. Anpassbare Werte:

   * ``imgsz=224`` - Niedrigste Auflösung, höchste Geschwindigkeit
   * ``imgsz=320`` - Standardeinstellung
   * ``imgsz=416`` - Höhere Genauigkeit, langsamere Geschwindigkeit
   * ``imgsz=640`` - Höchste Genauigkeit, sehr langsam auf dem Raspberry Pi

2. **Das richtige Modell wählen**:

   * ``yolov8n.pt`` (6 MB) - Am schnellsten, geeignet für Echtzeiterkennung
   * ``yolov8s.pt`` (22 MB) - Etwas langsamer, aber genauer
   * ``yolov8m.pt`` (49 MB) - Langsamer, höhere Genauigkeit
   * ``yolov8l/x.pt`` - Auf dem Raspberry Pi in der Regel nicht nutzbar
   * Sie können auch Ihr eigenes trainiertes Modell verwenden, z. B. ``"/home/pi/my_model.pt"``. Wie Sie eigene Modelle trainieren, wird in späteren Kapiteln behandelt.

3. **Erkennungsklassen einschränken**: Wenn nur bestimmte Objekte erkannt werden sollen (z. B. nur Personen), ändern Sie den Code:

.. code-block:: python

   results = model(frame, classes=[0], imgsz=320)  # 0 ist die Klassen-ID für Person

Häufige Klassen-IDs:

   * 0 - Person
   * 1 - Fahrrad
   * 2 - Auto
   * 3 - Motorrad
   * 5 - Bus
   * 7 - Lastwagen

4. **Leichte Modellvarianten verwenden**:

.. code-block:: python

   # Verwenden einer beschnittenen Version von YOLOv8n (falls verfügbar)
   model = YOLO("yolov8n.pt")
   
   # Oder TensorRT-Beschleunigung verwenden (erfordert zusätzliche Konfiguration)
   # model = YOLO("yolov8n.pt")
   # model.export(format="engine")  # Als TensorRT-Engine exportieren

5. **Bildverarbeitungsrate reduzieren**: Wenn keine Echtzeitanzeige aller Einzelbilder benötigt wird, verarbeiten Sie die Bilder intermittierend:

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       
       # Jedes 3. Bild verarbeiten
       if frame_count % 3 == 0:
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           cv2.imshow("YOLO auf dem Raspberry Pi", annotated)
       
       frame_count += 1
       
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

6. **Multithreading verwenden**: Kameraerfassung und YOLO-Inferenz in verschiedene Threads aufteilen:

.. code-block:: python

   import threading
   import queue
   
   frame_queue = queue.Queue(maxsize=2)
   result_queue = queue.Queue(maxsize=2)
   
   def capture_frames():
       while True:
           frame = picam2.capture_array()
           if frame_queue.full():
               frame_queue.get()
           frame_queue.put(frame)
   
   def process_frames():
       while True:
           frame = frame_queue.get()
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           if result_queue.full():
               result_queue.get()
           result_queue.put(annotated)
   
   # Threads starten
   threading.Thread(target=capture_frames, daemon=True).start()
   threading.Thread(target=process_frames, daemon=True).start()
   
   while True:
       if not result_queue.empty():
           cv2.imshow("YOLO auf dem Raspberry Pi", result_queue.get())
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

Fortgeschrittene Anwendung
--------------------------------

Verwendung von Videodateien als Eingabe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   from ultralytics import YOLO
   
   model = YOLO("yolov8n.pt")
   cap = cv2.VideoCapture("input_video.mp4")
   
   while cap.isOpened():
       ret, frame = cap.read()
       if not ret:
           break
       
       results = model(frame, imgsz=320)
       annotated = results[0].plot()
       cv2.imshow("YOLO-Erkennung", annotated)
       
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break
   
   cap.release()
   cv2.destroyAllWindows()

Zusammenfassung
------------------

Durch dieses Tutorial haben Sie gelernt:

* Wie Sie die YOLO-Umgebung auf dem Raspberry Pi einrichten
* Wie Sie eine Echtzeit-Objekterkennung mit der Kamera durchführen
* Wie Sie häufige Installations- und Laufzeitprobleme beheben
* Verschiedene Methoden zur Optimierung der Erkennungsleistung

Die Stärke von YOLO liegt in seiner Einfachheit und Effizienz, die eine respektable Objekterkennungsleistung selbst auf eingebetteten Geräten wie dem Raspberry Pi ermöglicht. Wenn Sie weiter experimentieren, können Sie verschiedene interessante Anwendungen wie intelligente Überwachung, Objektverfolgung und Personenzählung entwickeln.