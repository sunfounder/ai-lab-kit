.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_stt_whisper:

3. Vosk による STT（オフライン）
==============================================

Vosk は軽量な speech-to-text（STT）エンジンで、多くの言語に対応しており、Raspberry Pi 上で完全に **オフライン** で動作します。  
インターネット接続が必要なのは、最初に言語モデルをダウンロードするときだけです。その後は、ネットワーク接続なしで利用できます。  

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

このレッスンでは、次の内容を学びます：  

* Raspberry Pi のマイクを確認する  
* 使用する言語モデルを選び、Vosk をインストールしてテストする  

.. start_mic

.. _test_vosk:

プログラムの実行
--------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

新しい言語でこのコードを初めて実行すると、Vosk は次の処理を行います：

* **言語モデルを自動的にダウンロード** します（デフォルトでは small 版）。
* **対応言語の一覧を表示** します。
* マイクからの音声入力を **聞き取り開始** します。

ターミナルには次のような表示が出ます：

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

これは次の意味です：

   * モデルファイル（ ``vosk-model-small-en-us-0.15`` ）のダウンロードが完了した  
   * 対応言語の一覧が表示された  
   * システムが音声の聞き取りを開始した — Fusion HAT+ のマイクに向かって話すと、認識されたテキストがターミナルに表示されます

**ヒント：**

* 認識精度を上げるには、マイクを **15〜30 cm** ほど離して使ってください。  
* **言語やアクセントに合ったモデル** を選んでください。  
* 静かな環境で使うと認識しやすくなります。

コード
---------------

.. code-block:: python

   from fusion_hat.stt import Vosk as STT

   stt = STT(language="en-us")

   while True:
      print("Say something")
      for result in stt.listen(stream=True):
         if result["done"]:
               print(f"final:   {result['final']}")
         else:
               print(f"partial: {result['partial']}", end="\r", flush=True)


**コードの説明：**

* ``stt.listen(stream=True)`` — ストリーミング音声認識を開始し、話している途中の結果も順次返します。  
* ``result["partial"]`` — **リアルタイムの認識結果** を表示します（継続的に更新されます）。  
* ``result["final"]`` — 話し終えたときに、 **最終的な認識結果** を表示します。  
* このループは継続的に動作するため、 **ハンズフリーでのリアルタイム文字起こし** が可能です。

ヒント：このストリーミングモードは、 **音声アシスタント** 、 **音声コマンド制御** 、 **リアルタイム文字起こし** に最適です。

トラブルシューティング
-------------------------

* **No such file or directory（`arecord` 実行時）**

  カード番号またはデバイス番号が間違っている可能性があります。  
  次のコマンドを実行してください：

  .. code-block:: bash

     arecord -l

  表示された USB マイクの番号に合わせて、 ``1,0`` の部分を置き換えてください。


* **Vosk が音声を認識しない**

  * **言語コード** がモデルと一致していることを確認してください（例：英語なら ``en-us``、中国語なら ``zh-cn``）。  
  * マイクは 15〜30 cm ほど離し、周囲の雑音をできるだけ避けてください。  
  * はっきり、ゆっくり話してください。

* **遅延が大きい / 認識が遅い**

  * デフォルトで自動ダウンロードされるのは **small モデル** です（高速ですが、精度はやや低めです）。  
  * それでも遅い場合は、他のプログラムを閉じて CPU リソースを確保してください。  

.. end_mic