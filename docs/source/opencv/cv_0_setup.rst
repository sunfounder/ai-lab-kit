.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: 
   
   Wenn Sie das vorinstallierte Image „Raspberry Pi OS mit AI Fusion Lab Kit“ verwenden, können Sie diesen Abschnitt überspringen. Dieses Image enthält bereits alle in diesem Kapitel beschriebenen Softwareinstallationen, Umgebungskonfigurationen und Beispielcode-Bereitstellungen.


.. _opencv_install:

0. OpenCV einrichten
=========================================================================

In diesem Kapitel wird gezeigt, wie Sie OpenCV auf dem Raspberry Pi installieren und überprüfen, ob es korrekt funktioniert.

#. Um das Kameramodul komfortabel zu verwenden, wird :ref:`assemble_fusion_hat_pan_tilt` empfohlen.

   .. note:: 
     
      Beim Zusammenbau des Pan-Tilt-Moduls können einige Pins verdeckt werden. Daher wird empfohlen, es nur bei Verwendung der Kamera zu montieren oder es nach dem Zusammenbau außen zu platzieren.
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Greifen Sie auf den Raspberry-Pi-Desktop zu:

   * :ref:`remote_desktop`: Verwenden Sie **VNC** für eine vollständige Desktop-Umgebung.
   * |link_rpi_connect|: Verwenden Sie **Raspberry Pi Connect**, um sicher von jedem Browser aus auf Ihren Pi zuzugreifen.


#. Führen Sie die Einrichtung in :ref:`install_all_modules` vollständig durch (laden Sie das bereitgestellte Codepaket herunter und schließen Sie die Installation und Konfiguration des Fusion HAT+ ab).


#. Aktualisieren Sie nun die Softwarequellen des Raspberry Pi, um sicherzustellen, dass Sie die neuesten Pakete erhalten:

   .. code-block:: shell

      sudo apt update

#. Verwenden Sie den folgenden Befehl, um die Python-3-Version von OpenCV zu installieren:

   .. code-block:: bash

      sudo apt install python3-opencv

#. Führen Sie den folgenden Befehl aus, um zu überprüfen, ob OpenCV erfolgreich installiert wurde:

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   Wenn die OpenCV-Versionsnummer angezeigt wird, war die Installation erfolgreich.

   .. image:: img/install_opencv_check_version.png
      :align: center