.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. 手部检测
=================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在上一节中，我们使用 MediaPipe 实现了人脸检测
和关键点追踪。

本节介绍 **MediaPipe Hands** —
一个轻量且稳定的实时手部关键点检测模块。

使用该模块，我们可以：

- 同时检测最多两只手
- 识别每只手的 21 个关键点
- 实时可视化手部骨骼连接

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序按以下步骤执行：

1. 初始化 MediaPipe Hands 模型。
2. 从 Raspberry Pi 摄像头捕获帧。
3. 将图像转换为 RGB 格式（MediaPipe 所需格式）。
4. 使用 Hands 模块检测手部关键点。
5. 绘制 21 个关键点及其连接线。
6. 实时显示带注释的视频流。

该模块是以下应用的基础：

- 手势识别
- 手指计数
- 交互控制系统
- 无接触人机交互

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当一只或两只手出现在摄像头前时：

   - MediaPipe 会实时检测每只手。
   - 每只手上会识别出 21 个关键点。
   - 关键点之间用线连接，形成手部骨骼。

   如果两只手都可见，两只手都会被追踪并
   同时添加注释。

   当用户移动手或手指时：

   - 关键点会平滑跟随运动。
   - 手部骨骼实时更新。

   如果未检测到手，程序将仅显示
   正常的摄像头画面，不添加注释。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。

-----------------------------
4. 完整代码
-----------------------------

完整示例代码如下：

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

运行代码后，您将在摄像头画面中看到：

- 如果检测到一只或两只手，将显示：

  - 21 个手部关键点
  - 蓝色连接骨架
- 当手移动时，检测会实时追踪。

--------------------------------------------------------
5. MediaPipe Hands 关键点说明
--------------------------------------------------------

MediaPipe Hands 为每只手返回 **21 个关键点**，包括手腕、手掌和指尖等位置。

常见关键点包括：

.. list-table::
   :header-rows: 1

   * - 索引
     - 名称
     - 位置
   * - 0
     - WRIST
     - 手腕
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - 各手指指尖
   * - 5~17
     - 关节
     - 各手指中间关节
   * - 9
     - PALM_CENTER（近似）
     - 手掌区域

.. image:: img/mp_hand_point.png
  :width: 400
  :alt: MediaPipe Hands Landmarks Illustration
  :align: center

.. note::
   这些坐标是**归一化坐标**，可以根据图像分辨率转换为实际像素位置。
   它们可用于计算角度和距离，从而实现手势识别。

------------------------------------------------------------
6. 故障排除
------------------------------------------------------------

- 手部检测不稳定

  如果光线过暗、背景杂乱或手移动过快，手部检测可能变得不稳定。

  尝试改善光照条件，使用简单的背景，并缓慢稳定地移动手部。

- 未检测到手

  如果未检测到手，可能是摄像头角度不合适、手离摄像头太远或分辨率太低。

  调整摄像头位置，靠近摄像头，并确保分辨率至少为 640×480。

- 延迟高

  如果视频响应感觉缓慢，可能是 Raspberry Pi 负载过高或分辨率设置过高。

  降低分辨率（例如 320×240），并关闭不必要的后台进程。


-----------------------------
7. 总结
-----------------------------

- MediaPipe Hands 可在 Raspberry Pi 上实现稳定的**实时手部检测**。
- 每只手提供 21 个关键点，适用于：

  - 手势识别
  - 虚拟控制
  - 交互式 UI 控制

- 接下来，我们将基于这些关键点实现**自定义手势识别**。
