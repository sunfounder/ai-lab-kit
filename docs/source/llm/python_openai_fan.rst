.. _py_voice_controlled_fan:

(Example) Voice-Controlled Smart Fan
====================================

**Introduction**

This project creates an intelligent **Voice-Controlled Smart Fan** that combines speech recognition, AI processing, and motor control. The system allows users to control fan speed using natural voice commands and provides multiple control methods:

1. **Voice Commands** using speech-to-text for hands-free operation
2. **Physical Button** for manual speed adjustment
3. **AI Interpretation** using OpenAI's GPT to understand natural language
4. **Auditory Feedback** with a buzzer for button presses
5. **Dual Control Interface** supporting both voice and physical interaction

The smart fan understands commands like "make it faster," "slow down please," or "turn off the fan" and responds with appropriate actions and verbal confirmation.

You can combine various input and output modules to create voice-controlled smart devices. See:

* :ref:`py_online_llm` 
* :ref:`py_stt_whisper`
* :ref:`py_motor`

----------------------------------------------

**What You'll Need**

The following components are required for this project:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_motor`
        - |link_motor_buy|
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_buzzer`
        - \-
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Wiring Diagram**

Connect the components to the Fusion HAT+ as follows:

.. image:: img/fzz/llm_fan_bb.png
   :width: 80%
   :align: center

**Component Connections:**

- **Motor:**

  - Connect to Motor Port M0

- **Button:**

  - Connect between GPIO 17 and 3.3V (pull-up configuration)
  - Other side to Ground

- **Buzzer:**

  - Positive leg to GPIO 4
  - Negative leg to Ground

----------------------------------------------
.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Run the Code**
   
   .. raw:: html
   
      <run></run>
   
   .. code-block:: shell

      cd ~/ai-lab-kit/llm   
      sudo python3 llm_openai_fan.py

----------------------------------------------

**Code**

Here is the full Python script for the Voice-Controlled Smart Fan:

.. code-block:: python
   :linenos:
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.motor import Motor
   from fusion_hat.modules import Buzzer
   from fusion_hat.pin import Pin
   import random, time
   from fusion_hat.stt import STT
   
   # Initialize Speech-to-Text with English language
   stt = STT(language="en-us")
   
   # Initialize motor on port M0
   motor = Motor('M0')
   
   # Initialize button on GPIO 17 with pull-up and debounce
   button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
   
   # Initialize buzzer on GPIO 4
   buzzer = Buzzer(Pin(4))
   
   # Global speed variable (0-100%)
   speed = 0
   
   # Function for auditory feedback
   def beep():
       buzzer.on()
       time.sleep(0.1)
       buzzer.off()
   
   # Debounce variables for button
   last_triggered = 0 
   
   # Button callback function
   def speed_up():
       global speed, last_triggered
       
       # Debounce: ignore if pressed within 500ms
       if time.time() - last_triggered < 0.5:
           return
       
       last_triggered = time.time()
       
       # Increase speed by 10%
       speed += 10
       
       # Wrap around at 100% (go back to 0)
       if speed > 100:
           motor.stop()
           speed = 0
       else:
           motor.power(speed)
       
       # Auditory feedback
       beep()
       
       # Print current speed
       print(f"Speed set to: {speed}%")
   
   # Attach callback to button
   button.when_activated = speed_up
   
   # Function to parse natural language response and set appropriate speed
   def parse_response_for_speed(text_response):
       """
       Parse the LLM's natural language response to determine speed setting.
       Looks for keywords related to different speed levels.
       Returns the speed level to set (100, 50, 25, or 0)
       """
       text_lower = text_response.lower()
       
       # Check for "stop" or "off" keywords - highest priority
       if any(word in text_lower for word in ['stop', 'off', 'zero', '0%', 'turn off', 'shut off', 'halt']):
           return 0
       
       # Check for "slow" or "low" keywords
       if any(word in text_lower for word in ['slow', 'low', '25%', 'quarter', 'minimum', 'gentle']):
           return 25
       
       # Check for "medium" or "half" keywords
       if any(word in text_lower for word in ['medium', 'half', '50%', 'moderate', 'normal']):
           return 50
       
       # Check for "fast" or "high" or "full" keywords
       if any(word in text_lower for word in ['fast', 'high', 'full', '100%', 'maximum', 'top']):
           return 100
       
       # If no specific keywords found, return -1 to indicate no speed change
       return -1
   
   # Setup LLM with specific instructions for fan control
   INSTRUCTIONS = '''
   You are a fan control assistant. Your task is to interpret the user's speech input and respond with natural language.
   
   ### Input Format:
   The user will speak their command for fan control.
   
   ### CRITICAL RULES:
   1. **BE DECISIVE**: Always take clear action based on user requests. Do NOT ask follow-up questions.
   2. **NO CLARIFICATION QUESTIONS**: Never ask "Would you like me to..." or "Should I..." questions.
   3. **ASSUME INTENT**: If the user's request is ambiguous, make a reasonable assumption and take action.
   4. **CONFIRM ACTION**: Always state what action you are taking in your response.
   
   ### Response Guidelines:
   1. Respond naturally and conversationally to the user's request.
   2. Acknowledge what the user asked for.
   3. Use clear language about what action you're taking.
   4. Use keywords in your response that indicate speed levels:
      - For maximum speed: use words like "fast", "high", "full speed", "maximum"
      - For medium speed: use words like "medium", "half speed", "50%"
      - For low speed: use words like "slow", "low", "quarter speed", "25%"
      - For stopping: use words like "stop", "off", "zero", "turning off"
   5. If the user asks about current status, respond with helpful information.
   
   ### Example Responses:
   
   **When asked to go fast:**
   "I'll set the fan to maximum speed for you. Full speed activated!"
   
   **When asked to slow down:**
   "Reducing the fan speed to low. Enjoy the gentle breeze."
   
   **When asked for medium speed:**
   "Setting the fan to medium speed. This should be comfortable."
   
   **When asked to stop:**
   "Stopping the fan now. The motor is turned off."
   
   **When asked about status:**
   "Your fan is currently at 50% speed. Would you like me to adjust it?"
   
   '''
   
   WELCOME = "Hello, I am a fan control assistant. You can ask me to set the fan to fast, medium, slow, or stop it completely. You can also press the button to increase the speed by 10% or decrease it by 10%. If you ask about the current status, I will tell you the current speed. If you don't know what to do, you can ask me for instructions. Good luck!"
   
   # Initialize OpenAI LLM
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o",
   )
   
   # Set how many messages to keep
   llm.set_max_messages(20)
   
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   
   # Set welcome message
   llm.set_welcome(WELCOME)
   
   print(WELCOME)
   
   # Main loop for voice control
   while True:
       print("Say something")
       
       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")
               
               # Get the recognized speech
               input_text = result['final']
               
               # Add current speed context to the input
               contextual_input = f"Current speed is {speed}%. User says: {input_text}"
               
               # Get response from LLM
               response = llm.prompt(contextual_input, stream=True)
               
               # Collect the full response
               full_response = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       full_response += next_word
               
               print("\n")  # Add newline after response
               
               # Parse the response to determine speed setting
               new_speed = parse_response_for_speed(full_response)
               
               # Apply speed change if detected
               if new_speed >= 0:
                   speed = new_speed
                   motor.power(speed)
                   print(f"Speed set to: {speed}%")
               else:
                   print("No speed change detected in response")
                   
           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**Understanding the Code**

1. **Speech-to-Text Initialization**

   The system uses STT (Speech-to-Text) for voice recognition:
   
   .. code-block:: python
   
      stt = STT(language="en-us")
      
      for result in stt.listen(stream=True):
          if result["done"]:
              input_text = result['final']
          else:
              print(f"partial: {result['partial']}")

   This provides real-time speech recognition with partial results as you speak.

2. **Motor Control Setup**

   The fan motor is controlled via PWM on port M0:
   
   .. code-block:: python
   
      motor = Motor('M0')
      
      # Set speed as percentage (0-100)
      motor.power(speed)
      
      # Stop the motor completely
      motor.stop()

3. **Button with Debounce**

   The button includes debounce to prevent multiple triggers:
   
   .. code-block:: python
   
      button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      last_triggered = 0
      
      def speed_up():
          global speed, last_triggered
          if time.time() - last_triggered < 0.5:  # 500ms debounce
              return
          last_triggered = time.time()

4. **Auditory Feedback**

   A buzzer provides audible confirmation:
   
   .. code-block:: python
   
      buzzer = Buzzer(Pin(4))
      
      def beep():
          buzzer.on()
          time.sleep(0.1)
          buzzer.off()

5. **Keyword Parsing Function**

   The system parses AI responses for speed commands:
   
   .. code-block:: python
   
      def parse_response_for_speed(text_response):
          text_lower = text_response.lower()
          
          # Check for "stop" or "off" keywords
          if any(word in text_lower for word in ['stop', 'off', 'zero']):
              return 0
          
          # Check for "slow" or "low" keywords
          if any(word in text_lower for word in ['slow', 'low', '25%']):
              return 25
          
          # Similar checks for medium and fast
          
          return -1  # No speed change

6. **Contextual Input to AI**

   The current speed is included in the prompt for context-aware responses:
   
   .. code-block:: python
   
      contextual_input = f"Current speed is {speed}%. User says: {input_text}"
      response = llm.prompt(contextual_input, stream=True)

7. **Streaming Response Processing**

   AI responses are processed word-by-word:
   
   .. code-block:: python
   
      full_response = ""
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              full_response += next_word

8. **Dual Control Logic**

   The system supports both voice and button control:
   
   .. code-block:: python
   
      # Voice control in main loop
      new_speed = parse_response_for_speed(full_response)
      if new_speed >= 0:
          speed = new_speed
          motor.power(speed)
      
      # Button control via callback
      def speed_up():
          speed += 10
          if speed > 100:
              speed = 0
          motor.power(speed)

9. **Clear Terminal Output**

   Uses ANSI escape codes for clean console display:
   
   .. code-block:: python
   
      print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
      
   - ``\r``: Carriage return (go to start of line)
   - ``\x1b[K``: Clear from cursor to end of line
   - ``end=""``: No newline
   - ``flush=True``: Immediate display

10. **Intelligent AI Instructions**

    The AI is specifically instructed to be decisive and avoid clarification questions:
    
    .. code-block:: python
    
        INSTRUCTIONS = '''
        CRITICAL RULES:
        1. BE DECISIVE: Always take clear action based on user requests.
        2. NO CLARIFICATION QUESTIONS: Never ask "Would you like me to..." questions.
        3. ASSUME INTENT: If ambiguous, make reasonable assumption and take action.
        4. CONFIRM ACTION: Always state what action you are taking.
        '''

----------------------------------------------

**Control Methods**

**Voice Commands:**

- "Make it faster" / "Increase speed" → Sets to maximum (100%)
- "Slow down" / "Reduce speed" → Sets to low (25%)
- "Medium speed please" → Sets to medium (50%)
- "Turn off" / "Stop" → Stops motor (0%)
- "What's the current speed?" → Reports current speed
- "Make it cooler" → Interprets as request for higher speed

**Button Control:**

- Each press increases speed by 10%
- At 100%, next press cycles back to 0%
- Audible beep confirms each press
- Visual speed percentage displayed

**Natural Language Understanding:**

The AI understands variations like:
- "I'm feeling hot, can you make it faster?"
- "Could you please turn the fan down a bit?"
- "It's too windy in here!"
- "Set it to half speed"

----------------------------------------------

**Troubleshooting**


- **"Motor not spinning"**

  - Verify motor connections: M0 port, correct polarity
  - Test motor directly: ``motor.power(50)`` should spin at 50%
  - Ensure speed variable is being set (0-100 range)

- **"Button not responding"**

  - Check wiring: GPIO 17 to button, other side to 3.3V
  - Verify pull-up configuration
  - Test with simple script: print when button state changes
  - Check debounce time (0.5 seconds may be too long)

- **"No buzzer sound"**

  - Test buzzer directly: ``buzzer.on()`` should produce continuous tone
  - Check if buzzer is piezo (needs PWM) or active (works with DC)

- **"AI not understanding commands"**

  - Check API key in ``secret.py``
  - Verify internet connection
  - Examine AI instructions: ensure they're properly formatted
  - Test with simpler commands first

- **"Speed changes unexpectedly"**

  - Check button debounce: may be triggering multiple times
  - Verify keyword parsing: some phrases may trigger unintended speeds
  - Add print statements to trace speed changes

- **"Poor speech recognition accuracy"**

  - Reduce background noise
  - Speak clearly and at moderate pace
  - Consider using external USB microphone for better quality
  - Adjust STT parameters if available

- **"Motor makes noise but doesn't spin"**

  - Check if motor is stuck or blocked
  - Verify power supply voltage matches motor requirements
  - Some motors need capacitor across terminals for smooth operation

----------------------------------------------

**Try It Yourself**

1. **Temperature-Based Control**  

   Add temperature sensor to automatically adjust fan speed based on room temperature.

2. **Schedule Programming**  

   Add time-based scheduling: "Turn on at 3 PM" or "Run for 30 minutes."

3. **Voice Profile Recognition**  

   Implement voice recognition to identify different users with personalized settings.

4. **Oscillation Control**  

   Add servo motor to control fan direction: "Swing left and right."

5. **Energy Monitoring**  

   Add power meter to track electricity usage and provide efficiency suggestions.

6. **Mobile App Integration**  

   Create smartphone app for remote control and monitoring.

7. **Gesture Control**  

   Add camera or IR sensor for hand gesture control.

8. **Natural Wake-up Mode**  

   Gradually increase fan speed in the morning as a gentle alarm.

9. **Sleep Mode**  

   Automatically reduce speed during nighttime hours.

10. **Multiple Fan Zones**  

    Control multiple fans in different rooms with zone-based commands.

11. **Air Quality Integration**  

    Add air quality sensor and adjust fan based on CO2 or particulate levels.

12. **Weather Adaptation**  

    Connect to weather API to adjust based on outdoor temperature and humidity.

13. **Child Lock Feature**  

    Voice recognition to prevent unauthorized speed changes.

14. **Fan Speed Presets**  

    Save custom speed profiles: "Movie mode," "Sleep mode," "Workout mode."

15. **Power Failure Recovery**  

    Remember previous settings and restore after power outage.

16. **Voice Volume Adaptation**  

    Adjust fan speed based on ambient noise level.

17. **Maintenance Alerts**  

    Track motor hours and remind when cleaning or maintenance is due.

18. **Multi-Language Support**  

    Support voice commands in multiple languages.

19. **Voice Effects**  

    Add fun voice effects or celebrity voice modes for responses.

20. **Integration with Smart Home**  

    Connect to Alexa, Google Home, or Home Assistant for unified control.

This voice-controlled fan demonstrates how natural language processing, physical controls, and intelligent systems can create intuitive and accessible smart home devices that respond to human needs and preferences!