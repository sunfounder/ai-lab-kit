2.8 Morse-Code-Decoder
============================

Dieses Projekt ist ein Morse-Code-Decoder, der Tastendrücke als Morsezeichen interpretiert. Kurze Tastendrücke werden als Punkte erkannt, lange Tastendrücke als Striche. Das System sammelt diese Eingaben und sendet sie an einen OpenAI-gestützten Assistenten zur Decodierung. Nach der Auswertung wird die übersetzte Nachricht in der Konsole angezeigt.

----------------------------------------------

**Features**

- **Morse Code Input**: Tastenbetätigungen repräsentieren Morsezeichen.
- **Real-Time Signal Processing**: Erfasst Druck- und Loslasszeiten, um Punkte und Striche zu unterscheiden.
- **AI-Based Decoding**: Sendet Morse-Sequenzen zur Interpretation an OpenAI.
- **Start/Stop Button**: Steuert den Eingabesitzungsmodus.
- **LED Indicator**: Signalisiert, wenn die Morse-Eingabe aktiv ist.

----------------------------------------------

**Benötigte Komponenten**

Für dieses Projekt benötigen Sie folgende Bauteile:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - KOMPONENTE
        - KAUFLINK

    *   - :ref:`cpn_breadboard`
        - |link_breadboard_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_micro_switch`
        - \-
    *   - :ref:`cpn_capacitor`
        - |link_capacitor_buy|        
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------

**Schaltplan**

.. image:: img/fzz/gpt_morse_decoder_bb.png
   :width: 800
   :align: center



----------------------------------------------

**Beispiel ausführen**


Der gesamte Beispielcode dieses Tutorials befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_morse_decoder.py 

----------------------------------------------

**Code**


.. raw:: html

   <run></run>

.. code-block:: python


    import openai
    from keys import OPENAI_API_KEY
    from fusion_hat import Pin
    from signal import pause
    import time

    # init openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    assistant = client.beta.assistants.create(
        name="BOT",
        instructions="You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it.",
        model="gpt-4-1106-preview",
    )

    thread = client.beta.threads.create()

    # setup GPIO
    morse_input = Pin(22, Pin.IN, pull= Pin.PULL_DOWN)  
    start_stop_button = Pin(17, Pin.IN, pull= Pin.PULL_DOWN)  
    led = Pin(27, Pin.OUT)  # indicate LED to GPIO 27

    # store the morse code events
    morse_events = []
    input_active = False  # flag to indicate if the input is active

    # send the morse code to the AI for decoding
    def decode_and_speak():
        global morse_events
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=str(morse_events),
            )

            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
        )

            # print("Run completed with status: " + run.status)

            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)

                for message in messages.data:
                    if message.role == 'assistant':
                        for block in message.content:
                            if block.type == 'text':
                                decoded_message = block.text.value
                        break # only last reply

            print(f"Decoded Message: {decoded_message}")
        except Exception as e:
            print(f"Error in decoding: {e}")
        morse_events = []  # clear the morse code events

    # morse code input
    start_time = 0

    def morse_input_pressed():
        global start_time
        start_time = time.time()  

    def morse_input_released():
        release_time = time.time()  
        if release_time - start_time < 0.1:
            return  # debounce
        morse_events.append(('pressed', start_time))
        morse_events.append(('released', release_time))
        print(f" Pressed at {start_time}-{release_time}")

    # start/stop button
    def handle_start_stop():
        global input_active
        if input_active:
            led.off()
            print("Input stopped and decoded.")
            decode_and_speak()
            input_active = False
        else:
            input_active = True
            morse_events.clear()
            led.on()
            print("Input started.")

    # add event listeners
    morse_input.when_activated = morse_input_pressed
    morse_input.when_deactivated = morse_input_released
    start_stop_button.when_activated = handle_start_stop

    try:
        print("Morse Code Decoder is running. Press CTRL+C to exit.")
        handle_start_stop()
        pause()

    finally:
        client.beta.assistants.delete(assistant.id)
        print("\n Delete Assistant ID")

----------------------------------------------

**Code Erklärung**

Dieses Projekt gliedert sich in mehrere zentrale Funktionsbereiche:

1. **Initialisierung und Einrichtung:**

   - Importiert erforderliche Module, darunter ``openai`` für die KI-Verarbeitung und ``fusion_hat`` für die GPIO-Ansteuerung.
   - Richtet den OpenAI-API-Client über ``OPENAI_API_KEY`` ein.
   - Konfiguriert GPIO-Pins für die Morse-Eingabe, einen Start/Stop-Taster sowie eine LED-Anzeige.

2. **Verarbeitung der Morse-Eingaben:**

   - Zeichnet Zeitstempel für Tastendruck- und -loslassereignisse auf.
   - Bestimmt anhand der Druckdauer, ob es sich um einen Punkt oder einen Strich handelt.

   .. code-block:: python

       def morse_input_pressed():
           global start_time
           start_time = time.time()
       
       def morse_input_released():
           release_time = time.time()
           if release_time - start_time < 0.1:
               return  # debounce
           morse_events.append(('pressed', start_time))
           morse_events.append(('released', release_time))
           print(f" Pressed at {start_time}-{release_time}")

3. **Start/Stop-Taster:**

   - Steuert Beginn und Ende der Morse-Eingabe.
   - Löscht frühere Eingaben bei Neustart.
   - Löst beim Beenden die Decodierung aus.

   .. code-block:: python

       def handle_start_stop():
           global input_active
           if input_active:
               led.off()
               print("Input stopped and decoded.")
               decode_and_speak()
               input_active = False
           else:
               input_active = True
               morse_events.clear()
               led.on()
               print("Input started.")

4. **Morse-Decodierung**:

   - Sendet die gesammelten Morse-Ereignisse an OpenAI.
   - Ruft den decodierten Text ab und gibt ihn aus.

   .. code-block:: python

       def decode_and_speak():
           global morse_events
           try:
               message = client.beta.threads.messages.create(
                   thread_id=thread.id,
                   role="user",
                   content=str(morse_events),
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
                           break
               print(f"Decoded Message: {decoded_message}")
           except Exception as e:
               print(f"Error in decoding: {e}")
           morse_events = []

5. **Systemschleife und Aufräumen:**

   - Verwendet ``pause()``, um das Programm unbegrenzt laufen zu lassen.
   - Räumt beim Beenden Ressourcen auf und löscht den OpenAI-Assistenten.

   .. code-block:: python

       try:
           print("Morse Code Decoder is running. Press CTRL+C to exit.")
           handle_start_stop()
           pause()
       finally:
           client.beta.assistants.delete(assistant.id)
           print("\n Delete Assistant ID")

----------------------------------------------

**Debugging Tipps**

- **Button presses not registering?**

  - Überprüfen Sie die GPIO-Verbindungen und stellen Sie sicher, dass die Taster korrekt verdrahtet sind.
  - Geben Sie ``morse_events`` aus, um zu prüfen, ob Eingaben erfasst werden.

- **Incorrect Morse code interpretation?**

  - Passen Sie das Entprell-Intervall an, falls kurze Tastendrücke übersehen werden.
  - Verifizieren Sie, dass die Zeitstempel korrekt aufgezeichnet werden.

- **AI not responding?**

  - Stellen Sie sicher, dass der OpenAI-API-Schlüssel gültig ist.
  - Prüfen Sie die Netzwerkverbindung, damit API-Aufrufe funktionieren.

- **LED indicator not working?**

  - Prüfen Sie, ob ``led.on()`` und ``led.off()`` an den richtigen Stellen aufgerufen werden.
  - Verifizieren Sie, dass der korrekte GPIO-Pin der LED zugewiesen ist.

