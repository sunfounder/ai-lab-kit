.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: Se stai utilizzando l’immagine preinstallata "Raspberry Pi OS with AI Fusion Lab Kit", puoi saltare questa sezione. Questa immagine include gia’ tutte le installazioni software, le configurazioni ambientali e le distribuzioni del codice di esempio descritte in questo capitolo.

.. _install_all_modules:

Configura Alimentazione e Installa Software
================================================================

In questo capitolo, installerai il software correlato, configurerai l’audio, imposterai la gestione sicura dell’alimentazione e imparerai come gestire gli spegnimenti.


.. _download_code:

Scarica il Codice di Esempio
---------------------------------
Scarica il set completo di codice di esempio per il kit:

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
