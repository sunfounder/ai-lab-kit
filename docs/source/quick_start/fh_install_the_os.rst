.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

Installation des Betriebssystems
===================================

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager

Herunterladen der exklusiven Imagedatei
------------------------------------------------------

Laden Sie die Betriebssystem-Imagedatei des AI Fusion Lab Kits herunter: `Raspberry Pi OS mit AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_.

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

Dieses Image basiert auf Raspberry Pi OS und enthält das AI Fusion Lab Kit bereits vorinstalliert im System. Es umfasst die gesamte erforderliche Software, den Beispielcode und die zugehörigen Konfigurationen, die für das AI Fusion Lab Kit benötigt werden. Durch die Verwendung dieses Images können Sie einige im Handbuch beschriebene Einrichtungsschritte überspringen.

Wenn Sie lieber ein natives Raspberry Pi OS für die manuelle Konfiguration verwenden möchten, installieren Sie bitte:  
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. Gehen Sie zum Bereich „Betriebssystem“ und wählen Sie **Benutzerdefiniertes Image verwenden**.
   
   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   Wählen Sie die heruntergeladene Imagedatei ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip`` aus.

   .. image:: img/fusion_kit_imager2.png
      :width: 90%

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_storage
   :end-before: end_storage

.. .. include:: /_shared/pi_start/install_os_trixie.rst
..    :start-after: start_cutomization_os
..    :end-before: end_cutomization_os

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_write_os
   :end-before: end_write_os