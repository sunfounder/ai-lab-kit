.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Se stai utilizzando l'immagine preinstallata "Raspberry Pi OS with AI Fusion Lab Kit", puoi saltare questa sezione. Questa immagine include gia' tutte le installazioni software, le configurazioni ambientali e i deployment degli esempi di codice descritti in questo capitolo.


.. _opencv_install:

0. Configurare OpenCV
=====================

Questo capitolo mostra come installare OpenCV su Raspberry Pi e verificare che funzioni correttamente.

#. Per utilizzare comodamente il modulo fotocamera, si consiglia :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

     L'assemblaggio del pan-tilt potrebbe oscurare alcuni pin, quindi si consiglia di assemblarlo solo quando si utilizza la fotocamera, oppure posizionarlo all'esterno dopo l'assemblaggio.

   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accedi al desktop di Raspberry Pi:

   * :ref:`remote_desktop`: Usa **VNC** per un'esperienza desktop completa.
   * |link_rpi_connect|: Usa **Raspberry Pi Connect** per accedere al tuo Pi in modo sicuro da qualsiasi browser.

#. Completa la configurazione in :ref:`install_all_modules` (scarica il pacchetto di codice fornito e completa l'installazione e configurazione di Fusion HAT+).

#. Ora, aggiorna le sorgenti software di Raspberry Pi per assicurarti di ottenere i pacchetti piu' recenti:

   .. code-block:: shell

      sudo apt update

#. Usa il seguente comando per installare la versione Python 3 di OpenCV:

   .. code-block:: bash

      sudo apt install python3-opencv

#. Esegui il comando seguente per verificare che OpenCV sia stato installato correttamente:

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   Se viene visualizzato il numero di versione di OpenCV, l'installazione e' riuscita.

   .. image:: img/install_opencv_check_version.png
      :align: center