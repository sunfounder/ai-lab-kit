.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_voice_controlled_fan:

(Esempio) Ventilatore Intelligente a Controllo Vocale
=========================================================

**Introduzione**

Questo progetto crea un intelligente **Ventilatore Intelligente a Controllo Vocale** che combina riconoscimento vocale, elaborazione AI e controllo motore. Il sistema permette agli utenti di controllare la velocita' del ventilatore usando comandi vocali naturali e fornisce molteplici metodi di controllo:

1. **Comandi Vocali** utilizzando il riconoscimento vocale per il funzionamento a mani libere
2. **Pulsante Fisico** per la regolazione manuale della velocita'
3. **Interpretazione AI** utilizzando GPT di OpenAI per comprendere il linguaggio naturale
4. **Feedback Acustico** con un cicalino per le pressioni dei pulsanti
5. **Interfaccia di Controllo Duale** che supporta sia l'interazione vocale che fisica

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Voice_Controlled_Smart_Fan.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Il ventilatore intelligente comprende comandi come "accelera", "rallenta per favore" o "spegniti" e risponde con azioni appropriate e conferma verbale.

Puoi combinare vari moduli di input e output per creare dispositivi intelligenti a controllo vocale. Vedi:

* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`py_motor`

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
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

**Schema di Collegamento**

Collega i componenti al Fusion HAT+ come segue:

.. image:: img/fzz/llm_fan_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Esegui l'Esempio**


#. Esegui il codice

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_fan.py

#. Controlla il ventilatore

   Puoi controllare il ventilatore usando comandi vocali, il pulsante o il linguaggio naturale.

   * Comandi Vocali:

     - "Make it faster" / "Increase speed" -> Imposta al massimo (100%)
     - "Slow down" / "Reduce speed" -> Imposta al minimo (25%)
     - "Medium speed please" -> Imposta a medio (50%)
     - "Turn off" / "Stop" -> Ferma il motore (0%)
     - "What's the current speed?" -> Riporta la velocita' attuale
     - "Make it cooler" -> Interpreta come richiesta di velocita' maggiore

   * Controllo tramite Pulsante:

     - Ogni pressione aumenta la velocita' del 10%
     - Al 100%, la pressione successiva ritorna allo 0%
     - Un segnale acustico conferma ogni pressione
     - La percentuale di velocita' corrente viene visualizzata sullo schermo

   * Comprensione del Linguaggio Naturale:

     L'AI puo' anche comprendere variazioni come:

     - "I'm feeling hot, can you make it faster?"
     - "Could you please turn the fan down a bit?"
     - "It's too windy in here!"
     - "Set it to half speed"

--------

**Codice**

Ecco lo script Python completo per il Ventilatore Intelligente a Controllo Vocale:

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

**Comprensione del Codice**

1. Inizializzazione del Riconoscimento Vocale

   Il sistema utilizza STT (Speech-to-Text) per il riconoscimento vocale:

   .. code-block:: python

      stt = STT(language="en-us")

      for result in stt.listen(stream=True):
          if result["done"]:
              input_text = result['final']
          else:
              print(f"partial: {result['partial']}")

   Questo fornisce riconoscimento vocale in tempo reale con risultati parziali mentre parli.

2. Configurazione del Controllo Motore

   Il motore del ventilatore e' controllato tramite PWM sulla porta M0:

   .. code-block:: python

      motor = Motor('M0')

      # Imposta velocita' in percentuale (0-100)
      motor.power(speed)

      # Ferma completamente il motore
      motor.stop()

3. Pulsante con Debounce

   Il pulsante include debounce per prevenire attivazioni multiple:

   .. code-block:: python

      button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      last_triggered = 0

      def speed_up():
          global speed, last_triggered
          if time.time() - last_triggered < 0.5:  # 500ms debounce
              return
          last_triggered = time.time()

4. Feedback Acustico

   Un cicalino fornisce conferma uditiva:

   .. code-block:: python

      buzzer = Buzzer(Pin(4))

      def beep():
          buzzer.on()
          time.sleep(0.1)
          buzzer.off()

5. Funzione di Analisi delle Parole Chiave

   Il sistema analizza le risposte AI per i comandi di velocita':

   .. code-block:: python

      def parse_response_for_speed(text_response):
          text_lower = text_response.lower()

          # Controlla parole chiave per "stop" o "off"
          if any(word in text_lower for word in ['stop', 'off', 'zero']):
              return 0

          # Controlla parole chiave per "slow" o "low"
          if any(word in text_lower for word in ['slow', 'low', '25%']):
              return 25

          # Controlli simili per medio e veloce

          return -1  # Nessun cambiamento di velocita'

6. Input Contestuale all'AI

   La velocita' corrente e' inclusa nel prompt per risposte contestuali:

   .. code-block:: python

      contextual_input = f"Current speed is {speed}%. User says: {input_text}"
      response = llm.prompt(contextual_input, stream=True)

7. Elaborazione della Risposta in Streaming

   Le risposte AI vengono elaborate parola per parola:

   .. code-block:: python

      full_response = ""
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              full_response += next_word

8. Logica di Controllo Duale

   Il sistema supporta sia il controllo vocale che quello tramite pulsante:

   .. code-block:: python

      # Controllo vocale nel ciclo principale
      new_speed = parse_response_for_speed(full_response)
      if new_speed >= 0:
          speed = new_speed
          motor.power(speed)

      # Controllo tramite pulsante via callback
      def speed_up():
          speed += 10
          if speed > 100:
              speed = 0
          motor.power(speed)

9. Output Terminale Pulito

   Utilizza codici di escape ANSI per un display console pulito:

   .. code-block:: python

      print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

   - ``\r``: Ritorno a inizio riga
   - ``\x1b[K``: Cancella da cursore a fine riga
   - ``end=""``: Nessun newline
   - ``flush=True``: Visualizzazione immediata

10. Istruzioni AI Intelligenti

    L'AI e' specificamente istruita per essere decisa ed evitare domande di chiarimento:

    .. code-block:: python

        INSTRUCTIONS = '''
        CRITICAL RULES:
        1. BE DECISIVE: Always take clear action based on user requests.
        2. NO CLARIFICATION QUESTIONS: Never ask "Would you like me to..." questions.
        3. ASSUME INTENT: If ambiguous, make reasonable assumption and take action.
        4. CONFIRM ACTION: Always state what action you are taking.
        '''

----------------------------------------------

**Risoluzione dei Problemi**

- Il motore non gira

  - Verifica le connessioni del motore: porta M0, polarita' corretta
  - Prova il motore direttamente: ``motor.power(50)`` dovrebbe girare al 50%
  - Assicurati che la variabile speed venga impostata (intervallo 0-100)

- Il pulsante non risponde

  - Controlla il cablaggio: GPIO 17 al pulsante, altro lato a 3.3V
  - Verifica la configurazione pull-up
  - Prova con uno script semplice: stampa quando lo stato del pulsante cambia
  - Controlla il tempo di debounce (0.5 secondi potrebbe essere troppo lungo)

- Nessun suono dal cicalino

  - Prova il cicalino direttamente: ``buzzer.on()`` dovrebbe produrre un tono continuo
  - Controlla se il cicalino e' piezoelettrico (necessita PWM) o attivo (funziona con DC)

- L'AI non comprende i comandi

  - Controlla la chiave API in ``secret.py``
  - Verifica la connessione Internet
  - Esamina le istruzioni AI: assicurati che siano formattate correttamente
  - Prova prima con comandi piu' semplici

- La velocita' cambia inaspettatamente

  - Controlla il debounce del pulsante: potrebbe attivarsi piu' volte
  - Verifica l'analisi delle parole chiave: alcune frasi potrebbero attivare velocita' indesiderate
  - Aggiungi istruzioni print per tracciare i cambiamenti di velocita'

- Scarsa precisione del riconoscimento vocale

  - Riduci il rumore di fondo
  - Parla chiaramente e a ritmo moderato
  - Considera l'uso di un microfono USB esterno per una migliore qualita'
  - Regola i parametri STT se disponibili

- Il motore fa rumore ma non gira

  - Controlla se il motore e' bloccato o ostruito
  - Verifica che la tensione di alimentazione corrisponda ai requisiti del motore
  - Alcuni motori necessitano di un condensatore tra i terminali per un funzionamento regolare

----------------------------------------------

Questo ventilatore a controllo vocale dimostra come l'elaborazione del linguaggio naturale, i controlli fisici e i sistemi intelligenti possano creare dispositivi domestici intelligenti intuitivi e accessibili che rispondono ai bisogni e alle preferenze umane!
