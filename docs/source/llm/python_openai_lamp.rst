.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_led_controller:

（示例）AI 驱动 LED 控制器
=============================

**简介**

在这个项目中，你将构建一个\ **AI 驱动 LED 控制器**\ ，将 LLM 模型（这里使用 OpenAI 的 GPT-4o 语言模型）与 RGB LED 相结合。该系统可以解析控制 LED 颜色的自然语言指令，让你通过语音请求特定的颜色——使用颜色名称、HEX 值或 RGB 元组。这展示了人工智能通过自然语言处理与物理硬件集成的能力。

当你说出"打开红灯"或"显示暖黄光"等指令时，AI 会解析你的请求并生成适当的控制信号来相应地调整 LED。

要使用其他 LLM 模型，请参考 :ref:`py_online_llm`。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Led_Controller.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----------------------------------------------

**所需组件**

本项目需要以下组件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 组件
        - 购买链接
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

**接线图**

按以下方式将 RGB LED 连接到 Fusion HAT+：

.. image:: img/fzz/llm_book_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------------------

**运行代码**


#. 运行 AI LED 控制器：

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_lamp.py

#. 脚本运行后：

   * 你会看到一条欢迎消息："Smart Lighting Assistant started!"
   * 输入自然语言指令，例如：

     - "turn on red light"
     - "show blue color"
     - "set to warm white"
     - "turn off the light"

   * AI 将做出响应并相应地控制 LED
   * 输入 'quit' 或 'exit' 结束程序

----------------------------------------------

**代码**

以下是 AI LED 控制器的完整 Python 脚本：

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

**理解代码**

1. AI 助手初始化

   系统使用 OpenAI 的 GPT-4o 模型，配合自定义指令，以确保其以特定格式生成 LED 控制指令。

   .. code-block:: python

      self.llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      self.instructions = """You are an AI assistant that can control an RGB LED...
         ...End with [LED:color] where color can be:...
      """

      self.llm.set_instructions(self.instructions)

2. RGB LED 控制

   fusion_hat.modules 中的 RGB_LED 类提供了通过 PWM 控制三个颜色通道的接口。

   .. code-block:: python

      self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)

      # Set color using RGB tuple
      self.rgb_led.color((255, 0, 0))  # Red

      # Set color using hex value
      self.rgb_led.color(0xFF0000)  # Also red

3. 使用正则表达式解析指令

   系统使用正则表达式从 AI 回复中提取 LED 控制指令。

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

4. 多种颜色格式支持

   控制器接受各种颜色规格格式，以提供最大的灵活性。

   .. code-block:: python

      def apply_color(self, color_spec):
          """Convert color specification to RGB and apply to LED"""
          color_spec = color_spec.lower().strip()

          # 1. Color names (red, green, blue, etc.)
          # 2. HEX strings (#FF0000)
          # 3. RGB tuples ((255,0,0))
          # 4. Hex numbers (0xFF0000)
          # 5. Direct integers (16711680)

5. 流式回复

   AI 的回复逐词流式输出，带来更自然的对话体验。

   .. code-block:: python

      response = self.llm.prompt(user_input, stream=True)

      full_response = ""
      for word in response:
          if word:
              print(word, end="", flush=True)
              full_response += word

6. 增强版 Pro 版本

   AILEDControllerPro 类添加了直接指令预处理功能，以便更快速响应常见请求。

   .. code-block:: python

      direct_commands = {
          'turn on light': 'white',
          'turn off light': 'black',
          'red light': 'red',
          'green light': 'green',
          # ... etc
      }

----------------------------------------------

**故障排除**

- "No module named 'openai'" 错误

   确保已安装 fusion-hat 包：

   .. code-block::

      curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/install-fusion-hat.sh | sudo bash


- "Invalid API key" 错误

  验证 ``secret.py``\ 中的 API 密钥正确且未过期。
  检查你的 OpenAI 账户是否有有效的 API 密钥。

- LED 不亮

  - 检查接线（RGB 引脚连接到正确的 PWM 端口）
  - 检查共阴极是否连接到地
  - 确保限流电阻正确安装
  - 使用简单的测试代码单独测试每个颜色通道

- AI 回复中不包含 [LED:...] 标签

  - 检查系统指令是否正确设置
  - 尝试更明确的颜色指令
  - 确保 AI 模型（gpt-4o）在你的账户中可用

- 流式回复显得断续

  - 检查网络连接的稳定性
  - 通过调整网络超时减少流延迟
  - 测试时可考虑使用非流式模式

----------------------------------------------

该项目展示了 AI 如何桥接自然语言理解与物理硬件控制，为直观的人机交互界面开辟了可能性！
