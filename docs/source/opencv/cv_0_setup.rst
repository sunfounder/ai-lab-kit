.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Si estás usando la imagen preinstalada "Raspberry Pi OS with AI Fusion Lab Kit", puedes omitir esta sección. Esta imagen ya incluye todas las instalaciones de software, configuraciones de entorno e implementaciones de código de ejemplo descritas en este capítulo.


.. _opencv_install:

0. Configurar OpenCV
=========================================================================

Este capítulo te muestra cómo instalar OpenCV en la Raspberry Pi y verificar que funcione correctamente.

#. Para usar el módulo de cámara de manera conveniente, se recomienda :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

      Ensamblar el soporte para cámara puede obstruir algunos pines, por lo que se recomienda ensamblarlo solo cuando se use la cámara, o colocarlo en el exterior después del ensamblaje.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accede al escritorio de Raspberry Pi:

   * :ref:`remote_desktop`: Usa **VNC** para una experiencia de escritorio completa.
   * |link_rpi_connect|: Usa **Raspberry Pi Connect** para acceder a tu Pi de forma segura desde cualquier navegador.


#. Completa la configuración en :ref:`install_all_modules` (descarga el paquete de código proporcionado y finaliza la instalación y configuración de Fusion HAT+).


#. Ahora, actualiza las fuentes de software de Raspberry Pi para asegurarte de obtener los últimos paquetes:

   .. code-block:: shell

      sudo apt update

#. Usa el siguiente comando para instalar la versión Python 3 de OpenCV:

   .. code-block:: bash

      sudo apt install python3-opencv

#. Ejecuta el siguiente comando para verificar que OpenCV se haya instalado correctamente:

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   Si se muestra el número de versión de OpenCV, la instalación fue exitosa.

   .. image:: img/install_opencv_check_version.png
      :align: center
