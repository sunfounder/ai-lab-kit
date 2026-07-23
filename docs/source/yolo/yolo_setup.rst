.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: Si vous utilisez l'image préinstallée « Raspberry Pi OS with AI Fusion Lab Kit », vous pouvez sauter cette section. Cette image inclut déjà toutes les installations logicielles, les configurations d'environnement et les déploiements de code d'exemple décrits dans ce chapitre.


0. Configuration de l'environnement YOLO
=============================================



Ce chapitre vous montre comment installer YOLO sur le Raspberry Pi et vérifier qu'il fonctionne correctement.

#. Pour utiliser le module caméra facilement, il est recommandé d'assembler le :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

      L'assemblage du pan-tilt peut masquer certaines broches, il est donc recommandé de l'assembler uniquement lors de l'utilisation de la caméra, ou de le placer à l'extérieur après l'assemblage.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accédez au bureau du Raspberry Pi :

   * :ref:`remote_desktop`: Utilisez **VNC** pour une expérience de bureau complète.
   * |link_rpi_connect|: Utilisez **Raspberry Pi Connect** pour accéder à votre Pi en toute sécurité depuis n'importe quel navigateur.



3. Installez les dépendances requises :

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Installez Ultralytics (la bibliothèque officielle YOLO) :

   .. code-block:: bash

      # Installer la version CPU de PyTorch (spécifier la source CPU)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Installer ultralytics, mais ignorer les dépendances torch
      pip3 install ultralytics --no-deps --break-system-packages

      # Installer manuellement les autres dépendances d'ultralytics
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages

