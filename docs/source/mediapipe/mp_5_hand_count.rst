.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. 手のジェスチャーカウント
==============================================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

前のセクションでは、リアルタイムの手検出と
ランドマークの可視化を実装しました。

このセクションでは、その機能を拡張し、
指のランドマーク位置を利用して
挙げられている指の本数（0～5）をカウントします。

指先と対応する関節の相対位置を分析することで、
各指が伸びているかどうかを判定できます。


.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. 動作の仕組み
------------------------------------------------------------

プログラムは次の手順で動作します：

1. MediaPipe Hands モデルを初期化する
2. Raspberry Pi カメラから映像フレームを取得する
3. リアルタイムで 21 個の手ランドマークを検出する
4. 指先の座標と対応する関節の座標を比較する
5. 各指が伸びているかどうかを判定する
6. 挙げられている指の本数をカウントする
7. 結果を動画フレーム上に表示する

この方法の特徴：

- 軽量で効率的
- Raspberry Pi に適している
- ジェスチャー制御やインタラクティブシステムの基礎となる

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. プログラムを実行すると、「Show Video」というタイトルのウィンドウが開き、カメラのライブ映像が表示されます。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   カメラの前に手が現れると：

   - MediaPipe がリアルタイムで手を検出します
   - 手に 21 個のランドマークと接続線が描画されます
   - プログラムが指先と関節の位置を解析します
   - 挙げられている指の本数（0～5）が計算されます

   検出された指の本数は画面左上に次のように表示されます：

      Fingers: X

   指を伸ばしたり曲げたりすると、
   数値はリアルタイムで更新されます。

   手が検出されない場合は、
   指のカウント表示なしで通常のカメラ映像のみが表示されます。

   ``q`` を押すとプログラムを終了できます。
   カメラは停止し、OpenCV ウィンドウは自動的に閉じます。



-----------------------------
4. 完全なコード
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2 
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections on the frame
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
               )


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

各ループで 5 本の指が伸びているかどうかを判定し、
伸びている指の数をカウントします。例：

- ✊ すべての指を閉じる → 0
- ☝️ 人差し指のみ → 1
- ✌️ 人差し指＋中指 → 2
- 🖐️ 5 本すべて開く → 5

--------------------------------------------------------------
5. 検出ロジックと拡張
--------------------------------------------------------------

MediaPipe Hands は 21 個のランドマークを返します。
指先と関節の位置を利用して、
各指が伸びているかどうかを判定します。

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → 指先のランドマークインデックス  
  (Thumb=4, Index=8, Middle=12, Ring=16, Pinky=20)

- ``finger_dips`` → 対応する関節のランドマークインデックス  
  (Thumb=2, Index=6, Middle=10, Ring=14, Pinky=18)

------------------------------------------------------------

指カウントのロジック：

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

ロジック説明：

- **親指** → ``tip.x`` と ``dip.x`` を比較（右手の場合）
- **他の指** → ``tip.y`` と ``dip.y`` を比較
- 指先が関節より上（または外側）にある場合、
  その指は伸びていると判断されます
- 条件を満たすたびに ``+1`` されます

------------------------------------------------------------

拡張のヒント：

- 左手と右手の両方に対応する場合は、
  ``hands_detected.multi_handedness`` を使用して
  手の種類を判定し、
  親指の x 軸比較を反転させます。

- このロジックは次のような機能にも拡張できます：

  - OK ジェスチャー認識
  - サムズアップ検出
  - じゃんけんインタラクション
  - カスタムジェスチャー操作

------------------------------------------------------------
6. トラブルシューティング
------------------------------------------------------------

- 親指の検出が不正確

  親指は左右の手で判定ロジックが異なるため、
  検出が不正確になることがあります。

  ``multi_handedness`` を使用して
  左手か右手かを判定し、
  親指の検出ロジックを調整してください。

- 検出が不安定

  指のカウントが不安定な場合、
  照明不足または背景が複雑な可能性があります。

  照明を改善し、シンプルな背景を使用すると
  検出の安定性が向上します。

- 遅延が大きい

  応答が遅い場合、
  解像度が高すぎるか CPU 負荷が高い可能性があります。

  解像度を下げ（例：320×240）、
  不要なバックグラウンドプロセスを終了してください。
  必要に応じて指カウントロジックを簡略化することもできます。


-----------------------------
7. まとめ
-----------------------------

- MediaPipe Hands を使用すると **リアルタイムジェスチャー認識** を簡単に実装できます。
- 本セクションでは **指の本数ジェスチャー認識** を実装し、
  カスタムジェスチャー認識の基礎を構築しました。
- 左右の手への対応や判定ルールを拡張することで、
  より高度なインタラクションシステムを実装できます。