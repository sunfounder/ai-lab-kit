.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: 如果您使用的是预装的"Raspberry Pi OS with AI Fusion Lab Kit"镜像，可以跳过本节。该镜像已包含本章所述的所有软件安装、环境配置和示例代码部署。


.. _opencv_install:

0. 安装OpenCV
=========================================================================

本章将介绍如何在Raspberry Pi上安装OpenCV并验证其是否正常工作。

#. 为了方便使用摄像头模块，建议先完成 :ref:`assemble_fusion_hat_pan_tilt`。

   .. note::

      组装云台可能会遮挡部分引脚，因此建议仅在使用摄像头时组装，或在组装后将云台放置在外部。


   .. image:: ../quick_start/img/gimbal_assemble.png

#. 访问Raspberry Pi桌面：

   * :ref:`remote_desktop`: 使用\ **VNC**\ 获得完整的桌面体验。
   * |link_rpi_connect|: 使用\ **Raspberry Pi Connect**\ 从任何浏览器安全地访问您的Pi。


#. 完成 :ref:`install_all_modules`\ 中的设置（下载提供的代码包，并完成Fusion HAT+的安装和配置）。


#. 现在，更新Raspberry Pi软件源以确保您获得最新的软件包：

   .. code-block:: shell

      sudo apt update

#. 使用以下命令安装Python 3版本的OpenCV：

   .. code-block:: bash

      sudo apt install python3-opencv

#. 运行以下命令验证OpenCV是否安装成功：

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   如果显示OpenCV版本号，则表示安装成功。

   .. image:: img/install_opencv_check_version.png
      :align: center