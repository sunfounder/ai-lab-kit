.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

(Example) パン・チルトカメラ付き 宿題採点デモ
=====================================================

**はじめに**

このプロジェクトでは、コンピュータビジョン、人工知能、ロボティクスを組み合わせた対話型の **AI 宿題採点アシスタント** を作成します。システムは次のことを行います：

1. Raspberry Pi カメラで、手書きまたは印刷された宿題の問題を **撮影** します
2. OpenAI の GPT-4 Vision モデルで内容を **解析** し、解答が正しいかを判定します
3. サーボ制御のパン・チルトヘッド動作で **物理的なフィードバック** を返します：

   - 正解なら *うなずく*
   - 不正解なら *首を振る*
   
4. 1 回のボタン押下で動作する **シンプルなインタラクション** を採用しています

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

このデモは、AI が物理世界と連携できることを示す例であり、宿題の正誤をその場で視覚的にフィードバックする、学習向けの魅力的なツールになります。

他の LLM モジュールやハードウェア部品を組み合わせて、独自の AI 支援学習デバイスを作ることもできます。以下も参照してください：

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**必要なもの**

このプロジェクトに必要な部品は以下の通りです：

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_servo`
        - |link_servo_buy|
    *   - Pan-Tilt
        - 
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-
    *   - Homework sample (printed or handwritten)
        - \-

----------------------------------------------

**ハードウェアのセットアップ**

カメラモジュールを便利に使うために、:ref:`assemble_fusion_hat_pan_tilt` の組み立てを推奨します。

   .. note:: 
     
     パン・チルトを組み立てると一部のピンが隠れる場合があります。そのため、カメラを使用するときだけ組み立てるか、組み立て後に外側へ配置することを推奨します。
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**コードの実行**

#. 宿題サンプルを用意する：

   - 簡単な算数問題と答えを手書き、または印刷します
   - 例："5 + 3 = 8"（正解）または "5 + 3 = 7"（不正解）
   - 文字が読み取れるよう、はっきり書く／印刷してください

#. プログラムを実行する：
   
   .. code-block:: bash
   
      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. 画面の指示に従う：

   - 宿題用紙をカメラの下に置く
   - Fusion HAT+ の User Button（USR）を押す
   - サーボの反応を確認する

#. 想定される出力：
   
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

**コード**

以下は宿題採点デモの Python スクリプト全体です：


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

**コードの理解**

1. LLM の設定とセットアップ

   システムは Vision 機能を備えた OpenAI の GPT-4o を使用して画像を解析します：
   
   .. code-block:: python
   
      # Import and initialize the LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")
      
      # Set specific instructions for consistent responses
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)
      
      # Limit conversation history to manage tokens
      llm.set_max_messages(5)

2. ハードウェアの初期化

   3 つのハードウェア要素（サーボ、カメラ、ボタン）を初期化します：
   
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

3. サーボのアニメーション関数

   うなずき／首振りを自然に見せる動きです：
   
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

4. 画像撮影と AI 解析

   採点のメインワークフロー：
   
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

5. ボタンイベントの処理

   ユーザー操作はコールバックで完結します：
   
   .. code-block:: python
   
      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()
      
      # Assign callback to button
      user_button.set_on_click(on_button_click)

6. メインループ

   ボタン押下を待つだけの最小構成です：
   
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

7. リソースのクリーンアップ

   終了時にサーボとカメラを安全に停止します：
   
   .. code-block:: python
   
      def cleanup():
          # Return servos to neutral position
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)
          
          # Stop camera
          camera.stop()

----------------------------------------------

**トラブルシューティング**

- No module named ``picamera2``

  必要なライブラリをインストールしてください：
  
  .. code-block:: bash
     
     sudo apt update
     sudo apt install python3-picamera2

- Camera not detected

  1. カメラの接続を確認：フラットケーブルが正しい向きで確実に挿入されているか
  2. カメラが有効か確認： ``sudo raspi-config`` → Interface Options → Camera
  3. カメラ単体テスト： ``libcamera-hello``

- Servos not moving

  1. 電源接続を確認：サーボには 5V 電源が必要です
  2. サーボのチャンネルがコードと一致しているか確認（Channels 2 と 3）
  3. 単体テスト：角度指定でサーボが動くか確認してください

- AI not responding or error

  1. ``secret.py`` の API キーが正しいか確認してください
  2. ネット接続を確認： ``ping 8.8.8.8``
  3. OpenAI アカウントにクレジットがあるか確認してください
  4. モデル "gpt-4o" が利用可能か確認してください

- Incorrect servo movements

  1. pan と tilt のサーボが入れ替わっていないか確認してください
  2. ``nod_head()`` と ``shake_head()`` の角度値を調整してください
  3. センター位置のキャリブレーションが必要な場合があります

- Image too blurry or dark

  1. 宿題用紙に十分な照明を当ててください
  2. 調整可能な場合はフォーカスを調整してください
  3. 用紙から 15〜30cm 程度の距離にカメラを配置してください
  4. 手書きは濃いペン／マーカーで書くと読み取りやすくなります

- Button not responding

  1. ボタン押下時に User Button の LED が点灯するか確認してください
  2. コールバックが登録されているか確認してください
  3. 簡単な print を入れて押下検出を確認してください

- AI returns unexpected response

  1. コード内の prompt の書式を確認してください
  2. 画像に「問題」と「答え」の両方がはっきり写っているか確認してください
  3. まずは簡単な四則演算でテストしてください

----------------------------------------------


この宿題採点デモは、AI のビジョンモデルが物理ハードウェアと連携して学習体験を拡張できることを示します。デジタルな知能と手触りのあるフィードバックを融合し、教育用途に魅力的な体験を提供します。