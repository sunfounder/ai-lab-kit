.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_object:


10. 物体检测
===================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

除了面向人脸、手部和姿态的专业模型外，
MediaPipe 还提供了一个基于 TensorFlow Lite 的通用 **Object Detector** （物体检测器）。

本章演示如何在 Raspberry Pi 上使用
``efficientdet_lite0.tflite`` 模型
进行实时物体检测，并在摄像头画面上可视化结果。

.. image:: img/mp_object.png
   :width: 500
   :align: center

该模块可用于：

- 实时物体识别演示
- 智能家居/机器人感知
- 简单的安全监控
- 嵌入式视觉项目


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

程序执行以下步骤：

1. 初始化 MediaPipe Tasks **ObjectDetector**
   并加载 ``efficientdet_lite0.tflite`` 模型。
2. 从 Picamera2 视频流捕获帧。
3. 将每帧转换为 MediaPipe ``mp.Image`` 对象。
4. 调用 ``detect_for_video`` 进行实时物体检测。
5. 使用 OpenCV 绘制边界框和标签。
6. 限制显示检测结果的数量，以保持输出清晰
   并在 Raspberry Pi 上维持稳定的性能。

-----------------------------
3. 模型准备
-----------------------------

本示例使用 TensorFlow Lite（TFLite）格式的 **EfficientDet Lite0** 模型。

EfficientDet Lite0 轻量高效，针对
Raspberry Pi 等嵌入式设备进行了优化。
它在速度和精度之间提供了良好的平衡。

``efficientdet_lite0.tflite`` 文件包含在项目目录中，
可直接使用。

* `官方模型下载页面 <https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector#efficientdet-lite0_model_recommended>`_

如果硬件性能允许且需要更高精度，
可以切换到：

- EfficientDet Lite1
- EfficientDet Lite2

您也可以使用自己训练的 TFLite 物体检测模型替换，
只要它遵循 MediaPipe Tasks Object Detector 的格式要求即可。


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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_object.py


#. 运行程序后，一个标题为"Show Video"的窗口将打开并显示实时摄像头画面。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_10.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   对于每个视频帧，Object Detector 模型（``efficientdet_lite0.tflite``）会实时运行，并在画面中搜索可识别的物体。

   当检测到物体时：

   - 每个物体周围会绘制一个矩形边界框。
   - 边界框上方会显示标签和置信度分数，格式为 ``name: score``（例如 ``person: 0.87``）。
   - 只有高于 ``SCORE_THRESHOLD``\ （默认 0.5）的检测结果才会显示。
   - 为了保持显示清晰并维持性能，程序每帧最多绘制 ``MAX_DRAW``\ （默认 20）个检测结果。

   随着摄像头画面的变化，边界框和标签会持续实时更新。

   按 ``q`` 键退出程序。
   摄像头将停止，OpenCV 窗口将自动关闭。

-----------------------------
5. 完整代码
-----------------------------

.. code-block:: python

   # STEP 1: Import the necessary modules.
   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import time
   from pathlib import Path

   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Paths & basic settings --------------------
   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")  # Model path
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20  # Limit the number of drawn detections

   # -------------------- Helper: visualization --------------------
   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       img = bgr_image.copy()
       h, w = img.shape[:2]
       drawn = 0

       for det in detection_result.detections:
           bbox = det.bounding_box
           x1 = max(0, min(int(bbox.origin_x), w - 1))
           y1 = max(0, min(int(bbox.origin_y), h - 1))
           x2 = max(0, min(int(bbox.origin_x + bbox.width), w - 1))
           y2 = max(0, min(int(bbox.origin_y + bbox.height), h - 1))

           # top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw bounding box
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break
       return img

   # STEP 2: Initialize the detector
   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,
   )
   detector = vision.ObjectDetector.create_from_options(options)

   # STEP 3: Camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()
   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert to RGB and wrap as mp.Image
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

       # STEP 4: Detect
       ts_ms = int(time.time() * 1000)
       detection_result = detector.detect_for_video(mp_image, ts_ms)

       # STEP 5: Visualize
       annotated = visualize(frame_bgr, detection_result)

       cv2.imshow("Show Video", annotated)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

运行脚本后，摄像头画面将显示：

- 检测到的物体周围有边界框
- 分类标签和置信度分数
- 实时检测（在 Raspberry Pi 上可实现约 10~20 FPS）

-----------------------------
6. 代码说明
-----------------------------

**配置**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20

- ``SCORE_THRESHOLD`` 控制显示检测结果的最低置信度（在 Tasks 运行时内部应用）。
- ``MAX_DRAW`` 是 UI 便利参数，用于限制每帧绘制的边界框数量。

**导入**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2, numpy as np, time
   from pathlib import Path
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

- ``mediapipe.tasks.python.vision`` 包含 **ObjectDetector** Tasks API。
- 我们仍使用经典的 OpenCV 进行窗口显示和绘制。

**可视化辅助函数**

.. code-block:: python

   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       """
       Draw bounding boxes and category labels on a BGR image.
       Compatible with MediaPipe Tasks ObjectDetector's detection_result.
       """
       img = bgr_image.copy()
       h, w = img.shape[:2]

       drawn = 0
       for det in detection_result.detections:
           bbox = det.bounding_box  # (origin_x, origin_y, width, height) in pixels
           x1 = int(bbox.origin_x); y1 = int(bbox.origin_y)
           x2 = int(bbox.origin_x + bbox.width); y2 = int(bbox.origin_y + bbox.height)

           # Clamp to frame bounds (defensive)
           x1 = max(0, min(x1, w - 1)); y1 = max(0, min(y1, h - 1))
           x2 = max(0, min(x2, w - 1)); y2 = max(0, min(y2, h - 1))

           # Top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw rectangle and caption
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break

       return img

- 保持主循环简洁。
- 避免依赖不存在的"visualize"工具；直接与 Tasks 输出配合使用。

**创建 ObjectDetector**

.. code-block:: python

   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,  # VIDEO mode for streaming input
   )
   detector = vision.ObjectDetector.create_from_options(options)

- ``RunningMode.VIDEO`` 针对流式输入进行了优化，**需要时间戳**。
- Tasks 运行时内部会自动处理图像的缩放和归一化。

**摄像头设置（流式源）**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

- 640×480 是在 Raspberry Pi 上平衡帧率和精度的良好折中选择。
- Picamera2 返回 BGRA（``XRGB8888``）；我们会转换为 BGR/RGB。

**逐帧检测**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr,  cv2.COLOR_BGR2RGB)

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

   ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp
   detection_result = detector.detect_for_video(mp_image, ts_ms)

- MediaPipe 需要 **RGB** 缓冲区。
- 时间戳必须**每帧递增**；使用 ``time.time()*1000`` 对本演示来说足够。

**渲染与显示**

.. code-block:: python

   annotated = visualize(frame_bgr, detection_result)
   cv2.imshow("Show Video", annotated)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

- 辅助函数返回可直接用于 OpenCV 显示的 BGR 图像。
- 按 ``q`` 键退出循环。

**清理**

.. code-block:: python

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

始终释放摄像头并销毁窗口，以避免锁定设备。

------------------------------------------------------
7. 性能与应用
------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - 优化方向
     - 效果
     - 建议
   * - 分辨率
     - 越高图像越清晰但速度越慢
     - 640x480 已足够
   * - 模型选择
     - Lite0 ~ Lite2
     - Lite0 更快，Lite2 更精确
   * - 多物体绘制
     - 物体太多会导致延迟
     - 使用 ``MAX_DRAW`` 限制

------------------------------------------------------
8. 故障排除
------------------------------------------------------

- 没有检测结果

  如果什么都没检测到，可能是置信度阈值太高。

  尝试降低 ``SCORE_THRESHOLD``\ （例如从 0.5 降到 0.3）并重新测试。

- 帧率低

  如果视频感觉卡顿，可能是模型或分辨率对 Raspberry Pi 来说太沉重。

  使用更轻量的模型（``efficientdet_lite0.tflite``）并降低分辨率（例如 640×480 或 320×240）。关闭其他后台进程也可以提高性能。

- 检测框偏移

  如果边界框看起来偏移或超出画面，通常是坐标转换问题引起的。

  确保边界框坐标被限制在图像边界内。本示例已经对 ``x1, y1, x2, y2`` 进行了限制，以防止超出范围的绘制。

- 检测结果混乱

  如果检测到太多物体导致画面杂乱，可能难以阅读结果。

  使用 ``MAX_DRAW``\ （例如 10–20）限制绘制的检测结果数量，以保持可视化清晰稳定。

-----------------------------
9. 总结
-----------------------------

- 本章基于 MediaPipe Tasks 实现了通用物体检测；
- 使用了 EfficientDet Lite0 模型，平衡了精度和性能；
- 掌握了检测结果可视化的方法；
- 可扩展至自定义模型（例如水果、车辆、危险物品检测场景）。
