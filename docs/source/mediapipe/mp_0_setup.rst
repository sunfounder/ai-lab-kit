.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: 如果您使用的是预装的"Raspberry Pi OS with AI Fusion Lab Kit"镜像，可以跳过本节。该镜像已包含本章所述的所有软件安装、环境配置和示例代码部署。


.. _mediapipe_install:

0. 安装 MediaPipe
====================================================================

关于操作系统版本
-------------------------------

.. warning::

   **推荐操作系统**：Raspberry Pi OS Bookworm（Debian 12，64 位）

   不推荐使用 Raspberry Pi OS Trixie（Debian 13），原因如下：

   * MediaPipe 尚未支持 Python 3.13。
   * Picamera2 仅适用于系统 Python。

   一旦 Trixie 获得支持，本教程将进行更新。

   如果您希望官方 MediaPipe 支持 Python 3.13，可以通过以下渠道提交反馈：

   * GitHub Issue：https://github.com/google-ai-edge/mediapipe/issues/5708
   * 支持页面：https://ai.google.dev/edge/mediapipe/support



开始之前
----------------

.. important::


   开始之前，请确保：

   * 云台已组装完成
   * 可以访问 Raspberry Pi 桌面
   * 代码包已安装
   * Fusion HAT+ 已安装并配置
   * OpenCV 已安装

   详细说明请参见 :ref:`opencv_install`。

这些准备工作可确保 MediaPipe 在 Raspberry Pi 上具备完整的图形和摄像头功能。


安装步骤
----------------------------------

#. 安装 MediaPipe

   使用 pip 安装 MediaPipe。在 Raspberry Pi OS Bookworm（Debian 12，64 位）上，
   pip 会自动下载正确的 wheel 包。

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. 验证安装

   运行以下命令确认 MediaPipe 已正确安装。

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   预期输出：

   .. code-block:: text

      MediaPipe version: 0.10.18


常见问题及解决方案
-------------------------

#. MediaPipe 安装失败

   这种情况通常发生在使用不支持的操作系统版本时。

   解决方案：

   * MediaPipe 目前仅支持 Raspberry Pi OS Bookworm（Debian 12，64 位）。
   * Raspberry Pi OS Trixie（Debian 13，Python 3.13）不受支持。

#. 摄像头无法在 MediaPipe 或 OpenCV 中打开

   这种情况通常是因为 Raspberry Pi 的摄像头接口未启用。

   解决方案：

   * 在 ``raspi-config`` 中启用摄像头：
     接口选项 → 摄像头 → 启用

#. OpenCV 导入错误

   某些通过 pip 安装的 OpenCV 版本可能与 Raspberry Pi OS 的库不兼容。

   解决方案：

   .. code-block:: bash

      sudo apt install python3-opencv

#. 安装后无法导入 MediaPipe

   这可能是由于 pip、setuptools 或 wheel 版本过旧。

   解决方案：

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


您的 MediaPipe 现已准备就绪。
接下来可以使用 Raspberry Pi 摄像头运行实时人脸检测了。
