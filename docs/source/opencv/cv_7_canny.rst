.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

7. Canny边缘检测
=========================================

在本章中，我们将使用Raspberry Pi + Picamera2捕获实时视频，并利用OpenCV的\ **Canny算法**\ 进行边缘检测。
边缘检测是计算机视觉的基础部分，而Canny算法被广泛认为是最稳定、抗噪能力最强的方法之一。

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_7.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Canny算法的作用是什么？
--------------------------------------------------

在图像中，\ **边缘**\ 通常对应于灰度强度发生剧烈变化的位置，例如：

- 物体的轮廓
- 明亮区域与黑暗区域之间的边界
- 结构性的边缘线条

Canny边缘检测的目的是：

- **精确提取边缘信息**，同时减少不必要的干扰；
- 为后续的\ **轮廓检测**、\ **物体分割**\ 和\ **几何形状识别**（如圆形、矩形）提供可靠基础；
- 在机器人视觉中，常用于\ **路径检测**\ 和\ **障碍物识别**。

.. image:: img/opencv_canny.png
   :alt: Canny边缘检测示意图
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
      python3 cv_7_canny.py

   .. tip::

      我们还提供\ ``cv_7_canny_video.py``\ 用于处理视频文件，以及\ ``cv_7_canny_conbine.py``\ 用于结合实时捕捉和视频（组合视图）。

#. 运行程序后，将出现两个OpenCV窗口：

   * **Camera** – 显示实时摄像头画面
   * **Canny Edges** – 实时显示检测到的边缘

   您可以使用滑动条调整边缘检测阈值。
   按 **q** 或关闭任意窗口退出程序。

3. 完整代码
---------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2

   # Empty callback function for trackbars (required by OpenCV API)
   def _noop(x):
      pass

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()

   # Create a preview configuration:
   # size: resolution of the camera image
   # format: XRGB8888 (4-channel image, similar to BGRA)
   picam2.configure(
      picam2.create_preview_configuration(
         main={"size": (640, 480), "format": "XRGB8888"}
      )
   )

   # Start the camera
   picam2.start()

   # -----------------------------
   # Create OpenCV windows
   # -----------------------------
   WIN_CAM = "Camera"        # window for original image
   WIN_EDGE = "Canny Edges"  # window for edge detection result

   cv2.namedWindow(WIN_CAM)
   cv2.namedWindow(WIN_EDGE)

   # -----------------------------
   # Create trackbars to tune Canny thresholds
   # -----------------------------
   # low_th: lower threshold for Canny
   # high_th: higher threshold for Canny
   cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
   cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   print("Press 'q' to exit")

   # -----------------------------
   # Main loop
   # -----------------------------
   while True:
      # Capture one frame from the camera (BGRA format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for OpenCV processing
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame to grayscale
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

      # Apply Gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Read current threshold values from trackbars
      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      # Ensure high_th is always larger than low_th
      if high_th <= low_th:
         high_th = low_th + 1
         cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

      # Perform Canny edge detection
      edges = cv2.Canny(blurred, low_th, high_th)

      # Show original camera image
      cv2.imshow(WIN_CAM, frame_bgr)

      # Show edge detection result
      cv2.imshow(WIN_EDGE, edges)

      # Process GUI events and keyboard input
      key = cv2.waitKey(1) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
         break

   # -----------------------------
   # Cleanup
   # -----------------------------
   picam2.stop()             # Stop the camera
   cv2.destroyAllWindows()   # Close all OpenCV windows

4. 代码解释
---------------------------------
#. 为滑动条定义回调函数：

   .. code-block:: python

      def _noop(x):
          pass

   OpenCV滑动条需要一个回调函数。
   我们不需要在其中执行任何操作，因此空函数即可。

#. 初始化Picamera2并设置预览格式：

   .. code-block:: python

      picam2 = Picamera2()
      picam2.configure(
          picam2.create_preview_configuration(
              main={"size": (640, 480), "format": "XRGB8888"}
          )
      )
      picam2.start()

   以640×480分辨率启动Raspberry Pi摄像头。
   ``XRGB8888``\ 是4通道格式，因此帧数据类似BGRA。

#. 创建两个OpenCV窗口：

   .. code-block:: python

      WIN_CAM = "Camera"
      WIN_EDGE = "Canny Edges"

      cv2.namedWindow(WIN_CAM)
      cv2.namedWindow(WIN_EDGE)

   一个窗口显示原始摄像头图像，另一个显示Canny边缘检测结果。

#. 创建滑动条以实时调整Canny阈值：

   .. code-block:: python

      cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
      cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   - ``low_th``: Canny的低阈值。
   - ``high_th``: Canny的高阈值。

   您可以拖动这些滑块来改变边缘检测的灵敏度。

#. 捕获帧并转换为OpenCV处理的格式：

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   摄像头输出为4通道，因此我们将其转换为标准的3通道BGR。

#. 转换为灰度图并模糊图像：

   .. code-block:: python

      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

   - Canny在灰度图像上运行。
   - 高斯模糊减少噪点，有助于避免检测到过多的虚假边缘。

#. 读取滑动条值并保持有效：

   .. code-block:: python

      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      if high_th <= low_th:
          high_th = low_th + 1
          cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

   Canny要求\ ``high_th``\ 大于\ ``low_th``。
   如果用户将值拖得太接近，此代码块会自动修正。

#. 执行Canny边缘检测：

   .. code-block:: python

      edges = cv2.Canny(blurred, low_th, high_th)

   Canny突出显示图像中的强边缘。
   较低的阈值通常会检测到更多边缘，但也会增加噪声。

#. 显示两个窗口：

   .. code-block:: python

      cv2.imshow(WIN_CAM, frame_bgr)
      cv2.imshow(WIN_EDGE, edges)

   左侧窗口显示实时摄像头画面，另一个窗口显示检测到的边缘。

#. 退出条件（按 ``q`` 或关闭窗口）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
          break

   初学者可以通过键盘或关闭窗口两种方式停止程序。

#. 清理资源：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   始终停止摄像头并关闭所有OpenCV窗口以释放资源。

5. 为什么Canny有用？
--------------------------

Canny输出非常适合后续的视觉任务：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 应用
     - 描述
   * - 轮廓检测
     - 在Canny输出上使用 ``cv2.findContours``\ 获取物体形状
   * - 物体分割
     - 以边缘为基础将目标与背景分离
   * - 形状识别
     - 结合霍夫变换检测圆形、直线等
   * - 机器人导航
     - 检测地面、道路、障碍物轮廓以辅助规划
   * - OCR / 目标定位
     - 文本区域、二维码、标记通常具有清晰的边缘特征

Canny不仅仅是"看起来很酷"——它是更广泛的计算机视觉流程的\ **入口**。


6. 阈值选择建议
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30 30 70

   * - 场景
     - low_th
     - high_th
     - 说明
   * - 室内光照稳定
     - 50
     - 150
     - 一般情况，结果稳定
   * - 强光高对比度
     - 100
     - 200
     - 提高阈值以减少虚假边缘
   * - 低光照、有噪声
     - 30
     - 100
     - 降低阈值以保留更多细节
   * - 边缘非常模糊
     - 20
     - 80
     - 进一步降低阈值使边缘更敏感

使用滑动条快速调出一个合适的范围，然后将其作为固定值写在程序中。


7. 扩展练习
---------------------

- 在Canny输出上使用 ``cv2.findContours``\ 绘制物体边界。
- 改变高斯核大小，观察边缘精度的变化。
- 在低/高光照下尝试不同的阈值，理解双阈值的效果。
- 使用边缘图结合 ``cv2.HoughLines``（直线）或 ``cv2.HoughCircles``（圆形）进行形状检测。