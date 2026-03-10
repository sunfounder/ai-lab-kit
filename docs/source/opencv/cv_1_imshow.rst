.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. 画像の表示
==============================================

この章では、OpenCV の基本的な使い方を素早く体験するためのシンプルな例として、**画像の読み込みと表示** を行います。

サンプルプロジェクトフォルダには、すでに ``my_photo.jpg`` というサンプル画像が用意されています。  
また、:ref:`py_photograph` の例を使って写真を撮影し、現在のフォルダに保存して使用することもできます。


1. プロジェクト概要
--------------------

このセクションでは、次の操作を行います：

- ``cv2.imread`` を使ってローカル画像を読み込む
- ``cv2.imshow`` を使って画像を表示する
- ``cv2.waitKey`` を使ってウィンドウの動作を制御する
- ``cv2.destroyAllWindows`` を使ってウィンドウを閉じる

このコードを正常に実行すると、画面に画像表示用のウィンドウがポップアップします。

.. image:: img/opencv_imshow.png
   :alt: Preview of the result
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
      python3 cv_1_imgshow.py

#. スクリプトを実行すると、OpenCV は ``Picture`` というタイトルのウィンドウを開き、 ``my_photo.jpg`` から読み込んだ画像を表示します。  

   このウィンドウは、ユーザーがプログラムを終了するまで表示されたままになります。
   
   プログラムを終了するには、次のいずれかを行います：
   
   * キーボードで **q** を押す  
   * ウィンドウの閉じるボタンをクリックする  
   
   ウィンドウが閉じられると、OpenCV のすべてのリソースが解放され、プログラムは終了します。

3. 完全なコード
-------------------

.. code-block:: python

   # Python code to read and display an image using OpenCV
   import cv2
   from pathlib import Path

   # Get the directory of the current Python file
   BASE_DIR = Path(__file__).resolve().parent

   # Read image from disk
   # cv2.imread loads the image as a NumPy array
   img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

   # Create a GUI window to display the image
   # First parameter: window title
   # Second parameter: image array
   cv2.imshow("Picture", img)

   # Keep the window open until the user closes it or presses 'q'
   # cv2.waitKey only listens for keyboard events, not the close button
   # Therefore, we use a loop to detect both window close and key press
   while True:
      # Check if the window has been closed
      if cv2.getWindowProperty("Picture", cv2.WND_PROP_VISIBLE) < 1:
         break

      # Wait for 1 ms and check for key press
      # Press 'q' to exit the program
      if cv2.waitKey(1) & 0xFF == ord("q"):
         break

   # Destroy all OpenCV windows and release memory
   cv2.destroyAllWindows()

4. コードの解説
----------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``  

  ``my_photo.jpg`` という画像ファイルを読み込み、カラー画像としてロードします。

- ``cv2.imshow("Picture", img)``  

  「Picture」というタイトルのウィンドウを作成し、画像を表示します。

- ``cv2.waitKey(0)``  

  引数が ``0`` の場合、ウィンドウを閉じるか任意のキーが押されるまでプログラムは待機します。

- ``cv2.getWindowProperty()``

  指定したウィンドウのプロパティ（例えば、ウィンドウが表示されているかどうか）を取得します。


- ``cv2.destroyAllWindows()``  

  すべての OpenCV ウィンドウを閉じ、リソースを解放します。

5. さらに試してみよう
-----------------------

- ``imshow`` のウィンドウタイトルを “My First OpenCV Window” に変更してみましょう。  
- 別の画像に置き換えて、表示結果を確認してみましょう。  
- ``waitKey`` のパラメータを `3000` に変更し、3 秒後にウィンドウが自動的に閉じるようにしてみましょう。