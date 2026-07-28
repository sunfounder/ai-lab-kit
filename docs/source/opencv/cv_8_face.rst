.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

8. 人脸与眼睛检测
=========================================

在本章中，我们将使用Raspberry Pi的Picamera2捕获视频，并应用OpenCV的Haar特征分类器进行\ **实时人脸和眼睛检测**。
这种方法轻量且实用——非常适合初学者在Raspberry Pi上部署。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_8.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Haar特征与检测原理
-----------------------------------------

1. Haar特征的本质

Haar特征是一种经典的物体检测方法。它们编码图像区域内\ **亮度差异的模式**，以判断某个区域是否可能包含人脸、眼睛等。

典型的Haar特征示例：

- 眼睛区域通常比上方的额头暗
- 鼻梁两侧的亮度对称
- 嘴巴下方的区域常呈现清晰的边缘图案

.. image:: img/opencv_haar_f.png
   :alt: Haar特征示意图
   :align: center

OpenCV需要预训练的Haar分类器（\ ``.xml``\ 文件）。示例目录中已包含这些文件——直接加载使用即可。

2. 检测流程

   1. 使用 ``CascadeClassifier``\ 加载训练好的Haar模型
   2. 将实时视频转换为灰度图（提高效率）
   3. 使用 ``detectMultiScale``\ 检测人脸/眼睛区域
   4. 在检测到的目标周围绘制矩形

.. image:: img/opencv_haar_show.png
   :alt: 检测流程示意图
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
      python3 cv_8_haarcascade.py

   .. tip::

      我们还提供\ ``cv_8_haarcascade_video.py``\ 用于从视频文件中检测人脸和眼睛。

#. 运行程序后，将出现一个名为\ **Raspberry Pi Camera - Face Detection**\ 的窗口，并显示来自Raspberry Pi摄像头的实时画面。

   视频流中检测到的人脸用\ **黄色矩形**\ 高亮显示，每个人脸都带有标签（Face 1, Face 2, ...）。
   在每个检测到的人脸区域内，程序还会检测眼睛，并用\ **橙色矩形**\ 标记。

   检测是实时进行的，当人在摄像头前移动时，矩形会随之移动。

   要停止程序：

   * 按键盘上的 **q** 键
   * 或使用关闭按钮（X）关闭显示窗口

   退出后，摄像头停止工作，所有OpenCV窗口关闭。


3. 完整代码
-------------------


.. code-block:: python

   # Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
   import cv2
   from picamera2 import Picamera2
   from pathlib import Path

   # -----------------------------
   # Load Haar cascade classifiers
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent

   face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
   eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   # Check if cascade files are loaded correctly
   if face_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
   if eye_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   # -----------------------------
   # Initialize Picamera2
   # -----------------------------
   picam2 = Picamera2()

   # Video configuration (resolution can be adjusted)
   config = picam2.create_video_configuration(main={"size": (640, 480)})
   picam2.configure(config)
   picam2.start()

   WIN = "Raspberry Pi Camera - Face Detection"
   print("Camera started. Press 'q' to quit.")

   try:
      while True:
         # Capture a frame (Picamera2 typically provides RGB)
         frame_rgb = picam2.capture_array()

         # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
         gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

         # Improve contrast to make detection more stable under different lighting
         gray = cv2.equalizeHist(gray)

         # Detect faces
         faces = face_cascade.detectMultiScale(
               gray,
               scaleFactor=1.2,
               minNeighbors=5,
               minSize=(60, 60)
         )

         # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
         frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

         # Draw face and eye results
         for i, (x, y, w, h) in enumerate(faces, start=1):
               # Draw face rectangle + label
               cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
               cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

               # ROI for eye detection (search eyes only inside the detected face area)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = frame_bgr[y:y + h, x:x + w]

               eyes = eye_cascade.detectMultiScale(
                  roi_gray,
                  scaleFactor=1.2,
                  minNeighbors=8,
                  minSize=(20, 20)
               )

               # Draw up to 2 eyes (typical for a face)
               for (ex, ey, ew, eh) in eyes[:2]:
                  cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

         # Show the frame
         cv2.imshow(WIN, frame_bgr)

         # Handle keyboard input
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
               break

         # Exit if the user closes the window (click X)
         if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
               break

   finally:
      picam2.stop()
      cv2.destroyAllWindows()
      print("Camera stopped.")

4. 代码解释
----------------------

#. 导入所需库：

   .. code-block:: python

      import cv2
      from picamera2 import Picamera2
      from pathlib import Path

   OpenCV用于检测和绘制，Picamera2用于从Raspberry Pi摄像头捕获帧。

#. 获取当前脚本的目录：

   .. code-block:: python

      BASE_DIR = Path(__file__).resolve().parent

   这样可以从Python脚本所在的同一文件夹加载级联XML文件。

#. 加载Haar级联分类器（人脸和眼睛）：

   .. code-block:: python

      face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
      eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   Haar级联是预训练的模型，可以检测人脸和眼睛。

#. 检查级联文件是否正确加载：

   .. code-block:: python

      if face_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
      if eye_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   如果文件路径错误或文件丢失，\ ``CascadeClassifier``\ 将为空。
   这些检查有助于及早发现问题。

#. 初始化摄像头并设置分辨率：

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_video_configuration(main={"size": (640, 480)})
      picam2.configure(config)
      picam2.start()

   以640×480的视频模式启动摄像头。

#. 持续捕获帧：

   .. code-block:: python

      frame_rgb = picam2.capture_array()

   每次循环捕获一帧。Picamera2通常以RGB格式返回帧。

#. 转换为灰度图（检测速度更快）：

   .. code-block:: python

      gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

   人脸/眼睛检测在灰度图像上进行，比使用彩色图像运行速度更快。

#. 提高对比度以获得更稳定的检测：

   .. code-block:: python

      gray = cv2.equalizeHist(gray)

   直方图均衡化可以改善不同光照条件下的检测结果。

#. 在帧中检测人脸：

   .. code-block:: python

      faces = face_cascade.detectMultiScale(
          gray,
          scaleFactor=1.2,
          minNeighbors=5,
          minSize=(60, 60)
      )

   返回所有检测到的人脸矩形列表\ ``(x, y, w, h)``。

   - ``scaleFactor``\ 控制图像缩放步长（越小越精确但越慢）。
   - ``minNeighbors``\ 减少误检（越大越严格）。
   - ``minSize``\ 忽略非常小的检测结果。

#. 将RGB转换为BGR用于绘制和显示：

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

   OpenCV的绘图函数和\ ``imshow``\ 期望彩色图像使用BGR格式。

#. 绘制人脸矩形和标签：

   .. code-block:: python

      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
      cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   在每个检测到的人脸周围绘制一个框，并添加"Face 1"等标签。

#. 在每张人脸内部检测眼睛（ROI）：

   .. code-block:: python

      roi_gray = gray[y:y + h, x:x + w]
      roi_color = frame_bgr[y:y + h, x:x + w]

      eyes = eye_cascade.detectMultiScale(
          roi_gray,
          scaleFactor=1.2,
          minNeighbors=8,
          minSize=(20, 20)
      )

   ROI即"感兴趣区域"。仅在脸部区域内检测眼睛速度更快，且能减少误检。

#. 绘制最多两只眼睛：

   .. code-block:: python

      for (ex, ey, ew, eh) in eyes[:2]:
          cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

   在检测到的前两只眼睛周围绘制矩形。

#. 显示结果并处理退出：

   .. code-block:: python

      cv2.imshow(WIN, frame_bgr)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
          break

   按 ``q`` 退出，或关闭窗口以安全退出。

#. 清理资源（始终执行）：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   即使发生错误，摄像头也会停止，所有OpenCV窗口也会关闭。


5. Haar检测的优缺点
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 方面
     - 优点
     - 缺点
   * - 速度
     - 非常快；适合Raspberry Pi
     - -
   * - 精度
     - 对正面人脸效果良好
     - 对旋转和侧面敏感
   * - 光照
     - 均匀光照下表现良好
     - 过亮/过暗时性能下降
   * - 模型
     - 模型小，易于部署
     - 精度低于深度学习方法

由于轻量和快速，Haar特征在嵌入式设备上仍然非常实用。


6. 常见改进方法
----------------------

1. **光照预处理**：检测前应用直方图均衡化或CLAHE以改善低光性能。
2. **多角度检测**：同时加载正面和侧面人脸分类器以检测更多姿态。
3. **更多面部特征**：添加眼睛/嘴巴/鼻子的Haar分类器以丰富检测。
4. **使用DNN代替Haar**：OpenCV DNN + ResNet/MobileNet可以获得更高精度（但需要更多计算）。



7. 扩展练习
---------------------

- 使用 ``cv2.equalizeHist``\ 增强灰度图像，改善低光检测。
- 添加嘴巴或鼻子的Haar分类器以检测更多面部特征。
- 使用 ``cv2.VideoWriter``\ 记录检测过程。
- 结合GPIO输出制作Raspberry Pi项目："检测到人脸时点亮LED"。