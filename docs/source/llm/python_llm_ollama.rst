.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Ollamaでテキスト＆ビジョン対話
=====================================

このレッスンでは、 **Ollama** を使ってローカル環境で大規模言語モデルやビジョンモデルを実行する方法を学びます。  
Ollama のインストール方法、モデルのダウンロード方法、そして Fusion HAT+ と接続する手順を紹介します。

この構成では、Fusion HAT+ がカメラでスナップショットを撮影し、モデルが **「見て説明する（see and tell）」** ことができます。  
画像について自由に質問すると、モデルが自然言語で回答します。

.. _download_ollama:

1. Ollama（LLM）のインストールとモデルのダウンロード
-----------------------------------------------------

**Ollama** は次の場所にインストールできます：

* Raspberry Pi 上（ローカル実行）  
* 同じ **ローカルネットワーク** 内の別のコンピュータ（Mac / Windows / Linux）

**モデルサイズとハードウェアの目安**

|link_ollama_hub| で利用可能な任意のモデルを選択できます。  
モデルにはさまざまなサイズ（3B、7B、13B、70B など）があり、小さいモデルは高速でメモリ使用量も少なく、大きいモデルはより高品質な結果を提供しますが高性能なハードウェアが必要です。

以下の表を参考に、お使いのデバイスに適したモデルサイズを選択してください。

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - Model size
     - Min RAM Required
     - Recommended Hardware
   * - ~3B parameters
     - 8GB (16GB better)
     - Raspberry Pi 5 (16GB) またはミドルレンジPC / Mac
   * - ~7B parameters
     - 16GB+
     - Pi 5 (16GB、実用ギリギリ) またはミドルレンジPC / Mac
   * - ~13B parameters
     - 32GB+
     - 高RAMのデスクトップPC / Mac
   * - 30B+ parameters
     - 64GB+
     - ワークステーション / サーバー / GPU推奨
   * - 70B+ parameters
     - 128GB+
     - 複数GPUを備えたハイエンドサーバー

**Raspberry Pi にインストール**

Raspberry Pi 上で Ollama を直接実行する場合：

* **64-bit Raspberry Pi OS** を使用  
* **Raspberry Pi 5（16GB RAM）** を強く推奨  

以下のコマンドを実行します：

.. code-block:: bash

   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull a lightweight model (good for testing)
   ollama pull llama3.2:3b

   # Quick run test (type 'hi' and press Enter)
   ollama run llama3.2:3b

   # Serve the API (default port 11434)
   # Tip: set OLLAMA_HOST=0.0.0.0 to allow access from LAN
   OLLAMA_HOST=0.0.0.0 ollama serve

**Mac / Windows / Linux にインストール（デスクトップアプリ）**

1. |link_ollama| から Ollama をダウンロードしてインストールします  

   .. image:: img/llm_ollama_download.png

2. Ollama アプリを開き、 **Model Selector** に移動し、検索バーでモデルを検索します。  
   例： ``llama3.2:3b`` （最初に試す軽量モデル）

   .. image:: img/llm_ollama_choose.png

3. ダウンロード完了後、チャットウィンドウで「Hi」など簡単な入力をすると、最初の実行時にモデルが自動的にダウンロードされます。

   .. image:: img/llm_olama_llama_download.png

4. **Settings** → **Expose Ollama to the network** を有効にします。  
   これにより Raspberry Pi が LAN 経由で接続できるようになります。

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   次のようなエラーが表示された場合：

   ``Error: model requires more system memory ...``

   モデルがマシンのメモリ容量に対して大きすぎます。  
   **より小さいモデル** を使用するか、RAMの多いコンピュータを使用してください。

2. Ollama のテスト
----------------------

Ollama のインストールとモデルの準備ができたら、簡単なチャットループで動作確認ができます。

**IPアドレスの設定**

#. サンプルスクリプトを開きます：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. 必要に応じてパラメータを更新します：

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``  
     ``ip`` と ``model`` を自分の環境に合わせて変更します。

     * ``ip``：Ollama を **同じ Pi** で実行する場合は ``localhost`` を使用。  
       別のPCで実行している場合は **Expose to network** を有効にし、そのPCの LAN IP を設定します。  
     * ``model``：Ollama でダウンロードまたは有効化したモデル名と完全に一致させる必要があります。


**プログラムの実行**

.. code-block:: bash
  
   cd ~/ai-lab-kit/llm
   sudo python3 llm_ollama.py

これでターミナルから Fusion HAT+ と直接チャットできます。

* |link_ollama_hub| から **任意のモデル** を選択できますが、8～16GB RAM の場合は  
  ``moondream:1.8b`` や ``phi3:mini`` などの小型モデルを推奨します。  
* コード内のモデル名が、Ollama で取得済みのモデルと一致していることを確認してください。  
* ``exit`` または ``quit`` と入力するとプログラムを終了します。  
* 接続できない場合は、Ollama が実行中であること、リモートホストを使用する場合は同じ LAN に接続されていることを確認してください。

**コード**

.. code-block:: python

   from fusion_hat.llm import Ollama
 
   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   # Change this to your computer IP, if you run it on your pi, then change it to localhost
   llm = Ollama(
      ip="localhost",
      model="llama3.2:3b"
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Response without stream
      # response = llm.prompt(input_text)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


3. Ollamaでビジョン対話
--------------------------

このデモでは、 **質問を入力するたびに** Pi カメラがスナップショットを撮影します。  
プログラムは **入力テキスト + 新しい写真** を Ollama 経由でローカルのビジョンモデルに送信し、  
モデルの回答を英語でストリーミング表示します。  

これは最小構成の「see & tell」デモで、後から色検出・顔認識・QRコード解析などの機能を追加できます。

**開始前に**

#. **Ollama** アプリを起動（またはサービスを実行）し、 **ビジョン対応モデル** をダウンロード済みであることを確認してください。

   * 十分なメモリ（≥16GB RAM）がある場合： ``llava:7b`` を試せます。
   * **8GB RAM** の場合： ``moondream:1.8b`` または ``granite3.2-vision:2b`` を推奨。

   .. image:: img/llm_ollama_image_model.png

**サンプルの実行**

#. サンプルフォルダに移動してスクリプトを実行します：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. 実行時の動作：

   * プログラムはウェルカムメッセージを表示し、入力待ち（ ``>>>`` ）になります。
   * **何か入力するたびに** （例：「hello」「Is there yellow?」「Any faces?」「What is on the desk?」）

     * Pi カメラで **写真を撮影** （ ``/tmp/llm-img.jpg`` に保存）  
     * **テキスト + 写真** を Ollama のビジョンモデルへ送信  
     * モデルの回答を **ストリーミング表示**

   * ``exit`` または ``quit`` と入力すると終了します。

**コード**

.. code-block:: python

   from fusion_hat.llm import Ollama
   from picamera2 import Picamera2
   import time

   '''
   You need to setup ollama first, see llm_local.py

   You need at leaset 8GB RAM to run llava:7b large multimodal model
   '''

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   llm = Ollama(
      ip="localhost",          # e.g., "192.168.100.145" if remote
      model="llava:7b"         # change to "moondream:1.8b" or "granite3.2-vision:2b" for 8GB RAM
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   # Init camera
   camera = Picamera2()
   config = camera.create_still_configuration(
      main={"size": (1280, 720)},
   )
   camera.configure(config)
   camera.start()
   time.sleep(2)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Capture image
      img_path = '/tmp/llm-img.jpg'
      camera.capture_file(img_path)

      # Response without stream
      # response = llm.prompt(input_text, image_path=img_path)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True, image_path=img_path)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


トラブルシューティング
-----------------------------


* **`model requires more system memory ...` というエラーが表示される**

  * モデルがデバイスのメモリ容量に対して大きすぎます。  
  * ``moondream:1.8b`` や ``granite3.2-vision:2b`` などの小型モデルを使用してください。  
  * または RAM の多いマシンで Ollama を実行し、ネットワーク経由で接続してください。

* **コードが Ollama に接続できない（connection refused）**

  次の点を確認してください：

  * Ollama が実行中である（``ollama serve`` またはアプリが起動している）。  
  * リモートPCを使用する場合は **Expose to network** を有効にする。  
  * コード内の ``ip="..."`` が正しい LAN IP である。  
  * 両方のデバイスが同じローカルネットワークに接続されている。

* **Pi カメラが撮影されない**

  * ``Picamera2`` がインストールされ、簡単なテストスクリプトで動作するか確認。  
  * カメラケーブルが正しく接続され、 ``raspi-config`` で有効になっているか確認。  
  * スクリプトが ``/tmp/llm-img.jpg`` に書き込みできる権限を持っているか確認。

* **応答が遅い**

  * 小さいモデルほど高速ですが、回答は簡易になります。  
  * カメラ解像度を下げる（例：1280×720 → 640×480）と処理が高速になります。  
  * Pi 上で不要なプログラムを終了し、CPU と RAM を確保してください。
  