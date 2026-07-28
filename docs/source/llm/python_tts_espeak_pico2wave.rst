.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. 使用 Espeak 和 Pico2Wave 实现 TTS
=============================================

在本课中，我们将使用树莓派上两个内置的文字转语音（TTS）引擎——\ **Espeak**\ 和\ **Pico2Wave**\ ——让 Fusion HAT+ 开口说话。

这两个引擎都很简单，可以离线运行，但音质差别很大：

* **Espeak**：非常轻量且快速，但声音带有机器感。你可以调整速度、音调和音量。
* **Pico2Wave**：比 Espeak 产生更平滑、更自然的声音，但可配置的选项较少。

你将听到它们在\ **音质**\ 和\ **功能**\ 上的区别。

----

1. 测试 Espeak
--------------------

Espeak 是树莓派操作系统自带的一个轻量级 TTS 引擎。
它的声音听起来带有机器感，但可配置性很高：你可以调整音量、音调、速度等。

**运行程序**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * 你应该会听到 Fusion HAT+ 说："Hello! I'm Espeak TTS."
  * 尝试修改代码中的调参，体验 ``amp``、``speed``、``gap`` 和 ``pitch`` 对声音的影响。

**代码**

.. code-block:: python

  from fusion_hat.tts import Espeak

  # Create Espeak TTS instance
  tts = Espeak()
  # Set amplitude 0-200, default 100
  tts.set_amp(200)
  # Set speed 80-260, default 150
  tts.set_speed(150)
  # Set gap 0-200, default 1
  tts.set_gap(1)
  # Set pitch 0-99, default 80
  tts.set_pitch(80)

  tts.say("Hello! I'm Espeak TTS.")

**代码说明：**

* ``tts.set_amp()`` — 控制音量（0–200）。
* ``tts.set_speed()`` — 调整说话速度（80–260）。
* ``tts.set_gap()`` — 设置单词间隔（0–200）。
* ``tts.set_pitch()`` — 设置音调（0–99）。
* ``tts.say()`` — 将文字转换为语音并播放。

💡 **提示：** 尝试提高音调和速度让声音听起来更欢快，或降低它们让声音更严肃。

----


2. 测试 Pico2Wave
---------------------

Pico2Wave 能够产生比 Espeak **更自然、更像人声**\ 的语音。
它使用非常简单，但灵活性较低——你只能\ **更改语言**\ ，不能调整音调、速度或音量。
这使得 Pico2Wave 在需要清晰流畅的语音而不需要太多配置时，是一个很好的选择。

**运行程序**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* 你应该会听到 Fusion HAT+ 说："Hello! I'm Pico2Wave TTS."
* 尝试更改语言（例如，西班牙语用 ``es-ES``），听听声音的变化。

**代码**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**代码说明：**

* ``tts.set_lang()`` — 设置语音合成的输出语言。

  - ``en-US``（默认）
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` — 将文字转换为语音并立即播放。


----

故障排除
-------------------

* **运行 Espeak 或 Pico2Wave 时没有声音**

  * 检查你的扬声器/耳机是否已连接，音量是否未静音。
  * 在终端中快速测试：

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  如果听不到任何声音，问题出在音频输出上，而非你的 Python 代码。

* **Espeak 声音太快或太机械**

  * 尝试调整代码中的参数：

    .. code-block:: python

       tts.set_speed(120)   # slower
       tts.set_pitch(60)    # different pitch

* **运行代码时提示权限被拒绝**

  * 尝试使用 ``sudo`` 运行：

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

Espeak 与 Pico2Wave 对比
-------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - 特性
     - Espeak
     - Pico2Wave
   * - 语音质量
     - 机械、合成音
     - 更自然，更像人声
   * - 语言支持
     - 默认为英语
     - 较少，但覆盖常用语言
   * - 可调节性
     - 是（速度、音调等）
     - 否（仅语言）
   * - 性能
     - 非常快，轻量
     - 稍慢，较重
