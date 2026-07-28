.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _py_stt_whisper:
.. _test_vosk:

3. 使用 Vosk 实现 STT（离线）
=================================

Vosk 是一个轻量级的语音转文字（STT）引擎，支持多种语言，可在树莓派上\ **完全离线**\ 运行。
你只需要联网一次来下载语言模型。之后，一切都可以在无网络连接的情况下工作。

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

在本课中，我们将：

* 检查树莓派上的麦克风。
* 安装并测试 Vosk，使用所选择的语言模型。


.. start_mic


运行程序
----------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

首次使用新语言运行此代码时，Vosk 将：

* **自动下载语言模型**（默认是小版本）。
* **打印出支持的语言列表**。
* 开始通过麦克风\ **监听**\ 音频输入。

你会在终端中看到类似这样的信息：

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

这意味着：

   * 模型文件（\ ``vosk-model-small-en-us-0.15``）已下载。
   * 支持的语言列表已打印。
   * 系统现在正在监听——对着 Fusion HAT+ 麦克风说话，识别的文字将出现在终端中。

**提示：**

* 保持麦克风距离约 **15–30 厘米**\ 以获得更好的准确率。
* 选择一种\ **与你的语言和口音匹配的模型**。
* 在安静的环境中使用，以提高识别效果。

代码
-----------

.. code-block:: python

   from fusion_hat.stt import Vosk as STT

   stt = STT(language="en-us")

   while True:
      print("Say something")
      for result in stt.listen(stream=True):
         if result["done"]:
               print(f"final:   {result['final']}")
         else:
               print(f"partial: {result['partial']}", end="\r", flush=True)


**代码说明：**

* ``stt.listen(stream=True)`` — 启动流式语音识别，并在你说话时返回中间结果。
* ``result["partial"]`` — 显示\ **实时识别的文字**（持续更新）。
* ``result["final"]`` — 在你停止说话时显示\ **最终识别的句子**。
* 循环持续运行，实现\ **免提实时转录**。

提示：这种流式模式非常适合\ **语音助手**、**命令控制**\ 或\ **实时转录**。

故障排除
-----------------

* **运行 `arecord` 时提示 "No such file or directory"**

  你可能使用了错误的声卡/设备编号。
  运行：

  .. code-block:: bash

     arecord -l

  并将 ``1,0``\ 替换为你的 USB 麦克风所显示的编号。


* **Vosk 无法识别语音**

  * 确保\ **语言代码**\ 与你的模型匹配（例如，英语用 ``en-us``，中文用 ``zh-cn``）。
  * 保持麦克风距离 15–30 厘米，避免背景噪音。
  * 清晰且缓慢地说话。

* **高延迟 / 识别缓慢**

  * 默认自动下载的是\ **小模型**（更快，但准确率较低）。
  * 如果仍然缓慢，关闭其他程序以释放 CPU。

.. end_mic
