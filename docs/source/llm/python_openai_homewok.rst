.. _py_homework_grading_demo:

(Example) Homework Grading Demo with Pan-Tilt Camera
=====================================================

**Introduction**

This project creates an interactive **AI Homework Grading Assistant** that combines computer vision, artificial intelligence, and robotics. The system:

1. **Captures photos** of handwritten or printed homework questions using a Raspberry Pi camera
2. **Analyzes content** using OpenAI's GPT-4 Vision model to determine if answers are correct
3. **Provides physical feedback** through servo-controlled pan-tilt head movements:

   - *Nods* for correct answers
   - *Shakes* for incorrect answers
   
4. **Uses simple interaction** triggered by a single button press

This demonstration showcases how AI can interact with the physical world, creating an engaging educational tool that provides immediate visual feedback on homework accuracy.

You can use other LLM modules and hardware components to build your own AI-assisted learning devices. See:

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**What You'll Need**

The following components are required for this project:

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
        - |link_camera_module_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-
    *   - Homework sample (printed or handwritten)
        - \-

----------------------------------------------

**Hardware Setup**

Assemble the pan-tilt module, camera module, and servo module as shown in :ref:`assemble_fusion_hat_pan_tilt` .

- **Pan Servo (Horizontal):** Channel 2 on Fusion HAT+

   - Signal (yellow/orange) → PWM output
   - Power (red) → 5V
   - Ground (brown/black) → GND

- **Tilt Servo (Vertical):** Channel 3 on Fusion HAT+

   - Signal (yellow/orange) → PWM output
   - Power (red) → 5V
   - Ground (brown/black) → GND

----------------------------------------------


**Get and Save your API Key**

#. Go to |link_openai_platform| and log in. On the **API keys** page, click **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Fill in the details (Owner, Name, Project, and permissions if needed), then click **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Once the key is created, copy it right away — you won't be able to see it again. If you lose it, you'll need to generate a new one.

   .. image:: img/llm_openai_copy.png

#. In your project folder (for example: ``/``), create a file called ``secret.py``:

   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Paste your key into the file like this:

   .. code-block:: python
   
       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Enable billing and check models**

#. Before using the key, go to the **Billing** page in your OpenAI account, add your payment details, and top up a small amount of credits.  

   .. image:: img/llm_openai_billing.png

#. Then go to the **Limits** page to check which models are available for your account and copy the exact model ID to use in your code.  

   .. image:: img/llm_openai_models.png

----------------------------------------------

**Running the Code**

#. **Create Homework Sample:**

   - Write or print a simple math problem with answer
   - Example: "5 + 3 = 8" (correct) or "5 + 3 = 7" (incorrect)
   - Ensure clear handwriting or printing

#. **Run the Program:**
   
   .. code-block:: bash
   
      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. **Follow On-Screen Instructions:**

   - Position homework under camera
   - Press User Button (USR) on Fusion HAT+
   - Watch for servo response

#. **Expected Output:**
   
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

**Code**

Here is the full Python script for the Homework Grading Demo:

.. code-block:: python
   :linenos:
   
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

**Understanding the Code**

1. **LLM Configuration and Setup**

   The system uses OpenAI's GPT-4o with Vision capabilities to analyze images:
   
   .. code-block:: python
   
      # Import and initialize the LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")
      
      # Set specific instructions for consistent responses
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)
      
      # Limit conversation history to manage tokens
      llm.set_max_messages(5)

2. **Hardware Initialization**

   Three hardware components are initialized: servos, camera, and button:
   
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

3. **Servo Animation Functions**

   Natural-looking movements for nodding and shaking:
   
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

4. **Image Capture and AI Analysis**

   The main grading workflow:
   
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

5. **Button Event Handling**

   Simple callback system for user interaction:
   
   .. code-block:: python
   
      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()
      
      # Assign callback to button
      user_button.set_on_click(on_button_click)

6. **Main Application Loop**

   Minimal main loop that waits for button presses:
   
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

7. **Resource Cleanup**

   Proper shutdown procedure:
   
   .. code-block:: python
   
      def cleanup():
          # Return servos to neutral position
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)
          
          # Stop camera
          camera.stop()

----------------------------------------------

**Troubleshooting**

- **"No module named 'picamera2'"**

  Install the required library:
  
  .. code-block:: bash
     
     sudo apt update
     sudo apt install python3-picamera2

- **"Camera not detected"**

  1. Check camera connection: ensure ribbon cable is inserted correctly
  2. Verify camera is enabled: ``sudo raspi-config`` → Interface Options → Camera
  3. Test camera independently: ``libcamera-hello``

- **"Servos not moving"**

  1. Check power connections: servos need 5V power
  2. Verify servo channels match code (Channels 2 and 3)
  3. Test servos independently with simple angle commands

- **"AI not responding or error"**

  1. Verify API key in ``secret.py`` is correct
  2. Check internet connection: ``ping 8.8.8.8``
  3. Ensure you have credits in your OpenAI account
  4. Verify model "gpt-4o" is available in your account

- **"Incorrect servo movements"**

  1. Check if pan and tilt servos are swapped
  2. Adjust angle values in ``nod_head()`` and ``shake_head()`` functions
  3. Verify servo center positions (may need calibration)

- **"Image too blurry or dark"**

  1. Ensure adequate lighting on homework
  2. Adjust camera focus if adjustable
  3. Position camera 15-30cm from paper
  4. Use high-contrast pen/marker for handwriting

- **"Button not responding"**

  1. Check if User Button LED lights when pressed
  2. Verify button callback is registered
  3. Test button with simple print statement

- **"AI returns unexpected response"**

  1. Check prompt formatting in code
  2. Ensure image clearly shows question AND answer
  3. Test with very simple arithmetic problems first

----------------------------------------------

**Try It Yourself**

1. **Multiple Choice Grading**  

   Extend to grade multiple choice questions with A/B/C/D options.

2. **Voice Feedback**  

   Add text-to-speech to announce "Correct!" or "Try again!" 

3. **Score Tracking**  

   Keep track of correct/incorrect answers and display score on LED matrix.

4. **Subject Specialization**  

   Create different modes for math, science, language arts with specialized prompts.

5. **Step-by-Step Evaluation**  

   Ask AI to identify which step in a multi-step problem contains the error.

6. **Handwriting Improvement**  

   Use AI to give feedback on handwriting legibility.

7. **Multiple Languages**  

   Support grading homework in different languages.

8. **Timer Mode**  

   Add timed tests with automatic grading at the end.

9. **Progress Reports**  

   Generate weekly progress reports based on grading history.

10. **Peer Comparison**  

   Anonymously compare performance with class averages (simulated).

11. **Adaptive Difficulty**  

   Adjust question difficulty based on student performance.

12. **Emotional Recognition**  

   Add emotion detection to provide encouragement when frustrated.

13. **AR Overlays**  

   Use augmented reality to show corrections directly on the homework.

14. **Parent Notifications**  

   Send email summaries to parents with performance metrics.

15. **Study Recommendations**  

   Suggest specific topics to study based on incorrect answers.

16. **Group Competition**  

   Multi-station setup for classroom competitions.

17. **Accessibility Features**  

   Audio descriptions for visually impaired students.

18. **Historical Analysis**  

   Track improvement over time with graphs and statistics.

19. **Cross-Subject Integration**  

   Connect math problems to real-world science applications.

20. **Gamification**  

   Add points, badges, and achievements for learning milestones.

This homework grading demo showcases how AI vision models can interact with physical hardware to create engaging educational experiences, blending digital intelligence with tangible feedback mechanisms!