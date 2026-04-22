.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. パンチルトユニットによる物体追跡
==============================================================

これまでのチュートリアルでは、Raspberry Pi上でYOLOを使用して物体検出を行う方法を学びました。しかし、検出は最初のステップに過ぎません。カメラが実際にターゲットを「追従」するためには、検出と機械制御を組み合わせる必要があります。

このチュートリアルでは、**YOLO物体検出・追跡システム** を開発する方法を説明します。このシステムは以下を実現します：

* YOLOによる特定物体のリアルタイム検出
* 画像内のターゲット位置の偏差を自動計算
* サーボ制御のパンチルトユニットでターゲットを画像中央に維持
* データセット作成のためのスペースキーによる現在画像の保存

ここでは、前のチュートリアルでトレーニングしたカスタムモデル（私の場合は雪だるま）を使用してターゲットを追跡します。他のモデル（yolov8nなど）を選択して、他のターゲット（人、車など）を追跡することもできます。

.. image:: img/yolo_track.png

図：動作中のYOLO物体検出システム。ターゲットが動くと、カメラのパンチルトユニットが自動的に追従し、黄色の照準の付いた画像中央付近にターゲットを維持します。緑色のバウンディングボックスは検出されたターゲットを示しています。

**応用シナリオ**：

* スマート監視：不審なターゲットの自動追跡
* ペットコンパニオン：ペットの動きにカメラが追従
* ビデオ会議：話し手の自動中央配置
* データ収集：ターゲットの多角度画像を自動撮影

ハードウェアのセットアップ
---------------------------------------

このプロジェクトでは、:ref:`assemble_fusion_hat_pan_tilt` の手順に従ってパンチルトユニットを組み立てる必要があります。

.. image:: ../quick_start/img/gimbal_assemble.png

コードの実行
----------------------------------------

1. **設定パラメータの調整**

   .. code-block:: bash

      cd ~/ai-lab-kit/yolo
      nano yolo_tracking.py

   コードの先頭にある変数 ``TARGET`` を、追跡したいオブジェクトに変更します：

   .. code-block:: python

      TARGET = "person"     # 人を追跡
      # または
      TARGET = "snowman"    # 雪だるまを追跡

2. **モデルファイルの準備**

   * 事前学習済みモデルを使用： ``model = YOLO("yolov8n.pt")``
   * カスタムモデルを使用： ``model = YOLO("snowman.pt")``

3. **コードを保存して実行**

   .. code-block:: bash

      python3 yolo_tracking.py

4. **操作手順**

   * 起動後、カメラが自動的に動作します
   * ターゲットが検出されると、サーボが自動的に回転してターゲットを画像中央に維持します
   * ``スペースキー`` を押すと、現在の画像が保存されます（トレーニングデータ収集用）
   * ``ESC`` を押すとプログラムが終了します

コード
-----------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   Raspberry Pi用YOLOベース物体追跡
   YOLOで特定のオブジェクト（例：人）を追跡し、サーボを制御します
   スペースキーでデータセット用の画像をキャプチャ、ESCで終了
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- 設定 --------------------
   TARGET = "your_object"      # 追跡するオブジェクト（クラス名）
   W, H = 640, 480             # カメラ解像度
   CX, CY = W // 2, H // 2     # 画像中心
   CONFIDENCE = 0.3            # 検出信頼度しきい値
   DEADZONE = 50               # 動作開始までの中心からのピクセル数
   SAVE_DIR = "captured_images"  # データセット保存ディレクトリ

   # 保存ディレクトリを作成
   os.makedirs(SAVE_DIR, exist_ok=True)

   print(f"=== YOLO追跡システム ===")
   print(f"ターゲット: {TARGET}")
   print(f"信頼度しきい値: {CONFIDENCE}")
   print(f"デッドゾーン: {DEADZONE}ピクセル")

   # -------------------- サーボ初期化 --------------------
   print("サーボを初期化中...")
   pan = Servo(2)    # チャンネル2 パン（水平）
   tilt = Servo(3)   # チャンネル3 チルト（垂直）
   pan.angle(0)      # 中央位置
   tilt.angle(0)     # 中央位置
   time.sleep(1)

   # -------------------- YOLOモデル読み込み --------------------
   print("YOLOモデルを読み込み中...")
   # Raspberry Piでの最高のパフォーマンスにはYOLOv8nを使用
   model = YOLO("your_model.pt")
   print("モデルの読み込み成功")

   # -------------------- カメラ初期化 --------------------
   print("カメラを初期化中...")
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (W, H)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()
   time.sleep(2)

   print("\n=== システム準備完了 ===")
   print("操作方法:")
   print("  スペースキー - 画像をキャプチャ（データセット用）")
   print("  ESC       - 終了")
   print("  （ターゲット検出時に自動追跡）")
   print("==========================\n")

   # -------------------- 追跡変数 --------------------
   pan_pos = 0    # 現在のパン角度（-90～90）
   tilt_pos = 0   # 現在のチルト角度（-45～45）
   capture_count = 0

   def simple_track(x, y):
      """
      デッドゾーン付きのシンプルな4方向追跡
      戻り値: (pan_move, tilt_move) ここで:
         pan_move: -1（左）, 0（停止）, 1（右）
         tilt_move: -1（下）, 0（停止）, 1（上）
      """
      if x is None or y is None:
         return 0, 0
      
      pan_move = 0
      tilt_move = 0
      
      # 水平移動（パン）
      if x < CX - DEADZONE:
         pan_move = 1           # 右に移動
      elif x > CX + DEADZONE:
         pan_move = -1          # 左に移動
      
      # 垂直移動（チルト）
      if y < CY - DEADZONE:
         tilt_move = -1         # 下に移動
      elif y > CY + DEADZONE:
         tilt_move = 1          # 上に移動
      
      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      YOLO検出結果からターゲットオブジェクトを検索
      戻り値: (x_center, y_center, confidence) または (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None
      
      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])
         
         # 大文字小文字を区別しない部分一致
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence
      
      return None, None, None

   # -------------------- メイン追跡ループ --------------------
   try:
      while True:
         # フレームをキャプチャ
         frame = picam2.capture_array()
         
         # YOLO検出を実行
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)
         
         # ターゲットオブジェクトを検索
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)
         
         # オブジェクトが見つかった場合の追跡処理
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move
               
               # サーボ角度を安全な範囲に制限
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))
               
               # サーボにコマンドを送信
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)
               
               # 検出フレームを描画
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30), 
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)
               
               status = f"{TARGET} 検出: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"{TARGET} 未検出"
               color = (0, 0, 255)
         
         # 中心に照準を描画
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         
         # デッドゾーン矩形を描画（視覚的参照）
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)
         
         # ステータス情報を表示
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"パン: {pan_pos:.0f} チルト: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"キャプチャ枚数: {capture_count}", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "スペース=キャプチャ ESC=終了", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         # ビデオウィンドウを表示
         cv2.imshow(f"YOLO追跡 - {TARGET}", frame)
         
         # キー入力を処理
         key = cv2.waitKey(1) & 0xFF
         
         if key == 32:  # スペースキー - 画像キャプチャ
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"キャプチャ: {filename}")
               capture_count += 1
               
               # フラッシュ効果
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO追跡 - {TARGET}", flash)
               cv2.waitKey(50)
               
         elif key == 27:  # ESCキー - 終了
               print(f"\n終了します。総キャプチャ枚数: {capture_count}")
               break

   finally:
      # -------------------- 後処理 --------------------
      print("後処理中...")
      pan.angle(0)      # 中央に戻す
      tilt.angle(0)     # 中央に戻す
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("追跡停止。サーボを中央に戻しました。")

コードの説明
------------------------------

これは完全なYOLO物体検出コードです。セクションごとに動作を分析します。

**1. ライブラリのインポートと設定パラメータ**

.. code-block:: python

   #!/usr/bin/env python3
   """
   Raspberry Pi用YOLOベース物体追跡
   YOLOで特定のオブジェクト（例：人）を追跡し、サーボを制御します
   スペースキーでデータセット用の画像をキャプチャ、ESCで終了
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- 設定 --------------------
   TARGET = "your_object"      # 追跡するオブジェクト（クラス名）
   W, H = 640, 480             # カメラ解像度
   CX, CY = W // 2, H // 2     # 画像中心
   CONFIDENCE = 0.3            # 検出信頼度しきい値
   DEADZONE = 50               # 動作開始までの中心からのピクセル数
   SAVE_DIR = "captured_images"  # データセット保存ディレクトリ

   # 保存ディレクトリを作成
   os.makedirs(SAVE_DIR, exist_ok=True)

設定パラメータ：

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - パラメータ
     - 説明
     - 推奨値
   * - ``TARGET``
     - 追跡するオブジェクトの名前
     - "person", "snowman", "cup"
   * - ``W, H``
     - カメラ解像度
     - 640x480（バランスの取れた性能）
   * - ``DEADZONE``
     - デッドゾーン領域（ピクセル）
     - 50-100、頻繁な振動を防止
   * - ``CONFIDENCE``
     - 検出信頼度しきい値
     - 0.3-0.5
   * - ``SAVE_DIR``
     - 画像保存ディレクトリ
     - captured_images

**2. サーボの初期化**

.. code-block:: python

   # -------------------- サーボ初期化 --------------------
   print("サーボを初期化中...")
   pan = Servo(2)    # チャンネル2 パン（水平）
   tilt = Servo(3)   # チャンネル3 チルト（垂直）
   pan.angle(0)      # 中央位置
   tilt.angle(0)     # 中央位置
   time.sleep(1)

サーボの角度範囲：

* パンサーボ（水平）：-90°～90°、0°が中央
* チルトサーボ（垂直）：-45°～45°、0°が中央

**3. YOLOモデルの読み込み**

.. code-block:: python

   # -------------------- YOLOモデル読み込み --------------------
   print("YOLOモデルを読み込み中...")
   # Raspberry Piでの最高のパフォーマンスにはYOLOv8nを使用
   model = YOLO("your_model.pt")
   print("モデルの読み込み成功")

モデル選択の推奨：

* 自分でトレーニングしたモデルを使用： ``"snowman.pt"``, ``"my_pet.pt"``
* 事前学習済みモデルを使用： ``"yolov8n.pt"`` （80種類の一般的なオブジェクトを検出）

**4. 物体検出と追跡ロジック**

.. code-block:: python

   def simple_track(x, y):
      """
      デッドゾーン付きのシンプルな4方向追跡
      戻り値: (pan_move, tilt_move) ここで:
         pan_move: -1（左）, 0（停止）, 1（右）
         tilt_move: -1（下）, 0（停止）, 1（上）
      """
      if x is None or y is None:
         return 0, 0
      
      pan_move = 0
      tilt_move = 0
      
      # 水平移動（パン）
      if x < CX - DEADZONE:
         pan_move = 1           # 右に移動
      elif x > CX + DEADZONE:
         pan_move = -1          # 左に移動
      
      # 垂直移動（チルト）
      if y < CY - DEADZONE:
         tilt_move = -1         # 下に移動
      elif y > CY + DEADZONE:
         tilt_move = 1          # 上に移動
      
      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      YOLO検出結果からターゲットオブジェクトを検索
      戻り値: (x_center, y_center, confidence) または (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None
      
      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])
         
         # 大文字小文字を区別しない部分一致
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence
      
      return None, None, None

追跡ロジックの説明：

* **デッドゾーン機構**：ターゲットが画像中央付近のデッドゾーン内にある場合、サーボは動かず、頻繁な振動を防止します
* **方向決定**：ターゲットが中央より左にある場合は右に回転、右にある場合は左に回転
* **ターゲット識別**：クラス名のマッチングにより追跡するオブジェクトを特定

**5. メインループ**

.. code-block:: python

   # -------------------- メイン追跡ループ --------------------
   try:
      while True:
         # フレームをキャプチャ
         frame = picam2.capture_array()
         
         # YOLO検出を実行
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)
         
         # ターゲットオブジェクトを検索
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)
         
         # オブジェクトが見つかった場合の追跡処理
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move
               
               # サーボ角度を安全な範囲に制限
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))
               
               # サーボにコマンドを送信
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)
               
               # 検出フレームを描画
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30), 
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)
               
               status = f"{TARGET} 検出: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"{TARGET} 未検出"
               color = (0, 0, 255)
         
         # 中心に照準を描画
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         
         # デッドゾーン矩形を描画（視覚的参照）
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)
         
         # ステータス情報を表示
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"パン: {pan_pos:.0f} チルト: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"キャプチャ枚数: {capture_count}", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "スペース=キャプチャ ESC=終了", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         # ビデオウィンドウを表示
         cv2.imshow(f"YOLO追跡 - {TARGET}", frame)
         
         # キー入力を処理
         key = cv2.waitKey(1) & 0xFF
         
         if key == 32:  # スペースキー - 画像キャプチャ
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"キャプチャ: {filename}")
               capture_count += 1
               
               # フラッシュ効果
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO追跡 - {TARGET}", flash)
               cv2.waitKey(50)
               
         elif key == 27:  # ESCキー - 終了
               print(f"\n終了します。総キャプチャ枚数: {capture_count}")
               break

   finally:
      # -------------------- 後処理 --------------------
      print("後処理中...")
      pan.angle(0)      # 中央に戻す
      tilt.angle(0)     # 中央に戻す
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("追跡停止。サーボを中央に戻しました。")

パフォーマンス最適化
-----------------------------------------

Raspberry Pi上で追跡システムを実行する際、以下の最適化が役立ちます：

1. **検出頻度の低減**：2～3フレームに1回検出し、中間フレームでは検出結果を再利用

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       if frame_count % 3 == 0:
           results = model.predict(frame, imgsz=320)
       frame_count += 1

2. **検出領域の制限**：ターゲットが現れそうな領域のみを検出

3. **小さなモデルの使用**： ``yolov8n.pt`` が最適な選択

4. **デッドゾーン領域の調整**： ``DEADZONE`` を大きくするとサーボの頻繁な動作が減少

よくある質問
---------------------------------

**Q: サーボが動かない場合は？**

* サーボが正しく接続されているか確認
* fusion_hatライブラリが正しくインストールされているか確認

**Q: 追跡応答が遅すぎる場合は？**

* カメラ解像度を下げる（例：320x240）
* 検出解像度 ``imgsz`` を下げる
* デッドゾーン領域を広げてサーボの動作を減らす

**Q: ターゲット検出が不安定な場合は？**

* ``CONFIDENCE`` しきい値を調整（値を下げるとより多く検出するが、誤検出も増加）
* 十分な照明を確保
* より高い特異性のためにカスタムモデルを使用

**Q: サーボの感度を調整するには？**

``simple_track`` 関数のステップ値を変更します：

.. code-block:: python

   # より速いサーボ動作のためにステップ値を増やす
   pan_move = 2  # 元は1
   tilt_move = 2

**Q: 複数のターゲットを追跡できますか？**

``find_target_detection`` 関数を変更して、最も近いターゲットや最も信頼度の高いターゲットを返すようにするか、複数ターゲットの切り替え機能を実装します。

高度な機能
-----------------------------------

**1. PID制御の追加** （よりスムーズな追跡）

.. code-block:: python

   # 簡易PIDコントローラーの例
   pan_error = CX - obj_x
   pan_output = pan_error * 0.05  # 比例制御
   pan_pos += int(pan_output)

**2. 追跡軌跡の自動記録**

.. code-block:: python

   # ターゲット位置の履歴を記録
   trajectory = []
   trajectory.append((obj_x, obj_y))

**3. ターゲット検出時の通知送信**

.. code-block:: python

   if obj_x is not None:
       # メールやプッシュ通知を送信
       pass

**4. 顔認識の統合**

顔認識ライブラリと組み合わせて、特定の人だけを追跡

まとめ
---------------------

このチュートリアルを通して、以下を学びました：

* YOLO物体検出とサーボ制御を組み合わせる方法
* ビジョンベースの自動追跡システムを実装する方法
* 振動を避けるためのデッドゾーン機構の使用方法
* 追跡中にトレーニングデータを収集する方法

このシステムは、スマート監視、自動写真撮影、ロボットビジョンなどのシナリオで広く応用できます。YOLOモデルの進化に伴い、ターゲットのサイズに基づく自動ズーム調整や、動きの軌跡に基づくターゲット動作の予測など、さらにインテリジェントな追跡システムを構築することができます。