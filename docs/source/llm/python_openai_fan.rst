.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_voice_controlled_fan:

(Ejemplo) Ventilador Inteligente Controlado por Voz
==================================================

**Introducción**

Este proyecto crea un inteligente **Ventilador Inteligente Controlado por Voz** que combina reconocimiento de voz, procesamiento con IA y control de motores. El sistema permite a los usuarios controlar la velocidad del ventilador usando comandos de voz naturales y proporciona múltiples métodos de control:

1. **Comandos de Voz** usando speech-to-text para operación manos libres
2. **Botón Físico** para ajuste manual de velocidad
3. **Interpretación con IA** usando GPT de OpenAI para entender lenguaje natural
4. **Retroalimentación Auditiva** con un zumbador para las pulsaciones de botón
5. **Interfaz de Control Dual** que admite interacción por voz y física

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Voice_Controlled_Smart_Fan.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

El ventilador inteligente entiende comandos como "make it faster", "slow down please" o "turn off the fan" y responde con acciones apropiadas y confirmación verbal.

Puedes combinar varios módulos de entrada y salida para crear dispositivos inteligentes controlados por voz. Consulta:

* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`py_motor`

----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
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

**Diagrama de Conexión**

Conecta los componentes al Fusion HAT+ de la siguiente manera:

.. image:: img/fzz/llm_fan_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Ejecutar el Ejemplo**


#. Ejecuta el código

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_fan.py

#. Controla el ventilador

   Puedes controlar el ventilador usando comandos de voz, el botón o lenguaje natural.

   * Comandos de Voz:

     - "Make it faster" / "Increase speed" → Establece al máximo (100%)
     - "Slow down" / "Reduce speed" → Establece a bajo (25%)
     - "Medium speed please" → Establece a medio (50%)
     - "Turn off" / "Stop" → Detiene el motor (0%)
     - "What's the current speed?" → Informa de la velocidad actual
     - "Make it cooler" → Interpreta como una solicitud de mayor velocidad

   * Control con Botón:

     - Cada pulsación aumenta la velocidad en un 10%
     - Al 100%, la siguiente pulsación vuelve al 0%
     - Un pitido audible confirma cada pulsación
     - El porcentaje de velocidad actual se muestra en pantalla

   * Comprensión de Lenguaje Natural:

     La IA también puede entender variaciones como:

     - "I'm feeling hot, can you make it faster?"
     - "Could you please turn the fan down a bit?"
     - "It's too windy in here!"
     - "Set it to half speed"

--------

**Código**

Aquí está el script completo en Python para el Ventilador Inteligente Controlado por Voz:

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

**Entendiendo el Código**

1. Inicialización de Speech-to-Text

   El sistema usa STT (Speech-to-Text) para el reconocimiento de voz:

   .. code-block:: python

      stt = STT(language="en-us")

      for result in stt.listen(stream=True):
          if result["done"]:
              input_text = result['final']
          else:
              print(f"partial: {result['partial']}")

   Esto proporciona reconocimiento de voz en tiempo real con resultados parciales mientras hablas.

2. Configuración del Control del Motor

   El motor del ventilador se controla mediante PWM en el puerto M0:

   .. code-block:: python

      motor = Motor('M0')

      # Set speed as percentage (0-100)
      motor.power(speed)

      # Stop the motor completely
      motor.stop()

3. Botón con Anti-rebote

   El botón incluye anti-rebote para evitar múltiples disparos:

   .. code-block:: python

      button = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      last_triggered = 0

      def speed_up():
          global speed, last_triggered
          if time.time() - last_triggered < 0.5:  # 500ms debounce
              return
          last_triggered = time.time()

4. Retroalimentación Auditiva

   Un zumbador proporciona confirmación audible:

   .. code-block:: python

      buzzer = Buzzer(Pin(4))

      def beep():
          buzzer.on()
          time.sleep(0.1)
          buzzer.off()

5. Función de Análisis de Palabras Clave

   El sistema analiza las respuestas de la IA en busca de comandos de velocidad:

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

6. Entrada Contextual a la IA

   La velocidad actual se incluye en el prompt para respuestas conscientes del contexto:

   .. code-block:: python

      contextual_input = f"Current speed is {speed}%. User says: {input_text}"
      response = llm.prompt(contextual_input, stream=True)

7. Procesamiento de Respuesta en Streaming

   Las respuestas de la IA se procesan palabra por palabra:

   .. code-block:: python

      full_response = ""
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              full_response += next_word

8. Lógica de Control Dual

   El sistema admite control por voz y por botón:

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

9. Salida de Terminal Limpia

   Usa códigos de escape ANSI para una visualización limpia en consola:

   .. code-block:: python

      print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

   - ``\r``: Retorno de carro (ir al inicio de la línea)
   - ``\x1b[K``: Borrar desde el cursor hasta el final de la línea
   - ``end=""``: Sin nueva línea
   - ``flush=True``: Visualización inmediata

10. Instrucciones Inteligentes para la IA

    La IA está específicamente instruida para ser decisiva y evitar preguntas de aclaración:

    .. code-block:: python

        INSTRUCTIONS = '''
        CRITICAL RULES:
        1. BE DECISIVE: Always take clear action based on user requests.
        2. NO CLARIFICATION QUESTIONS: Never ask "Would you like me to..." questions.
        3. ASSUME INTENT: If ambiguous, make reasonable assumption and take action.
        4. CONFIRM ACTION: Always state what action you are taking.
        '''

----------------------------------------------

**Solución de problemas**

- El motor no gira

  - Verifica las conexiones del motor: puerto M0, polaridad correcta
  - Prueba el motor directamente: ``motor.power(50)`` debería girar al 50%
  - Asegúrate de que la variable de velocidad se esté estableciendo (rango 0-100)

- El botón no responde

  - Verifica el cableado: GPIO 17 al botón, el otro lado a 3.3V
  - Verifica la configuración de pull-up
  - Prueba con un script simple: imprime cuando cambie el estado del botón
  - Verifica el tiempo de anti-rebote (0.5 segundos puede ser demasiado largo)

- No hay sonido del zumbador

  - Prueba el zumbador directamente: ``buzzer.on()`` debería producir un tono continuo
  - Verifica si el zumbador es piezoeléctrico (necesita PWM) o activo (funciona con DC)

- La IA no entiende los comandos

  - Verifica la clave API en ``secret.py``
  - Verifica la conexión a internet
  - Examina las instrucciones de la IA: asegúrate de que tengan el formato correcto
  - Prueba primero con comandos más simples

- La velocidad cambia inesperadamente

  - Verifica el anti-rebote del botón: puede estar disparándose múltiples veces
  - Verifica el análisis de palabras clave: algunas frases pueden activar velocidades no deseadas
  - Añade declaraciones de impresión para rastrear los cambios de velocidad

- Baja precisión en el reconocimiento de voz

  - Reduce el ruido de fondo
  - Habla claramente y a un ritmo moderado
  - Considera usar un micrófono USB externo para mejor calidad
  - Ajusta los parámetros de STT si están disponibles

- El motor hace ruido pero no gira

  - Verifica si el motor está atascado o bloqueado
  - Verifica que el voltaje de la fuente de alimentación coincida con los requisitos del motor
  - Algunos motores necesitan un condensador entre los terminales para un funcionamiento suave

----------------------------------------------

¡Este ventilador controlado por voz demuestra cómo el procesamiento de lenguaje natural, los controles físicos y los sistemas inteligentes pueden crear dispositivos domésticos inteligentes intuitivos y accesibles que responden a las necesidades y preferencias humanas!