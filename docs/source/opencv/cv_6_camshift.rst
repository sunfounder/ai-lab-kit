.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. CAMShift による物体追跡
==============================

前章では、色ヒストグラムに基づいて動画内のターゲットを連続的に追跡できる MeanShift アルゴリズムを学びました。  
この節では、 **CAMShift (Continuously Adaptive Mean Shift)** を紹介します。  
CAMShift は MeanShift を拡張し、 **追跡ウィンドウのサイズと向きを自動的に適応** できるため、実際のアプリケーションでより実用的です。  
さらに、この例では **色ではなく明るさに基づいて** ターゲットを追跡します。これは実際の用途でも非常によく使われる方法です。

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>
   
1. アルゴリズムの特徴
---------------------

**MeanShift** はターゲットの位置だけを追跡でき、ウィンドウサイズは固定です。  
一方、 **CAMShift** は位置の追跡に加えて、 **ウィンドウのサイズと角度も自動的に調整** できます。

たとえば、ターゲットがカメラに近づけば追跡枠は大きくなり、遠ざかれば小さくなります。さらに、ターゲットが回転すれば、枠もそれに合わせて回転します。

.. image:: img/opencv_camshift.png
   :alt: CAMShift tracking illustration
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
      python3 cv_6_camshift.py

#. プログラムを実行すると、 **CAMShift Tracker** という名前の OpenCV ウィンドウが表示され、動画ファイル *sample3.mp4* の再生が始まります。  

   このプログラムでは、CAMShift（Continuously Adaptive Mean Shift）アルゴリズムを使って黒い猫を追跡します。

   追跡対象の周囲には、緑色の回転矩形が描画されます。  
   猫が移動したり、サイズや向きが変わったりすると、追跡ウィンドウは位置・大きさ・角度を自動的に調整します。

   プログラムを終了する方法は 2 つあります：

   * キーボードの **q** キーを押す  
   * ウィンドウの閉じるボタン（X）をクリックして閉じる  

   終了すると、動画の再生が停止し、すべての OpenCV ウィンドウが閉じられます。

3. 完全なコード
---------------------

完全なコードは ``cv_6_camshift.py`` を開いて確認してください。

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. コード解説
---------------------------

#. 動画ファイルを開き、最初のフレームを読み込む：

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift は、最初のフレームを使って何を追跡するかを学習します。

#. 初期追跡ウィンドウ（ROI）を設定する：

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   この矩形は、最初のフレーム内でターゲット物体を覆う必要があります。  
   CAMShift は追跡中にこのウィンドウを自動更新します。

#. 最初のフレームを HSV に変換し、ROI を切り出す：

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV は、V チャンネルのような特定の成分を選んで扱えるため、追跡に便利です。

#. 暗い物体用のマスクを作成する（低い V 値）：

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   これにより、ROI 内の「暗い」画素だけが残ります。  
   黒色や暗い物体では、明るさ（V）がもっとも有効な特徴になることが多いです。

#. V チャンネルのヒストグラムを計算し、正規化する：

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - チャンネル ``2`` は、HSV の **V（Value / 明るさ）** チャンネルを意味します。
   - このヒストグラムは、ターゲット ROI の「暗さ / 明るさ」の分布を表します。
   - 正規化によって追跡がより安定します。

#. CAMShift の終了条件を設定する：

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift は、10 回の反復に達するか、移動量が 1 ピクセル未満になった時点で更新を終了します。

#. FPS に基づいて再生速度を設定する：

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   これにより、動画が元の FPS に近い速度で再生されます。

#. バックプロジェクションで確率マップを作成する（V チャンネル）：

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   バックプロジェクションは、フレーム内で ROI ヒストグラムに一致する V 値を持つ画素を強調します。  
   ``back_proj`` 内で明るい値ほど、「ターゲットである可能性が高い」ことを意味します。

#. CAMShift で追跡し、ウィンドウを更新する：

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift は MeanShift をベースにしていますが、追跡ウィンドウの **サイズと回転** にも対応できます。

   - ``track_window`` は各フレームで更新されます。
   - ``rot_rect`` には回転矩形（中心、サイズ、角度）が含まれます。

#. 回転した追跡枠を描画する：

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   これにより、回転矩形が 4 つの頂点に変換され、フレーム上に描画されます。

#. 終了条件（キーボード入力 + ウィンドウを閉じる）：

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   ``q`` を押すか、ウィンドウを閉じると安全に終了できます。

#. リソースを解放する：

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   最後に必ず動画ファイルを解放し、ウィンドウを閉じてください。


5. CAMShift と MeanShift の比較
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - MeanShift
     - CAMShift
   * - Window size
     - 固定
     - 可変
   * - Angle
     - 非対応
     - 回転対応
   * - Tracking accuracy
     - 中程度
     - より高く、適応性が高い
   * - Applications
     - 静的なターゲット
     - 複雑な動き、回転するターゲット

CAMShift は MeanShift を発展させた手法であり、  
ターゲットの変形、回転、距離変化にもより柔軟に対応できるため、現実のシーンに適しています。

6. 拡張と練習
-------------------------------------------

- ``inRange`` のしきい値を調整して、緑や青のターゲットを追跡してみましょう  
- ライブカメラ入力と組み合わせて、リアルタイムの色ベース追跡システムを作ってみましょう


7. 応用: インタラクティブな ROI 選択と HSV しきい値の自動調整
-------------------------------------------------------------------------

前節と同様に、このプロジェクトでもマウス操作による ROI の選択と、HSV しきい値の自動調整を行えます。

変更版のコードは ``cv_6_camshift_auto.py`` を実行してください。

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

プログラムを実行すると、動画の最初のフレームが表示され、マウスで Region of Interest（ROI）を選択するよう求められます。

マウスをドラッグしてターゲット物体を囲む矩形を描き、 **Enter** または **Space** を押して確定します。  
**Esc** を押すと選択をキャンセルできます。

ROI を選択すると、 **CAMShift Tracker** という名前のウィンドウが表示されます。  
選択した物体は緑色の回転矩形で追跡され、物体が動くと、追跡ウィンドウは位置・サイズ・向きを自動的に調整します。

プログラムを停止するには：

* キーボードの **q** キーを押す  
* または表示ウィンドウの閉じるボタン（X）をクリックする  

終了すると、動画の再生が停止し、すべての OpenCV ウィンドウが閉じられます。


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

   ...

