.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. MeanShift目标跟踪
===============================

MeanShift是一种经典的基于直方图的目标跟踪算法。
在本课中，我们不仅将实现一个完整的\ **MeanShift跟踪**\ 示例，还将解释\ **为什么**\ 要执行每一步以及\ **底层发生了什么**。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. 什么是MeanShift？
-------------------------

MeanShift根据概率密度迭代移动窗口，以\ **找到目标最可能的位置**。

通俗地说：
您首先给算法一个"初始目标区域"。它计算该区域的颜色特征（例如目标的颜色直方图），然后在后续的每一帧中找到与该颜色最相似的区域，并将矩形移动到那里。

这个过程不依赖深度学习，也不需要预训练——非常轻量。

.. image:: img/opencv_meanshift.png
   :alt: MeanShift跟踪
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
      python3 cv_5_meanshift.py

#. 运行程序后，将出现一个名为\ **MeanShift Tracker**\ 的OpenCV窗口，并开始播放视频文件\ ``sample2.mp4``。

   目标物体周围将绘制一个绿色矩形，并使用MeanShift跟踪算法实时更新。

   跟踪窗口将随着物体在视频中的移动而移动。

   您可以通过两种方式退出程序：

   * 按键盘上的 **q** 键
   * 单击窗口的关闭按钮（X）

   退出后，视频播放停止，所有OpenCV窗口关闭。

3. 完整代码
-----------------------

以下是完整的MeanShift跟踪脚本（\ ``cv_5_meanshift.py``\ ）：

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. 代码解释
---------------------------

#. 打开视频文件：

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   创建视频捕获对象，使OpenCV能够从文件中读取帧。

#. 读取第一帧并确保其有效：

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   MeanShift跟踪需要初始帧来学习要跟踪的目标。

#. 设置初始跟踪窗口（要跟踪的物体）：

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   这个矩形是目标（ROI）的起始位置。
   您通常需要调整这些值以匹配第一帧中的物体。

#. 将第一帧转换为HSV并提取ROI：

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV常用于跟踪，因为色相通道比RGB/BGR更能一致地描述颜色。

#. 构建掩膜以忽略ROI中的弱/无效像素：

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   过滤掉饱和度/亮度非常低的像素（通常是阴影或噪点），提高跟踪稳定性。

#. 计算并归一化ROI直方图（色相通道）：

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - 直方图描述了目标的颜色分布（色相）。
   - 归一化使直方图在不同光照或ROI大小下保持一致的尺度。

#. 定义MeanShift的终止条件：

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift将在以下任一条件满足时停止：
   - 运行了15次迭代，或
   - 窗口移动小于2个像素。

#. 根据视频FPS设置播放延迟：

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   使播放速度接近原始视频速度。
   如果无法读取FPS，则回退到30 FPS。

#. 将每帧转换为HSV（用于跟踪）：

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   在HSV中执行跟踪，以便匹配目标的色相直方图。

#. 反向投影（找到目标颜色可能存在的位置）：

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   反向投影生成概率图：明亮的区域更可能匹配ROI直方图。

#. 使用MeanShift更新跟踪窗口：

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift将跟踪窗口移向概率图中密度最高的区域，逐帧更新目标位置。

#. 绘制跟踪结果：

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   在视频帧上绘制当前的跟踪矩形。

#. 显示窗口和退出条件：

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - 按 ``q`` 退出。
   - 关闭窗口也会安全退出。

#. 释放资源：

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   始终释放视频并关闭窗口以释放系统资源。

5. MeanShift vs. CAMShift
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 特性
     - MeanShift
     - CAMShift
   * - 窗口大小
     - 固定
     - 自动调整（自适应目标缩放）
   * - 旋转目标
     - 不支持
     - 支持
   * - 适用场景
     - 目标尺寸相对稳定
     - 目标可能缩放/旋转
   * - 应用
     - 简单跟踪、球体、标记
     - 实际跟踪、监控、识别


6. 进阶：使用鼠标选择ROI
--------------------------------------

之前，我们使用了固定值：

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

这样虽然简单，但不够灵活。
如果您切换视频或目标在其他位置，就需要修改代码。

OpenCV提供了 ``cv2.selectROI``，让您可以在\ **第一帧上使用鼠标交互式选择目标区域**，程序将自动获取\ ``(x, y, w, h)``。

**修改后的初始化代码**

运行 ``cv_5_meanshift_auto.py``\ 查看修改后的代码。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

运行程序后，将显示视频的第一帧，并要求您使用鼠标选择感兴趣区域（ROI）。

拖动鼠标在目标物体周围绘制一个矩形，然后按 **Enter** 或 **Space** 确认选择。
按 **Esc** 取消选择。

确认ROI后，将出现一个名为\ **MeanShift Tracker**\ 的窗口。
选定的物体将用一个绿色边界框进行跟踪，框会随着物体在视频中移动而移动。

要停止程序：

* 按键盘上的 **q** 键
* 或使用关闭按钮（X）关闭显示窗口

退出后，视频播放停止，所有OpenCV窗口关闭。

.. image:: img/opencv_meanshift_mouse.png
   :alt: 交互式ROI选择窗口
   :align: center

**注意**

``cv2.selectROI``\ 是OpenCV内置的交互式ROI选择器——非常适合手动初始化。
它返回\ ``(x, y, w, h)``，与\ ``track_window``\ 完全兼容，因此您无需更改主要的CAMShift/MeanShift逻辑。
这让您可以在不同的视频和目标上重用相同的程序。


7. 进阶二：动态计算ROI的HSV阈值
--------------------------------------------------------------

原始的\ ``cv_5_meanshift.py``\ 使用手动设置的HSV阈值，适用于目标颜色固定且光照稳定的情况。

.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

如果光照变化显著或目标颜色不固定，硬编码的\ ``inRange``\ 范围可能不是最优的。
更智能的方法是\ **从选定的ROI自动计算HSV的上下限**。

**示例：自动计算HSV阈值**

运行 ``cv_5_meanshift_auto.py``\ 查看修改后的代码。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

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


当选择非常暗或非常亮的目标时，您不再需要手动调整阈值；它也能快速适应不同的光照和颜色。

.. note::

   - ``np.percentile``\ （5%–95%）裁剪ROI内的极端值（边缘、阴影、高光等），提高了鲁棒性。
   - ``pad_h``、``pad_s``、``pad_v``\ 提供容差范围，使轻微的颜色偏移仍能被捕获。
   - ``lower``\ 和\ ``upper``\ 是动态的HSV边界，直接与\ ``cv2.inRange``\ 一起使用。


**总结**

- 使用 ``cv2.selectROI``\ 实现灵活的目标初始化。
- 使用 ``np.percentile``\ 自动计算HSV边界以提高适应性。
- 结合 ``cv2.inRange``\ 和CAMShift/MeanShift，这种方法在具有挑战性的光照和目标变化下仍能保持稳定。