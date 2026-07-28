.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. 实时摄像头画面捕捉
================================================================

在前几章中，我们学习了如何读取和播放本地视频文件。
在本章中，我们将更进一步，使用\ **Raspberry Pi摄像头**\ 进行实时视频捕捉，并利用OpenCV进行\ **颜色空间转换**。


1. 项目目标
--------------------------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

- 使用 **Picamera2** 捕捉实时摄像头帧
- 将摄像头输出从BGRA格式转换为BGR格式
- 使用OpenCV进行实时预览
- 了解不同颜色空间的特性和用途

.. image:: img/opencv_camera.png
   :alt: 实时摄像头预览示意图
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
      python3 cv_3_camera.py

#. 运行程序后，将出现两个OpenCV窗口：

   * **BGR Frame** – 显示实时的彩色摄像头图像
   * **GRAY Frame** – 显示同一图像的灰度版本

   您可以通过两种方式退出程序：

   * 按键盘上的 **q** 键
   * 单击任意窗口的关闭按钮（X）

   退出后，摄像头停止采集，所有OpenCV窗口关闭。

3. 示例代码
-------------------------------

以下是本章的完整Python示例（\ ``cv_3_camera.py``\ ）：

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. 代码解释
-------------------

#. 导入所需库：

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2用于从Raspberry Pi摄像头捕捉帧，OpenCV用于图像转换和显示。

#. 创建Picamera2对象并配置摄像头：

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   将摄像头设置为640×480分辨率。
   ``XRGB8888``\ 是4通道格式，因此每帧图像类似BGRA格式。

#. 以NumPy数组形式捕捉帧：

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   每次循环从摄像头读取一帧图像。

#. 转换帧用于显示：

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr``\ 用于正常的彩色显示。
   - ``frame_gray``\ 是同一帧的灰度版本。

#. 在两个窗口中显示帧：

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   打开两个OpenCV窗口：一个显示彩色帧，另一个显示灰度帧。

#. 退出条件（按 ``q`` 或关闭窗口）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - 按 ``q`` 退出。
   - 关闭任一窗口也会安全停止程序。

#. 限制FPS以降低CPU使用率：

   .. code-block:: python

      time.sleep(1 / 30)

   增加一个小延迟，使循环以约30 FPS运行，可降低Raspberry Pi的CPU负载。

#. 停止摄像头并关闭OpenCV窗口：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   在程序退出前释放摄像头并关闭所有OpenCV窗口。

5. 颜色空间转换的重要性
-------------------------------------------------------------------

摄像头输出的原始图像格式可能与OpenCV处理所需的格式不匹配。
在本示例中，Picamera2输出的是\ **XRGB8888（BGRA）**\ 格式，而OpenCV主要使用\ **BGR**\ 格式。

因此，我们需要进行如下图像转换：

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

这确保了图像按OpenCV使用的标准BGR通道顺序排列，从而正确显示和处理。

然后，我们可以将BGR图像转换为灰度图像以进行后续处理：

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

这使我们能够将摄像头捕捉的图像转换为适合OpenCV图像处理工作流程的格式。

**常见颜色空间及其用途**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 颜色空间
     - 特点
     - 典型用途
   * - **BGR**
     - OpenCV默认格式
     - 图像显示、基本处理、边缘检测
   * - **RGB**
     - 符合人眼感知直觉
     - 可视化、深度学习图像输入
   * - **GRAY**
     - 单通道灰度图像
     - 物体检测、边缘检测、性能优化
   * - **HSV**
     - 分离颜色和亮度
     - 颜色检测、物体跟踪、图像分割
   * - **YCrCb**
     - 分离亮度和色度
     - 人脸检测、视频压缩、光照鲁棒性

例如，**HSV**\ 通常更适合\ **颜色检测和物体跟踪**，
而 **YCrCb**\ 在\ **人脸识别**\ 或\ **光照变化场景**\ 中更加稳健。

6. 扩展练习
-------------------------------------------

- 尝试将BGR转换为GRAY或HSV并观察结果。

  例如，使用：

  - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
  - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
  - 等等

- 测试不同的分辨率（例如1280×720），观察对延迟和帧率的影响。
- 将此代码与之前的视频播放示例结合，实现摄像头画面与视频源的切换。