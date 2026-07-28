.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. 本地语音聊天机器人
=========================

在本课中，你将结合迄今为止学到的所有知识——\ **语音识别（STT）**、**文字转语音（TTS）**\ 和\ **本地 LLM（Ollama）**——构建一个完全离线的\ **语音聊天机器人**\ ，运行在你的 Fusion HAT+ 上。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Local_Voice_Chatbot.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

工作流程很简单：

#. **监听** — 麦克风捕捉你的语音，并使用 **Vosk** 转录为文字。
#. **思考** — 文字被发送到运行在 Ollama 上的本地 **LLM**（例如，\ ``llama3.2:3b``）。
#. **说话** — 聊天机器人使用 **Piper TTS** 语音回答。

这将创建一个\ **免提对话机器人**\ ，能够实时理解和回复。

----

开始之前
------------

确保你已准备好以下内容：

* 已测试 **Piper TTS**（:ref:`test_piper`）并选择了可用的语音模型。
* 已测试 **Vosk STT**（:ref:`test_vosk`）并选择了正确的语言包（例如，\ ``en-us``）。
* 在你的 Pi 或另一台电脑上安装了 **Ollama**（:ref:`download_ollama`），并下载了一个模型，如 ``llama3.2:3b``（如果内存有限，可选用 ``moondream:1.8b``\ 等更小的模型）。

----

运行代码
----------

#. 打开示例脚本：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano local_voice_chatbot.py

#. 根据需要更新参数：

   * ``stt = Vosk(language="en-us")``：更改此设置以匹配你的口音/语言包（例如，\ ``en-us``、``zh-cn``、``es``）。
   * ``tts.set_model("en_US-amy-low")``：替换为你在 :ref:`test_piper` 中验证过的 Piper 语音模型。
   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``：根据你的设置更新 ``ip``\ 和 ``model``。

     * ``ip``：如果 Ollama 运行在\ **同一台 Pi**\ 上，使用 ``localhost``。如果 Ollama 运行在局域网中的另一台电脑上，在 Ollama 中开启 **Expose to network**\ 并将 ``ip``\ 设置为该电脑的局域网 IP。
     * ``model``：必须与你下载/在 Ollama 中激活的模型名称完全匹配。

#. 运行脚本：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo python3 local_voice_chatbot.py

#. 运行后，你应该会看到：

   * 机器人用语音欢迎消息向你打招呼。
   * 它等待语音输入。
   * Vosk 将你的语音转录为文字。
   * 文字被发送到 Ollama，后者流式返回回复。
   * 回复被清理（移除隐藏的推理内容）并由 Piper 朗读出来。
   * 随时按 ``Ctrl+C``\ 停止程序。

----

代码
----

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

代码分析
---------

**导入和全局设置**

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

引入了你之前构建的三个子系统：
**Vosk** 用于语音转文字（STT），**Ollama** 用于 LLM，**Piper** 用于文字转语音（TTS）。



**初始化 STT（Vosk）**

.. code-block:: python

   stt = Vosk(language="en-us")

加载美式英语的 Vosk 模型。
更改语言代码（例如，\ ``zh-cn``、``es``）以匹配你的语音包，可获得更好的准确率。



**初始化 TTS（Piper）**

.. code-block:: python

   tts = Piper()
   tts.set_model("en_US-amy-low")

创建一个 Piper 引擎并选择特定的语音。
选择你在 :ref:`test_piper` 中测试过的模型。质量较低的语音速度更快，CPU 占用更少。



**LLM 指令和欢迎语**

.. code-block:: python

   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

两个关键的用户体验选择：

* 保持\ **答案简短直接**（有助于 TTS 清晰度）。
* 明确禁止隐藏的"思维链"标签，以减少噪音输出。



**连接 Ollama 并设置对话范围**

.. code-block:: python

   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

* ``ip="localhost"``\ 假设 Ollama 服务器运行在同一台 Pi 上。如果运行在另一台局域网机器上，填入该电脑的\ **局域网 IP**\ 并在 Ollama 中启用 *Expose to network*。
* ``set_max_messages(20)``\ 保持较短的对话历史记录。如果内存/延迟紧张，可以降低此值。

**在说话前剥离隐藏的推理/标签**

.. code-block:: python

   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

某些模型可能会输出内部风格的标签（例如，\ ``<think>…``）。
此函数移除这些内容，确保 TTS **只**\ 朗读最终答案。

**提示：** 如果你在屏幕上看到其他工件（因为你流式输出了原始 token），此函数已经确保\ **朗读的**\ 输出保持干净。

**主循环：问候一次，然后监听 → 思考 → 说话**

.. code-block:: python

   print(WELCOME)
   tts.say(WELCOME)

通过终端和扬声器向用户打招呼。启动时执行一次。

**监听（带实时部分结果的流式 STT）**

.. code-block:: python

   print("\n🎤 Listening... (Press Ctrl+C to stop)")

   text = ""
   for result in stt.listen(stream=True):
       if result["done"]:
           text = result["final"].strip()
           print(f"[YOU] {text}")
       else:
           print(f"[YOU] {result['partial']}", end="\r", flush=True)

* ``stream=True``\ 产生\ **部分**\ 转录以实现即时反馈，并在话语结束时产生\ **最终**\ 转录。
* 最终识别到的文字存储在 ``text``\ 中并打印一次。

**守卫：** 如果未识别到任何内容，跳过 LLM 调用：

.. code-block:: python

   if not text:
       print("[INFO] Nothing recognized. Try again.")
       time.sleep(0.1)
       continue

这可以避免向模型发送空提示（节省时间和 token）。

**思考（LLM）带流式打印**

.. code-block:: python

   reply_accum = ""
   response = llm.prompt(text, stream=True)
   for next_word in response:
       if next_word:
           print(next_word, end="", flush=True)
           reply_accum += next_word
   print("")

* 将最终转录发送给本地 LLM，并在 token 到达时\ **即时打印**\ 以实现低延迟。
* 同时，你将完整回复累积在 ``reply_accum``\ 中以供后续处理。

**注意：** 如果你\ **不想**\ 显示原始 token，可以设置 ``stream=False``\ 并只打印最终字符串。

**说话（先清理，然后一次 TTS）**

.. code-block:: python

   clean = strip_thinking(reply_accum)
   if clean:
       tts.say(clean)
   else:
       tts.say("Sorry, I didn't catch that.")

* 清理最终文本以移除隐藏标签，然后\ **只朗读一次**。
* 保持 TTS 只执行一次，避免重复提示如 "[LLM] / [SAY]"。

**退出和清理**

.. code-block:: python

   except KeyboardInterrupt:
       print("\n[INFO] Stopping...")
   finally:
       tts.say("Goodbye!")
       print("Bye.")

使用 **Ctrl+C**\ 停止。机器人说一声简短的再见以表示安全退出。


----

故障排除与常见问题
---------------------

* **模型太大（内存错误）**

  使用较小的模型，如 ``moondream:1.8b``\ 或在性能更强的电脑上运行 Ollama。

* **Ollama 没有响应**

  确保 Ollama 正在运行（\ ``ollama serve``\ 或桌面应用已打开）。如果使用远程，启用 **Expose to network**\ 并检查 IP 地址。

* **Vosk 无法识别语音**

  验证你的麦克风是否正常工作。如有需要，尝试其他语言包（\ ``zh-cn``、``es``\ 等）。

* **Piper 静音或出错**

  确认所选语音模型已下载并在 :ref:`test_piper` 中测试过。

* **答案太长或偏离主题**

  编辑 ``INSTRUCTIONS``，添加：\ **"Keep answers short and to the point."**
