.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. MeanShift-Objektverfolgung
===============================

MeanShift ist ein klassischer histogrammbasierter Algorithmus zur Objektverfolgung.  
In dieser Lektion implementieren wir nicht nur ein vollständiges Beispiel für **MeanShift-Tracking**, sondern erklären auch, **warum** jeder Schritt durchgeführt wird und **was intern dabei passiert**.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. Was ist MeanShift?
-------------------------

MeanShift verschiebt ein Fenster iterativ anhand der Wahrscheinlichkeitsdichte, um **die wahrscheinlichste Position des Zielobjekts** zu finden.

Einfach ausgedrückt:  
Zuerst geben Sie dem Algorithmus einen „anfänglichen Zielbereich“. Er berechnet daraus die Farbmerkmale dieses Bereichs (zum Beispiel das Farbhistogramm des Zielobjekts) und sucht dann in jedem folgenden Frame den Bereich, der dieser Farbe am ähnlichsten ist, und verschiebt das Rechteck dorthin.

Dieser Prozess basiert nicht auf Deep Learning und benötigt kein Vortraining – er ist daher sehr leichtgewichtig.

.. image:: img/opencv_meanshift.png
   :alt: MeanShift-Verfolgung
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
      python3 cv_5_meanshift.py

#. Wenn Sie das Programm ausführen, erscheint ein OpenCV-Fenster mit dem Namen **MeanShift Tracker** und beginnt mit der Wiedergabe der Videodatei ``sample2.mp4``.  

   Ein grünes Rechteck wird um das Zielobjekt gezeichnet und mithilfe des MeanShift-Tracking-Algorithmus in Echtzeit aktualisiert.
   
   Das Tracking-Fenster bewegt sich mit, wenn sich das Objekt im Video bewegt.
   
   Sie können das Programm auf zwei Arten beenden:
   
   * Drücken Sie die **q**-Taste auf der Tastatur  
   * Schließen Sie das Fenster über die Schaltfläche zum Schließen (X)  
   
   Nach dem Beenden stoppt die Videowiedergabe und alle OpenCV-Fenster werden geschlossen.

3. Vollständiger Code
-----------------------

Unten finden Sie das vollständige MeanShift-Tracking-Skript (``cv_5_meanshift.py``):

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Erklärung
---------------------------

#. Die Videodatei öffnen:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Dadurch wird ein VideoCapture-Objekt erstellt, damit OpenCV Frames aus der Datei lesen kann.

#. Das erste Frame lesen und sicherstellen, dass es funktioniert:

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   MeanShift-Tracking benötigt ein initiales Frame, um zu lernen, was verfolgt werden soll.

#. Das anfängliche Tracking-Fenster festlegen (das Objekt, das verfolgt werden soll):

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   Dieses Rechteck ist die Startposition des Zielobjekts (ROI).  
   In der Regel passen Sie diese Werte so an, dass sie dem Objekt im ersten Frame entsprechen.

#. Das erste Frame in HSV umwandeln und die ROI extrahieren:

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV wird häufig für Tracking verwendet, weil der Hue-Kanal die Farbe konsistenter beschreibt als RGB/BGR.

#. Eine Maske erstellen, um schwache oder ungültige Pixel in der ROI zu ignorieren:

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   Dadurch werden Pixel mit sehr niedriger Sättigung oder Helligkeit herausgefiltert (oft Schatten oder Rauschen), was die Tracking-Stabilität verbessert.

#. Das ROI-Histogramm berechnen und normalisieren (Hue-Kanal):

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - Das Histogramm beschreibt die Farbverteilung des Zielobjekts (Hue).
   - Die Normalisierung sorgt dafür, dass die Histogrammskala bei unterschiedlichen Lichtverhältnissen oder ROI-Größen konsistent bleibt.

#. Abbruchkriterien für MeanShift definieren:

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift stoppt, wenn entweder:
   - 15 Iterationen erreicht sind, oder
   - die Fensterbewegung kleiner als 2 Pixel ist.

#. Eine Wiedergabeverzögerung basierend auf der Video-FPS festlegen:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Dadurch bleibt die Wiedergabe nahe an der ursprünglichen Videogeschwindigkeit.  
   Wenn die FPS nicht gelesen werden können, wird auf 30 FPS zurückgegriffen.

#. Jedes Frame in HSV umwandeln (für das Tracking):

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   Das Tracking wird in HSV durchgeführt, damit das Hue-Histogramm des Zielobjekts abgeglichen werden kann.

#. Back Projection anwenden (finden, wo die Zielfarbe wahrscheinlich ist):

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   Die Back Projection erzeugt eine Wahrscheinlichkeitskarte: helle Bereiche entsprechen mit höherer Wahrscheinlichkeit dem ROI-Histogramm.

#. Das Tracking-Fenster mit MeanShift aktualisieren:

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift verschiebt das Tracking-Fenster in Richtung des Bereichs mit der höchsten Dichte in der Wahrscheinlichkeitskarte und aktualisiert so die Zielposition Frame für Frame.

#. Das Tracking-Ergebnis zeichnen:

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   Dadurch wird das aktuelle Tracking-Rechteck auf das Videobild gezeichnet.

#. Das Fenster anzeigen und Abbruchbedingungen prüfen:

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - Drücken Sie ``q``, um das Programm zu beenden.
   - Das Schließen des Fensters beendet das Programm ebenfalls sicher.

#. Ressourcen freigeben:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Geben Sie das Video immer frei und schließen Sie die Fenster, um Systemressourcen freizugeben.

5. MeanShift vs. CAMShift
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Merkmal
     - MeanShift
     - CAMShift
   * - Fenstergröße
     - Fest
     - Passt sich automatisch an (an die Zielgröße)
   * - Rotierendes Zielobjekt
     - Nicht unterstützt
     - Unterstützt
   * - Geeignete Szenarien
     - Zielgröße relativ stabil
     - Ziel kann skaliert oder gedreht werden
   * - Anwendungen
     - Einfaches Tracking, Bälle, Marker
     - Praktisches Tracking, Überwachung, Erkennung


6. Erweitert: ROI mit der Maus auswählen
----------------------------------------------------

Bisher haben wir feste Werte verwendet:

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

Das ist einfach, aber nicht flexibel.  
Wenn Sie das Video wechseln oder das Zielobjekt an einer anderen Stelle startet, müssten Sie den Code anpassen.

OpenCV bietet ``cv2.selectROI``, sodass Sie **die Zielregion im ersten Frame interaktiv mit der Maus auswählen** können und das Programm ``(x, y, w, h)`` dann automatisch erhält.

**Geänderter Initialisierungscode**

Führen Sie ``cv_5_meanshift_auto.py`` aus, um den angepassten Code zu verwenden.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

Wenn Sie das Programm ausführen, wird das erste Frame des Videos angezeigt, und Sie werden aufgefordert, mit der Maus eine Region of Interest (ROI) auszuwählen.

Ziehen Sie mit der Maus ein Rechteck um das Zielobjekt und drücken Sie dann **Enter** oder **Leertaste**, um die Auswahl zu bestätigen.  
Drücken Sie **Esc**, um die Auswahl abzubrechen.

Nach dem Bestätigen der ROI erscheint ein Fenster mit dem Namen **MeanShift Tracker**.  
Das ausgewählte Objekt wird mit einem grünen Begrenzungsrahmen verfolgt, und der Rahmen bewegt sich mit dem Objekt im Video mit.

So beenden Sie das Programm:

* Drücken Sie die **q**-Taste auf der Tastatur  
* Oder schließen Sie das Anzeigefenster über die Schaltfläche zum Schließen (X)  

Nach dem Beenden stoppt die Videowiedergabe und alle OpenCV-Fenster werden geschlossen.

.. image:: img/opencv_meanshift_mouse.png
   :alt: Fenster zur interaktiven ROI-Auswahl
   :align: center

**Hinweise**

``cv2.selectROI`` ist der integrierte interaktive ROI-Selektor von OpenCV und eignet sich hervorragend für die manuelle Initialisierung.  
Er gibt ``(x, y, w, h)`` zurück, was vollständig mit ``track_window`` kompatibel ist, sodass Sie die Hauptlogik von CAMShift/MeanShift nicht ändern müssen.  
Dadurch können Sie dasselbe Programm für verschiedene Videos und Zielobjekte wiederverwenden.


7. Erweitert II: HSV-Schwellenwerte für die ROI dynamisch berechnen
--------------------------------------------------------------------------------

Das ursprüngliche ``cv_5_meanshift.py`` verwendet manuell festgelegte HSV-Schwellenwerte, was geeignet ist, wenn die Zielfarbe fest ist und die Beleuchtung stabil bleibt.


.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

Wenn sich die Beleuchtung stark verändert oder die Zielfarbe nicht fest definiert ist, sind fest codierte ``inRange``-Grenzen möglicherweise nicht optimal.  
Ein intelligenterer Ansatz besteht darin, die unteren und oberen HSV-Grenzen **automatisch aus der ausgewählten ROI zu berechnen**.

**Beispiel: HSV-Schwellenwerte automatisch berechnen**

Führen Sie ``cv_5_meanshift_auto.py`` aus, um den angepassten Code zu verwenden.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)


Bei der Auswahl sehr dunkler oder sehr heller Zielobjekte müssen Sie die Schwellenwerte nicht mehr manuell anpassen; das Verfahren passt sich auch schnell an unterschiedliche Lichtverhältnisse und Farben an.

.. note::

   - ``np.percentile`` (5 %–95 %) entfernt extreme Werte (Ränder, Schatten, Glanzlichter usw.) innerhalb der ROI und verbessert dadurch die Robustheit.  
   - ``pad_h``, ``pad_s``, ``pad_v`` bieten eine Toleranz, sodass leichte Farbverschiebungen weiterhin erfasst werden.  
   - ``lower`` und ``upper`` sind die dynamischen HSV-Grenzen, die direkt mit ``cv2.inRange`` verwendet werden.


**Zusammenfassung**

- Verwenden Sie ``cv2.selectROI`` für eine flexible Initialisierung des Zielobjekts.  
- Verwenden Sie ``np.percentile``, um HSV-Grenzen automatisch zu berechnen und die Anpassungsfähigkeit zu verbessern.  
- In Kombination mit ``cv2.inRange`` und CAMShift/MeanShift bleibt dieser Ansatz auch bei schwierigen Lichtverhältnissen und unterschiedlichen Zielobjekten stabil.
