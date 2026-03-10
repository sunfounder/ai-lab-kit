.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. 手の検出（Hand Detection）
===============================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

前のセクションでは、MediaPipe を使用した顔検出と
ランドマーク追跡を実装しました。

このセクションでは **MediaPipe Hands** を紹介します。
これは軽量で安定したリアルタイム手ランドマーク検出モジュールです。

このモジュールを使用すると、次のことが可能になります：

- 最大 2 つの手を同時に検出
- 各手につき 21 個のランドマークを識別
- 手の骨格接続をリアルタイムで可視化

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. 動作の仕組み
------------------------------------------------------------

プログラムは次の手順で動作します：

1. MediaPipe Hands モデルを初期化する
2. Raspberry Pi カメラからフレームを取得する
3. 画像を RGB 形式に変換する（MediaPipe の要件）
4. Hands モジュールを使用して手のランドマークを検出する
5. 21 個のランドマークとその接続線を描画する
6. 注釈付きの映像ストリームをリアルタイムで表示する

このモジュールは次の機能の基盤になります：

- ジェスチャー認識
- 指の本数カウント
- インタラクティブ制御システム
- 非接触型ヒューマンコンピュータインタラクション

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. プログラムを実行すると、「Show Video」というタイトルのウィンドウが開き、カメラのライブ映像が表示されます。

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
   
   カメラの前に 1 つまたは 2 つの手が現れると：

   - MediaPipe がリアルタイムで各手を検出します。
   - 各手に対して 21 個のランドマークを識別します。
   - ランドマークを線で接続し、手の骨格を表示します。
   
   2 つの手が見える場合、両方の手が同時に追跡され、
   画面上に表示されます。
   
   ユーザーが手や指を動かすと：

   - ランドマークポイントが動きに滑らかに追従します。
   - 手の骨格表示がリアルタイムで更新されます。
   
   手が検出されない場合、プログラムは
   注釈のない通常のカメラ映像を表示します。
   
   ``q`` を押すとプログラムを終了できます。
   カメラは停止し、OpenCV ウィンドウは自動的に閉じます。

-----------------------------
4. 完全なコード
-----------------------------

完全なサンプルコードは以下の通りです：

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

コードを実行すると、カメラ映像に次の内容が表示されます：

- 1 つまたは 2 つの手が検出された場合：

  - 21 個の手ランドマーク
  - 青い接続線による骨格表示

- 手が動くと、検出結果はリアルタイムで追跡されます。

--------------------------------------------------------
5. MediaPipe Hands ランドマークの説明
--------------------------------------------------------

MediaPipe Hands は各手について **21 個のランドマーク** を返します。
これには手首、手のひら、指先などの位置が含まれます。

代表的なランドマーク：

.. list-table::
   :header-rows: 1

   * - Index
     - Name
     - Location
   * - 0
     - WRIST
     - 手首
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - 各指の先端
   * - 5~17
     - Joints
     - 各指の中間関節
   * - 9
     - PALM_CENTER (approximate)
     - 手のひら付近

.. image:: img/mp_hand_point.png
  :width: 400
  :alt: MediaPipe Hands Landmarks Illustration
  :align: center

.. note::
   これらの座標は **正規化座標** であり、画像の解像度に基づいて
   実際のピクセル座標へ変換できます。  
   角度や距離の計算に利用でき、ジェスチャー認識などに応用できます。

------------------------------------------------------------
6. トラブルシューティング
------------------------------------------------------------

- 手の検出が不安定

  照明が暗すぎる、背景が複雑、または手の動きが速すぎる場合、
  検出が不安定になることがあります。
  
  照明を改善し、背景をシンプルにし、手をゆっくり安定して動かしてください。

- 手が検出されない

  カメラの角度が適切でない、手がカメラから遠すぎる、
  または解像度が低すぎる可能性があります。
  
  カメラ位置を調整し、手をカメラに近づけ、
  解像度が少なくとも 640×480 であることを確認してください。

- 遅延が大きい

  動画の反応が遅い場合、Raspberry Pi の負荷が高い、
  または解像度が高すぎる可能性があります。
  
  解像度を下げ（例：320×240）、不要なバックグラウンドプロセスを終了してください。


-----------------------------
7. まとめ
-----------------------------

- MediaPipe Hands は Raspberry Pi 上で安定した **リアルタイム手検出** を実現します。
- 各手に対して 21 個のランドマークを提供し、次の用途に適しています：

  - ジェスチャー認識
  - 仮想操作
  - インタラクティブ UI 制御
  
- 次の章では、これらのランドマークを利用した **カスタムジェスチャー認識** を実装します。