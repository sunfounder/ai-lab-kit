.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_led_controller:

(Beispiel) AI-gestützter LED-Controller
===================================================

**Einführung**

In diesem Projekt erstellen Sie einen **AI-gestützten LED-Controller**, der ein LLM-Modell (hier verwenden wir das Sprachmodell GPT-4o von OpenAI) mit einer RGB-LED kombiniert. Das System interpretiert natürliche Sprachbefehle zur Steuerung der LED-Farben, sodass Sie per Sprache bestimmte Farben über Farbnamen, HEX-Werte oder RGB-Tupel anfordern können. Dieses Projekt demonstriert die Verbindung von künstlicher Intelligenz mit physischer Hardware durch natürliche Sprachverarbeitung.

Wenn Sie Befehle wie „schalte rotes Licht ein“ oder „zeige warmgelbes Licht“ geben, analysiert die AI Ihre Anweisung und erzeugt passende Steuersignale, um die LED entsprechend anzupassen.

Wenn Sie andere LLM-Modelle verwenden möchten, lesen Sie bitte :ref:`py_online_llm` .

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Led_Controller.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
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

**Schaltplan**

Verbinden Sie die RGB-LED wie folgt mit dem Fusion HAT+:

.. image:: img/fzz/llm_book_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------------------

**Code ausführen**


#. Den AI-LED-Controller starten:

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_lamp.py

#. Wenn das Skript ausgeführt wird:

   * Sie sehen eine Begrüßungsmeldung: "Smart Lighting Assistant started!"
   * Geben Sie natürliche Sprachbefehle ein, zum Beispiel:

     - "turn on red light"
     - "show blue color"  
     - "set to warm white"
     - "turn off the light"

   * Die AI antwortet und steuert die LED entsprechend
   * Geben Sie 'quit' oder 'exit' ein, um das Programm zu beenden

----------------------------------------------

**Code**

Hier ist das vollständige Python-Skript für den AI-LED-Controller:

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

**Code verstehen**

1. Initialisierung des AI-Assistenten

   Das System verwendet das GPT-4o-Modell von OpenAI mit benutzerdefinierten Anweisungen, damit es LED-Steuerbefehle in einem bestimmten Format generiert.

   .. code-block:: python

      self.llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )
      
      self.instructions = """You are an AI assistant that can control an RGB LED...
         ...End with [LED:color] where color can be:...
      """
      
      self.llm.set_instructions(self.instructions)

2. RGB-LED-Steuerung

   Die Klasse RGB_LED aus fusion_hat.modules bietet eine Schnittstelle zur Steuerung der drei Farbkanäle über PWM.

   .. code-block:: python

      self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
      
      # Farbe über RGB-Tupel setzen
      self.rgb_led.color((255, 0, 0))  # Rot
      
      # Farbe über HEX-Wert setzen
      self.rgb_led.color(0xFF0000)  # Ebenfalls Rot

3. Befehlsanalyse mit regulären Ausdrücken

   Das System verwendet Regex, um LED-Steuerbefehle aus der AI-Antwort zu extrahieren.

   .. code-block:: python

      def parse_led_command(self, text):
          """LED-Steuerbefehl aus der AI-Antwort extrahieren"""
          pattern = r'\[LED:(.*?)\]'
          match = re.search(pattern, text)
          
          if not match:
              return None, text
              
          led_command = match.group(1).strip()
          display_text = re.sub(pattern, '', text).strip()
          
          return led_command, display_text

4. Unterstützung mehrerer Farbformate

   Der Controller akzeptiert verschiedene Farbformate für maximale Flexibilität.

   .. code-block:: python

      def apply_color(self, color_spec):
          """Farbangabe in RGB umwandeln und auf LED anwenden"""
          color_spec = color_spec.lower().strip()
          
          # 1. Farbnamen (red, green, blue usw.)
          # 2. HEX-Strings (#FF0000)
          # 3. RGB-Tupel ((255,0,0))
          # 4. HEX-Zahlen (0xFF0000)
          # 5. Direkte Integerwerte (16711680)

5. Streaming-Antwort

   Die AI-Antwort wird Wort für Wort gestreamt, um eine natürlichere Interaktion zu ermöglichen.

   .. code-block:: python

      response = self.llm.prompt(user_input, stream=True)
      
      full_response = ""
      for word in response:
          if word:
              print(word, end="", flush=True)
              full_response += word

6. Erweiterte Pro-Version

   Die Klasse AILEDControllerPro fügt eine direkte Vorverarbeitung häufiger Befehle hinzu, um schneller auf typische Anfragen zu reagieren.

   .. code-block:: python

      direct_commands = {
          'turn on light': 'white',
          'turn off light': 'black',
          'red light': 'red',
          'green light': 'green',
          # ... usw.
      }

----------------------------------------------

**Fehlerbehebung**

- Fehler „No module named 'openai'“

   Stellen Sie sicher, dass das Paket fusion-hat installiert ist:  

   .. code-block::

      curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/install-fusion-hat.sh | sudo bash


- Fehler „Invalid API key“

  Überprüfen Sie, ob der API-Schlüssel in ``secret.py`` korrekt ist und noch gültig ist.  
  Prüfen Sie außerdem in Ihrem OpenAI-Konto, ob aktive API-Schlüssel vorhanden sind.

- LED leuchtet nicht

  - Überprüfen Sie die Verkabelung (RGB-Pins müssen mit den richtigen PWM-Ports verbunden sein)  
  - Prüfen Sie, ob die gemeinsame Kathode mit GND verbunden ist  
  - Stellen Sie sicher, dass Vorwiderstände korrekt eingesetzt sind  
  - Testen Sie jeden Farbkanal einzeln mit einfachem Testcode

- AI gibt keine [LED:...] Tags zurück

  - Prüfen Sie, ob die Systemanweisungen korrekt gesetzt werden  
  - Versuchen Sie eindeutigere Farbbefehle  
  - Stellen Sie sicher, dass das AI-Modell (gpt-4o) in Ihrem Konto verfügbar ist

- Streaming-Ausgabe wirkt ruckelig

  - Überprüfen Sie die Stabilität Ihrer Internetverbindung  
  - Reduzieren Sie mögliche Verzögerungen durch Anpassung von Netzwerk-Timeouts  
  - Verwenden Sie zum Testen den Nicht-Streaming-Modus

----------------------------------------------

Dieses Projekt zeigt, wie AI das Verständnis natürlicher Sprache mit der Steuerung physischer Hardware verbinden kann und eröffnet neue Möglichkeiten für intuitive Mensch-Maschine-Schnittstellen.