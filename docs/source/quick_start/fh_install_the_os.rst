.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

Installazione del Sistema Operativo
===================================



.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager


Scarica il File Immagine Esclusivo
------------------------------------------------------

Scarica il file immagine del sistema operativo AI Fusion Lab Kit: `Raspberry Pi OS with AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_.

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

Questa immagine e' basata su Raspberry Pi OS e include AI Fusion Lab Kit pre-integrato nel sistema. Contiene tutto il software necessario, il codice di esempio e le configurazioni correlate richieste per AI Fusion Lab Kit. Utilizzando questa immagine, puoi saltare alcuni passaggi di configurazione descritti nella documentazione.

Se preferisci utilizzare un Raspberry Pi OS nativo per la configurazione manuale, installa:
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. Vai alla sezione OS e scegli **Use custom** (Usa personalizzato)

   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   E seleziona il file immagine scaricato ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip``.

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
