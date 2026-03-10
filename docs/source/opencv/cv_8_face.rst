.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

8. 顔と目の検出
=========================================

この章では、Raspberry Pi の Picamera2 を使って映像を取得し、OpenCV の Haar 特徴分類器を用いて **リアルタイムの顔検出と目の検出** を行います。  
この方法は軽量で実用性が高く、Raspberry Pi 上での導入を始める初学者にも適しています。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_8.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Haar 特徴と検出の原理
-----------------------------------------

1. Haar 特徴の本質

Haar 特徴は、物体検出に使われる古典的な手法です。画像領域内の **明るさの差のパターン** を表現することで、その領域に顔や目などが含まれている可能性を判断します。

代表的な Haar 特徴の例：

- 目の領域は、上にある額よりも暗いことが多い  
- 鼻筋の左右では、明るさが対称になりやすい  
- 口の下には、はっきりしたエッジパターンが現れやすい  

.. image:: img/opencv_haar_f.png
   :alt: Illustration of Haar features
   :align: center

OpenCV では、事前学習済みの Haar 分類器（ ``.xml`` ファイル）が必要です。これらはすでにサンプルディレクトリに含まれているため、そのまま読み込んで使用できます。

2. 検出パイプライン

   1. ``CascadeClassifier`` を使って学習済み Haar モデルを読み込む  
   2. リアルタイム映像をグレースケールに変換する（処理効率向上のため）  
   3. ``detectMultiScale`` を使って顔や目の領域を検出する  
   4. 検出された対象の周囲に矩形を描画する  

.. image:: img/opencv_haar_show.png
   :alt: Detection pipeline illustration
   :align: center


2. コードの実行
------------------------

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
      python3 cv_8_haarcascade.py

   .. tip::
      
      動画ファイルから顔と目を検出するための ``cv_8_haarcascade_video.py`` も用意しています。

#. プログラムを実行すると、 **Raspberry Pi Camera - Face Detection** という名前のウィンドウが表示され、Raspberry Pi Camera のライブ映像が映し出されます。

   映像内で検出された顔は **黄色の矩形** で囲まれ、それぞれの顔には ``Face 1``、 ``Face 2`` ... のようにラベルが付けられます。  
   また、各顔領域の内部では目も検出され、 **オレンジ色の矩形** で表示されます。
   
   検出はリアルタイムで行われ、人がカメラの前で動くと矩形もそれに追従して移動します。
   
   プログラムを停止するには、次のいずれかを行ってください：
   
   * キーボードの **q** キーを押す  
   * ウィンドウ右上の閉じるボタン（X）でウィンドウを閉じる  
   
   終了後は、カメラが停止し、OpenCV のウィンドウもすべて閉じられます。


3. 完全なコード
-------------------


.. code-block:: python

   # Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
   import cv2
   from picamera2 import Picamera2
   from pathlib import Path

   # -----------------------------
   # Load Haar cascade classifiers
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent

   face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
   eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   # Check if cascade files are loaded correctly
   if face_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
   if eye_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   # -----------------------------
   # Initialize Picamera2
   # -----------------------------
   picam2 = Picamera2()

   # Video configuration (resolution can be adjusted)
   config = picam2.create_video_configuration(main={"size": (640, 480)})
   picam2.configure(config)
   picam2.start()

   WIN = "Raspberry Pi Camera - Face Detection"
   print("Camera started. Press 'q' to quit.")

   try:
      while True:
         # Capture a frame (Picamera2 typically provides RGB)
         frame_rgb = picam2.capture_array()

         # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
         gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

         # Improve contrast to make detection more stable under different lighting
         gray = cv2.equalizeHist(gray)

         # Detect faces
         faces = face_cascade.detectMultiScale(
               gray,
               scaleFactor=1.2,
               minNeighbors=5,
               minSize=(60, 60)
         )

         # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
         frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

         # Draw face and eye results
         for i, (x, y, w, h) in enumerate(faces, start=1):
               # Draw face rectangle + label
               cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
               cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

               # ROI for eye detection (search eyes only inside the detected face area)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = frame_bgr[y:y + h, x:x + w]

               eyes = eye_cascade.detectMultiScale(
                  roi_gray,
                  scaleFactor=1.2,
                  minNeighbors=8,
                  minSize=(20, 20)
               )

               # Draw up to 2 eyes (typical for a face)
               for (ex, ey, ew, eh) in eyes[:2]:
                  cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

         # Show the frame
         cv2.imshow(WIN, frame_bgr)

         # Handle keyboard input
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
               break

         # Exit if the user closes the window (click X)
         if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
               break

   finally:
      picam2.stop()
      cv2.destroyAllWindows()
      print("Camera stopped.")

4. コード解説
----------------------

#. 必要なライブラリをインポートする：

   .. code-block:: python

      import cv2
      from picamera2 import Picamera2
      from pathlib import Path

   OpenCV は検出と描画に使用し、Picamera2 は Raspberry Pi カメラからフレームを取得するために使用します。

#. 現在のスクリプトのディレクトリを取得する：

   .. code-block:: python

      BASE_DIR = Path(__file__).resolve().parent

   これにより、Python スクリプトと同じフォルダにある cascade XML ファイルを読み込めます。

#. Haar 分類器（顔と目）を読み込む：

   .. code-block:: python

      face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
      eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   Haar Cascade は、顔や目を検出するために事前学習されたモデルです。

#. Cascade ファイルが正しく読み込まれたか確認する：

   .. code-block:: python

      if face_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
      if eye_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   パスが間違っていたり、ファイルが存在しない場合、 ``CascadeClassifier`` は空になります。  
   この確認を行うことで、問題を早い段階で見つけやすくなります。

#. カメラを初期化し、解像度を設定する：

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_video_configuration(main={"size": (640, 480)})
      picam2.configure(config)
      picam2.start()

   これにより、640×480 のビデオモードでカメラが起動します。

#. フレームを連続して取得する：

   .. code-block:: python

      frame_rgb = picam2.capture_array()

   ループごとに 1 フレームを取得します。Picamera2 は通常 RGB 形式のフレームを返します。

#. グレースケールへ変換する（検出を高速化するため）：

   .. code-block:: python

      gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

   顔検出や目検出はグレースケール画像で動作し、カラー画像よりも高速です。

#. コントラストを改善して検出を安定させる：

   .. code-block:: python

      gray = cv2.equalizeHist(gray)

   ヒストグラム平坦化を行うことで、異なる照明条件でも検出結果が安定しやすくなります。

#. フレーム内の顔を検出する：

   .. code-block:: python

      faces = face_cascade.detectMultiScale(
          gray,
          scaleFactor=1.2,
          minNeighbors=5,
          minSize=(60, 60)
      )

   これにより、検出されたすべての顔について ``(x, y, w, h)`` の矩形リストが返されます。

   - ``scaleFactor`` は画像スケールの縮小ステップを制御します（小さいほど高精度になりやすい一方、遅くなります）。
   - ``minNeighbors`` は誤検出を減らします（大きいほど厳しくなります）。
   - ``minSize`` は非常に小さい検出結果を無視します。

#. 描画と表示のために RGB を BGR へ変換する：

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

   OpenCV の描画関数と ``imshow`` は、カラー画像に対して BGR を前提としています。

#. 顔の矩形とラベルを描画する：

   .. code-block:: python

      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
      cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   これにより、検出された各顔の周囲に矩形を描き、 ``Face 1`` のようなラベルを表示します。

#. 各顔の内部（ROI）で目を検出する：

   .. code-block:: python

      roi_gray = gray[y:y + h, x:x + w]
      roi_color = frame_bgr[y:y + h, x:x + w]

      eyes = eye_cascade.detectMultiScale(
          roi_gray,
          scaleFactor=1.2,
          minNeighbors=8,
          minSize=(20, 20)
      )

   ROI は “Region of Interest” の略です。目の検出を顔領域の内部だけに限定することで、高速化でき、誤検出も減らせます。

#. 最大 2 つの目を描画する：

   .. code-block:: python

      for (ex, ey, ew, eh) in eyes[:2]:
          cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

   これにより、最初に検出された 2 つの目の周囲に矩形を描きます。

#. 結果を表示し、終了を処理する：

   .. code-block:: python

      cv2.imshow(WIN, frame_bgr)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
          break

   ``q`` キーを押すか、ウィンドウを閉じることで安全に終了できます。

#. 後片付け（必ず実行される）：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   エラーが発生した場合でも、最後にカメラを停止し、OpenCV のウィンドウをすべて閉じます。


5. Haar 検出の長所と短所
----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Advantages
     - Disadvantages
   * - Speed
     - 非常に高速で、Raspberry Pi に適している
     - -
   * - Accuracy
     - 正面顔にはよく機能する
     - 回転や横顔には弱い
   * - Lighting
     - 均一な照明下では良好
     - 明るすぎる／暗すぎる環境では性能が低下する
   * - Model
     - モデルサイズが小さく、導入が容易
     - 深層学習ベースの手法より精度は低い

軽量かつ高速であるため、Haar 特徴は現在でも組み込み機器において十分実用的です。


6. よく使われる改善方法
-------------------------

1. **照明前処理**：検出前にヒストグラム平坦化や CLAHE を適用すると、暗所での性能を改善できます。  
2. **多角度検出**：正面顔用だけでなく横顔用の分類器も読み込むことで、より多くの顔姿勢に対応できます。  
3. **顔パーツの追加検出**：目や口、鼻の Haar 分類器を追加し、検出内容をより充実させることができます。  
4. **Haar の代わりに DNN を使う**：OpenCV DNN + ResNet/MobileNet を使うと、より高い精度が得られます（ただし計算量は増えます）。



7. 発展練習
---------------------

- ``cv2.equalizeHist`` をグレースケール画像に適用して、暗い環境での検出性能を改善してみましょう。  
- 口や鼻の Haar 分類器を追加して、より多くの顔パーツを検出してみましょう。  
- ``cv2.VideoWriter`` を使って、検出結果を動画として記録してみましょう。  
- GPIO 出力と組み合わせて、「顔を検出したら LED を点灯する」Raspberry Pi プロジェクトを作ってみましょう。  