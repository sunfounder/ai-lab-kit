.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

9. パンチルトカメラによる赤色物体追跡
=============================================

物体追跡と機械制御を組み合わせることで、多くのロボティクスおよびコンピュータビジョンアプリケーションの基礎を構成できます。  
この章では、 **赤色物体をリアルタイムで検出し、パンチルトサーボを制御して物体がカメラ画面の中央に来るよう保つ** システムを作成します。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_9.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

これは、基本的な色検出を、自律的に移動物体を追従できるアクティブな追跡システムへと発展させたものです。

.. image:: img/color_track.png
   :alt: Pan-tilt camera tracking system overview
   :align: center


1. 目的とアプローチ
-------------------------

- **Picamera2** を使ってリアルタイムの映像フレームを取得する
- **HSV 色空間** とモルフォロジー処理を使って赤色物体を検出する
- 物体位置に基づく **シンプルな4方向追跡** アルゴリズムを実装する
- **パン／チルトサーボ** を制御して物体を中央に保つ
- **リアルタイムのデバッグ情報** と追跡状態を表示する
- 追跡動作を細かく調整できる **可変パラメータ** を用意する


2. コードの実行
--------------------

.. important::

   開始する前に、次の項目を確認してください：

   * パンチルトが組み立てられている
   * Raspberry Pi のデスクトップにアクセスできる
   * コードパッケージがインストールされている
   * Fusion HAT+ がインストールされ、設定されている
   * OpenCV がインストールされている

   詳細については :ref:`opencv_install` を参照してください。

#. ターミナルを開き、次のコマンドを入力します：

   .. code-block:: bash

        cd ~/ai-lab-kit/opencv_python
        python3 cv_9_track_color.py

3. 実行結果
---------------------------------

正常に実行されると、次のような表示になります：

**1. OpenCV ウィンドウ：**

- ``Red Object Tracking``：追跡オーバーレイ付きのカメラ映像を表示

**2. 追跡ウィンドウ内の表示要素：**

- 画面中央の黄色い照準マーク
- デッドゾーン（サーボが動かない範囲）を示す青い矩形
- 検出された物体の中心を示す赤い円
- 物体と画面中央を結ぶ緑色の線
- リアルタイム情報オーバーレイ：

  - 物体位置の座標
  - 現在のサーボ角度
  - 追跡モード（Simple 4-Direction）
  - 移動ステップとデッドゾーン設定

**3. コンソール出力：**

- FPS（1秒あたりのフレーム数）
- 現在のサーボ位置
- 物体検出の状態
- 移動ステップの調整状況

**4. サーボの動作：**

- 赤色物体を中央に保つため、サーボが一定ステップで移動します
- 物体がデッドゾーン内にある場合は動作しません
- ``r`` キーを押すと、サーボは中央位置に戻ります


**操作方法：**

- **`q`** を押すとプログラムを終了
- **`r`** を押すとサーボを中央にリセット
- **`+`** を押すと移動速度を上げる
- **`-`** を押すと移動速度を下げる

4. 完全なコード
-------------------------------

以下は、赤色物体追跡の完全な Python プログラムです：

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


5. コード解説
----------------------------------

#. ``simple_tracking(x, y)``

   この関数は、検出された物体の位置に基づいてサーボをどのように動かすかを決定します。

   - 物体が検出されなかった場合（ ``x`` または ``y`` が ``None``）、 ``(0, 0)`` を返します（移動なし）。
   - 物体がデッドゾーンの外側にある場合は、小さな移動ステップを返します：

     - 物体が左  → ``pan_move = +MOVE_STEP``
     - 物体が右  → ``pan_move = -MOVE_STEP``
     - 物体が上  → ``tilt_move = -MOVE_STEP``
     - 物体が下  → ``tilt_move = +MOVE_STEP``

   デッドゾーンは、物体がすでに中央付近にあるときにカメラが細かく揺れるのを防ぎます。

#. ``update_servo_position(pan_move, tilt_move)``

   この関数は、パン／チルトサーボの角度を安全に更新します。

   - 現在のサーボ角度に移動ステップを加算します。
   - 角度を安全範囲（ ``PAN_MIN/PAN_MAX`` および ``TILT_MIN/TILT_MAX``）に制限します。
   - 実際に角度が変わった場合にのみサーボへコマンドを送ります。

   これにより、ハードウェアの過回転を防げます。

#. ``find_red_object(frame)``

   この関数は、カメラフレーム内で最も大きな赤色物体を検出します。

   主な処理手順：

   - フレームを BGR から HSV に変換する
   - 2つの HSV 範囲を使って赤色ピクセルのバイナリマスクを作成する
   - モルフォロジー処理（OPEN + CLOSE）でマスクを整える
   - 輪郭を検出し、最も大きいものを選ぶ
   - ``MIN_CONTOUR_AREA`` を使って小さなノイズを除外する
   - 画像モーメントを使って物体中心を計算する

   戻り値：

   - ``center_x, center_y``：物体の中心座標（見つからない場合は ``None, None``）
   - ``mask``：赤色領域を示すバイナリマスク

#. ``draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle)``

   この関数は、動画フレーム上に追跡の補助情報を描画します。内容は次のとおりです：

   - 中央照準マーク
   - デッドゾーン矩形
   - 検出された物体位置
   - サーボ角度（pan と tilt）
   - 追跡モードとステップサイズ
   - 操作キーの説明

   これにより、トラッカーがどのように動作しているかを視覚的に確認しやすくなります。

#. ``cleanup()``

   この関数は、終了前にシステムを安全に停止します。

   - サーボを中央位置へ戻す
   - カメラを停止する
   - OpenCV のウィンドウをすべて閉じる

   これにより、カメラが不自然な向きのまま終了するのを防げます。

#. ``main()``

   これはメインの追跡ループです。

   各ループで以下を行います：

   - カメラフレームを取得する
   - 赤色物体を検出する
   - サーボの移動量を決定する
   - サーボ角度を更新する
   - デバッグ情報を描画する
   - 結果ウィンドウを表示する

   また、実行中の操作にも対応しています：

   - ``q`` で終了
   - ``r`` でサーボをリセット
   - ``+`` / ``-`` で追跡速度を調整

   プログラムは常に ``finally`` ブロック内で ``cleanup()`` を呼び出し、安全に終了するようになっています。


6. 主要パラメータと調整
----------------------------

#. 色検出パラメータ

   .. code-block:: python
   
      # HSV thresholds for red detection
      LOWER_RED1 = np.array([0, 100, 80])     # [Hue, Saturation, Value]
      UPPER_RED1 = np.array([10, 255, 255])
      LOWER_RED2 = np.array([170, 100, 80])
      UPPER_RED2 = np.array([180, 255, 255])
   
      # Minimum object size
      MIN_CONTOUR_AREA = 500
   
   調整のポイント：
   
   - Hue の値を変更すると、別の色にも対応できます
   - 明るい環境では Saturation / Value の下限を上げると安定しやすくなります
   - 想定する物体サイズに応じて ``MIN_CONTOUR_AREA`` を調整します

#. 追跡パラメータ

   .. code-block:: python
   
      # Deadzone size (pixels)
      DEADZONE_X = 50    # Larger = less jitter, but less precision
      DEADZONE_Y = 50
   
      # Movement step size (degrees)
      MOVE_STEP = 2      # Larger = faster tracking, but may overshoot
   
   調整のポイント：
   
   - まずは大きめのデッドゾーン（50〜100px）から始めると安定しやすくなります
   - ``MOVE_STEP`` は追跡条件に応じて調整します（0.5〜5°）
   - 実行中に ``+`` と ``-`` キーで速度を調整できます

#. サーボパラメータ

   .. code-block:: python
   
      # Servo limits (calibrate for your hardware)
      PAN_MIN = -90   # Maximum left
      PAN_MAX = 90    # Maximum right
      TILT_MIN = -45  # Maximum down
      TILT_MAX = 45   # Maximum up
   
   .. note:: これらの値は、ハードウェア破損を防ぐために、使用する機材に合わせて必ずキャリブレーションしてください。


7. よくある問題とトラブルシューティング
----------------------------------------

* サーボが動かない

  - **原因**：物体がデッドゾーン内にある、または ``MIN_CONTOUR_AREA`` が大きすぎる
  - **対処法**：物体位置を確認し、 ``MIN_CONTOUR_AREA`` を下げるか、デッドゾーンを小さくしてください

* サーボの動きが遅すぎる

  - **原因**： ``MOVE_STEP`` が小さすぎる
  - **対処法**： ``+`` キーを押して移動速度を上げてください

* サーボの動きがぎこちない

  - **原因**： ``MOVE_STEP`` が大きすぎる
  - **対処法**： ``-`` キーを押して移動速度を下げてください

* 誤検出が多い

  - **原因**：HSV のしきい値範囲が広すぎる、または照明条件が不適切
  - **対処法**：HSV 範囲を調整し、照明を改善し、 ``MIN_CONTOUR_AREA`` を大きくしてください

* FPS が低い（10 FPS 未満）

  - **原因**：処理負荷が高すぎる、またはカメラ設定が重い
  - **対処法**：フレーム解像度を下げるか、デバッグ描画を簡略化してください

8. 拡張と高度な機能
------------------------------------

#. 複数物体の追跡

   .. code-block:: python
   
      # Instead of taking the largest contour:
      for contour in contours:
          if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
              # Track multiple objects

#. 比例制御への切り替え

   .. code-block:: python
   
      # Re-implement proportional control if desired
      KP_PAN = 0.3
      pan_move = -x_error * KP_PAN / CENTER_X

#. 物体サイズに基づく速度調整

   .. code-block:: python
   
      # Adjust movement speed based on object size
      object_size = cv2.contourArea(largest_contour)
      if object_size > 1000:  # Large object
          adjusted_step = MOVE_STEP * 0.5  # Move slower
      else:  # Small object
          adjusted_step = MOVE_STEP * 1.5  # Move faster

#. ログ取得とデータ記録

   .. code-block:: python
   
      # Record tracking data for analysis
      with open('tracking_log.csv', 'a') as f:
          f.write(f"{time.time()},{obj_x},{obj_y},{pan_angle},{tilt_angle}\n")

#. ネットワーク配信

   .. code-block:: python
   
      # Stream video over network
      import socket
      # Add network streaming code


9. 学習成果
---------------------

このプロジェクトを完了すると、次の内容を理解できるようになります：

1. **コンピュータビジョン**：リアルタイムの色検出と物体追跡
2. **制御システム**：シンプルな4方向追跡アルゴリズムの実装
3. **ハードウェア統合**：Raspberry Pi におけるカメラとサーボの連携
4. **対話的制御**：実行中のリアルタイムなパラメータ調整
5. **システム設計**：簡易追跡システムの構成

このプロジェクトは、顔追跡、自律移動、産業用自動化システムなど、さらに高度な応用への基礎になります。シンプルな4方向アプローチを採用しているため、仕組みを理解しやすく、さまざまな用途に合わせて改造しやすいのも特長です。