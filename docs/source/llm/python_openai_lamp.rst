.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_led_controller:

(Exemple) Controleur de LED alimente par l'IA
======================================

**Introduction**

Dans ce projet, vous allez construire un **controleur de LED alimente par l'IA** qui combine un modele LLM (ici nous utilisons le modele de langage GPT-4o d'OpenAI) avec une LED RGB. Le systeme interprete les commandes en langage naturel pour controler les couleurs de la LED, vous permettant de demander verbalement des couleurs specifiques en utilisant des noms de couleurs, des valeurs HEX ou des triplets RGB. Cela demontre l'integration de l'intelligence artificielle avec du materiel physique via le traitement du langage naturel.

Lorsque vous dites des commandes comme "turn on red light" ou "show warm yellow light", l'IA analyse votre demande et genere des signaux de controle appropries pour ajuster la LED en consequence.

Pour utiliser les autres modeles LLM, veuillez vous referer a :ref:`py_online_llm` .

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Led_Controller.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
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

**Schema de cablage**

Connectez la LED RGB au Fusion HAT+ comme suit :

.. image:: img/fzz/llm_book_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------------------

**Executer le code**


#. Executez le controleur de LED IA :

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_lamp.py

#. Lorsque le script s'execute :

   * Vous verrez un message de bienvenue : "Smart Lighting Assistant started!"
   * Tapez des commandes en langage naturel comme :

     - "turn on red light"
     - "show blue color"
     - "set to warm white"
     - "turn off the light"

   * L'IA repondra et controlera la LED en consequence
   * Tapez 'quit' ou 'exit' pour terminer le programme

----------------------------------------------

**Code**

Voici le script Python complet pour le Controleur de LED IA :

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
                           print(f"Applied color: {led_command}")
                       else:
                           print(f"Unrecognized color format: {led_command}")

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

**Comprendre le code**

1. Initialisation de l'assistant IA

   Le systeme utilise le modele GPT-4o d'OpenAI avec des instructions personnalisees pour garantir qu'il genere des commandes de controle LED dans un format specifique.

   .. code-block:: python

      self.llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      self.instructions = """You are an AI assistant that can control an RGB LED...
         ...End with [LED:color] where color can be:...
      """

      self.llm.set_instructions(self.instructions)

2. Controle de la LED RGB

   La classe RGB_LED de fusion_hat.modules fournit une interface pour controler les trois canaux de couleur via PWM.

   .. code-block:: python

      self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)

      # Set color using RGB tuple
      self.rgb_led.color((255, 0, 0))  # Red

      # Set color using hex value
      self.rgb_led.color(0xFF0000)  # Also red

3. Analyse des commandes avec expressions regulieres

   Le systeme utilise regex pour extraire les commandes de controle LED de la reponse de l'IA.

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

4. Prise en charge de plusieurs formats de couleur

   Le controleur accepte differents formats de specification de couleur pour une flexibilite maximale.

   .. code-block:: python

      def apply_color(self, color_spec):
          """Convert color specification to RGB and apply to LED"""
          color_spec = color_spec.lower().strip()

          # 1. Color names (red, green, blue, etc.)
          # 2. HEX strings (#FF0000)
          # 3. RGB tuples ((255,0,0))
          # 4. Hex numbers (0xFF0000)
          # 5. Direct integers (16711680)

5. Reponse en continu

   La reponse de l'IA est diffusee mot par mot pour une experience de conversation plus naturelle.

   .. code-block:: python

      response = self.llm.prompt(user_input, stream=True)

      full_response = ""
      for word in response:
          if word:
              print(word, end="", flush=True)
              full_response += word

6. Version Pro amelioree

   La classe AILEDControllerPro ajoute un pre-traitement des commandes directes pour une reponse plus rapide aux demandes courantes.

   .. code-block:: python

      direct_commands = {
          'turn on light': 'white',
          'turn off light': 'black',
          'red light': 'red',
          'green light': 'green',
          # ... etc
      }

----------------------------------------------

**Depannage**

- Erreur "No module named 'openai'"

   Assurez-vous que le package fusion-hat est installe :

   .. code-block::

      curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/install-fusion-hat.sh | sudo bash

- Erreur "Invalid API key"

  Verifiez que votre cle API dans ``secret.py`` est correcte et n'a pas expire.
  Verifiez votre compte OpenAI pour les cles API actives.

- La LED ne s'allume pas

  - Verifiez les connexions de cablage (broches RGB vers les ports PWM corrects)
  - Verifiez si la cathode commune est connectee a la masse
  - Assurez-vous que les resistances de limitation de courant sont correctement installees
  - Testez chaque canal de couleur individuellement avec un code de test simple

- L'IA ne repond pas avec les balises [LED:...]

  - Verifiez que les instructions du systeme sont correctement definies
  - Essayez des commandes de couleur plus explicites
  - Assurez-vous que le modele IA (gpt-4o) est disponible sur votre compte

- La reponse en continu semble saccadee

  - Verifiez la stabilite de la connexion Internet
  - Reduisez le delai de streaming en ajustant les timeouts reseau
  - Envisagez d'utiliser le mode non-streaming pour les tests

----------------------------------------------

Ce projet demontre comment l'IA peut faire le pont entre la comprehension du langage naturel et le controle de materiel physique, ouvrant des possibilites pour des interfaces homme-machine intuitives !