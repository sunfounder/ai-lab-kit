.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. パンチルトカメラによる物体追跡
=============================================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

この章では、MediaPipe の物体検出を拡張し、
パンチルトサーボプラットフォームを使った
シンプルな **物体追跡システム** を構築します。

このシステムは、指定した対象物
（たとえば ``banana``）
を検出し、2 つのサーボを自動的に制御して、
対象がカメラ映像の中央付近に収まるように調整します。

.. image:: img/mp_object_track.png
   :width: 500
   :align: center

このプロジェクトは、以下の要素を組み合わせています：

- リアルタイム物体検出
- サーボモータ制御
- 比例追跡ロジック
- 視覚的フィードバック表示

これは、コンピュータビジョンが
リアルタイムで物理ハードウェアを直接駆動できることを示す
実践的な例です。


------------------------------------------------------------
2. 動作の仕組み
------------------------------------------------------------

追跡システムは次の手順で動作します：

1. パン・チルトサーボを中央位置に初期化する
2. Raspberry Pi カメラを動画ストリーミング用に設定する
3. 物体検出用に EfficientDet Lite0 モデルを読み込む
4. 各フレームで MediaPipe Tasks を使って物体を検出する
5. 目標物体（例：``banana``）を特定する
6. フレーム中心に対する物体のずれ量を計算する
7. 比例制御を使ってサーボ角度を調整する
8. 追跡ガイドと状態情報を画面に表示する

このサンプルは、視覚フィードバックを使って
ハードウェアの動きを動的に制御する方法を示しています。

------------------------
3. コードの実行
------------------------

.. important::

   開始する前に、次の項目を確認してください：

   * パンチルトが組み立てられている
   * Raspberry Pi のデスクトップにアクセスできる
   * コードパッケージがインストールされている
   * Fusion HAT+ がインストールおよび設定されている
   * OpenCV がインストールされている


   詳細な手順については :ref:`opencv_install` を参照してください。

#. ターミナルを開き、次のコマンドを入力します：

   .. code-block:: bash

       sudo python3 ~/ai-lab-kit/mediapipe/mp_track_object.py

#. プログラムを実行すると、カメラウィンドウが開き、リアルタイム物体検出が始まります。

   .. raw:: html
   
         <video width="300" loop muted controls>
             <source src="../_static/video/object_tracking.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
   
   システムは指定された対象物（デフォルト：``banana``）を探します。  
   画面中央には基準点として黄色の十字マーカーが表示されます。
   
   対象物がフレーム内に現れると：
   
   - MediaPipe が EfficientDet Lite0 モデルを使って物体を検出します。
   - 検出されたバウンディングボックスの中心座標を計算します。
   - 物体が中央のデッドゾーン外にある場合、パン・チルトサーボが段階的に動きます。
   - カメラが物理的に回転し、物体がフレーム中央付近に来るようにします。
   - 物体の周囲に緑色の追跡ボックスが描画されます。
   - 画面には次の情報が表示されます：
   
     - ``Tracking banana`` （状態表示）
     - 現在のサーボ角度（Pan / Tilt）
   
   物体が検出されない場合：
   
   - サーボは動作を停止します。
   - 状態表示は ``No banana found`` に切り替わります（赤色表示）。
   
   追跡ロジックには、シンプルな 4 方向デッドゾーン制御を使用しています。  
   物体が中心から十分に離れたときだけサーボが動くため、
   ジッターを防げます。
   
   ``q`` を押すとプログラムを停止できます。
   
   終了時には：
   
   - 2 つのサーボが中央位置に戻ります。
   - カメラが停止します。
   - 表示ウィンドウが閉じます。
   - ``Tracking stopped. Servos centered.`` というメッセージが出力されます。

-----------------------------
4. 完全なコード
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
5. コードの説明
-----------------------------

**設定セクション**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET``: 追跡する物体カテゴリ（COCO データセットのクラスに含まれている必要があります）
- ``W, H``: カメラ解像度。速度と細部のバランスを取った設定です
- ``CX, CY``: 追跡基準となるフレーム中心座標
- ``SCORE_THRESHOLD``: 有効な検出とみなす最小信頼度
- ``DEADZONE``: サーボが動き始める中心からの距離（ジッター低減用）

**サーボの初期化**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` と ``Servo(3)`` は Fusion HAT 上のチャンネルに対応しています
- ``.angle(0)`` でサーボを 0° の中央位置に設定します
- ``time.sleep(1)`` により、処理を続ける前にサーボが所定位置に到達する時間を確保します

**カメラ設定**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- 最新のカメラ API として Picamera2 ライブラリを使用しています
- ``XRGB8888`` 形式は 8-bit カラーチャンネルを提供します
- ``time.sleep(2)`` により、カメラセンサが安定するまで待機します

**MediaPipe Detector**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- 同じディレクトリから EfficientDet Lite0 モデルを読み込みます
- ``RunningMode.VIDEO`` は連続フレーム処理向けに最適化されています
- ``detect_for_video()`` は各フレームごとにタイムスタンプを必要とします

**追跡関数**

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

- シンプルな比例制御であり、厳密な PID ではありません
- デッドゾーンにより、小さな揺れによるサーボのジッターを防ぎます
- 各軸について -1、0、1 の移動値を返します

**メインループ処理**

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

1. フレームを MediaPipe の画像形式に変換します
2. 現在のタイムスタンプで物体検出を実行します
3. 検出結果の中から目標物体を探します（大文字小文字は区別しません）
4. 物体の中心座標を計算します

**サーボ制御ロジック**

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

1. 追跡関数から移動指令を取得します
2. 現在位置の累積値を更新します
3. 機械的な安全範囲内にクランプします
4. 新しい角度をサーボに送信します

**視覚的フィードバック**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)
   
   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)
   
   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- 緑のボックス: 現在追跡中の物体
- 黄色の十字マーカー: フレーム中央の基準位置
- 状態テキスト: 追跡状態とサーボ角度

**クリーンアップ処理**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- サーボを中央位置に戻します
- カメラキャプチャを停止します
- OpenCV ウィンドウを閉じます
- エラーが発生しても必ず実行されます（ ``try...finally`` ）

------------------------------------------------------
6. 設定オプション
------------------------------------------------------

**追跡対象の変更**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking  
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**追跡パラメータの調整**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive
   
   # Faster, more responsive tracking  
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**サーボ可動範囲の制限**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**パフォーマンス調整**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing
   
   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. パフォーマンス上の考慮点
------------------------------------------------------

.. list-table:: Performance Factors
   :header-rows: 1

   * - Factor
     - Effect on Performance
     - Recommendation
   * - Camera Resolution
     - 高いほど検出は遅くなる
     - 640x480 が良いバランス
   * - Detection Threshold
     - 低いほど検出は増えるが誤検出も増える
     - 0.3-0.5 が最適
   * - Deadzone Size
     - 大きいほど滑らかだが反応は鈍くなる
     - 40-60 ピクセル
   * - Servo Speed
     - 速いほど反応は良いがオーバーシュートしやすい
     - 加速度制御の導入を検討
   * - Model Size
     - Lite0 が最速、Lite2 が最高精度
     - リアルタイム追跡には Lite0 を推奨

**想定パフォーマンス：**

- **Raspberry Pi 4:** 640x480 で 8-15 FPS
- **検出遅延:** 100-200ms
- **サーボ応答時間:** 1 度あたり 50-100ms
- **システム全体の遅延:** 200-400ms

------------------------------------------------------
8. トラブルシューティングガイド
------------------------------------------------------

.. list-table:: Common Issues and Solutions
   :header-rows: 1

   * - Issue
     - Possible Cause
     - Solution
   * - No object detection
     - 物体が COCO クラスに含まれていない
     - 対応している物体名を使用する
   * - Jerky servo movement
     - デッドゾーンが小さすぎる
     - DEADZONE を 60-80 に上げる
   * - Servo overshoot
     - 移動ステップが大きすぎる
     - pan_move を 1 から 0.5 に変更する
   * - Low frame rate
     - 解像度が高すぎる
     - 320x240 に下げる
   * - Camera not working
     - カメラが有効化されていない
     - ``sudo raspi-config`` を実行する
   * - Servos not moving
     - 配線ミスまたは電源不足
     - 接続と電源を確認する
   * - Object lost frequently
     - 閾値が高すぎる
     - SCORE_THRESHOLD を 0.2 に下げる
   * - Incorrect tracking direction
     - サーボの向きが逆
     - pan_move の符号を反転する

**デバッグのヒント：**

1. **サーボを個別にテストする：**
   
   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **物体検出を確認する：**
   
   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **物体座標を確認する：**
   
   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **フレームレートを監視する：**
   
   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. 高度な改造
------------------------------------------------------

**1. PID 制御の実装**

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

**2. 複数物体の追跡**

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

**3. 距離に比例した速度制御**

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

**4. 物体記憶（慣性追跡）**

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
10. 応用と拡張
------------------------------------------------------

**教育用途：**

- ロボティクスと自動化の原理学習
- コンピュータビジョンの基礎
- 制御システム（P 制御 vs PID）
- リアルタイムシステム設計

**実用用途：**

- セキュリティカメラの自動追跡
- ビデオ会議用カメラの自動化
- 野生動物の観察
- 追跡支援のための補助技術

**拡張プロジェクト：**

1. **Web インターフェース:** ブラウザ経由の遠隔操作
2. **プリセット位置:** よく使う追跡位置の保存 / 読み込み
3. **物体学習:** 独自の物体を学習させる
4. **マルチカメラ:** 複数追跡ユニットの連携
5. **クラウド連携:** 追跡データをアップロードして解析する
6. **音声フィードバック:** 追跡状態を音声で通知する
7. **ジェスチャー制御:** 手のジェスチャーで追跡を制御する

--------------------------------------

11. 安全上の注意とベストプラクティス
-----------------------------------------

1. **機械的安全性：**

   - すべての可動部をしっかり固定する
   - ケーブルマネジメントを行う
   - 指はさみの危険箇所を避ける
   - 適切な角度制限を設定する

2. **電気的安全性：**

   - サーボには外部電源を使用する
   - 適切なグラウンド接続を確保する
   - 電源の過負荷を避ける
   - 適切な太さの配線を使用する

3. **ソフトウェア安全性：**

   - 終了時には必ずサーボを中央に戻す処理を入れる
   - 緊急停止機構を実装する
   - デバッグ用にエラーログを残す
   - 入力値と制限値を検証する

4. **運用上の安全性：**

   - 可動機構に近づきすぎない
   - 過熱がないか監視する
   - 定期的に保守点検を行う
   - 手動で介入できる手段を用意する

-----------------------------
12. まとめ
-----------------------------

この章では、以下を組み合わせた
完全な物体追跡システムを実装しました：

1. **MediaPipe Tasks** による高信頼な物体検出
2. **パンチルトサーボ** による物理的な追跡
3. **シンプルな比例制御** による移動ロジック
4. **OpenCV** による視覚的フィードバックと表示

このシステムは、より高度な追跡アプリケーションの基礎となり、
リアルタイムコンピュータビジョン、制御システム、
組み込み Python プログラミングの重要な概念を実証しています。

追跡対象の変更、各種パラメータの調整、制御ロジックの拡張により、
このシステムは教育用デモから実用的な自動化ソリューションまで、
さまざまな用途に適応できます。

**次のステップ：**

- より滑らかな追跡のために PID 制御を実装する
- 一時的な遮蔽に対応するため物体記憶を追加する
- リモート監視用の Web インターフェースを作成する
- ホームオートメーションシステムと統合する
- 独自の物体検出モデルを学習する