.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: Se stai utilizzando l'immagine preinstallata "Raspberry Pi OS with AI Fusion Lab Kit", puoi saltare questa sezione. Questa immagine include già tutte le installazioni software, le configurazioni ambientali e i deployment del codice di esempio descritti in questo capitolo.


0. Configurare l'Ambiente YOLO
==============================



Questo capitolo mostra come installare YOLO su Raspberry Pi e verificare che funzioni correttamente.

#. Per utilizzare il modulo fotocamera comodamente, si consiglia :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

      L'assemblaggio del pan-tilt potrebbe oscurare alcuni pin, quindi si consiglia di assemblarlo solo quando si utilizza la fotocamera, o di posizionarlo all'esterno dopo l'assemblaggio.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accedere al Desktop di Raspberry Pi:

   * :ref:`remote_desktop`: Usare **VNC** per un'esperienza desktop completa.
   * |link_rpi_connect|: Usare **Raspberry Pi Connect** per accedere al tuo Pi in modo sicuro da qualsiasi browser.



3. Installare le dipendenze richieste:

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Installare Ultralytics (la libreria YOLO ufficiale):

   .. code-block:: bash

      # Install CPU version of PyTorch (specify CPU source)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Install ultralytics, but skip torch dependencies
      pip3 install ultralytics --no-deps --break-system-packages

      # Manually install ultralytics' other dependencies
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages

