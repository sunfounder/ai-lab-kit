.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: 如果您使用的是预装的"Raspberry Pi OS with AI Fusion Lab Kit"镜像，可以跳过本节。该镜像已包含本章所述的所有软件安装、环境配置和示例代码部署。


0. 安装YOLO环境
==============================



本章将介绍如何在Raspberry Pi上安装YOLO并验证其是否正常工作。

#. 为了方便使用摄像头模块，建议先完成 :ref:`assemble_fusion_hat_pan_tilt`。

   .. note::

      组装云台可能会遮挡部分引脚，因此建议仅在使用摄像头时组装，或在组装后将云台放置在外部。


   .. image:: ../quick_start/img/gimbal_assemble.png

#. 访问Raspberry Pi桌面：

   * :ref:`remote_desktop`: 使用\ **VNC**\ 获得完整的桌面体验。
   * |link_rpi_connect|: 使用\ **Raspberry Pi Connect**\ 从任何浏览器安全地访问您的Pi。



3. 安装所需的依赖包：

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. 安装Ultralytics（官方YOLO库）：

   .. code-block:: bash

      # Install CPU version of PyTorch (specify CPU source)
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Install ultralytics, but skip torch dependencies
      pip3 install ultralytics --no-deps --break-system-packages

      # Manually install ultralytics' other dependencies
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages