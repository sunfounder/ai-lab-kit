.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. AI音声アシスタント
===========================

このレッスンでは、Fusion HAT+ を **音声中心のAIアシスタント** に変えます。  
提供されたコードを使用すると、ロボットは **ウェイクワードを待機** し、 **Voskで音声を文字起こし** し、 **OpenAIのLLMへ送信** し、 **Piper TTSで音声応答** を行います。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Voice_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----

開始前に
----------------

以下の準備が完了していることを確認してください：

* :ref:`test_piper` — Piper の音声が正常に動作する（例：「Hello」を再生できる）。  
* :ref:`test_vosk` — 使用する言語で Vosk STT が動作する（例： ``en-us`` ）。  
* :ref:`py_online_llm` — **OpenAI APIキー** を ``secret.py`` に ``OPENAI_API_KEY`` として保存済み。  
* Fusion HAT+ に **マイク** と **スピーカー** が正しく接続されている。  
* 安定したネットワーク接続（LLMはオンラインサービス）。

----

サンプルの実行
------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**コードで使用される構成：**

* LLM: **OpenAI** ( ``gpt-4o-mini`` )  
* TTS: **Piper** ( ``en_US-ryan-low`` )  
* STT: **Vosk** ( ``en-us`` )  
* ウェイクワード: ``"hey buddy"``  
* キーボード入力: **有効** （任意の手動入力）  
* 画像モード: **有効** （ ``WITH_IMAGE=True`` ）— 将来的に画像を扱う場合はマルチモーダル対応LLMが必要

**動作の流れ：**

1. アシスタントがウェイクフレーズ付きのウェルカムメッセージを表示します。  
2. **「hey buddy」** を待機します。  
3. ウェイク後、音声が文字起こしされます（Vosk → テキスト）。  
4. テキストが **OpenAI（gpt-4o-mini）** に送信され、応答が生成されます。  
5. 生成された回答が **Piper** （ ``en_US-ryan-low`` ）で音声再生されます。

**実行例**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What’s the capital of Italy?
   Robot: The capital of Italy is Rome.

コード
-----------------

.. code-block:: python

  from fusion_hat.voice_assistant import VoiceAssistant
  from fusion_hat.llm import OpenAI as LLM
  from secret import OPENAI_API_KEY as API_KEY

  llm = LLM(
      api_key=API_KEY,
      model="gpt-4o-mini",
  )

  # Robot name
  NAME = "Buddy"

  # Enable image, need to set up a multimodal language model
  WITH_IMAGE = True

  # Set models and languages
  LLM_MODEL = "gpt-4o-mini"
  TTS_MODEL = "en_US-ryan-low"
  STT_LANGUAGE = "en-us"

  # Enable keyboard input
  KEYBOARD_ENABLE = True

  # Enable wake word
  WAKE_ENABLE = True
  WAKE_WORD = [f"hey {NAME.lower()}"]
  # Set wake word answer, set empty to disable
  ANSWER_ON_WAKE = "Hi there"

  # Welcome message
  WELCOME = f"Hi, I'm {NAME}. Wake me up with: " + ", ".join(WAKE_WORD)

  # Set instructions
  INSTRUCTIONS = f"""
  You are a helpful assistant, named {NAME}.
  """

  va = VoiceAssistant(
      llm,
      name=NAME,
      with_image=WITH_IMAGE,
      tts_model=TTS_MODEL,
      stt_language=STT_LANGUAGE,
      keyboard_enable=KEYBOARD_ENABLE,
      wake_enable=WAKE_ENABLE,
      wake_word=WAKE_WORD,
      answer_on_wake=ANSWER_ON_WAKE,
      welcome=WELCOME,
      instructions=INSTRUCTIONS,
  )

  if __name__ == "__main__":
      va.run()

**コードの解説**

* ``OpenAI(..., model="gpt-4o-mini")`` — このレッスンでは **OpenAI** を唯一のLLMとして使用します。  
* ``NAME`` / ``WAKE_WORD`` — アシスタント名をカスタマイズできます（例：「Buddy」「hey buddy」）。  
* ``WITH_IMAGE=True`` — アシスタントの画像モードを有効化します（ここでは画像入出力ロジックは含まれていません）。  
* ``TTS_MODEL="en_US-ryan-low"`` — 応答音声として使用する Piper の音声モデル。  
* ``STT_LANGUAGE="en-us"`` — 音声認識に使用する Vosk の言語設定。  
* ``KEYBOARD_ENABLE=True`` — デバッグ時に手動テキスト入力を可能にします。  
* ``WELCOME`` / ``INSTRUCTIONS`` — 起動メッセージとアシスタントの人格（システムプロンプト）。  
* ``va.run()`` — **wake → listen → LLM → speak** のループ処理を開始します。


他のLLMまたはTTSへの切り替え
---------------------------------

いくつかの設定を変更するだけで、他の LLM、TTS、STT 言語へ簡単に切り替えることができます：

* 対応しているLLM：

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — **Piper TTS** が対応する言語を確認できます。  
* :ref:`test_vosk` — **Vosk STT** が対応する言語を確認できます。  

切り替える場合は、コードの初期化部分を変更するだけです：

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key="YOUR_KEY", model="gemini-pro")

   # Set models and languages
   TTS_MODEL = "en_US-ryan-low"
   STT_LANGUAGE = "en-us"



----

トラブルシューティング
-----------------------------

* **ロボットがウェイクワードに反応しない**

  - マイクが正常に動作しているか確認してください。  
  - ``WAKE_ENABLE = True`` になっていることを確認してください。  
  - 発音に合わせてウェイクワードを調整してください。  
  - 周囲のノイズを減らし、はっきりと発話してください。

* **スピーカーから音が出ない**

  - TTSモデル名（例： ``en_US-ryan-low`` ）を確認してください。  
  - Piper または Espeak を手動でテストしてください。  
  - スピーカー接続と音量を確認してください。

* **APIキーエラーまたはタイムアウト**

  - ``secret.py`` 内のキーを確認してください。  
  - ネットワーク接続が安定しているか確認してください。  
  - 使用しているLLMモデル（例： ``gpt-4o-mini`` ）が利用可能か確認してください。

* **ウェイクワードは動作するが応答がない**

  - STT言語設定が発音と一致しているか確認してください。  
  - モデルが正しくダウンロードされているか確認してください。  
  - デバッグログを出力して STT が動作しているか確認してください。

* **TTSは動作するがLLMの応答がない**

  - APIキーが有効か確認してください。  
  - モデル名およびLLM設定を確認してください。  
  - インターネット接続を確認してください。



