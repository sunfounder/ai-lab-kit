.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: 
   
   Wenn Sie das vorinstallierte Image „Raspberry Pi OS mit AI Fusion Lab Kit“ verwenden, können Sie diesen Abschnitt überspringen. Dieses Image enthält bereits alle in diesem Kapitel beschriebenen Softwareinstallationen, Umgebungskonfigurationen und Beispielcode-Bereitstellungen.

.. _mediapipe_install:

0. MediaPipe einrichten
====================================================================

Informationen zur Betriebssystemversion
-------------------------------------------------

.. warning::

   **Empfohlenes Betriebssystem**: Raspberry Pi OS Bookworm (Debian 12, 64-bit)

   Raspberry Pi OS Trixie (Debian 13) wird derzeit nicht empfohlen, weil:

   * MediaPipe Python 3.13 noch nicht unterstützt.
   * Picamera2 nur mit der System-Python-Version funktioniert.

Dieses Tutorial wird aktualisiert, sobald Trixie offiziell unterstützt wird.

Wenn Sie eine offizielle MediaPipe-Unterstützung für Python 3.13 anfragen möchten, können Sie hier Feedback einreichen:

* GitHub Issue: https://github.com/google-ai-edge/mediapipe/issues/5708
* Support Page: https://ai.google.dev/edge/mediapipe/support



Bevor Sie beginnen
---------------------------------

.. important::


   Stellen Sie vor dem Start sicher, dass:

   * das Pan-Tilt-Modul montiert ist
   * Sie Zugriff auf den Raspberry Pi Desktop haben
   * das Codepaket installiert ist
   * das Fusion HAT+ installiert und konfiguriert ist
   * OpenCV installiert ist

   Detaillierte Anweisungen finden Sie unter :ref:`opencv_install`.

Diese Vorbereitungen stellen sicher, dass MediaPipe auf Ihrem Raspberry Pi mit vollständiger Grafik- und Kamerafunktionalität ausgeführt werden kann.


Installationsschritte
----------------------------------

#. MediaPipe installieren

   Installieren Sie MediaPipe mit pip. Unter Raspberry Pi OS Bookworm (Debian 12, 64-bit)
   lädt pip automatisch das passende Wheel herunter.

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. Installation überprüfen

   Führen Sie den folgenden Befehl aus, um zu bestätigen, dass MediaPipe korrekt installiert wurde.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Erwartete Ausgabe:

   .. code-block:: text

      MediaPipe version: 0.10.18


Häufige Probleme und Lösungen
-------------------------------------------

#. MediaPipe-Installation schlägt fehl

   Dies passiert in der Regel, wenn eine nicht unterstützte Betriebssystemversion verwendet wird.

   Lösung:

   * MediaPipe funktioniert derzeit nur unter Raspberry Pi OS Bookworm (Debian 12, 64-bit).
   * Raspberry Pi OS Trixie (Debian 13, Python 3.13) wird nicht unterstützt.

#. Kamera kann in MediaPipe oder OpenCV nicht geöffnet werden

   Dies passiert in der Regel, wenn die Raspberry-Pi-Kameraschnittstelle nicht aktiviert ist.

   Lösung:

   * Aktivieren Sie die Kamera in ``raspi-config``:
     Interface Options → Camera → Enable

#. OpenCV-Importfehler

   Einige über pip installierte OpenCV-Versionen können mit den Bibliotheken von Raspberry Pi OS inkompatibel sein.

   Lösung:

   .. code-block:: bash

      sudo apt install python3-opencv

#. MediaPipe kann nach der Installation nicht importiert werden

   Dies kann auftreten, wenn pip, setuptools oder wheel veraltet sind.

   Lösung:

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


MediaPipe ist jetzt einsatzbereit.  
Sie können im nächsten Abschnitt mit der Echtzeit-Gesichtserkennung mithilfe der Raspberry-Pi-Kamera fortfahren.