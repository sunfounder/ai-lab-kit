.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Objekte mit Schwenk-Neige-Einheit verfolgen
==============================================================

In den vorherigen Tutorials haben wir gelernt, wie man YOLO für die Objekterkennung auf dem Raspberry Pi verwendet. Die Erkennung ist jedoch nur der erste Schritt – wenn die Kamera einem Ziel wirklich „folgen“ soll, müssen Sie die Erkennung mit mechanischer Steuerung kombinieren.

Dieses Tutorial führt Sie durch die Entwicklung eines **YOLO-Objekterkennungs- und Verfolgungssystems**, das Folgendes erreicht:

* Echtzeiterkennung spezifischer Objekte mit YOLO
* Automatische Berechnung der Positionsabweichung des Ziels im Bild
* Servogesteuerte Schwenk-Neige-Einheit, um das Ziel in der Bildmitte zu halten
* Unterstützung zum Speichern aktueller Bilder mit der LEERTASTE für die Datensatzerstellung

Hier verfolgen wir das Ziel aus unserem benutzerdefinierten Modell, das wir im vorherigen Tutorial trainiert haben – bei mir ist es ein Schneemann. Sie können auch andere Modelle (wie yolov8n) wählen, um andere Ziele (wie Personen, Autos usw.) zu verfolgen.

.. image:: img/yolo_track.png

Abbildung: YOLO-Objekterkennungssystem in Aktion. Wenn sich das Ziel bewegt, folgt die Kamera-Schwenk-Neige-Einheit automatisch und hält das Ziel nahe dem gelben Fadenkreuz in der Bildmitte. Der grüne Begrenzungsrahmen markiert das erkannte Ziel.

**Anwendungsszenarien**:

* Intelligente Überwachung: Automatische Verfolgung verdächtiger Ziele
* Haustierbegleiter: Die Kamera folgt den Bewegungen Ihres Haustiers
* Videokonferenzen: Automatische Zentrierung sprechender Personen
* Datenerfassung: Automatische Aufnahme von Mehrwinkelbildern eines Ziels

Hardware-Aufbau
---------------------------------------

Für dieses Projekt müssen Sie die Schwenk-Neige-Einheit gemäß der Anleitung in :ref:`assemble_fusion_hat_pan_tilt` zusammenbauen.

.. image:: ../quick_start/img/gimbal_assemble.png

Ausführen des Codes
----------------------------------------

1. **Konfigurationsparameter anpassen**

   .. code-block:: bash

      cd ~/ai-lab-kit/yolo
      nano yolo_tracking.py

   Ändern Sie die Variable ``TARGET`` am Anfang des Codes auf das Objekt, das Sie verfolgen möchten:

   .. code-block:: python

      TARGET = "person"     # Eine Person verfolgen
      # oder
      TARGET = "snowman"    # Einen Schneemann verfolgen

2. **Die Modelldatei vorbereiten**

   * Verwenden Sie ein vortrainiertes Modell: ``model = YOLO("yolov8n.pt")``
   * Verwenden Sie ein benutzerdefiniertes Modell: ``model = YOLO("snowman.pt")``

3. **Speichern und Ausführen des Codes**

   .. code-block:: bash

      python3 yolo_tracking.py

4. **Bedienungsanleitung**

   * Nach dem Start arbeitet die Kamera automatisch
   * Wenn ein Ziel erkannt wird, drehen sich die Servos automatisch, um das Ziel in der Bildmitte zu halten
   * Drücken Sie die ``LEERTASTE``, um das aktuelle Bild zu speichern (zum Sammeln von Trainingsdaten)
   * Drücken Sie ``ESC``, um das Programm zu beenden

Code
-----------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-basierte Objektverfolgung für Raspberry Pi
   Verfolgt ein bestimmtes Objekt (z.B. Person) mit YOLO und steuert Servos
   Drücken Sie LEERTASTE, um Bilder für den Datensatz aufzunehmen, ESC zum Beenden
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Konfiguration --------------------
   TARGET = "your_object"      # Zu verfolgendes Objekt (Klassenname)
   W, H = 640, 480             # Kamerauflösung
   CX, CY = W // 2, H // 2     # Bildmittelpunkt
   CONFIDENCE = 0.3            # Konfidenzschwelle für Erkennung
   DEADZONE = 50               # Pixel um die Mitte, bevor Bewegung erfolgt
   SAVE_DIR = "captured_images"  # Verzeichnis zum Speichern von Datensätzen

   # Erstelle das Speicherverzeichnis
   os.makedirs(SAVE_DIR, exist_ok=True)

   print(f"=== YOLO-Verfolgungssystem ===")
   print(f"Ziel: {TARGET}")
   print(f"Konfidenzschwelle: {CONFIDENCE}")
   print(f"Totzone: {DEADZONE} Pixel")

   # -------------------- Servo-Initialisierung --------------------
   print("Initialisiere Servos...")
   pan = Servo(2)    # Kanal 2 für Schwenken (horizontal)
   tilt = Servo(3)   # Kanal 3 für Neigen (vertikal)
   pan.angle(0)      # Mittelposition
   tilt.angle(0)     # Mittelposition
   time.sleep(1)

   # -------------------- Laden des YOLO-Modells --------------------
   print("Lade YOLO-Modell...")
   # Verwenden Sie YOLOv8n für beste Leistung auf dem Raspberry Pi
   model = YOLO("your_model.pt")
   print("Modell erfolgreich geladen")

   # -------------------- Kamera-Initialisierung --------------------
   print("Initialisiere Kamera...")
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (W, H)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()
   time.sleep(2)

   print("\n=== System bereit ===")
   print("Bedienung:")
   print("  LEERTASTE - Bild aufnehmen (für Datensatz)")
   print("  ESC       - Beenden")
   print("  (Automatische Verfolgung bei Zielerkennung)")
   print("==========================\n")

   # -------------------- Verfolgungsvariablen --------------------
   pan_pos = 0    # Aktueller Schwenkwinkel (-90 bis 90)
   tilt_pos = 0   # Aktueller Neigungswinkel (-45 bis 45)
   capture_count = 0

   def simple_track(x, y):
      """
      Einfache 4-Richtungs-Verfolgung mit Totzone
      Gibt zurück: (pan_move, tilt_move) wobei:
         pan_move: -1 (links), 0 (stopp), 1 (rechts)
         tilt_move: -1 (runter), 0 (stopp), 1 (hoch)
      """
      if x is None or y is None:
         return 0, 0
      
      pan_move = 0
      tilt_move = 0
      
      # Horizontale Bewegung (Schwenken)
      if x < CX - DEADZONE:
         pan_move = 1           # Nach rechts bewegen
      elif x > CX + DEADZONE:
         pan_move = -1          # Nach links bewegen
      
      # Vertikale Bewegung (Neigen)
      if y < CY - DEADZONE:
         tilt_move = -1         # Nach unten bewegen
      elif y > CY + DEADZONE:
         tilt_move = 1          # Nach oben bewegen
      
      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Durchsucht die YOLO-Erkennungsergebnisse nach dem Zielobjekt
      Gibt zurück: (x_center, y_center, confidence) oder (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None
      
      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])
         
         # Groß-/Kleinschreibung-unabhängige Teilübereinstimmung
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence
      
      return None, None, None

   # -------------------- Hauptverfolgungsschleife --------------------
   try:
      while True:
         # Einzelbild erfassen
         frame = picam2.capture_array()
         
         # YOLO-Erkennung ausführen
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)
         
         # Zielobjekt finden
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)
         
         # Verfolgung verarbeiten, wenn Objekt gefunden
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move
               
               # Servowinkel auf sichere Bereiche begrenzen
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))
               
               # Befehle an die Servos senden
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)
               
               # Erkennungsrahmen zeichnen
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30), 
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)
               
               status = f"{TARGET} erkannt: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"Kein {TARGET} erkannt"
               color = (0, 0, 255)
         
         # Fadenkreuz in der Mitte zeichnen
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         
         # Totzone-Rechteck zeichnen (visuelle Referenz)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)
         
         # Statusinformationen anzeigen
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Schwenk: {pan_pos:.0f} Neigung: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Aufgenommene Bilder: {capture_count}", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "LEERTASTE=aufnehmen  ESC=beenden", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         # Videofenster anzeigen
         cv2.imshow(f"YOLO-Verfolgung - {TARGET}", frame)
         
         # Tastendrücke verarbeiten
         key = cv2.waitKey(1) & 0xFF
         
         if key == 32:  # LEERTASTE - Bild aufnehmen
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Aufgenommen: {filename}")
               capture_count += 1
               
               # Blitzeffekt
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO-Verfolgung - {TARGET}", flash)
               cv2.waitKey(50)
               
         elif key == 27:  # ESC-Taste - Beenden
               print(f"\nBeende. Insgesamt aufgenommen: {capture_count} Bilder")
               break

   finally:
      # -------------------- Aufräumen --------------------
      print("Räume auf...")
      pan.angle(0)      # Zurück zur Mitte
      tilt.angle(0)     # Zurück zur Mitte
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Verfolgung gestoppt. Servos zentriert.")

Code-Erklärung
------------------------------

Hier ist der vollständige YOLO-Objekterkennungscode. Wir analysieren seine Funktionsweise Abschnitt für Abschnitt.

**1. Bibliotheken importieren und Konfigurationsparameter**

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-basierte Objektverfolgung für Raspberry Pi
   Verfolgt ein bestimmtes Objekt (z.B. Person) mit YOLO und steuert Servos
   Drücken Sie LEERTASTE, um Bilder für den Datensatz aufzunehmen, ESC zum Beenden
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Konfiguration --------------------
   TARGET = "your_object"      # Zu verfolgendes Objekt (Klassenname)
   W, H = 640, 480             # Kamerauflösung
   CX, CY = W // 2, H // 2     # Bildmittelpunkt
   CONFIDENCE = 0.3            # Konfidenzschwelle für Erkennung
   DEADZONE = 50               # Pixel um die Mitte, bevor Bewegung erfolgt
   SAVE_DIR = "captured_images"  # Verzeichnis zum Speichern von Datensätzen

   # Erstelle das Speicherverzeichnis
   os.makedirs(SAVE_DIR, exist_ok=True)

Konfigurationsparameter:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Parameter
     - Beschreibung
     - Empfohlener Wert
   * - ``TARGET``
     - Name des zu verfolgenden Objekts
     - "person", "snowman", "cup"
   * - ``W, H``
     - Kamerauflösung
     - 640x480 (ausgewogene Leistung)
   * - ``DEADZONE``
     - Totzonenbereich (Pixel)
     - 50-100, verhindert häufiges Zittern
   * - ``CONFIDENCE``
     - Konfidenzschwelle für Erkennung
     - 0.3-0.5
   * - ``SAVE_DIR``
     - Bildspeicherverzeichnis
     - captured_images

**2. Servos initialisieren**

.. code-block:: python

   # -------------------- Servo-Initialisierung --------------------
   print("Initialisiere Servos...")
   pan = Servo(2)    # Kanal 2 für Schwenken (horizontal)
   tilt = Servo(3)   # Kanal 3 für Neigen (vertikal)
   pan.angle(0)      # Mittelposition
   tilt.angle(0)     # Mittelposition
   time.sleep(1)

Servo-Winkelbereiche:

* Schwenkservo (horizontal): -90° bis 90°, 0° ist die Mitte
* Neigungsservo (vertikal): -45° bis 45°, 0° ist die Mitte

**3. YOLO-Modell laden**

.. code-block:: python

   # -------------------- Laden des YOLO-Modells --------------------
   print("Lade YOLO-Modell...")
   # Verwenden Sie YOLOv8n für beste Leistung auf dem Raspberry Pi
   model = YOLO("your_model.pt")
   print("Modell erfolgreich geladen")

Modellauswahl-Empfehlungen:

* Verwenden Sie Ihr eigenes trainiertes Modell: ``"snowman.pt"``, ``"my_pet.pt"``
* Verwenden Sie ein vortrainiertes Modell: ``"yolov8n.pt"`` (erkennt 80 gängige Objekte)

**4. Objekterkennungs- und Verfolgungslogik**

.. code-block:: python

   def simple_track(x, y):
      """
      Einfache 4-Richtungs-Verfolgung mit Totzone
      Gibt zurück: (pan_move, tilt_move) wobei:
         pan_move: -1 (links), 0 (stopp), 1 (rechts)
         tilt_move: -1 (runter), 0 (stopp), 1 (hoch)
      """
      if x is None or y is None:
         return 0, 0
      
      pan_move = 0
      tilt_move = 0
      
      # Horizontale Bewegung (Schwenken)
      if x < CX - DEADZONE:
         pan_move = 1           # Nach rechts bewegen
      elif x > CX + DEADZONE:
         pan_move = -1          # Nach links bewegen
      
      # Vertikale Bewegung (Neigen)
      if y < CY - DEADZONE:
         tilt_move = -1         # Nach unten bewegen
      elif y > CY + DEADZONE:
         tilt_move = 1          # Nach oben bewegen
      
      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Durchsucht die YOLO-Erkennungsergebnisse nach dem Zielobjekt
      Gibt zurück: (x_center, y_center, confidence) oder (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None
      
      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])
         
         # Groß-/Kleinschreibung-unabhängige Teilübereinstimmung
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence
      
      return None, None, None

Erklärung der Verfolgungslogik:

* **Totzonen-Mechanismus**: Wenn sich das Ziel innerhalb der Totzone nahe der Bildmitte befindet, bewegen sich die Servos nicht, um häufiges Zittern zu verhindern
* **Richtungsbestimmung**: Wenn das Ziel links von der Mitte ist, nach rechts drehen; wenn rechts von der Mitte, nach links drehen
* **Zielidentifikation**: Finden des zu verfolgenden Objekts durch Abgleich der Klassennamen

**5. Hauptschleife**

.. code-block:: python

   # -------------------- Hauptverfolgungsschleife --------------------
   try:
      while True:
         # Einzelbild erfassen
         frame = picam2.capture_array()
         
         # YOLO-Erkennung ausführen
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)
         
         # Zielobjekt finden
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)
         
         # Verfolgung verarbeiten, wenn Objekt gefunden
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move
               
               # Servowinkel auf sichere Bereiche begrenzen
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))
               
               # Befehle an die Servos senden
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)
               
               # Erkennungsrahmen zeichnen
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30), 
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)
               
               status = f"{TARGET} erkannt: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"Kein {TARGET} erkannt"
               color = (0, 0, 255)
         
         # Fadenkreuz in der Mitte zeichnen
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         
         # Totzone-Rechteck zeichnen (visuelle Referenz)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)
         
         # Statusinformationen anzeigen
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Schwenk: {pan_pos:.0f} Neigung: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Aufgenommene Bilder: {capture_count}", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "LEERTASTE=aufnehmen  ESC=beenden", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         # Videofenster anzeigen
         cv2.imshow(f"YOLO-Verfolgung - {TARGET}", frame)
         
         # Tastendrücke verarbeiten
         key = cv2.waitKey(1) & 0xFF
         
         if key == 32:  # LEERTASTE - Bild aufnehmen
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Aufgenommen: {filename}")
               capture_count += 1
               
               # Blitzeffekt
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO-Verfolgung - {TARGET}", flash)
               cv2.waitKey(50)
               
         elif key == 27:  # ESC-Taste - Beenden
               print(f"\nBeende. Insgesamt aufgenommen: {capture_count} Bilder")
               break

   finally:
      # -------------------- Aufräumen --------------------
      print("Räume auf...")
      pan.angle(0)      # Zurück zur Mitte
      tilt.angle(0)     # Zurück zur Mitte
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Verfolgung gestoppt. Servos zentriert.")

Leistungsoptimierung
-----------------------------------------

Beim Ausführen des Verfolgungssystems auf dem Raspberry Pi können folgende Optimierungen helfen:

1. **Erkennungshäufigkeit reduzieren**: Alle 2-3 Bilder erkennen, Erkennungsergebnisse für die anderen Bilder wiederverwenden

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       if frame_count % 3 == 0:
           results = model.predict(frame, imgsz=320)
       frame_count += 1

2. **Erkennungsbereich eingrenzen**: Nur in Bereichen erkennen, in denen das Ziel wahrscheinlich erscheint

3. **Kleinere Modelle verwenden**: ``yolov8n.pt`` ist die beste Wahl

4. **Totzonenbereich anpassen**: Eine Vergrößerung von ``DEADZONE`` reduziert häufige Servobewegungen

Häufige Fragen
---------------------------------

**F: Was tun, wenn sich die Servos nicht bewegen?**

* Überprüfen Sie, ob die Servos richtig angeschlossen sind
* Stellen Sie sicher, dass die fusion_hat-Bibliothek korrekt installiert ist

**F: Was tun, wenn die Verfolgungsreaktion zu langsam ist?**

* Kamerauflösung verringern (z. B. 320x240)
* Erkennungsauflösung ``imgsz`` reduzieren
* Totzonenbereich vergrößern, um Servobewegungen zu reduzieren

**F: Was tun, wenn die Zielerkennung instabil ist?**

* Passen Sie die ``CONFIDENCE``-Schwelle an (niedrigere Werte erkennen mehr, erhöhen aber falsch-positive Ergebnisse)
* Sorgen Sie für ausreichende Beleuchtung
* Verwenden Sie ein benutzerdefiniertes Modell für bessere Spezifität

**F: Wie kann die Servoempfindlichkeit angepasst werden?**

Ändern Sie den Schrittweitenwert in der ``simple_track``-Funktion:

.. code-block:: python

   # Schrittweite für schnellere Servobewegung erhöhen
   pan_move = 2  # Ursprünglich 1
   tilt_move = 2

**F: Kann ich mehrere Ziele verfolgen?**

Ändern Sie die ``find_target_detection``-Funktion so, dass sie das nächste oder das Ziel mit der höchsten Konfidenz zurückgibt, oder implementieren Sie eine Umschaltfunktionalität für mehrere Ziele.

Erweiterte Funktionen
-----------------------------------

**1. PID-Regelung hinzufügen** (weichere Verfolgung)

.. code-block:: python

   # Vereinfachtes PID-Reglerbeispiel
   pan_error = CX - obj_x
   pan_output = pan_error * 0.05  # Proportionalregelung
   pan_pos += int(pan_output)

**2. Automatische Aufzeichnung der Verfolgungsbahn**

.. code-block:: python

   # Zielpositionsverlauf aufzeichnen
   trajectory = []
   trajectory.append((obj_x, obj_y))

**3. Benachrichtigung bei Zielerkennung senden**

.. code-block:: python

   if obj_x is not None:
       # E-Mail oder Push-Benachrichtigung senden
       pass

**4. Gesichtserkennung integrieren**

Kombinieren Sie mit Gesichtserkennungsbibliotheken, um nur bestimmte Personen zu verfolgen.

Zusammenfassung
---------------------

Durch dieses Tutorial haben Sie gelernt:

* Wie Sie YOLO-Objekterkennung mit Servosteuerung kombinieren
* Wie Sie ein visionäres automatisches Verfolgungssystem implementieren
* Wie Sie Totzonenmechanismen zur Vermeidung von Zittern einsetzen
* Wie Sie während der Verfolgung Trainingsdaten sammeln

Dieses System kann in Szenarien wie intelligenter Überwachung, automatisierter Fotografie und robotischer Vision weit verbreitet eingesetzt werden. Da sich YOLO-Modelle weiterentwickeln, können Sie noch intelligentere Verfolgungssysteme aufbauen – wie z. B. automatische Zoomanpassung basierend auf der Zielgröße oder Vorhersage von Zielbewegungen basierend auf Bewegungstrajektorien.