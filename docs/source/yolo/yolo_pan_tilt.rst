.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. 使用云台追踪物体
==============================================================


在前面的教程中，我们学习了如何使用YOLO在Raspberry Pi上进行目标检测。然而，检测只是第一步——如果您想让摄像头真正"跟随"目标，就需要将检测与机械控制结合起来。

本教程将引导您构建一个\ **YOLO物体跟踪系统**，实现以下功能：

* 使用YOLO实时检测特定物体
* 自动计算目标在画面中的位置偏差
* 通过舵机控制摄像头云台，使目标保持在画面中央
* 支持按SPACE键保存当前帧，用于数据集采集

这里我们追踪的目标是前一个教程中训练的自定义模型中的物体——我的是一个雪人。您也可以选择其他模型（如yolov8n）来追踪其他目标（如人、车等）。

.. image:: img/yolo_track.png

图示：YOLO物体跟踪系统运行中。当目标移动时，摄像头云台自动跟随，使目标保持在画面中央的黄色十字准星附近。绿色边界框标记检测到的目标。

**应用场景**：

* 智能监控：自动跟踪可疑目标
* 宠物伴侣：让摄像头跟随宠物的移动
* 视频会议：自动让讲话者保持在画面中央
* 数据采集：自动捕获目标的多角度图像

硬件设置
---------------------------------------

要使用此项目，您需要按照 :ref:`assemble_fusion_hat_pan_tilt`\ 中的说明组装云台。

.. image:: ../quick_start/img/gimbal_assemble.png


运行代码
----------------------------------------

1. **修改配置参数**

   .. code-block:: bash

      cd ~/ai-lab-kit/yolo
      nano yolo_tracking.py

   将代码开头的 ``TARGET``\ 变量改为您要追踪的物体：

   .. code-block:: python

      TARGET = "person"     # Track a person
      # or
      TARGET = "snowman"    # Track a snowman

2. **准备模型文件**

   * 使用预训练模型：\ ``model = YOLO("yolov8n.pt")``
   * 使用自定义模型：\ ``model = YOLO("snowman.pt")``

3. **保存并运行代码**

   .. code-block:: bash

      python3 yolo_tracking.py

4. **操作说明**

   * 启动程序后，摄像头自动开始工作
   * 检测到目标时，舵机自动旋转，使目标保持在画面中央
   * 按 ``SPACE``\ 保存当前帧（用于采集训练数据）
   * 按 ``ESC``\ 退出程序

代码
-----------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480         # Camera resolution
   CX, CY = W // 2, H // 2 # Center coordinates
   CONFIDENCE = 0.3        # Detection confidence threshold
   DEADZONE = 50           # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

   print(f"=== YOLO Tracking System ===")
   print(f"Target: {TARGET}")
   print(f"Confidence threshold: {CONFIDENCE}")
   print(f"Deadzone: {DEADZONE} pixels")

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

   # -------------------- Camera Initialization --------------------
   print("Initializing camera...")
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (W, H)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()
   time.sleep(2)

   print("\n=== System Ready ===")
   print("Controls:")
   print("  SPACE - Capture image (for dataset)")
   print("  ESC   - Exit")
   print("  (Auto-tracks object when detected)")
   print("==========================\n")

   # -------------------- Tracking Variables --------------------
   pan_pos = 0    # Current pan angle (-90 to 90)
   tilt_pos = 0   # Current tilt angle (-45 to 45)
   capture_count = 0

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

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

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

         # Draw deadzone rectangle (visual reference)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")


代码解释
------------------------------

以下是完整的YOLO物体跟踪代码。我们逐节分析其工作原理。

**1. 导入库和配置参数**

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480             # Camera resolution
   CX, CY = W // 2, H // 2     # Center coordinates
   CONFIDENCE = 0.3            # Detection confidence threshold
   DEADZONE = 50               # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

配置参数：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 参数
     - 说明
     - 推荐值
   * - ``TARGET``
     - 要追踪的物体名称
     - "person"、 "snowman"、 "cup"
   * - ``W, H``
     - 摄像头分辨率
     - 640x480（性能平衡）
   * - ``DEADZONE``
     - 死区范围（像素）
     - 50-100，防止频繁抖动
   * - ``CONFIDENCE``
     - 检测置信度阈值
     - 0.3-0.5
   * - ``SAVE_DIR``
     - 图像保存目录
     - captured_images

**2. 初始化舵机**

.. code-block:: python

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

舵机角度范围：

* 水平舵机：-90° 到 90°，0°为居中
* 垂直舵机：-45° 到 45°，0°为居中

**3. 加载YOLO模型**

.. code-block:: python

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

模型选择建议：

* 使用自己训练的模型：\ ``"snowman.pt"``\ 、\ ``"my_pet.pt"``
* 使用预训练模型：\ ``"yolov8n.pt"``\ （可检测80种常见物体）

**4. 物体检测与跟踪逻辑**

.. code-block:: python

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

跟踪逻辑说明：

* **死区机制**：当目标在画面中央附近的死区内时，舵机不移动，防止频繁抖动
* **方向判断**：物体偏左则向右转，偏右则向左转
* **目标识别**：通过匹配类名找到要追踪的物体

**5. 主循环**

.. code-block:: python

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

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

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair and deadzone
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")

性能优化
-----------------------------------------

在Raspberry Pi上运行跟踪系统时，以下优化方法可以提供帮助：

1. **降低检测频率**：每2-3帧检测一次，中间帧复用检测结果

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       if frame_count % 3 == 0:
           results = model.predict(frame, imgsz=320)
       frame_count += 1

2. **缩小检测区域**：只在目标可能出现的区域进行检测

3. **使用更小的模型**：\ ``yolov8n.pt``\ 是最佳选择

4. **调整死区范围**：增大 ``DEADZONE``\ 可以减少舵机的频繁移动

常见问题
---------------------------------

**问：舵机不动怎么办？**

* 检查舵机是否正确连接
* 确认fusion_hat库已正确安装

**问：跟踪响应太慢怎么办？**

* 降低摄像头分辨率（如320x240）
* 降低检测分辨率 ``imgsz``
* 增大死区范围以减少舵机移动

**问：目标检测不稳定怎么办？**

* 调整 ``CONFIDENCE``\ 阈值（值越低检测越多，但误检也增加）
* 确保充足的光照
* 使用自定义训练的模型以获得更好的针对性

**问：如何调整舵机灵敏度？**

修改\ ``simple_track``\ 函数中的步长值：

.. code-block:: python

   # Increase step size for faster servo movement
   pan_move = 2  # Originally 1
   tilt_move = 2

**问：可以追踪多个目标吗？**

修改\ ``find_target_detection``\ 函数，返回最近或置信度最高的目标，或实现多目标切换功能。

扩展功能
-----------------------------------

**1. 添加PID控制**\ （更平滑的跟踪）

.. code-block:: python

   # Simplified PID controller example
   pan_error = CX - obj_x
   pan_output = pan_error * 0.05  # Proportional control
   pan_pos += int(pan_output)

**2. 自动记录跟踪轨迹**

.. code-block:: python

   # Record target position history
   trajectory = []
   trajectory.append((obj_x, obj_y))

**3. 检测到目标时发送通知**

.. code-block:: python

   if obj_x is not None:
       # Send email or push notification
       pass

**4. 集成人脸识别**

结合人脸识别库，只追踪特定人物。

总结
---------------------

通过本教程，您已学会：

* 如何将YOLO目标检测与舵机控制相结合
* 如何实现基于视觉的自动跟踪系统
* 如何使用死区机制避免抖动
* 如何在跟踪过程中采集训练数据

该系统可广泛应用于智能监控、自动拍摄、机器人视觉等场景。随着YOLO模型的不断发展，您可以构建更加智能的跟踪系统——例如根据目标大小自动调整变焦，或根据运动轨迹预测目标移动方向。