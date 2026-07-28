.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. AI 语音助手
=================

本课程将你的 Fusion HAT+ 转变为一个\ **以语音为先的 AI 助手**。
借助提供的代码，机器人将：\ **等待唤醒词**\ ，使用 Vosk **转录你的语音**\ ，将其发送给\ **OpenAI LLM**\ ，然后使用 Piper TTS **语音回复**。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Voice_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----

开始之前
------------

确保你已完成以下准备：

* :ref:`test_piper` — Piper 语音正常工作（例如，可以播放 "Hello"）。
* :ref:`test_vosk` — Vosk STT 适用于你的语言（例如，\ ``en-us``）。
* :ref:`py_online_llm` — 你的 **OpenAI API 密钥**\ 已保存在 ``secret.py``\ 中，变量名为 ``OPENAI_API_KEY``。
* 在 Fusion HAT+ 上有一个正常工作的\ **麦克风**\ 和\ **扬声器**。
* 稳定的网络连接（LLM 在线）。

----

运行示例
-----------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**代码使用的配置：**

* LLM：**OpenAI**（\ ``gpt-4o-mini``）
* TTS：**Piper**（\ ``en_US-ryan-low``）
* STT：**Vosk**（\ ``en-us``）
* 唤醒词：\ ``"hey buddy"``
* 键盘输入：**已启用**（可选的手动输入）
* 图像模式：**已启用**（\ ``WITH_IMAGE=True``）——如果你以后决定使用图像，需要多模态能力的 LLM

**运行过程：**

1. 助手显示带有唤醒短语的欢迎消息。
2. 它监听\ **"hey buddy"**。
3. 唤醒后，你的语音被转录为文字（Vosk → text）。
4. 文字被发送到 **OpenAI（gpt-4o-mini）**\ 以获取回复。
5. 回复通过 **Piper**（\ ``en_US-ryan-low``）\ 朗读出来。

**交互示例**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What's the capital of Italy?
   Robot: The capital of Italy is Rome.

代码
---------

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

**代码说明：**

* ``OpenAI(..., model="gpt-4o-mini")`` — 在本课程中使用 **OpenAI** 作为唯一的 LLM。
* ``NAME`` / ``WAKE_WORD`` — 个性化设置助手（"Buddy"，"hey buddy"）。
* ``WITH_IMAGE=True`` — 在助手中启用图像模式（此处未包含图像 I/O 逻辑）。
* ``TTS_MODEL="en_US-ryan-low"`` — 用于回复的 Piper 语音模型。
* ``STT_LANGUAGE="en-us"`` — Vosk 的识别语言。
* ``KEYBOARD_ENABLE=True`` — 允许在调试期间进行可选的键盘文字输入。
* ``WELCOME`` / ``INSTRUCTIONS`` — 启动消息和助手的角色/系统提示词。
* ``va.run()`` — 启动循环：\ **唤醒 → 监听 → LLM → 说话**。


切换到其他 LLM 或 TTS
------------------------------

你可以通过少量修改，轻松切换到其他 LLM、TTS 或 STT 语言：

* 支持的 LLM：

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — 查看 **Piper TTS** 支持的语言。
* :ref:`test_vosk` — 查看 **Vosk STT** 支持的语言。

要切换，只需修改代码中的初始化部分：

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key="YOUR_KEY", model="gemini-pro")

   # Set models and languages
   TTS_MODEL = "en_US-ryan-low"
   STT_LANGUAGE = "en-us"



----

故障排除
-----------------------------

* **机器人对唤醒词没有响应**

  - 检查麦克风是否正常工作。
  - 确保 ``WAKE_ENABLE = True``。
  - 调整唤醒词以匹配你的发音。
  - 减少背景噪音并清晰说话。

* **扬声器没有声音**

  - 检查 TTS 模型名称（例如，\ ``en_US-ryan-low``）。
  - 手动测试 Piper 或 Espeak。
  - 检查扬声器连接和音量。

* **API 密钥错误或超时**

  - 检查 ``secret.py``\ 中的密钥。
  - 确保网络连接稳定。
  - 确认 LLM 模型受支持（例如，\ ``gpt-4o-mini``）。

* **唤醒词生效但没有回复**

  - 检查 STT 语言是否与你的口音匹配。
  - 确保模型已正确下载。
  - 尝试打印调试日志以确认 STT 正在运行。

* **TTS 正常工作但没有 LLM 回复**

  - 检查 API 密钥是否有效。
  - 验证模型名称和 LLM 设置。
  - 确保网络连接正常。
