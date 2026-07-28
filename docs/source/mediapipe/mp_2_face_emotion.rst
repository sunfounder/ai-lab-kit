.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_emotion:

2. 情绪检测
=======================================

-----------------------------
1. 概述
-----------------------------

在本节中，我们将扩展 Face Mesh 检测，实现基本的情绪识别。

该方法不使用深度学习模型，而是利用面部关键点几何特征（眼睛和嘴部比例）实时对表情进行分类。

.. image:: img/mp_face_emotion_happy.png
   :align: center

可识别的情绪：

- 😮 惊讶
- 😀 开心
- 😢 悲伤
- 😠 生气
- 😐 中性

-----------------------------
2. 工作原理
-----------------------------

程序按以下步骤执行：

1. 使用 ``Picamera2`` + ``MediaPipe FaceMesh`` 获取 468 个关键点。
2. 选择眼睛和嘴部周围的关键特征点。
3. 计算归一化比例：

   - 眼睛睁开度
   - 嘴部宽度
   - 嘴部张开度

4. 将数值与预设阈值进行比较。
5. 使用 OpenCV 显示检测到的情绪。

这种方法的优势：

- 快速且轻量（适用于 Raspberry Pi）
- 无需神经网络
- 易于调整阈值

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

        sudo python3 ~/ai-lab-kit/mediapipe/mp_face_emotion.py
#. 运行程序后，将打开一个视频窗口并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_2.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当摄像头前出现人脸时，系统会：

   - 实时检测 468 个面部关键点
   - 计算眼睛睁开度和嘴部张开度比例
   - 对当前面部表情进行分类

   检测到的情绪标签（如 ``Happy``、``Surprised``、``Sad``、``Angry`` 或 ``Neutral``）会显示在视频画面上。

   当用户改变面部表情时，情绪标签会实时更新。

   如果未检测到人脸，程序将继续显示正常的摄像头画面，不显示情绪标签。

   按 ``q`` 键退出程序。摄像头将停止，OpenCV 窗口将自动关闭。


-----------------------------
4. 完整代码
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   import numpy as np

   # --------- Emotion judgment auxiliary function ---------
   def euclidean(p1, p2):
       return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

   def classify_emotion(landmarks):
       """
       landmarks: results.multi_face_landmarks[0].landmark (length ~468)
       Returns (label, details_dict)
       """
       # Keypoint Index (MediaPipe 468 points)
       L_EYE_TOP, L_EYE_BOT = 159, 145
       R_EYE_TOP, R_EYE_BOT = 386, 374
       L_EYE_CENTER, R_EYE_CENTER = 33, 263
       MOUTH_LEFT, MOUTH_RIGHT = 61, 291
       LIP_UP, LIP_DOWN = 13, 14

       # Normalization scale: distance between left and right eye centers
       io = euclidean(landmarks[L_EYE_CENTER], landmarks[R_EYE_CENTER])
       if io < 1e-6:
           return "Neutral", {}

       mouth_width = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT]) / io
       mouth_open  = euclidean(landmarks[LIP_UP], landmarks[LIP_DOWN]) / io
       eye_open_L  = euclidean(landmarks[L_EYE_TOP], landmarks[L_EYE_BOT]) / io
       eye_open_R  = euclidean(landmarks[R_EYE_TOP], landmarks[R_EYE_BOT]) / io
       eye_open    = 0.5 * (eye_open_L + eye_open_R)

       # --------- Simple threshold rules (adjustable) ---------
       if mouth_open > 0.08 and eye_open > 0.055:
           label = "Surprised"
       elif mouth_width > 0.48 and mouth_open > 0.035:
           label = "Happy"
       elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
           label = "Sad"
       elif mouth_open < 0.02 and eye_open < 0.028:
           label = "Angry"
       else:
           label = "Neutral"

       details = {
           "mouth_width": round(mouth_width, 3),
           "mouth_open": round(mouth_open, 3),
           "eye_open": round(eye_open, 3),
       }
       return label, details

   # Initialize FaceMesh
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
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

       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       results = face.process(frame)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

               # --------- Emotion detection ---------
               label, metrics = classify_emotion(face_landmarks.landmark)

               # Draw emotion label on the frame
               cv2.putText(frame, f"Emotion: {label}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

               # Debug information
               dbg = f"mw:{metrics.get('mouth_width',0)} mo:{metrics.get('mouth_open',0)} eo:{metrics.get('eye_open',0)}"
               cv2.putText(frame, dbg, (20, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

运行后，摄像头画面上将实时显示识别的情绪类别，以及包括嘴部宽度、嘴部张开度、眼睛睁开度等调试信息。

-----------------------------
5. 关键步骤说明
-----------------------------

#. 选择关键点

   .. code-block:: python

      # Keypoint Index (MediaPipe 468 points)
      L_EYE_TOP, L_EYE_BOT = 159, 145
      R_EYE_TOP, R_EYE_BOT = 386, 374
      L_EYE_CENTER, R_EYE_CENTER = 33, 263
      MOUTH_LEFT, MOUTH_RIGHT = 61, 291
      LIP_UP, LIP_DOWN = 13, 14

   这些索引对应：

   - 159, 145 → 左眼上下边缘
   - 386, 374 → 右眼上下边缘
   - 33, 263 → 眼睛中心（用于归一化）
   - 61, 291 → 嘴角
   - 13, 14 → 上下唇中点

   .. image:: img/mp_face_point.jpg
      :align: center

#. 归一化距离

   为了减少摄像头距离的影响，
   使用两眼中心之间的距离作为归一化尺度。

   .. code-block:: python

      def euclidean(p1, p2):
          return np.linalg.norm(
              np.array([p1.x, p1.y]) -
              np.array([p2.x, p2.y])
          )

      io = euclidean(
          landmarks[L_EYE_CENTER],
          landmarks[R_EYE_CENTER]
      )

#. 计算几何特征

   .. code-block:: python

      mouth_width = euclidean(
          landmarks[MOUTH_LEFT],
          landmarks[MOUTH_RIGHT]
      ) / io

      mouth_open = euclidean(
          landmarks[LIP_UP],
          landmarks[LIP_DOWN]
      ) / io

      eye_open_L = euclidean(
          landmarks[L_EYE_TOP],
          landmarks[L_EYE_BOT]
      ) / io

      eye_open_R = euclidean(
          landmarks[R_EYE_TOP],
          landmarks[R_EYE_BOT]
      ) / io

      eye_open = 0.5 * (eye_open_L + eye_open_R)

   计算出的特征：

   - ``mouth_width`` → 嘴部水平宽度
   - ``mouth_open`` → 嘴部垂直张开度
   - ``eye_open`` → 平均眼睛睁开度

#. 使用阈值分类情绪

   .. code-block:: python

      if mouth_open > 0.08 and eye_open > 0.055:
          label = "Surprised"
      elif mouth_width > 0.48 and mouth_open > 0.035:
          label = "Happy"
      elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
          label = "Sad"
      elif mouth_open < 0.02 and eye_open < 0.028:
          label = "Angry"
      else:
          label = "Neutral"

   情绪规则（经验阈值）：

   - 惊讶 → 嘴和眼睛都睁大
   - 开心 → 嘴张宽，眼睛正常
   - 悲伤 / 生气 → 嘴和眼睛基本闭合
   - 中性 → 不匹配其他条件

-----------------------------------------------------
6. 阈值和鲁棒性调整
-----------------------------------------------------

- 像 ``0.08``、``0.035``、``0.018`` 这样的阈值基于 640×480 分辨率的经验值。
- 如果摄像头距离不同或分辨率不同，请使用调试信息（mw/mo/eo）调整阈值。
- 情绪判断逻辑可以修改得更复杂，或使用训练好的模型以获得更高精度，例如计算嘴角相对位置、嘴部形状等特征。

------------------------------------------------------------
7. 故障排除
------------------------------------------------------------

- 情绪识别不灵敏

  阈值可能与当前摄像头距离不匹配。
  调整 ``mouth_open`` 和 ``eye_open`` 的值。

- 检测延迟

  分辨率可能过高。
  降低分辨率或禁用 ``refine_landmarks``。

- 无法识别情绪

  光照可能不足或面部角度偏斜。
  改善光照条件并正对摄像头。

-----------------------------
8. 总结
-----------------------------

- 本章实现了基于 **几何特征 + FaceMesh 关键点** 的轻量级情绪识别。
- 具有 **高实时性** 和 **可调阈值** 的优势。
- 可用于互动艺术、人机交互、课堂/会议状态检测等项目。
