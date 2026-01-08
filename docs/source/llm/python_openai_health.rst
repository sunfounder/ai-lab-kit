.. _py_ai_health_assistant:

(Example) AI Health Assistant with Temperature Monitoring
=========================================================

**Introduction**

This project creates an intelligent **AI Health Assistant** that combines body temperature sensing with voice interaction to provide personalized health assessments. The system integrates:

1. **Thermistor-based Temperature Sensing** for accurate body temperature measurement
2. **Speech Recognition** for understanding user symptoms and queries
3. **AI-Powered Health Analysis** using OpenAI GPT for medical assessment
4. **Text-to-Speech Feedback** providing audible health recommendations
5. **Real-time Monitoring** with continuous temperature conversion

The health assistant measures body temperature through a thermistor circuit, analyzes the reading with AI, and provides appropriate health advice based on established medical temperature ranges.


* :ref:`py_online_llm` 
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**What You'll Need**

The following components are required for this project:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_thermistor`
        - |link_thermistor_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy| (10kΩ)
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Wiring Diagram**

Connect the components to the Fusion HAT+ as follows:

.. image:: img/fzz/health_assistant_bb.png
   :width: 80%
   :align: center

**Thermistor Circuit:**

- Connect thermistor and 10kΩ resistor in series between 3.3V and GND
- Connect the middle point (voltage divider) to ADC Channel 3 (A3)
- **Thermistor Pinout:**

  - One leg → 3.3V
  - Other leg → ADC A3 AND to 10kΩ resistor
  - Other end of 10kΩ resistor → GND



*Note: The thermistor uses a voltage divider circuit. Ensure the 10kΩ resistor matches the thermistor's nominal resistance at 25°C.*

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
      sudo python3 llm_openai_health.py

----------------------------------------------

**Code**

Here is the full Python script for the AI Health Assistant:

.. code-block:: python
   :linenos:
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   import time
   from fusion_hat.stt import STT
   from fusion_hat.adc import ADC
   import math
   from fusion_hat.tts import Pico2Wave
   
   # Setup Text-to-Speech and Speech-to-Text
   tts = Pico2Wave()
   tts.set_lang('en-US')
   stt = STT(language="en-us")
   
   # Register OpenAI API
   # openai.com
   
   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
   
   # Setup ADC for thermistor reading on channel A3
   thermistor = ADC('A3')
   
   # Setup LLM with health assessment instructions
   INSTRUCTIONS = '''
   You are a health assistant. Your task is to assess the user's body temperature based on the thermistor reading and provide appropriate health advice.
   
   The thermistor reading represents body temperature in Celsius.
   
   ### Input Format:
   "thermistor: [value], message: [user query]"
   
   ### Output Guidelines:
   1. If temperature < 35.0°C, warn about hypothermia and suggest warming up.
   2. If 35.0°C ≤ temperature ≤ 37.5°C, confirm normal temperature and reassure the user.
   3. If 37.5°C < temperature ≤ 38.5°C, indicate mild fever and suggest rest and hydration.
   4. If temperature > 38.5°C, alert about high fever and recommend medical attention.
   5. Include the temperature value in your response to justify your assessment.
   6. Your reply should be brief and concise, no more than two sentences.
   
   ### Example Input:
   thermistor: 39.0, message: I feel unwell.
   
   ### Example Output:
   Your body temperature is 39.0°C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
   '''
   
   WELCOME = "Hello, I am a health assistant. Please hold your thermometer and I will assess your body temperature based on the thermistor reading. If you feel unwell, please provide your symptoms and I will provide appropriate health advice."
   
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
   
   # Function to read and convert thermistor value to temperature
   def temperature():
       while True:
           # Read analog value (0-4095)
           analogVal = thermistor.read()
           
           # Calculate voltage across thermistor
           Vr = 3.3 * float(analogVal) / 4095
           
           # Check for sensor issues
           if 3.3 - Vr < 0.1:
               print("Please check the sensor")
               continue
           
           # Calculate thermistor resistance
           Rt = 10000 * Vr / (3.3 - Vr)
           
           # Convert resistance to temperature using Steinhart-Hart equation
           # B = 3950 (thermistor coefficient), R0 = 10000Ω at 25°C
           temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
           
           # Convert from Kelvin to Celsius
           Cel = temp - 273.15
           
           return Cel
   
   # Main loop for voice interaction
   while True:
       print("Say something")
       
       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")
               
               # Measure temperature and combine with user query
               current_temp = temperature()
               input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"
               
               # Get response from LLM with streaming
               response = llm.prompt(input_text, stream=True)
               
               # Collect the full response
               string = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       string += next_word
               
               # Speak the response
               tts.say(string)
               print("")  # New line after response
               
           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**Running Example**

**Typical Console Output:**

.. code-block:: text

   Hello, I am a health assistant. Please hold your thermometer and I will assess your 
   body temperature based on the thermistor reading. If you feel unwell, please provide 
   your symptoms and I will provide appropriate health advice.
   
   Say something
   partial: I feel
   partial: I feel very
   partial: I feel very warm
   final: I feel very warm and tired
   
   Your body temperature is 38.7°C, which indicates a mild fever. Please rest, stay 
   hydrated, and monitor your symptoms. If the fever persists or worsens, consider 
   seeking medical attention.

**Different Scenarios:**

1. **Normal Temperature (36.5°C):**
   
   .. code-block:: text
   
      User: "How's my temperature?"
      AI: "Your body temperature is 36.5°C, which is within the normal range. You're 
      doing well, but continue to monitor how you feel."

2. **High Fever (39.2°C):**
   
   .. code-block:: text
   
      User: "I have a headache and feel hot"
      AI: "Your body temperature is 39.2°C, indicating a high fever. Please rest 
      immediately, stay hydrated, and consider seeking medical advice as soon as possible."

3. **Low Temperature (34.2°C):**
   
   .. code-block:: text
   
      User: "I feel cold and shivering"
      AI: "Your body temperature is 34.2°C, which is below normal and may indicate 
      hypothermia. Please warm up immediately with blankets and warm drinks."

----------------------------------------------

**Understanding the Code**

1. **Temperature Sensor Initialization**

   The thermistor is connected to ADC channel A3:
   
   .. code-block:: python
   
      thermistor = ADC('A3')
      
   This reads analog values from 0-4095 representing voltage levels.

2. **Steinhart-Hart Temperature Conversion**

   The thermistor uses the Steinhart-Hart equation for accurate temperature calculation:
   
   .. code-block:: python
   
      # Read analog value (0-4095)
      analogVal = thermistor.read()
      
      # Convert to voltage (0-3.3V)
      Vr = 3.3 * float(analogVal) / 4095
      
      # Calculate thermistor resistance using voltage divider formula
      Rt = 10000 * Vr / (3.3 - Vr)
      
      # Steinhart-Hart equation: 1/T = 1/T0 + 1/B * ln(R/R0)
      temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
      
      # Convert Kelvin to Celsius
      Cel = temp - 273.15

3. **Sensor Error Checking**

   The code includes basic error detection:
   
   .. code-block:: python
   
      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue
      
   This detects if the thermistor is disconnected or shorted.

4. **Speech Recognition Setup**

   Both STT and TTS are configured for English:
   
   .. code-block:: python
   
      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. **Contextual Input Construction**

   Temperature data is combined with user query:
   
   .. code-block:: python
   
      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"
      
   Format: ``"thermistor: 37.2, message: I feel dizzy"``

6. **Medical Classification Logic**

   The AI instructions define temperature ranges:
   
   .. code-block:: python
   
      # Temperature ranges for medical assessment:
      # < 35.0°C: Hypothermia warning
      # 35.0-37.5°C: Normal range
      # 37.5-38.5°C: Mild fever
      # > 38.5°C: High fever

7. **Real-time Speech Processing**

   The system shows partial recognition results:
   
   .. code-block:: python
   
      for result in stt.listen(stream=True):
          if result["done"]:
              # Final recognition
              print(f"final: {result['final']}")
          else:
              # Partial recognition
              print(f"partial: {result['partial']}", end="", flush=True)

8. **Streaming AI Response**

   AI response is streamed and spoken simultaneously:
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      string = ""
      
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word
      
      tts.say(string)  # Speak complete response

9. **Temperature Formatting**

   Temperature is formatted to one decimal place:
   
   .. code-block:: python
   
      f"thermistor: {current_temp:.1f}"
      
   This ensures consistent precision (e.g., 36.5°C instead of 36.512345°C).

10. **Clear Console Display**

    Uses ANSI escape codes for clean output:
    
    .. code-block:: python
    
        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
        
    - ``\r``: Return to start of line
    - ``\x1b[K``: Clear to end of line
    - Prevents overlapping text during streaming

----------------------------------------------

**Temperature Ranges and Medical Significance**

**Normal Body Temperature Ranges:**

- **Oral:** 36.5-37.5°C (97.7-99.5°F)
- **Rectal:** 37.0-38.0°C (98.6-100.4°F)
- **Axillary (armpit):** 35.5-37.0°C (95.9-98.6°F)
- **Ear:** 35.8-38.0°C (96.4-100.4°F)

**Fever Classification:**

- **Low-grade fever:** 37.5-38.3°C (99.5-100.9°F)
- **Moderate fever:** 38.4-39.4°C (101.1-102.9°F)
- **High fever:** 39.5-40.0°C (103.1-104.0°F)
- **Hyperpyrexia:** > 40.0°C (> 104.0°F) - Medical emergency

**Hypothermia Classification:**

- **Mild:** 32-35°C (89.6-95.0°F)
- **Moderate:** 28-32°C (82.4-89.6°F)
- **Severe:** < 28°C (< 82.4°F) - Life-threatening

----------------------------------------------

**How It Works - Step by Step**

1. **Initialization:**

   - System prints welcome message
   - Thermistor circuit is ready
   - Speech recognition is active

2. **User Interaction:**

   - User speaks symptoms: "I feel feverish and have a headache"
   - System shows partial recognition as user speaks
   - Final text is captured when user stops speaking

3. **Temperature Measurement:**

   - Thermistor circuit measures resistance
   - ADC converts to digital value (0-4095)
   - Steinhart-Hart equation converts to Celsius
   - Temperature formatted to one decimal place

4. **AI Processing:**

   - Temperature and query combined: "thermistor: 38.7, message: I feel feverish..."
   - Sent to OpenAI GPT with medical instructions
   - AI classifies temperature range
   - Generates appropriate health advice

5. **Response Delivery:**

   - AI response streams to console
   - Text-to-speech converts to audio
   - User hears spoken health recommendations

6. **Continuous Operation:**

   - System returns to listening mode
   - Ready for next health assessment
   - Maintains conversation history (20 messages)

----------------------------------------------

**Thermistor Calibration**

For accurate readings, calibrate your thermistor:

1. **Calculate Actual Beta Value:**
   
   .. code-block:: python
   
      # Measure resistance at two known temperatures
      # R1 at T1, R2 at T2
      # B = ln(R1/R2) / (1/T1 - 1/T2)
      
      # Example: 10kΩ at 25°C, 3.5kΩ at 50°C
      B = math.log(10000/3500) / (1/(273+25) - 1/(273+50))

2. **Add Calibration Offset:**
   
   .. code-block:: python
   
      # If readings are consistently off by 0.5°C
      Cel = temp - 273.15 + 0.5  # Add calibration offset

3. **Multi-point Calibration:**

   - Measure at ice water (0°C)
   - Measure at room temperature (known)
   - Measure at body temperature (medical thermometer)
   - Create lookup table or linear correction

----------------------------------------------

**Troubleshooting**

- **"Temperature readings inaccurate"**

  - Check thermistor wiring: proper voltage divider configuration
  - Verify resistor value: should match thermistor's nominal resistance
  - Calibrate with known temperature source
  - Check ADC reference voltage (should be 3.3V stable)

- **"No speech recognition"**

  - Test microphone: ``arecord --duration=3 test.wav && aplay test.wav``
  - Check audio device selection in STT initialization
  - Ensure background noise is minimal
  - Speak clearly and at moderate pace

- **"AI not responding"**

  - Check internet connection
  - Verify OpenAI API key in ``secret.py``
  - Ensure billing is enabled on OpenAI account
  - Check if API rate limits are exceeded

- **"Temperature jumps erratically"**

  - Add software filtering: moving average of readings
  - Check for loose connections
  - Add capacitor (0.1µF) across thermistor for noise reduction
  - Ensure thermistor is making good thermal contact

- **"Text-to-speech not working"**

  - Test audio output: ``speaker-test -t sine -f 440``
  - Verify language setting: ``tts.set_lang('en-US')``
  - Check volume: ``alsamixer``
  - Re-execute the audio setup script: ``sudo /opt/setup_fusion_hat_audio.sh``

- **"Sensor reading shows 0 or 4095"**

  - Check wiring: thermistor may be shorted (0) or open (4095)
  - Verify voltage divider calculation
  - Test ADC with known voltage source
  - Check ADC channel (should be A3)

- **"Response too slow"**

  - Reduce streaming complexity
  - Pre-measure temperature before speech ends
  - Implement local temperature assessment as fallback
  - Check network latency

- **"Medical advice seems generic"**

  - Enhance AI instructions with more specific guidance
  - Include common symptoms and responses
  - Add follow-up question capability
  - Implement severity scoring system

----------------------------------------------

**Safety and Medical Disclaimer**

.. warning:: This project is for educational and demonstration purposes only. It is NOT a medical device and should NOT be used for actual medical diagnosis or treatment.

**Critical Safety Guidelines:**

1. **NOT FOR MEDICAL USE:** Do not rely on this system for health decisions
2. **EMERGENCY SITUATIONS:** Always seek professional medical help for serious symptoms
3. **ACCURACY LIMITS:** Thermistor accuracy is limited compared to medical thermometers
4. **CALIBRATION REQUIRED:** Regular calibration against medical thermometers is essential
5. **SUPERVISION NEEDED:** Use under adult supervision if intended for educational purposes

**When to Seek Medical Attention:**

- Temperature > 39.5°C (103.1°F) in adults
- Temperature > 38.0°C (100.4°F) in infants under 3 months
- Fever lasting more than 3 days
- Difficulty breathing or chest pain
- Severe headache or stiff neck
- Confusion or seizures

----------------------------------------------

**Try It Yourself**

1. **Multiple Vital Signs**  

   Add heart rate sensor (pulse oximeter) and blood pressure monitor.

2. **Symptom Checker**  

   Expand to full symptom assessment with decision tree logic.

3. **Medical History Integration**  

   Store user medical history for personalized recommendations.

4. **Medication Reminder**  

   Add medication scheduling and reminder system.

5. **Telemedicine Integration**  

   Connect to telemedicine platforms for remote consultations.

6. **Emergency Alert System**  

   Automatically alert emergency contacts for critical readings.

7. **Multi-user Profiles**  

   Support multiple family members with individual profiles.

8. **Health Trend Analysis**  

   Track temperature over time and identify patterns.

9. **Environmental Monitoring**  

   Add room temperature and humidity sensors for context.

10. **Nutrition Advisor**  

   Provide dietary recommendations based on health status.

11. **Exercise Recommendations**  

   Suggest appropriate physical activity based on health metrics.

12. **Sleep Monitoring**  

   Integrate sleep tracking with temperature correlation.

13. **Allergy Tracker**  

   Monitor symptoms and identify potential allergens.

14. **Vaccination Reminder**  

   Track vaccination schedules and send reminders.

15. **First Aid Guide**  

   Provide step-by-step first aid instructions.

16. **Mental Health Assessment**  

   Include mood tracking and mental wellness recommendations.

17. **Chronic Condition Management**  

   Specialized tracking for diabetes, hypertension, etc.

18. **Medical Dictionary**  

   Explain medical terms and conditions in simple language.

19. **Health Goal Setting**  

   Help users set and track health improvement goals.

20. **Integration with Wearables**  

   Connect to smartwatches and fitness trackers for comprehensive data.

This AI Health Assistant demonstrates how sensor technology, voice interaction, and artificial intelligence can work together to create accessible health monitoring tools, while emphasizing the importance of professional medical consultation for serious health concerns!