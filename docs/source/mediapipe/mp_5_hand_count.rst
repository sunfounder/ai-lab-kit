.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. 手势计数
==============================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在上一节中，我们实现了实时手部检测和关键点可视化。

本节扩展了这一功能，利用手指关键点位置
来计算抬起的手指数量（0–5）。

通过分析指尖与其对应关节的相对位置，
我们可以判断每根手指是否伸直。

.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序按以下步骤执行：

1. 初始化 MediaPipe Hands 模型。
2. 从 Raspberry Pi 摄像头捕获视频帧。
3. 实时检测 21 个手部关键点。
4. 比较指尖坐标与其近端关节。
5. 判断每根手指是否伸直。
6. 统计抬起的手指数量。
7. 在视频帧上显示结果。

这种方法：

- 轻量高效
- 适用于 Raspberry Pi
- 是手势控制和交互系统的基础

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当手出现在摄像头前时：

   - MediaPipe 会实时检测手部。
   - 在手上绘制 21 个关键点和连接线。
   - 程序分析指尖和关节的位置。
   - 计算抬起的手指数量（0–5）。

   检测到的手指数量会显示在屏幕左上角：

      Fingers: X

   当您伸直或弯曲手指时，数字会实时更新。

   如果未检测到手，则仅显示正常的摄像头画面，
   不显示手指计数。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。



-----------------------------
4. 完整代码
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

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


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

在每个循环迭代中，程序判断 5 根手指是否伸直并统计伸直的数量。例如：

- ✊ 所有手指握拳 → 计数 0
- ☝️ 食指伸直 → 计数 1
- ✌️ 食指 + 中指 → 计数 2
- 🖐️ 五指全部张开 → 计数 5

--------------------------------------------------------------
5. 检测逻辑与扩展
--------------------------------------------------------------

MediaPipe Hands 返回 21 个关键点。
我们使用指尖和关节位置来判断每根手指是否伸直。

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → 指尖索引
  （拇指=4，食指=8，中指=12，无名指=16，小指=20）

- ``finger_dips`` → 对应的近端关节
  （拇指=2，食指=6，中指=10，无名指=14，小指=18）

------------------------------------------------------------

手指计数逻辑：

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

逻辑说明：

- **拇指** → 比较 ``tip.x`` 和 ``dip.x``\ （适用于右手）。
- **其他手指** → 比较 ``tip.y`` 和 ``dip.y``。
- 如果指尖在关节上方（或外侧），则认为该手指伸直。
- 每个满足条件的手指会使计数 ``+1``。

------------------------------------------------------------

扩展提示：

- 要同时支持左右手，
  可使用 ``hands_detected.multi_handedness`` 判断手型，
  并相应地反转拇指的 x 轴比较方向。

- 此逻辑可扩展实现：

  - OK 手势识别
  - 竖拇指检测
  - 石头剪刀布交互
  - 自定义手势控制

------------------------------------------------------------
6. 故障排除
------------------------------------------------------------

- 拇指检测不准确

  拇指检测可能不准确，因为左右手的逻辑不同。拇指使用的水平比较取决于手的方向。

  使用 ``multi_handedness`` 判断检测到的手是左手还是右手，并相应调整拇指检测逻辑。

- 检测不稳定

  如果手指计数显示不稳定，可能是光照不足或背景杂乱。

  改善光照条件并使用简单的背景以提高检测稳定性。

- 延迟高

  如果响应感觉缓慢，可能是分辨率太高或 CPU 负载过高。

  降低分辨率（例如 320×240），关闭不必要的后台进程。如有需要，也可简化手指计数逻辑。


-----------------------------
7. 总结
-----------------------------

- 使用 MediaPipe Hands，我们可以快速实现**实时手势识别**。
- 本节实现了基于指尖位置的**数字手势计数**，为自定义手势识别奠定了基础。
- 通过适配左右手和扩展判断规则，可以实现更复杂的交互场景。
