.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. 使用 Piper 和 OpenAI 实现 TTS
==================================

在上一课中，我们探索了\ **Espeak**\ 和\ **Pico2Wave**\ ——两个在树莓派上运行简单的离线 TTS 引擎。
现在，让我们向前迈进一大步，尝试两种\ **更高级的 TTS 选项**\ ，它们提供\ **更高的语音质量**\ 和更大的灵活性：

* **Piper** —— 一个基于神经网络的快速 TTS 引擎，可在树莓派上\ **完全离线**\ 运行。
* **OpenAI TTS** —— 一种在线服务，提供\ **非常自然、像人声的语音**\ ，非常适合表达性强的语音。

这些引擎将使你的 Fusion HAT+ 听起来更真实、更逼真。

----

.. _test_piper:

1. 测试 Piper
------------------

Piper 是一个\ **离线神经 TTS 引擎**\ ，这意味着一旦模型安装完成，你就不需要网络连接。
它支持多种\ **语言**\ 和\ **声音**\ ，使其成为嵌入式语音应用的强大选择。

**运行程序**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* 首次运行时，所选\ **语音模型**\ 会自动下载。
* 然后你应该会听到 Fusion HAT+ 说：\ ``Hello! I'm Piper TTS.``
* 你可以通过调用 ``set_model()``\ 并传入不同的模型名称来切换声音或语言。

**代码**

.. code-block:: python

  from fusion_hat.tts import Piper

  tts = Piper()

  # List supported languages
  print(tts.available_countrys())

  # List models for English (en_us)
  print(tts.available_models('en_us'))

  # Set a voice model (auto-download if not already present)
  tts.set_model("en_US-amy-low")

  # Say something
  tts.say("Hello! I'm Piper TTS.")

**代码说明：**

* ``available_countrys()`` — 列出所有支持的语言。
* ``available_models()`` — 列出特定语言的可用模型。
* ``set_model()`` — 设置语音模型。如果模型尚未安装，会自动下载。
* ``say()`` — 将文字转换为语音并立即播放。

💡 **提示：** 尝试不同的模型，比较速度、清晰度和口音。有些模型更轻量（更快），而其他模型保真度更高。

----

2. 测试 OpenAI TTS
-------------------------------

**获取并保存你的 API 密钥**

#. 前往 |link_openai_platform| 并登录。在 **API keys** 页面，点击 **Create new secret key**。

   .. image:: img/llm_openai_create.png

#. 填写详细信息（所有者、名称、项目及权限，如有需要），然后点击 **Create secret key**。

   .. image:: img/llm_openai_create_confirm.png

#. 密钥创建后，立即复制——你将无法再次看到它。如果丢失，必须生成一个新的。

   .. image:: img/llm_openai_copy.png

#. 在你的项目文件夹中（例如：\ ``/``），创建一个名为 ``secret.py``\ 的文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 将你的密钥粘贴到文件中，如下所示：

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**运行程序**

.. code-block:: bash

  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* 程序将连接到 OpenAI 的 TTS 服务，Fusion HAT+ 将使用\ **自然、富有表现力的语音输出**\ 来讲话。
* 你可以更改\ **语音风格**\ 并添加\ **指令**\ 来控制语气和表达方式（例如，悲伤、戏剧化、俏皮）。
* 这使得 OpenAI TTS 非常适合交互式机器人、讲故事或教育助手。


**代码**

.. code-block:: python

  from fusion_hat.tts import OpenAI_TTS
  from secret import OPENAI_API_KEY

  # Export your OpenAI_API_KEY before running the script
  # export OPENAI_API_KEY="sk-proj-xxxxxx"

  tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
  # tts.set_model('tts-1')
  tts.set_voice('alloy')
  tts.set_model('gpt-4o-mini-tts')

  msg = "Hello! I'm OpenAI TTS."
  print(f"Say: {msg}")
  tts.say(msg)

  msg = "with instructions, I can say word sadly"
  instructions = "say it sadly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)

  msg = "or say something dramaticly."
  instructions = "say it dramaticly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)


**代码说明：**

* ``OpenAI_TTS()`` — 使用你的 API 密钥初始化 OpenAI TTS 引擎。
* ``set_model()`` — 选择 TTS 模型（例如，\ ``gpt-4o-mini-tts``）。
* ``set_voice()`` — 选择特定的语音（例如，\ ``alloy``）。
* ``say(text)`` — 将文字转换为语音并播放。
* ``say(text, instructions=...)`` — 添加\ **表达性语气指令**\ ，让你可以动态控制语音风格。

**示例：**

- "say it sadly" → 柔和、带有情感的语调
- "say it dramatically" → 大胆且富有表现力的表达
- "say it excitedly" → 热情的语调

----

故障排除
-------------------

* **没有名为 'secret' 的模块**

  这意味着 ``secret.py``\ 不在你的 Python 文件所在的文件夹中。
  将 ``secret.py``\ 移动到运行脚本的同一目录，例如：

  .. code-block:: bash

     ls ~/
     # Make sure you see both: secret.py and your .py file

* **OpenAI：无效的 API 密钥 / 401**

  * 检查是否粘贴了完整的密钥（以 ``sk-``\ 开头），且没有多余的空格/换行。
  * 确保你的代码正确导入了它：

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * 确认树莓派上的网络访问正常（尝试 ``ping api.openai.com``）。

* **OpenAI：配额超限 / 计费错误**

  * 你可能需要在 OpenAI 控制面板中添加计费信息或增加配额。
  * 解决账户/计费问题后重试。

* **Piper: tts.say() 运行时没有声音**

  * 确保语音模型确实存在：

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * 确认代码中的模型名称完全匹配：

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * 检查树莓派的音频输出设备/音量（\ ``alsamixer``），确保扬声器已连接并通电。

* **ALSA / 声音设备错误（例如，"Audio device busy" 或 "No such file or directory"）**

  * 关闭其他正在使用音频的程序。
  * 如果设备持续繁忙，重新启动树莓派。
  * 对于 HDMI 与耳机插孔输出，在树莓派操作系统音频设置中选择正确的设备。

* **运行 Python 时提示权限被拒绝**

  * 如果你的环境需要，可以尝试使用 ``sudo``：

    .. code-block:: bash

       sudo python3 tts_piper.py

TTS 引擎对比
-----------------

.. list-table:: 功能对比：Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - 项目
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - 运行方式
     - 树莓派内置（离线）
     - 树莓派内置（离线）
     - 树莓派 / PC（离线，需要模型）
     - 云端（在线，需要 API 密钥）
   * - 语音质量
     - 机械音
     - 比 Espeak 更自然
     - 自然（神经 TTS）
     - 非常自然 / 像人声
   * - 控制选项
     - 速度、音调、音量
     - 有限的控制
     - 选择不同的语音/模型
     - 选择模型和语音
   * - 语言支持
     - 多种（质量各异）
     - 有限集合
     - 多种语音/语言可用
     - 英语最佳（其他语言视可用性而定）
   * - 延迟/速度
     - 非常快
     - 快
     - 在 Pi 4/5 上使用 "low" 模型可实时
     - 依赖网络（通常低延迟）
   * - 设置步骤
     - 最少
     - 最少
     - 下载 ``.onnx`` + ``.onnx.json`` 模型
     - 创建 API 密钥，安装客户端
   * - 最适合
     - 快速测试、基本提示
     - 稍微好一点的离线语音
     - 本地项目，音质更好
     - 最高质量，丰富的语音选项
