2.15 Weather Assistant
==================================

Dieses Projekt zeigt, wie ein interaktiver Wetter-Assistent erstellt wird, der per Sprachbefehl in Echtzeit Kleiderempfehlungen auf Basis der lokalen Wetterlage gibt. 

Der Assistent ist bewusst einfach, intuitiv und alltagstauglich gehalten – etwa, um schnell zu entscheiden, was man bei aktuellem Wetter anziehen sollte. Das Projekt eignet sich ideal, um zu demonstrieren, wie sprachgesteuerte KI und IoT-Technologien zu einem praktischen, benutzerfreundlichen System zusammenwirken.

----------------------------------------------

**Features**

* Voice Interaction: Erfasst Nutzeranfragen über ein Mikrofon und verarbeitet sie mit dem Whisper-Modell von OpenAI für die Sprach-zu-Text-Umwandlung.

* Weather Fetching: Ruft Echtzeit-Wetterdaten der OpenWeatherMap-API für eine angegebene Stadt ab.

* LCD Display: Zeigt kompakte Wetterinformationen (z. B. Temperatur, Luftfeuchte) auf einem 16×2-LCD an.

* Clothing Suggestions: Nutzt OpenAI GPT-4, um Wetterlage und Nutzerfragen auszuwerten und passende Kleidung vorzuschlagen.

* Text-to-Speech: Wandelt die von GPT generierten Texte in Sprache um – für einen dialogartigen Nutzungsfluss.

----------------------------------------------

**What You’ll Need**

Für dieses Projekt werden folgende Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK


    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_i2c_lcd`
        - |link_i2clcd1602_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -


----------------------------------------------

**Diagram**

.. image:: img/fzz/1.1.7_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Get OpenWeather API keys**

|link_openweather| ist ein Online-Dienst von OpenWeather Ltd, der über APIs globale Wetterdaten bereitstellt – darunter aktuelle Wetterwerte, Vorhersagen, Nowcasts sowie historische Daten für beliebige Orte.

#. |link_openweather| aufrufen und einloggen/registrieren.

    .. image:: img/OWM-1.png


#. In der Navigationsleiste zur API-Seite wechseln.

    .. image:: img/OWM-2.png


#. **Current Weather Data** finden und auf Subscribe klicken.

    .. image:: img/OWM-3.png


#. Unter **Current weather and forecasts collection** den passenden Dienst abonnieren. Für dieses Projekt reicht Free aus.

   .. image:: img/OWM-4.png


#. Den Schlüssel auf der Seite **API keys** kopieren.

   .. image:: img/OWM-5.png

#. Die Datei ``keys.py`` mit folgendem Befehl öffnen:

   .. code-block:: shell

      nano ~/ai-explorer-lab-kit/gpt_example/keys.py

#. Den kopierten API-Schlüssel einfügen:

   .. code-block:: shell
      :emphasize-lines: 2

      OPENAI_API_KEY = "sk-proj-vEBo7Ahxxxx-xxxxx-xxxx"
      OPENWEATHER_API_KEY = "732exxxxxxxxxxxxxxxxxxxxx919b"


#. Mit ``Ctrl + X``, ``Y`` und anschließend ``Enter`` speichern und beenden.



----------------------------------------------

**Running the Example**


Der gesamte Beispielcode zu diesem Tutorial liegt im Verzeichnis ``ai-explorer-lab-kit``.  
So führen Sie das Beispiel aus:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_weather.py




----------------------------------------------

**Code**



.. raw:: html

   <run></run>
   
.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY, OPENWEATHER_API_KEY
   from pathlib import Path
   import sys,os,subprocess
   import speech_recognition as sr
   import time
   import json
   import requests
   # pip install requests

   from fusion_hat import LCD1602  # Import module for interfacing with lcd

   os.system("fusion_hat enable_speaker")

   # Initialize LCD with I2C address 0x27 and enable backlight
   lcd=LCD1602(0x27, 1) 

   # LCD Initialization
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   # OpenAI Assistant Setup
   assistant = client.beta.assistants.create(
      name="Weather Butler",
      instructions=(
         "You are a weather assistant. Based on the provided local weather data, "
         "offer appropriate clothing recommendations in natural language. "
         "Your responses will be converted to speech, so avoid symbols like braces."
      ),
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()
   recognizer = sr.Recognizer()

   def speech_to_text(audio_file):
      """
      Convert speech audio to text using OpenAI Whisper model.
      """
      from io import BytesIO

      try:
         wav_data = BytesIO(audio_file.get_wav_data())
         wav_data.name = "record.wav"
         transcription = client.audio.transcriptions.create(
               model="whisper-1", file=wav_data, language=["zh", "en"]
         )
         return transcription.text
      except Exception as e:
         print(f"Error in speech-to-text: {e}")
         return ""

   def redirect_error_2_null():
      devnull = os.open(os.devnull, os.O_WRONLY)
      old_stderr = os.dup(2)
      sys.stderr.flush()
      os.dup2(devnull, 2)
      os.close(devnull)
      return old_stderr

   def cancel_redirect_error(old_stderr):
      os.dup2(old_stderr, 2)
      os.close(old_stderr)

   def sox_volume(input_file, output_file):
      """
      Adjust the volume of an audio file using the sox library.
      """
      import sox

      VOLUME_DB=3  # The volume adjustment in decibels (increase by 3 dB)
      try:
         transform = sox.Transformer()
         transform.vol(VOLUME_DB)
         transform.build(input_file, output_file)
         return True 
      except Exception as e:
         print(f"sox_volume err: {e}")
         return False

   def text_to_speech(text):
      """
      Convert text to speech using OpenAI TTS model.
      """
      speech_file_path = Path(__file__).parent / "speech.wav"
      speech_file_path_db = Path(__file__).parent / "speech_db.wav"
      try:
         with client.audio.speech.with_streaming_response.create(
               model="tts-1", voice="alloy", input=text, response_format="wav"
         ) as response:
               response.stream_to_file(speech_file_path)
         sox_volume(speech_file_path,speech_file_path_db)
         subprocess.Popen(
               ["mplayer", str(speech_file_path_db)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
         ).wait()
         os.remove(str(speech_file_path))
         os.remove(str(speech_file_path_db))
      except Exception as e:
         print(f"Error in text-to-speech: {e}")

   def get_weather(api_key, city):
      """
      Fetch current weather data for a given city.
      """
      try:
         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
         response = requests.get(url)
         response.raise_for_status() 
         return response.json()
      
      except requests.RequestException as e:
         print("Error: ", e)

   def lcd_print(weather_data):
      """
      Update the LCD display with weather information.
      """
      if not weather_data:
         lcd.clear()
         lcd.write(0, 0, "Weather Unavailable")
         return

      weather=weather_data["weather"][0]["main"]
      t=weather_data["main"]["temp"]
      rh=weather_data["main"]["humidity"]

      lcd.clear() 
      time.sleep(0.2)
      lcd.write(0,0,f'{weather}')
      lcd.write(0,1,f'{t}{"°C"} {rh}%rh')

   try:
      while True:
         print(f'\033[1;30m{"listing... "}\033[0m')
         _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
         with sr.Microphone(chunk_size=8192) as source:
               cancel_redirect_error(_stderr_back) # restore error print
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)
         print(f'\033[1;30m{"stop listening... "}\033[0m')

         msg = ""
         msg = speech_to_text(audio)
         if msg == False or msg == "":
               print() # new line
               continue

         weather_data=get_weather(OPENWEATHER_API_KEY, 'shenzhen')
         lcd_print(weather_data)
         
         message_content = {
               "weather": weather_data,
               "message": msg,
         }

         # Send the user's message and weather data to the assistant
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=str(message_content),
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
                              response = block.text.value
                              print(f'{assistant.name:>10} >>> {response}')
                              text_to_speech(response)
                     break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up.")


----------------------------------------------

**Code Explanation**

1. Libraries and Hardware Initialization

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY, OPENWEATHER_API_KEY
   from pathlib import Path
   import sys,os,subprocess
   import speech_recognition as sr
   import time
   import json
   import requests
   from fusion_hat import LCD1602 

* OpenAI API: Anbindung von GPT-4 und Whisper.
* OpenWeatherMap API: Abruf von Wetterdaten in Echtzeit.
* LCD1602-Modul: Ansteuerung des 16×2-LCD zur Anzeige der Wetterdaten.
* SpeechRecognition: Erfasst Mikrofoneingaben und wandelt sie für die Texterkennung auf.

2. LCD, Speaker and OpenAI Setup

.. code-block:: python

   os.system("fusion_hat enable_speaker")

   # Initialize LCD with I2C address 0x27 and enable backlight
   lcd=LCD1602(0x27, 1) 

   # LCD Initialization
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   # OpenAI Assistant Setup
   assistant = client.beta.assistants.create(
      name="Weather Butler",
      instructions=(
         "You are a weather assistant. Based on the provided local weather data, "
         "offer appropriate clothing recommendations in natural language. "
         "Your responses will be converted to speech, so avoid symbols like braces."
      ),
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()
   recognizer = sr.Recognizer()

* Speaker-Initialisierung: Aktiviert den Lautsprecher des Fusion HAT.
* LCD-Initialisierung: Setzt die I2C-Adresse und aktiviert die Hintergrundbeleuchtung.
* OpenAI-Assistent: Erstellt einen auf wetterbasierte Empfehlungen spezialisierten GPT-4-Assistenten.
* Thread und Recognizer: Initialisiert den Thread für den Assistenten sowie den Recognizer für STT.

3. Speech-to-Text Conversion

.. code-block:: python

   def speech_to_text(audio_file):
      from io import BytesIO
      try:
         wav_data = BytesIO(audio_file.get_wav_data())
         wav_data.name = "record.wav"
         transcription = client.audio.transcriptions.create(
               model="whisper-1", file=wav_data, language=["zh", "en"]
         )
         return transcription.text
      except Exception as e:
         print(f"Error in speech-to-text: {e}")
         return ""

* Verwendet OpenAI Whisper für die Spracherkennung; unterstützt u. a. Chinesisch und Englisch.

4. Text-to-Speech Conversion

.. code-block:: python

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.wav"
      speech_file_path_db = Path(__file__).parent / "speech_db.wav"
      try:
         with client.audio.speech.with_streaming_response.create(
               model="tts-1", voice="alloy", input=text, response_format="wav"
         ) as response:
               response.stream_to_file(speech_file_path)
         sox_volume(speech_file_path,speech_file_path_db)
         subprocess.Popen(
               ["mplayer", str(speech_file_path_db)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
         ).wait()
         os.remove(str(speech_file_path))
         os.remove(str(speech_file_path_db))
      except Exception as e:
         print(f"Error in text-to-speech: {e}")

* Wandelt GPT-Antworten per TTS-API in Sprache um.
* Die Wiedergabe erfolgt via ``mplayer``.

5. Weather Data Retrieval

.. code-block:: python

   def get_weather(api_key, city):
      try:
         url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
         response = requests.get(url)
         response.raise_for_status() 
         return response.json()
      
      except requests.RequestException as e:
         print("Error: ", e)

* Ruft Wetterdaten der angegebenen Stadt über die OpenWeatherMap-API ab.

6. LCD Display Update

.. code-block:: python

   def lcd_print(weather_data):
      """
      Update the LCD display with weather information.
      """
      if not weather_data:
         lcd.clear()
         lcd.write(0, 0, "Weather Unavailable")
         return

      weather=weather_data["weather"][0]["main"]
      t=weather_data["main"]["temp"]
      rh=weather_data["main"]["humidity"]

      lcd.clear() 
      time.sleep(0.2)
      lcd.write(0,0,f'{weather}')
      lcd.write(0,1,f'{t}{"°C"} {rh}%rh')

* Aktualisiert die LCD-Anzeige mit den abgerufenen Wetterwerten.

7. Main Loop

.. code-block:: python

   try:
      while True:
         print(f'\033[1;30m{"listing... "}\033[0m')
         _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
         with sr.Microphone(chunk_size=8192) as source:
               cancel_redirect_error(_stderr_back) # restore error print
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)
         print(f'\033[1;30m{"stop listening... "}\033[0m')

         msg = ""
         msg = speech_to_text(audio)
         if msg == False or msg == "":
               print() # new line
               continue

         weather_data=get_weather(OPENWEATHER_API_KEY, 'shenzhen')
         lcd_print(weather_data)
         
         message_content = {
               "weather": weather_data,
               "message": msg,
         }

         # Send the user's message and weather data to the assistant
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=str(message_content),
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
                              response = block.text.value
                              print(f'{assistant.name:>10} >>> {response}')
                              text_to_speech(response)
                     break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up.")

* Voice Input: Erfasst Nutzeranfragen per Mikrofon.
* Weather Fetching: Ruft Wetterdaten für die festgelegte Stadt ab.
* Assistant Interaction: Übergibt Wetterdaten und Nutzeranfrage an GPT-4 und verarbeitet die Antwort.
* Output: Zeigt Werte auf dem LCD an und gibt die Empfehlungen per TTS aus.

----------------------------------------------

**Debugging Tips**

#. No Voice Input Detected:
   
   * Prüfen, ob das Mikrofon korrekt angeschlossen und konfiguriert ist.
   * Hintergrundgeräusche minimieren, da sie die Erkennung stören können.

#. Weather Data Unavailable:
   
   * OpenWeatherMap-API-Schlüssel und Internetverbindung verifizieren.
   * Sicherstellen, dass die angegebene Stadt gültig ist.

#. No Response from Assistant:
   
   * Gültigkeit des OpenAI-API-Schlüssels prüfen.
   * Überprüfen, ob der Assistent korrekt initialisiert wurde.

#. LCD Not Displaying:
   
   * I2C-Verkabelung und Adresse kontrollieren.
   * Das LCD-Modul bei Bedarf neu starten.
