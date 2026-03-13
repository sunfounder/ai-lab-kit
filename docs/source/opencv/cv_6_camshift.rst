.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. CAMShift-Objektverfolgung
==============================

Im vorherigen Kapitel haben wir den MeanShift-Algorithmus kennengelernt, der ein Zielobjekt in einem Video anhand seines Farbhistogramms kontinuierlich verfolgen kann.  
In diesem Abschnitt stellen wir **CAMShift (Continuously Adaptive Mean Shift)** vor.  
Dieser erweitert MeanShift, indem er **Fenstergröße und Orientierung automatisch anpasst**, wodurch er für reale Anwendungen deutlich praktischer wird.  
Zusätzlich verfolgen wir in diesem Beispiel ein Ziel **auf Basis der Helligkeit statt der Farbe**, was in der Praxis ebenfalls sehr häufig vorkommt.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. Algorithmusmerkmale
----------------------------------

**MeanShift** kann nur die Position eines Zielobjekts verfolgen und verwendet ein Fenster mit fester Größe.  
**CAMShift** verfolgt die Position **und** passt Fenstergröße und Winkel automatisch an.

Beispielsweise wächst das Tracking-Fenster, wenn sich das Zielobjekt der Kamera nähert; es verkleinert sich, wenn sich das Objekt entfernt; und wenn sich das Objekt dreht, rotiert auch das Tracking-Fenster entsprechend.

.. image:: img/opencv_camshift.png
   :alt: Illustration der CAMShift-Verfolgung
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
      python3 cv_6_camshift.py

#. Wenn Sie das Programm ausführen, erscheint ein OpenCV-Fenster mit dem Namen **CAMShift Tracker** und beginnt mit der Wiedergabe der Videodatei *sample3.mp4*.  

   Das Programm verfolgt die schwarze Katze mithilfe des CAMShift-Algorithmus (Continuously Adaptive Mean Shift).

   Ein grünes, rotiertes Begrenzungsrechteck wird um das verfolgte Objekt gezeichnet.  
   Während sich die Katze bewegt oder ihre Größe und Orientierung ändert, passt das Tracking-Fenster automatisch seine Position, Größe und seinen Winkel an.

   Sie können das Programm auf zwei Arten beenden:

   * Drücken Sie die **q**-Taste auf der Tastatur  
   * Schließen Sie das Fenster über die Schaltfläche zum Schließen (X)  

   Nach dem Beenden stoppt die Videowiedergabe und alle OpenCV-Fenster werden geschlossen.

3. Vollständiger Code
---------------------

Öffnen Sie ``cv_6_camshift.py``, um den vollständigen Code anzusehen.

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Code-Erklärung
---------------------------

#. Videodatei öffnen und das erste Frame lesen:

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift benötigt ein initiales Frame, um zu lernen, welches Objekt verfolgt werden soll.

#. Das anfängliche Tracking-Fenster (ROI) festlegen:

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   Dieses Rechteck sollte das Zielobjekt im ersten Frame vollständig abdecken.  
   Während des Trackings wird dieses Fenster von CAMShift automatisch aktualisiert.

#. Das erste Frame in HSV umwandeln und die ROI extrahieren:

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV ist für Tracking praktisch, da bestimmte Kanäle (zum Beispiel V für Helligkeit) gezielt verwendet werden können.

#. Eine Maske für ein dunkles Objekt erstellen (niedrige V-Werte):

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   Dadurch bleiben nur „dunkle“ Pixel innerhalb der ROI erhalten.  
   Für schwarze oder dunkle Objekte ist die Helligkeit (V) häufig das wichtigste Merkmal.

#. Ein Histogramm des V-Kanals berechnen und normalisieren:

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - Kanal ``2`` entspricht dem **V-Kanal (Value/Helligkeit)** im HSV-Farbraum.
   - Das Histogramm beschreibt, wie „dunkel oder hell“ die Ziel-ROI ist.
   - Die Normalisierung verbessert die Stabilität des Trackings.

#. Abbruchkriterien für CAMShift festlegen:

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift beendet die Aktualisierung, wenn entweder 10 Iterationen erreicht sind oder die Bewegung kleiner als 1 Pixel ist.

#. Wiedergabegeschwindigkeit anhand der FPS festlegen:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Dadurch wird eine Verzögerung gesetzt, sodass das Video ungefähr mit seiner ursprünglichen Bildrate abgespielt wird.

#. Eine Wahrscheinlichkeitskarte mittels Back Projection erstellen (V-Kanal):

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   Die Back Projection hebt Pixel im Frame hervor, deren V-Werte dem Histogramm der ROI entsprechen.  
   Höhere Werte in ``back_proj`` bedeuten eine größere Wahrscheinlichkeit, dass es sich um das Zielobjekt handelt.

#. Tracking mit CAMShift durchführen und das Fenster aktualisieren:

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift basiert auf MeanShift, kann jedoch zusätzlich **Größe und Rotation** des Tracking-Fensters anpassen.

   - ``track_window`` wird in jedem Frame aktualisiert.
   - ``rot_rect`` enthält ein rotiertes Rechteck (Zentrum, Größe, Winkel).

#. Das rotierte Tracking-Rechteck zeichnen:

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   Dadurch wird das rotierte Rechteck in vier Eckpunkte umgewandelt und im Frame eingezeichnet.

#. Abbruchbedingungen (Tastatur + Fensterschließen):

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   Drücken Sie ``q``, um das Programm zu beenden, oder schließen Sie das Fenster für einen sicheren Abbruch.

#. Ressourcen freigeben:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Geben Sie am Ende immer die Videodatei frei und schließen Sie alle Fenster.

5. CAMShift vs. MeanShift
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Merkmal
     - MeanShift
     - CAMShift
   * - Fenstergröße
     - Fest
     - Adaptiv
   * - Winkel
     - Nicht unterstützt
     - Unterstützt Rotation
   * - Tracking-Genauigkeit
     - Mittel
     - Höher, anpassungsfähiger
   * - Anwendungen
     - Statische Zielobjekte
     - Komplexe Bewegungen, rotierende Zielobjekte

CAMShift ist eine Weiterentwicklung von MeanShift  
und kann Zielverformungen, Rotation und Distanzänderungen besser handhaben – daher eignet es sich gut für reale Anwendungsszenarien.

6. Erweiterungen und Übungen
-------------------------------------------

- Passen Sie die ``inRange``-Schwellenwerte an, um grüne oder blaue Zielobjekte zu verfolgen  
- Kombinieren Sie das Programm mit einer Live-Kameraquelle, um ein Echtzeit-Tracking-System auf Farbbasis zu erstellen


7. Erweitert: Interaktive ROI-Auswahl und automatische HSV-Schwellenwerte
-------------------------------------------------------------------------

Wie im vorherigen Abschnitt kann dieses Projekt ebenfalls die Mausinteraktion verwenden, um die ROI auszuwählen und die HSV-Schwellenwerte automatisch anzupassen.

Führen Sie ``cv_6_camshift_auto.py`` aus, um den angepassten Code zu verwenden.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

Wenn Sie das Programm ausführen, wird das erste Frame des Videos angezeigt, und Sie werden aufgefordert, mit der Maus eine Region of Interest (ROI) auszuwählen.

Ziehen Sie mit der Maus ein Rechteck um das Zielobjekt und drücken Sie anschließend **Enter** oder **Leertaste**, um die Auswahl zu bestätigen.  
Drücken Sie **Esc**, um die Auswahl abzubrechen.

Nach der Auswahl der ROI erscheint ein Fenster mit dem Namen **CAMShift Tracker**.  
Das ausgewählte Objekt wird mit einem grünen, rotierten Rechteck verfolgt, und das Tracking-Fenster passt seine Position, Größe und Orientierung automatisch an, während sich das Objekt bewegt.

So beenden Sie das Programm:

* Drücken Sie die **q**-Taste auf der Tastatur  
* Oder schließen Sie das Anzeigefenster über die Schaltfläche zum Schließen (X)  

Nach dem Beenden stoppt die Videowiedergabe und alle OpenCV-Fenster werden geschlossen.

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

   ...

