.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: 
   
   Wenn Sie das vorinstallierte Image „Raspberry Pi OS mit AI Fusion Lab Kit“ verwenden, können Sie diesen Abschnitt überspringen. Dieses Image enthält bereits alle in diesem Kapitel beschriebenen Softwareinstallationen, Umgebungskonfigurationen und Beispielcode-Bereitstellungen.

.. _install_all_modules:

Stromversorgung konfigurieren & Software installieren
================================================================

In diesem Kapitel installieren Sie die benötigte Software, konfigurieren das Audio-System, richten ein sicheres Energiemanagement ein und lernen, wie Sie das System korrekt herunterfahren.


.. _download_code:

Beispielcode herunterladen
---------------------------------

Laden Sie den vollständigen Satz an Beispielcode für dieses Kit herunter:

   .. raw:: html

      <run></run>

   .. code-block::

      cd ~/
      git clone https://github.com/sunfounder/ai-lab-kit.git --depth 1


.. _install_fusion_hat:

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_install_fusion_hat
   :end-before: end_install_fusion_hat

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_configure_safe_shutdown
   :end-before: end_configure_safe_shutdown