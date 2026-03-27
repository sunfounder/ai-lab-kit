0. Setup YOLO Environment
==============================



This chapter shows you how to install Yolo on the Raspberry Pi and verify that it works correctly.

#. To use camera module conveniently, :ref:`assemble_fusion_hat_pan_tilt` is recommended.

   .. note:: 
     
      Assembling the pan-tilt may obscure some pins, so it is recommended to assemble it only when using the camera, or place it on the outside after assembly.
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Access the Raspberry Pi Desktop:

   * :ref:`remote_desktop`: Use **VNC** for a full desktop experience.
   * |link_rpi_connect|: Use **Raspberry Pi Connect** to access your Pi securely from any browser.



3. Install required dependencies:

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Install Ultralytics (the official YOLO library):

   .. code-block:: bash

      # Install CPU version of PyTorch (specify CPU source)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Install ultralytics, but skip torch dependencies
      pip3 install ultralytics --no-deps --break-system-packages

      # Manually install ultralytics' other dependencies
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages

