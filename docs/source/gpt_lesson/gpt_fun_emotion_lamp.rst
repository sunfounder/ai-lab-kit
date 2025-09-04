Voice-Activated Smart Lamp Control
======================================

In diesem Beispiel kombinieren wir Spracherkennung, Text-to-Speech-Synthese und die Steuerung eines IoT-Geräts, um eine sprachgesteuerte Smart-Lampe zu realisieren. Nutzer können per Sprachbefehl die Farbe einer RGB-Lampe ändern und erhalten dabei eine freundliche Audio-Rückmeldung.

Dieses Projekt macht nicht nur Spaß, sondern zeigt auch das Potenzial von GPT-Modellen in Smart-Home-Anwendungen.

----------------------------------------------

**Features**

Das Projekt umfasst folgende Funktionen:

* **Voice Input**: Erfasst Sprachbefehle über ein Mikrofon und wandelt sie in Text um.
* **GPT Response Generation**: Nutzt GPT, um die Nutzerintention zu interpretieren und sowohl Lampenfarbe als auch Audio-Feedback zurückzugeben.
* **RGB Lamp Control**: Stellt die Farbe einer RGB-Lampe anhand der von GPT gelieferten RGB-Werte ein.
* **Audio Feedback**: Wandelt die Textantwort von GPT in Sprache um und spielt sie dem Nutzer vor.


----------------------------------------------


**What You’ll Need**

Die folgenden Komponenten werden für dieses Projekt benötigt:


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
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------


**Diagram**

.. image:: img/fzz/1.1.2_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Running the Example**


Der gesamte Beispielcode zu diesem Tutorial ist im Verzeichnis ``ai-explorer-lab-kit`` verfügbar. 
Gehe wie folgt vor, um das Beispiel auszuführen:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_emotion_lamp.py 

----------------------------------------------

**Code**


.. raw:: html

   <run></run>
   
.. code-block:: python
         
   import openai
   from keys import OPENAI_API_KEY
   from pathlib import Path

   import readline # optimize keyboard input, only need to import
   import sys
   import os
   import subprocess

   import speech_recognition as sr
   from fusion_hat import RGB_LED, PWM

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   os.system("fusion_hat enable_speaker")

   TTS_OUTPUT_FILE = 'tts_output.mp3'

   instructions_text = '''
   You are a smart lamp assistant. Your role is to respond to user commands by providing two outputs: 
   1. A color in RGB format to control the lamp.
   2. A textual response to the user.

   **Input Format**:
   The user will provide a command describing their mood or desired lighting condition in plain text (e.g., "I feel happy" or "Set a relaxing light").

   **Output Requirements**:
   1. Return a JSON output with no extraneous text or wrappers:
   - `color`: A list of three floating-point values representing the RGB color components (each between 0 and 1).
   - `message`: A textual response to the user.

   **Example JSON Output**:
   {
   "color": [0.5, 0.4, 0.2],
   "message": "Setting a warm and relaxing light for you."
   }
   '''

   # assistant=client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()
   recognizer = sr.Recognizer()

   # Initialize an RGB LED.
   rgb_led = RGB_LED(PWM('P0'), PWM('P1'), PWM('P2'),common=RGB_LED.CATHODE)


   recognizer.dynamic_energy_adjustment_damping = 0.15
   recognizer.dynamic_energy_ratio = 1
   recognizer.operation_timeout = None  # seconds after an internal operation (e.g., an API request) starts before it times out, or ``None`` for no timeout
   recognizer.pause_threshold = 1

   def speech_to_text(audio_file):
      from io import BytesIO

      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "record.wav"

      transcription = client.audio.transcriptions.create(
         model="whisper-1", 
         file=wav_data,
         language=['zh','en']
      )
      return transcription.text

   def redirect_error_2_null():
      # https://github.com/spatialaudio/python-sounddevice/issues/11

      devnull = os.open(os.devnull, os.O_WRONLY)
      old_stderr = os.dup(2)
      sys.stderr.flush()
      os.dup2(devnull, 2)
      os.close(devnull)
      return old_stderr

   def cancel_redirect_error(old_stderr):
      os.dup2(old_stderr, 2)
      os.close(old_stderr)


   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",
         voice="alloy",
         input=text
      ) as response:
         response.stream_to_file(speech_file_path)
      p=subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      p.wait()


   try:
      rgb_led.color(0xFF00FF)  # light up the LED to indicate that the program is running
      while True:
         msg = ""
         # msg = input(f'\033[1;30m{"intput: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')

         print(f'\033[1;30m{"listening... "}\033[0m')
         _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
         with sr.Microphone(chunk_size=8192) as source:
               cancel_redirect_error(_stderr_back) # restore error print
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)
         
         print(f'\033[1;30m{"stop listening... "}\033[0m')
         # with open("stt-rec.wav", "wb") as f:
         #     f.write(audio.get_wav_data())
         # os.system('play stt-rec.wav')

         msg = speech_to_text(audio)

         if msg == False or msg == "":
               print() # new line
               continue

         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=msg,
         )

         run = client.beta.threads.runs.create_and_poll(
               thread_id=thread.id,
               assistant_id=assistant.id,
         )

         if run.status == "completed":
               messages = client.beta.threads.messages.list(thread_id=thread.id)

               for message in messages.data:
                  if message.role == 'user':
                     for block in message.content:
                           if block.type == 'text':
                              label = message.role 
                              value = block.text.value
                              print(f'{label:>10} >>> {value}')
                     break # only last reply

               for message in messages.data:
                  if message.role == 'assistant':
                     for block in message.content:
                           if block.type == 'text':
                              label = assistant.name
                              value = block.text.value
                              #print(f'value: {value}')
                              try:
                                 value = eval(value)
                              except Exception as e:
                                 value = str(value)
                              if isinstance(value, dict):
                                 if 'color' in value:
                                       color = list(value['color'])
                                 else:
                                       color = [0,0,0]
                                 if 'message' in value:
                                       text = value['message']
                                 else :
                                       text = ''
                              else:
                                 color = [0,0,0]
                                 text = value

                              print(f'{label:>10} >>> {text} {color}')
                              rgb_led.color = color
                              text_to_speech(text)
                     break # only last reply

   finally:
      rgb_led.color(0x000000)  
      client.beta.assistants.delete(assistant.id)

----------------------------------------------

**Code Explanation**

1. **Import Libraries**

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   from pathlib import Path
   import readline # optimize keyboard input, only need to import
   import sys
   import os
   import subprocess
   import speech_recognition as sr
   from fusion_hat import RGB_LED, PWM

* **openai**: Zur Interaktion mit der OpenAI-API.
* **speech_recognition**: Erfasst Sprachbefehle und wandelt sie in Text um.
* **fusion_hat**: Zur Ansteuerung der physischen RGB-LED-Hardware.
* **subprocess**: Führt Systembefehle wie die Audiowiedergabe aus.
* **sys**, **os**: Für Pfad-, Ein-/Ausgabe- und weitere Systemfunktionen.

2. **Initialize OpenAI Client**

.. code-block:: python

   client = openai.OpenAI(api_key=OPENAI_API_KEY)

Verwendet den OpenAI-API-Schlüssel (``OPENAI_API_KEY``), um eine Clientinstanz für GPT-Interaktionen, TTS und Transkription zu erstellen.

3. **Create a GPT Assistant**

.. code-block:: python

   instructions_text = '''
   You are a smart lamp assistant. Your role is to respond to user commands by providing two outputs:
   1. A color in RGB format to control the lamp.
   2. A textual response to the user.

   **Input Format**:
   The user will provide a command describing their mood or desired lighting condition in plain text (e.g., "I feel happy" or "Set a relaxing light").

   **Output Requirements**:
   1. Return a JSON output with no extraneous text or wrappers:
   - `color`: A list of three floating-point values representing the RGB color components (each between 0 and 1).
   - `message`: A textual response to the user.

   **Example JSON Output**:
   {
   "color": [0.5, 0.4, 0.2],
   "message": "Setting a warm and relaxing light for you."
   }
   '''
   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4-1106-preview",
   )

Definiert das Verhalten des Assistenten:

   * **instructions_text**: Legt Eingabeformat und erwartete Ausgabe fest.
   * **create**: Erstellt einen auf Smart-Lamp-Anfragen zugeschnittenen GPT-Assistenten.

4. **Initialize Core Components**

.. code-block:: python

   thread = client.beta.threads.create()
   recognizer = sr.Recognizer()
   rgb_led = RGB_LED(PWM('P0'), PWM('P1'), PWM('P2'),common=RGB_LED.CATHODE)
   os.system("fusion_hat enable_speaker")

* **Thread**: Hält den Gesprächskontext mit dem Assistenten.
* **Speech Recognizer**: Erfasst und verarbeitet Spracheingaben.
* **RGB LED**: Steuert die physische Lampe über GPIO-Pins.
* **Speaker**: Aktiviert die Audioausgabe für Assistenten-Antworten.

5. **Configure Speech Recognizer**

.. code-block:: python

   recognizer.dynamic_energy_adjustment_damping = 0.15
   recognizer.dynamic_energy_ratio = 1
   recognizer.operation_timeout = None
   recognizer.pause_threshold = 1

* **Dynamische Energieschwelle**: Passt sich Umgebungsgeräuschen an.
* **Pause-Schwellwert**: Definiert die Stille-Dauer, die eine Aufnahme beendet.

6. **Convert Speech to Text**

.. code-block:: python

   def speech_to_text(audio_file):
      from io import BytesIO
      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "record.wav"
      transcription = client.audio.transcriptions.create(
         model="whisper-1",
         file=wav_data,
         language=['zh', 'en']
      )
      return transcription.text

* **Functionality**: Verwendet OpenAI Whisper, um aufgezeichnete Audiodaten in Text zu transkribieren.

* **Implementation**:

  * Konvertiert Audiodaten in ein In-Memory-Dateiobjekt.
  * Unterstützt mehrsprachige Transkription (z. B. Englisch und Chinesisch).

7. **Convert Text to Speech**

.. code-block:: python

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",
         voice="alloy",
         input=text
      ) as response:
         response.stream_to_file(speech_file_path)

* **Functionality**: Erzeugt aus der Textantwort des Assistenten eine MP3-Audiodatei.

* **Details**:

  * Verwendet das Modell ``tts-1`` für die Echtzeit-Audiogenerierung.
  * Speichert die Audiodatei im aktuellen Verzeichnis.

8. **Capture User Voice Input**

.. code-block:: python

   try:
      while True:
         ...
         with sr.Microphone(chunk_size=8192) as source:
               ...
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)

* Verwendet ein Mikrofon als Audioeingangsquelle.
* Passt sich dynamisch an Hintergrundgeräusche an, um die Qualität zu verbessern.
* Erfasst die Spracheingabe des Nutzers und speichert sie als ``audio``-Objekt.

9. **Send Transcribed Text to GPT**

.. code-block:: python

   if msg == False or msg == "":
      print() # new line
      continue

   message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=msg,
   )

* Wandelt die Spracheingabe des Nutzers in Text (``msg``) um.
* Sendet die transkribierte Nachricht an den GPT-Assistenten.

10. **Retrieve GPT Response**

.. code-block:: python

   run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
   )
   if run.status == "completed":
      ...
      for message in messages.data:
         if message.role == 'assistant':
               ...

* Führt die Logik des Assistenten aus und ruft dessen Antwort ab.
* Parst die Antwort, um die Ausgabewerte des Assistenten zu extrahieren.

11. **Parse GPT JSON Response**

.. code-block:: python

   try:
      value = eval(value)
      if isinstance(value, dict):
         color = value.get('color', [0, 0, 0])
         text = value.get('message', '')

* Wandelt die JSON-Antwort des Assistenten mittels ``eval`` in ein Python-Dictionary um.
* Extrahiert ``color`` (RGB-Werte) und ``message`` (Textantwort).

12. **Control Lamp and Play Audio**

.. code-block:: python

   rgb_led.color = color
   text_to_speech(text)
   p = subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
   p.wait()

* **Lamp Control**: Stellt die Lampenfarbe anhand der RGB-Werte ein.
* **Audio Playback**: Wandelt Text in Sprache um und spielt die Ausgabe über ``mplayer`` ab.

13. **Clean Up Resources**

.. code-block:: python

   finally:
      client.beta.assistants.delete(assistant.id)

Sorgt für eine ordnungsgemäße Bereinigung, indem die Assistenteninstanz gelöscht wird, um Ressourcen freizugeben.


----------------------------------------------

**Debugging Tips**

1. **RGB LED Issues**:

   * Überprüfe die GPIO-Pin-Belegung.

2. **Speech Recognition Issues**:

   * Reduziere Hintergrundgeräusche.
   * Stelle die Funktionsfähigkeit des Mikrofons sicher.

3. **GPT Response Errors**:

   * Verifiziere, dass die Assistenten-Anweisungen das erwartete JSON-Format eindeutig definieren.
   * Nutze ``print``, um Rohantworten zu debuggen.

4. **TTS Playback Issues**:

   * Stelle sicher, dass ``mplayer`` installiert und funktionsfähig ist.
   * Prüfe, ob die erzeugte MP3-Datei gültig ist.
   * Achte darauf, dass der Befehl ``fusion_hat enable_speaker`` ausgeführt wurde.
