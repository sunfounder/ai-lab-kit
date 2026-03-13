.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_voice_controlled_fan:

(Beispiel) Sprachgesteuerter Smart-Ventilator
==================================================

**Einführung**

Dieses Projekt erstellt einen intelligenten **sprachgesteuerten Smart-Ventilator**, der Spracherkennung, AI-Verarbeitung und Motorsteuerung kombiniert. Das System ermöglicht es Benutzern, die Lüftergeschwindigkeit mit natürlichen Sprachbefehlen zu steuern, und bietet mehrere Steuerungsmethoden:

1. **Sprachbefehle** mithilfe von Speech-to-Text für freihändige Bedienung
2. **Physische Taste** zur manuellen Geschwindigkeitsanpassung
3. **AI-Interpretation** mit OpenAI GPT zum Verstehen natürlicher Sprache
4. **Akustisches Feedback** über einen Buzzer bei Tastendruck
5. **Duale Steueroberfläche** mit Unterstützung für Sprach- und physische Bedienung

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Voice_Controlled_Smart_Fan.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Der Smart-Ventilator versteht Befehle wie „mach ihn schneller“, „bitte langsamer“ oder „schalte den Ventilator aus“ und reagiert mit passenden Aktionen sowie einer gesprochenen Bestätigung.

Sie können verschiedene Ein- und Ausgabemodule kombinieren, um sprachgesteuerte Smart-Geräte zu erstellen. Siehe:

* :ref:`py_online_llm` 
* :ref:`py_stt_whisper`
* :ref:`py_motor`

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

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

**Schaltplan**

Verbinden Sie die Komponenten wie folgt mit dem Fusion HAT+:

.. image:: img/fzz/llm_fan_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Beispiel ausführen**


#. Code ausführen

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_fan.py

#. Den Ventilator steuern

   Sie können den Ventilator mit Sprachbefehlen, der Taste oder über natürliche Sprache steuern.

   * Sprachbefehle:

     - „Mach ihn schneller“ / „Geschwindigkeit erhöhen“ → Setzt die Geschwindigkeit auf maximal (100 %)
     - „Langsamer“ / „Geschwindigkeit verringern“ → Setzt die Geschwindigkeit auf niedrig (25 %)
     - „Bitte mittlere Geschwindigkeit“ → Setzt die Geschwindigkeit auf mittel (50 %)
     - „Ausschalten“ / „Stopp“ → Stoppt den Motor (0 %)
     - „Wie hoch ist die aktuelle Geschwindigkeit?“ → Gibt die aktuelle Geschwindigkeit aus
     - „Mach es kühler“ → Wird als Wunsch nach höherer Geschwindigkeit interpretiert

   * Tastensteuerung:

     - Jeder Tastendruck erhöht die Geschwindigkeit um 10 %
     - Bei 100 % springt der nächste Tastendruck wieder auf 0 %
     - Ein akustisches Signal bestätigt jeden Tastendruck
     - Die aktuelle Geschwindigkeit in Prozent wird auf dem Bildschirm angezeigt

   * Verarbeitung natürlicher Sprache:

     Die AI versteht auch Varianten wie:

     - „Mir ist heiß, kannst du ihn schneller machen?“
     - „Könntest du den Ventilator bitte etwas herunterregeln?“
     - „Hier drin ist es zu windig!“
     - „Stell ihn auf halbe Geschwindigkeit“

--------

**Code**

Hier ist das vollständige Python-Skript für den sprachgesteuerten Smart-Ventilator:

.. raw:: html

   <run></run>

.. code-block:: python
   
   
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

**Code verstehen**

1. Initialisierung von Speech-to-Text

   Das System verwendet STT (Speech-to-Text) zur Spracherkennung:
   
   .. code-block:: python
   
      stt = STT(language="en-us")
      
      for result in stt.listen(stream=True):
          if result["done"]:
              input_text = result['final']
          else:
              print(f"partial: {result['partial']}")

   Dadurch wird eine Spracherkennung in Echtzeit mit Teilergebnissen während des Sprechens ermöglicht.

2. Einrichtung der Motorsteuerung

   Der Lüftermotor wird per PWM über Port M0 gesteuert:
   
   .. code-block:: python
   
      motor = Motor('M0')
      
      # Geschwindigkeit als Prozentwert setzen (0-100)
      motor.power(speed)
      
      # Motor vollständig stoppen
      motor.stop()

3. Taster mit Entprellung

   Der Taster verwendet eine Entprellung, um Mehrfachauslösungen zu verhindern:
   
   .. code-block:: python
   
      button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      last_triggered = 0
      
      def speed_up():
          global speed, last_triggered
          if time.time() - last_triggered < 0.5:  # 500 ms Entprellung
              return
          last_triggered = time.time()

4. Akustisches Feedback

   Ein Buzzer gibt eine akustische Bestätigung:
   
   .. code-block:: python
   
      buzzer = Buzzer(Pin(4))
      
      def beep():
          buzzer.on()
          time.sleep(0.1)
          buzzer.off()

5. Funktion zum Parsen von Schlüsselwörtern

   Das System analysiert AI-Antworten auf Geschwindigkeitsbefehle:
   
   .. code-block:: python
   
      def parse_response_for_speed(text_response):
          text_lower = text_response.lower()
          
          # Auf Schlüsselwörter wie "stop" oder "off" prüfen
          if any(word in text_lower for word in ['stop', 'off', 'zero']):
              return 0
          
          # Auf Schlüsselwörter wie "slow" oder "low" prüfen
          if any(word in text_lower for word in ['slow', 'low', '25%']):
              return 25
          
          # Ähnliche Prüfungen für medium und fast
          
          return -1  # Keine Geschwindigkeitsänderung

6. Kontextbezogene Eingabe an die AI

   Die aktuelle Geschwindigkeit wird in den Prompt aufgenommen, damit die AI kontextbezogen reagieren kann:
   
   .. code-block:: python
   
      contextual_input = f"Current speed is {speed}%. User says: {input_text}"
      response = llm.prompt(contextual_input, stream=True)

7. Verarbeitung gestreamter Antworten

   AI-Antworten werden Wort für Wort verarbeitet:
   
   .. code-block:: python
   
      full_response = ""
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              full_response += next_word

8. Doppelte Steuerlogik

   Das System unterstützt sowohl Sprach- als auch Tastensteuerung:
   
   .. code-block:: python
   
      # Sprachsteuerung in der Hauptschleife
      new_speed = parse_response_for_speed(full_response)
      if new_speed >= 0:
          speed = new_speed
          motor.power(speed)
      
      # Tastensteuerung per Callback
      def speed_up():
          speed += 10
          if speed > 100:
              speed = 0
          motor.power(speed)

9. Saubere Terminalausgabe

   Verwendet ANSI-Escape-Codes für eine übersichtliche Konsolenausgabe:
   
   .. code-block:: python
   
      print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
      
   - ``\r``: Wagenrücklauf (zum Zeilenanfang springen)
   - ``\x1b[K``: Vom Cursor bis zum Zeilenende löschen
   - ``end=""``: Kein Zeilenumbruch
   - ``flush=True``: Sofortige Ausgabe

10. Intelligente AI-Anweisungen

    Die AI wird ausdrücklich angewiesen, entschlossen zu handeln und keine Rückfragen zur Klärung zu stellen:
    
    .. code-block:: python
    
        INSTRUCTIONS = '''
        CRITICAL RULES:
        1. BE DECISIVE: Always take clear action based on user requests.
        2. NO CLARIFICATION QUESTIONS: Never ask "Would you like me to..." questions.
        3. ASSUME INTENT: If ambiguous, make reasonable assumption and take action.
        4. CONFIRM ACTION: Always state what action you are taking.
        '''

----------------------------------------------

**Fehlerbehebung**

- Motor dreht sich nicht

  - Prüfen Sie die Motorverbindungen: M0-Port, richtige Polarität
  - Testen Sie den Motor direkt: ``motor.power(50)`` sollte ihn mit 50 % drehen lassen
  - Stellen Sie sicher, dass die Variable ``speed`` korrekt gesetzt wird (Bereich 0-100)

- Taster reagiert nicht

  - Prüfen Sie die Verkabelung: GPIO 17 zum Taster, andere Seite an 3.3V
  - Überprüfen Sie die Pull-up-Konfiguration
  - Testen Sie mit einem einfachen Skript: Ausgabe bei jeder Zustandsänderung des Tasters
  - Prüfen Sie die Entprellzeit (0.5 Sekunden könnten zu lang sein)

- Kein Ton vom Buzzer

  - Testen Sie den Buzzer direkt: ``buzzer.on()`` sollte einen Dauerton erzeugen
  - Prüfen Sie, ob es sich um einen Piezo-Buzzer (benötigt PWM) oder einen aktiven Buzzer (funktioniert mit Gleichspannung) handelt

- AI versteht die Befehle nicht

  - Prüfen Sie den API-Schlüssel in ``secret.py``
  - Überprüfen Sie die Internetverbindung
  - Kontrollieren Sie die AI-Anweisungen und stellen Sie sicher, dass sie korrekt formatiert sind
  - Testen Sie zunächst mit einfacheren Befehlen

- Geschwindigkeit ändert sich unerwartet

  - Prüfen Sie die Entprellung des Tasters: möglicherweise wird mehrfach ausgelöst
  - Überprüfen Sie das Schlüsselwort-Parsing: manche Formulierungen könnten unbeabsichtigt eine bestimmte Geschwindigkeit auslösen
  - Fügen Sie ``print``-Ausgaben hinzu, um Geschwindigkeitsänderungen nachzuverfolgen

- Schlechte Genauigkeit bei der Spracherkennung

  - Reduzieren Sie Hintergrundgeräusche
  - Sprechen Sie deutlich und in mäßigem Tempo
  - Verwenden Sie gegebenenfalls ein externes USB-Mikrofon für bessere Qualität
  - Passen Sie, falls verfügbar, die STT-Parameter an

- Motor macht Geräusche, dreht sich aber nicht

  - Prüfen Sie, ob der Motor blockiert oder festgeklemmt ist
  - Stellen Sie sicher, dass die Versorgungsspannung zu den Anforderungen des Motors passt
  - Manche Motoren benötigen einen Kondensator an den Anschlüssen für einen ruhigeren Lauf

----------------------------------------------

Dieser sprachgesteuerte Ventilator zeigt, wie natürliche Sprachverarbeitung, physische Bedienelemente und intelligente Systeme kombiniert werden können, um intuitive und barrierearme Smart-Home-Geräte zu schaffen, die auf menschliche Bedürfnisse und Vorlieben reagieren.