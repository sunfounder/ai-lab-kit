.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(示例) AI 驱动的摩斯电码解码器
================================

**简介**

本项目创建一个智能\ **摩斯电码解码器**\ ，利用 AI 解读按键按下的时间模式。系统捕捉精确的计时数据，并借助 OpenAI 的 GPT 实时解码摩斯电码消息。该解码器具有以下特点：

1. **基于计时的输入**：捕捉精确的按下和释放时间
2. **AI 驱动的解码**：使用 GPT 解读点划模式
3. **视觉指示器**：LED 显示当前解码状态
4. **双按键界面**：独立的输入按键和控制按键
5. **实时反馈**：在输入时显示计时数据

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

系统记录按键按下的持续时间，将计时数据发送给 AI 进行解读，并准确解码像通用求救信号 "SOS" 这样的摩斯电码序列。

您可以将时序敏感的输入与 AI 解读相结合，用于各种编码系统。请参阅：

* :ref:`py_online_llm`

----------------------------------------------

**所需材料**

本项目需要以下元器件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 元器件
        - 购买链接
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

**接线图**

按如下方式将元器件连接到 Raspberry Pi：

.. image:: img/fzz/morse_decoder_bb.png
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
      sudo python3 llm_openai_morse_decoder.py

#. 尝试一个简单的摩斯电码消息（例如："SOS"）

   程序启动后，按下开始/停止按钮开始录音。
   然后按下摩斯按键输入点（短按）和划（长按）。

   完成后，再次按下开始/停止按钮停止录音并解码消息。

#. 查看控制台输出

   控制台将显示按下/释放时间戳，AI 将分析计时数据并输出解码后的消息。

   **输入 "SOS" 时的典型控制台输出：**

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

#. 理解工作流程

   1. 开始录音：按下开始/停止按钮（GPIO 17），LED 亮起
   2. 输入摩斯电码：使用摩斯按键（GPIO 22）输入点和划
   3. 实时显示：控制台显示按下/释放时间戳
   4. 停止并解码：再次按下开始/停止按钮，LED 熄灭
   5. AI 分析：计时数据发送至 OpenAI GPT 进行解读
   6. 输出解码结果：AI 打印解码后的消息

**代码**

以下是 AI 驱动的摩斯电码解码器的完整 Python 脚本：

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

**理解代码**

1. GPIO 引脚配置

   三个 GPIO 引脚被配置用于不同的用途：

   .. code-block:: python

      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)

   - 防抖时间（0.05 秒）：防止机械开关抖动导致的多次检测
   - 下拉电阻：确保未按下按钮时信号为低电平
   - 功能分离：输入按键和控制按键分离，防止误触

2. 计时数据存储

   按下/释放事件附带精确的时间戳进行存储：

   .. code-block:: python

      morse_events = []  # Empty list to store events

      # Each event stored as tuple: ('pressed'/'released', timestamp)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. 防抖机制

   防止开关抖动导致的误触发：

   .. code-block:: python

      def morse_input_released():
          if release_time - start_time < 0.1:  # 100ms debounce
              return  # Ignore very short releases

          morse_events.append(('released', release_time))

4. 状态管理

   系统使用标志位来跟踪录音状态：

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

5. 视觉指示器

   LED 提供录音状态的视觉反馈：

   .. code-block:: python

      def handle_start_stop():
          if input_active:
              led.off()  # LED OFF when not recording
          else:
              led.on()   # LED ON when recording

6. AI 提示词构建

   计时数据转换为字符串，供 AI 处理：

   .. code-block:: python

      input_text = str(morse_events)

      # Example format sent to AI:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. 流式响应

   AI 响应被实时处理和显示：

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. 事件驱动架构

   按键事件触发即时回调函数：

   .. code-block:: python

      # Assign callback functions to button events
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. 计时精度

   使用 ``time.time()`` 实现微秒级精确定时：

   .. code-block:: python

      start_time = time.time()  # Current time in seconds since epoch

      # Calculate press duration:
      duration = release_time - start_time

10. 数据清除

    解码完成后，清除事件列表以准备接收下一条消息：

    .. code-block:: python

        def decode_and_print():
            # ... process events ...
            morse_events = []  # Clear for next message

----------------------------------------------

**摩斯电码计时标准**

* 标准计时（基于单词 PARIS）：

  - 点：1 个单位
  - 划：3 个单位
  - 字符内间隔（点/划之间）：1 个单位
  - 字符间间隔（字母之间）：3 个单位
  - 单词间间隔（单词之间）：7 个单位

* 实际实现：

  - 点：< 0.3 秒（短按）
  - 划：> 0.5 秒（长按）
  - 元素之间：< 0.5 秒停顿
  - 字母之间：0.5-1.5 秒停顿
  - 单词之间：> 1.5 秒停顿

* 常见摩斯电码字母：

  - A: • —（点-划）
  - B: — • • •（划-点-点-点）
  - C: — • — •（划-点-划-点）
  - S: • • •（点-点-点）
  - O: — — —（划-划-划）

----------------------------------------------

**故障排除**

- 按键按下无响应

  - 检查接线：GPIO 22/17 连接至按键，另一端接 GND
  - 验证下拉配置是否正确
  - 用简单脚本测试：\ ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``
  - 检查防抖时间设置（0.05 秒可能过高）

- LED 不亮

  - 检查 LED 极性：正极（长脚）通过电阻连接至 GPIO 27
  - 检查电阻值（建议 220Ω）
  - 直接测试 LED：\ ``Pin(27, Pin.OUT).on()`` 应点亮 LED
  - 确保接地连接完整

- 计时数据异常

  - 检查系统时钟：\ ``date`` 命令
  - 如果过于灵敏，减少防抖时间
  - 添加打印语句验证回调执行情况
  - 使用一致的按键持续时间进行测试

- AI 解码不正确

  - 检查 API 密钥和网络连接
  - 检查发送给 AI 的计时数据（打印 ``morse_events``）
  - 确保按键持续时间一致（点短、划长）
  - 在字母之间添加更清晰的停顿

- 单次按下触发多次

  - 增加 ``bounce_time`` 参数（尝试 0.1 秒）
  - 检查机械开关抖动
  - 使用电容添加硬件防抖
  - 验证按键接线是否正确

- 系统对开始/停止无响应

  - 检查是否有其他回调函数干扰
  - 验证 ``input_active`` 标志位逻辑
  - 在 ``handle_start_stop()`` 中添加调试打印
  - 确保没有其他进程使用 GPIO

- AI 响应过慢

  - 检查网络连接速度
  - 减少事件数量（更短的消息）
  - 考虑使用本地解码作为备用方案
  - 为 AI 响应实现超时机制

- 无法区分点和划

  - 练习一致的按键节奏
  - 调整 AI 指令中的阈值
  - 在发送给 AI 之前添加本地预处理
  - 在输入时使用视觉反馈

----------------------------------------------

这款 AI 驱动的摩斯电码解码器展示了精确的计时数据与智能模式识别相结合，如何复兴并使历史通信方式现代化，使其对新一代用户来说既易于上手又富有教育意义！
