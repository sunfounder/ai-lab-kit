.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. 顔輪郭と虹彩検出（Facial Contours and Iris Detection）
=================================================================

------------------------------------------------------------
1. 概要
------------------------------------------------------------

これまでのセクションでは、基本的な Face Mesh 検出と  
シンプルな表情認識を実装しました。

このセクションでは、MediaPipe FaceMesh が提供する  
より詳細な特徴接続方法に焦点を当てます：

- ``FACEMESH_CONTOURS`` — 顔の輪郭線を描画  
  （顔の外周や主要な特徴の境界）

- ``FACEMESH_IRISES`` — 両目の虹彩領域を描画

輪郭と虹彩のみを描画することで、可視化がよりシンプルで軽量になります。  
これは次のような用途に適しています：

- 顔特徴の抽出
- 視線追跡
- 瞳孔追跡
- 視線インタラクション

.. image:: img/mp_face_iris.png
   :align: center

------------------------------------------------------------
2. 動作原理
------------------------------------------------------------

プログラムは次の手順で処理を行います：

1. MediaPipe FaceMesh モデルを初期化する  
2. Raspberry Pi カメラから動画フレームを取得する  
3. 画像を RGB 形式に変換する（MediaPipe の要求）  
4. ``FACEMESH_CONTOURS`` を使用して顔の輪郭線を描画する  
5. ``FACEMESH_IRISES`` を使用して虹彩ランドマークを描画する  
6. 主要部分のみを表示して、より見やすい可視化を行う  

------------------------
3. コードの実行
------------------------

.. important::

   開始する前に、次の項目を確認してください：

   * パンチルト機構が組み立てられている
   * Raspberry Pi のデスクトップにアクセスできる
   * コードパッケージがインストールされている
   * Fusion HAT+ がインストールおよび設定されている
   * OpenCV がインストールされている


   詳細な手順については :ref:`opencv_install` を参照してください。

#. ターミナルを開き、次のコマンドを入力します：

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

#. プログラムを実行すると、「Show Video」というタイトルのビデオウィンドウが開き、カメラのライブ映像が表示されます。

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_3.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>
         
   カメラの前に顔が現れると：

   - MediaPipe が顔ランドマークをリアルタイムで検出します。  
   - 顔の輪郭線（顔の外周、眉、唇など）のみが描画されます。  
   - 両目の虹彩領域が円形のランドマーク接続で強調表示されます。  

   フル Face Mesh と異なり、画面には主要な輪郭と虹彩のみが表示されるため、  
   可視化がよりシンプルで見やすくなります。

   ユーザーが頭や目を動かすと：

   - 輪郭線が顔の動きに滑らかに追従します。  
   - 虹彩ランドマークが目の動きをリアルタイムで追跡します。  

   顔が検出されない場合は、通常のカメラ映像のみが表示され、  
   注釈は描画されません。

   ``q`` を押すとプログラムを終了できます。  
   カメラは停止し、OpenCV ウィンドウは自動的に閉じます。

-----------------------------
4. 完全なコード
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize FaceMesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Enable if hardware preview is needed
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      if results.multi_face_landmarks:
         for face_landmarks in results.multi_face_landmarks:
            # Draw facial contours
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_CONTOURS,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            # Draw iris features
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

プログラムを実行すると、画面には顔の輪郭と両目の虹彩領域のみが表示されます。

-----------------------------
5. 主要ステップの解説
-----------------------------

このセクションのコードは :ref:`mp_face` とほぼ同じです。

主な違いは、メインループ内で使用する描画方法です。  
``draw_landmarks()`` 関数が 2 回呼び出されます：

- 1 回目： ``FACEMESH_CONTOURS``  
- 2 回目： ``FACEMESH_IRISES``  

どちらかの描画ブロックをコメントアウトすると、  
表示結果の違いを確認できます。

------------------------------------------------------------

``FACEMESH_CONTOURS``

- MediaPipe が提供する接続セットです。  
- 主に次の要素を描画します：

  - 顔の外周
  - 目の輪郭
  - 鼻の輪郭
  - 唇の輪郭

この方法により、顔輪郭の変化を観察しやすい  
簡略化された可視化が得られます。

------------------------------------------------------------

``FACEMESH_IRISES``

- 両目の虹彩領域を描画します。  
- 虹彩のキーポイントと円形の接続線が含まれます。  
- 次の用途に適しています：

  - 視線追跡
  - 瞳孔追跡
  - 視線検出

------------------------------------------------------------

``landmark_drawing_spec=None``

- 個々のランドマーク点の描画を無効にします。  
- 接続線のみが表示されるため、  
  よりシンプルで見やすい表示になります。

点と線の両方を表示したい場合は、  
カスタム ``DrawingSpec`` を定義してください。

------------------------------------------------------------

``drawing_styles.get_default_face_mesh_contours_style()``

- デフォルトの輪郭描画スタイルを返します。

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- デフォルトの虹彩接続線スタイルを返します。


------------------------------------------------------------
6. トラブルシューティング
------------------------------------------------------------

- 虹彩が検出されない

  虹彩が検出されない場合、照明が不足している、  
  顔がカメラから遠すぎる、または ``refine_landmarks`` が  
  有効になっていない可能性があります。

  照明を改善し、カメラに近づき、  
  FaceMesh 初期化時に ``refine_landmarks=True`` が  
  設定されていることを確認してください。

- 輪郭線が不安定

  輪郭線が揺れる場合、検出信頼度が低すぎる、  
  または照明や頭の動きが追跡に影響している可能性があります。

  ``min_detection_confidence`` を高く設定し、  
  照明を改善し、頭の動きをゆっくり滑らかにしてください。

- 遅延が大きい

  映像の応答が遅い場合、解像度が高すぎる、  
  または ``refine_landmarks`` が追加の計算負荷を  
  発生させている可能性があります。

  解像度を下げる（例：320×240）か、  
  虹彩検出が不要な場合は ``refine_landmarks`` を無効にしてください。

-----------------------------
7. まとめ
-----------------------------

- ``FACEMESH_CONTOURS`` と ``FACEMESH_IRISES`` は MediaPipe が提供する重要な接続方法です。
- フルメッシュ描画と比べて軽量で直感的なため、実用的なインタラクション用途に適しています。
- 次の章では、これらの機能を利用した視線追跡や瞬き検出の方法を紹介します。