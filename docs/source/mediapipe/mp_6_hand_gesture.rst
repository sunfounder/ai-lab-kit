.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_gesture:


6. 手势识别器
==========================================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在上一章中，我们使用 MediaPipe Hands
获取了 21 个手部关键点并可视化了手部骨骼。

本章介绍 **MediaPipe Tasks – Gesture Recognizer**，
它可以直接输出语义手势标签，例如：

- ``Thumb_Up``
- ``Open_Palm``
- ``Victory``
- ``Closed_Fist``

通过结合：

- ``Picamera2`` 进行视频采集
- ``MediaPipe Hands`` 进行关键点可视化
- ``Gesture Recognizer`` 进行分类

我们可以实现实时手势识别，
同时显示骨骼渲染和标签。

.. image:: img/mp_hang_gesture.png
   :alt: Gesture Recognizer
   :align: center


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序执行以下步骤：

1. 使用 ``Picamera2`` 捕获视频帧。
2. （可选）使用 ``MediaPipe Hands`` 绘制关键点。
3. 在 ``VIDEO`` 模式下使用 **MediaPipe Tasks – Gesture Recognizer**。
4. 对于检测到的每只手，获取：

   - 手势类别列表（标签 + 置信度）
   - 左右手信息（Left / Right）
   - 归一化关键点

5. 选择排名第一的手势，并在对应手的
   上方绘制"标签 + 置信度分数"。

.. note::

   本章使用 MediaPipe **Tasks API（0.10+）**。


------------------------------------------------------------
3. 模型
------------------------------------------------------------

Gesture Recognizer 需要一个模型文件：

``gesture_recognizer.task``

该模型文件已包含在示例目录中。
请使用提供的版本。

内置模型支持以下手势标签：

- 0 → ``Unknown``
- 1 → ``Closed_Fist``
- 2 → ``Open_Palm``
- 3 → ``Pointing_Up``
- 4 → ``Thumb_Down``
- 5 → ``Thumb_Up``
- 6 → ``Victory``
- 7 → ``ILoveYou``

------------------------
4. 运行代码
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_gesture.py

#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_6.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当一只或两只手出现在摄像头前时，程序会：

   - 实时检测并绘制 21 个手部关键点和连接线（手部骨骼）。
   - 在每帧上运行 Gesture Recognizer 模型以对手势进行分类。

   如果识别到的手势分数超过 ``SCORE_THRESHOLD``（默认 0.5），程序会在对应手附近显示标签，包括：

   - 左右手信息（Left/Right）
   - 手势名称（例如 ``Thumb_Up``、``Open_Palm``、``Victory``）
   - 置信度分数（例如 ``0.87``）

   还会在手部区域周围绘制一个细边框，使标签位置更清晰。

   当您改变手部姿势时，手势标签和分数会持续实时更新。

   如果未检测到手，或手势置信度低于阈值，则仅显示手部骨骼（或原始摄像头画面），不显示手势标签。

   按 ``q`` 键退出程序。摄像头将停止，OpenCV 窗口将自动关闭。


-----------------------------
5. 完整代码
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Import MediaPipe Tasks (Gesture Recognizer)
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   from pathlib import Path

   # --------------------- Settings ---------------------
   BASE_DIR = Path(__file__).resolve().parent
   GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")  # Path to the gesture model
   SCORE_THRESHOLD = 0.5                           # Show gestures above this score
   # ---------------------------------------------------

   # Initialize the Hands model (kept for landmark drawing)
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

   # Initialize Gesture Recognizer (VIDEO mode for streaming)
   BaseOptions = python.BaseOptions
   GestureRecognizerOptions = vision.GestureRecognizerOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=GESTURE_MODEL_PATH)
   gr_options = GestureRecognizerOptions(
       base_options=base_options,
       running_mode=RunningMode.VIDEO
   )
   recognizer = vision.GestureRecognizer.create_from_options(gr_options)

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # (Optional) helper to draw a label near a hand bounding box computed from landmarks
   def draw_gesture_label(frame_bgr, norm_landmarks, text, color=(0, 175, 255)):
       """
       norm_landmarks: list of 21 normalized landmarks (x,y in [0,1]).
       We compute a tight bbox to place the gesture text.
       """
       if not norm_landmarks:
           return
       h, w = frame_bgr.shape[:2]
       xs = [int(lm.x * w) for lm in norm_landmarks]
       ys = [int(lm.y * h) for lm in norm_landmarks]
       x1, y1 = max(0, min(xs)), max(0, min(ys))
       x2, y2 = min(w-1, max(xs)), min(h-1, max(ys))
       cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)
       (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
       y_text = max(0, y1 - th - 6)
       cv2.rectangle(frame_bgr, (x1, y_text), (x1 + tw + 6, y_text + th + 6), color, -1)
       cv2.putText(frame_bgr, text, (x1 + 3, y_text + th + 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert the frame from BGR to RGB (required by MediaPipe)
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # ---- A) Run legacy Hands (for landmark drawing you already have) ----
       hands_detected = hands.process(frame_rgb)

       # ---- B) Run Gesture Recognizer (direct gesture labels) ----
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
       ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
       gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

       # Convert the frame back from RGB to BGR (required by OpenCV)
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # If hands are detected, draw landmarks and connections on the frame
       if hands_detected.multi_hand_landmarks:
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

       # ---- C) Overlay gesture names on top of each detected hand ----
       if gesture_result and getattr(gesture_result, "gestures", None):
           for i, gesture_list in enumerate(gesture_result.gestures):
               if not gesture_list:
                   continue
               top = gesture_list[0]
               label = top.category_name  # e.g., "Thumb_Up"
               score = top.score or 0.0
               if score < SCORE_THRESHOLD:
                   continue

               hand_label = ""
               if gesture_result.handedness and i < len(gesture_result.handedness):
                   if gesture_result.handedness[i]:
                       hand_label = gesture_result.handedness[i][0].category_name or ""

               text = f"{hand_label} {label} ({score:.2f})".strip()

               hand_lms = None
               if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
                   hand_lms = gesture_result.hand_landmarks[i]

               if hand_lms:
                   draw_gesture_label(frame, hand_lms, text)
               else:
                   cv2.putText(frame, text, (20, 40 + 30*i),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

       # Display the frame with annotations
       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   # Release the camera
   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

运行脚本后，窗口将显示手部骨骼（可选）和手势文本框。当识别到与模型类别匹配的手势时，会在对应手的边界框上方显示：

- 左右手信息（handedness）
- 手势名称（例如 ``Thumb_Up``）
- 置信度分数（0~1）

-----------------------------
6. 代码说明
-----------------------------

本示例结合了两部分：

- **Hands（Solutions API）**：用于绘制手部骨骼（21 个关键点 + 连接）。
- **Gesture Recognizer（Tasks API）**：用于预测手势标签，如 ``Thumb_Up`` 或 ``Open_Palm``。

**高级流程**

#. 初始化 Hands 用于关键点绘制（可选，但有助于可视化）。
#. 加载 Gesture Recognizer 模型（``gesture_recognizer.task``）并启用 ``VIDEO`` 模式。
#. 启动摄像头并在循环中处理帧：

   - 将帧转换为 RGB（MediaPipe 需要 RGB）。
   - 运行 Hands 绘制骨骼。
   - 运行 Gesture Recognizer 获取每只手的 ``label + score``。
   - 在对应手附近绘制标签。

#. 按 ``q`` 键退出并释放资源。

**需要理解的关键点**

- 模型文件

  Gesture Recognizer 需要 ``gesture_recognizer.task``。确保模型文件与脚本放在同一文件夹中（或更新路径）。

- VIDEO 模式需要时间戳

  ``recognize_for_video()`` 需要一个持续递增的毫秒级时间戳。在本示例中，我们使用 OpenCV 的 tick 时间生成。

- 使用置信度阈值显示标签

  只有分数 >= ``SCORE_THRESHOLD`` 的手势才会显示。这避免了显示不稳定的预测结果。

-----------------------------
7. 参数与调优
-----------------------------

.. list-table::
   :header-rows: 1

   * - 参数
     - 说明
     - 建议
   * - ``SCORE_THRESHOLD``
     - 低于此分数的手势将被忽略
     - 提高可减少误报；降低可提高召回率
   * - ``max_num_hands``
     - 同时检测的手的数量
     - 2 足以应对大多数场景
   * - ``running_mode=VIDEO``
     - 视频流模式，需要时间戳
     - 保持使用（流式识别更稳定）
   * - 分辨率
     - 影响速度和精度
     - 在 Raspberry Pi 上推荐 640×480 或更低以获得更好 FPS

-------------------------------------------------------
8. 故障排除
-------------------------------------------------------

- ``FileNotFoundError: gesture_recognizer.task``

  这通常意味着模型文件路径错误。
  确保模型文件与脚本放在同一目录中，
  或相应更新 ``GESTURE_MODEL_PATH``。

- ``ImportError: cannot import name 'vision'``

  此错误表明 MediaPipe 版本过旧。
  使用以下命令将 MediaPipe 升级到 0.10 或更高版本：

  ``pip install --upgrade mediapipe``

- 识别的类别与预期不符

  模型类别集可能不同，或光照条件影响识别。
  尝试改善光照、简化背景，
  或切换到不同的模型版本。

- 帧率低

  Raspberry Pi 性能可能有限。
  降低分辨率、禁用骨骼绘制，
  或关闭不必要的后台进程。

-----------------------------
9. 总结
-----------------------------

- **Gesture Recognizer** 可在 Raspberry Pi 上实现实时语义手势识别；
- 结合 **Hands** 骨骼渲染，既直观又易于调试；
- 通过调整阈值和分辨率，可以在"稳定性/速度"之间取得平衡；
- 未来的可能性：

  - 将不同手势映射到特定命令（快捷键、GPIO 控制等）；
  - 为特定场景训练自定义手势模型。
