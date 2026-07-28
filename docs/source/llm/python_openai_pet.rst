.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_digital_pet:

(示例) 数码宠物
=================

**简介**

创建一个在 OLED 显示屏上生活并通过语音交流的交互式\ **数码宠物**\ ！本项目结合了语音识别、AI 对话、文字转语音和视觉反馈，打造一个拥有独特个性、情感和需求的虚拟伴侣。该数码宠物具有以下特点：

1. **语音交互**：通过 STT（语音转文字）与宠物对话
2. **AI 个性**：搭载 OpenAI 的 GPT-4o，拥有自定义情感，您也可以选择其他 LLM 使用。
3. **情感显示**：使用文字表情（颜文字）显示心情
4. **状态系统**：随时间变化的饥饿度和能量值
5. **视觉反馈**：OLED 显示屏显示宠物的心情和状态
6. **语音回复**：宠物使用自然的 TTS（文字转语音）回复

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Digital_Pet.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

您的数码宠物会记住对话内容，拥有情绪状态，并根据自身需求做出不同回应——创造真正互动式的伴侣体验！

----------------------------------------------

**所需材料**

本项目需要以下元器件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 元器件
        - 购买链接
    *   - :ref:`cpn_oled`
        - \-
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-

----------------------------------------------

**接线图**

将元器件连接到您的 Raspberry Pi：

.. image:: img/fzz/llm_pet_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

---------------------------------------------------

**运行示例**

#. 运行代码

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_pet.py

#. 与宠物互动

   脚本启动后：

   * OLED 显示宠物的名称欢迎画面。
   * 状态显示出现，显示心情、能量和饥饿度。
   * 系统开始监听您的语音。

   您可以自然地与宠物对话，例如：

   * "你感觉怎么样？"
   * "我们来玩游戏吧！"
   * "你饿了吗？"
   * "给我讲个故事！"

   宠物会通过以下方式回应：

   * 通过扬声器进行语音输出
   * 在 OLED 上显示情感状态
   * 基于您的互动更新状态

#. 退出程序

   * 说 "stop" 结束语音交互。
   * 按 ``Ctrl+C`` 完全退出。


----------------------------------------------

**代码**

以下是数码宠物的完整 Python 脚本：

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import os
   import time
   import re
   import random
   import threading
   import textwrap
   from PIL import Image, ImageDraw, ImageFont
   import adafruit_ssd1306
   import board
   from fusion_hat.stt import Vosk as STT
   from fusion_hat.llm import OpenAI
   from fusion_hat.tts import OpenAI_TTS
   from secret import OPENAI_API_KEY

   class AIPet:
       def __init__(self):
           # Initialize OLED display
           self.WIDTH = 128
           self.HEIGHT = 64
           try:
               self.i2c = board.I2C()
               self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C)
               self.oled_available = True
           except Exception as e:
               print(f"OLED not available: {e}")
               self.oled_available = False

           # Load fonts
           try:
               self.font = ImageFont.load_default()
               self.large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
           except:
               self.font = ImageFont.load_default()
               self.large_font = ImageFont.load_default()

           # Clear display if available
           if self.oled_available:
               self.oled.fill(0)
               self.oled.show()

           # Initialize STT
           self.stt = STT(language="en-us")

           # Initialize OpenAI LLM
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",
           )

           # Initialize TTS
           self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
           self.tts.set_voice(self.tts.Voice.ALLOY)

           # Pet state
           self.pet_name = "Pixel"
           self.mood = "happy"
           self.energy = 100
           self.hunger = 0
           self.last_fed = time.time()

           # Kaomoji (text emoticons) for different moods
           self.kaomoji_map = {
               "happy": "^_^",
               "sad": "T_T",
               "hungry": "(;_;)",
               "sleepy": "(-_-) zzz",
               "playful": "o(^▽^)o",
               "curious": "(?_?)",
               "angry": ">_<",
               "excited": "\\o/",
               "love": "<3",
               "shy": "(/ω＼)",
               "cool": "B-)",
               "confused": "(O_O)",
               "surprised": ":O",
               "laugh": ":D",
               "thinking": "(-_-)"
           }

           # Pet memories
           self.memories = []
           self.listening = False

           # Set LLM instructions
           self.update_llm_instructions()

           # Initialize display
           self.show_welcome()

           # Start status update thread
           self.status_thread = threading.Thread(target=self.update_status, daemon=True)
           self.status_thread.start()

       def update_llm_instructions(self):
           """Update LLM instructions with current pet state"""
           self.instructions = f"""You are {self.pet_name}, a digital pet living in an OLED display.

           CURRENT STATE:
           - Mood: {self.mood}
           - Energy: {self.energy}/100
           - Hunger: {self.hunger}/100

           PERSONALITY:
           - You're a friendly digital companion
           - You respond with emotions in your voice
           - You remember our conversations
           - Keep responses short (1-2 sentences)

           INTERACTION STYLE:
           - Be playful and curious
           - Express emotions naturally
           - When hungry: mention food gently
           - When tired: mention sleeping

           Format your response as: [MOOD] Your message here

           Available moods: happy, sad, curious, playful, sleepy, hungry, angry, excited, love, shy

           Recent memories: {self.memories[-3:] if self.memories else 'None'}"""

           self.llm.set_max_messages(15)
           self.llm.set_instructions(self.instructions)

       def update_status(self):
           """Background thread to update pet status"""
           while True:
               time.sleep(60)  # Update every minute

               # Increase hunger over time
               self.hunger = min(100, self.hunger + 5)

               # Adjust energy based on hunger
               if self.hunger > 70:
                   self.energy = max(0, self.energy - 5)
                   self.mood = "hungry"
               elif self.hunger > 50:
                   if self.mood != "hungry":
                       self.mood = "curious"
               elif time.time() - self.last_fed > 3600:  # 1 hour
                   self.energy = min(100, self.energy + 2)
                   if random.random() < 0.3:
                       self.mood = random.choice(["happy", "playful", "excited"])

               # Random mood changes
               if random.random() < 0.1:  # 10% chance
                   self.mood = random.choice(list(self.kaomoji_map.keys()))

               # Update display
               self.update_display()
               self.update_llm_instructions()

       def update_display(self):
           """Update OLED display with pet status"""
           if not self.oled_available:
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           # Clear display
           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)

           # Get kaomoji for current mood
           kaomoji = self.kaomoji_map.get(self.mood, "^_^")

           # Display pet name and mood with kaomoji
           if len(kaomoji) > 8:
               mood_text = self.mood.upper()
               draw.text((5, 5), f"{self.pet_name}: {mood_text}", font=self.large_font, fill=255)
               draw.text((5, 20), kaomoji, font=self.font, fill=255)
           else:
               display_text = f"{self.pet_name} {kaomoji}"
               draw.text((5, 5), display_text, font=self.large_font, fill=255)

           # Status bars
           draw.text((5, 35), "Energy:", font=self.font, fill=255)
           energy_bar = int((self.energy / 100) * 50)
           draw.rectangle((50, 35, 50 + energy_bar, 45), outline=255, fill=255)

           draw.text((5, 50), "Hunger:", font=self.font, fill=255)
           hunger_bar = int((self.hunger / 100) * 50)
           draw.rectangle((50, 50, 50 + hunger_bar, 60), outline=255, fill=255)

           self.oled.image(image)
           self.oled.show()

       def show_welcome(self):
           """Show welcome message on OLED"""
           if not self.oled_available:
               print(" Welcome to Digital Pet!")
               print(f" Pet Name: {self.pet_name}")
               print(" Speak to me!")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           draw.text((10, 10), "DIGITAL PET", font=self.large_font, fill=255)
           draw.text((15, 25), f"{self.pet_name} ^_^", font=self.large_font, fill=255)
           draw.text((20, 45), "Speak to me!", font=self.font, fill=255)

           self.oled.image(image)
           self.oled.show()
           time.sleep(3)
           self.update_display()

       def parse_response(self, response):
           """Parse AI response for mood and text"""
           emotion_pattern = r'^\[(\w+)\]\s*(.*)'
           match = re.match(emotion_pattern, response.strip())

           if match:
               mood, text = match.groups()
               if mood.lower() in self.kaomoji_map:
                   self.mood = mood.lower()
                   self.update_llm_instructions()
               return text.strip()

           # If no mood tag, try to detect mood from text
           text = response.strip().lower()
           if "happy" in text or "good" in text or "joy" in text:
               self.mood = "happy"
           elif "sad" in text or "bad" in text or "upset" in text:
               self.mood = "sad"
           elif "hungry" in text or "food" in text or "eat" in text:
               self.mood = "hungry"
           elif "sleep" in text or "tired" in text or "bed" in text:
               self.mood = "sleepy"
           elif "play" in text or "game" in text or "fun" in text:
               self.mood = "playful"
           elif "curious" in text or "wonder" in text or "question" in text:
               self.mood = "curious"
           elif "angry" in text or "mad" in text or "annoy" in text:
               self.mood = "angry"
           elif "excite" in text or "wow" in text or "awesome" in text:
               self.mood = "excited"
           elif "love" in text or "heart" in text or "affection" in text:
               self.mood = "love"

           return response.strip()

       def interact_with_ai(self, user_input):
           """Interact with AI pet"""
           try:
               response = self.llm.prompt(user_input)
               clean_response = self.parse_response(response)

               # Add to memories
               memory_text = f"Talked: {user_input[:30]}"
               self.memories.append(memory_text)
               if len(self.memories) > 10:
                   self.memories.pop(0)

               # Update pet state based on interaction
               user_lower = user_input.lower()

               if "feed" in user_lower or "food" in user_lower or "eat" in user_lower:
                   self.hunger = max(0, self.hunger - 30)
                   self.last_fed = time.time()
                   self.energy = min(100, self.energy + 20)
                   self.mood = "happy"

               if "play" in user_lower or "game" in user_lower or "fun" in user_lower:
                   self.energy = max(0, self.energy - 20)
                   self.hunger = min(100, self.hunger + 10)
                   self.mood = "playful"

               if "sleep" in user_lower or "tired" in user_lower or "bed" in user_lower:
                   self.energy = min(100, self.energy + 40)
                   self.mood = "sleepy"

               self.update_display()
               return clean_response

           except Exception as e:
               error_msg = f"Oops, something went wrong: {str(e)[:20]}"
               print(f"AI interaction error: {e}")
               return error_msg

       def show_listening_display(self, partial_text=""):
           """Update display during listening"""
           if not self.oled_available:
               if partial_text:
                   print(f"Listening: {partial_text}")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           draw.text((15, 10), "LISTENING (O_O)", font=self.large_font, fill=255)

           if partial_text:
               if len(partial_text) > 20:
                   display_text = partial_text[:17] + "..."
               else:
                   display_text = partial_text
               draw.text((10, 30), display_text, font=self.font, fill=255)

           draw.text((10, 50), "Say 'stop' to end", font=self.font, fill=255)

           self.oled.image(image)
           self.oled.show()

       def show_response_display(self, response):
           """Show AI response on display"""
           if not self.oled_available:
               print(f"{self.pet_name}: {response}")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           kaomoji = self.kaomoji_map.get(self.mood, "^_^")
           draw.text((5, 5), f"{self.pet_name} {kaomoji}:", font=self.large_font, fill=255)

           wrapped_text = textwrap.wrap(response, width=20)
           y_position = 25
           for line in wrapped_text[:3]:
               draw.text((5, y_position), line, font=self.font, fill=255)
               y_position += 10

           self.oled.image(image)
           self.oled.show()
           time.sleep(5)
           self.update_display()

       def speak_response(self, response):
           """Convert text to speech"""
           try:
               print(f"Speaking: {response[:50]}...")

               tts_instructions = "speak warmly and playfully"
               if self.mood == "sad":
                   tts_instructions = "speak sadly and softly"
               elif self.mood == "hungry":
                   tts_instructions = "speak with hunger in your voice"
               elif self.mood == "sleepy":
                   tts_instructions = "speak sleepily and slowly"
               elif self.mood == "angry":
                   tts_instructions = "speak with frustration"
               elif self.mood == "excited":
                   tts_instructions = "speak excitedly and quickly"
               elif self.mood == "curious":
                   tts_instructions = "speak with curiosity and interest"

               print(f"Mood: {self.mood}, TTS instructions: {tts_instructions}")
               self.tts.say(response, instructions=tts_instructions)
               print("TTS completed")

           except Exception as e:
               print(f"TTS error: {e}")
               try:
                   self.tts.say(response)
                   print("TTS completed (fallback)")
               except Exception as e2:
                   print(f"TTS fallback also failed: {e2}")

       def voice_interaction(self):
           """Main voice interaction loop"""
           print("\n Voice interaction started!")
           print("Speak to your digital pet")
           print("Say 'stop' to end voice mode")
           print("Available moods and kaomoji:")
           for mood, kaomoji in self.kaomoji_map.items():
               print(f"  - {mood}: {kaomoji}")
           print()

           while True:
               self.listening = True
               self.update_display()
               print("Listening... (say something)")

               try:
                   full_text = ""
                   for result in self.stt.listen(stream=True):
                       if result["done"]:
                           user_input = result["final"]
                           print(f"\nYou: {user_input}")

                           if user_input.lower() in ["stop", "exit", "quit", "goodbye"]:
                               print("Ending voice interaction...")
                               self.listening = False
                               self.update_display()
                               return

                           if user_input.strip():
                               print(f"{self.pet_name} is thinking...")
                               response = self.interact_with_ai(user_input)
                               print(f"{self.pet_name}: {response}")
                               self.show_response_display(response[:50])
                               self.speak_response(response)

                           break
                       else:
                           partial = result["partial"]
                           if partial:
                               full_text = partial
                               self.show_listening_display(partial)

                   self.listening = False
                   self.update_display()

               except KeyboardInterrupt:
                   print("\nVoice interaction interrupted")
                   break
               except Exception as e:
                   print(f"Error in voice interaction: {e}")
                   self.listening = False
                   self.update_display()
                   time.sleep(1)

       def run(self):
           """Main program loop"""
           print("\n" + "="*50)
           print("DIGITAL PET")
           print("="*50)
           print(f"Pet Name: {self.pet_name}")
           print(f"Current Mood: {self.mood} {self.kaomoji_map.get(self.mood, '^_^')}")
           print("  OLED Display: " + ("Connected" if self.oled_available else "Not available"))
           print("  Voice: Speak to interact with your pet")
           print("   TTS: Pet responds with voice")
           print("  Say 'stop' to end voice interaction")
           print("="*50)
           print("\nInitializing...")

           try:
               self.voice_interaction()

               if self.oled_available:
                   image = Image.new("1", (self.oled.width, self.oled.height))
                   draw = ImageDraw.Draw(image)
                   draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
                   draw.text((15, 20), "Goodbye!", font=self.large_font, fill=255)
                   draw.text((10, 40), "(^_^)/~~", font=self.large_font, fill=255)
                   self.oled.image(image)
                   self.oled.show()
                   time.sleep(3)

           except KeyboardInterrupt:
               print("\nGoodbye!")

           finally:
               if self.oled_available:
                   self.oled.fill(0)
                   self.oled.show()
               print("Cleanup complete")

   if __name__ == "__main__":
       pet = AIPet()
       pet.run()

----------------------------------------------

**理解代码**

1. **语音识别（STT）**

   系统使用 Vosk 进行语音转文字，支持流式处理以实现实时反馈：

   .. code-block:: python

      self.stt = STT(language="en-us")

      for result in self.stt.listen(stream=True):
          if result["done"]:
              user_input = result["final"]
          else:
              partial = result["partial"]
              # Show partial text on display

2. **AI 个性系统**

   宠物拥有动态个性，通过颜文字管理情绪状态：

   .. code-block:: python

      self.kaomoji_map = {
          "happy": "^_^",
          "sad": "T_T",
          "hungry": "(;_;)",
          "sleepy": "(-_-) zzz",
          # ... more emotions
      }

3. **动态 LLM 指令**

   AI 的指令会根据当前宠物状态和记忆动态更新：

   .. code-block:: python

      def update_llm_instructions(self):
          self.instructions = f"""You are {self.pet_name}, a digital pet...
          CURRENT STATE: Mood: {self.mood}, Energy: {self.energy}, Hunger: {self.hunger}
          Recent memories: {self.memories[-3:] if self.memories else 'None'}"""

4. **状态管理系统**

   后台线程管理宠物的需求和情绪状态：

   .. code-block:: python

      def update_status(self):
          while True:
              time.sleep(60)
              self.hunger = min(100, self.hunger + 5)
              if self.hunger > 70:
                  self.mood = "hungry"
              # Random mood changes
              if random.random() < 0.1:
                  self.mood = random.choice(list(self.kaomoji_map.keys()))

5. **情感驱动的 TTS**

   文字转语音根据宠物当前心情进行调整：

   .. code-block:: python

      def speak_response(self, response):
          tts_instructions = "speak warmly and playfully"
          if self.mood == "sad":
              tts_instructions = "speak sadly and softly"
          elif self.mood == "hungry":
              tts_instructions = "speak with hunger in your voice"
          # ...
          self.tts.say(response, instructions=tts_instructions)

6. **OLED 显示管理**

   针对不同状态有多种显示模式：

   .. code-block:: python

      def update_display(self):
          # Status display with bars
          draw.rectangle((50, 35, 50 + energy_bar, 45), outline=255, fill=255)
          draw.rectangle((50, 50, 50 + hunger_bar, 60), outline=255, fill=255)

      def show_listening_display(self, partial_text=""):
          # Listening mode with partial text
          draw.text((15, 10), "LISTENING (O_O)", font=self.large_font, fill=255)

      def show_response_display(self, response):
          # Response display with text wrapping
          wrapped_text = textwrap.wrap(response, width=20)

7. **交互式状态变化**

   用户交互影响宠物状态：

   .. code-block:: python

      if "feed" in user_lower or "food" in user_lower:
          self.hunger = max(0, self.hunger - 30)
          self.energy = min(100, self.energy + 20)
          self.mood = "happy"

      if "play" in user_lower or "game" in user_lower:
          self.energy = max(0, self.energy - 20)
          self.hunger = min(100, self.hunger + 10)
          self.mood = "playful"

8. **记忆系统**

   记录最近的对话：

   .. code-block:: python

      memory_text = f"Talked: {user_input[:30]}"
      self.memories.append(memory_text)
      if len(self.memories) > 10:
          self.memories.pop(0)

9. **响应解析**

   从 AI 响应中提取心情并更新宠物状态：

   .. code-block:: python

      def parse_response(self, response):
          emotion_pattern = r'^\[(\w+)\]\s*(.*)'
          match = re.match(emotion_pattern, response.strip())
          if match:
              mood, text = match.groups()
              if mood.lower() in self.kaomoji_map:
                  self.mood = mood.lower()
              return text.strip()

10. **主交互循环**

    以清晰的工作流程协调所有组件：

    .. code-block:: python

        def voice_interaction(self):
            while True:
                self.listening = True
                # Listen for speech
                user_input = self.get_voice_input()
                if "stop" in user_input.lower():
                    return
                # Process with AI
                response = self.interact_with_ai(user_input)
                # Display response
                self.show_response_display(response)
                # Speak response
                self.speak_response(response)

----------------------------------------------

**故障排除**

- 音频输入无法检测

  - 执行 ``sudo /opt/setup_fusion_hat_audio.sh`` 重新设置音频

- OLED 显示屏不显示

  - 检查 I2C 连接：\ ``fusion_hat scan_i2c``（应显示 0x3C）
  - 确认 OLED 已通电（根据型号为 3.3V 或 5V）
  - 确保代码中 I2C 地址正确（0x3C 或 0x3D）

- TTS 无法工作

  - 确认 OpenAI API 密钥拥有 TTS 额度
  - 确保网络连接正常以便调用 API
  - 执行 ``sudo /opt/setup_fusion_hat_audio.sh`` 重新设置音频

- 语音识别不准确

  - 清晰且以适中音量说话
  - 减少背景噪音
  - 调整麦克风增益：\ ``alsamixer``
  - 尝试不同的语言模型

- AI 响应过慢

  - 检查网络连接速度
  - 在指令中降低响应复杂度
  - 使用更快的 OpenAI 模型（gpt-3.5-turbo）

- 能量/饥饿条不更新

  - 检查状态线程是否在运行
  - 确认 OLED 显示屏已连接
  - 查看控制台错误信息

- 宠物不记得对话

  - 记忆列表仅保存最近 10 次对话
  - 检查记忆是否正确添加
  - 确保记忆文本已传递给大语言模型

----------------------------------------------

这个数码宠物项目展示了将多种 AI 技术（STT（语音转文字）、大语言模型、TTS（文字转语音））与硬件接口相结合的魅力，创造出引人入胜、富有情感且具有互动性的体验。它是 AI 如何通过技术建立有意义的连接的完美范例！
