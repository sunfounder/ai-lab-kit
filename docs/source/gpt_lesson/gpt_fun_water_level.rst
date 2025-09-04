2.14 Water Level Monitoring System
=======================================================

Dieses Projekt ist ein **voice-controlled water level monitoring system**, das mit einem Ultraschallsensor den Wasserstand misst und über Spracherkennung sowie Text-to-Speech mit den Nutzern interagiert. Das System verwendet **OpenAI’s GPT-4**, um Sensordaten zu analysieren und Rückmeldungen zu geben, ob der Wasserstand normal, niedrig oder hoch ist. Die Kommunikation erfolgt per Spracheingabe, und der Assistent antwortet mit Echtzeit-Sprachausgabe.

----------------------------------------------

**Features**

- **Ultrasonic Sensor-Based Water Level Measurement**: Liest den Abstand zwischen Sensor und Wasseroberfläche.
- **Voice Interaction**: Nutzt **speech recognition (STT)** und **text-to-speech (TTS)** für eine freihändige Bedienung.
- **OpenAI GPT-4 Integration**: Verarbeitet Wasserstandsdaten und liefert kontextbezogene Antworten.
- **Real-Time Monitoring**: Liest Sensordaten kontinuierlich aus und aktualisiert den Assistenten fortlaufend.

----------------------------------------------

**What You’ll Need**

Hier sind die für dieses Projekt benötigten Komponenten:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT INTRODUCTION
        - PURCHASE LINK

    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_ultrasonic_sensor`
        - |link_ultrasonic_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -


----------------------------------------------

**Wiring Diagram**

.. image:: img/fzz/2.2.7_bb.png
   :width: 800
   :align: center


----------------------------------------------

**Running the Example**


Der komplette Beispielcode zu diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
So führen Sie das Beispiel aus:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_water_level.py 

----------------------------------------------

**Code**


.. raw:: html

   <run></run>
   
.. code-block:: python

    import openai
    from keys import OPENAI_API_KEY
    import readline  # Optimize keyboard input
    import sys
    import os
    import subprocess
    from pathlib import Path
    import speech_recognition as sr
    from fusion_hat import Ultrasonic,Pin
    import time
    import threading

    os.system("fusion_hat enable_speaker")

    # Initialize OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Initialize speech recognizer
    recognizer = sr.Recognizer()

    # Initialize the DistanceSensor using GPIO Zero library
    # Trigger pin is connected to GPIO 27, Echo pin to GPIO 22
    sensor = Ultrasonic(trig=Pin(27), echo=Pin(22))
    distance = 0

    # Function to fetch sensor data
    def fetch_sensor_data():
        global distance
        while True:
            dis = sensor.read()  # Measure distance in centimeters
            if dis > 0:
                distance = dis
            time.sleep(1)

    # Start a background thread for sensor data
    sensor_thread = threading.Thread(target=fetch_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()

    # Function for text-to-speech conversion
    def text_to_speech(text):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        try:
            with client.audio.speech.with_streaming_response.create(
                model="tts-1", voice="alloy", input=text
            ) as response:
                response.stream_to_file(speech_file_path)
            p=subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
        except Exception as e:
            print(f"Error in TTS: {e}")

    # Function for speech-to-text conversion
    def speech_to_text(audio_file):
        from io import BytesIO

        wav_data = BytesIO(audio_file.get_wav_data())
        wav_data.name = "record.wav"
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=wav_data, language=["zh", "en"]
        )
        return transcription.text

    # Function to redirect errors to null
    def redirect_error_to_null():
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        os.close(devnull)
        return old_stderr

    # Function to cancel redirected errors
    def cancel_redirect_error(old_stderr):
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

    # Create OpenAI assistant
    assistant = client.beta.assistants.create(
        name="Water Level Assistant",
        instructions=(
            "You are an assistant designed to help users monitor water levels using ultrasonic sensor data. The 'distance' refers to the measurement from the sensor to the surface of the water, which you will use to determine the current water level status. When a user sends you this distance along with a message, analyze the data to provide feedback on whether the water level is normal, low, or high based on preset thresholds. Offer advice or actions to take if the water levels are outside normal ranges."
        ),
        model="gpt-4-1106-preview",
    )

    # Create a conversation thread
    thread = client.beta.threads.create()

    try:
        while True:
            # Listen for user input
            print(f'\033[1;30m{"Listening..."}\033[0m')
            old_stderr = redirect_error_to_null()
            with sr.Microphone(chunk_size=8192) as source:
                cancel_redirect_error(old_stderr)
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            print(f'\033[1;30m{"Processing audio..."}\033[0m')

            # Convert speech to text
            user_message = speech_to_text(audio)
            if not user_message:
                print("No valid input detected.")
                continue

            # Prepare input for assistant
            assistant_input = {
                "distance": distance,
                "message": user_message,
            }

            # Send message to assistant
            message = client.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=str(assistant_input)
            )

            # Get assistant response
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant.id
            )

            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in messages.data:
                    if message.role == "assistant":
                        for block in message.content:
                            if block.type == "text":
                                response = block.text.value
                                print(f"Bot >>> {response}")
                                text_to_speech(response)
    
                        break
    finally:
        client.beta.assistants.delete(assistant.id)
        print("Cleaned up resources.")


----------------------------------------------

**Code Explanation**

Das Programm besteht aus mehreren Hauptkomponenten:

1. **Initializing OpenAI Assistant and Sensor**

.. code-block:: python

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    sensor = Ultrasonic(trig=Pin(27), echo=Pin(22))
    assistant = client.beta.assistants.create(
        name="Water Level Assistant",
        instructions="You are an assistant designed to help users monitor water levels...",
        model="gpt-4-1106-preview",
    )

- Initialisiert einen OpenAI-Assistenten mit spezifischen Anweisungen zur Wasserstandüberwachung.
- Konfiguriert den Ultraschallsensor mit seinen GPIO-Trigger- und Echo-Pins.

2. **Background Sensor Data Collection**

.. code-block:: python

    def fetch_sensor_data():
        global distance
        while True:
            dis = sensor.read()
            if dis > 0:
                distance = dis
            time.sleep(1)
    
    sensor_thread = threading.Thread(target=fetch_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()

- Liest den Abstand (Wasserstand) im Sekundentakt vom Ultraschallsensor.
- Läuft als Hintergrund-Thread, um Echtzeitdaten ohne Blockieren des Hauptprogramms bereitzustellen.

3. **Speech Recognition and Processing**

.. code-block:: python

    with sr.Microphone(chunk_size=8192) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    user_message = speech_to_text(audio)

- Erfasst Spracheingaben über ein Mikrofon.
- Konvertiert die Eingabe mit dem Modell ``whisper-1`` von OpenAI in Text.
- Unterstützt mehrsprachige Eingaben (Chinesisch und Englisch).

4. **Assistant Response Processing**

.. code-block:: python

    assistant_input = {
        "distance": distance,
        "message": user_message,
    }
    message = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=str(assistant_input)
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

- Sendet den Wasserstand und die Nutzeranfrage an den Assistenten.
- Wartet auf die Antwort des Assistenten und ruft sie anschließend ab.

5. **Text-to-Speech Conversion and Playback**

.. code-block:: python

    def text_to_speech(text):
        speech_file_path = Path(__file__).parent / "speech.mp3"
        with client.audio.speech.with_streaming_response.create(
            model="tts-1", voice="alloy", input=text
        ) as response:
            response.stream_to_file(speech_file_path)
        subprocess.Popen("mplayer speech.mp3", shell=True).wait()

- Wandelt die Textantwort des Assistenten in eine Audiodatei um.
- Gibt die generierte Sprachausgabe mit ``mplayer`` wieder.

6. **Error Handling for Microphone Input**

.. code-block:: python

    def redirect_error_to_null():
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull, 2)
        os.close(devnull)
        return old_stderr
    
    def cancel_redirect_error(old_stderr):
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

- Unterdrückt Mikrofon-/ALSA-Warnungen, um unnötige Ausgaben zu vermeiden.
- Stellt nach der Aufnahme den normalen Fehlerausgabekanal wieder her.

7. **Graceful Cleanup on Exit**

.. code-block:: python

    finally:
        client.beta.assistants.delete(assistant.id)
        print("Cleaned up resources.")

- Löscht beim Beenden die Instanz des OpenAI-Assistenten.
- Stellt sicher, dass reservierte Ressourcen ordnungsgemäß freigegeben werden.

----------------------------------------------

**Debugging Tips**

1. **Microphone Not Capturing Input?**

   - Umgebungsgeräusche prüfen und mittels ``recognizer.adjust_for_ambient_noise(source)`` kompensieren.

2. **Assistant Response Delayed or Missing?**

   - OpenAI-API-Zugangsdaten und Internetverbindung verifizieren.
   - Vor dem Senden ``assistant_input`` ausgeben, um das Format zu prüfen.

3. **No Audio Output?**

   - Installation von ``mplayer`` sicherstellen (``mplayer test.mp3``).
   - Prüfen, ob ``speech.mp3`` im richtigen Verzeichnis erzeugt wird.

4. **Sensor Not Providing Data?**

   - GPIO-Belegung kontrollieren (Trigger: GPIO 27, Echo: GPIO 22).
   - Rückgabewerte von ``sensor.read()`` zur Laufzeit ausgeben.

5. **Program Freezes or Crashes?**

   - Mit ``top`` / ``htop`` CPU-Auslastung prüfen.
   - Threading debuggen, indem in ``fetch_sensor_data()`` periodisch Statusmeldungen ausgegeben werden.

