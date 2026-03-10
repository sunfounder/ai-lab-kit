.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

7. Canny エッジ検出
=========================================

この章では、Raspberry Pi + Picamera2 を使ってリアルタイム動画を取得し、OpenCV の **Canny アルゴリズム** によるエッジ検出を行います。  
エッジ検出はコンピュータビジョンの基本処理のひとつであり、Canny アルゴリズムは安定性が高く、ノイズにも強い手法として広く知られています。

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_7.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Canny アルゴリズムは何をするのか？
--------------------------------------------------

画像における **エッジ** とは、通常、濃度（グレースケール値）が大きく変化する位置を指します。たとえば：

- 物体の輪郭
- 明るい領域と暗い領域の境界
- 構造を表すエッジ線

Canny エッジ検出の目的は、次のとおりです：

- 不要な干渉を抑えながら、 **エッジ情報を正確に抽出する** こと
- 後続の **輪郭検出** 、 **物体分割** 、 **幾何形状認識** （たとえば円や長方形の検出）のための信頼できる基盤を提供すること
- ロボットビジョンでは、 **経路検出** や **障害物認識** によく利用されること

.. image:: img/opencv_canny.png
   :alt: Illustration of Canny edge detection
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
      python3 cv_7_canny.py

   .. tip::
   
      動画ファイルを処理するための ``cv_7_canny_video.py`` と、リアルタイム映像と動画を組み合わせて表示する ``cv_7_canny_conbine.py`` も用意しています。

#. プログラムを実行すると、次の 2 つの OpenCV ウィンドウが表示されます：

   * **Camera** – ライブカメラ映像を表示  
   * **Canny Edges** – 検出されたエッジをリアルタイムで表示  
   
   トラックバーを使ってエッジ検出のしきい値を調整できます。  
   **q** キーを押すか、いずれかのウィンドウを閉じると終了します。

3. 完全なコード
---------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2

   # Empty callback function for trackbars (required by OpenCV API)
   def _noop(x):
      pass

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()

   # Create a preview configuration:
   # size: resolution of the camera image
   # format: XRGB8888 (4-channel image, similar to BGRA)
   picam2.configure(
      picam2.create_preview_configuration(
         main={"size": (640, 480), "format": "XRGB8888"}
      )
   )

   # Start the camera
   picam2.start()

   # -----------------------------
   # Create OpenCV windows
   # -----------------------------
   WIN_CAM = "Camera"        # window for original image
   WIN_EDGE = "Canny Edges"  # window for edge detection result

   cv2.namedWindow(WIN_CAM)
   cv2.namedWindow(WIN_EDGE)

   # -----------------------------
   # Create trackbars to tune Canny thresholds
   # -----------------------------
   # low_th: lower threshold for Canny
   # high_th: higher threshold for Canny
   cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
   cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   print("Press 'q' to exit")

   # -----------------------------
   # Main loop
   # -----------------------------
   while True:
      # Capture one frame from the camera (BGRA format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for OpenCV processing
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame to grayscale
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

      # Apply Gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Read current threshold values from trackbars
      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      # Ensure high_th is always larger than low_th
      if high_th <= low_th:
         high_th = low_th + 1
         cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

      # Perform Canny edge detection
      edges = cv2.Canny(blurred, low_th, high_th)

      # Show original camera image
      cv2.imshow(WIN_CAM, frame_bgr)

      # Show edge detection result
      cv2.imshow(WIN_EDGE, edges)

      # Process GUI events and keyboard input
      key = cv2.waitKey(1) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
         break

   # -----------------------------
   # Cleanup
   # -----------------------------
   picam2.stop()             # Stop the camera
   cv2.destroyAllWindows()   # Close all OpenCV windows

4. コード解説
---------------------------------
#. トラックバー用のコールバック関数を定義する：

   .. code-block:: python

      def _noop(x):
          pass

   OpenCV のトラックバーにはコールバック関数が必要です。  
   今回は特に処理を行わないため、空の関数で十分です。

#. Picamera2 を初期化し、プレビュー形式を設定する：

   .. code-block:: python

      picam2 = Picamera2()
      picam2.configure(
          picam2.create_preview_configuration(
              main={"size": (640, 480), "format": "XRGB8888"}
          )
      )
      picam2.start()

   これにより、Raspberry Pi カメラが 640×480 で起動します。  
   ``XRGB8888`` は 4 チャンネル形式なので、取得されるフレームは BGRA ライクな形式になります。

#. 2 つの OpenCV ウィンドウを作成する：

   .. code-block:: python

      WIN_CAM = "Camera"
      WIN_EDGE = "Canny Edges"

      cv2.namedWindow(WIN_CAM)
      cv2.namedWindow(WIN_EDGE)

   ひとつのウィンドウには元のカメラ画像を表示し、もうひとつには Canny の結果を表示します。

#. Canny のしきい値をリアルタイム調整するためのトラックバーを作成する：

   .. code-block:: python

      cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
      cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   - ``low_th``: Canny の低しきい値
   - ``high_th``: Canny の高しきい値
   
   これらのスライダーを動かすことで、エッジ検出の感度を調整できます。

#. フレームを取得し、OpenCV 処理用に変換する：

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   カメラ出力は 4 チャンネルのため、標準的な 3 チャンネル BGR 形式へ変換します。

#. グレースケール化し、画像をぼかす：

   .. code-block:: python

      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

   - Canny はグレースケール画像に対して動作します。
   - Gaussian blur はノイズを低減し、不要な偽エッジが出すぎるのを防ぎます。

#. トラックバーの値を読み取り、妥当な状態に保つ：

   .. code-block:: python

      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      if high_th <= low_th:
          high_th = low_th + 1
          cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

   Canny では ``high_th`` が ``low_th`` より大きい必要があります。  
   この処理では、ユーザーが値を近づけすぎた場合でも、自動的に補正します。

#. Canny エッジ検出を実行する：

   .. code-block:: python

      edges = cv2.Canny(blurred, low_th, high_th)

   Canny は画像中の強いエッジを強調して抽出します。  
   しきい値を低くするとエッジは多く検出されますが、ノイズも増えやすくなります。

#. 2 つのウィンドウを表示する：

   .. code-block:: python

      cv2.imshow(WIN_CAM, frame_bgr)
      cv2.imshow(WIN_EDGE, edges)

   一方のウィンドウにはライブカメラ映像を表示し、もう一方には検出されたエッジを表示します。

#. 終了条件（ ``q`` キーまたはウィンドウを閉じる）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
          break

   初学者でも、キーボード操作とウィンドウのクローズの 2 通りで停止できるようになっています。

#. 後片付け：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   リソースを解放するため、最後に必ずカメラを停止し、OpenCV のウィンドウをすべて閉じてください。

5. なぜ Canny は有用なのか？
---------------------------------

Canny の出力は、その後のビジョンタスクに非常に適しています：

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Application
     - Description
   * - Contour detection
     - ``cv2.findContours`` を Canny の出力に適用して、物体形状を取得できる
   * - Object segmentation
     - エッジを手がかりとして、ターゲットと背景を分離できる
   * - Shape recognition
     - Hough 変換と組み合わせて、円や直線などを検出できる
   * - Robot navigation
     - 地面、道路、障害物の輪郭を検出して経路計画を支援できる
   * - OCR / Target localization
     - 文字領域、QR コード、マーカーなどは明確なエッジ特徴を持つことが多い

Canny は単に「見た目が面白い」処理ではなく、より広い CV パイプラインへの **入口** となる重要な処理です。


6. しきい値選択のヒント
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30 30 70
   
   * - Scenario
     - low_th
     - high_th
     - Notes
   * - 安定した室内照明
     - 50
     - 150
     - 一般的なケースで、安定した結果が得られる
   * - 強い照明・高コントラスト
     - 100
     - 200
     - 偽エッジを減らすため、しきい値を高めに設定する
   * - 暗所・ノイズが多い環境
     - 30
     - 100
     - より多くのディテールを残すため、しきい値を低めにする
   * - 非常にぼやけたエッジ
     - 20
     - 80
     - さらに低く設定して、エッジに対する感度を上げる

トラックバーを使って適切な範囲をすばやく調整し、その後プログラム内に固定値として書き込むとよいでしょう。


7. 発展練習
---------------------

- ``cv2.findContours`` を Canny の出力に適用して、物体の輪郭を描いてみましょう。  
- Gaussian カーネルのサイズを変更して、エッジ精度がどう変化するか観察してみましょう。  
- 明るい環境と暗い環境で異なるしきい値を試し、ダブルしきい値の効果を理解してみましょう。  
- ``cv2.HoughLines`` （直線）や ``cv2.HoughCircles`` （円）と組み合わせて、エッジ画像から図形検出を行ってみましょう。
