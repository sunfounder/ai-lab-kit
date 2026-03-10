.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. ローカル音声チャットボット
================================

このレッスンでは、これまで学んだ **音声認識（STT）**、  
**音声合成（TTS）**、そして **ローカルLLM（Ollama）** を組み合わせて、  
Fusion HAT+ 上で完全オフラインで動作する **音声チャットボット** を構築します。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Local_Voice_Chatbot.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

ワークフローはシンプルです：

#. **聞く** — マイクがあなたの音声を取得し、 **Vosk** で文字起こしします。  
#. **考える** — テキストは Ollama 上で動作するローカル **LLM** （例： ``llama3.2:3b`` ）に送信されます。  
#. **話す** — チャットボットが **Piper TTS** を使って音声で応答します。  

これにより、リアルタイムで理解し応答できる **ハンズフリーの会話型ロボット** を実現できます。

----

開始前に
----------------

以下の準備が完了していることを確認してください：

* **Piper TTS** （ :ref:`test_piper` ）をテストし、使用する音声モデルを選んでいること。  
* **Vosk STT** （ :ref:`test_vosk` ）をテストし、適切な言語パック（例： ``en-us`` ）を選んでいること。  
* **Ollama** （ :ref:`download_ollama` ）を Pi または別のコンピュータにインストールし、 ``llama3.2:3b`` のようなモデルをダウンロード済みであること（メモリが限られている場合は ``moondream:1.8b`` のような小さなモデルを使用）。

----

サンプルの実行
--------------

#. サンプルスクリプトを開きます：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano local_voice_chatbot.py

#. 必要に応じてパラメータを更新します：

   * ``stt = Vosk(language="en-us")`` : 使用するアクセントや言語パックに合わせて変更します（例： ``en-us`` 、 ``zh-cn`` 、 ``es`` ）。  
   * ``tts.set_model("en_US-amy-low")`` : :ref:`test_piper` で確認した Piper の音声モデルに置き換えます。  
   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")`` : ``ip`` と ``model`` の両方を自分の環境に合わせて更新します。  

     * ``ip``: Ollama を **同じ Pi** 上で実行している場合は ``localhost`` を使います。LAN 内の別のコンピュータで Ollama を実行している場合は、Ollama で **Expose to network** を有効にし、そのコンピュータの LAN IP を ``ip`` に設定します。  
     * ``model``: Ollama でダウンロードまたは有効化したモデル名と完全に一致している必要があります。  

#. スクリプトを実行します：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo python3 local_voice_chatbot.py

#. 実行後、次のような動作になります：

   * ボットが音声付きのウェルカムメッセージで挨拶します。  
   * 音声入力を待機します。  
   * Vosk が音声をテキストに変換します。  
   * テキストは Ollama に送信され、応答がストリーミングで返されます。  
   * 応答は整形され（内部的な思考出力を除去）、Piper によって音声で読み上げられます。  
   * ``Ctrl+C`` でいつでもプログラムを停止できます。

----

コード
---------

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

   # Initialize speech recognition
   stt = Vosk(language="en-us")

   # Initialize TTS
   tts = Piper()
   tts.set_model("en_US-amy-low")

   # Instructions for the LLM
   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

   # Initialize Ollama connection
   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

   # Utility: clean hidden reasoning
   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

   def main():
       print(WELCOME)
       tts.say(WELCOME)

       try:
           while True:
               print("\n🎤 Listening... (Press Ctrl+C to stop)")

               # Collect final transcript from Vosk
               text = ""
               for result in stt.listen(stream=True):
                   if result["done"]:
                       text = result["final"].strip()
                       print(f"[YOU] {text}")
                   else:
                       print(f"[YOU] {result['partial']}", end="\r", flush=True)

               if not text:
                   print("[INFO] Nothing recognized. Try again.")
                   time.sleep(0.1)
                   continue

               # Query Ollama with streaming
               reply_accum = ""
               response = llm.prompt(text, stream=True)
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       reply_accum += next_word
               print("")

               # Clean and speak
               clean = strip_thinking(reply_accum)
               if clean:
                   tts.say(clean)
               else:
                   tts.say("Sorry, I didn't catch that.")

               time.sleep(0.05)

       except KeyboardInterrupt:
           print("\n[INFO] Stopping...")
       finally:
           tts.say("Goodbye!")
           print("Bye.")

   if __name__ == "__main__":
       main()

----

コードの解説
----------------

**インポートとグローバル設定**

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

ここでは、前のレッスンで構築した 3 つのサブシステムを読み込んでいます：  
音声認識用の **Vosk**、LLM 用の **Ollama**、音声合成用の **Piper** です。



**STT（Vosk）の初期化**

.. code-block:: python

   stt = Vosk(language="en-us")

米国英語用の Vosk モデルを読み込みます。  
認識精度を高めるため、言語コード（例： ``zh-cn`` 、 ``es`` ）は使用する音声パックに合わせて変更してください。



**TTS（Piper）の初期化**

.. code-block:: python

   tts = Piper()
   tts.set_model("en_US-amy-low")

Piper エンジンを作成し、特定の音声モデルを選択します。  
:ref:`test_piper` で確認済みのモデルを使ってください。低品質の音声モデルは高速で、CPU 使用率も低くなります。



**LLM への指示とウェルカムメッセージ**

.. code-block:: python

   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

ここには UX 上の重要な 2 つの工夫があります：

* **短く直接的な回答** にすること（TTS で聞き取りやすくなるため）。
* 不要な出力を減らすため、内部的な “chain-of-thought” タグを明示的に禁止すること。



**Ollama への接続と会話履歴の設定**

.. code-block:: python

   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

* ``ip="localhost"`` は、Ollama サーバーが同じ Pi 上で動作している前提です。別の LAN 内マシンで動作している場合は、そのコンピュータの **LAN IP** を指定し、Ollama で *Expose to network* を有効にしてください。
* ``set_max_messages(20)`` は短めの会話履歴を保持します。メモリや遅延が厳しい場合は、この値をさらに小さくしてください。

**読み上げ前に内部思考 / タグを除去**

.. code-block:: python

   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

一部のモデルは ``<think>…`` のような内部用タグを出力することがあります。  
この関数はそれらを削除し、TTS が **最終的な回答だけ** を読み上げるようにします。

**Tip:** 画面上には生のトークンが表示される場合がありますが、この関数によって **音声出力** はクリーンに保たれます。

**メインループ：最初に挨拶し、その後 listen → think → speak を繰り返す**

.. code-block:: python

   print(WELCOME)
   tts.say(WELCOME)

ターミナルとスピーカーの両方でユーザーに挨拶します。これは起動時に 1 回だけ実行されます。

**聞く（ライブ partial 付きのストリーミング STT）**

.. code-block:: python

   print("\n🎤 Listening... (Press Ctrl+C to stop)")

   text = ""
   for result in stt.listen(stream=True):
       if result["done"]:
           text = result["final"].strip()
           print(f"[YOU] {text}")
       else:
           print(f"[YOU] {result['partial']}", end="\r", flush=True)

* ``stream=True`` により、すぐに確認できる **partial** 文字起こしと、発話終了時の **final** 文字起こしが得られます。
* 最終的に認識されたテキストは ``text`` に保存され、一度だけ表示されます。

**Guard:** 何も認識されなかった場合は、LLM 呼び出しをスキップします：

.. code-block:: python

   if not text:
       print("[INFO] Nothing recognized. Try again.")
       time.sleep(0.1)
       continue

これにより、空のプロンプトをモデルへ送信することを防ぎ、時間とトークンを節約できます。

**考える（LLM）＋ ストリーミング表示**

.. code-block:: python

   reply_accum = ""
   response = llm.prompt(text, stream=True)
   for next_word in response:
       if next_word:
           print(next_word, end="", flush=True)
           reply_accum += next_word
   print("")

* 最終的な文字起こし結果をローカル LLM に送信し、 **トークン到着ごとに表示** することで低遅延の応答を実現します。
* 同時に、後処理のために ``reply_accum`` に完全な応答を蓄積します。

**Note:** 生のトークンを表示したくない場合は、 ``stream=False`` にして最終文字列だけを表示してください。

**話す（先に整形し、その後 TTS を 1 回だけ実行）**

.. code-block:: python

   clean = strip_thinking(reply_accum)
   if clean:
       tts.say(clean)
   else:
       tts.say("Sorry, I didn't catch that.")

* 最終テキストから不要なタグを除去した後、 **1 回だけ** 読み上げます。  
* TTS を 1 回にまとめることで、「[LLM] / [SAY]」のような重複した出力を避けられます。


**終了処理とクリーンアップ**

.. code-block:: python

   except KeyboardInterrupt:
       print("\n[INFO] Stopping...")
   finally:
       tts.say("Goodbye!")
       print("Bye.")

**Ctrl+C** で停止できます。終了時に短い別れの言葉を発声し、正常終了したことを示します。


----

トラブルシューティング
------------------------------

* **モデルが大きすぎる（メモリエラー）**

  ``moondream:1.8b`` のような小さなモデルを使用するか、より高性能なコンピュータ上で Ollama を実行してください。  

* **Ollama から応答が返らない**

  Ollama が起動していることを確認してください（ ``ollama serve`` またはデスクトップアプリ）。リモート接続の場合は **Expose to network** を有効にし、IP アドレスを確認してください。  

* **Vosk が音声を認識しない** 

  マイクが正常に動作していることを確認してください。必要に応じて別の言語パック（ ``zh-cn`` 、 ``es`` など）も試してください。  

* **Piper が無音、またはエラーになる**  

  選択した音声モデルがダウンロード済みであり、:ref:`test_piper` で正常にテストされていることを確認してください。  

* **回答が長すぎる、または話がそれる**

  ``INSTRUCTIONS`` に **“Keep answers short and to the point.”** を追加してください。  




