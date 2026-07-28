.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. 使用 Ollama 实现文本与视觉对话
===================================

在本课中，你将学习如何使用 **Ollama**——一个在本地运行大语言和视觉模型的工具。
我们将向你展示如何安装 Ollama、下载模型，并将 Fusion HAT+ 连接到它。

有了这个设置，Fusion HAT+ 可以拍摄相机快照，模型将\ **看到并描述**——
你可以询问任何关于图像的问题，模型会以自然语言回答。

.. _download_ollama:

1. 安装 Ollama（LLM）并下载模型
---------------------------------------

你可以选择在哪里安装 **Ollama**：

* 在你的树莓派上（本地运行）
* 或在**同一局域网**内的另一台电脑上（Mac/Windows/Linux）

**推荐模型 vs 硬件**

你可以选择 |link_ollama_hub| 上的任何可用模型。
模型有不同的参数规模（3B、7B、13B、70B...）。
较小的模型运行更快，所需内存更少，而较大的模型提供更好的质量但需要更强大的硬件。

查看下表，选择适合你设备的模型大小。

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - 模型大小
     - 最低内存要求
     - 推荐硬件
   * - ~3B 参数
     - 8GB（建议 16GB）
     - 树莓派 5（16GB）或中端 PC/Mac
   * - ~7B 参数
     - 16GB+
     - Pi 5（16GB，勉强可用）或中端 PC/Mac
   * - ~13B 参数
     - 32GB+
     - 高内存台式 PC / Mac
   * - 30B+ 参数
     - 64GB+
     - 工作站 / 服务器 / 建议使用 GPU
   * - 70B+ 参数
     - 128GB+
     - 配备多 GPU 的高端服务器

**在树莓派上安装**

如果你想直接在树莓派上运行 Ollama：

* 使用 **64 位树莓派操作系统**
* 强烈建议：**树莓派 5（16GB RAM）**

运行以下命令：

.. code-block:: bash

   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull a lightweight model (good for testing)
   ollama pull llama3.2:3b

   # Quick run test (type 'hi' and press Enter)
   ollama run llama3.2:3b

   # Serve the API (default port 11434)
   # Tip: set OLLAMA_HOST=0.0.0.0 to allow access from LAN
   OLLAMA_HOST=0.0.0.0 ollama serve

**在 Mac / Windows / Linux 上安装（桌面应用）**

1. 从 |link_ollama| 下载并安装 Ollama

   .. image:: img/llm_ollama_download.png

2. 打开 Ollama 应用，进入 **Model Selector**，使用搜索栏查找模型。例如，输入 ``llama3.2:3b``\ （一个适合入门的小型轻量模型）。

   .. image:: img/llm_ollama_choose.png

3. 下载完成后，在聊天窗口中输入简单的 "Hi" 之类的内容，Ollama 会在你首次使用时自动下载。

   .. image:: img/llm_olama_llama_download.png

4. 进入 **Settings** → 开启 **Expose Ollama to the network**。这允许你的树莓派通过局域网连接到它。

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   如果你看到类似这样的错误：

   ``Error: model requires more system memory ...``

   说明模型对你的机器来说太大。
   使用一个\ **更小的模型**\ 或切换到内存更大的电脑。

2. 测试 Ollama
--------------

一旦 Ollama 安装完成且模型就绪，你可以通过一个简单的聊天循环快速测试。

**设置 IP 地址**

#. 打开示例脚本：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. 根据需要更新参数：

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``：根据你的设置更新 ``ip``\ 和 ``model``。

     * ``ip``：如果 Ollama 运行在\ **同一台 Pi**\ 上，使用 ``localhost``。如果 Ollama 运行在局域网中的另一台电脑上，在 Ollama 中开启 **Expose to network**\ 并将 ``ip``\ 设置为该电脑的局域网 IP。
     * ``model``：必须与你下载/在 Ollama 中激活的模型名称完全匹配。


**运行程序**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 llm_ollama.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

   * 你可以选择 |link_ollama_hub| 上的\ **任何模型**\ ，但如果你只有 8–16GB 内存，建议使用较小的模型（如 ``moondream:1.8b``\ 或 ``phi3:mini``）。
   * 确保你在代码中指定的模型与你已在 Ollama 中下载的模型匹配。
   * 输入 ``exit``\ 或 ``quit``\ 停止程序。
   * 如果无法连接，确保 Ollama 正在运行，并且如果你使用远程主机，两台设备在同一个局域网内。

**代码**

.. code-block:: python

   from fusion_hat.llm import Ollama

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   # Change this to your computer IP, if you run it on your pi, then change it to localhost
   llm = Ollama(
      ip="localhost",
      model="llama3.2:3b"
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Response without stream
      # response = llm.prompt(input_text)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


3. 使用 Ollama 进行视觉对话
---------------------------

在这个演示中，Pi 摄像头会在你\ **每次输入问题时**\ 拍摄一张快照。
程序将\ **你的输入文字 + 新照片**\ 通过 Ollama 发送给本地视觉模型，
然后以纯文本流式输出模型的回复。
这是一个最简的"看见并描述"基础示例，你可以之后扩展加入颜色/人脸/二维码检测。

**开始之前**

#. 打开 **Ollama** 应用（或运行服务），确保已拉取一个\ **支持视觉的模型**。

   * 如果你有足够内存（≥16GB RAM），可以尝试 ``llava:7b``。
   * 如果你只有 **8GB RAM**，建议使用较小的模型，如 ``moondream:1.8b``\ 或 ``granite3.2-vision:2b``。

   .. image:: img/llm_ollama_image_model.png

**运行演示**

#. 进入示例文件夹并运行脚本：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. 运行时的过程：

   * 程序打印一行欢迎信息，然后等待你的输入（\ ``>>>``）。
   * **每次你输入任何内容**\ （例如，"hello"、"Is there yellow?"、"Any faces?"、"What is on the desk?"），它会：

     * **拍摄一张照片**\ （保存到 ``/tmp/llm-img.jpg``），
     * **将你的文字 + 照片**\ 通过 Ollama 发送给视觉模型，
     * **流式返回**\ 模型的答案到终端。

   * 输入 ``exit``\ 或 ``quit``\ 结束程序。

**代码**

.. code-block:: python

   from fusion_hat.llm import Ollama
   from picamera2 import Picamera2
   import time

   '''
   You need to setup ollama first, see llm_local.py

   You need at leaset 8GB RAM to run llava:7b large multimodal model
   '''

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   llm = Ollama(
      ip="localhost",          # e.g., "192.168.100.145" if remote
      model="llava:7b"         # change to "moondream:1.8b" or "granite3.2-vision:2b" for 8GB RAM
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   # Init camera
   camera = Picamera2()
   config = camera.create_still_configuration(
      main={"size": (1280, 720)},
   )
   camera.configure(config)
   camera.start()
   time.sleep(2)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Capture image
      img_path = '/tmp/llm-img.jpg'
      camera.capture_file(img_path)

      # Response without stream
      # response = llm.prompt(input_text, image_path=img_path)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True, image_path=img_path)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


故障排除
--------


* **出现错误：`model requires more system memory ...`。**

  * 这意味着模型对你的设备来说太大。
  * 使用较小的模型，如 ``moondream:1.8b``\ 或 ``granite3.2-vision:2b``。
  * 或者切换到内存更大的机器，并将 Ollama 暴露到网络。

* **代码无法连接到 Ollama（连接被拒绝）。**

  请检查以下内容：

  * 确保 Ollama 正在运行（\ ``ollama serve``\ 或桌面应用已打开）。
  * 如果使用远程电脑，在 Ollama 设置中开启 **Expose to network**。
  * 再次检查代码中的 ``ip="..."``\ 是否正确的局域网 IP。
  * 确认两台设备在同一个局域网内。

* **我的 Pi 摄像头无法拍照。**

  * 验证 ``Picamera2``\ 是否已安装并能通过简单的测试脚本正常工作。
  * 检查摄像头排线是否正确连接并在 ``raspi-config``\ 中启用。
  * 确保你的脚本有权限写入目标路径（\ ``/tmp/llm-img.jpg``）。

* **输出太慢。**

  * 较小的模型回复更快，但答案更简单。
  * 你可以降低摄像头分辨率（例如 640×480 而非 1280×720）以加快图像处理速度。
  * 关闭树莓派上的其他程序以释放 CPU 和内存。
