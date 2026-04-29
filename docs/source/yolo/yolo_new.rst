.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Raspberry PiでのYOLOの実行
==============================================================

YOLO（You Only Look Once）は、その速度と精度で知られる革新的な物体検出アルゴリズムです。物体検出を回帰問題に変換し、1回のニューラルネットワークの推論で画像内のすべての物体カテゴリと位置を予測します。

「一目で全てを把握する」画像処理システムを想像してみてください。監視カメラ、自動運転、産業用品質管理など、リアルタイムの物体検出が必要とされるあらゆる場面でYOLOは活躍しています。

.. image:: img/yolo_new.png

図：Raspberry Pi上でのYOLOv8nのリアルタイム実行。カメラ画像内の物体が正確に検出・注釈付けされ、検出されたクラスと信頼度が左側に表示されています。この画像は、モデルが人、椅子、テレビなどの物体を正常に識別している様子を示しています。

核となる原理
------------------------------------------

古い2段階の手法（R-CNNなど）が「まず候補領域を見つけ、それから識別する」のに対し、YOLOは根本的に異なるアプローチを取ります：

* **統一されたフレームワーク**：画像をグリッド（例：元の7x7グリッド）に分割します。

* **グリッドベースの予測**：各グリッドセルは、そのセル内に中心がある物体の予測を担当します。各セルは、複数のバウンディングボックス（位置とサイズを含む）とその信頼度を予測し、さらに物体クラスの確率も予測します。

* **ワンステップ処理**：分類と位置特定を同じニューラルネットワーク内で同時に実行するため、まさに「You Only Look Once」を実現し、速度において従来の手法を大幅に上回ります。

コードの実行
------------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_test.py

このコードは自動的にモデル（約6 MB）をダウンロードし、カメラで実行します。結果は「YOLOv8」というタイトルのウィンドウに表示されます。

（初回起動時には、約6 MBのモデルが自動的にダウンロードされます）：

.. code-block:: python

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")  # ナノモデル

   # カメラの初期化
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLOを開始しました。「q」を押すと終了します...")

   try:
      while True:
         # フレームを取得
         frame = picam2.capture_array()
         
         # YOLOを実行し、imgsz=320を設定
         results = model(frame, imgsz=320)
         
         # 結果を描画
         annotated = results[0].plot()
         
         # 結果を表示
         cv2.imshow("Raspberry PiでのYOLO", annotated)
         
         # 「q」を押すと終了
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("終了しました")



トラブルシューティング
-------------------------

Q: Numpy.dtypeのサイズ変更に関するエラー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Numpyのバージョンをリセットします：

.. code-block:: bash

   # バージョン2.xの場合は、1.xにリセット
   pip3 install "numpy<2.0" --break-system-packages --force-reinstall

Q: ``libopenblas.so.0`` が見つからないエラー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenBLASライブラリをインストールします：

.. code-block:: bash

   sudo apt install libopenblas-dev

Q: カメラを開けないエラー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

カメラの接続を確認し、有効になっていることを確認します：

.. code-block:: bash

   sudo raspi-config
   # Interface Options -> Camera -> Enable を選択

Q: メモリ不足によるエラー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スワップ領域を拡張します：

.. code-block:: bash

   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # CONF_SWAPSIZE=2048 に変更
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon

パフォーマンス最適化手法
--------------------------------------------------------

Raspberry Pi（4B/5でも）でYOLOを動作させるのは負荷が高い場合があります。以下に、いくつかの実証済みの最適化手法を示します：

1. **YOLO推論解像度の調整**：上記のコードではすでに imgsz=320 を使用しており、これはバランスの取れた設定です。調整可能な値：

   * ``imgsz=224`` - 最低解像度、最高速度
   * ``imgsz=320`` - デフォルト設定
   * ``imgsz=416`` - より高い精度、低速
   * ``imgsz=640`` - 最高精度、Raspberry Pi上では非常に低速

2. **適切なモデルの選択**：

   * ``yolov8n.pt`` (6 MB) - 最速、リアルタイム検出に適しています
   * ``yolov8s.pt`` (22 MB) - やや遅いが、より正確
   * ``yolov8m.pt`` (49 MB) - 低速だが、より高い精度
   * ``yolov8l/x.pt`` - Raspberry Pi上では通常使用不可
   * 自分でトレーニングしたモデル（例：``"/home/pi/my_model.pt"``）も使用できます。独自モデルのトレーニング方法については、後の章で説明します。

3. **検出クラスの制限**：特定の物体のみを検出する場合（例：人のみ）、コードを変更します：

.. code-block:: python

   results = model(frame, classes=[0], imgsz=320)  # 0は人のクラスID

一般的なクラスID：

   * 0 - 人
   * 1 - 自転車
   * 2 - 車
   * 3 - バイク
   * 5 - バス
   * 7 - トラック

4. **軽量モデルバリアントの使用**：

.. code-block:: python

   # YOLOv8nの枝刈りバージョンを使用（利用可能な場合）
   model = YOLO("yolov8n.pt")
   
   # またはTensorRTアクセラレーションを使用（追加設定が必要）
   # model = YOLO("yolov8n.pt")
   # model.export(format="engine")  # TensorRTエンジンとしてエクスポート

5. **画像処理レートの低減**：すべてのフレームをリアルタイム表示する必要がない場合は、画像を間欠的に処理します：

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       
       # 3フレームに1回処理
       if frame_count % 3 == 0:
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           cv2.imshow("Raspberry PiでのYOLO", annotated)
       
       frame_count += 1
       
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

6. **マルチスレッドの使用**：カメラキャプチャとYOLO推論を別々のスレッドに分離します：

.. code-block:: python

   import threading
   import queue
   
   frame_queue = queue.Queue(maxsize=2)
   result_queue = queue.Queue(maxsize=2)
   
   def capture_frames():
       while True:
           frame = picam2.capture_array()
           if frame_queue.full():
               frame_queue.get()
           frame_queue.put(frame)
   
   def process_frames():
       while True:
           frame = frame_queue.get()
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           if result_queue.full():
               result_queue.get()
           result_queue.put(annotated)
   
   # スレッドを開始
   threading.Thread(target=capture_frames, daemon=True).start()
   threading.Thread(target=process_frames, daemon=True).start()
   
   while True:
       if not result_queue.empty():
           cv2.imshow("Raspberry PiでのYOLO", result_queue.get())
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

高度な応用
--------------------------------

ビデオファイルを入力として使用
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   from ultralytics import YOLO
   
   model = YOLO("yolov8n.pt")
   cap = cv2.VideoCapture("input_video.mp4")
   
   while cap.isOpened():
       ret, frame = cap.read()
       if not ret:
           break
       
       results = model(frame, imgsz=320)
       annotated = results[0].plot()
       cv2.imshow("YOLO検出", annotated)
       
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break
   
   cap.release()
   cv2.destroyAllWindows()

まとめ
------------------

このチュートリアルを通して、以下を学びました：

* Raspberry Pi上にYOLO環境をセットアップする方法
* カメラを使用してリアルタイム物体検出を実行する方法
* 一般的なインストールおよび実行時の問題を解決する方法
* 検出パフォーマンスを最適化するためのさまざまな方法

YOLOの強みはそのシンプルさと効率性にあり、Raspberry Piのような組み込みデバイス上でも十分な物体検出性能を実現します。さらに実験を進めることで、スマート監視、物体追跡、人数カウントなど、さまざまな興味深いアプリケーションを開発できます。