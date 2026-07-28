.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. 播放视频
=======================================

在本章中，您将学习如何在OpenCV中读取和播放视频流，以及如何通过计算帧处理时间来控制播放速度。



1. 项目概览
-------------------

在本节中，我们将实现以下目标：

- 使用 ``cv2.VideoCapture`` 打开视频文件
- 逐帧读取和显示视频
- 视频结束后自动重新开始播放
- 通过处理时间计算来控制播放帧率
- 按 ``q`` 键退出播放

.. image:: img/opencv_video.png
   :alt: 视频播放界面示意图
   :align: center


2. 运行代码
------------------------

.. important::

   开始之前，请确保：

   * 云台已组装
   * 您可以访问Raspberry Pi桌面
   * 代码包已安装
   * Fusion HAT+已安装并配置
   * OpenCV已安装

   详细说明请参见 :ref:`opencv_install`。

#. 打开终端并输入以下命令：

   .. code-block:: bash

      cd ~/ai-lab-kit/opencv_python
      python3 cv_2_video.py

#. 运行脚本后，OpenCV会打开一个标题为\ **Video**\ 的窗口，并实时显示视频帧。

   如果视频播放到结尾，它将自动从头开始重新播放。

   要停止程序，您可以：

   * 按键盘上的 **q** 键退出播放
   * 点击关闭按钮关闭窗口

   窗口关闭后，所有OpenCV资源将被释放，程序退出。


3. 完整代码
------------------------------

.. code-block:: python

  import cv2

  # Open the video file
  cap = cv2.VideoCapture("sample2.mp4")

  while True:
      # Read one frame from the video
      ret, frame = cap.read()

      # If the video ends, restart from the beginning
      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

      # Resize the frame for better display performance
      frame = cv2.resize(frame, (640, 480))

      # Display the frame in a window named "Video"
      cv2.imshow("Video", frame)

      # Wait 30 ms between frames (~30 FPS)
      # This also processes GUI events (keyboard and window events)
      key = cv2.waitKey(30) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
          break

      # Exit if the user closes the window (click the close button)
      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

  # Release the video capture object
  cap.release()

  # Close all OpenCV windows
  cv2.destroyAllWindows()


4. 代码解释
-----------------------

#. 打开视频文件：

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   这将打开视频文件并创建一个\ ``VideoCapture``\ 对象用于读取帧。

#. 从视频中读取一帧：

   .. code-block:: python

      ret, frame = cap.read()

   - 如果帧读取成功，\ ``ret``\ 为\ ``True``。
   - 当视频结束或读取失败时，\ ``ret``\ 变为\ ``False``。
   - ``frame``\ 是图像数据（一个NumPy数组）。

#. 视频结束后循环播放：

   .. code-block:: python

      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

   当视频结束时，将播放位置重置为第一帧，从而实现重新播放。

#. 调整帧大小：

   .. code-block:: python

      frame = cv2.resize(frame, (640, 480))

   将每帧图像调整为640×480，以便在Raspberry Pi上更流畅地显示并降低CPU使用率。

#. 显示帧：

   .. code-block:: python

      cv2.imshow("Video", frame)

   在名为\ ``Video``\ 的窗口中显示当前帧。

#. 控制播放速度并读取键盘输入：

   .. code-block:: python

      key = cv2.waitKey(30) & 0xFF

   每帧之间等待约30毫秒（约30 FPS），同时处理GUI事件。

#. 按 ``q`` 退出：

   .. code-block:: python

      if key == ord("q"):
          break

   按 ``q`` 停止程序。

#. 窗口关闭时退出：

   .. code-block:: python

      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

   检查窗口是否仍然可见。
   如果用户关闭窗口，程序将安全退出。

#. 释放视频捕获对象：

   .. code-block:: python

      cap.release()

   释放视频文件资源。

#. 关闭所有OpenCV窗口：

   .. code-block:: python

      cv2.destroyAllWindows()

   关闭所有OpenCV窗口并释放GUI资源。


5. 扩展练习
-------------------

- 尝试更改窗口大小，观察对图像清晰度的影响。
- 替换为不同的视频文件以测试兼容性。
- 打印每帧的处理时间，以更好地理解FPS与播放延迟之间的关系。