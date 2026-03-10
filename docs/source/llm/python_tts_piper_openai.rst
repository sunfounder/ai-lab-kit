.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. Piper と OpenAI による TTS
========================================================

前のレッスンでは、Raspberry Pi 上で動作するシンプルなオフライン TTS エンジン **Espeak** と **Pico2Wave** を紹介しました。  
ここではさらに一歩進んで、 **より高品質な音声** と柔軟性を備えた **高度な TTS オプション** を試してみます：

* **Piper** — ニューラルネットワークベースの高速 TTS エンジンで、Raspberry Pi 上で **完全にオフライン** で動作します。  
* **OpenAI TTS** — **非常に自然で人間らしい音声** を提供するオンラインサービスで、表現豊かな読み上げに適しています。

これらのエンジンを使うことで、Fusion HAT+ の音声はよりリアルで生き生きとしたものになります。

----

.. _test_piper:

1. Piper のテスト
--------------------

Piper は **オフラインのニューラル TTS エンジン** で、モデルを一度インストールすればインターネット接続は不要です。  
複数の **言語** と **音声モデル** に対応しており、組み込み用途の音声出力として非常に強力な選択肢です。

**プログラムを実行する**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* 初回実行時には、選択した **音声モデル** が自動的にダウンロードされます。  
* その後、Fusion HAT+ から ``Hello! I'm Piper TTS.`` と聞こえるはずです。  
* ``set_model()`` に別のモデル名を指定することで、音声や言語を変更できます。

**コード**

.. code-block:: python

  from fusion_hat.tts import Piper

  tts = Piper()

  # List supported languages
  print(tts.available_countrys())

  # List models for English (en_us)
  print(tts.available_models('en_us'))

  # Set a voice model (auto-download if not already present)
  tts.set_model("en_US-amy-low")

  # Say something
  tts.say("Hello! I'm Piper TTS.")

**コードの説明：**

* ``available_countrys()`` — サポートされている言語の一覧を表示します。  
* ``available_models()`` — 指定した言語で利用可能なモデルを表示します。  
* ``set_model()`` — 音声モデルを設定します。モデルが未インストールの場合は自動でダウンロードされます。  
* ``say()`` — テキストを音声に変換して再生します。

💡 **ヒント：** モデルごとに速度、音質、アクセントが異なるため、複数のモデルを試して比較してみてください。軽量モデルは高速ですが、より高品質なモデルもあります。

----

2. OpenAI TTS のテスト
-------------------------------

**API キーの取得と保存**

#. |link_openai_platform| にアクセスしてログインします。 **API keys** ページで **Create new secret key** をクリックします。

   .. image:: img/llm_openai_create.png

#. 必要な情報（Owner、Name、Project、必要に応じて権限）を入力し、 **Create secret key** をクリックします。

   .. image:: img/llm_openai_create_confirm.png

#. キーが作成されたら、すぐにコピーしてください。後から再表示することはできません。紛失した場合は新しいキーを生成する必要があります。

   .. image:: img/llm_openai_copy.png

#. プロジェクトフォルダ（例： ``~/ai-lab-kit/llm`` ）に ``secret.py`` というファイルを作成します：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 次のように API キーを保存します：

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**プログラムを実行する**

.. code-block:: bash
  
  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* プログラムは OpenAI の TTS サービスに接続し、Fusion HAT+ が **自然で表現豊かな音声** で話します。  
* **音声スタイル** を変更したり、 **instructions** を追加することで、声のトーンや感情（悲しい、ドラマチック、楽しいなど）を制御できます。  
* そのため、OpenAI TTS はインタラクティブロボット、ストーリーテリング、教育アシスタントなどに最適です。


**コード**

.. code-block:: python

  from fusion_hat.tts import OpenAI_TTS
  from secret import OPENAI_API_KEY

  # Export your OpenAI_API_KEY before running the script
  # export OPENAI_API_KEY="sk-proj-xxxxxx"

  tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
  # tts.set_model('tts-1')
  tts.set_voice('alloy')
  tts.set_model('gpt-4o-mini-tts')

  msg = "Hello! I'm OpenAI TTS."
  print(f"Say: {msg}")
  tts.say(msg)

  msg = "with instructions, I can say word sadly"
  instructions = "say it sadly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)

  msg = "or say something dramaticly."
  instructions = "say it dramaticly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)


**コードの説明：**

* ``OpenAI_TTS()`` — API キーを使って OpenAI TTS エンジンを初期化します。  
* ``set_model()`` — 使用する TTS モデルを選択します（例： ``gpt-4o-mini-tts`` ）。  
* ``set_voice()`` — 使用する音声（例： ``alloy`` ）を選択します。  
* ``say(text)`` — テキストを音声に変換して再生します。  
* ``say(text, instructions=...)`` — **音声表現の指示** を追加し、話し方のスタイルを動的に制御できます。

**例：** 

- “say it sadly” → やわらかく感情的なトーン  
- “say it dramatically” → ドラマチックで強調された話し方  
- “say it excitedly” → 明るく興奮したトーン

----

トラブルシューティング
------------------------

* **No module named 'secret'**

  ``secret.py`` が Python ファイルと同じフォルダに存在しない可能性があります。  
  スクリプトを実行しているディレクトリに ``secret.py`` を移動してください。例：

  .. code-block:: bash

     ls ~/
     # Make sure you see both: secret.py and your .py file

* **OpenAI: Invalid API key / 401**

  * API キーが正しくコピーされているか確認してください（ ``sk-`` で始まる）。余分なスペースや改行がないかも確認してください。
  * コードで正しく読み込んでいるか確認してください：

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * Raspberry Pi からネットワーク接続できるか確認してください（ ``ping api.openai.com`` ）。

* **OpenAI: Quota exceeded / billing error**

  * OpenAI ダッシュボードで課金設定またはクォータを確認してください。
  * アカウント設定を修正した後に再度実行してください。

* **Piper: tts.say() は動くが音が出ない**

  * 音声モデルが実際に存在するか確認してください：

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * コード内のモデル名が正しいか確認してください：

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * Raspberry Pi の音声出力設定と音量を確認してください（ ``alsamixer`` ）。スピーカーが接続されて電源が入っているかも確認してください。

* **ALSA / sound device エラー（例：「Audio device busy」「No such file or directory」）**

  * 音声デバイスを使用している他のプログラムを終了してください。
  * デバイスが解放されない場合は Raspberry Pi を再起動してください。
  * HDMI とイヤホンジャックの出力を切り替える場合は、Raspberry Pi OS の音声設定で正しいデバイスを選択してください。

* **Python 実行時に Permission denied**

  * 環境によっては ``sudo`` を使用してください：

    .. code-block:: bash

       sudo python3 tts_piper.py

TTS エンジンの比較
-------------------------

.. list-table:: Feature comparison: Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - Item
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - Runs on
     - Raspberry Pi 内蔵（オフライン）
     - Raspberry Pi 内蔵（オフライン）
     - Raspberry Pi / PC（オフライン、モデル必要）
     - クラウド（オンライン、API キー必要）
   * - Voice quality
     - 機械的
     - Espeak より自然
     - 自然（ニューラル TTS）
     - 非常に自然 / 人間らしい
   * - Controls
     - 速度、ピッチ、音量
     - 限定的
     - 音声モデルを選択
     - モデルと音声を選択
   * - Languages
     - 多言語（品質はモデル依存）
     - 限定的
     - 多くの言語・音声モデル
     - 英語が最も高品質（他言語はモデルによる）
   * - Latency / speed
     - 非常に高速
     - 高速
     - Pi 4/5 でリアルタイム（low モデル）
     - ネットワーク依存（通常は低遅延）
   * - Setup
     - 最小限
     - 最小限
     - ``.onnx`` と ``.onnx.json`` モデルをダウンロード
     - API キー作成、クライアント設定
   * - Best for
     - 簡単なテストや基本音声
     - 少し自然なオフライン音声
     - ローカルで高品質音声
     - 最高品質・表現力の高い音声
