.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(Example) AI 搭載モールス信号デコーダー
========================================

**はじめに**

このプロジェクトでは、ボタンの押下タイミングのパターンを AI で解釈するインテリジェントな **モールス信号デコーダー** を作成します。  
システムは正確なタイミングデータを取得し、OpenAI の GPT を活用して、モールス信号のメッセージをリアルタイムでデコードします。主な機能は以下の通りです：

1. 押下・解放の正確な時刻を記録する **タイミングベース入力**
2. GPT を用いた **AI デコード** による点・線パターンの解釈
3. デコード中であることを示す LED の **視覚インジケーター**
4. 入力用ボタンと制御用ボタンを分けた **2 ボタンインターフェース**
5. 入力中のタイミングデータをその場で表示する **リアルタイムフィードバック**

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

このシステムはボタンの押下時間を記録し、そのタイミングデータを AI に送って解釈させることで、世界共通の救難信号である「SOS」のようなモールス信号列を正確にデコードできます。

タイミングに敏感な入力と AI による解釈を組み合わせることで、さまざまな符号化システムに応用できます。以下も参照してください：

* :ref:`py_online_llm` 

----------------------------------------------

**必要なもの**

このプロジェクトに必要な部品は以下の通りです：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_button`
        - |link_button_buy| (x2)
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**配線図**

以下のように部品を Raspberry Pi に接続します：

.. image:: img/fzz/morse_decoder_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**サンプルの実行**

#. コードを実行する

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_morse_decoder.py

#. 簡単なモールス信号メッセージを試す（例："SOS"）

   プログラム開始後、start/stop ボタンを押して記録を開始します。  
   その後、モールス用ボタンを使って、点（短押し）と線（長押し）を入力します。

   入力が終わったら、もう一度 start/stop ボタンを押して記録を終了し、メッセージをデコードします。

#. コンソール出力を確認する

   コンソールには押下／解放のタイムスタンプが表示され、AI がそのタイミングデータを解析して、
   デコード結果を出力します。

   **"SOS" を入力したときの典型的なコンソール出力：**

   .. code-block:: text

      To decode the Morse code message based on the button press times provided, we need to interpret the duration of each press. Typically, a short press (dot) is around 0.2 to 0.3 seconds, while a long press (dash) is about 0.5 seconds or longer. Let's analyze the press durations:

      1. `1767773542.1257536` to `1767773542.285196` - Duration: ~0.16 seconds - Dot (.)
      2. `1767773542.4936137` to `1767773542.6315389` - Duration: ~0.14 seconds - Dot (.)
      3. `1767773542.9092748` to `1767773543.0543947` - Duration: ~0.15 seconds - Dot (.)
      4. `1767773544.2299025` to `1767773544.5774245` - Duration: ~0.35 seconds - Dash (-)
      5. `1767773545.1017563` to `1767773545.4954002` - Duration: ~0.39 seconds - Dash (-)
      6. `1767773546.11932` to `1767773546.5881057` - Duration: ~0.47 seconds - Dash (-)
      7. `1767773547.824543` to `1767773547.9534554` - Duration: ~0.13 seconds - Dot (.)
      8. `1767773548.1879761` to `1767773548.2895174` - Duration: ~0.10 seconds - Dot (.)
      9. `1767773548.5281847` to `1767773548.6453152` - Duration: ~0.12 seconds - Dot (.)

      Now let's decode the sequence into letters using Morse code:

      - `...` (Dot Dot Dot) = S
      - `---` (Dash Dash Dash) = O
      - `...` (Dot Dot Dot) = S

      Putting it all together, the decoded message is "SOS".

#. ワークフローを理解する

   1. 記録開始：start/stop ボタン（GPIO 17）を押すと LED が ON になります
   2. モールス信号を入力：モールス用ボタン（GPIO 22）で点と線を入力します
   3. リアルタイム表示：コンソールに押下／解放のタイムスタンプが表示されます
   4. 停止してデコード：もう一度 start/stop ボタンを押すと LED が OFF になります
   5. AI 解析：タイミングデータが OpenAI GPT に送られて解釈されます
   6. デコード結果：AI が解読したメッセージを表示します

**コード**

以下は AI 搭載モールス信号デコーダーの Python スクリプト全体です：

.. raw:: html

   <run></run>

.. code-block:: python
   
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.pin import Pin
   import random, time
   
   # Register OpenAI API
   # openai.com
   
   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
   
   # Setup GPIO pins
   morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   led = Pin(27, Pin.OUT)  # Indicator LED on GPIO 27
   
   # Store the morse code events with timing data
   morse_events = []
   input_active = False  # Flag to indicate if input is active
   
   # Setup LLM with Morse code decoding instructions
   INSTRUCTIONS = "You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it."
   
   WELCOME = "Hello, I am a Morse code decoder. Please press the button to start decoding. When you are done, press the button again to stop."
   
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o",
   )
   
   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)
   
   print(WELCOME)
   
   # Send the morse code timing data to the AI for decoding
   def decode_and_print():
       global morse_events
       
       # Convert timing events to string for AI processing
       input_text = str(morse_events)
       
       # Get response from AI with streaming
       response = llm.prompt(input_text, stream=True)
       
       # Print streaming response
       for next_word in response:
           if next_word:
               print(next_word, end="", flush=True)
       
       print("")  # New line after complete response
       
       morse_events = []  # Clear the morse code events for next message
   
   # Morse code input handling variables
   start_time = 0
   
   # Function called when morse input button is pressed
   def morse_input_pressed():
       global start_time
       start_time = time.time()  
       morse_events.append(('pressed', start_time))
       print(f" Pressed at {start_time} -", end="")
   
   # Function called when morse input button is released
   def morse_input_released():
       global morse_events, start_time
       release_time = time.time()  
       
       # Debounce: ignore releases within 0.1 seconds
       if release_time - start_time < 0.1:
           return
       
       morse_events.append(('released', release_time))
       print(f" {release_time}")
   
   # Start/stop button handler
   def handle_start_stop():
       global input_active, morse_events
       
       if input_active:
           # Stop recording and decode
           led.off()
           print("Input stopped and decoded.")
           decode_and_print()
           input_active = False
       else:
           # Start recording new message
           input_active = True
           morse_events.clear()  # Clear previous events
           led.on()
           print("Input started.")
   
   # Add event listeners to buttons
   start_stop_button.when_activated = handle_start_stop
   morse_input.when_activated = morse_input_pressed
   morse_input.when_deactivated = morse_input_released
   
   # Main program loop
   try:
       while True:
           time.sleep(0.1)
   except KeyboardInterrupt:
       pass


----------------------------------------------

**コードの理解**

1. GPIO ピンの設定

   3 本の GPIO ピンをそれぞれ異なる用途で設定しています：
   
   .. code-block:: python
   
      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)
   
   - バウンスタイム（0.05 秒）：メカニカルスイッチのチャタリングによる多重検出を防ぎます
   - プルダウン：ボタン未押下時に安定した LOW 信号を保ちます
   - 役割分離：入力ボタンと制御ボタンを分けることで誤入力を防ぎます

2. タイミングデータの保存

   押下／解放イベントは正確なタイムスタンプとともに保存されます：
   
   .. code-block:: python
   
      morse_events = []  # Empty list to store events
      
      # Each event stored as tuple: ('pressed'/'released', timestamp)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. デバウンス機構

   スイッチのチャタリングによる誤検出を防ぎます：
   
   .. code-block:: python
   
      def morse_input_released():
          if release_time - start_time < 0.1:  # 100ms debounce
              return  # Ignore very short releases
          
          morse_events.append(('released', release_time))

4. 状態管理

   システムはフラグを使って記録状態を管理します：
   
   .. code-block:: python
   
      input_active = False  # Initially not recording
      
      def handle_start_stop():
          if input_active:
              # Stop recording and decode
              input_active = False
          else:
              # Start recording
              input_active = True
              morse_events.clear()  # Clear previous data

5. 視覚インジケーター

   LED によって記録状態を視覚的に確認できます：
   
   .. code-block:: python
   
      def handle_start_stop():
          if input_active:
              led.off()  # LED OFF when not recording
          else:
              led.on()   # LED ON when recording

6. AI へのプロンプト構築

   タイミングデータは AI が処理しやすいよう文字列化して送信します：
   
   .. code-block:: python
   
      input_text = str(morse_events)
      
      # Example format sent to AI:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. ストリーミング応答

   AI の応答はリアルタイムで処理・表示されます：
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. イベント駆動アーキテクチャ

   ボタンイベントに対して即時にコールバックが実行されます：
   
   .. code-block:: python
   
      # Assign callback functions to button events
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. タイミング精度

   ``time.time()`` を使って高精度のタイミングを取得します：
   
   .. code-block:: python
   
      start_time = time.time()  # Current time in seconds since epoch
      
      # Calculate press duration:
      duration = release_time - start_time

10. データのクリア

    デコード後は、次のメッセージ入力に備えてイベントリストをクリアします：
    
    .. code-block:: python
    
        def decode_and_print():
            # ... process events ...
            morse_events = []  # Clear for next message

----------------------------------------------

**モールス信号のタイミング基準**

* 標準タイミング（単語 PARIS 基準）：

  - 点：1 単位
  - 線：3 単位
  - 文字内間隔（点・線の間）：1 単位
  - 文字間隔（文字と文字の間）：3 単位
  - 単語間隔（単語と単語の間）：7 単位

* 実用上の目安：

  - 点：0.3 秒未満（短押し）
  - 線：0.5 秒超（長押し）
  - 要素間：0.5 秒未満の間隔
  - 文字間：0.5〜1.5 秒の間隔
  - 単語間：1.5 秒超の間隔

* よく使うモールス信号の文字：

  - A: • —（点・線）
  - B: — • • •（線・点・点・点）
  - C: — • — •（線・点・線・点）
  - S: • • •（点・点・点）
  - O: — — —（線・線・線）

----------------------------------------------

**トラブルシューティング**

- ボタン入力が認識されない

  - 配線を確認してください：GPIO 22 / 17 からボタンへ、反対側は Ground へ接続
  - プルダウン設定を確認してください
  - 簡単なスクリプトでテスト： ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``
  - バウンスタイム設定を確認してください（0.05 秒が長すぎる場合があります）

- LED が点灯しない

  - LED の極性を確認してください：アノード（長い脚）は抵抗を介して GPIO 27 へ
  - 抵抗値を確認してください（220Ω 推奨）
  - 直接テスト： ``Pin(27, Pin.OUT).on()`` で LED が点灯するはずです
  - GND 接続が正しく完了しているか確認してください

- タイミングデータがおかしい

  - システムクロックを確認： ``date`` コマンド
  - 反応が敏感すぎる場合はデバウンス時間を下げてください
  - print を追加してコールバックが正しく実行されているか確認してください
  - 一定の長さで押すテストを行ってください

- AI が正しくデコードできない

  - API キーとインターネット接続を確認してください
  - AI に送っているタイミングデータを確認してください（ ``morse_events`` を print）
  - 押下時間を安定させてください（点は短く、線は長く）
  - 文字の間により明確な間隔を入れてください

- 1 回押しただけで複数回トリガーされる

  - ``bounce_time`` パラメータを増やしてください（0.1 秒など）
  - メカニカルスイッチのチャタリングを確認してください
  - コンデンサによるハードウェアデバウンスを追加してください
  - ボタン配線が正しいか確認してください

- start/stop に反応しない

  - 他のコールバックが干渉していないか確認してください
  - ``input_active`` フラグのロジックを確認してください
  - ``handle_start_stop()`` にデバッグ用 print を追加してください
  - 他のプロセスが GPIO を使用していないことを確認してください

- AI の応答が遅い

  - インターネット接続速度を確認してください
  - イベント数を減らしてください（短いメッセージで試す）
  - 代替としてローカルデコードの導入も検討してください
  - AI 応答にタイムアウト処理を追加してください

- 点と線を区別しにくい

  - タイミングを一定にする練習をしてください
  - AI への instructions 内の閾値を調整してください
  - AI に送る前にローカル前処理を追加してください
  - 入力中に視覚フィードバックを追加すると分かりやすくなります

----------------------------------------------


この AI 搭載モールス信号デコーダーは、正確なタイミングデータと高度なパターン認識を組み合わせることで、歴史ある通信手段を現代的に再解釈し、新しい世代にとって学びやすく親しみやすい形で活用できることを示しています。