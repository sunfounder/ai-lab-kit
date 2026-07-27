.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_blindfolded_watermelon_game:

(Ejemplo) Juego de Romper Sandías con los Ojos Vendados
====================================================

**Introducción**

Este proyecto crea un interactivo **Juego de Romper Sandías con los Ojos Vendados** donde los jugadores navegan por una cuadrícula de 20×20 metros usando un joystick mientras dependen de un asistente de IA para obtener orientación direccional. El sistema integra:

1. **Controles de joystick** para el movimiento del jugador en los ejes X/Y
2. **Orientación con IA** usando GPT-4o de OpenAI
3. **Retroalimentación de voz (TTS)** usando Pico2Wave
4. **Generación aleatoria de objetivos** para la colocación de sandías
5. **Botón interactivo** para la acción de romper

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Blindfolded_Watermelon_Smashing_Game.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

El jugador comienza en el centro (0,0) y debe encontrar una sandía colocada aleatoriamente usando solo las indicaciones de audio del asistente de IA, creando una experiencia de juego atractiva con privación sensorial.

Puedes combinar varios dispositivos de entrada con módulos LLM para crear juegos de IA interactivos. Consulta:

* :ref:`py_online_llm`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_joystick`

----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
    *   - :ref:`cpn_joystick`
        - \-
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Diagrama de Conexión**

Conecta los componentes al Fusion HAT+ de la siguiente manera:

.. image:: img/fzz/watermelon_game_bb.png
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
      sudo python3 llm_openai_blindfolded_game.py

#. Juega

   Después de que el script se inicie, el juego colocará aleatoriamente una sandía en el campo de 20×20 metros.
   Usa el joystick para moverte paso a paso, y escucha al asistente de IA para obtener orientación direccional.

   Cuando creas que has alcanzado la posición de la sandía, presiona el botón para romper.
   Si tus coordenadas coinciden exactamente con las de la sandía, ¡ganas el juego!

#. Entiende la mecánica del juego

   * Sistema de Coordenadas:

     - El campo de juego es una cuadrícula de 20×20 metros
     - Las coordenadas van desde (-10,-10) hasta (10,10)
     - X positiva = Este, X negativa = Oeste
     - Y positiva = Sur, Y negativa = Norte (eje Y invertido)
     - El punto central es (0,0)

   * Reglas de Movimiento:

     - Joystick a la derecha → X+1 (Este)
     - Joystick a la izquierda → X-1 (Oeste)
     - Joystick arriba → Y-1 (Norte)
     - Joystick abajo → Y+1 (Sur)
     - Cada movimiento cambia la posición en 1 metro

   * Condición de Victoria:

     - El jugador debe estar en las coordenadas exactas de la sandía
     - Presiona el botón para "romper" en la posición actual
     - La coincidencia exacta termina el juego con un mensaje de victoria

   * Rol del Asistente de IA:

     - Recibe tanto las coordenadas del jugador como de la sandía
     - Proporciona orientación direccional (N, NE, E, SE, S, SW, W, NW)
     - Da una aproximación de distancia en metros
     - Mantiene las respuestas breves para la reproducción de audio


**Código**

Aquí está el script completo en Python para el Juego de Romper Sandías con los Ojos Vendados:

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.adc import ADC
   from fusion_hat.pin import Pin
   from fusion_hat.tts import Pico2Wave
   import random, time

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup TTS
   tts = Pico2Wave()
   tts.set_lang('en-US')

   # Setup Joystick
   btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
   x_axis = ADC('A1')
   y_axis = ADC('A0')

   def MAP(x, in_min, in_max, out_min, out_max):
       """
       Map a value from one range to another.
       """
       return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

   def activate():
       global smash_tips
       smash_tips = True

   btn_pin.when_activated = activate

   # Setup LLM
   INSTRUCTIONS = "This is a blindfolded watermelon-smashing game. A point representing a watermelon is randomly generated within a 20x20 meter area with coordinates ranging from (-10,-10) to (10,10). The player starts from the origin (0,0) and moves using a joystick. Even if the player can't see anything, they press a button to perform a smash action. After smashing, you will receive the watermelon's and player's coordinates. You need to advise the player on the direction of the watermelon, like 'The watermelon is ten meters to your northeast.' If the smash coordinates match, the game ends. Your responses will be converted into speech via TTS, so please keep them brief, ideally within two sentences."

   WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant. Use the joystick to move and press the button to smash. I will guide you to find the watermelon. Good luck!"


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

   # Define the map size and the joystick pins
   watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
   player_x, player_y = 0, 0
   smash_tips = False

   while True:
       x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
       y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

       if x_val > 80:
           player_x += 1
       elif x_val < -80:
           player_x -= 1

       if y_val > 80:
           player_y -= 1
       elif y_val < -80:
           player_y += 1

       # Debug positions (commented out in actual game)
       # print('Watermelon position: %d, %d  ' % (watermelon_x, watermelon_y))
       # print('Player position: %d, %d  ' % (player_x, player_y))

       time.sleep(0.3)

       if smash_tips:
           smash_tips = False
           print("Smash!")

           if (player_x, player_y) == (watermelon_x, watermelon_y):
               print("Target hit!")
               tts.say("Target hit!")
               break
           else:
               input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

               # Response with stream
               response = llm.prompt(input_text, stream=True)
               string = ""

               for next_word in response:
                   if next_word:
                       # print(next_word, end="", flush=True)  # Uncomment for streaming display
                       string += next_word

               # print("")  # New line after streaming
               print("AI: " + string)
               tts.say(string)

   print("Game over!")

----------------------------------------------

**Entendiendo el Código**

1. Configuración de Text-to-Speech

   El juego usa Pico2Wave para la retroalimentación de audio:

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')

   Esto convierte las respuestas de texto de la IA en instrucciones habladas en inglés.

2. Manejo de Entrada del Joystick

   El joystick usa dos canales ADC para leer los ejes X e Y:

   .. code-block:: python

      x_axis = ADC('A1')  # Horizontal movement
      y_axis = ADC('A0')  # Vertical movement

      def MAP(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

      # Convert 0-4095 ADC reading to -100 to 100 range
      x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
      y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

3. Configuración del Botón con Interrupción

   El botón usa una devolución de llamada de interrupción para respuesta inmediata:

   .. code-block:: python

      btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)

      def activate():
          global smash_tips
          smash_tips = True

      btn_pin.when_activated = activate

   Cuando se presiona, establece ``smash_tips`` a ``True``, activando la acción de romper en el bucle principal.

4. Configuración del LLM de OpenAI

   El asistente de IA está configurado con instrucciones específicas del juego:

   .. code-block:: python

      INSTRUCTIONS = "This is a blindfolded watermelon-smashing game..."
      WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant..."

      llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      llm.set_max_messages(20)       # Keep conversation history
      llm.set_instructions(INSTRUCTIONS)  # Set game rules
      llm.set_welcome(WELCOME)       # Set initial greeting

5. Gestión del Estado del Juego

   El juego mantiene las posiciones del jugador y del objetivo:

   .. code-block:: python

      # Random watermelon placement
      watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)

      # Player starts at center
      player_x, player_y = 0, 0

      # Movement thresholds (80% joystick deflection)
      if x_val > 80:
          player_x += 1      # Move right
      elif x_val < -80:
          player_x -= 1      # Move left

      if y_val > 80:
          player_y -= 1      # Move up (negative Y)
      elif y_val < -80:
          player_y += 1      # Move down (positive Y)

6. Acción de Romper y Respuesta de la IA

   Cuando se presiona el botón, el juego verifica si hay un acierto o solicita orientación a la IA:

   .. code-block:: python

      if smash_tips:
          smash_tips = False
          print("Smash!")

          if (player_x, player_y) == (watermelon_x, watermelon_y):
              print("Target hit!")
              tts.say("Target hit!")
              break  # Game ends
          else:
              # Send positions to AI for guidance
              input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

              # Get streaming response from AI
              response = llm.prompt(input_text, stream=True)
              string = ""

              for next_word in response:
                  if next_word:
                      string += next_word

              print("AI: " + string)
              tts.say(string)  # Speak the guidance

7. Procesamiento de Respuesta en Streaming

   La respuesta de la IA se procesa palabra por palabra para posible visualización en tiempo real:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              # Uncomment to display words as they arrive
              # print(next_word, end="", flush=True)
              string += next_word

8. Lógica de Movimiento con Zona Muerta

   El joystick tiene una zona muerta de 80 unidades para evitar movimientos accidentales:

   .. code-block:: python

      # Only move when joystick is pushed >80% in any direction
      # This prevents drifting from center position
      if x_val > 80:    # Right
      elif x_val < -80: # Left

      if y_val > 80:    # Up
      elif y_val < -80: # Down

9. Estructura del Bucle del Juego

   El bucle principal del juego continuamente:

   1. Lee la posición del joystick
   2. Actualiza las coordenadas del jugador si el joystick está presionado
   3. Verifica la pulsación del botón de romper
   4. Procesa las respuestas de la IA cuando es necesario
   5. Proporciona retroalimentación de audio a través de TTS

----------------------------------------------

**Solución de problemas**

- Sin respuesta del joystick

  - Verifica las conexiones ADC: A0 para el eje Y, A1 para el eje X
  - Verifica la alimentación: VCC a 3.3V, GND a tierra
  - Prueba la lectura ADC: ``print(x_axis.read())`` debería mostrar 0-4095
  - Asegúrate de que el joystick esté centrado (debería leer ~2048)


- Sin audio del TTS

  - Verifica la salida de audio: ``sudo raspi-config`` → **System Options** → **Audio**
  - Prueba el altavoz: ``speaker-test -t sine -f 440``
  - Asegúrate de que Pico2Wave esté instalado: ``pico2wave --help``
  - Verifica el volumen: ``alsamixer``
  - Re-ejecuta el script de configuración de audio: ``sudo /opt/setup_fusion_hat_audio.sh``

- Errores de API de OpenAI

  - Verifica la clave API en ``secret.py``
  - Verifica la conexión a internet: ``ping 8.8.8.8``
  - Asegúrate de que la facturación esté habilitada en la cuenta de OpenAI
  - Verifica que el modelo "gpt-4o" esté disponible en tu cuenta

- El jugador se mueve demasiado rápido/lento

  - Ajusta el umbral de movimiento (actualmente 80): más alto = más desviación del joystick necesaria
  - Modifica el incremento de movimiento (actualmente 1): cambia a 0.5 para un control más fino
  - Ajusta el tiempo de espera (actualmente 0.3s): más largo = respuesta de movimiento más lenta


- Respuestas de IA demasiado largas

  - Enfatiza la brevedad en INSTRUCTIONS
  - Añade "Respond in 10 words or less" a las instrucciones
  - Implementa verificación de longitud de respuesta en el código

----------------------------------------------

¡Este juego de la sandía con los ojos vendados demuestra cómo los controles físicos, la orientación de IA y la retroalimentación de audio pueden crear una experiencia de juego atractiva basada en los sentidos que desafía la conciencia espacial y las habilidades de escucha!