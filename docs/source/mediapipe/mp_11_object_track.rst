.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. 使用云台摄像头进行物体追踪
=========================================================

------------------------------------------------------------
1. 概述
------------------------------------------------------------

在本章中，我们扩展 MediaPipe 物体检测功能，
构建一个使用云台舵机平台的简单**物体追踪系统**。

该系统检测指定的目标物体
（例如"香蕉"）
并自动调整两个舵机，
使物体保持在摄像头画面中心。

.. image:: img/mp_object_track.png
   :width: 500
   :align: center

该项目结合了：

- 实时物体检测
- 舵机电机控制
- 比例追踪逻辑
- 视觉反馈叠加

它展示了计算机视觉如何实时直接驱动
物理硬件。


------------------------------------------------------------
2. 工作原理
------------------------------------------------------------

追踪系统按以下步骤执行：

1. 将水平和垂直舵机初始化到中心位置。
2. 配置 Raspberry Pi 摄像头进行视频流式传输。
3. 加载 EfficientDet Lite0 模型用于物体检测。
4. 使用 MediaPipe Tasks 检测每帧中的物体。
5. 识别目标物体（例如"banana"）。
6. 计算物体相对于画面中心的偏移量。
7. 使用比例控制调整舵机角度。
8. 在屏幕上显示追踪引导线和状态。

本示例展示了基于视觉的反馈
如何动态控制硬件运动。

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

       sudo python3 ~/ai-lab-kit/mediapipe/mp_track_object.py

#. 运行程序后，摄像头窗口打开并开始实时物体检测。

   .. raw:: html

         <video width="300" loop muted controls>
             <source src="../_static/video/object_tracking.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   系统会搜索指定的目标物体（默认：``banana``）。
   屏幕中心会显示一个黄色十字准星作为参考点。

   当目标物体出现在画面中时：

   - MediaPipe 使用 EfficientDet Lite0 模型检测物体。
   - 计算检测到的边界框的中心。
   - 如果物体位于中心死区之外，水平和垂直舵机会逐步移动。
   - 摄像头物理旋转，使物体保持在画面中心附近。
   - 物体周围会绘制一个绿色追踪框。
   - 屏幕显示：

     - ``Tracking banana``（状态）
     - 当前舵机角度（Pan / Tilt）

   当未检测到物体时：

   - 舵机停止移动。
   - 状态文本变为 ``No banana found``（以红色显示）。

   追踪逻辑使用简单的 4 方向死区控制：
   只有当物体距离中心足够远时舵机才移动，
   防止抖动。

   按 ``q`` 键停止程序。

   退出时：

   - 两个舵机回到中心位置。
   - 摄像头停止。
   - 显示窗口关闭。
   - 打印消息：``Tracking stopped. Servos centered.``

-----------------------------
4. 完整代码
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3

   import cv2
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2
   from pathlib import Path

   # MediaPipe imports
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Configuration --------------------
   TARGET = "banana"      # Object to track
   W, H = 640, 480           # Camera resolution
   CX, CY = W // 2, H // 2   # Center coordinates
   SCORE_THRESHOLD = 0.3     # Detection confidence threshold
   DEADZONE = 50             # Pixels from center before moving

   print(f"Tracking: {TARGET}")

   # -------------------- Servo Initialization --------------------
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)     # Allow servos to reach position

   # -------------------- Camera Initialization --------------------
   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))
   cam.start()
   time.sleep(2)     # Allow camera to stabilize

   # -------------------- MediaPipe Detector Setup --------------------
   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")

   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

   detector = vision.ObjectDetector.create_from_options(options)

   print("Ready. Press 'q' to quit")

   # -------------------- Tracking Logic --------------------
   def simple_track(x, y):
       """Basic 4-direction tracking with deadzone"""
       if x is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Left/right movement decision
       if x < CX - DEADZONE:
           pan_move = 1          # Move right
       elif x > CX + DEADZONE:
           pan_move = -1         # Move left

       # Up/down movement decision
       if y < CY - DEADZONE:
           tilt_move = -1        # Move down
       elif y > CY + DEADZONE:
           tilt_move = 1         # Move up

       return pan_move, tilt_move

   # -------------------- Main Tracking Loop --------------------
   pan_pos = 0   # Current pan angle (-90° to +90°)
   tilt_pos = 0  # Current tilt angle (-45° to +45°)

   try:
       while True:
           # Capture frame from camera
           frame = cam.capture_array()
           frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

           # Convert to RGB for MediaPipe
           rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

           # Detect objects in frame
           detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

           # Search for target object
           obj_x = obj_y = None
           for detection in detections.detections:
               for category in detection.categories:
                   # Case-insensitive search for target
                   if TARGET.lower() in str(category.category_name).lower():
                       bbox = detection.bounding_box
                       # Calculate object center
                       obj_x = bbox.origin_x + bbox.width // 2
                       obj_y = bbox.origin_y + bbox.height // 2
                       break

           # Process tracking if object found
           if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move

               # Limit servo angles to safe ranges
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))

               # Send commands to servos
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)

               # Draw tracking box around object
               cv2.rectangle(frame,
                            (obj_x - 30, obj_y - 30),
                            (obj_x + 30, obj_y + 30),
                            (0, 255, 0), 2)
               status = f"Tracking {TARGET}"
               color = (0, 255, 0)  # Green for tracking
           else:
               status = f"No {TARGET} found"
               color = (0, 0, 255)  # Red for not found

           # Draw center crosshair for reference
           cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
           cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

           # Display status information
           cv2.putText(frame, status, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
           cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                      (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
           cv2.putText(frame, "Press 'q' to quit", (10, 90),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

           # Show video window
           cv2.imshow(f"Track: {TARGET}", frame)

           # Exit on 'q' key press
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break

   finally:
       # -------------------- Cleanup --------------------
       pan.angle(0)      # Return to center
       tilt.angle(0)     # Return to center
       time.sleep(0.5)   # Allow movement
       cam.stop()        # Stop camera
       cv2.destroyAllWindows()  # Close display
       print("Tracking stopped. Servos centered.")

-----------------------------
5. 代码说明
-----------------------------

**配置部分**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET``：要追踪的物体类别（必须是 COCO 数据集中的类别）；
- ``W, H``：摄像头分辨率——在速度和细节之间取得平衡；
- ``CX, CY``：画面中心坐标，用作追踪参考；
- ``SCORE_THRESHOLD``：有效检测的最低置信度；
- ``DEADZONE``：舵机开始移动前与中心的距离（减少抖动）。

**舵机初始化**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` 和 ``Servo(3)`` 对应 Fusion HAT 上的通道；
- ``.angle(0)`` 将舵机居中在 0° 位置；
- ``time.sleep(1)`` 确保舵机在继续前到达位置。

**摄像头设置**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- 使用 Picamera2 库实现现代摄像头 API；
- ``XRGB8888`` 格式提供 8 位颜色通道；
- ``time.sleep(2)`` 允许摄像头传感器稳定。

**MediaPipe 检测器**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- 从同一目录加载 EfficientDet Lite0 模型；
- ``RunningMode.VIDEO`` 针对连续帧处理进行了优化；
- ``detect_for_video()`` 需要每帧提供时间戳。

**追踪函数**

.. code-block:: python

   def simple_track(x, y):
       if x < CX - DEADZONE:
           pan_move = 1      # Object left → move right
       elif x > CX + DEADZONE:
           pan_move = -1     # Object right → move left

       if y < CY - DEADZONE:
           tilt_move = -1    # Object up → move down
       elif y > CY + DEADZONE:
           tilt_move = 1     # Object down → move up

- 简单的比例控制（非真正的 PID）；
- 死区防止小幅度移动引起舵机抖动；
- 每个轴返回 -1、0 或 1 的移动值。

**主循环处理**

.. code-block:: python

   # Object detection
   detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

   # Find target object
   for detection in detections.detections:
       for category in detection.categories:
           if TARGET.lower() in str(category.category_name).lower():
               bbox = detection.bounding_box
               obj_x = bbox.origin_x + bbox.width // 2
               obj_y = bbox.origin_y + bbox.height // 2

1. 将帧转换为 MediaPipe 图像格式；
2. 使用当前时间戳运行物体检测；
3. 在检测结果中搜索目标物体（不区分大小写）；
4. 计算物体中心坐标。

**舵机控制逻辑**

.. code-block:: python

   if obj_x is not None:
       pan_move, tilt_move = simple_track(obj_x, obj_y)
       pan_pos += pan_move
       tilt_pos += tilt_move

       # Enforce safe angle limits
       pan_pos = max(-90, min(90, pan_pos))
       tilt_pos = max(-45, min(45, tilt_pos))

       pan.angle(pan_pos)
       tilt.angle(tilt_pos)

1. 从追踪函数获取移动指令；
2. 更新位置累加器；
3. 将位置限制在机械范围内；
4. 向舵机发送新角度。

**视觉反馈**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)

   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)

   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- 绿色框：当前追踪的物体；
- 黄色十字准星：画面中心参考；
- 状态文本：追踪状态和舵机角度。

**清理例程**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- 将舵机回到中心位置；
- 停止摄像头捕获；
- 关闭 OpenCV 窗口；
- 即使发生错误也会执行（``try...finally``）。

------------------------------------------------------
6. 配置选项
------------------------------------------------------

**更改目标物体**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**调整追踪参数**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive

   # Faster, more responsive tracking
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**舵机范围限制**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**性能调优**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing

   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. 性能考量
------------------------------------------------------

.. list-table:: 性能因素
   :header-rows: 1

   * - 因素
     - 对性能的影响
     - 建议
   * - 摄像头分辨率
     - 越高检测越慢
     - 640x480 是良好的平衡
   * - 检测阈值
     - 越低检测越多但误报也越多
     - 0.3-0.5 最佳
   * - 死区大小
     - 越大越平滑但响应越慢
     - 40-60 像素
   * - 舵机速度
     - 越快响应越快但可能过冲
     - 考虑加速度控制
   * - 模型大小
     - Lite0 最快，Lite2 最准确
     - 实时追踪使用 Lite0

**预期性能：**

- **Raspberry Pi 4：** 640x480 下 8-15 FPS
- **检测延迟：** 100-200ms
- **舵机响应时间：** 每度 50-100ms
- **系统总延迟：** 200-400ms

------------------------------------------------------
8. 故障排除指南
------------------------------------------------------

.. list-table:: 常见问题及解决方案
   :header-rows: 1

   * - 问题
     - 可能原因
     - 解决方案
   * - 没有物体检测
     - 物体不在 COCO 类别中
     - 使用支持的物体名称
   * - 舵机运动卡顿
     - 死区太小
     - 将 DEADZONE 增加到 60-80
   * - 舵机过冲
     - 移动步长太大
     - 将 pan_move 从 1 改为 0.5
   * - 帧率低
     - 分辨率太高
     - 降低到 320x240
   * - 摄像头不工作
     - 摄像头未启用
     - 运行 ``sudo raspi-config``
   * - 舵机不移动
     - 接线或电源不正确
     - 检查连接和电源
   * - 频繁丢失物体
     - 阈值太高
     - 将 SCORE_THRESHOLD 降低到 0.2
   * - 追踪方向错误
     - 舵机方向相反
     - 交换 pan_move 符号

**调试技巧：**

1. **单独测试舵机：**

   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **验证物体检测：**

   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **检查物体坐标：**

   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **监控帧率：**

   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. 高级修改
------------------------------------------------------

**1. PID 控制实现**

.. code-block:: python

   class PIDController:
       def __init__(self, kp=0.1, ki=0.01, kd=0.05):
           self.kp, self.ki, self.kd = kp, ki, kd
           self.prev_error = 0
           self.integral = 0

       def update(self, error, dt=1.0):
           self.integral += error * dt
           derivative = (error - self.prev_error) / dt
           output = self.kp*error + self.ki*self.integral + self.kd*derivative
           self.prev_error = error
           return output

**2. 多物体追踪**

.. code-block:: python

   # Track closest object
   best_dist = float('inf')
   best_obj = None
   for detection in detections.detections:
       bbox = detection.bounding_box
       obj_x = bbox.origin_x + bbox.width // 2
       obj_y = bbox.origin_y + bbox.height // 2
       dist = ((obj_x - CX)**2 + (obj_y - CY)**2)**0.5
       if dist < best_dist:
           best_dist = dist
           best_obj = (obj_x, obj_y)

**3. 速度与距离成比例**

.. code-block:: python

   def adaptive_track(x, y):
       if x is None:
           return 0, 0

       # Calculate distance from center
       dx = x - CX
       dy = y - CY

       # Speed proportional to distance (with deadzone)
       pan_move = 0
       tilt_move = 0

       if abs(dx) > DEADZONE:
           pan_move = dx * 0.02  # 2% of distance per frame

       if abs(dy) > DEADZONE:
           tilt_move = dy * 0.02

       return pan_move, tilt_move

**4. 物体记忆（惯性追踪）**

.. code-block:: python

   # Keep tracking briefly when object lost
   OBJECT_TIMEOUT = 10  # frames
   lost_counter = 0

   if obj_x is not None:
       last_x, last_y = obj_x, obj_y
       lost_counter = 0
   elif lost_counter < OBJECT_TIMEOUT:
       obj_x, obj_y = last_x, last_y  # Use last known position
       lost_counter += 1

------------------------------------------------------
10. 应用与扩展
------------------------------------------------------

**教育应用：**

- 机器人和自动化原理
- 计算机视觉基础
- 控制系统（P vs PID）
- 实时系统设计

**实际应用：**

- 安防摄像头自动追踪
- 视频会议摄像头自动化
- 野生动物观察
- 辅助追踪技术

**扩展项目：**

1. **Web 界面：** 通过浏览器远程控制
2. **预设位置：** 保存/加载常用追踪位置
3. **物体学习：** 训练自定义物体
4. **多摄像头：** 协调多个追踪单元
5. **云端集成：** 上传追踪数据进行分析
6. **音频反馈：** 播报追踪状态
7. **手势控制：** 使用手势控制追踪

-----------------------------
11. 安全与最佳实践
-----------------------------

1. **机械安全：**

   - 固定所有运动部件
   - 使用线缆管理
   - 避免夹手点
   - 设置合理的角度限制

2. **电气安全：**

   - 舵机使用外部电源
   - 确保正确接地
   - 避免电源过载
   - 使用适当规格的导线

3. **软件安全：**

   - 退出时始终将舵机居中
   - 实现紧急停止机制
   - 记录错误以便调试
   - 验证输入和限制

4. **操作安全：**

   - 远离运动机构
   - 监控是否过热
   - 定期维护检查
   - 具备手动超控能力

-----------------------------
12. 总结
-----------------------------

本章演示了一个完整的物体追踪系统，使用：

1. **MediaPipe Tasks** 进行可靠的物体检测
2. **云台舵机** 进行物理追踪
3. **简单的比例控制** 作为运动逻辑
4. **OpenCV** 提供视觉反馈和显示

该系统为更高级的追踪应用提供了基础，并展示了实时计算机视觉、控制系统和嵌入式 Python 编程中的关键概念。

通过修改目标物体、调整参数和扩展控制逻辑，该系统可适应从教育演示到实际自动化解决方案的各种应用。

**下一步：**

- 实现 PID 控制以获得更平滑的追踪
- 添加物体记忆以处理临时遮挡
- 创建用于远程监控的 Web 界面
- 与家庭自动化系统集成
- 训练自定义物体检测模型
