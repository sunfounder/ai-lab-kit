.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. 顔検出（Face Detection）
===========================

このセクションでは、**Raspberry Pi** 上で **MediaPipe Face Mesh** モジュールを使用し、リアルタイムの顔検出と顔ランドマークメッシュ描画を行う方法を紹介します。

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe は Google が開発したクロスプラットフォームの機械学習パイプラインフレームワークで、動画ストリームや画像をリアルタイムで処理することができます。Face Mesh モジュールは MediaPipe が提供するモデルの一つで、リアルタイムの顔検出とランドマーク追跡を行い、さまざまな顔認識やインタラクションアプリケーションを構築することが可能です。

OpenCV の Haar 検出と比較して、MediaPipe はディープラーニングモデルを使用して検出を行うため、次のような利点があります：

- より高い検出精度
- 照明や角度の変化に対して高いロバスト性
- 顔ランドマーク追跡（468 点）に対応
- OpenCV とシームレスに統合でき、検出結果を動画ストリーム上に直接描画可能

------------------------
1. コードの実行
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
   
      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. スクリプトを実行すると、OpenCV が「Show Video」というタイトルのウィンドウを開き、Raspberry Pi カメラから取得したライブ映像を表示します。

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   * カメラの前に顔が現れると、プログラムが自動的に検出し、顔の上に詳細なランドマークメッシュをリアルタイムで描画します。人が動いたり、まばたきをしたり、表情が変化しても、メッシュは滑らかに追従します。
   * 顔が検出されない場合は、ウィンドウには通常のカメラ映像のみが表示され、ランドマークは描画されません。
   
   動画ストリームはユーザーがプログラムを終了するまで継続して実行されます。  
   プログラムを終了するには、キーボードの ``q`` を押してください。  
   カメラは停止し、OpenCV のリソースも自動的に解放されます。

------------------------
2. コード例
------------------------

完全なコードは以下の通りです：

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the mp_face_mesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,          # Set to False for video streams
       max_num_faces=1,                  # Maximum number of faces to detect
       refine_landmarks=True,           # Whether to refine landmarks
       min_detection_confidence=0.5     # Detection confidence threshold
   )

   # Open Raspberry Pi camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 → BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert BGR to RGB (MediaPipe requires RGB)
       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # Face detection and landmark tracking
       results = face.process(frame)

       # Convert RGB back to BGR (for OpenCV display)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       # Draw detected facial landmarks
       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

プログラムを実行すると、ライブカメラ映像が表示され、顔が検出されると自動的に顔メッシュが描画されます。

-----------------------------
3. 主要ステップの解説
-----------------------------

#. ライブラリのインポート

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   これらのライブラリは以下の用途で使用されます：

   - Raspberry Pi カメラの制御
   - 画像の処理と表示
   - 顔ランドマークの検出

#. FaceMesh の初期化

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   これにより顔検出モデルが作成されます。  
   動画モードで 1 人の顔を継続的に追跡します。

#. カメラの起動

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   カメラは 640×480 の解像度でストリーミングを開始します。

#. ループでフレームを取得

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   各ループで 1 フレームを取得し、OpenCV 用の形式に変換します。

#. 顔ランドマークの検出

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   フレームを RGB に変換し、MediaPipe が画像を解析して顔ランドマークを検出します。

#. 顔メッシュの描画

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   顔が検出された場合、その上にメッシュを描画します。

#. 結果の表示と終了

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   ``q`` を押すとプログラムが終了し、カメラも自動的に停止します。

---------------------------------------------
4. よくある問題とトラブルシューティング
---------------------------------------------

* カメラが開けない

  * CSI カメラケーブルが正しく接続されているか確認してください
  * カメラインターフェースを有効にします：

    ``sudo raspi-config`` → Interface Options → Camera

  * 有効化後は Raspberry Pi を再起動してください

* プログラムの起動が遅い

  初回実行時は MediaPipe モデルを読み込むため、数秒かかる場合があります。  
  これは正常な動作で、2 回目以降はより高速に起動します。

* 検出が不安定 / 遅延がある

  * カメラ解像度を下げる（例：320×240）
  * CPU 使用率を下げるため ``refine_landmarks`` を無効にする
  * 他のプログラムを終了する

* ``mediapipe`` モジュールが見つからない

  MediaPipe をインストールしてください：

  .. code-block:: bash

     pip install mediapipe

  64-bit の Raspberry Pi OS を使用していることを確認してください。

-----------------------------
5. まとめ
-----------------------------

- MediaPipe FaceMesh はディープラーニングモデルを使用して Raspberry Pi 上で高精度な顔検出を実現します
- OpenCV と非常に密接に統合されています
- 表情認識、アバター追跡、AR アプリケーションなどの用途に適しています
- 従来の Haar 特徴量ベースの方法よりも堅牢で拡張性があります

次のセクションでは、**Face Mesh のランドマークを利用した簡単な顔特徴分析とインタラクション** を紹介します。