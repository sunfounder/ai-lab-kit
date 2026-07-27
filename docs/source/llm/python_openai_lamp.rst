.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_led_controller:

(Ejemplo) Controlador de LED con IA
======================================

**Introducción**

En este proyecto, construirás un **controlador de LED con IA** que combina un modelo LLM (aquí usamos el modelo de lenguaje GPT-4o de OpenAI) con un LED RGB. El sistema interpreta comandos en lenguaje natural para controlar los colores del LED, permitiéndote solicitar verbalmente colores específicos usando nombres de colores, valores HEX o tuplas RGB. Esto demuestra la integración de la inteligencia artificial con hardware físico a través del procesamiento de lenguaje natural.

Cuando dices comandos como "turn on red light" o "show warm yellow light", la IA analiza tu solicitud y genera las señales de control apropiadas para ajustar el LED en consecuencia.

Para usar otro modelo LLM, consulta :ref:`py_online_llm` .

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Led_Controller.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Diagrama de Conexión**

Conecta el LED RGB al Fusion HAT+ de la siguiente manera:

.. image:: img/fzz/llm_book_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------------------

**Ejecutar el Código**


#. Ejecuta el controlador LED con IA:

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_lamp.py

#. Cuando el script se ejecute:

   * Verás un mensaje de bienvenida: "Smart Lighting Assistant started!"
   * Escribe comandos en lenguaje natural como:

     - "turn on red light"
     - "show blue color"
     - "set to warm white"
     - "turn off the light"

   * La IA responderá y controlará el LED en consecuencia
   * Escribe 'quit' o 'exit' para finalizar el programa

----------------------------------------------

**Código**

Aquí está el script completo en Python para el Controlador de LED con IA:

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import re
   from fusion_hat.llm import OpenAI
   from fusion_hat.modules import RGB_LED
   from fusion_hat.pwm import PWM
   from secret import OPENAI_API_KEY

   class AILEDController:
       def __init__(self):
           # Initialize LED
           self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)

           # Initialize AI assistant
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",
           )

           # Enhanced instructions for LED control
           self.instructions = """You are an AI assistant that can control an RGB LED.
           When the user mentions colors, you need to respond with a specific format to control the LED.

           Response format:
           1. Normal conversation part
           2. End with [LED:color] where color can be:
              - Color names: red, green, blue, yellow, purple, etc.
              - HEX values: #FF0000, #00FF00, etc.
              - RGB tuples: (255,0,0), (0,255,0), etc.
              - Numbers: 0xFF0000, etc.

           Examples:
           User: Turn the light red
           You: OK, set to red. [LED:red]

           User: Show warm yellow light
           You: Set to warm yellow light. [LED:#FFD700]

           User: Turn off the light
           You: Light turned off. [LED:black] or [LED:(0,0,0)]

           If the user doesn't mention anything color-related, don't include the [LED:...] tag."""

           # Color name to RGB mapping
           self.color_map = {
               'red': (255, 0, 0),
               'green': (0, 255, 0),
               'blue': (0, 0, 255),
               'yellow': (255, 255, 0),
               'purple': (255, 0, 255),
               'cyan': (0, 255, 255),
               'white': (255, 255, 255),
               'black': (0, 0, 0),
               'orange': (255, 165, 0),
               'pink': (255, 192, 203),
               'brown': (165, 42, 42),
               'grey': (128, 128, 128),
               'warmwhite': (255, 197, 143),
           }

           self.llm.set_max_messages(20)
           self.llm.set_instructions(self.instructions)
           self.llm.set_welcome("Hello! I'm your smart lighting assistant. I can control RGB LED colors.")

           # Initial state: light off
           self.rgb_led.color((0, 0, 0))

       def parse_led_command(self, text):
           """Parse LED control command from AI response"""
           pattern = r'\[LED:(.*?)\]'
           match = re.search(pattern, text)

           if not match:
               return None, text

           led_command = match.group(1).strip()
           display_text = re.sub(pattern, '', text).strip()

           return led_command, display_text

       def apply_color(self, color_spec):
           """Convert color specification to RGB and apply to LED"""
           color_spec = color_spec.lower().strip()

           try:
               # 1. Process color names
               if color_spec in self.color_map:
                   rgb = self.color_map[color_spec]
                   self.rgb_led.color(rgb)
                   return True

               # 2. Process hex strings (e.g., #FF0000)
               elif color_spec.startswith('#'):
                   hex_color = color_spec.lstrip('#')
                   if len(hex_color) == 6:
                       rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                       self.rgb_led.color(rgb)
                       return True

               # 3. Process RGB tuple strings (e.g., (255,0,0))
               elif color_spec.startswith('(') and color_spec.endswith(')'):
                   numbers = color_spec[1:-1].split(',')
                   if len(numbers) == 3:
                       rgb = tuple(int(num.strip()) for num in numbers)
                       if all(0 <= val <= 255 for val in rgb):
                           self.rgb_led.color(rgb)
                           return True

               # 4. Process hex number strings (e.g., 0xFF0000)
               elif color_spec.startswith('0x'):
                   hex_num = int(color_spec, 16)
                   self.rgb_led.color(hex_num)
                   return True

               # 5. Try direct integer conversion
               else:
                   try:
                       num = int(color_spec)
                       if 0 <= num <= 0xFFFFFF:
                           self.rgb_led.color(num)
                           return True
                   except ValueError:
                       pass

               return False

           except Exception as e:
               print(f"Color setting error: {e}")
               return False

       def run(self):
           """Main run loop"""
           print("Smart Lighting Assistant started!")
           print("You can say: 'turn on red light', 'show blue', 'set to purple', 'turn off light', etc.")
           print("Type 'quit' or 'exit' to end the program\n")

           while True:
               try:
                   user_input = input(">>> ").strip()

                   if user_input.lower() in ['quit', 'exit', 'bye']:
                       print("Goodbye!")
                       self.rgb_led.color((0, 0, 0))
                       break

                   response = self.llm.prompt(user_input, stream=True)

                   full_response = ""
                   for word in response:
                       if word:
                           print(word, end="", flush=True)
                           full_response += word
                   print()

                   led_command, display_only = self.parse_led_command(full_response)

                   if led_command:
                       print(f"Detected LED command: {led_command}")
                       if self.apply_color(led_command):
                           print(f"✓ Applied color: {led_command}")
                       else:
                           print(f"✗ Unrecognized color format: {led_command}")

               except KeyboardInterrupt:
                   print("\nProgram interrupted")
                   self.rgb_led.color((0, 0, 0))
                   break
               except Exception as e:
                   print(f"Error: {e}")
                   continue

   # Enhanced version with direct command support
   class AILEDControllerPro(AILEDController):
       def __init__(self):
           super().__init__()

           self.instructions = """You control an RGB LED light. When user mentions colors, add [LED:color_value] at the end.

           Color values can be:
           1. English color names: red, green, blue, yellow, purple, cyan, white, black, orange, pink
           2. HEX values: #FF0000
           3. RGB tuples: (255,0,0)

           Examples:
           User: Turn on red light
           Response: Red light activated. [LED:red]

           User: Turn off the light
           Response: Light turned off. [LED:black]

           User: How is the weather today?
           Response: I can't check real-time weather, but I can adjust your lighting! [LED:#FFFFFF]"""

           self.llm.set_instructions(self.instructions)

       def process_user_input(self, text):
           """Preprocess user input for direct commands"""
           text_lower = text.lower()

           direct_commands = {
               'turn on light': 'white',
               'turn off light': 'black',
               'red light': 'red',
               'green light': 'green',
               'blue light': 'blue',
               'yellow light': 'yellow',
               'purple light': 'purple',
               'white light': 'white',
           }

           for cmd, color in direct_commands.items():
               if cmd in text_lower:
                   self.apply_color(color)
                   return f"Set to {color}. [LED:{color}]"

           return None


   if __name__ == "__main__":
       # Create an instance of the controller
       controller = AILEDControllerPro()
       controller.run()

----------------------------------------------

**Entendiendo el Código**

1. Inicialización del Asistente IA

   El sistema usa el modelo GPT-4o de OpenAI con instrucciones personalizadas para asegurar que genere comandos de control LED en un formato específico.

   .. code-block:: python

      self.llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      self.instructions = """You are an AI assistant that can control an RGB LED...
         ...End with [LED:color] where color can be:...
      """

      self.llm.set_instructions(self.instructions)

2. Control de LED RGB

   La clase RGB_LED de fusion_hat.modules proporciona una interfaz para controlar los tres canales de color mediante PWM.

   .. code-block:: python

      self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)

      # Set color using RGB tuple
      self.rgb_led.color((255, 0, 0))  # Red

      # Set color using hex value
      self.rgb_led.color(0xFF0000)  # Also red

3. Análisis de Comandos con Expresiones Regulares

   El sistema usa regex para extraer comandos de control LED de la respuesta de la IA.

   .. code-block:: python

      def parse_led_command(self, text):
          """Parse LED control command from AI response"""
          pattern = r'\[LED:(.*?)\]'
          match = re.search(pattern, text)

          if not match:
              return None, text

          led_command = match.group(1).strip()
          display_text = re.sub(pattern, '', text).strip()

          return led_command, display_text

4. Soporte para Múltiples Formatos de Color

   El controlador acepta varios formatos de especificación de color para máxima flexibilidad.

   .. code-block:: python

      def apply_color(self, color_spec):
          """Convert color specification to RGB and apply to LED"""
          color_spec = color_spec.lower().strip()

          # 1. Color names (red, green, blue, etc.)
          # 2. HEX strings (#FF0000)
          # 3. RGB tuples ((255,0,0))
          # 4. Hex numbers (0xFF0000)
          # 5. Direct integers (16711680)

5. Respuesta en Streaming

   La respuesta de la IA se transmite palabra por palabra para una experiencia de conversación más natural.

   .. code-block:: python

      response = self.llm.prompt(user_input, stream=True)

      full_response = ""
      for word in response:
          if word:
              print(word, end="", flush=True)
              full_response += word

6. Versión Pro Mejorada

   La clase AILEDControllerPro añade preprocesamiento de comandos directos para una respuesta más rápida a solicitudes comunes.

   .. code-block:: python

      direct_commands = {
          'turn on light': 'white',
          'turn off light': 'black',
          'red light': 'red',
          'green light': 'green',
          # ... etc
      }

----------------------------------------------

**Solución de problemas**

- Error "No module named 'openai'"

   Asegúrate de que el paquete fusion-hat esté instalado:

   .. code-block::

      curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/install-fusion-hat.sh | sudo bash


- Error "Invalid API key"

  Verifica que tu clave API en ``secret.py`` sea correcta y no haya expirado.
  Verifica las claves API activas en tu cuenta de OpenAI.

- El LED no se enciende

  - Verifica las conexiones del cableado (pines RGB a los puertos PWM correctos)
  - Verifica si el cátodo común está conectado a tierra
  - Asegúrate de que las resistencias limitadoras de corriente estén instaladas correctamente
  - Prueba cada canal de color individualmente usando código de prueba simple

- La IA no responde con etiquetas [LED:...]

  - Verifica que las instrucciones del sistema se estén configurando correctamente
  - Prueba con comandos de color más explícitos
  - Asegúrate de que el modelo de IA (gpt-4o) esté disponible en tu cuenta

- La respuesta en streaming aparece entrecortada

  - Verifica la estabilidad de la conexión a internet
  - Reduce el retardo del streaming ajustando los tiempos de espera de la red
  - Considera usar el modo sin streaming para pruebas

----------------------------------------------

¡Este proyecto demuestra cómo la IA puede tender un puente entre la comprensión del lenguaje natural y el control de hardware físico, abriendo posibilidades para interfaces humano-máquina intuitivas!