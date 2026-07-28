.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_voice_controlled_fan:

(示例) 语音控制智能风扇
=======================

**简介**

本项目创建了一个智能\ **语音控制风扇**\ ，它结合了语音识别、AI 处理和电机控制。该系统允许用户通过自然语音指令控制风扇转速，并提供多种控制方式：

1. **语音指令**\ ——通过 STT（语音转文字）实现免提操作
2. **物理按钮**\ ——用于手动调节转速
3. **AI 解析**\ ——使用 OpenAI 的 GPT 理解自然语言
4. **声音反馈**\ ——使用蜂鸣器提示按钮操作
5. **双控制界面**\ ——同时支持语音和物理交互

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Voice_Controlled_Smart_Fan.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

智能风扇能理解如"调快一点"、"请减速"或"关闭风扇"等指令，并以相应的动作和语音确认做出响应。

您可以将各种输入和输出模块组合，创建语音控制的智能设备。请参阅：

* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`py_motor`

----------------------------------------------

**所需元件**

本项目需要以下组件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 元件
        - 购买链接
    *   - :ref:`cpn_motor`
        - |link_motor_buy|
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_buzzer`
        - \-
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**接线图**

按如下方式将组件连接到 Fusion HAT+：

.. image:: img/fzz/llm_fan_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**运行示例**


#. 运行代码

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_fan.py

#. 控制风扇

   您可以通过语音指令、按钮或自然语言来控制风扇。

   * 语音指令：

     - "Make it faster" / "Increase speed" → 设置为最高速（100%）
     - "Slow down" / "Reduce speed" → 设置为低速（25%）
     - "Medium speed please" → 设置为中速（50%）
     - "Turn off" / "Stop" → 停止电机（0%）
     - "What's the current speed?" → 播报当前速度
     - "Make it cooler" → 解析为请求更高速度

   * 按钮控制：

     - 每次按下增加 10% 的转速
     - 达到 100% 后，再次按下循环回到 0%
     - 每次按下伴有蜂鸣声确认
     - 当前转速百分比显示在屏幕上

   * 自然语言理解：

     AI 还能理解以下各类表达：

     - "I'm feeling hot, can you make it faster?"
     - "Could you please turn the fan down a bit?"
     - "It's too windy in here!"
     - "Set it to half speed"

--------

**代码**

以下是语音控制智能风扇的完整 Python 脚本：

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.motor import Motor
   from fusion_hat.modules import Buzzer
   from fusion_hat.pin import Pin
   import random, time
   from fusion_hat.stt import STT

   # Initialize Speech-to-Text with English language
   stt = STT(language="en-us")

   # Initialize motor on port M0
   motor = Motor('M0')

   # Initialize button on GPIO 17 with pull-up and debounce
   button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)

   # Initialize buzzer on GPIO 4
   buzzer = Buzzer(Pin(4))

   # Global speed variable (0-100%)
   speed = 0

   # Function for auditory feedback
   def beep():
       buzzer.on()
       time.sleep(0.1)
       buzzer.off()

   # Debounce variables for button
   last_triggered = 0

   # Button callback function
   def speed_up():
       global speed, last_triggered

       # Debounce: ignore if pressed within 500ms
       if time.time() - last_triggered < 0.5:
           return

       last_triggered = time.time()

       # Increase speed by 10%
       speed += 10

       # Wrap around at 100% (go back to 0)
       if speed > 100:
           motor.stop()
           speed = 0
       else:
           motor.power(speed)

       # Auditory feedback
       beep()

       # Print current speed
       print(f"Speed set to: {speed}%")

   # Attach callback to button
   button.when_activated = speed_up

   # Function to parse natural language response and set appropriate speed
   def parse_response_for_speed(text_response):
       """
       Parse the LLM's natural language response to determine speed setting.
       Looks for keywords related to different speed levels.
       Returns the speed level to set (100, 50, 25, or 0)
       """
       text_lower = text_response.lower()

       # Check for "stop" or "off" keywords - highest priority
       if any(word in text_lower for word in ['stop', 'off', 'zero', '0%', 'turn off', 'shut off', 'halt']):
           return 0

       # Check for "slow" or "low" keywords
       if any(word in text_lower for word in ['slow', 'low', '25%', 'quarter', 'minimum', 'gentle']):
           return 25

       # Check for "medium" or "half" keywords
       if any(word in text_lower for word in ['medium', 'half', '50%', 'moderate', 'normal']):
           return 50

       # Check for "fast" or "high" or "full" keywords
       if any(word in text_lower for word in ['fast', 'high', 'full', '100%', 'maximum', 'top']):
           return 100

       # If no specific keywords found, return -1 to indicate no speed change
       return -1

   # Setup LLM with specific instructions for fan control
   INSTRUCTIONS = '''
   You are a fan control assistant. Your task is to interpret the user's speech input and respond with natural language.

   ### Input Format:
   The user will speak their command for fan control.

   ### CRITICAL RULES:
   1. **BE DECISIVE**: Always take clear action based on user requests. Do NOT ask follow-up questions.
   2. **NO CLARIFICATION QUESTIONS**: Never ask "Would you like me to..." or "Should I..." questions.
   3. **ASSUME INTENT**: If the user's request is ambiguous, make a reasonable assumption and take action.
   4. **CONFIRM ACTION**: Always state what action you are taking in your response.

   ### Response Guidelines:
   1. Respond naturally and conversationally to the user's request.
   2. Acknowledge what the user asked for.
   3. Use clear language about what action you're taking.
   4. Use keywords in your response that indicate speed levels:
      - For maximum speed: use words like "fast", "high", "full speed", "maximum"
      - For medium speed: use words like "medium", "half speed", "50%"
      - For low speed: use words like "slow", "low", "quarter speed", "25%"
      - For stopping: use words like "stop", "off", "zero", "turning off"
   5. If the user asks about current status, respond with helpful information.

   ### Example Responses:

   **When asked to go fast:**
   "I'll set the fan to maximum speed for you. Full speed activated!"

   **When asked to slow down:**
   "Reducing the fan speed to low. Enjoy the gentle breeze."

   **When asked for medium speed:**
   "Setting the fan to medium speed. This should be comfortable."

   **When asked to stop:**
   "Stopping the fan now. The motor is turned off."

   **When asked about status:**
   "Your fan is currently at 50% speed. Would you like me to adjust it?"

   '''

   WELCOME = "Hello, I am a fan control assistant. You can ask me to set the fan to fast, medium, slow, or stop it completely. You can also press the button to increase the speed by 10% or decrease it by 10%. If you ask about the current status, I will tell you the current speed. If you don't know what to do, you can ask me for instructions. Good luck!"

   # Initialize OpenAI LLM
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

   # Main loop for voice control
   while True:
       print("Say something")

       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")

               # Get the recognized speech
               input_text = result['final']

               # Add current speed context to the input
               contextual_input = f"Current speed is {speed}%. User says: {input_text}"

               # Get response from LLM
               response = llm.prompt(contextual_input, stream=True)

               # Collect the full response
               full_response = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       full_response += next_word

               print("\n")  # Add newline after response

               # Parse the response to determine speed setting
               new_speed = parse_response_for_speed(full_response)

               # Apply speed change if detected
               if new_speed >= 0:
                   speed = new_speed
                   motor.power(speed)
                   print(f"Speed set to: {speed}%")
               else:
                   print("No speed change detected in response")

           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**理解代码**

1. STT（语音转文字）初始化

   系统使用 STT（语音转文字）进行语音识别：

   .. code-block:: python

      stt = STT(language="en-us")

      for result in stt.listen(stream=True):
          if result["done"]:
              input_text = result['final']
          else:
              print(f"partial: {result['partial']}")

   这提供了实时语音识别，在说话时即可输出部分识别结果。

2. 电机控制设置

   风扇电机通过 M0 端口的 PWM 进行控制：

   .. code-block:: python

      motor = Motor('M0')

      # Set speed as percentage (0-100)
      motor.power(speed)

      # Stop the motor completely
      motor.stop()

3. 带去抖的按钮

   按钮包含去抖处理以防止多次触发：

   .. code-block:: python

      button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      last_triggered = 0

      def speed_up():
          global speed, last_triggered
          if time.time() - last_triggered < 0.5:  # 500ms debounce
              return
          last_triggered = time.time()

4. 声音反馈

   蜂鸣器提供可闻的确认提示：

   .. code-block:: python

      buzzer = Buzzer(Pin(4))

      def beep():
          buzzer.on()
          time.sleep(0.1)
          buzzer.off()

5. 关键词解析函数

   系统解析 AI 响应中的速度指令关键词：

   .. code-block:: python

      def parse_response_for_speed(text_response):
          text_lower = text_response.lower()

          # Check for "stop" or "off" keywords
          if any(word in text_lower for word in ['stop', 'off', 'zero']):
              return 0

          # Check for "slow" or "low" keywords
          if any(word in text_lower for word in ['slow', 'low', '25%']):
              return 25

          # Similar checks for medium and fast

          return -1  # No speed change

6. 向 AI 提供上下文输入

   当前速度被包含在提示词中，以便 AI 做出上下文感知的回复：

   .. code-block:: python

      contextual_input = f"Current speed is {speed}%. User says: {input_text}"
      response = llm.prompt(contextual_input, stream=True)

7. 流式响应处理

   AI 响应逐词处理：

   .. code-block:: python

      full_response = ""
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              full_response += next_word

8. 双控制逻辑

   系统同时支持语音和按钮控制：

   .. code-block:: python

      # Voice control in main loop
      new_speed = parse_response_for_speed(full_response)
      if new_speed >= 0:
          speed = new_speed
          motor.power(speed)

      # Button control via callback
      def speed_up():
          speed += 10
          if speed > 100:
              speed = 0
          motor.power(speed)

9. 清除终端输出

   使用 ANSI 转义码实现干净的终端显示：

   .. code-block:: python

      print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

   - ``\r``\ ：回车（回到行首）
   - ``\x1b[K``\ ：从光标清除到行尾
   - ``end=""``\ ：不换行
   - ``flush=True``\ ：立即显示

10. 智能 AI 指令

    AI 被特别指示要果断决策，避免询问澄清问题：

    .. code-block:: python

        INSTRUCTIONS = '''
        CRITICAL RULES:
        1. BE DECISIVE: Always take clear action based on user requests.
        2. NO CLARIFICATION QUESTIONS: Never ask "Would you like me to..." questions.
        3. ASSUME INTENT: If ambiguous, make reasonable assumption and take action.
        4. CONFIRM ACTION: Always state what action you are taking.
        '''

----------------------------------------------

**故障排除**

- 电机不转动

  - 检查电机连接：M0 端口，极性正确
  - 直接测试电机：\ ``motor.power(50)``\ 应以 50% 转速旋转
  - 确保转速变量已被设置（范围 0-100）

- 按钮无响应

  - 检查接线：GPIO 17 接按钮，另一端接 3.3V
  - 验证上拉配置
  - 使用简单脚本测试：按钮状态变化时打印
  - 检查去抖时间（0.5 秒可能过长）

- 蜂鸣器无声

  - 直接测试蜂鸣器：\ ``buzzer.on()``\ 应发出持续音调
  - 检查蜂鸣器类型：压电式（需要 PWM）或有源型（直流驱动）

- AI 无法理解指令

  - 检查 ``secret.py``\ 中的 API 密钥
  - 验证网络连接
  - 检查 AI 指令的格式是否正确
  - 先尝试更简单的指令

- 速度意外变化

  - 检查按钮去抖：可能触发了多次
  - 验证关键词解析：某些短语可能触发意外速度
  - 添加打印语句以追踪速度变化

- 语音识别准确率低

  - 减少背景噪音
  - 清晰且以适中语速说话
  - 考虑使用外置 USB 麦克风以获得更好音质
  - 如有可用，调整 STT 参数

- 电机有响声但不转动

  - 检查电机是否卡住或受阻
  - 验证电源电压是否符合电机要求
  - 某些电机需要在端子间并联电容以实现平稳运行

----------------------------------------------

这个语音控制风扇展示了自然语言处理、物理控制和智能系统如何结合，创造出直观便捷的智能家居设备，响应人类的需求和偏好！
