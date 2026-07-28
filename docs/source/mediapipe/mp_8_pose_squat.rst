.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. 深蹲计数器
==============================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在上一章中，我们实现了基本的人体姿态估计。
本章在此基础上，使用 MediaPipe Pose 实现一个简单的
**深蹲计数器**。

这是一个结合了以下要素的实用示例：

- 姿态检测
- 动作识别
- 实时计数

它可用于智能健身系统、
家庭健身助手或运动分析应用。

.. image:: img/mp_pose_s2.png
   :alt: Squat Count Example
   :align: center


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

深蹲计数器使用以下逻辑实现：

1. 使用 MediaPipe Pose 检测 33 个人体关键点。
2. 选择关键关节（肩部、髋部、踝部）。
3. 使用归一化的 y 坐标估计髋部高度。
4. 定义上下阈值（例如 0.55 和 0.45）。
5. 使用简单的状态机检测转换：
   "站立 → 下蹲 → 站立"。
6. 当完成一个完整的深蹲周期时，计数器增加。
7. 在屏幕上显示深蹲次数和当前髋部值。

.. note::

   - 本示例不使用关节角度计算。
   - 它依赖归一化坐标来减少计算量。
   - 该方法轻量级，适用于 Raspberry Pi。

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_8.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当人站在摄像头前时：

   - MediaPipe Pose 会实时检测 33 个人体关键点。
   - 在屏幕上绘制全身骨骼。
   - 系统持续计算相对髋部位置（HipRel）。

   当您做深蹲时：

   - 当您下蹲且髋部超过下阈值（DOWN_TH）时，
     系统标记您处于"底部"位置。
   - 当您站起且髋部超过上阈值（UP_TH）时，
     深蹲计数器增加 1。

   屏幕上显示：

   - ``Squats: N`` — 完成的深蹲总数。
   - ``HipRel: value`` — 用于检测的当前归一化髋部位置。

   计数器仅在一个完整的运动周期
   （站立 → 下蹲 → 站立）完成后才增加，防止重复计数。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。


-----------------------------
4. 完整代码
-----------------------------

以下是完整的深蹲计数器实现：

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

执行脚本后，系统将：

- 检测人体骨骼；
- 计算相对髋部位置；
- 当完成从"下蹲"到"站起"的完整周期时，计数 +1；
- 在屏幕上实时显示 **Squats: N** 和当前的 HipRel 值。

-----------------------------------------------
5. 坐标与状态设计
-----------------------------------------------

我们使用以下 6 个关键点（每侧 3 个）：

.. list-table::
   :header-rows: 1

   * - 关键点
     - 索引
     - 说明
   * - 肩部
     - 11（左）/ 12（右）
     - 上部参考
   * - 髋部
     - 23（左）/ 24（右）
     - 计算深蹲位置的核心
   * - 踝部
     - 27（左）/ 28（右）
     - 下部参考

.. image:: img/mp_pose_s1.png
   :alt: MediaPipe Pose Keypoints
   :align: center

**髋部相对位置** 的计算公式：

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- hip_rel 越大表示越接近地面（即正在下蹲）。
- hip_rel 越小表示站得越直。

我们定义两个阈值：

- **DOWN_TH = 0.55**：认为已进入深蹲底部
- **UP_TH = 0.45**：认为已恢复站立

使用简单的状态机进行可靠计数：

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
6. 参数调优与优化
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - 参数
     - 说明
     - 调整建议
   * - DOWN_TH
     - 深蹲动作阈值
     - 值越高需要蹲得更深才计数
   * - UP_TH
     - 站起动作阈值
     - 值越低需要站得更直
   * - model_complexity
     - 姿态模型复杂度
     - 使用 1 以获得更快速度
   * - 分辨率
     - 影响帧率和精度
     - 推荐 640×480

.. tip::
   对于不同身高的人，可以使用自适应阈值或个性化校准以获得更准确的计数。

---------------------------------------------------------
7. 故障排除
---------------------------------------------------------

- 计数不准确

  如果深蹲计数不准确，阈值可能与您的身体位置或摄像头角度不匹配。

  尝试实时打印 ``hip_rel`` 的值，并相应调整 ``DOWN_TH`` 和 ``UP_TH``。
  同时确保您的深蹲动作一致且清晰可见。

- 未检测到人

  如果未检测到身体，请改善光照条件，避免复杂的背景。

  确保您完全站在画面内并正对摄像头。

- 延迟高

  如果视频响应缓慢，请将 ``model_complexity`` 降低到 1，并降低摄像头分辨率（例如 640×480 或 320×240）。

  关闭不必要的后台程序以提高性能。

-----------------------------
8. 总结
-----------------------------

- 使用 Pose 关键点 + 状态机实现了**实时深蹲计数器**；
- 无需复杂的角度计算，运行效率高；
- 适用于 Raspberry Pi 或其他边缘设备应用；
- 未来可扩展：

  - 俯卧撑/仰卧起坐检测
  - 数据记录与可视化
  - 自动节奏指导和训练反馈
