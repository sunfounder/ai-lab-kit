.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
   
.. _py_blindfolded_watermelon_game:

(Example) 目隠しスイカ割りゲーム
====================================================

**はじめに**

このプロジェクトでは、インタラクティブな **目隠しスイカ割りゲーム** を作成します。プレイヤーはジョイスティックで 20×20 メートルのグリッド上を移動し、AI アシスタントの音声ガイドだけを頼りに方向を判断します。システムは次の要素で構成されます：

1. X/Y 軸によるプレイヤー移動の **ジョイスティック操作**
2. OpenAI の GPT-4 による **AIガイダンス**
3. Pico2Wave による **Text-to-Speech フィードバック**
4. スイカ位置の **ランダム生成**
5. スマッシュ動作のための **ボタン入力**

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Blindfolded_Watermelon_Smashing_Game.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

プレイヤーは中心点 (0,0) からスタートし、AI アシスタントが音声で提示する方向情報だけを手がかりに、ランダムに配置されたスイカを探します。視覚を使わない没入型のゲーム体験を楽しめます。

さまざまな入力デバイスと LLM モジュールを組み合わせることで、インタラクティブな AI ゲームを作成できます。以下も参照してください：

* :ref:`py_online_llm` 
* :ref:`tts_espeak_pico2wave`
* :ref:`py_joystick`

----------------------------------------------

**必要なもの**

このプロジェクトに必要な部品は以下の通りです：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_joystick`
        - \-
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**配線図**

以下のように部品を Fusion HAT+ に接続します：

.. image:: img/fzz/watermelon_game_bb.png
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
      sudo python3 llm_openai_blindfolded_game.py

#. ゲームをプレイする

   スクリプトを起動すると、ゲームは 20×20 メートルのフィールド内にスイカをランダムに配置します。  
   ジョイスティックで 1 歩ずつ移動し、AI アシスタントの方向ガイダンスを聞きながら進めてください。

   スイカの位置に到達したと思ったら、ボタンを押してスマッシュします。  
   現在座標がスイカ座標と完全一致していれば、ゲームに勝利します。

#. ゲームの仕組みを理解する

   * 座標系：

     - ゲームフィールドは 20×20 メートルのグリッド
     - 座標範囲は (-10,-10) から (10,10)
     - 正の X = 東、負の X = 西
     - 正の Y = 南、負の Y = 北（Y軸が反転）
     - 中心点は (0,0)

   * 移動ルール：

     - ジョイスティック右 → X+1（東）
     - ジョイスティック左 → X-1（西）
     - ジョイスティック上 → Y-1（北）
     - ジョイスティック下 → Y+1（南）
     - 1 回の移動で 1 メートル進む

   * 勝利条件：

     - プレイヤーがスイカ座標に完全一致している必要がある
     - ボタンを押して現在位置で「スマッシュ」する
     - 完全一致で勝利メッセージを表示して終了

   * AI アシスタントの役割：

     - プレイヤー座標とスイカ座標の両方を受け取る
     - 方角（N, NE, E, SE, S, SW, W, NW）で誘導する
     - 距離の目安（メートル）を提示する
     - 音声再生のため、回答は短く保つ


**Code**

Here is the full Python script for the Blindfolded Watermelon Smashing Game:

.. raw:: html

   <run></run>

.. code-block:: python
   
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.adc import ADC
   from fusion_hat.pin import Pin
   from fusion_hat.tts import Pico2Wave
   import random, time
   
   # Register OpenAI API
   # openai.com
   
   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
   
   # Setup TTS
   tts = Pico2Wave()
   tts.set_lang('en-US')
   
   # Setup Joystick
   btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
   x_axis = ADC('A1')
   y_axis = ADC('A0')
   
   def MAP(x, in_min, in_max, out_min, out_max):
       """
       Map a value from one range to another.
       """
       return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   
   def activate():
       global smash_tips
       smash_tips = True
           
   btn_pin.when_activated = activate
   
   # Setup LLM
   INSTRUCTIONS = "This is a blindfolded watermelon-smashing game. A point representing a watermelon is randomly generated within a 20x20 meter area with coordinates ranging from (-10,-10) to (10,10). The player starts from the origin (0,0) and moves using a joystick. Even if the player can't see anything, they press a button to perform a smash action. After smashing, you will receive the watermelon's and player's coordinates. You need to advise the player on the direction of the watermelon, like 'The watermelon is ten meters to your northeast.' If the smash coordinates match, the game ends. Your responses will be converted into speech via TTS, so please keep them brief, ideally within two sentences."
   
   WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant. Use the joystick to move and press the button to smash. I will guide you to find the watermelon. Good luck!"

   
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
   
   # Define the map size and the joystick pins
   watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
   player_x, player_y = 0, 0
   smash_tips = False
   
   while True:
       x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
       y_val = MAP(y_axis.read(), 0, 4095, -100, 100)
       
       if x_val > 80:
           player_x += 1
       elif x_val < -80:
           player_x -= 1
           
       if y_val > 80:
           player_y -= 1
       elif y_val < -80:
           player_y += 1
           
       # Debug positions (commented out in actual game)
       # print('Watermelon position: %d, %d  ' % (watermelon_x, watermelon_y))
       # print('Player position: %d, %d  ' % (player_x, player_y))
   
       time.sleep(0.3)
   
       if smash_tips:
           smash_tips = False
           print("Smash!")
           
           if (player_x, player_y) == (watermelon_x, watermelon_y):
               print("Target hit!")
               tts.say("Target hit!")
               break
           else:
               input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"
               
               # Response with stream
               response = llm.prompt(input_text, stream=True)
               string = ""
               
               for next_word in response:
                   if next_word:
                       # print(next_word, end="", flush=True)  # Uncomment for streaming display
                       string += next_word
                       
               # print("")  # New line after streaming
               print("AI: " + string)
               tts.say(string)
               
   print("Game over!")

----------------------------------------------

**コードの理解**

1. Text-to-Speech の設定

   ゲームでは Pico2Wave を音声フィードバックに使用します：
   
   .. code-block:: python
   
      tts = Pico2Wave()
      tts.set_lang('en-US')
   
   これにより、AI のテキスト応答が英語音声の指示として読み上げられます。

2. ジョイスティック入力の処理

   ジョイスティックは X/Y 軸の読み取りに 2 つの ADC チャンネルを使用します：
   
   .. code-block:: python
   
      x_axis = ADC('A1')  # Horizontal movement
      y_axis = ADC('A0')  # Vertical movement
      
      def MAP(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
      
      # Convert 0-4095 ADC reading to -100 to 100 range
      x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
      y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

3. 割り込みによるボタン設定

   ボタンは割り込みコールバックにより即時反応します：
   
   .. code-block:: python
   
      btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      
      def activate():
          global smash_tips
          smash_tips = True
              
      btn_pin.when_activated = activate
   
   押下されると ``smash_tips`` が ``True`` になり、メインループでスマッシュ動作が実行されます。

4. OpenAI LLM の設定

   AI アシスタントはゲーム用の指示文で構成されます：
   
   .. code-block:: python
   
      INSTRUCTIONS = "This is a blindfolded watermelon-smashing game..."
      WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant..."
      
      llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )
      
      llm.set_max_messages(20)       # Keep conversation history
      llm.set_instructions(INSTRUCTIONS)  # Set game rules
      llm.set_welcome(WELCOME)       # Set initial greeting

5. ゲーム状態の管理

   ゲームはプレイヤー位置とターゲット位置を保持します：
   
   .. code-block:: python
   
      # Random watermelon placement
      watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
      
      # Player starts at center
      player_x, player_y = 0, 0
      
      # Movement thresholds (80% joystick deflection)
      if x_val > 80:
          player_x += 1      # Move right
      elif x_val < -80:
          player_x -= 1      # Move left
          
      if y_val > 80:
          player_y -= 1      # Move up (negative Y)
      elif y_val < -80:
          player_y += 1      # Move down (positive Y)

6. スマッシュ動作と AI 応答

   ボタンが押されると、命中判定を行い、外れた場合は AI へガイダンスを要求します：
   
   .. code-block:: python
   
      if smash_tips:
          smash_tips = False
          print("Smash!")
          
          if (player_x, player_y) == (watermelon_x, watermelon_y):
              print("Target hit!")
              tts.say("Target hit!")
              break  # Game ends
          else:
              # Send positions to AI for guidance
              input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"
              
              # Get streaming response from AI
              response = llm.prompt(input_text, stream=True)
              string = ""
              
              for next_word in response:
                  if next_word:
                      string += next_word
                      
              print("AI: " + string)
              tts.say(string)  # Speak the guidance

7. ストリーミング応答の処理

   AI の応答は、リアルタイム表示に対応できるよう単語（トークン）単位で処理されます：
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      string = ""
      
      for next_word in response:
          if next_word:
              # Uncomment to display words as they arrive
              # print(next_word, end="", flush=True)
              string += next_word

8. デッドゾーン付きの移動ロジック

   ジョイスティックには誤動作を防ぐため、80 ユニットのデッドゾーンがあります：
   
   .. code-block:: python
   
      # Only move when joystick is pushed >80% in any direction
      # This prevents drifting from center position
      if x_val > 80:    # Right
      elif x_val < -80: # Left
      
      if y_val > 80:    # Up
      elif y_val < -80: # Down

9. ゲームループの構造

   メインループは継続的に次を実行します：
   
   1. ジョイスティック位置の読み取り
   2. ジョイスティックが押された場合の座標更新
   3. スマッシュボタン押下の確認
   4. 必要に応じて AI 応答の取得と処理
   5. TTS による音声フィードバック

----------------------------------------------

**トラブルシューティング**

- ジョイスティックが反応しない

  - ADC 配線を確認：Y 軸は A0、X 軸は A1
  - 電源を確認：VCC は 3.3V、GND はグラウンドへ
  - ADC 読み取りテスト： ``print(x_axis.read())`` が 0〜4095 を表示すること
  - ジョイスティックが中央に戻っていること（~2048 付近になるはず）


- TTS から音が出ない

  - 音声出力を確認： ``sudo raspi-config`` → **System Options** → **Audio**
  - スピーカーテスト： ``speaker-test -t sine -f 440``
  - Pico2Wave のインストール確認： ``pico2wave --help``
  - 音量確認： ``alsamixer``
  - 音声セットアップスクリプトを再実行： ``sudo /opt/setup_fusion_hat_audio.sh``

- OpenAI API エラー

  - ``secret.py`` の API キーを確認
  - ネット接続確認： ``ping 8.8.8.8``
  - OpenAI アカウントで課金が有効になっていること
  - モデル "gpt-4o" がアカウントで利用可能であること

- プレイヤーの移動が速すぎる／遅すぎる

  - 移動しきい値（現在 80）を調整：大きいほど強く倒さないと移動しない
  - 移動量（現在 1）を調整：0.5 にすればより細かい制御が可能
  - sleep 時間（現在 0.3s）を調整：長くすると反応が遅くなる


- AI の回答が長すぎる

  - INSTRUCTIONS で短さを強調する
  - 指示に "Respond in 10 words or less" を追加する
  - コード側で応答長をチェックする

----------------------------------------------

この目隠しスイカ割りゲームは、物理入力、AI の誘導、音声フィードバックを組み合わせることで、空間認識と聴覚を頼りに挑戦する、感覚ベースの没入型ゲーム体験を実現できることを示しています！