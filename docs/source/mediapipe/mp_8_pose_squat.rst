.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. スクワットカウンター
==========================================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

前の章では、基本的な人体姿勢推定を実装しました。  
この章では、その基礎の上に **MediaPipe Pose** を用いた
シンプルな **スクワットカウンター** を実装します。

これは次の要素を組み合わせた実用的な例です：

- 姿勢検出
- 動作認識
- リアルタイムカウント

スマートフィットネスシステム、  
ホームトレーニングアシスタント、  
または動作解析アプリケーションに活用できます。

.. image:: img/mp_pose_s2.png
   :alt: Squat Count Example
   :align: center


------------------------------------------------------------
2. 動作の仕組み
------------------------------------------------------------

スクワットカウンターは、次のロジックで実装されています：

1. MediaPipe Pose を使用して 33 個の身体キーポイントを検出する
2. 主要な関節（肩・腰・足首）を選択する
3. 正規化された y 座標を使って腰の高さを推定する
4. 上側と下側の閾値を設定する（例：0.55 と 0.45）
5. シンプルな状態遷移で  
   「立つ → しゃがむ → 立つ」  
   を検出する
6. スクワット 1 回分の動作が完了したらカウンタを増やす
7. スクワット回数と現在の腰位置を画面に表示する

.. note::

   - このサンプルでは関節角度の計算は使用しません。
   - 計算量を減らすため、正規化座標を利用しています。
   - この方法は軽量で、Raspberry Pi に適しています。

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

#. プログラムを実行すると、「Show Video」というタイトルのウィンドウが開き、ライブカメラ映像が表示されます。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_8.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   カメラの前に人が立つと：

   - MediaPipe Pose が 33 個の身体ランドマークをリアルタイムで検出します。
   - 全身骨格が画面上に描画されます。
   - システムは腰の相対位置（HipRel）を継続的に計算します。

   スクワットを行うと：

   - 体を下げて腰が下側の閾値（DOWN_TH）を超えると、
     システムは「しゃがみ込み位置」に入ったと判断します。
   - そこから再び立ち上がり、腰が上側の閾値（UP_TH）を超えると、
     スクワット回数が 1 増加します。

   画面には次の情報が表示されます：

   - ``Squats: N`` — 完了したスクワットの総回数
   - ``HipRel: value`` — 判定に使用している現在の正規化腰位置

   カウンタは、完全な 1 サイクル
   （立つ → しゃがむ → 立つ）
   が完了した後にのみ増加するため、重複カウントを防げます。

   ``q`` を押すとプログラムを終了できます。  
   カメラは停止し、OpenCV ウィンドウは自動的に閉じます。


-----------------------------
4. 完全なコード
-----------------------------

以下がスクワットカウンターの完全な実装です：

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

スクリプトを実行すると、システムは次の処理を行います：

- 人体骨格を検出する
- 腰の相対位置を計算する
- 「しゃがむ → 立つ」の完全な動作サイクルが完了すると +1 する
- 画面上に **Squats: N** と現在の HipRel 値をリアルタイムで表示する

-----------------------------------------------
5. 座標と状態設計
-----------------------------------------------

ここでは次の 6 つのキーポイント（左右 3 点ずつ）を使用します：

.. list-table::
   :header-rows: 1

   * - Keypoint
     - Index
     - Description
   * - Shoulder
     - 11 (Left) / 12 (Right)
     - 上側の基準点
   * - Hip
     - 23 (Left) / 24 (Right)
     - スクワット位置計算の中心となる点
   * - Ankle
     - 27 (Left) / 28 (Right)
     - 下側の基準点

.. image:: img/mp_pose_s1.png
   :alt: MediaPipe Pose Keypoints
   :align: center

**Hip Relative** 値の計算式：

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- hip_rel が大きいほど、腰は地面に近い位置にあります（つまり深くしゃがんでいる状態）。
- hip_rel が小さいほど、立ち上がった姿勢に近くなります。

ここでは 2 つの閾値を定義します：

- **DOWN_TH = 0.55**: スクワットの最下部に入ったとみなす
- **UP_TH = 0.45**: 立ち上がり動作に戻ったとみなす

信頼性の高いカウントのために、シンプルな状態機械を使用します：

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
6. パラメータ調整と最適化
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Adjustment Suggestion
   * - DOWN_TH
     - スクワット判定の閾値
     - 値を高くすると、より深くしゃがまないとカウントされない
   * - UP_TH
     - 立ち上がり判定の閾値
     - 値を低くすると、よりしっかり立ち上がらないと判定されない
   * - model_complexity
     - Pose モデルの複雑度
     - 高速化のため 1 を推奨
   * - Resolution
     - フレームレートと精度に影響する
     - 640×480 を推奨

.. tip::
   身長や体型が異なる人に対しては、適応型閾値や個別キャリブレーションを使用すると、より正確なカウントが可能になります。

---------------------------------------------------------
5. トラブルシューティング
---------------------------------------------------------

- カウントが不正確

  スクワット回数が正確にカウントされない場合、閾値があなたの体の位置やカメラ角度に合っていない可能性があります。 
  
  ``hip_rel`` をリアルタイムで表示しながら、``DOWN_TH`` と ``UP_TH`` を調整してください。  
  また、スクワット動作が安定しており、はっきり見えるようにしてください。

- 人物が検出されない

  人体が検出されない場合は、照明条件を改善し、複雑な背景を避けてください。 
  
  全身がフレーム内に入っていること、そしてカメラに正面を向いていることを確認してください。

- 遅延が大きい

  動画の応答が遅い場合は、 ``model_complexity`` を 1 に下げ、カメラ解像度も下げてください（例：640×480 または 320×240）。
  
  不要なバックグラウンドプログラムを終了すると、パフォーマンスが改善します。

-----------------------------
6. まとめ
-----------------------------

- Pose キーポイント + 状態機械を用いた **リアルタイムスクワットカウンター** を実装しました
- 複雑な角度計算は不要で、動作効率が高いです
- Raspberry Pi などのエッジデバイスに適しています
- 今後はさらに次のような拡張が可能です：

  - 腕立て伏せ / 腹筋の検出
  - データ記録と可視化
  - 自動リズムガイドやトレーニングフィードバック