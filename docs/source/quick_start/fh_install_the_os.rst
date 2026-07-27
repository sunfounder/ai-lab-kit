.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

Instalacion del Sistema Operativo
===================================



.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager


Descarga del Archivo de Imagen Exclusivo
------------------------------------------------------

Descarga el archivo de imagen del sistema operativo AI Fusion Lab Kit: `Raspberry Pi OS with AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_.

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

Esta imagen esta basada en Raspberry Pi OS y viene con el AI Fusion Lab Kit preintegrado en el sistema. Incluye todo el software necesario, el codigo de ejemplo y las configuraciones relacionadas requeridas para el AI Fusion Lab Kit. Al usar esta imagen, puedes omitir algunos pasos de configuracion descritos en la documentacion.

Si prefieres usar un sistema operativo nativo de Raspberry Pi para la configuracion manual, instala:
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. Ve a la seccion de SO y elige **Use custom**

   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   Y selecciona el archivo de imagen descargado ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip``.

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
