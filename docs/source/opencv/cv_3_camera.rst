.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. リアルタイムカメラキャプチャ
================================================================

前の章では、ローカルの動画ファイルを読み込み再生する方法を学びました。  
この章ではさらに一歩進み、 **Raspberry Pi カメラ** を使ってリアルタイムで映像を取得し、OpenCV を用いた **色空間変換** を行います。


1. プロジェクトの目的
--------------------------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

- **Picamera2** を使用してカメラのリアルタイムフレームを取得する  
- カメラ出力を BGRA 形式から BGR 形式へ変換する  
- OpenCV を使用してリアルタイムプレビューを表示する  
- 異なる色空間の特徴と用途を理解する

.. image:: img/opencv_camera.png
   :alt: Real-time camera preview illustration
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
      python3 cv_3_camera.py

#. プログラムを実行すると、OpenCV のウィンドウが 2 つ表示されます：

   * **BGR Frame** – カメラのカラー映像を表示  
   * **GRAY Frame** – 同じ映像をグレースケールで表示  
   
   プログラムを終了する方法は次の 2 つです：
   
   * キーボードの **q** キーを押す  
   * ウィンドウの閉じるボタン（X）をクリックする  
   
   終了すると、カメラのストリーミングが停止し、すべての OpenCV ウィンドウが閉じられます。

3. サンプルコード
-------------------------------

以下は、この章で使用する完全な Python サンプルコード（ ``cv_3_camera.py`` ）です：

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. コードの解説
-------------------

#. 必要なライブラリをインポートします：

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2 は Raspberry Pi カメラからフレームを取得するために使用し、OpenCV は画像の変換と表示に使用します。

#. Picamera2 オブジェクトを作成し、カメラを設定します：

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   これにより、カメラは 640×480 の解像度で動作します。  
   ``XRGB8888`` は 4 チャンネル形式のため、取得されるフレームは BGRA に近い形式になります。

#. NumPy 配列としてフレームを取得します：

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   ループごとにカメラから 1 フレームを取得します。

#. 表示用にフレームを変換します：

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr`` は通常のカラー表示用です。
   - ``frame_gray`` は同じフレームのグレースケール版です。

#. 2 つのウィンドウに表示します：

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   OpenCV のウィンドウが 2 つ開き、1 つはカラー映像、もう 1 つはグレースケール映像を表示します。

#. 終了条件（ ``q`` キーまたはウィンドウを閉じる）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - ``q`` キーを押すとプログラムを終了します。
   - どちらかのウィンドウを閉じても安全に終了します。

#. FPS を制限して CPU 使用率を抑える：

   .. code-block:: python

      time.sleep(1 / 30)

   小さな待機時間を入れることで、ループを約 30 FPS で実行し、Raspberry Pi の CPU 負荷を軽減できます。

#. カメラを停止し、OpenCV ウィンドウを閉じます：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   プログラム終了前にカメラを解放し、すべての OpenCV ウィンドウを閉じます。

5. 色空間変換の重要性
-------------------------------------------------------------------

カメラから出力される生の画像形式は、OpenCV が処理に使用する形式と必ずしも一致するとは限りません。  
この例では、Picamera2 は **XRGB8888（BGRA）** 形式で画像を出力しますが、OpenCV では主に **BGR** 形式が使用されます。

そのため、次のように画像を変換する必要があります：

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

これにより、画像のチャンネル順序が OpenCV の標準である BGR 形式になり、正しく表示・処理できるようになります。

さらに、画像をグレースケールへ変換することもできます：

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

これにより、カメラから取得した画像を OpenCV の画像処理ワークフローに適した形式へ変換できます。

**代表的な色空間と用途**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Color Space
     - Characteristics
     - Typical Use Cases
   * - **BGR**
     - OpenCV の標準フォーマット
     - 画像表示、基本処理、エッジ検出
   * - **RGB**
     - 人間の知覚に近い色表現
     - 可視化、ディープラーニングの入力画像
   * - **GRAY**
     - 単一チャンネルのグレースケール画像
     - 物体検出、エッジ検出、処理速度の最適化
   * - **HSV**
     - 色相と明るさを分離
     - 色検出、物体追跡、セグメンテーション
   * - **YCrCb**
     - 輝度と色差を分離
     - 顔検出、動画圧縮、照明変化への耐性

例えば、 **HSV** は **色検出や物体追跡** に適しており、  
**YCrCb** は **顔認識や照明条件が変化するシーン** に強い特徴があります。

6. 拡張と練習
-------------------------------------------

- BGR から GRAY や HSV への変換を試し、結果を観察してみましょう。

   例えば次のように使用します：

   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
   - その他

- 異なる解像度（例：1280×720）を試し、遅延やフレームレートへの影響を確認してみましょう。  
- 前章の動画再生コードと組み合わせて、カメラ映像と動画ソースを切り替える機能を実装してみましょう。