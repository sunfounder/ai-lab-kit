.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

9. 云台摄像头红色物体追踪
=============================================

将物体跟踪与机械控制相结合，构成了许多机器人和计算机视觉应用的基础。
在本章中，我们将创建一个系统，能够\ **实时检测红色物体并控制云台舵机**，使物体保持在摄像头画面的中央。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_9.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

这扩展了基本的颜色检测，使之成为一个能够自主跟随移动物体的主动跟踪系统。

.. image:: img/color_track.png
   :alt: 云台摄像头跟踪系统概览
   :align: center


1. 目标与方法
-------------------------

- 使用 **Picamera2** 捕捉实时视频帧
- 使用 **HSV颜色空间** 和形态学滤波检测红色物体
- 实现基于物体位置的\ **简易四方向跟踪**\ 算法
- 控制 **水平和垂直舵机** 以保持物体居中
- 显示 **实时调试信息** 和跟踪状态
- 提供 **可调参数** 用于微调跟踪行为


2. 运行代码
--------------------

.. important::

   开始之前，请确保：

   * 云台已组装
   * 您可以访问Raspberry Pi桌面
   * 代码包已安装
   * Fusion HAT+已安装并配置
   * OpenCV已安装

   详细说明请参见 :ref:`opencv_install`。

#. 打开终端并输入以下命令：

   .. code-block:: bash

        cd ~/ai-lab-kit/opencv_python
        python3 cv_9_track_color.py

3. 运行结果
---------------------------------

成功运行时，您应该看到：

**1. OpenCV窗口：**

- "Red Object Tracking"：显示带有跟踪叠加信息的摄像头画面

**2. 跟踪窗口中的视觉元素：**

- 画面中央的黄色十字准星
- 表示死区（无运动区域）的蓝色矩形
- 标记检测到的物体中心的红色圆点
- 连接物体与画面中心的绿色线条
- 实时信息叠加：

  - 物体位置坐标
  - 当前舵机角度
  - 跟踪模式（简易四方向）
  - 移动步长和死区设置

**3. 控制台输出：**

- FPS（每秒帧数）
- 当前舵机位置
- 物体检测状态
- 移动步长调整

**4. 舵机行为：**

- 舵机将以固定步长移动，使红色物体保持居中
- 当物体在死区范围内时，不移动
- 按 'r' 键时，舵机回到中央位置


**控制方式：**

- 按 **'q'** 退出程序
- 按 **'r'** 将舵机重置到中央位置
- 按 **'+'** 增加移动速度
- 按 **'-'** 降低移动速度

4. 完整代码
-------------------------------

以下是红色物体跟踪的完整Python程序：

.. code-block:: python

   #!/usr/bin/env python3
   """
   Red Object Tracking with Pan-Tilt Camera
   """

   import cv2
   import numpy as np
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2

   # ========== SERVO SETTINGS ==========
   # Servo channels
   PAN_CHANNEL = 2    # Horizontal servo
   TILT_CHANNEL = 3   # Vertical servo

   # Servo angle limits (adjust according to your hardware)
   PAN_MIN = -90      # Maximum left rotation
   PAN_MAX = 90       # Maximum right rotation
   TILT_MIN = -45     # Maximum down rotation
   TILT_MAX = 45      # Maximum up rotation

   # Initial position (center)
   PAN_CENTER = 0
   TILT_CENTER = 0

   # ========== CAMERA SETTINGS ==========
   FRAME_WIDTH = 640
   FRAME_HEIGHT = 480
   CENTER_X = FRAME_WIDTH // 2
   CENTER_Y = FRAME_HEIGHT // 2

   # ========== COLOR DETECTION SETTINGS ==========
   # Red color range in HSV (two ranges for red)
   LOWER_RED1 = np.array([0, 100, 80])     # Lower range for red
   UPPER_RED1 = np.array([10, 255, 255])   # Upper range for red
   LOWER_RED2 = np.array([170, 100, 80])   # Lower range for red (wrap-around)
   UPPER_RED2 = np.array([180, 255, 255])  # Upper range for red (wrap-around)

   # Morphology kernel for noise removal
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

   # Minimum contour area to consider (adjust based on object size)
   MIN_CONTOUR_AREA = 500

   # ========== TRACKING SETTINGS ==========
   # Deadzone around center (pixels) - no movement inside this zone
   DEADZONE_X = 50    # Horizontal deadzone
   DEADZONE_Y = 50    # Vertical deadzone

   # Movement step size in degrees (how much to move each frame)
   MOVE_STEP = 2      # Degrees to move per adjustment

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Red Object Tracking System...")

   # Initialize servos
   print("Setting up servos...")
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center the servos initially
   print("Centering servos...")
   pan_servo.angle(PAN_CENTER)
   tilt_servo.angle(TILT_CENTER)
   time.sleep(1)  # Wait for servos to move to center

   # Current servo positions
   current_pan = PAN_CENTER
   current_tilt = TILT_CENTER

   # Initialize camera
   print("Setting up camera...")
   picam2 = Picamera2()

   # Configure camera for OpenCV
   config = picam2.create_preview_configuration(
       main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "XRGB8888"}
   )
   picam2.configure(config)
   picam2.start()

   print("Camera started. Looking for red objects...")
   print("Press 'q' to quit the program")
   print("-" * 50)

   def simple_tracking(x, y):
       """
       Simple 4-direction tracking algorithm
       Args:
           x: Object x-coordinate (None if not found)
           y: Object y-coordinate (None if not found)
       Returns:
           pan_move, tilt_move: Degrees to move each servo (+/-)
       """
       # If no object detected, don't move
       if x is None or y is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Check if object is left of center (outside deadzone)
       if x < CENTER_X - DEADZONE_X:
           # Object is left, move camera right (positive pan)
           pan_move = MOVE_STEP
       # Check if object is right of center (outside deadzone)
       elif x > CENTER_X + DEADZONE_X:
           # Object is right, move camera left (negative pan)
           pan_move = -MOVE_STEP

       # Check if object is above center (outside deadzone)
       if y < CENTER_Y - DEADZONE_Y:
           # Object is up, move camera down (negative tilt)
           tilt_move = -MOVE_STEP
       # Check if object is below center (outside deadzone)
       elif y > CENTER_Y + DEADZONE_Y:
           # Object is down, move camera up (positive tilt)
           tilt_move = MOVE_STEP

       return pan_move, tilt_move

   def update_servo_position(pan_move, tilt_move):
       """
       Update servo positions with limits checking
       Args:
           pan_move: Degrees to move pan servo (+/-)
           tilt_move: Degrees to move tilt servo (+/-)
       Returns:
           current_pan, current_tilt: New servo positions
       """
       global current_pan, current_tilt

       # Calculate new positions
       new_pan = current_pan + pan_move
       new_tilt = current_tilt + tilt_move

       # Apply angle limits to prevent hardware damage
       new_pan = max(min(new_pan, PAN_MAX), PAN_MIN)
       new_tilt = max(min(new_tilt, TILT_MAX), TILT_MIN)

       # Move servos only if position changed
       if new_pan != current_pan:
           pan_servo.angle(new_pan)
           current_pan = new_pan

       if new_tilt != current_tilt:
           tilt_servo.angle(new_tilt)
           current_tilt = new_tilt

       return current_pan, current_tilt

   def find_red_object(frame):
       """
       Detect red object in frame using HSV color space
       Args:
           frame: Input BGR image frame
       Returns:
           center_x, center_y: Coordinates of largest red object, or (None, None)
           mask: Binary mask showing detected red areas
       """
       # Convert BGR to HSV color space (better for color detection)
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

       # Create masks for red color (red wraps around 0 in HSV)
       mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)   # Lower red range
       mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)   # Upper red range
       mask = cv2.bitwise_or(mask1, mask2)                # Combine both ranges

       # Apply morphological operations to clean up noise
       mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
       mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

       # Find contours in the mask
       contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

       # Return if no contours found
       if not contours:
           return None, None, mask

       # Find the largest contour (assume it's our target)
       largest_contour = max(contours, key=cv2.contourArea)
       area = cv2.contourArea(largest_contour)

       # Filter by minimum area to ignore small noise
       if area < MIN_CONTOUR_AREA:
           return None, None, mask

       # Calculate center of the contour using image moments
       M = cv2.moments(largest_contour)
       if M["m00"] == 0:  # Prevent division by zero
           return None, None, mask

       center_x = int(M["m10"] / M["m00"])
       center_y = int(M["m01"] / M["m00"])

       return center_x, center_y, mask

   def draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle):
       """
       Draw debugging information on the frame for visualization
       Args:
           frame: Frame to draw on
           object_x, object_y: Object coordinates
           mask: Detection mask
           pan_angle, tilt_angle: Current servo angles
       Returns:
           frame: Frame with debug drawings
       """
       # Draw center crosshair
       cv2.line(frame, (CENTER_X - 20, CENTER_Y), (CENTER_X + 20, CENTER_Y), (0, 255, 255), 2)
       cv2.line(frame, (CENTER_X, CENTER_Y - 20), (CENTER_X, CENTER_Y + 20), (0, 255, 255), 2)
       cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (0, 255, 255), -1)

       # Draw deadzone rectangle
       cv2.rectangle(frame,
                    (CENTER_X - DEADZONE_X, CENTER_Y - DEADZONE_Y),
                    (CENTER_X + DEADZONE_X, CENTER_Y + DEADZONE_Y),
                    (255, 255, 0), 1)

       # Draw object center if detected
       if object_x is not None and object_y is not None:
           cv2.circle(frame, (object_x, object_y), 10, (0, 0, 255), -1)
           cv2.line(frame, (CENTER_X, CENTER_Y), (object_x, object_y), (0, 255, 0), 2)

           # Display position information
           pos_text = f"Position: ({object_x}, {object_y})"
           cv2.putText(frame, pos_text, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

       # Display servo angles
       angle_text = f"Pan: {pan_angle:+03.0f}, Tilt: {tilt_angle:+03.0f}"
       cv2.putText(frame, angle_text, (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

       # Display tracking mode
       cv2.putText(frame, "Mode: Simple 4-Direction", (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Display movement step
       step_text = f"Step: {MOVE_STEP}, Deadzone: {DEADZONE_X}px"
       cv2.putText(frame, step_text, (10, 120),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Draw quit instruction
       cv2.putText(frame, "Press 'q' to quit, 'r' to reset", (10, FRAME_HEIGHT - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

       return frame

   def cleanup():
       """
       Clean up resources before exiting
       """
       print("\nCleaning up...")

       # Center servos before stopping
       print("Centering servos...")
       pan_servo.angle(PAN_CENTER)
       tilt_servo.angle(TILT_CENTER)
       time.sleep(0.5)

       # Stop camera
       print("Stopping camera...")
       picam2.stop()

       # Close OpenCV windows
       cv2.destroyAllWindows()
       print("System shutdown complete.")

   # ========== MAIN LOOP ==========
   def main():
       """
       Main tracking loop
       """
       frame_count = 0
       start_time = time.time()
       global MOVE_STEP
       global current_pan, current_tilt
       try:
           while True:
               # Capture frame from camera
               frame_bgra = picam2.capture_array()
               frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

               # Find red object in frame
               obj_x, obj_y, mask = find_red_object(frame_bgr)

               # Use simple tracking algorithm to determine movement
               pan_move, tilt_move = simple_tracking(obj_x, obj_y)

               # Update servo positions
               pan_angle, tilt_angle = update_servo_position(pan_move, tilt_move)

               # Draw debugging information
               frame_display = draw_debug_info(frame_bgr, obj_x, obj_y, mask, pan_angle, tilt_angle)

               # Display frames
               cv2.imshow("Red Object Tracking", frame_display)

               # Calculate and display FPS every 30 frames
               frame_count += 1
               if frame_count % 30 == 0:
                   elapsed_time = time.time() - start_time
                   fps = frame_count / elapsed_time
                   print(f"FPS: {fps:.1f} | Pan: {pan_angle:+03.0f}° | Tilt: {tilt_angle:+03.0f}° | "
                         f"Object: {'Found' if obj_x else 'Not found'}")

               # Check for user input
               key = cv2.waitKey(1) & 0xFF
               if key == ord('q'):
                   print("\nQuit command received.")
                   break
               elif key == ord('r'):
                   # Reset to center position
                   print("Resetting to center...")
                   pan_servo.angle(PAN_CENTER)
                   tilt_servo.angle(TILT_CENTER)
                   current_pan = PAN_CENTER
                   current_tilt = TILT_CENTER
                   time.sleep(0.5)
               elif key == ord('+'):
                   # Increase movement speed
                   MOVE_STEP = min(MOVE_STEP + 0.5, 5)
                   print(f"Movement step increased to {MOVE_STEP}°")
               elif key == ord('-'):
                   # Decrease movement speed
                   MOVE_STEP = max(MOVE_STEP - 0.5, 0.5)
                   print(f"Movement step decreased to {MOVE_STEP}°")

       except KeyboardInterrupt:
           print("\nProgram interrupted.")

       finally:
           cleanup()

   # ========== PROGRAM START ==========
   if __name__ == "__main__":
       print("=" * 60)
       print("RED OBJECT TRACKING WITH PAN-TILT CAMERA")
       print("=" * 60)
       print("System will:")
       print("1. Detect red objects using OpenCV")
       print("2. Move servos in 4 directions to keep object centered")
       print("3. Display tracking information")
       print("\nControls:")
       print("  Press 'q' to quit")
       print("  Press 'r' to reset servos to center")
       print("  Press '+' to increase movement speed")
       print("  Press '-' to decrease movement speed")
       print("\nTracking Logic:")
       print(f"  Deadzone: {DEADZONE_X}px around center (no movement)")
       print(f"  Movement: {MOVE_STEP}° per adjustment")
       print("  Left object → Move right (+pan)")
       print("  Right object → Move left (-pan)")
       print("  Up object → Move down (-tilt)")
       print("  Down object → Move up (+tilt)")
       print("=" * 60)

       main()


5. 代码解释
----------------------------------

#. ``simple_tracking(x, y)``

   此函数根据检测到的物体位置决定舵机应如何移动。

   - 如果没有检测到物体（\ ``x``\ 或\ ``y``\ 为\ ``None``），返回\ ``(0, 0)``（不移动）。
   - 如果物体在死区之外，返回一个小的移动步长：

     - 物体在左 → ``pan_move = +MOVE_STEP``
     - 物体在右 → ``pan_move = -MOVE_STEP``
     - 物体在上 → ``tilt_move = -MOVE_STEP``
     - 物体在下 → ``tilt_move = +MOVE_STEP``

   死区防止当物体已接近画面中央时摄像头抖动。

#. ``update_servo_position(pan_move, tilt_move)``

   此函数安全地更新水平和垂直舵机的角度。

   - 将移动步长加到当前舵机角度。
   - 将角度限制在安全范围内（\ ``PAN_MIN/PAN_MAX``\ 和\ ``TILT_MIN/TILT_MAX``）。
   - 仅在角度实际变化时才发送舵机指令。

   这可以保护硬件免于过度旋转。

#. ``find_red_object(frame)``

   此函数检测摄像头画面中最大的红色物体。

   主要步骤：

   - 将帧从BGR转换为HSV。
   - 使用两个HSV范围创建红色像素的二值掩膜。
   - 使用形态学操作（OPEN + CLOSE）清理掩膜。
   - 查找轮廓并选择最大的一个。
   - 使用 ``MIN_CONTOUR_AREA``\ 过滤小区域。
   - 使用图像矩计算物体中心。

   它返回：

   - ``center_x, center_y``：物体中心位置（或\ ``None, None``）
   - ``mask``：显示红色区域的二值掩膜

#. ``draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle)``

   此函数在视频帧上绘制有用的跟踪信息，包括：

   - 中央十字准星
   - 死区矩形
   - 检测到的物体位置
   - 舵机角度（水平和垂直）
   - 跟踪模式和步长
   - 按键说明

   这便于直观地观察跟踪器的工作情况。

#. ``cleanup()``

   此函数在退出前安全关闭系统。

   - 将舵机移回中央位置。
   - 停止摄像头。
   - 关闭所有OpenCV窗口。

   这防止摄像头被留在异常位置。

#. ``main()``

   这是主跟踪循环。

   每次迭代执行：

   - 捕获摄像头帧。
   - 检测红色物体。
   - 决定如何移动舵机。
   - 更新舵机角度。
   - 绘制调试信息。
   - 显示结果窗口。

   它还支持运行时控制：

   - ``q``\ 退出
   - ``r``\ 重置舵机
   - ``+`` / ``-``\ 调整跟踪速度

   程序始终在 ``finally``\ 块中调用 ``cleanup()``\ 以确保安全关闭。


6. 关键参数与调试
----------------------------

#. 颜色检测参数

   .. code-block:: python

      # HSV thresholds for red detection
      LOWER_RED1 = np.array([0, 100, 80])     # [Hue, Saturation, Value]
      UPPER_RED1 = np.array([10, 255, 255])
      LOWER_RED2 = np.array([170, 100, 80])
      UPPER_RED2 = np.array([180, 255, 255])

      # Minimum object size
      MIN_CONTOUR_AREA = 500

   调试建议：

   - 调整Hue值以检测不同颜色
   - 在明亮环境中增加Saturation/Value的最小值
   - 根据预期物体大小调整 ``MIN_CONTOUR_AREA``

#. 跟踪参数

   .. code-block:: python

      # Deadzone size (pixels)
      DEADZONE_X = 50    # Larger = less jitter, but less precision
      DEADZONE_Y = 50

      # Movement step size (degrees)
      MOVE_STEP = 2      # Larger = faster tracking, but may overshoot

   调试建议：

   - 从较大的死区（50-100px）开始，以获得稳定运行
   - 根据跟踪需求调整MOVE_STEP（0.5-5°）
   - 运行时使用 '+' 和 '-' 键调整速度

#. 舵机参数

   .. code-block:: python

      # Servo limits (calibrate for your hardware)
      PAN_MIN = -90   # Maximum left
      PAN_MAX = 90    # Maximum right
      TILT_MIN = -45  # Maximum down
      TILT_MAX = 45   # Maximum up

   .. note:: 请根据您的具体硬件校准这些值，以防止损坏。


7. 常见问题与故障排除
------------------------------------

* 舵机不移动

  - **原因**：物体在死区内或MIN_CONTOUR_AREA过高
  - **解决方法**：检查物体位置，降低MIN_CONTOUR_AREA，或减小死区

* 舵机移动太慢

  - **原因**：MOVE_STEP过小
  - **解决方法**：按 '+' 键增加移动速度

* 舵机移动太抖动

  - **原因**：MOVE_STEP过大
  - **解决方法**：按 '-' 键降低移动速度

* 物体检测错误

  - **原因**：HSV阈值范围过宽或光照问题
  - **解决方法**：调整HSV范围，改善光照，增加MIN_CONTOUR_AREA

* FPS过低（低于10 FPS）

  - **原因**：处理过载或摄像头设置
  - **解决方法**：降低帧分辨率，简化调试绘制

8. 扩展与高级功能
------------------------------------

#. 多物体跟踪

   .. code-block:: python

      # Instead of taking the largest contour:
      for contour in contours:
          if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
              # Track multiple objects

#. 比例控制

   .. code-block:: python

      # Re-implement proportional control if desired
      KP_PAN = 0.3
      pan_move = -x_error * KP_PAN / CENTER_X

#. 基于物体大小的速度调整

   .. code-block:: python

      # Adjust movement speed based on object size
      object_size = cv2.contourArea(largest_contour)
      if object_size > 1000:  # Large object
          adjusted_step = MOVE_STEP * 0.5  # Move slower
      else:  # Small object
          adjusted_step = MOVE_STEP * 1.5  # Move faster

#. 日志记录与数据记录

   .. code-block:: python

      # Record tracking data for analysis
      with open('tracking_log.csv', 'a') as f:
          f.write(f"{time.time()},{obj_x},{obj_y},{pan_angle},{tilt_angle}\n")

#. 网络视频流

   .. code-block:: python

      # Stream video over network
      import socket
      # Add network streaming code


9. 学习成果
---------------------

完成此项目后，您应理解：

1. **计算机视觉**：实时颜色检测和物体跟踪
2. **控制系统**：简易四方向跟踪算法的实现
3. **硬件集成**：连接摄像头和舵机与Raspberry Pi
4. **交互控制**：运行时的实时参数调整
5. **系统设计**：简化的跟踪系统架构

本项目为更高级的应用奠定了基础，如人脸跟踪、自主导航和工业自动化系统。简化的四方向方法使其易于理解和修改，以适应不同的应用场景。