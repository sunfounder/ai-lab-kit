.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _opencv_install:

0. Setup OpenCV
=========================================================================

This chapter shows you how to install OpenCV on the Raspberry Pi and verify that it works correctly.

#. To use camera module conveniently, :ref:`assemble_fusion_hat_pan_tilt` is recommended.

   .. note:: 
     
      Assembling the pan-tilt may obscure some pins, so it is recommended to assemble it only when using the camera, or place it on the outside after assembly.
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Access the Raspberry Pi Desktop:

   * :ref:`remote_desktop`: Use **VNC** for a full desktop experience.
   * |link_rpi_connect|: Use **Raspberry Pi Connect** to access your Pi securely from any browser.


#. Complete the setup in :ref:`install_all_modules` (download the provided code package, and finish the Fusion HAT+ installation and configuration).


#. Now, update the Raspberry Pi software sources to ensure you get the latest packages:

   .. code-block:: shell

      sudo apt update

#. Use the following command to install the Python 3 version of OpenCV:

   .. code-block:: bash

      sudo apt install python3-opencv

#. Run the command below to verify that OpenCV has been installed successfully:

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   If the OpenCV version number is displayed, the installation was successful.

   .. image:: img/install_opencv_check_version.png
      :align: center