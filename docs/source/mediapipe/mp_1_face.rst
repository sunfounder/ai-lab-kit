.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. 人脸检测
==========================

本节介绍如何在 **Raspberry Pi** 上使用 **MediaPipe Face Mesh** 模块进行实时人脸检测和人脸关键点网格绘制。

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe 是 Google 开发的跨平台机器学习流水线框架，支持对视频流和图像进行实时处理。Face Mesh 模块是 MediaPipe 提供的用于实时人脸检测和关键点追踪的模型，可用于构建各种人脸识别和交互应用。

与 OpenCV 的 Haar 检测相比，MediaPipe 使用深度学习模型进行检测，具有以下优势：

-  更高的精度
-  对光照和角度具有更好的鲁棒性
-  支持人脸关键点追踪（468 个点）
-  与 OpenCV 无缝集成，可直接在视频流上绘制检测结果。

------------------------
1. 运行代码
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. 运行脚本后，OpenCV 会打开一个标题为"Show Video"的窗口，显示 Raspberry Pi 摄像头捕获的实时视频流。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   * 如果摄像头前出现人脸，程序会检测到人脸并实时绘制详细的人脸关键点网格。当人移动、眨眼或改变表情时，网格会平滑地跟随面部运动。
   * 如果未检测到人脸，窗口将继续显示正常的摄像头画面，不显示任何关键点。

   视频流将持续运行，直到用户退出程序。
   按键盘上的 ``q`` 键可退出程序。
   摄像头将停止，所有 OpenCV 资源将被自动释放。

------------------------
2. 代码示例
------------------------

完整代码如下所示：

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the mp_face_mesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,          # Set to False for video streams
       max_num_faces=1,                  # Maximum number of faces to detect
       refine_landmarks=True,           # Whether to refine landmarks
       min_detection_confidence=0.5     # Detection confidence threshold
   )

   # Open Raspberry Pi camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 → BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert BGR to RGB (MediaPipe requires RGB)
       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # Face detection and landmark tracking
       results = face.process(frame)

       # Convert RGB back to BGR (for OpenCV display)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       # Draw detected facial landmarks
       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

运行程序后，您将看到实时摄像头画面，检测到人脸时会自动绘制面部网格。

-----------------------------
3. 关键步骤说明
-----------------------------

#. 导入库

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   这些库用于：

   - 控制 Raspberry Pi 摄像头
   - 处理和显示图像
   - 检测人脸关键点

#. 初始化 FaceMesh

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   这会创建人脸检测模型。
   它在视频模式下持续追踪一张人脸。

#. 启动摄像头

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   摄像头以 640×480 分辨率开始流式传输。

#. 在循环中捕获帧

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   每次循环捕获一帧并转换格式以供 OpenCV 使用。

#. 检测人脸关键点

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   将帧转换为 RGB。
   MediaPipe 分析图像并检测人脸关键点。

#. 绘制人脸网格

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   如果检测到人脸，则在其上绘制网格。

#. 显示结果并退出

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   按 ``q`` 键停止程序。
   摄像头将自动关闭。

---------------------------------------------
4. 常见问题与故障排除
---------------------------------------------

* 摄像头无法打开

  * 确保 CSI 摄像头线缆已正确插入
  * 启用摄像头接口：

    ``sudo raspi-config`` → Interface Options → Camera

  * 启用后重新启动 Raspberry Pi

* 程序启动缓慢

  首次运行会加载 MediaPipe 模型，可能需要几秒钟。
  这属于正常现象，后续运行会更快。

* 检测不稳定 / 卡顿

  * 降低摄像头分辨率（例如 320×240）
  * 禁用 ``refine_landmarks`` 以减少 CPU 占用
  * 关闭其他正在运行的程序

* 找不到模块 ``mediapipe``

  安装 MediaPipe：

  .. code-block:: bash

     pip install mediapipe

  请确保使用的是 64 位 Raspberry Pi OS 系统。

-----------------------------
5. 总结
-----------------------------

- MediaPipe FaceMesh 使用深度学习模型，在 Raspberry Pi 上实现高精度人脸检测
- 与 OpenCV 的集成非常紧密
- 适用于表情识别、虚拟形象追踪、AR 应用等场景
- 相比传统的 Haar 特征检测，更加鲁棒且易于扩展

下一节将进一步介绍 **如何使用 Face Mesh 关键点** 进行简单的面部特征分析和交互。
