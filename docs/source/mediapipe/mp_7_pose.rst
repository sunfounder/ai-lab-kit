.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. 人体姿态估计
====================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在实现了手部和手势识别之后，
本章介绍 **MediaPipe Pose** —
一个轻量且强大的实时人体姿态估计模块。

使用 MediaPipe Pose，我们可以实时检测 **33 个人体关键点**
并在视频画面上绘制全身骨骼。

.. image:: img/mp_pose.png
   :width: 400
   :align: center

该模块可用于：

- 动作识别
- 姿态纠正
- 健身监测
- 运动分析

------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序执行以下步骤：

1. 初始化 MediaPipe Pose 模型
   （配置模型复杂度和可选的分割功能）。
2. 使用 ``Picamera2`` 捕获视频帧。
3. 将帧转换为 RGB 格式（MediaPipe 所需格式）。
4. 运行 Pose 模型获取 33 个人体关键点。
5. 使用 OpenCV 绘制关键点和骨骼连接。
6. 实时显示带注释的视频流。

本章为更高级的人机交互和身体运动分析任务
奠定基础。


------------------------
3. 运行代码
------------------------

.. important::


   开始之前，请确保：

   * 云台已组装完成
   * 可以访问 Raspberry Pi 桌面
   * 代码包已安装
   * Fusion HAT+ 已安装并配置
   * OpenCV 已安装

   详细说明请参见 :ref:`opencv_install`。

#. 打开终端并输入以下命令：

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   如果您想将 MediaPipe Pose 应用于录制视频，可以运行以下命令：

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当人出现在摄像头前时：

   - MediaPipe Pose 会实时检测 33 个人体关键点。
   - 在视频帧上绘制全身骨骼。
   - 肩部、肘部、手腕、髋部、膝部和踝部等关键关节会用线连接。

   当人移动时：

   - 骨骼关键点会平滑跟随身体运动。
   - 骨骼会持续实时更新。

   如果启用了背景分割（``enable_segmentation=True``），
   模型会在内部计算分割遮罩，不过在本示例中
   仅显示骨骼。

   如果未检测到人，程序将仅显示正常的摄像头画面，不添加注释。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。

-----------------------------
4. 完整代码
-----------------------------

以下是一个基本的人体姿态检测程序：

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
       static_image_mode=False,  # False for processing video streams
       model_complexity=2,       # 0~2, higher is more accurate
       enable_segmentation=True, # Enable background segmentation (optional)
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Pose detection
      results = pose.process(frame_rgb)

      # Convert RGB back to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If human body is detected, draw skeleton
      if results.pose_landmarks:
         drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

运行程序后，摄像头画面将显示实时人体骨骼，包括：

- 33 个关键点
- 骨骼连接线
- 人移动时骨骼跟随运动

-----------------------------
5. 代码说明
-----------------------------

**1. 导入库**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  控制 Raspberry Pi 摄像头，基于 libcamera。

* **cv2（OpenCV）**
  用于图像颜色空间转换（BGR↔RGB）、显示窗口、绘制图形。

* **mediapipe.python.solutions.pose**
  MediaPipe 的 **Pose 模型**\ ，可检测 **33 个全身关键点**\ （头部、肩部、肘部、膝部等），并可以返回分割遮罩（人与背景）。

* **drawing_utils / drawing_styles**
  MediaPipe 内置的绘制工具和样式定义，用于绘制关键点和骨骼线。

**2. 初始化 Pose 模型**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Continuous video mode
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False``：表示输入为连续视频流，而非单张图像。首次检测后进行追踪，速度更快。通常设为 False。

* ``model_complexity=1``：模型复杂度，0=轻量，1=中等，2=高精度（较慢）。Raspberry Pi 性能允许时可设为 1 或 2。

* ``enable_segmentation=True``：输出人体分割遮罩，可区分前景人物和背景。设为 True 时，可实现背景替换、抠像等效果。此用法将在后续文档中说明：:ref:`mp_pose_segmentation`

MediaPipe Pose 返回的结果结构包括：

* ``pose_landmarks``：33 个关键点；
* ``pose_world_landmarks``：3D 世界坐标；
* ``segmentation_mask``：人体分割图。

**3. 打开摄像头**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

* 创建摄像头对象 ``Picamera2()``
* 设置分辨率 **640x480**\ ，像素格式 ``"XRGB8888"``\ （4 通道 BGRA）。
  此格式与 OpenCV 兼容性最好，省去解码步骤。
* 启动摄像头。

可选：
``picam2.start_preview(Preview.QTGL)`` 可直接在 GPU 上显示视频流窗口；此处注释掉，改用 OpenCV 的 ``imshow()``。

**4. 主循环：处理每一帧**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Capture a frame from the camera (BGRA format)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. 捕获当前帧。Picamera2 默认以 **BGRA**\ （蓝绿红+Alpha）格式返回图像。
2. 转换为 **BGR** 供后续 OpenCV 处理。

.. code-block:: python

   # Convert to RGB for MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

MediaPipe 模型**必须使用 RGB**。

* 调用 ``pose.process()`` 进行关键点检测。
* ``results`` 是一个复杂对象，可能包含：

  * ``results.pose_landmarks``：关键点（33 个点）
  * ``results.pose_world_landmarks``：3D 坐标
  * ``results.segmentation_mask``：分割遮罩

.. code-block:: python

   # Convert back to BGR for OpenCV display
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

转换回来，因为 OpenCV 的 ``imshow()`` 需要 BGR 顺序。

**5. 绘制姿态关键点**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

如果检测到人体：

* ``results.pose_landmarks``：包含每个关键点的 ``(x, y, z, visibility)``。

  * ``x, y``：归一化坐标（0~1）
  * ``z``：相对深度
  * ``visibility``：关键点置信度（0~1）

* ``draw_landmarks`` 参数说明：

   * ``frame``：要绘制的图像（BGR 格式）
   * ``results.pose_landmarks``：当前帧的人体关键点
   * ``mp_pose.POSE_CONNECTIONS``：连接规则（哪些点之间用线连接）
   * ``landmark_drawing_spec``：点绘制样式
   * ``connection_drawing_spec``：线绘制样式（可省略，使用系统默认样式）

效果：在图像上绘制骨骼（头、手臂、腿的连接）和关键点（关节位置）。

**6. 显示帧与退出逻辑**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

在 ``"Show Video"`` 窗口中显示每一帧。
按 'q' 键退出循环。

**7. 释放资源**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

停止预览、释放摄像头、关闭所有 OpenCV 窗口。

-----------------------------
6. Pose 模型介绍
-----------------------------

MediaPipe Pose 模块返回 **33 个关键点**，覆盖头部、躯干、手臂和腿等区域：

.. list-table::
   :header-rows: 1

   * - 身体部位
     - 索引
   * - 鼻子
     - 0
   * - 左/右肩
     - 11 / 12
   * - 左/右肘
     - 13 / 14
   * - 左/右手腕
     - 15 / 16
   * - 左/右髋
     - 23 / 24
   * - 左/右膝
     - 25 / 26
   * - 左/右踝
     - 27 / 28
   * - 左/右足尖
     - 31 / 32

这些点可用于\ **姿态判断**\ 、\ **动作计数**\ （如下蹲、俯卧撑、瑜伽姿势检测）等。

-----------------------------
7. 性能与调优
-----------------------------

.. list-table::
   :header-rows: 1

   * - 项目
     - 影响
     - 优化建议
   * - 分辨率
     - 更高的分辨率提高精度但也增加延迟
     - 使用 640x480 平衡性能和速度
   * - model_complexity
     - 提高识别精度但减慢计算速度
     - Raspberry Pi 推荐 1~2
   * - 分割功能
     - 增加 GPU/CPU 负载
     - 如不需要背景替换，建议禁用

------------------------------------------------------------
8. 故障排除
------------------------------------------------------------

- 未检测到人体

  如果程序运行但未检测到人，请确保整个身体在摄像头画面内。避免强逆光，改善光照条件。与摄像头保持约 1-2 米的距离效果最佳。

- 视频卡顿或延迟

  如果帧率低，尝试将分辨率降低到 640×480 或更低。设置 ``model_complexity = 1`` 以获得更好的性能。如果不需要分割功能，请禁用它，并关闭其他后台程序以释放系统资源。

- 发生段错误

  大多数段错误是由于系统架构与安装的 MediaPipe wheel 不匹配引起的。

  检查系统架构：

  .. code-block:: bash

     uname -m

  输出应为 ``aarch64``。

  如果您看到 ``armv7l`` 或 ``armhf``，说明您使用的是 32 位 Raspberry Pi OS，与官方 MediaPipe wheel 不兼容。

  您也可以在 Python 中验证：

  .. code-block:: python

     import platform
     print(platform.machine())

  结果也必须是 ``aarch64``。

- 使用 aarch64 但仍然发生段错误

  这可能是由于某些 TensorFlow Lite XNNPACK 内核与您的 MediaPipe 版本不完全兼容。

  可能的解决方案：

  - 使用 ``model_complexity = 1``\ （本教程推荐）。
  - 确保 MediaPipe 安装在正确的虚拟环境中。
  - 安装针对 Raspberry Pi 优化的 wheel 包，例如 ``mediapipe-bin``\ （PINTO0309 版本）。

- ``model_complexity = 2`` 崩溃但 ``1`` 可以工作

  复杂度 2 加载更大的模型，可能触发高级 CPU 优化。在 Raspberry Pi 上，某些优化的 TensorFlow Lite 内核可能不受完全支持。复杂度 1 可避免这些内核，在 Raspberry Pi 上通常更稳定且更快。



-----------------------------
9. 总结
-----------------------------

- 本章基于 MediaPipe Pose 实现了**实时人体骨骼检测**；
- Pose 提供 33 个关键点，可用于健身、姿态分析、动作识别等领域；
- 通过调整分辨率和模型复杂度，可在 Raspberry Pi 上流畅运行；
- 基于这些关键点，我们可以进一步开发：

  - 动作识别（如"举手"、"下蹲"）
  - 姿态评估（如"坐姿是否正确"）
  - 人体交互控制。
