.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: Wenn Sie das vorinstallierte Image „Raspberry Pi OS mit AI Fusion Lab Kit“ verwenden, können Sie diesen Abschnitt überspringen. Dieses Image enthält bereits alle in diesem Kapitel beschriebenen Softwareinstallationen, Umgebungskonfigurationen und Beispielcode-Bereitstellungen.

0. YOLO-Umgebung einrichten
==============================

Dieses Kapitel zeigt Ihnen, wie Sie YOLO auf dem Raspberry Pi installieren und überprüfen, ob es korrekt funktioniert.

#. Um das Kameramodul bequem nutzen zu können, wird der Zusammenbau der :ref:`assemble_fusion_hat_pan_tilt` empfohlen.

   .. note:: 
     
      Der Zusammenbau der Schwenk-Neige-Einheit kann einige Pins verdecken. Daher wird empfohlen, sie erst bei Verwendung der Kamera zusammenzubauen oder sie nach dem Zusammenbau außen zu platzieren.
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Zugriff auf den Raspberry Pi Desktop:

   * :ref:`remote_desktop`: Verwenden Sie **VNC** für eine vollständige Desktop-Umgebung.
   * |link_rpi_connect|: Verwenden Sie **Raspberry Pi Connect**, um sicher von einem beliebigen Browser auf Ihren Pi zuzugreifen.

3. Installieren Sie die erforderlichen Abhängigkeiten:

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Installieren Sie Ultralytics (die offizielle YOLO-Bibliothek):

   .. code-block:: bash

      # CPU-Version von PyTorch installieren (CPU-Quelle angeben)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Ultralytics installieren, aber torch-Abhängigkeiten überspringen
      pip3 install ultralytics --no-deps --break-system-packages

      # Andere Abhängigkeiten von Ultralytics manuell installieren
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages