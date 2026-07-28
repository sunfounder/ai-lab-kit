.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

安装操作系统
===================================



.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager


下载专属镜像文件
------------------------------------------------------

下载 AI Fusion Lab Kit 操作系统镜像文件： `Raspberry Pi OS with AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_。

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

此镜像基于 Raspberry Pi OS，并预集成了 AI Fusion Lab Kit 到系统中。它包含了 AI Fusion Lab Kit 所需的所有必要软件、示例代码及相关配置。使用此镜像，您可以跳过文档中描述的部分设置步骤。

如果您更倾向于使用原生 Raspberry Pi OS 进行手动配置，请安装：
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. 进入 OS 部分，选择 **Use custom**

   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   然后选择下载的镜像文件 ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip``\ 。

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
