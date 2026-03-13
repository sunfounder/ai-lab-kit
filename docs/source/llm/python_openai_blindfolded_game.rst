.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
   
.. _py_blindfolded_watermelon_game:

(Beispiel) Blindfold-Wassermelonen-Zerschlagspiel
====================================================

**Einführung**

Dieses Projekt erstellt ein interaktives **Blindfold-Wassermelonen-Zerschlagspiel**, bei dem sich Spieler mithilfe eines Joysticks auf einem 20×20-Meter-Raster bewegen und dabei auf die Richtungsanweisungen eines AI-Assistenten angewiesen sind. Das System integriert:

1. **Joystick-Steuerung** für die Bewegung des Spielers auf der X-/Y-Achse
2. **AI-gestützte Führung** mit OpenAI GPT-4
3. **Text-to-Speech-Feedback** mit Pico2Wave
4. **Zufällige Zielgenerierung** für die Position der Wassermelone
5. **Interaktive Taste** für die Schlagaktion

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Blindfolded_Watermelon_Smashing_Game.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Der Spieler startet in der Mitte bei (0,0) und muss eine zufällig platzierte Wassermelone finden, wobei er sich ausschließlich auf die Audiohinweise des AI-Assistenten verlässt. Dadurch entsteht ein spannendes Spielerlebnis mit sensorischer Einschränkung.

Sie können verschiedene Eingabegeräte mit LLM-Modulen kombinieren, um interaktive AI-Spiele zu entwickeln. Siehe:

* :ref:`py_online_llm` 
* :ref:`tts_espeak_pico2wave`
* :ref:`py_joystick`

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
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

**Schaltplan**

Verbinden Sie die Komponenten wie folgt mit dem Fusion HAT+:

.. image:: img/fzz/watermelon_game_bb.png
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
      sudo python3 llm_openai_blindfolded_game.py

#. Das Spiel spielen

   Nach dem Start des Skripts wird die Wassermelone zufällig auf dem 20×20 Meter großen Spielfeld platziert.
   Bewegen Sie sich mit dem Joystick Schritt für Schritt und hören Sie auf die Richtungsanweisungen des AI-Assistenten.

   Wenn Sie glauben, die Position der Wassermelone erreicht zu haben, drücken Sie die Taste, um zuzuschlagen.
   Stimmen Ihre Koordinaten exakt mit der Position der Wassermelone überein, gewinnen Sie das Spiel.

#. Spielmechanik verstehen

   * Koordinatensystem:

     - Das Spielfeld ist ein 20×20-Meter-Raster
     - Die Koordinaten reichen von (-10,-10) bis (10,10)
     - Positives X = Osten, negatives X = Westen
     - Positives Y = Süden, negatives Y = Norden (invertierte Y-Achse)
     - Der Mittelpunkt ist (0,0)

   * Bewegungsregeln:

     - Joystick nach rechts → X+1 (Osten)
     - Joystick nach links → X-1 (Westen)
     - Joystick nach oben → Y-1 (Norden)
     - Joystick nach unten → Y+1 (Süden)
     - Jede Bewegung verändert die Position um 1 Meter

   * Gewinnbedingung:

     - Der Spieler muss sich genau auf den Koordinaten der Wassermelone befinden
     - Drücken Sie die Taste, um an der aktuellen Position zu „zerschlagen“
     - Bei exakter Übereinstimmung endet das Spiel mit einer Siegmeldung

   * Rolle des AI-Assistenten:

     - Erhält sowohl die Koordinaten des Spielers als auch der Wassermelone
     - Gibt Richtungsanweisungen anhand der Himmelsrichtungen (N, NE, E, SE, S, SW, W, NW)
     - Gibt eine ungefähre Entfernung in Metern an
     - Hält die Antworten kurz, damit sie sich gut für die Audiowiedergabe eignen


**Code**

Hier ist das vollständige Python-Skript für das Blindfold-Wassermelonen-Zerschlagspiel:

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

**Code verstehen**

1. Text-to-Speech-Einrichtung

   Das Spiel verwendet Pico2Wave für die Audioausgabe:
   
   .. code-block:: python
   
      tts = Pico2Wave()
      tts.set_lang('en-US')
   
   Dadurch werden die Textantworten der AI in gesprochene englische Anweisungen umgewandelt.

2. Verarbeitung der Joystick-Eingaben

   Der Joystick verwendet zwei ADC-Kanäle zum Auslesen der X- und Y-Achse:
   
   .. code-block:: python
   
      x_axis = ADC('A1')  # Horizontale Bewegung
      y_axis = ADC('A0')  # Vertikale Bewegung
      
      def MAP(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
      
      # ADC-Wert von 0–4095 auf Bereich -100 bis 100 umrechnen
      x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
      y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

3. Taster mit Interrupt einrichten

   Der Taster verwendet einen Interrupt-Callback für eine sofortige Reaktion:
   
   .. code-block:: python
   
      btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
      
      def activate():
          global smash_tips
          smash_tips = True
              
      btn_pin.when_activated = activate
   
   Wenn der Taster gedrückt wird, setzt er ``smash_tips`` auf ``True`` und löst dadurch im Hauptprogramm die Schlagaktion aus.

4. OpenAI-LLM-Konfiguration

   Der AI-Assistent wird mit spezifischen Spielanweisungen konfiguriert:
   
   .. code-block:: python
   
      INSTRUCTIONS = "This is a blindfolded watermelon-smashing game..."
      WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant..."
      
      llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )
      
      llm.set_max_messages(20)       # Gesprächsverlauf speichern
      llm.set_instructions(INSTRUCTIONS)  # Spielregeln festlegen
      llm.set_welcome(WELCOME)       # Begrüßung festlegen

5. Verwaltung des Spielzustands

   Das Spiel speichert die Positionen des Spielers und des Ziels:
   
   .. code-block:: python
   
      # Zufällige Platzierung der Wassermelone
      watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
      
      # Spieler startet in der Mitte
      player_x, player_y = 0, 0
      
      # Bewegungsschwellenwert (80 % Joystick-Auslenkung)
      if x_val > 80:
          player_x += 1      # Nach rechts bewegen
      elif x_val < -80:
          player_x -= 1      # Nach links bewegen
          
      if y_val > 80:
          player_y -= 1      # Nach oben bewegen (negatives Y)
      elif y_val < -80:
          player_y += 1      # Nach unten bewegen (positives Y)

6. Schlagaktion und AI-Antwort

   Wenn der Taster gedrückt wird, überprüft das Spiel, ob ein Treffer vorliegt oder ob eine AI-Anweisung benötigt wird:
   
   .. code-block:: python
   
      if smash_tips:
          smash_tips = False
          print("Smash!")
          
          if (player_x, player_y) == (watermelon_x, watermelon_y):
              print("Target hit!")
              tts.say("Target hit!")
              break  # Spiel endet
          else:
              # Positionen an die AI senden
              input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"
              
              # Streaming-Antwort von der AI abrufen
              response = llm.prompt(input_text, stream=True)
              string = ""
              
              for next_word in response:
                  if next_word:
                      string += next_word
                      
              print("AI: " + string)
              tts.say(string)  # Anleitung aussprechen

7. Verarbeitung der Streaming-Antwort

   Die AI-Antwort wird Wort für Wort verarbeitet, um eine mögliche Echtzeitanzeige zu ermöglichen:
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      string = ""
      
      for next_word in response:
          if next_word:
              # Zum Anzeigen während des Empfangs auskommentieren entfernen
              # print(next_word, end="", flush=True)
              string += next_word

8. Bewegungslogik mit Dead-Zone

   Der Joystick hat eine Dead-Zone von 80 Einheiten, um unbeabsichtigte Bewegungen zu vermeiden:
   
   .. code-block:: python
   
      # Bewegung nur, wenn der Joystick >80 % in eine Richtung gedrückt wird
      # Dies verhindert Drift aus der Mittelposition
      if x_val > 80:    # Rechts
      elif x_val < -80: # Links
      
      if y_val > 80:    # Oben
      elif y_val < -80: # Unten

9. Struktur der Spielschleife

   Die Hauptschleife des Spiels führt kontinuierlich folgende Schritte aus:

   1. Joystick-Position lesen
   2. Spielerkoordinaten aktualisieren, wenn der Joystick bewegt wird
   3. Prüfen, ob der Schlag-Taster gedrückt wurde
   4. AI-Antworten verarbeiten, falls erforderlich
   5. Audiofeedback über TTS ausgeben

----------------------------------------------

**Fehlerbehebung**

- Keine Reaktion vom Joystick

  - ADC-Verbindungen prüfen: A0 für Y-Achse, A1 für X-Achse
  - Stromversorgung prüfen: VCC an 3.3V, GND an Masse
  - ADC-Werte testen: ``print(x_axis.read())`` sollte Werte von 0–4095 anzeigen
  - Sicherstellen, dass der Joystick zentriert ist (sollte etwa ~2048 anzeigen)


- Kein Ton bei TTS

  - Audioausgabe prüfen: ``sudo raspi-config`` → **System Options** → **Audio**
  - Lautsprecher testen: ``speaker-test -t sine -f 440``
  - Sicherstellen, dass Pico2Wave installiert ist: ``pico2wave --help``
  - Lautstärke prüfen: ``alsamixer``
  - Audio-Setup-Skript erneut ausführen: ``sudo /opt/setup_fusion_hat_audio.sh``

- OpenAI-API-Fehler

  - API-Schlüssel in ``secret.py`` prüfen
  - Internetverbindung testen: ``ping 8.8.8.8``
  - Sicherstellen, dass die Abrechnung im OpenAI-Konto aktiviert ist
  - Prüfen, ob das Modell „gpt-4o“ für Ihr Konto verfügbar ist

- Spieler bewegt sich zu schnell/langsam

  - Bewegungsschwelle anpassen (derzeit 80): höher = größere Joystick-Auslenkung erforderlich
  - Bewegungsschritt ändern (derzeit 1): z. B. 0.5 für feinere Steuerung
  - Wartezeit anpassen (derzeit 0.3 s): längere Zeit = langsamere Bewegung

- AI-Antworten sind zu lang

  - Kürzere Antworten in den ``INSTRUCTIONS`` festlegen
  - Beispiel hinzufügen: **„Respond in 10 words or less.“**
  - Begrenzung der Antwortlänge im Code implementieren

----------------------------------------------

Dieses Blindfold-Wassermelonenspiel zeigt, wie physische Steuerungen, AI-gestützte Führung und Audiofeedback kombiniert werden können, um ein spannendes sensorisches Spielerlebnis zu schaffen, das räumliches Denken und Zuhörfähigkeiten herausfordert.