.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. MeanShift による物体追跡
===============================

MeanShift は、ヒストグラムに基づく古典的な物体追跡アルゴリズムです。  
このレッスンでは、完全な **MeanShift 追跡** の実装例を示すだけでなく、 **なぜ** 各手順を行うのか、そして内部で **何が起きているのか** も説明します。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. MeanShift とは？
-------------------------

MeanShift は、確率密度に基づいてウィンドウを反復的に移動させ、 **ターゲットが最も存在しそうな位置** を見つけるアルゴリズムです。

簡単に言えば、  
まずアルゴリズムに「初期ターゲット領域」を与えます。すると、その領域の色情報（たとえばターゲットの色ヒストグラム）を計算し、以降の各フレームで、その色に最も近い領域を探して矩形をそこへ移動させます。

この処理はディープラーニングに依存せず、事前学習も不要なため、とても軽量です。

.. image:: img/opencv_meanshift.png
   :alt: MeanShift tracking
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
      python3 cv_5_meanshift.py

#. プログラムを実行すると、 **MeanShift Tracker** という名前の OpenCV ウィンドウが表示され、動画ファイル ``sample2.mp4`` の再生が始まります。  

   ターゲット物体の周囲には緑色の矩形が描画され、MeanShift 追跡アルゴリズムによってリアルタイムで更新されます。
   
   動画内で物体が移動すると、その追跡ウィンドウも一緒に移動します。
   
   プログラムを終了する方法は 2 つあります：
   
   * キーボードの **q** キーを押す  
   * ウィンドウの閉じるボタン（X）をクリックして閉じる  
   
   終了すると、動画の再生が停止し、すべての OpenCV ウィンドウが閉じられます。

3. 完全なコード
-----------------------

以下は、MeanShift 追跡スクリプト（ ``cv_5_meanshift.py`` ）の完全なコードです：

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. 解説
---------------------------

#. 動画ファイルを開く：

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   これにより動画キャプチャオブジェクトが作成され、OpenCV がファイルからフレームを読み込めるようになります。

#. 最初のフレームを読み込み、正常に取得できたか確認する：

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   MeanShift で追跡を始めるには、まず最初のフレームから追跡対象を学習する必要があります。

#. 初期追跡ウィンドウ（追跡したい物体）を設定する：

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   この矩形はターゲット（ROI）の初期位置です。  
   通常は、最初のフレーム内の対象物に合わせてこれらの値を調整します。

#. 最初のフレームを HSV に変換し、ROI を取り出す：

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV は、RGB/BGR よりも Hue（色相）チャンネルで色を安定して表現できるため、追跡によく使われます。

#. ROI 内の弱い画素や無効な画素を無視するためにマスクを作る：

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   これにより、彩度や明度が極端に低い画素（影やノイズになりやすい部分）が除外され、追跡の安定性が向上します。

#. ROI のヒストグラム（Hue チャンネル）を計算し、正規化する：

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - ヒストグラムはターゲットの色分布（Hue）を表します。
   - 正規化によって、照明の違いや ROI サイズの違いがあっても比較しやすくなります。

#. MeanShift の終了条件を定義する：

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift は次のいずれかで停止します：
   - 15 回繰り返したとき
   - ウィンドウの移動量が 2 ピクセル未満になったとき

#. 動画の FPS に基づいて再生待機時間を設定する：

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   これにより、再生速度が元の動画に近くなるよう調整されます。  
   FPS を取得できない場合は、30 FPS を既定値として使います。

#. 各フレームを HSV に変換する（追跡のため）：

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   追跡は HSV 空間で行われ、ターゲットの Hue ヒストグラムとの一致を利用します。

#. バックプロジェクション（ターゲット色が存在しそうな場所を求める）：

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   バックプロジェクションは確率マップを生成します。  
   明るい領域ほど、ROI のヒストグラムに近い可能性が高いことを示します。

#. MeanShift を使って追跡ウィンドウを更新する：

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift は、確率マップの中で密度が最も高い方向へ追跡ウィンドウを移動し、フレームごとにターゲット位置を更新します。

#. 追跡結果を描画する：

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   これにより、現在の追跡矩形が動画フレーム上に描画されます。

#. ウィンドウ表示と終了条件：

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - ``q`` を押すと終了します。
   - ウィンドウを閉じても安全に終了します。

#. リソースを解放する：

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   システムリソースを解放するため、必ず動画を閉じてウィンドウを破棄してください。

5. MeanShift と CAMShift の比較
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - MeanShift
     - CAMShift
   * - Window size
     - 固定
     - 自動調整（ターゲットのスケールに追従）
   * - Rotating target
     - 非対応
     - 対応
   * - Suitable scenarios
     - ターゲットサイズが比較的安定している場合
     - ターゲットが拡大縮小・回転する可能性がある場合
   * - Applications
     - シンプルな追跡、ボール、マーカー
     - 実用的な追跡、監視、認識


6. 応用: マウスで ROI を選択する
--------------------------------------

これまでは、次のように固定値を使っていました：

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

これは簡単ですが、柔軟性に欠けます。  
動画を変えたり、ターゲットの初期位置が異なったりすると、コードを書き換える必要があります。

OpenCV には ``cv2.selectROI`` が用意されており、**最初のフレーム上でマウスを使ってターゲット領域を対話的に選択** できます。すると、プログラムが自動的に ``(x, y, w, h)`` を取得します。

**初期化コードの変更版**

変更後のコードは ``cv_5_meanshift_auto.py`` を実行してください。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

プログラムを実行すると、動画の最初のフレームが表示され、マウスで ROI（関心領域）を選択するよう求められます。

マウスをドラッグしてターゲット物体を囲む矩形を描き、 **Enter** または **Space** を押して選択を確定します。  
**Esc** を押すと選択をキャンセルできます。

ROI を確定すると、 **MeanShift Tracker** という名前のウィンドウが表示されます。  
選択した物体は緑色のバウンディングボックスで追跡され、動画内で動くとその矩形も一緒に移動します。

プログラムを停止するには：

* キーボードの **q** キーを押す  
* または表示ウィンドウを閉じるボタン（X）で閉じる  

終了すると、動画の再生が停止し、すべての OpenCV ウィンドウが閉じられます。

.. image:: img/opencv_meanshift_mouse.png
   :alt: Interactive ROI selection window
   :align: center

**Notes**

``cv2.selectROI`` は、OpenCV に標準搭載されている対話型 ROI 選択機能で、手動初期化に最適です。  
戻り値は ``(x, y, w, h)`` で、 ``track_window`` と完全に互換性があるため、CAMShift/MeanShift のメインロジックを変更する必要はありません。  
これにより、同じプログラムを異なる動画や異なるターゲットに再利用できます。


7. 応用 II: ROI に対する HSV しきい値を動的に計算する
--------------------------------------------------------------

元の ``cv_5_meanshift.py`` では、HSV のしきい値を手動で設定しています。これは、ターゲット色が固定されており、照明条件も安定している場合に適しています。


.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

照明が大きく変化したり、ターゲット色が固定でなかったりする場合、固定の ``inRange`` 境界は最適ではないことがあります。  
そこで、より賢い方法として、 **選択した ROI から HSV の lower / upper 境界を自動計算する** 方法があります。

**例: HSV しきい値の自動計算**

変更後のコードは ``cv_5_meanshift_auto.py`` を実行してください。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)


暗いターゲットや明るいターゲットを選んだ場合でも、手動でしきい値を微調整する必要がなくなり、照明や色の違いにも素早く適応できます。

.. note::

   - ``np.percentile`` （5%–95%）は、ROI 内の極端な値（境界、影、ハイライトなど）を除外できるため、頑健性が向上します。  
   - ``pad_h`` , ``pad_s`` , ``pad_v`` は許容範囲を持たせるための余裕であり、軽微な色変化も捉えられるようにします。  
   - ``lower`` と ``upper`` は、 ``cv2.inRange`` で直接使用される動的な HSV 範囲です。


**Summary**

- ``cv2.selectROI`` を使うことで、柔軟にターゲットを初期化できます。  
- ``np.percentile`` を使えば、適応性の高い HSV 範囲を自動計算できます。  
- ``cv2.inRange`` と CAMShift / MeanShift を組み合わせることで、照明変化やターゲットの違いがあっても安定した追跡を実現できます。  