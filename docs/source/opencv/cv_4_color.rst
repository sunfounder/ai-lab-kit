.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. 颜色检测
===========================================

颜色检测是计算机视觉中最基础且最实用的功能之一。
在本章中，我们将通过逐步的代码和讲解，使用\ **HSV颜色空间**\ 来\ **检测红色物体**\ 并\ **绘制边界框**。

这为更高级的物体跟踪技术（如CAMShift）奠定了基础。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. 目标与方法
--------------------------------------------

- 使用 **Picamera2** 捕捉实时摄像头帧
- 将图像从BGR转换为HSV颜色空间
- 使用 ``cv2.inRange`` 提取红色区域
- 使用形态学滤波去除噪点
- 使用 ``cv2.findContours`` 查找红色物体轮廓
- 在检测到的红色区域周围绘制边界框

.. image:: img/color_detection.png
   :alt: 颜色检测预览示意图
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
      python3 cv_4_color.py

#. 运行程序后，屏幕上将出现两个OpenCV窗口：

   * **Red Detection** – 显示实时摄像头画面，检测到的红色物体周围带有绿色边界框
   * **Red Mask** – 显示用于红色检测的二值掩膜图像

   程序持续从Raspberry Pi摄像头捕捉帧并实时检测红色区域。
   如果检测到红色物体，彩色图像上将显示绿色矩形和面积值。

   您可以通过两种方式退出程序：

   * 按键盘上的 **q** 键
   * 单击任意OpenCV窗口的关闭按钮（X）

   退出后，摄像头停止采集，所有OpenCV窗口关闭。

3. 完整代码
------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. 代码解释
--------------------------------

#. 初始化Picamera2并开始视频流：

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   将摄像头配置为640×480并开始预览流。
   ``XRGB8888``\ 是4通道格式，因此捕获的帧类似BGRA格式。

#. 将捕获的帧转换为OpenCV常用的格式：

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2返回4通道图像，我们将其转换为标准的3通道BGR进行处理。

#. 使用HSV颜色空间进行稳健的颜色检测：

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV将颜色（色相）与亮度分离，使颜色检测在不同光照下更加稳定。

#. 定义红色的两个HSV范围：

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   在OpenCV的HSV中，红色在色相刻度上"环绕"（接近0和接近180），因此需要组合两个范围来覆盖所有红色。

#. 使用形态学操作清理掩膜（减少噪点并填充空洞）：

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** 去除微小的噪点。
   - **CLOSE** 填充检测到的红色区域内部的小空洞。

#. 查找红色区域并过滤小区域：

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   从二值掩膜中检测轮廓。
   ``MIN_AREA``\ 忽略小的红色区域以减少误检。

#. 在结果图像上绘制边界框和标签：

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   显示OpenCV发现红色物体的位置，并打印检测到的区域面积供参考。

#. 同时显示结果和掩膜：

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   **结果窗口**\ 显示带框的摄像头画面，\ **掩膜窗口**\ 显示仅包含红色的二值图像。

#. 退出条件（键盘 + 窗口关闭）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   按 ``q`` 退出，或关闭任一窗口以安全退出。

#. 清理资源：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   始终停止摄像头并关闭OpenCV窗口以释放资源。


5. 参数调试建议
-----------------------------

- ``LOWER_RED1 / UPPER_RED1``: 调整此范围以检测其他颜色。
  例如，绿色大约为\ ``[35, 50, 50]``\ 到\ ``[85, 255, 255]``。

- ``KERNEL``: 更大的内核提供更强的滤波效果，但可能去除小物体。

- ``MIN_AREA``: 增大此值可过滤小的噪点轮廓；减小则使检测更灵敏。

.. note::
   您可以先只显示 ``mask``，调整阈值直到目标区域清晰可见，然后再进行后续处理。



6. 扩展练习
--------------------------

- 修改HSV阈值以检测其他颜色（例如蓝色或绿色）。
- 在更复杂的背景下尝试不同的形态学参数。