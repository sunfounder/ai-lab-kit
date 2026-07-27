.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: Si estas usando la imagen preinstalada "Raspberry Pi OS with AI Fusion Lab Kit", puedes omitir esta seccion. Esta imagen ya incluye todas las instalaciones de software, configuraciones de entorno e implementaciones de codigo de ejemplo descritas en este capitulo.


0. Configurar el Entorno YOLO
==============================



Este capitulo te muestra como instalar YOLO en la Raspberry Pi y verificar que funcione correctamente.

#. Para usar el modulo de la camara de forma conveniente, se recomienda :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

      El montaje del pan-tilt puede obstruir algunos pines, por lo que se recomienda ensamblarlo solo cuando se use la camara, o colocarlo en la parte exterior despues del montaje.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accede al escritorio de la Raspberry Pi:

   * :ref:`remote_desktop`: Usa **VNC** para una experiencia completa de escritorio.
   * |link_rpi_connect|: Usa **Raspberry Pi Connect** para acceder a tu Pi de forma segura desde cualquier navegador.



3. Instala las dependencias necesarias:

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Instala Ultralytics (la libreria oficial de YOLO):

   .. code-block:: bash

      # Install CPU version of PyTorch (specify CPU source)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Install ultralytics, but skip torch dependencies
      pip3 install ultralytics --no-deps --break-system-packages

      # Manually install ultralytics' other dependencies
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages
