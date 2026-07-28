.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. CAMShift目标跟踪
==============================

在前一章中，我们学习了MeanShift算法，它能够基于颜色直方图在视频中持续跟踪目标。
在本节中，我们将介绍\ **CAMShift（Continuously Adaptive Mean Shift，连续自适应均值漂移）**，
它扩展了MeanShift，通过\ **自动调整窗口大小和方向**\ 使其在实际应用中更加实用。
此外，在本示例中，我们将基于\ **亮度而非颜色**\ 来跟踪目标，这在实际应用中也非常常见。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. 算法特点
---------------------

**MeanShift**\ 只能跟踪目标位置，且使用固定大小的窗口。
**CAMShift**\ 跟踪位置\ **并**\ 自动调整窗口大小和角度。

例如，当目标靠近摄像头时，跟踪框变大；远离时，跟踪框缩小；目标旋转时，跟踪框也相应旋转。

.. image:: img/opencv_camshift.png
   :alt: CAMShift跟踪示意图
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
      python3 cv_6_camshift.py

#. 运行程序后，将出现一个名为\ **CAMShift Tracker**\ 的OpenCV窗口，并开始播放视频文件\ *sample3.mp4*。

   程序使用CAMShift算法跟踪黑猫。

   被跟踪的物体周围将绘制一个绿色旋转边界框。
   随着猫移动或改变大小和方向，跟踪窗口将自动调整其位置、大小和角度。

   您可以通过两种方式退出程序：

   * 按键盘上的 **q** 键
   * 单击窗口的关闭按钮（X）

   退出后，视频播放停止，所有OpenCV窗口关闭。

3. 完整代码
---------------------

打开 ``cv_6_camshift.py``\ 查看完整代码。

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. 代码解释
---------------------------

#. 打开视频文件并读取第一帧：

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift需要初始帧来学习要跟踪的目标。

#. 设置初始跟踪窗口（ROI）：

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   此矩形应覆盖第一帧中的目标物体。
   CAMShift将在跟踪过程中自动更新此窗口。

#. 将第一帧转换为HSV并提取ROI：

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV便于跟踪，因为您可以选择特定的通道（如V通道用于亮度）。

#. 为暗色物体（低V值）构建掩膜：

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   仅保留ROI中的"暗"像素。
   对于黑色/深色物体，亮度（V）通常是最有用的特征。

#. 计算并归一化V通道的直方图：

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - 通道 ``2``\ 指HSV中的\ **V（值/亮度）**\ 通道。
   - 直方图描述了目标ROI的"暗/亮"程度。
   - 归一化使跟踪更稳定。

#. 设置CAMShift的终止条件：

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift在达到10次迭代或移动小于1个像素时停止更新。

#. 使用FPS设置播放速度：

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   设置延迟使视频播放接近其原始FPS。

#. 使用反向投影创建概率图（V通道）：

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   反向投影突出显示帧中V值与ROI直方图匹配的像素。
   ``back_proj``\ 中越亮的值表示"越可能是目标"。

#. 使用CAMShift跟踪并更新窗口：

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift基于MeanShift，但还可以适应跟踪窗口的\ **大小和旋转**。

   - ``track_window``\ 每帧更新。
   - ``rot_rect``\ 包含旋转矩形（中心、大小、角度）。

#. 绘制旋转跟踪框：

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   将旋转矩形转换为四个角点，并在帧上绘制。

#. 退出条件（键盘 + 窗口关闭）：

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   按 ``q`` 退出，或关闭窗口以安全停止。

#. 释放资源：

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   始终在结束时释放视频文件并关闭窗口。


5. CAMShift vs. MeanShift
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 特性
     - MeanShift
     - CAMShift
   * - 窗口大小
     - 固定
     - 自适应
   * - 角度
     - 不支持
     - 支持旋转
   * - 跟踪精度
     - 中等
     - 更高，更具适应性
   * - 应用
     - 静态目标
     - 复杂运动、旋转目标

CAMShift是MeanShift的升级版，
能更好地处理目标变形、旋转和距离变化——非常适合实际场景。

6. 扩展练习
-------------------------------------------

- 调整 ``inRange``\ 阈值以跟踪绿色或蓝色目标
- 结合实时摄像头输入，构建基于颜色的实时跟踪系统


7. 进阶：交互式ROI选择和自动调整HSV阈值
-------------------------------------------------------------------------

与前一节相同，本项目也可以使用鼠标交互选择ROI并自动调整HSV阈值。

运行 ``cv_6_camshift_auto.py``\ 查看修改后的代码。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

运行程序后，将显示视频的第一帧，并要求您使用鼠标选择感兴趣区域（ROI）。

拖动鼠标在目标物体周围绘制一个矩形，然后按 **Enter** 或 **Space** 确认选择。
按 **Esc** 取消选择。

选择ROI后，将出现一个名为\ **CAMShift Tracker**\ 的窗口。
选定的物体将用一个绿色旋转矩形进行跟踪，跟踪窗口将随着物体移动自动调整其位置、大小和方向。

要停止程序：

* 按键盘上的 **q** 键
* 或使用关闭按钮（X）关闭显示窗口

退出后，视频播放停止，所有OpenCV窗口关闭。


.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

   ...