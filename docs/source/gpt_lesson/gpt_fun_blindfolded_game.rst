2.11 Blindfolded Watermelon-smashing Game
==================================================

Dieses Projekt ist ein interaktives Spiel „Blindfolded Watermelon-smashing“, das von OpenAI GPT-4 und einem joystickbasierten Steuersystem betrieben wird. Dabei wird eine virtuelle Wassermelone zufällig in einem 20x20-Meter-Bereich platziert. Der Spieler, der am Ursprungspunkt (0,0) startet, bewegt sich mithilfe eines Joysticks durch das Spielfeld und versucht, die Melone durch Drücken des Joystick-Buttons zu treffen. Nach jedem Versuch gibt die KI eine Richtungsanweisung, um dem Spieler beim Auffinden des Ziels zu helfen. Die Antworten des Assistenten werden per Sprachsynthese ausgegeben, um ein immersives Spielerlebnis zu schaffen.

----------------------------------------

**Features**

- **OpenAI GPT-4 Integration**: Der Assistent verarbeitet Spieleraktionen und liefert sprachliche Hinweise in Echtzeit.
- **Joystick-Based Navigation**: Die Bewegung erfolgt über einen analogen Joystick, der auf ein Koordinatensystem abgebildet ist.
- **Button-Based Smashing Action**: Ein physischer Button löst den Schlagversuch aus.
- **Text-to-Speech (TTS)**: Die Antworten der KI werden mit dem TTS-Modell von OpenAI in Sprache umgewandelt.
- **Randomized Watermelon Placement**: Die Position der Wassermelone wird bei jedem Durchlauf neu bestimmt, um Abwechslung im Gameplay zu garantieren.
- **Real-Time Position Updates**: Der Spieler erhält Rückmeldungen sowohl zu seiner eigenen Position als auch zur Lage des Ziels.

----------------------------------------

**What You’ll Need**

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT INTRODUCTION
        - PURCHASE LINK

    *   - :ref:`cpn_joystick`
        - 
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------

**Wiring Diagram**


.. image:: img/fzz/2.1.9_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Running the Example**


Der gesamte Beispielcode zu diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``. 
So führst du das Beispiel aus:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_blindfolded_game.py 

----------------------------------------

**Code**


.. raw:: html

   <run></run>
   
.. code-block:: python

    import openai
    from keys import OPENAI_API_KEY
    import time
    from fusion_hat import Pin, ADC
    import sys, os
    import subprocess
    from pathlib import Path
    import random

    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    assistant = client.beta.assistants.create(
        name="BOT",
        instructions="This is a blindfolded watermelon-smashing game. A point representing a watermelon is randomly generated within a 20x20 meter area with coordinates ranging from (-10,-10) to (10,10). The player starts from the origin (0,0) and moves using a joystick. Even if the player can't see anything, they press a button to perform a smash action. After smashing, you will receive the watermelon's and player's coordinates. You need to advise the player on the direction of the watermelon, like 'The watermelon is ten meters to your northeast.' If the smash coordinates match, the game ends. Your responses will be converted into speech via TTS, so please keep them brief, ideally within two sentences.",
        model="gpt-4-1106-preview",
    )

    thread = client.beta.threads.create()
    os.system("fusion_hat enable_speaker")

    # Setup GPIO ports
    btn_pin = Pin(17, Pin.IN, Pin.PULL_UP)
    x_axis = ADC('A1')
    y_axis = ADC('A0')

    def MAP(x, in_min, in_max, out_min, out_max):
        """
        Map a value from one range to another.
        """
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def text_to_speech(text):
        """
        Convert text to speech and play it using an external player.
        """
        speech_file_path = Path(__file__).parent / "speech.mp3"
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",  # Low-latency TTS model for real-time usage
            voice="alloy",  # Selected voice for audio playback
            input=text  # Text to convert to speech
        ) as response:
            response.stream_to_file(speech_file_path)  # Save audio to the specified file
        p = subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

    def activate():
        global smash_tips
        smash_tips = True
            
    watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
    player_x, player_y = 0, 0
    btn_pin.when_activated = activate

    try:
        text_to_speech("game start!")
        smash_tips = True
        # Main loop to read and print ADC values and button state
        while True:
            x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
            y_val = MAP(y_axis.read(), 0, 4095, -100, 100)
            if x_val > 80:
                player_x += 1
            elif x_val < -80:
                player_x -= 1
            if y_val > 80:
                player_y += 1
            elif y_val < -80:
                player_y -= 1

            print('Watermelon position: %d, %d  ' % (watermelon_x, watermelon_y))
            print('Player position: %d, %d  ' % (player_x, player_y))

            time.sleep(0.3)

            if smash_tips:
                smash_tips = False
                print("Smash!")
                send_message = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

                try:
                    message = client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=send_message,
                    )

                    run = client.beta.threads.runs.create_and_poll(
                        thread_id=thread.id,
                        assistant_id=assistant.id,
                    )

                    if run.status == "completed":
                        messages = client.beta.threads.messages.list(thread_id=thread.id)

                        for message in messages.data:
                            if message.role == 'assistant':
                                for block in message.content:
                                    if block.type == 'text':
                                        decoded_message = block.text.value
                                break  # Only take the last reply

                    print("Assistant:", decoded_message)
                    text_to_speech(decoded_message)
                    if (player_x, player_y) == (watermelon_x, watermelon_y):
                        print("Target hit!")
                        break
                except Exception as e:
                    print(f"Error in AI processing: {e}")
        print("Good Game. Bye!")

    finally:
        client.beta.assistants.delete(assistant.id)
        print("\n Delete Assistant ID")

----------------------------------------

**Code Explanation**

Das Spiel ist in mehrere zentrale Komponenten gegliedert:

1. **Initializing OpenAI GPT-4 Assistant**

.. code-block:: python

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    assistant = client.beta.assistants.create(
        name="BOT",
        instructions="This is a blindfolded watermelon-smashing game...",
        model="gpt-4-1106-preview",
    )

- Initialisiert einen OpenAI-Assistenten mit spezifischen Anweisungen, wie er auf Spieleraktionen reagieren soll.
- Der Assistent gibt nach jedem Schlagversuch Richtungsanweisungen, um den Spieler zum Ziel zu führen.

2. **Mapping Joystick Input to Movement**

.. code-block:: python

    def MAP(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    x_axis = ADC('A1')
    y_axis = ADC('A0')
    
    x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
    y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

- Die Joystick-Werte werden als ADC-Signale (0–4095) eingelesen und in einen Koordinatenbereich von -100 bis 100 abgebildet.
- Die Bewegung erfolgt anhand von Schwellwerten:

.. code-block:: python

    if x_val > 80:
        player_x += 1
    elif x_val < -80:
        player_x -= 1
    if y_val > 80:
        player_y += 1
    elif y_val < -80:
        player_y -= 1

3. **Smash Attempt and AI Response Processing**

- Beim Drücken des Buttons wird ein Schlagversuch ausgelöst und eine Nachricht an OpenAI gesendet:

.. code-block:: python

    send_message = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=send_message,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

- Die KI wertet die Nachricht aus und gibt Hinweise, wie weit der Spieler vom Ziel entfernt ist.
- Stimmen Spieler- und Zielkoordinaten überein, endet das Spiel mit einer Siegesmeldung.

4. **Text-to-Speech Output**

.. code-block:: python

    def text_to_speech(text):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=text
        ) as response:
            response.stream_to_file(speech_file_path)
        subprocess.Popen("mplayer speech.mp3", shell=True).wait()

- Wandelt die Antworten der KI in Sprache um und spielt sie mit ``mplayer`` ab.

5. **Game Loop and Termination**

.. code-block:: python

    try:
        text_to_speech("game start!")
        while True:
            # Read joystick values, update position
            # Process smashing logic
            if (player_x, player_y) == (watermelon_x, watermelon_y):
                print("Target hit!")
                break
    finally:
        client.beta.assistants.delete(assistant.id)
        print("\n Delete Assistant ID")

- Führt eine Dauerschleife aus, in der der Spieler navigiert und Schlagversuche ausführt.
- Nach Spielende wird die Assistenteninstanz gelöscht, um Ressourcen freizugeben.

----------------------------------------

**Debugging Tips**

1. **Joystick reagiert nicht?**

   - Verkabelung prüfen und sicherstellen, dass ADC-Werte korrekt eingelesen werden.
   - Mit ``x_axis.read()`` und ``y_axis.read()`` die Eingabewerte verifizieren.

2. **Keine Audioausgabe?**

   - Prüfen, ob ``mplayer`` installiert und funktionsfähig ist (``mplayer test.mp3``).
   - Die erzeugte Datei ``speech.mp3`` auf Fehler kontrollieren.

3. **Assistent antwortet nicht?**

   - API-Key und Internetverbindung überprüfen.
   - Den Status der KI-Antworten ausgeben, um Fehler zu erkennen.

4. **Spiel endet zu früh?**

   - Bewegungslogik debuggen, um sicherzustellen, dass die Spielerposition korrekt aktualisiert wird.
   - Die Werte von ``(player_x, player_y)`` in jeder Iteration ausgeben, um Bewegungen nachzuvollziehen.

