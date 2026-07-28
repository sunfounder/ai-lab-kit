.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_book_cover_analyzer:

(示例) 图书专家
===============

**简介**

在本项目中，您将构建一个\ **AI 驱动的图书封面分析器**\ ，它利用计算机视觉和自然语言处理技术，通过图书封面识别书籍。系统使用 Raspberry Pi 摄像头拍摄图书封面图像，将其发送给大语言模型（LLM）（此处使用 OpenAI 的 GPT-4o 视觉模型）进行分析，并通过 TTS（文字转语音）技术播报书籍的标题、作者、摘要和评价等音频反馈。

该项目结合了多种技术：

- 使用 Picamera2 进行摄像头拍摄
- 利用 GPT-4o 视觉能力进行图像分析
- 使用 TTS（文字转语音）转换实现音频响应
- 使用 RGB LED 提供视觉状态反馈
- 使用物理按钮实现直观交互

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Book_Expert.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

如需使用其他大语言模型，请参考 :ref:`py_online_llm`。

----------------------------------------------

**所需元件**

本项目需要以下组件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 元件
        - 购买链接
    *   - Raspberry Pi 摄像头模组
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - 书籍（用于测试）
        - \-

----------------------------------------------

**接线图**

#. 为了方便使用摄像头模组，建议参考 :ref:`assemble_fusion_hat_pan_tilt`。

   .. note::

     组装云台可能会遮挡一些引脚，因此建议仅在需要使用摄像头时组装，或在组装后将云台放置在外侧。


   .. image:: ../quick_start/img/gimbal_assemble.png

#. 按如下方式将组件连接到 Fusion HAT+：

   .. image:: img/fzz/llm_book_bb.png
      :width: 80%
      :align: center

#. 用户按钮（User Button）已集成在 Fusion HAT+ 上，无需额外接线。它位于 BATTERY 端口附近。*

   .. image:: img/3.1_user_button.png
      :width: 50%

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

**运行示例**

#. 访问 Raspberry Pi 桌面：

   * :ref:`remote_desktop`: 使用 **VNC** 获得完整桌面体验。
   * |link_rpi_connect|: 使用 **Raspberry Pi Connect** 从任何浏览器安全访问您的 Pi。

#. 打开终端并进入代码文件夹：

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_bookexpert.py

#. 当脚本运行时：

   * 摄像头预览窗口将打开
   * RGB LED 将亮起蓝色，表示就绪状态
   * 将一本书的封面放在摄像头前
   * 按下 Fusion HAT+ 上的 USR 按钮（位于 BATTERY 端口附近）
   * 系统将执行：

     1. 拍摄照片（LED 变为黄色 🟡）
     2. 使用 AI 分析（LED 变为紫色 🟣）
     3. 语音播报分析结果（LED 变为绿色 🟢）
     4. 恢复到就绪状态（LED 变为蓝色 🔵）
     5. 如果发生错误，LED 将变为红色 🔴

   * 照片将保存到 ``~/Pictures/book_covers/``
   * 按 Ctrl+C 退出

----------------------------------------------

**代码**

以下是 AI 图书封面分析器的完整 Python 脚本：

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import os
   import time
   import re
   import base64
   import threading
   from pathlib import Path
   from picamera2 import Picamera2, Preview
   from fusion_hat.user_button import UserButton
   from fusion_hat.modules import RGB_LED
   from fusion_hat.pwm import PWM
   from fusion_hat.llm import OpenAI
   from fusion_hat.tts import OpenAI_TTS
   from secret import OPENAI_API_KEY

   class BookCoverAnalyzer:
       def __init__(self):
           # Initialize LED for status feedback
           self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
           self.set_led_color("blue")  # Ready state

           # Initialize OpenAI LLM for image analysis
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",  # GPT-4o supports image input
           )

           # Initialize TTS for audio responses
           self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
           self.tts.set_voice(self.tts.Voice.ALLOY)

           # Initialize camera
           self.camera = Picamera2()
           self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))

           # Initialize button
           self.btn = UserButton()

           # Set up directories
           self.real_user = os.getenv("SUDO_USER") or os.getlogin()
           self.user_home = f"/home/{self.real_user}"
           self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
           self.pictures_dir.mkdir(parents=True, exist_ok=True)

           # Threading locks
           self.photo_lock = threading.Lock()
           self.photo_index = 1

           # Set LLM instructions
           self.instructions = """You are a book expert. Analyze book covers that are sent to you.

           When you receive a book cover image, provide:
           1. Book title (if identifiable from cover)
           2. Author (if identifiable from cover)
           3. Brief summary of what the book is about (50 words)
           4. Overall rating/reception (e.g., "Highly acclaimed", "Classic", "Popular", etc.)

           Keep your response under 100 words total.
           Speak in a friendly, informative tone suitable for an audio response.

           If the image is not a book cover or is unclear, politely say you can't identify it and ask for another photo."""

           self.llm.set_max_messages(10)
           self.llm.set_instructions(self.instructions)

       def set_led_color(self, color_name):
           """Set RGB LED color for status feedback"""
           color_map = {
               "red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "yellow": (255, 255, 0),
               "purple": (255, 0, 255),
               "white": (255, 255, 255),
               "off": (0, 0, 0),
           }

           if color_name in color_map:
               self.rgb_led.color(color_map[color_name])

       def capture_photo(self):
           """Capture a photo and return the filepath"""
           with self.photo_lock:
               filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
               print(f"\n📸 Capturing photo: {filepath}")

               # LED feedback: yellow for capturing
               self.set_led_color("yellow")

               # Capture image
               self.camera.capture_file(str(filepath))

               # Increment counter for next photo
               self.photo_index += 1

               print("Photo captured successfully")
               return str(filepath)

       def analyze_book_cover(self, image_path):
           """Send book cover image to OpenAI for analysis"""
           print("\n Analyzing book cover...")

           # LED feedback: purple for processing
           self.set_led_color("purple")

           try:
               # use fusion_hat.llm's prompt method to process the image
               prompt_text = "Please analyze this book cover and tell me about the book. Provide: 1) Book title if identifiable, 2) Author if identifiable, 3) Brief summary, 4) Overall rating/reception. Keep under 100 words."

               print("Sending to AI for analysis...")

               # method1: non-streaming response
               response = self.llm.prompt(prompt_text, image_path=image_path)

               # if the response is a string, use it directly
               if isinstance(response, str):
                   analysis = response
               else:
                   # if response is not a string, try to convert it to a string
                   analysis = str(response)

               print(f"\n Analysis:\n{analysis}")

               # LED feedback: green for success
               self.set_led_color("green")

               return analysis

           except Exception as e:
               print(f"Error analyzing image: {e}")
               print(f"Error type: {type(e)}")

               # method2: streaming response
               try:
                   print("Trying stream method...")
                   stream_response = self.llm.prompt(prompt_text, stream=True, image_path=image_path)

                   # receive the stream response
                   analysis_parts = []
                   for next_word in stream_response:
                       if next_word:
                           analysis_parts.append(next_word)

                   analysis = ''.join(analysis_parts)
                   print(f"\n Analysis (stream):\n{analysis}")

                   # LED feedback: green for success
                   self.set_led_color("green")
                   return analysis

               except Exception as e2:
                   print(f"Stream method also failed: {e2}")

                   # LED feedback: red for error
                   self.set_led_color("red")
                   return "Sorry, I couldn't analyze the book cover. Please make sure the book cover is clearly visible and try again."

       def speak_response(self, text):
           """Convert text to speech"""
           print("\nSpeaking response...")

           # Clean up text for TTS (remove markdown, etc.)
           clean_text = re.sub(r'[*_\[\]()#]', '', text)

           # Speak with friendly instructions
           self.tts.say(clean_text, instructions="speak clearly and warmly")
           print("Response spoken")

           # Return to ready state
           self.set_led_color("blue")

       def button_handler(self):
           """Handle button press: capture photo, analyze, and speak"""
           print("\n" + "="*50)
           print("Processing request...")

           # Step 1: Capture photo
           try:
               image_path = self.capture_photo()
           except Exception as e:
               print(f"Failed to capture photo: {e}")
               self.set_led_color("red")
               self.tts.say("Sorry, I couldn't take a photo. Please try again.")
               self.set_led_color("blue")
               return

           # Step 2: Analyze with AI
           analysis = self.analyze_book_cover(image_path)

           # Step 3: Speak the analysis
           self.speak_response(analysis)

           print(f"Complete! Photo saved at: {image_path}")
           print("="*50 + "\n")

       def run(self):
           """Main program loop"""
           # Set button callback
           self.btn.set_on_click(self.button_handler)

           # Start camera preview
           print("Starting camera preview...")
           self.camera.start_preview(Preview.QT)
           self.camera.start()

           # LED feedback: blue for ready
           self.set_led_color("blue")

           print("\n" + "="*50)
           print("BOOK COVER ANALYZER")
           print("="*50)
           print("\nReady to analyze book covers!")
           print("Press the USR button to capture and analyze a book cover")
           print("I will speak the analysis aloud")
           print("LED colors:")
           print("   Blue: Ready")
           print("   Yellow: Capturing photo")
           print("   Purple: Analyzing with AI")
           print("   Green: Analysis successful")
           print("   Red: Error occurred")
           print(f"Photos saved to: {self.pictures_dir}")
           print("Press Ctrl+C to exit")
           print("="*50 + "\n")

           try:
               # Keep program running
               while True:
                   time.sleep(0.1)

           except KeyboardInterrupt:
               print("\nExiting...")

           finally:
               # Cleanup
               self.camera.stop_preview()
               self.camera.close()
               self.set_led_color("off")
               print("Cleanup complete")

   if __name__ == "__main__":
       analyzer = BookCoverAnalyzer()
       analyzer.run()

----------------------------------------------

**理解代码**

1. 摄像头初始化

   Picamera2 库为 Raspberry Pi 摄像头控制提供了现代接口，支持图像拍摄和预览。

   .. code-block:: python

      self.camera = Picamera2()
      self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))

      # Start preview and camera
      self.camera.start_preview(Preview.QT)
      self.camera.start()

2. 带线程安全的图像拍摄

   拍摄照片方法使用线程锁防止同时捕获，并确保文件命名正确。

   .. code-block:: python

      def capture_photo(self):
          with self.photo_lock:
              filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
              self.camera.capture_file(str(filepath))
              self.photo_index += 1
              return str(filepath)

3. AI 视觉分析

   系统使用 GPT-4o 的视觉能力分析图书封面。为实现健壮性，实现了流式和非流式两种方法。

   .. code-block:: python

      def analyze_book_cover(self, image_path):
          prompt_text = "Please analyze this book cover..."

          # Method 1: Non-streaming response
          response = self.llm.prompt(prompt_text, image_path=image_path)

          # Method 2: Fallback to streaming if needed
          stream_response = self.llm.prompt(prompt_text, stream=True, image_path=image_path)

4. 文字转语音（TTS）转换

   OpenAI 的 TTS API 将 AI 的分析结果转换为自然语音，并提供可配置的语音选项。

   .. code-block:: python

      self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
      self.tts.set_voice(self.tts.Voice.ALLOY)

      def speak_response(self, text):
          clean_text = re.sub(r'[*_\[\]()#]', '', text)  # Remove markdown
          self.tts.say(clean_text, instructions="speak clearly and warmly")

5. 状态反馈系统

   RGB LED 通过颜色编码在整个过程中提供视觉反馈：

   .. code-block:: python

      def set_led_color(self, color_name):
          color_map = {
              "red": (255, 0, 0),      # Error
              "green": (0, 255, 0),    # Success
              "blue": (0, 0, 255),     # Ready
              "yellow": (255, 255, 0), # Capturing
              "purple": (255, 0, 255), # Processing
          }
          self.rgb_led.color(color_map[color_name])

6. 按钮事件处理

   USR 按钮通过事件回调触发整个分析流程。

   .. code-block:: python

      def button_handler(self):
          # 1. Capture photo
          image_path = self.capture_photo()
          # 2. Analyze with AI
          analysis = self.analyze_book_cover(image_path)
          # 3. Speak the analysis
          self.speak_response(analysis)

      # Set callback
      self.btn.set_on_click(self.button_handler)

7. 文件管理

   照片自动按顺序编号保存到指定目录。

   .. code-block:: python

      self.real_user = os.getenv("SUDO_USER") or os.getlogin()
      self.user_home = f"/home/{self.real_user}"
      self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
      self.pictures_dir.mkdir(parents=True, exist_ok=True)

----------------------------------------------

**故障排除**

- "Camera not detected" 错误

  - 确保摄像头排线正确插入（金色触点朝向正确方向）
  - 运行 ``sudo raspi-config``\ 并启用摄像头接口
  - 启用摄像头后重启

- "No preview window appears"

  - 确保您在带有桌面环境的 Raspberry Pi 上运行
  - 对于无头操作，请移除或修改预览代码
  - 检查是否分配了足够的 GPU 内存

- "OpenAI API error"

  - 验证 ``secret.py``\ 中的 API 密钥是否正确且余额充足
  - 检查网络连接：\ ``ping 8.8.8.8``
  - 确保您的账户具有 GPT-4o 和 TTS API 的访问权限

- "TTS audio not playing"

  - 检查音频输出配置：\ ``sudo raspi-config`` → **系统选项** → **音频**
  - 测试音频：\ ``speaker-test -t sine -f 440``
  - 确保音箱/耳机已连接到正确的音频插孔

- "Button press not detected"

  - 按下时检查用户按钮（User Button）的 LED 是否亮起
  - 确保 Fusion HAT+ 正确安装在 GPIO 引脚上
  - 验证按钮回调是否正确设置

- "Image analysis returns generic responses"

  - 拍摄图书封面时确保光线充足
  - 将图书封面正对摄像头画面
  - 先尝试知名书籍以获得更好的识别效果
  - 如果画面模糊，请清洁摄像头镜头

----------------------------------------------

本项目展示了计算机视觉、自然语言处理和物理计算相结合的强大能力，创建了一个智能图书分析系统。它展示了 AI 如何增强与图书等日常物品的交互，让信息获取更加便捷和有趣！
