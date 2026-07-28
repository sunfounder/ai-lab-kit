.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_health_assistant:

（示例）带体温监测的 AI 健康助手
================================

**简介**

该项目创建了一个智能的\ **AI 健康助手**\ ，将体温感应与语音交互相结合，提供个性化的健康评估。该系统集成了：

1. **基于热敏电阻的体温感应**\ ：用于精确测量体温
2. **语音识别**\ ：用于理解用户的症状和询问
3. **AI 健康分析**\ ：使用 OpenAI GPT 进行医疗评估
4. **文字转语音反馈**\ ：提供可听的健康建议
5. **实时监测**\ ：持续的温度转换

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Health_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

健康助手通过热敏电阻电路测量体温，使用 AI 分析读数，并根据公认的医疗温度范围提供适当的健康建议。


* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**所需组件**

本项目需要以下组件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 组件
        - 购买链接
    *   - :ref:`cpn_thermistor`
        - |link_thermistor_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy| (10kΩ)
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**接线图**

按以下方式将组件连接到 Fusion HAT+：

.. image:: img/fzz/health_assistant_bb.png
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
      sudo python3 llm_openai_health.py

#. 查看结果

   程序启动后，会提示你说话。然后它会估算你的体温并提供健康建议。

   典型的控制台输出：

   .. code-block:: text

      Hello, I am a health assistant. Please hold your thermometer and I will assess your
      body temperature based on the thermistor reading. If you feel unwell, please provide
      your symptoms and I will provide appropriate health advice.

      Say something
      partial: I feel
      partial: I feel very
      partial: I feel very warm
      final: I feel very warm and tired

      Your body temperature is 38.7°C, which indicates a mild fever. Please rest, stay
      hydrated, and monitor your symptoms. If the fever persists or worsens, consider
      seeking medical attention.

#. 示例场景

   * 正常体温（36.5°C）：

     .. code-block:: text

        User: "How's my temperature?"
        AI: "Your body temperature is 36.5°C, which is within the normal range. You're
        doing well, but continue to monitor how you feel."

   * 高烧（39.2°C）：

     .. code-block:: text

        User: "I have a headache and feel hot"
        AI: "Your body temperature is 39.2°C, indicating a high fever. Please rest
        immediately, stay hydrated, and consider seeking medical advice as soon as possible."

   * 低温（34.2°C）：

     .. code-block:: text

        User: "I feel cold and shivering"
        AI: "Your body temperature is 34.2°C, which is below normal and may indicate
        hypothermia. Please warm up immediately with blankets and warm drinks."


**代码**

以下是 AI 健康助手的完整 Python 脚本：

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   import time
   from fusion_hat.stt import STT
   from fusion_hat.adc import ADC
   import math
   from fusion_hat.tts import Pico2Wave

   # Setup Text-to-Speech and Speech-to-Text
   tts = Pico2Wave()
   tts.set_lang('en-US')
   stt = STT(language="en-us")

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup ADC for thermistor reading on channel A3
   thermistor = ADC('A3')

   # Setup LLM with health assessment instructions
   INSTRUCTIONS = '''
   You are a health assistant. Your task is to assess the user's body temperature based on the thermistor reading and provide appropriate health advice.

   The thermistor reading represents body temperature in Celsius.

   ### Input Format:
   "thermistor: [value], message: [user query]"

   ### Output Guidelines:
   1. If temperature < 35.0°C, warn about hypothermia and suggest warming up.
   2. If 35.0°C ≤ temperature ≤ 37.5°C, confirm normal temperature and reassure the user.
   3. If 37.5°C < temperature ≤ 38.5°C, indicate mild fever and suggest rest and hydration.
   4. If temperature > 38.5°C, alert about high fever and recommend medical attention.
   5. Include the temperature value in your response to justify your assessment.
   6. Your reply should be brief and concise, no more than two sentences.

   ### Example Input:
   thermistor: 39.0, message: I feel unwell.

   ### Example Output:
   Your body temperature is 39.0°C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
   '''

   WELCOME = "Hello, I am a health assistant. Please hold your thermometer and I will assess your body temperature based on the thermistor reading. If you feel unwell, please provide your symptoms and I will provide appropriate health advice."

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

   # Function to read and convert thermistor value to temperature
   def temperature():
       while True:
           # Read analog value (0-4095)
           analogVal = thermistor.read()

           # Calculate voltage across thermistor
           Vr = 3.3 * float(analogVal) / 4095

           # Check for sensor issues
           if 3.3 - Vr < 0.1:
               print("Please check the sensor")
               continue

           # Calculate thermistor resistance
           Rt = 10000 * Vr / (3.3 - Vr)

           # Convert resistance to temperature using Steinhart-Hart equation
           # B = 3950 (thermistor coefficient), R0 = 10000Ω at 25°C
           temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))

           # Convert from Kelvin to Celsius
           Cel = temp - 273.15

           return Cel

   # Main loop for voice interaction
   while True:
       print("Say something")

       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")

               # Measure temperature and combine with user query
               current_temp = temperature()
               input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

               # Get response from LLM with streaming
               response = llm.prompt(input_text, stream=True)

               # Collect the full response
               string = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       string += next_word

               # Speak the response
               tts.say(string)
               print("")  # New line after response

           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**理解代码**

1. 温度传感器初始化

   热敏电阻连接到 ADC 通道 A3：

   .. code-block:: python

      thermistor = ADC('A3')

   这读取 0-4095 的模拟值，代表电压水平。

2. Steinhart-Hart 温度转换

   热敏电阻使用 Steinhart-Hart 方程进行精确的温度计算：

   .. code-block:: python

      # Read analog value (0-4095)
      analogVal = thermistor.read()

      # Convert to voltage (0-3.3V)
      Vr = 3.3 * float(analogVal) / 4095

      # Calculate thermistor resistance using voltage divider formula
      Rt = 10000 * Vr / (3.3 - Vr)

      # Steinhart-Hart equation: 1/T = 1/T0 + 1/B * ln(R/R0)
      temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))

      # Convert Kelvin to Celsius
      Cel = temp - 273.15

3. 传感器错误检查

   代码包含基本的错误检测：

   .. code-block:: python

      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue

   这检测热敏电阻是否断开或短路。

4. 语音识别设置

   STT 和 TTS 都配置为英语：

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. 上下文输入构建

   温度数据与用户查询结合：

   .. code-block:: python

      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

   格式：\ ``"thermistor: 37.2, message: I feel dizzy"``

6. 医疗分类逻辑

   AI 指令定义了温度范围：

   .. code-block:: python

      # Temperature ranges for medical assessment:
      # < 35.0°C: Hypothermia warning
      # 35.0-37.5°C: Normal range
      # 37.5-38.5°C: Mild fever
      # > 38.5°C: High fever

7. 实时语音处理

   系统显示部分识别结果：

   .. code-block:: python

      for result in stt.listen(stream=True):
          if result["done"]:
              # Final recognition
              print(f"final: {result['final']}")
          else:
              # Partial recognition
              print(f"partial: {result['partial']}", end="", flush=True)

8. 流式 AI 回复

   AI 回复被流式接收并同时朗读：

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word

      tts.say(string)  # Speak complete response

9. 温度格式化

   温度保留一位小数：

   .. code-block:: python

      f"thermistor: {current_temp:.1f}"

   这确保了一致的精度（例如，36.5°C 而不是 36.512345°C）。

10. 清晰的终端显示

    使用 ANSI 转义码实现干净的输出：

    .. code-block:: python

        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

    - ``\r``：回到行首
    - ``\x1b[K``：清除到行尾
    - 防止流式输出时文字重叠

----------------------------------------------

**故障排除**

- 温度读数不准确

  - 检查热敏电阻接线：正确的分压器配置
  - 验证电阻值：应与热敏电阻的标称电阻匹配
  - 使用已知温度源进行校准
  - 检查 ADC 参考电压（应为稳定的 3.3V）

- 语音识别无响应

  - 测试麦克风：\ ``arecord --duration=3 test.wav && aplay test.wav``
  - 检查 STT 初始化中的音频设备选择
  - 确保背景噪音最小
  - 清晰并以适中的语速说话

- AI 无响应

  - 检查网络连接
  - 验证 ``secret.py``\ 中的 OpenAI API 密钥
  - 确保 OpenAI 账户已启用计费
  - 检查是否超过 API 速率限制

- 温度读数跳动异常

  - 添加软件滤波：读取值的移动平均
  - 检查是否有松动连接
  - 在热敏电阻两端并联电容（0.1µF）以减少噪声
  - 确保热敏电阻良好接触热源

- 文字转语音不工作

  - 测试音频输出：\ ``speaker-test -t sine -f 440``
  - 验证语言设置：\ ``tts.set_lang('en-US')``
  - 检查音量：\ ``alsamixer``
  - 重新运行音频设置脚本：\ ``sudo /opt/setup_fusion_hat_audio.sh``

- 传感器读数为 0 或 4095

  - 检查接线：热敏电阻可能短路（0）或开路（4095）
  - 验证分压器计算
  - 使用已知电压源测试 ADC
  - 检查 ADC 通道（应为 A3）

**安全与医疗免责声明**

.. warning::

   本项目仅用于教育和演示目的。
   它\ **不是**\ 医疗设备，\ **不得**\ 用于真实的医疗诊断或治疗。

#. 安全指南

   * 非医疗用途：请勿依赖本系统做出任何健康或治疗决定。
   * 紧急情况：对于严重症状，请务必寻求专业医疗帮助。
   * 精度限制：与医用温度计相比，热敏电阻的精度有限。
   * 需要校准：定期使用医用温度计进行校准至关重要。
   * 需要监督：用于教育目的时，建议有成人监督。

#. 何时寻求医疗帮助

   如果出现以下任何情况，请寻求专业医疗帮助：

   * 成人体温 > 39.5°C（103.1°F）
   * 3 个月以下婴儿体温 > 38.0°C（100.4°F）
   * 发烧持续超过 3 天
   * 呼吸困难或胸痛
   * 剧烈头痛或脖子僵硬
   * 意识模糊或惊厥



----------------------------------------------

这个 AI 健康助手展示了传感器技术、语音交互和人工智能如何协同工作，创建便捷的健康监测工具，同时强调了在严重健康问题中咨询专业医务人员的重要性！
