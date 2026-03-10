.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. 色検出
===========================================

色検出は、コンピュータビジョンにおける最も基本的で実用的な機能のひとつです。  
この章では、段階的なコードと解説を通して、 **HSV 色空間を使って赤い物体を検出し** 、 **その周囲にバウンディングボックスを描画する** 方法を学びます。

これは、より高度な物体追跡技術（たとえば CAMShift）の基礎となります。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. 目的とアプローチ
--------------------------------------------

- **Picamera2** を使ってカメラのリアルタイムフレームを取得する  
- 画像を BGR から HSV 色空間へ変換する  
- ``cv2.inRange`` を使って赤色領域を抽出する  
- モルフォロジー処理でノイズを除去する  
- ``cv2.findContours`` を使って赤い物体の輪郭を見つける  
- 検出した赤色領域の周囲にバウンディングボックスを描画する

.. image:: img/color_detection.png
   :alt: Color detection preview illustration
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
      python3 cv_4_color.py

#. プログラムを実行すると、画面に OpenCV のウィンドウが 2 つ表示されます：

   * **Red Detection** – 検出された赤い物体の周囲に緑色のバウンディングボックスを描画したライブ映像を表示します  
   * **Red Mask** – 赤色検出に使用する二値マスク画像を表示します  

   プログラムは Raspberry Pi カメラからフレームを連続的に取得し、赤色領域をリアルタイムで検出します。  
   赤い物体が検出されると、カラー画像上に緑の矩形と面積値が表示されます。

   プログラムを終了する方法は 2 つあります：

   * キーボードの **q** キーを押す  
   * OpenCV ウィンドウのいずれかを閉じるボタン（X）で閉じる  

   終了すると、カメラのストリーミングが停止し、すべての OpenCV ウィンドウが閉じられます。

3. 完全なコード
------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. コードの解説
--------------------------------

#. Picamera2 を初期化し、ストリーミングを開始します：

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   これにより、カメラは 640×480 の解像度で設定され、プレビューのストリームが開始されます。  
   ``XRGB8888`` は 4 チャンネル形式のため、取得されるフレームは BGRA に近い形式になります。

#. 取得したフレームを、OpenCV で一般的に使用する形式へ変換します：

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   ここで Picamera2 は 4 チャンネル画像を返すため、処理しやすい標準的な 3 チャンネル BGR 形式へ変換します。

#. HSV 色空間を使って、より安定した色検出を行います：

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV は色相（Hue）と明るさを分離するため、照明条件が変わっても色検出が安定しやすくなります。

#. 赤色用に 2 つの HSV 範囲を定義します：

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   OpenCV の HSV において、赤は Hue スケールの端（0 付近と 180 付近）にまたがるため、2 つの範囲を組み合わせて赤全体をカバーします。

#. モルフォロジー処理でマスクを整えます（ノイズ除去と穴埋め）：

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** は小さなノイズ点を除去します。
   - **CLOSE** は検出された赤色領域の内部にある小さな穴を埋めます。

#. 赤色領域を見つけ、小さすぎる領域を除外します：

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   二値マスクから輪郭を検出します。  
   ``MIN_AREA`` によって、小さな赤色領域を無視し、誤検出を減らします。

#. 結果画像にバウンディングボックスとラベルを描画します：

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   これにより、OpenCV が赤い物体を検出した位置が表示され、参考情報として検出領域の面積も示されます。

#. 結果画像とマスク画像の両方を表示します：

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   **結果ウィンドウ** には枠付きのカメラ映像を表示し、 **マスクウィンドウ** には赤色だけを抽出した二値画像を表示します。

#. 終了条件（キーボード入力 + ウィンドウを閉じる）：

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   ``q`` を押すと終了し、どちらかのウィンドウを閉じても安全にプログラムを終了できます。

#. クリーンアップ：

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   リソースを解放するため、必ずカメラを停止し、OpenCV のウィンドウを閉じてください。


5. パラメータ調整のヒント
-----------------------------

- ``LOWER_RED1 / UPPER_RED1``: この範囲を調整することで、他の色も検出できます。  
  たとえば、緑はおおよそ ``[35, 50, 50]`` から ``[85, 255, 255]`` です。

- ``KERNEL``: カーネルを大きくするとフィルタリング効果は強くなりますが、小さな物体まで消えてしまう場合があります。

- ``MIN_AREA``: この値を大きくすると小さなノイズ輪郭を除外しやすくなり、小さくすると検出感度が上がります。

.. note::
   最初は ``mask`` だけを表示してしきい値を調整し、対象領域がはっきり見えるようにしてから、残りの処理を進めるのがおすすめです。




6. 拡張と練習
--------------------------

- HSV のしきい値を変更して、他の色（たとえば青や緑）を検出してみましょう。  
- より複雑な背景で、さまざまなモルフォロジーパラメータを試してみましょう。  