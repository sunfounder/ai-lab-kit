.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. 動画の再生
=======================================

この章では、OpenCV を使って動画ストリームを読み込み再生する方法と、フレーム処理時間を利用して再生速度を制御する方法を学びます。



1. プロジェクト概要
-------------------

このセクションでは、次のことを行います：

- ``cv2.VideoCapture`` を使用して動画ファイルを開く
- 動画をフレームごとに読み込み表示する
- 動画が終了した場合に自動的に先頭から再生する
- 処理時間の計算を利用して再生フレームレートを制御する
- ``q`` キーを押して再生を終了する

.. image:: img/opencv_video.png
   :alt: Video playback interface illustration
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
      python3 cv_2_video.py

#. スクリプトを実行すると、OpenCV は **Video** というタイトルのウィンドウを開き、動画フレームをリアルタイムで表示します。  

   動画が最後まで再生されると、自動的に先頭から再生が再開されます。
   
   プログラムを停止するには、次の方法があります：
   
   * キーボードで **q** を押して再生を終了する  
   * ウィンドウの閉じるボタンをクリックして閉じる  

   ウィンドウが閉じられると、OpenCV のすべてのリソースが解放され、プログラムは終了します。


3. 完全なコード
------------------------------

.. code-block:: python

  import cv2

  # Open the video file
  cap = cv2.VideoCapture("sample2.mp4")

  while True:
      # Read one frame from the video
      ret, frame = cap.read()

      # If the video ends, restart from the beginning
      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

      # Resize the frame for better display performance
      frame = cv2.resize(frame, (640, 480))

      # Display the frame in a window named "Video"
      cv2.imshow("Video", frame)

      # Wait 30 ms between frames (~30 FPS)
      # This also processes GUI events (keyboard and window events)
      key = cv2.waitKey(30) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
          break

      # Exit if the user closes the window (click the close button)
      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

  # Release the video capture object
  cap.release()

  # Close all OpenCV windows
  cv2.destroyAllWindows()


4. コードの解説
-----------------------

#. 動画ファイルを開く：

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   これは動画ファイルを開き、フレームを読み取るための ``VideoCapture`` オブジェクトを作成します。

#. 動画から 1 フレームを読み込む：

   .. code-block:: python

      ret, frame = cap.read()

   - ``ret`` はフレームの読み込みに成功した場合 ``True`` になります。
   - 動画が終了した場合や読み込みに失敗した場合は ``False`` になります。
   - ``frame`` は画像データ（NumPy 配列）です。

#. 動画が終了したらループ再生する：

   .. code-block:: python

      if not ret:
          cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
          continue

   動画が終了した場合、再生位置を最初のフレームに戻して再生を再開します。

#. フレームサイズを変更する：

   .. code-block:: python

      frame = cv2.resize(frame, (640, 480))

   各フレームを 640×480 にリサイズすることで、Raspberry Pi 上でも滑らかに表示でき、CPU 使用率を抑えることができます。

#. フレームを表示する：

   .. code-block:: python

      cv2.imshow("Video", frame)

   ``Video`` という名前のウィンドウに現在のフレームを表示します。

#. 再生速度の制御とキーボード入力の取得：

   .. code-block:: python

      key = cv2.waitKey(30) & 0xFF

   フレーム間で約 30 ms 待機し（約 30 FPS）、GUI イベントを処理します。

#. ``q`` を押して終了する：

   .. code-block:: python

      if key == ord("q"):
          break

   ``q`` キーを押すとプログラムを終了します。

#. ウィンドウが閉じられた場合に終了する：

   .. code-block:: python

      if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
          break

   ウィンドウがまだ表示されているかどうかを確認します。  
   ユーザーがウィンドウを閉じた場合、プログラムは安全に終了します。

#. 動画キャプチャオブジェクトを解放する：

   .. code-block:: python

      cap.release()

   動画ファイルのリソースを解放します。

#. すべての OpenCV ウィンドウを閉じる：

   .. code-block:: python

      cv2.destroyAllWindows()

   すべての OpenCV ウィンドウを閉じ、GUI リソースを解放します。


5. さらに試してみよう
-----------------------

- ウィンドウサイズを変更し、画質への影響を確認してみましょう。  
- 別の動画ファイルに置き換えて互換性を確認してみましょう。  
- フレームごとの処理時間を出力し、FPS と再生遅延の関係を理解してみましょう。
