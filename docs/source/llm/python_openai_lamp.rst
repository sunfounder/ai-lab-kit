.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_led_controller:

(Example) AI 搭載 LED コントローラー
======================================

**はじめに**

このプロジェクトでは、LLM モデル（ここでは OpenAI の GPT-4o 言語モデルを使用）と RGB LED を組み合わせた **AI 搭載 LED コントローラー** を作成します。  
システムは自然言語の指示を解釈して LED の色を制御し、色名、HEX 値、RGB タプルを使って色を指定できます。これは、自然言語処理を通じて人工知能と物理ハードウェアを統合する例です。

「turn on red light」や「show warm yellow light」のように話しかけると、AI が指示内容を解析し、それに応じた制御信号を生成して LED の色を変更します。

他の LLM モデルを使用する場合は、:ref:`py_online_llm` を参照してください。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Led_Controller.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----------------------------------------------

**必要なもの**

このプロジェクトに必要な部品は以下の通りです：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**配線図**

以下のように RGB LED を Fusion HAT+ に接続します：

.. image:: img/fzz/llm_book_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------------------

**コードの実行**


#. AI LED コントローラーを実行します：

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_lamp.py

#. スクリプトを実行すると：

   * 「Smart Lighting Assistant started!」というウェルカムメッセージが表示されます
   * 次のような自然言語コマンドを入力できます：

     - "turn on red light"
     - "show blue color"  
     - "set to warm white"
     - "turn off the light"

   * AI が応答し、それに応じて LED を制御します
   * プログラムを終了するには 'quit' または 'exit' と入力します

----------------------------------------------

**コード**

以下は AI LED コントローラーの Python スクリプト全体です：

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import re
   from fusion_hat.llm import OpenAI
   from fusion_hat.modules import RGB_LED
   from fusion_hat.pwm import PWM
   from secret import OPENAI_API_KEY

   class AILEDController:
       def __init__(self):
           # Initialize LED
           self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
           
           # Initialize AI assistant
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",
           )
           
           # Enhanced instructions for LED control
           self.instructions = """You are an AI assistant that can control an RGB LED.
           When the user mentions colors, you need to respond with a specific format to control the LED.

           Response format:
           1. Normal conversation part
           2. End with [LED:color] where color can be:
              - Color names: red, green, blue, yellow, purple, etc.
              - HEX values: #FF0000, #00FF00, etc.
              - RGB tuples: (255,0,0), (0,255,0), etc.
              - Numbers: 0xFF0000, etc.

           Examples:
           User: Turn the light red
           You: OK, set to red. [LED:red]
           
           User: Show warm yellow light
           You: Set to warm yellow light. [LED:#FFD700]
           
           User: Turn off the light
           You: Light turned off. [LED:black] or [LED:(0,0,0)]
           
           If the user doesn't mention anything color-related, don't include the [LED:...] tag."""
           
           # Color name to RGB mapping
           self.color_map = {
               'red': (255, 0, 0),
               'green': (0, 255, 0),
               'blue': (0, 0, 255),
               'yellow': (255, 255, 0),
               'purple': (255, 0, 255),
               'cyan': (0, 255, 255),
               'white': (255, 255, 255),
               'black': (0, 0, 0),
               'orange': (255, 165, 0),
               'pink': (255, 192, 203),
               'brown': (165, 42, 42),
               'grey': (128, 128, 128),
               'warmwhite': (255, 197, 143),
           }
           
           self.llm.set_max_messages(20)
           self.llm.set_instructions(self.instructions)
           self.llm.set_welcome("Hello! I'm your smart lighting assistant. I can control RGB LED colors.")
           
           # Initial state: light off
           self.rgb_led.color((0, 0, 0))
       
       def parse_led_command(self, text):
           """Parse LED control command from AI response"""
           pattern = r'\[LED:(.*?)\]'
           match = re.search(pattern, text)
           
           if not match:
               return None, text
               
           led_command = match.group(1).strip()
           display_text = re.sub(pattern, '', text).strip()
           
           return led_command, display_text
       
       def apply_color(self, color_spec):
           """Convert color specification to RGB and apply to LED"""
           color_spec = color_spec.lower().strip()
           
           try:
               # 1. Process color names
               if color_spec in self.color_map:
                   rgb = self.color_map[color_spec]
                   self.rgb_led.color(rgb)
                   return True
               
               # 2. Process hex strings (e.g., #FF0000)
               elif color_spec.startswith('#'):
                   hex_color = color_spec.lstrip('#')
                   if len(hex_color) == 6:
                       rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                       self.rgb_led.color(rgb)
                       return True
               
               # 3. Process RGB tuple strings (e.g., (255,0,0))
               elif color_spec.startswith('(') and color_spec.endswith(')'):
                   numbers = color_spec[1:-1].split(',')
                   if len(numbers) == 3:
                       rgb = tuple(int(num.strip()) for num in numbers)
                       if all(0 <= val <= 255 for val in rgb):
                           self.rgb_led.color(rgb)
                           return True
               
               # 4. Process hex number strings (e.g., 0xFF0000)
               elif color_spec.startswith('0x'):
                   hex_num = int(color_spec, 16)
                   self.rgb_led.color(hex_num)
                   return True
               
               # 5. Try direct integer conversion
               else:
                   try:
                       num = int(color_spec)
                       if 0 <= num <= 0xFFFFFF:
                           self.rgb_led.color(num)
                           return True
                   except ValueError:
                       pass
               
               return False
               
           except Exception as e:
               print(f"Color setting error: {e}")
               return False
       
       def run(self):
           """Main run loop"""
           print("Smart Lighting Assistant started!")
           print("You can say: 'turn on red light', 'show blue', 'set to purple', 'turn off light', etc.")
           print("Type 'quit' or 'exit' to end the program\n")
           
           while True:
               try:
                   user_input = input(">>> ").strip()
                   
                   if user_input.lower() in ['quit', 'exit', 'bye']:
                       print("Goodbye!")
                       self.rgb_led.color((0, 0, 0))
                       break
                   
                   response = self.llm.prompt(user_input, stream=True)
                   
                   full_response = ""
                   for word in response:
                       if word:
                           print(word, end="", flush=True)
                           full_response += word
                   print()
                   
                   led_command, display_only = self.parse_led_command(full_response)
                   
                   if led_command:
                       print(f"Detected LED command: {led_command}")
                       if self.apply_color(led_command):
                           print(f"✓ Applied color: {led_command}")
                       else:
                           print(f"✗ Unrecognized color format: {led_command}")
                           
               except KeyboardInterrupt:
                   print("\nProgram interrupted")
                   self.rgb_led.color((0, 0, 0))
                   break
               except Exception as e:
                   print(f"Error: {e}")
                   continue

   # Enhanced version with direct command support
   class AILEDControllerPro(AILEDController):
       def __init__(self):
           super().__init__()
           
           self.instructions = """You control an RGB LED light. When user mentions colors, add [LED:color_value] at the end.
           
           Color values can be:
           1. English color names: red, green, blue, yellow, purple, cyan, white, black, orange, pink
           2. HEX values: #FF0000
           3. RGB tuples: (255,0,0)
           
           Examples:
           User: Turn on red light
           Response: Red light activated. [LED:red]
           
           User: Turn off the light
           Response: Light turned off. [LED:black]
           
           User: How is the weather today?
           Response: I can't check real-time weather, but I can adjust your lighting! [LED:#FFFFFF]"""
           
           self.llm.set_instructions(self.instructions)
       
       def process_user_input(self, text):
           """Preprocess user input for direct commands"""
           text_lower = text.lower()
           
           direct_commands = {
               'turn on light': 'white',
               'turn off light': 'black',
               'red light': 'red',
               'green light': 'green',
               'blue light': 'blue',
               'yellow light': 'yellow',
               'purple light': 'purple',
               'white light': 'white',
           }
           
           for cmd, color in direct_commands.items():
               if cmd in text_lower:
                   self.apply_color(color)
                   return f"Set to {color}. [LED:{color}]"
           
           return None


   if __name__ == "__main__":
       # Create an instance of the controller
       controller = AILEDControllerPro()
       controller.run()

----------------------------------------------

**コードの理解**

1. AI アシスタントの初期化

   このシステムでは OpenAI の GPT-4o モデルを使用し、特定の形式で LED 制御コマンドを生成するようカスタム instructions を設定しています。

   .. code-block:: python

      self.llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )
      
      self.instructions = """You are an AI assistant that can control an RGB LED...
         ...End with [LED:color] where color can be:...
      """
      
      self.llm.set_instructions(self.instructions)

2. RGB LED の制御

   fusion_hat.modules の RGB_LED クラスを使用して、PWM 経由で 3 つの色チャンネルを制御します。

   .. code-block:: python

      self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
      
      # Set color using RGB tuple
      self.rgb_led.color((255, 0, 0))  # Red
      
      # Set color using hex value
      self.rgb_led.color(0xFF0000)  # Also red

3. 正規表現によるコマンド解析

   AI の応答から LED 制御コマンドを抽出するために、正規表現を使用しています。

   .. code-block:: python

      def parse_led_command(self, text):
          """Parse LED control command from AI response"""
          pattern = r'\[LED:(.*?)\]'
          match = re.search(pattern, text)
          
          if not match:
              return None, text
              
          led_command = match.group(1).strip()
          display_text = re.sub(pattern, '', text).strip()
          
          return led_command, display_text

4. 複数の色指定形式に対応

   コントローラーは柔軟性を高めるため、複数の色指定形式を受け付けます。

   .. code-block:: python

      def apply_color(self, color_spec):
          """Convert color specification to RGB and apply to LED"""
          color_spec = color_spec.lower().strip()
          
          # 1. Color names (red, green, blue, etc.)
          # 2. HEX strings (#FF0000)
          # 3. RGB tuples ((255,0,0))
          # 4. Hex numbers (0xFF0000)
          # 5. Direct integers (16711680)

5. ストリーミング応答

   より自然な会話体験のために、AI の応答を単語ごとにストリーミング表示します。

   .. code-block:: python

      response = self.llm.prompt(user_input, stream=True)
      
      full_response = ""
      for word in response:
          if word:
              print(word, end="", flush=True)
              full_response += word

6. 拡張版 Pro バージョン

   AILEDControllerPro クラスでは、よく使う指示にすばやく応答するための直接コマンド前処理を追加しています。

   .. code-block:: python

      direct_commands = {
          'turn on light': 'white',
          'turn off light': 'black',
          'red light': 'red',
          'green light': 'green',
          # ... etc
      }

----------------------------------------------

**トラブルシューティング**

- No module named 'openai'" error**

   fusion-hat パッケージがインストールされていることを確認してください：  

   .. code-block::

      curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/install-fusion-hat.sh | sudo bash


- “Invalid API key" error

  ``secret.py`` 内の API キーが正しく、有効期限切れになっていないことを確認してください。  
  また、OpenAI アカウントで有効な API キーが存在するか確認してください。

- LED が点灯しない

  - 配線を確認してください（RGB ピンが正しい PWM ポートに接続されているか）  
  - common cathode が GND に接続されているか確認してください  
  - 電流制限抵抗が正しく入っているか確認してください  
  - 簡単なテストコードで各色チャンネルを個別に確認してください

- AI が [LED:...] タグ付きで応答しない

  - system instructions が正しく設定されているか確認してください  
  - より明確な色指定コマンドで試してください  
  - AI モデル（gpt-4o）がアカウントで利用可能か確認してください

- ストリーミング応答が途切れがちに見える

  - ネットワーク接続が安定しているか確認してください  
  - ネットワークタイムアウトを調整して遅延を減らしてください  
  - テスト時は非ストリーミングモードの使用も検討してください

----------------------------------------------

このプロジェクトは、AI が自然言語理解と物理ハードウェア制御を橋渡しし、より直感的なヒューマンマシンインターフェースを実現できることを示しています。