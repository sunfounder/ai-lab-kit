.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

（示例）带云台摄像头的作业批改演示
==================================

**简介**

该项目创建了一个交互式的\ **AI 作业批改助手**\ ，结合了计算机视觉、人工智能和机器人技术。该系统：

1. **拍摄照片**\ ：使用树莓派摄像头拍摄手写或打印的作业题目
2. **分析内容**\ ：使用 OpenAI 的 GPT-4 Vision 模型判断答案是否正确
3. **提供物理反馈**\ ：通过舵机控制的云台运动：

   - *点头*\ 表示答案正确
   - *摇头*\ 表示答案错误

4. **简单交互**\ ：通过单次按钮触发

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

这个演示展示了 AI 如何与物理世界互动，创造出一个引人入胜的教育工具，为作业准确性提供即时视觉反馈。

你可以使用其他 LLM 模块和硬件组件来构建自己的 AI 辅助学习设备。参见：

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**所需组件**

本项目需要以下组件：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - 组件
        - 购买链接
    *   - :ref:`cpn_servo`
        - |link_servo_buy|
    *   - 云台
        -
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-
    *   - 作业样本（打印或手写）
        - \-

----------------------------------------------

**硬件设置**

为了方便使用摄像头模块，建议 :ref:`assemble_fusion_hat_pan_tilt`。

   .. note::

     安装云台可能会遮挡一些引脚，因此建议仅在使用摄像头时安装，或在安装后将其放置在外侧。


   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**运行代码**

#. 创建作业样本：

   - 写或打印一个简单的数学题目及答案
   - 例如："5 + 3 = 8"（正确）或 "5 + 3 = 7"（错误）
   - 确保手写或打印清晰

#. 运行程序：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. 按照屏幕提示操作：

   - 将作业放在摄像头下
   - 按下 Fusion HAT+ 上的用户按钮（USR）
   - 观察舵机的反应

#. 预期输出：

   .. code-block:: text

      HOMEWORK GRADING DEMO
      ==================================================
      Instructions:
      1. Place a homework question under the camera
      2. Make sure the question AND answer are visible
      3. Press the User Button (USR) on Fusion HAT to grade
      4. The camera will take a photo
      5. AI will grade the answer
      6. Servo will nod (correct) or shake (incorrect)
      ==================================================

      Waiting for button press...

      ==================================================
      Button pressed - Starting grading process

      Taking photo...
      Photo captured
      Sending to AI for grading...
      AI response: CORRECT
      Answer is correct - nodding head
      ==================================================

----------------------------------------------

**代码**

以下是作业批改演示的完整 Python 脚本：


.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   """
   Homework Grading Demo with Pan-Tilt Camera
   Press User Button to take photo, LLM grades, servo nods or shakes
   """

   import time
   from fusion_hat.llm import OpenAI
   from fusion_hat.servo import Servo
   from fusion_hat.user_button import UserButton
   from picamera2 import Picamera2, Preview

   # ========== LLM SETTINGS ==========
   # Create a secret.py file with: OPENAI_API_KEY = "your-api-key-here"
   try:
       from secret import OPENAI_API_KEY
   except ImportError:
       print("ERROR: Please create a secret.py file with your OpenAI API key")
       print("Example content: OPENAI_API_KEY = 'sk-...'")
       exit()

   # LLM instructions for grading
   INSTRUCTIONS = """You are a homework grading assistant.
   When you see a photo of a homework question with an answer,
   determine if the answer is correct or incorrect.

   Respond with ONLY ONE WORD:
   - If the answer is CORRECT, respond: "CORRECT"
   - If the answer is INCORRECT, respond: "INCORRECT"

   Do not provide any other text, explanations, or justifications.
   Only respond with "CORRECT" or "INCORRECT"."""

   # Initialize LLM
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o"
   )

   # Set LLM settings
   llm.set_max_messages(5)
   llm.set_instructions(INSTRUCTIONS)

   # ========== HARDWARE SETTINGS ==========
   PAN_CHANNEL = 2      # Horizontal servo for shaking head
   TILT_CHANNEL = 3     # Vertical servo for nodding head

   # Servo center positions
   TILT_CENTER = 0      # Looking straight ahead
   PAN_CENTER = 0       # Center position

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Homework Grading Demo...")
   print("-" * 50)

   # Initialize servos
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center servos
   tilt_servo.angle(TILT_CENTER)
   pan_servo.angle(PAN_CENTER)
   time.sleep(1)
   print("Servos ready")

   # Initialize camera
   camera = Picamera2()
   camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
   camera.configure(camera_config)
   camera.start_preview(Preview.QT)
   camera.start()
   time.sleep(2)
   print("Camera ready")

   # Initialize user button
   user_button = UserButton()
   print("User button ready")
   print("-" * 50)

   # ========== SERVO MOVEMENT FUNCTIONS ==========
   def nod_head():
       """
       Nodding head movement for "correct"
       """
       # Look down
       tilt_servo.angle(15)
       time.sleep(0.2)
       # Look up
       tilt_servo.angle(-10)
       time.sleep(0.2)
       # Return to center
       tilt_servo.angle(TILT_CENTER)

   def shake_head():
       """
       Shaking head movement for "incorrect"
       """
       # Look left
       pan_servo.angle(-20)
       time.sleep(0.15)
       # Look right
       pan_servo.angle(20)
       time.sleep(0.15)
       # Look left again
       pan_servo.angle(-15)
       time.sleep(0.15)
       # Return to center
       pan_servo.angle(PAN_CENTER)

   # ========== GRADING FUNCTION ==========
   def grade_homework():
       """
       Main grading function: take photo, send to LLM, move servo
       """
       print("\nTaking photo...")

       # Capture image
       img_path = './homework.jpg'
       camera.capture_file(img_path)
       print("Photo captured")

       # Send to LLM for grading
       print("Sending to AI for grading...")

       prompt = "Look at this homework question and answer. Is the answer correct? Respond with only one word: 'CORRECT' or 'INCORRECT'."

       response = llm.prompt(prompt, image_path=img_path)
       response_text = response.strip().upper()

       print(f"AI response: {response_text}")

       # Move servo based on response
       if "INCORRECT" in response_text:
           print("Answer is incorrect - shaking head")
           shake_head()
       elif "CORRECT" in response_text:
           print("Answer is correct - nodding head")
           nod_head()
       else:
           print(f"Unexpected response: {response_text}")

   # ========== BUTTON CALLBACK ==========
   def on_button_click():
       """
       Called when user button is pressed
       """
       print("\n" + "=" * 50)
       print("Button pressed - Starting grading process")
       grade_homework()
       print("=" * 50)

   # ========== MAIN DEMO ==========
   def main():
       """
       Main demo function
       """
       print("\nHOMEWORK GRADING DEMO")
       print("=" * 50)
       print("Instructions:")
       print("1. Place a homework question under the camera")
       print("2. Make sure the question AND answer are visible")
       print("3. Press the User Button (USR) on Fusion HAT to grade")
       print("4. The camera will take a photo")
       print("5. AI will grade the answer")
       print("6. Servo will nod (correct) or shake (incorrect)")
       print("=" * 50)
       print("\nWaiting for button press...")

       # Set button callback
       user_button.set_on_click(on_button_click)

       # Keep program running
       try:
           while True:
               time.sleep(0.1)
       except KeyboardInterrupt:
           print("\nDemo stopped by user")

   # ========== CLEANUP ==========
   def cleanup():
       """
       Clean up resources
       """
       print("\nCleaning up...")

       # Return servos to center
       tilt_servo.angle(TILT_CENTER)
       pan_servo.angle(PAN_CENTER)

       # Stop camera
       camera.stop()

       print("Demo ended")

   # ========== RUN DEMO ==========
   if __name__ == "__main__":
       try:
           main()
       finally:
           cleanup()

----------------------------------------------

**理解代码**

1. LLM 配置和设置

   系统使用 OpenAI 的 GPT-4o 视觉能力分析图像：

   .. code-block:: python

      # Import and initialize the LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

      # Set specific instructions for consistent responses
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)

      # Limit conversation history to manage tokens
      llm.set_max_messages(5)

2. 硬件初始化

   初始化三个硬件组件：舵机、摄像头和按钮：

   .. code-block:: python

      # Servo control for pan-tilt mechanism
      pan_servo = Servo(PAN_CHANNEL)   # Channel 2 for horizontal movement
      tilt_servo = Servo(TILT_CHANNEL) # Channel 3 for vertical movement

      # Camera setup with preview
      camera = Picamera2()
      camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
      camera.configure(camera_config)
      camera.start_preview(Preview.QT)
      camera.start()

      # User button for interaction
      user_button = UserButton()

3. 舵机动画函数

   实现自然的点头和摇头动作：

   .. code-block:: python

      def nod_head():
          """Nodding head movement for 'correct' answers"""
          tilt_servo.angle(15)    # Look down
          time.sleep(0.2)
          tilt_servo.angle(-10)   # Look up
          time.sleep(0.2)
          tilt_servo.angle(TILT_CENTER)  # Return to center

      def shake_head():
          """Shaking head movement for 'incorrect' answers"""
          pan_servo.angle(-20)    # Look left
          time.sleep(0.15)
          pan_servo.angle(20)     # Look right
          time.sleep(0.15)
          pan_servo.angle(-15)    # Look left again
          time.sleep(0.15)
          pan_servo.angle(PAN_CENTER)  # Return to center

4. 图像拍摄和 AI 分析

   主要的批改工作流：

   .. code-block:: python

      def grade_homework():
          # Capture image from camera
          img_path = './homework.jpg'
          camera.capture_file(img_path)

          # Send image to LLM with specific prompt
          prompt = "Look at this homework question and answer..."
          response = llm.prompt(prompt, image_path=img_path)
          response_text = response.strip().upper()

          # Interpret response and trigger appropriate servo movement
          if "INCORRECT" in response_text:
              shake_head()
          elif "CORRECT" in response_text:
              nod_head()

5. 按钮事件处理

   简单的回调系统用于用户交互：

   .. code-block:: python

      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()

      # Assign callback to button
      user_button.set_on_click(on_button_click)

6. 主应用程序循环

   等待按钮按下的最小主循环：

   .. code-block:: python

      def main():
          print("Waiting for button press...")
          user_button.set_on_click(on_button_click)

          # Keep program running until interrupted
          try:
              while True:
                  time.sleep(0.1)  # Low CPU usage wait
          except KeyboardInterrupt:
              print("\nDemo stopped by user")

7. 资源清理

   正确的关机程序：

   .. code-block:: python

      def cleanup():
          # Return servos to neutral position
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)

          # Stop camera
          camera.stop()

----------------------------------------------

**故障排除**

- 没有名为 ``picamera2``\ 的模块

  安装所需的库：

  .. code-block:: bash

     sudo apt update
     sudo apt install python3-picamera2

- 未检测到摄像头

  1. 检查摄像头连接：确保排线正确插入
  2. 验证摄像头已启用：\ ``sudo raspi-config`` → Interface Options → Camera
  3. 独立测试摄像头：\ ``libcamera-hello``

- 舵机不运动

  1. 检查电源连接：舵机需要 5V 电源
  2. 验证舵机通道是否与代码匹配（通道 2 和 3）
  3. 使用简单的角度命令独立测试舵机

- AI 无响应或报错

  1. 验证 ``secret.py``\ 中的 API 密钥正确
  2. 检查网络连接：\ ``ping 8.8.8.8``
  3. 确保 OpenAI 账户有余额
  4. 验证模型 "gpt-4o" 在你的账户中可用

- 舵机动作不正确

  1. 检查 pan 和 tilt 舵机是否接反
  2. 调整 ``nod_head()``\ 和 ``shake_head()``\ 函数中的角度值
  3. 验证舵机中心位置（可能需要校准）

- 图像模糊或过暗

  1. 确保作业上的光线充足
  2. 如果可调，调整摄像头焦距
  3. 将摄像头放置在距离纸张 15-30cm 处
  4. 使用高对比度的笔/记号笔书写

- 按钮无响应

  1. 按下时检查用户按钮 LED 是否亮起
  2. 验证按钮回调是否已注册
  3. 使用简单的打印语句测试按钮

- AI 返回意外回复

  1. 检查代码中的提示词格式
  2. 确保图像清晰显示题目和答案
  3. 先测试非常简单的算术题

----------------------------------------------


这个作业批改演示展示了 AI 视觉模型如何与物理硬件交互，创造出引人入胜的教育体验，将数字智能与有形的反馈机制融为一体！
