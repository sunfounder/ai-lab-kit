.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. 面部轮廓与虹膜检测
=================================================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在前面的章节中，我们实现了基本的 Face Mesh 检测
和简单的情绪识别。

本节重点介绍 MediaPipe FaceMesh 提供的详细特征连接方法：

- ``FACEMESH_CONTOURS`` — 绘制面部轮廓线
  （脸部边缘和外部特征边界）

- ``FACEMESH_IRISES`` — 绘制双眼虹膜区域

通过仅绘制轮廓和虹膜区域，可视化效果更加
清晰和轻量。这对于以下应用非常有用：

- 面部特征提取
- 眼睛追踪
- 瞳孔追踪
- 视线交互

.. image:: img/mp_face_iris.png
   :align: center

------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序执行以下步骤：

1. 初始化 MediaPipe FaceMesh 模型。
2. 从 Raspberry Pi 摄像头捕获视频帧。
3. 将图像转换为 RGB 格式（MediaPipe 所需格式）。
4. 使用 ``FACEMESH_CONTOURS`` 绘制面部轮廓线。
5. 使用 ``FACEMESH_IRISES`` 绘制虹膜关键点。
6. 仅显示关键区域以获得更清晰的可视化效果。

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

#. 运行程序后，一个标题为"Show Video"的视频窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_3.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   当摄像头前出现人脸时：

   - MediaPipe 会实时检测面部关键点。
   - 仅绘制面部轮廓线（脸部轮廓、眉毛、嘴唇等）。
   - 双眼的虹膜区域会以圆形关键点连接线突出显示。

   与完整的面部网格不同，屏幕上仅显示关键轮廓和虹膜特征，使可视化更清晰、不杂乱。

   当用户移动头部或眼睛时：

   - 轮廓线平滑跟随面部移动。
   - 虹膜关键点实时追踪眼球运动。

   如果未检测到人脸，窗口将继续显示正常的摄像头画面，不显示注释。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。

-----------------------------
4. 完整代码
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize FaceMesh model
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
   # picam2.start_preview(Preview.QTGL) # Enable if hardware preview is needed
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
            # Draw facial contours
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_CONTOURS,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            # Draw iris features
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

运行程序后，屏幕上将仅显示面部轮廓和双眼虹膜区域。

-----------------------------
5. 关键步骤说明
-----------------------------

本节代码与 :ref:`mp_face` 基本相同。

主要区别在于主循环中使用的绘制方法。
``draw_landmarks()`` 函数被调用了两次：

- 一次使用 ``FACEMESH_CONTOURS``
- 一次使用 ``FACEMESH_IRISES``

您可以注释掉任一绘制块，
观察视觉效果的差异。

------------------------------------------------------------

``FACEMESH_CONTOURS``

- MediaPipe 提供的一组连接。
- 主要绘制：

  - 外部面部轮廓
  - 眼睛边缘
  - 鼻子轮廓
  - 嘴唇轮廓

这种方法产生简化的可视化效果，
使观察面部轮廓变化更加容易。

------------------------------------------------------------

``FACEMESH_IRISES``

- 绘制双眼虹膜区域。
- 包含虹膜关键点和圆形连接线。
- 可用于：

  - 眼睛追踪
  - 瞳孔追踪
  - 视线检测

------------------------------------------------------------

``landmark_drawing_spec=None``

- 禁用单个关键点的绘制。
- 仅显示连接线，
  视觉效果更加干净。

如果您想同时显示点和线，
可以定义自定义的 ``DrawingSpec``。

------------------------------------------------------------

``drawing_styles.get_default_face_mesh_contours_style()``

- 返回默认的轮廓绘制样式。

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- 返回默认的虹膜连接线样式。


------------------------------------------------------------
6. 故障排除
------------------------------------------------------------

- 未检测到虹膜

  如果未检测到虹膜，可能是光照不足、
  人脸距离摄像头太远，
  或未启用 ``refine_landmarks``。

  改善光照条件，靠近摄像头，
  并确保在初始化 FaceMesh 时设置了 ``refine_landmarks=True``。

- 轮廓线抖动

  如果轮廓线显示不稳定，
  可能是检测置信度太低，
  或光照和头部运动影响了追踪。

  尝试提高 ``min_detection_confidence``，
  改善光照条件，并保持头部移动缓慢平稳。

- 延迟高

  如果视频响应感觉缓慢，
  可能是分辨率太高
  或 ``refine_landmarks`` 消耗了额外资源。

  降低分辨率（例如 320×240），
  或者如果不需要虹膜检测，禁用 ``refine_landmarks``。

-----------------------------
7. 总结
-----------------------------

- ``FACEMESH_CONTOURS`` 和 ``FACEMESH_IRISES`` 是 MediaPipe 提供的两种重要的连接方法。
- 与完整的面部网格绘制相比，它们更加轻量和直观，适用于实际交互场景。
- 下一章将介绍如何利用这些功能进行视线追踪和眨眼检测。
