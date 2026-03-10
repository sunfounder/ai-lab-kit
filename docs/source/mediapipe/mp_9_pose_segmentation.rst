.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. グリーンスクリーン
====================================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

この章では、MediaPipe Pose の **人物セグメンテーション** 機能を使って、
シンプルな **グリーンスクリーン効果** を実装します。

人物と背景を分離することで、
元の背景を単色のグリーンに置き換えることができます。
これにより、次のような用途に応用できます：

- バーチャル背景アプリケーション
- クロマキー合成（OBS / NLE）
- ライブ配信エフェクト
- AR 風のシーン置換

.. image:: img/mp_pose_green.png
   :align: center


------------------------------------------------------------
2. 動作の仕組み
------------------------------------------------------------

グリーンスクリーン効果は、次の手順で実装されます：

1. ``enable_segmentation=True`` で Pose モデルを初期化する
2. 各フレームについて ``results.segmentation_mask`` を取得する
3. マスクは単一チャンネルの確率マップ（範囲 0～1）である
4. 閾値（例：0.5）を適用して前景と背景を分離する
5. 背景ピクセルを単色のグリーンに置き換える
6. 必要に応じて、ぼかしやモルフォロジー処理で境界を滑らかにする

この方法は軽量で、Raspberry Pi 上でもリアルタイムに動作し、
人物セグメンテーションの実用例としても分かりやすい構成です。

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

   録画済み動画に対して MediaPipe Pose を使用したい場合は、次のコマンドを実行できます：

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

#. プログラムを実行すると、「Show Video」というタイトルのウィンドウが開き、ライブカメラ映像が表示されます。

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_9.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   同じウィンドウ内に ``Mask`` という名前のトラックバーも表示されます。  

   これはセグメンテーションの閾値（0～100）を調整するもので、デフォルト値は 50（0.5）です。

   カメラの前に人物が現れると：

   - MediaPipe Pose が各フレームに対して ``segmentation_mask`` を生成します。
   - マスク値が閾値を超えるピクセルは前景（人物）として扱われます。
   - それ以外のピクセルは単色のグリーン背景に置き換えられます。

   ``Mask`` トラックバーを動かすと：

   - 閾値を上げると、信頼度の高い前景領域だけが残ります  
     （背景漏れは減りますが、体の一部が欠けることがあります）
   - 閾値を下げると、より多くのピクセルが前景に含まれます  
     （シルエットは完全になりやすいですが、背景ノイズも入りやすくなります）

   セグメンテーションマスクが利用できない場合は、
   背景置換を行わず、通常のカメラ映像のみを表示します。

   ``q`` を押すとプログラムを終了できます。  
   カメラは停止し、OpenCV ウィンドウは自動的に閉じます。

-----------------------------
4. 完全なコード
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: empty callback for trackbars ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

スクリプトを実行すると、人物（前景）は保持され、
背景は単色のグリーンに置き換えられます。  
そのまま OBS、Premiere、DaVinci Resolve などで **Chroma Key** による後処理に利用できます。

-------------------------------------
5. 重要ポイントの解説
-------------------------------------

``segmentation_mask`` は、入力フレームと同じサイズの  
**単一チャンネル float 画像** （範囲 0～1）です：

- 値が **1 に近い** ： **前景（人物）** である確率が高い
- 値が **0 に近い** ： **背景** である確率が高い

一般的には、閾値 **T** （例：0.5）を設定し、
条件マスクを作成します：

.. code-block:: python

   condition = (mask > T)[..., None]

ここではトラックバーを使って、閾値をリアルタイムで調整できるようにしています：

.. code-block:: python

   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

その後、 ``np.where(condition, frame, background)`` を使って背景を置き換えます。  
このサンプルではグリーン背景に置き換えています：

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
6. 表示効果と境界最適化
----------------------------------------------------

単純な二値化だけでは、髪の毛や服の縁にギザギザや小さな穴が生じることがあります。  
**軽い後処理** を加えることで、境界をより自然にできます：

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **推奨 T 値の範囲は 0.3～0.7**：暗い環境や保守的なモデルでは少し下げ、ノイズが多い場合は上げるとよいです。
   - ぼかしカーネルを大きくしすぎると、人物の境界にグリーンがにじみやすくなります。

----------------------------------------------------
7. カスタム背景（画像 / 動画）の使用
----------------------------------------------------

単色のグリーンではなく、任意の背景画像に置き換えることもできます：

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

別の動画を背景として使うことも可能です  
（次のフレーム ``bg_frame`` を読み込み、同じサイズにリサイズしてから置き換えます）。

----------------------------------------------------
8. パフォーマンスと画質のバランス
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Item
     - Impact
     - Suggestion
   * - Resolution
     - 解像度が高いほど境界は細かくなるが速度は遅くなる
     - まずは 640×480 で開始し、必要なら上げる
   * - model_complexity
     - 高いほど精度は上がるが遅くなる
     - Raspberry Pi では 1～2 を推奨
   * - Post-processing strength
     - ぼかしやモルフォロジーが強すぎると境界が潰れたりグリーン漏れが発生する
     - 小さなカーネル + 少ない反復回数で様子を見る

------------------------------------------------------------
9. トラブルシューティング
------------------------------------------------------------

- 人物の周囲にギザギザや境界線が見える

  これは通常、マスクに硬い閾値を適用しているため、境界が急になっていることが原因です。  
  
  ``Mask`` トラックバーで閾値を調整してみてください。より滑らかな境界にしたい場合は、合成前にセグメンテーションマスクへ軽いぼかしや簡単なモルフォロジー閉処理を加えてください。

- 人物の一部が欠ける

  体の一部が切り取られてしまう場合、照明が弱すぎるか、服の色が背景と混ざっている可能性があります。  
  
  照明を改善し、閾値を調整し、被写体とのコントラストが高いシンプルな背景を使用してください。

- フレームレートが低い

  動画が遅く感じる場合、解像度が高すぎるか、モデルが重すぎる可能性があります。  
  
  カメラ解像度を下げ（例：640×480 または 320×240）、 ``model_complexity`` は 1 にするとパフォーマンスが向上します。

- グリーンが人物側にはみ出す

  グリーン背景が人物にかぶって見える場合、セグメンテーション境界が不正確か、被写体の色によって視覚的な混乱が生じている可能性があります。  
  
  置き換え色をグリーン以外（ブルーやグレー）に変更するか、単色ではなく背景画像に置き換えることで、より自然な見た目になります。


-----------------------------
10. まとめ
-----------------------------

- ``segmentation_mask`` を使うことで、「人物切り抜き + 背景置換」を素早く実現できます
- 閾値調整と軽い後処理によって、より自然な境界を得られます
- バーチャル背景、ライブ配信のクロマキー、遠隔授業などに適しています
- 次のステップとして、 **姿勢骨格** と **セグメンテーション** を組み合わせれば、より高度なインタラクティブ効果も実装できます
  （例：背景だけを置き換え、前景の骨格オーバーレイはそのまま残す）