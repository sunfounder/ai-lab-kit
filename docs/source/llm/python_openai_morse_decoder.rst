.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(Ejemplo) Decodificador de Código Morse con IA
========================================

**Introducción**

Este proyecto crea un inteligente **Decodificador de Código Morse** que usa IA para interpretar patrones de temporización de pulsaciones de botones. El sistema captura datos de temporización precisos y aprovecha GPT de OpenAI para decodificar mensajes en código Morse en tiempo real. El decodificador incluye:

1. **Entrada basada en temporización** que captura tiempos precisos de pulsación y liberación
2. **Decodificación con IA** usando GPT para interpretar patrones de puntos y rayas
3. **Indicador Visual** con LED que muestra el estado activo de decodificación
4. **Interfaz de Botón Dual** botones separados de entrada y control
5. **Retroalimentación en Tiempo Real** mostrando datos de temporización mientras introduces

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

El sistema registra las duraciones de las pulsaciones de botón, envía los datos de temporización a la IA para su interpretación, y decodifica con precisión secuencias de código Morse como la señal universal de socorro "SOS".

Puedes combinar entradas sensibles a la temporización con interpretación de IA para varios sistemas de codificación. Consulta:

* :ref:`py_online_llm`

----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
    *   - :ref:`cpn_button`
        - |link_button_buy| (x2)
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Diagrama de Conexión**

Conecta los componentes a la Raspberry Pi de la siguiente manera:

.. image:: img/fzz/morse_decoder_bb.png
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
      sudo python3 llm_openai_morse_decoder.py

#. Prueba un mensaje simple en código Morse (ejemplo: "SOS")

   Después de que el programa se inicie, presiona el botón de inicio/parada para comenzar a grabar.
   Luego presiona el botón Morse para introducir puntos (pulsaciones cortas) y rayas (pulsaciones largas).

   Cuando termines, presiona el botón de inicio/parada nuevamente para detener la grabación y decodificar el mensaje.

#. Verifica la salida de la consola

   La consola mostrará las marcas de tiempo de pulsación/liberación, y la IA analizará los datos de temporización
   y mostrará el mensaje decodificado.

   **Salida típica de la consola al introducir "SOS":**

   .. code-block:: text

      To decode the Morse code message based on the button press times provided, we need to interpret the duration of each press. Typically, a short press (dot) is around 0.2 to 0.3 seconds, while a long press (dash) is about 0.5 seconds or longer. Let's analyze the press durations:

      1. `1767773542.1257536` to `1767773542.285196` - Duration: ~0.16 seconds - Dot (.)
      2. `1767773542.4936137` to `1767773542.6315389` - Duration: ~0.14 seconds - Dot (.)
      3. `1767773542.9092748` to `1767773543.0543947` - Duration: ~0.15 seconds - Dot (.)
      4. `1767773544.2299025` to `1767773544.5774245` - Duration: ~0.35 seconds - Dash (-)
      5. `1767773545.1017563` to `1767773545.4954002` - Duration: ~0.39 seconds - Dash (-)
      6. `1767773546.11932` to `1767773546.5881057` - Duration: ~0.47 seconds - Dash (-)
      7. `1767773547.824543` to `1767773547.9534554` - Duration: ~0.13 seconds - Dot (.)
      8. `1767773548.1879761` to `1767773548.2895174` - Duration: ~0.10 seconds - Dot (.)
      9. `1767773548.5281847` to `1767773548.6453152` - Duration: ~0.12 seconds - Dot (.)

      Now let's decode the sequence into letters using Morse code:

      - `...` (Dot Dot Dot) = S
      - `---` (Dash Dash Dash) = O
      - `...` (Dot Dot Dot) = S

      Putting it all together, the decoded message is "SOS".

#. Entiende el flujo de trabajo

   1. Iniciar grabación: presiona el botón de inicio/parada (GPIO 17) y el LED se ENCIENDE
   2. Introducir código Morse: usa el botón Morse (GPIO 22) para puntos y rayas
   3. Visualización en tiempo real: la consola muestra las marcas de tiempo de pulsación/liberación
   4. Detener y decodificar: presiona el botón de inicio/parada nuevamente y el LED se APAGA
   5. Análisis de IA: los datos de temporización se envían a OpenAI GPT para su interpretación
   6. Salida decodificada: la IA imprime el mensaje decodificado

**Código**

Aquí está el script completo en Python para el Decodificador de Código Morse con IA:

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.pin import Pin
   import random, time

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup GPIO pins
   morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   led = Pin(27, Pin.OUT)  # Indicator LED on GPIO 27

   # Store the morse code events with timing data
   morse_events = []
   input_active = False  # Flag to indicate if input is active

   # Setup LLM with Morse code decoding instructions
   INSTRUCTIONS = "You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it."

   WELCOME = "Hello, I am a Morse code decoder. Please press the button to start decoding. When you are done, press the button again to stop."

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

   # Send the morse code timing data to the AI for decoding
   def decode_and_print():
       global morse_events

       # Convert timing events to string for AI processing
       input_text = str(morse_events)

       # Get response from AI with streaming
       response = llm.prompt(input_text, stream=True)

       # Print streaming response
       for next_word in response:
           if next_word:
               print(next_word, end="", flush=True)

       print("")  # New line after complete response

       morse_events = []  # Clear the morse code events for next message

   # Morse code input handling variables
   start_time = 0

   # Function called when morse input button is pressed
   def morse_input_pressed():
       global start_time
       start_time = time.time()
       morse_events.append(('pressed', start_time))
       print(f" Pressed at {start_time} -", end="")

   # Function called when morse input button is released
   def morse_input_released():
       global morse_events, start_time
       release_time = time.time()

       # Debounce: ignore releases within 0.1 seconds
       if release_time - start_time < 0.1:
           return

       morse_events.append(('released', release_time))
       print(f" {release_time}")

   # Start/stop button handler
   def handle_start_stop():
       global input_active, morse_events

       if input_active:
           # Stop recording and decode
           led.off()
           print("Input stopped and decoded.")
           decode_and_print()
           input_active = False
       else:
           # Start recording new message
           input_active = True
           morse_events.clear()  # Clear previous events
           led.on()
           print("Input started.")

   # Add event listeners to buttons
   start_stop_button.when_activated = handle_start_stop
   morse_input.when_activated = morse_input_pressed
   morse_input.when_deactivated = morse_input_released

   # Main program loop
   try:
       while True:
           time.sleep(0.1)
   except KeyboardInterrupt:
       pass


----------------------------------------------

**Entendiendo el Código**

1. Configuración de Pines GPIO

   Se configuran tres pines GPIO para diferentes propósitos:

   .. code-block:: python

      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)

   - Tiempo de anti-rebote (0.05s): Evita múltiples detecciones por rebote mecánico del interruptor
   - Pull-down: Asegura una señal LOW limpia cuando el botón no está presionado
   - Funciones separadas: Los botones de entrada y control evitan entradas accidentales

2. Almacenamiento de Datos de Temporización

   Los eventos de pulsación/liberación se almacenan con marcas de tiempo precisas:

   .. code-block:: python

      morse_events = []  # Empty list to store events

      # Each event stored as tuple: ('pressed'/'released', timestamp)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. Mecanismo de Anti-rebote

   Evita disparos falsos por rebote del interruptor:

   .. code-block:: python

      def morse_input_released():
          if release_time - start_time < 0.1:  # 100ms debounce
              return  # Ignore very short releases

          morse_events.append(('released', release_time))

4. Gestión de Estado

   El sistema usa una bandera para rastrear el estado de grabación:

   .. code-block:: python

      input_active = False  # Initially not recording

      def handle_start_stop():
          if input_active:
              # Stop recording and decode
              input_active = False
          else:
              # Start recording
              input_active = True
              morse_events.clear()  # Clear previous data

5. Indicador Visual

   El LED proporciona retroalimentación visual del estado de grabación:

   .. code-block:: python

      def handle_start_stop():
          if input_active:
              led.off()  # LED OFF when not recording
          else:
              led.on()   # LED ON when recording

6. Construcción del Prompt para la IA

   Los datos de temporización se convierten en cadena para el procesamiento de la IA:

   .. code-block:: python

      input_text = str(morse_events)

      # Example format sent to AI:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. Respuesta en Streaming

   La respuesta de la IA se procesa y muestra en tiempo real:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. Arquitectura Basada en Eventos

   Los eventos de botón activan devoluciones de llamada inmediatas:

   .. code-block:: python

      # Assign callback functions to button events
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. Precisión de Temporización

   Usa ``time.time()`` para temporización precisa en microsegundos:

   .. code-block:: python

      start_time = time.time()  # Current time in seconds since epoch

      # Calculate press duration:
      duration = release_time - start_time

10. Limpieza de Datos

    Después de la decodificación, la lista de eventos se limpia para el siguiente mensaje:

    .. code-block:: python

        def decode_and_print():
            # ... process events ...
            morse_events = []  # Clear for next message

----------------------------------------------

**Estándares de Temporización del Código Morse**

* Temporización Estándar (basada en la palabra PARIS):

  - Punto: 1 unidad
  - Raya: 3 unidades
  - Espacio entre caracteres (entre puntos/rayas): 1 unidad
  - Espacio entre letras: 3 unidades
  - Espacio entre palabras: 7 unidades

* Implementación Práctica:

  - Punto: < 0.3 segundos (pulsación corta)
  - Raya: > 0.5 segundos (pulsación larga)
  - Entre elementos: < 0.5 segundos de pausa
  - Entre letras: 0.5-1.5 segundos de pausa
  - Entre palabras: > 1.5 segundos de pausa

* Letras Comunes del Código Morse:

  - A: • — (punto-raya)
  - B: — • • • (raya-punto-punto-punto)
  - C: — • — • (raya-punto-raya-punto)
  - S: • • • (punto-punto-punto)
  - O: — — — (raya-raya-raya)

----------------------------------------------

**Solución de problemas**

- Las pulsaciones de botón no se registran

  - Verifica el cableado: GPIO 22/17 al botón, el otro lado a Tierra
  - Verifica la configuración de pull-down
  - Prueba con un script simple: ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``
  - Verifica la configuración del tiempo de anti-rebote (0.05s puede ser demasiado alto)

- El LED no se enciende

  - Verifica la polaridad del LED: ánodo (pata larga) a GPIO 27 a través de una resistencia
  - Verifica el valor de la resistencia (220Ω recomendado)
  - Prueba el LED directamente: ``Pin(27, Pin.OUT).on()`` debería encender el LED
  - Asegúrate de que la conexión a tierra esté completa

- Los datos de temporización parecen incorrectos

  - Verifica el reloj del sistema: comando ``date``
  - Reduce el tiempo de anti-rebote si es demasiado sensible
  - Añade declaraciones de impresión para verificar la ejecución de la devolución de llamada
  - Prueba con duraciones de pulsación consistentes

- La IA no decodifica correctamente

  - Verifica la clave API y la conexión a internet
  - Examina los datos de temporización enviados a la IA (imprime ``morse_events``)
  - Asegúrate de tener duraciones de pulsación consistentes (puntos cortos, rayas largas)
  - Añade pausas más claras entre letras

- Múltiples disparos de una sola pulsación

  - Aumenta el parámetro bounce_time (prueba con 0.1s)
  - Verifica el rebote mecánico del interruptor
  - Añade anti-rebote por hardware con un condensador
  - Verifica que el botón esté correctamente cableado

- El sistema no responde al inicio/parada

  - Verifica si otra devolución de llamada está interfiriendo
  - Verifica la lógica de la bandera ``input_active``
  - Añade impresiones de depuración en ``handle_start_stop()``
  - Asegúrate de que ningún otro proceso esté usando GPIO

- Respuesta de IA demasiado lenta

  - Verifica la velocidad de la conexión a internet
  - Reduce el número de eventos (mensajes más cortos)
  - Considera usar decodificación local como alternativa
  - Implementa un tiempo de espera para las respuestas de la IA

- No se pueden distinguir puntos de rayas

  - Practica una temporización consistente
  - Ajusta el umbral en las instrucciones de la IA
  - Añade preprocesamiento local antes de enviar a la IA
  - Usa retroalimentación visual durante la entrada

----------------------------------------------


¡Este decodificador de código Morse con IA demuestra cómo los datos de temporización precisos combinados con el reconocimiento inteligente de patrones pueden revivir y modernizar métodos de comunicación históricos, haciéndolos accesibles y educativos para las nuevas generaciones!