.. _gpt_easy_tts:

1.4 Voice-Enabled Chatbot
==============================================

Dieses Beispiel baut auf :ref:`gpt_easy_keyboard` auf und erweitert den Chatbot um die Möglichkeit, seine Antworten als Sprache auszugeben. 
Die Implementierung integriert die TTS-API (Text-to-Speech) von OpenAI und einen lokalen Audioplayer für die Wiedergabe.

.. image:: img/fusionhat_spk.png

----------------------------------------------

**Running the Example**

Bevor Sie dieses Beispiel ausführen, stellen Sie sicher, dass auf Ihrem System ein kompatibler Audioplayer installiert ist.

Unter Linux installieren Sie ``mplayer`` mit:

.. code-block:: shell

   sudo apt install mplayer


Nach der Installation wechseln Sie in das Projektverzeichnis und starten das Skript:

.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy_tts.py


----------------------------------------------

**Code**

Der vollständige Beispielcode lautet wie folgt:

.. raw:: html

   <run></run>

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import readline # optimize keyboard input, only need to import
   import sys
   import subprocess
   from pathlib import Path

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)
   os.system("fusion_hat enable_speaker")

   TTS_OUTPUT_FILE = 'tts_output.mp3'

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions="You are a chat bot, you answer people question to help them. ",
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",  # Low-latency TTS model for real-time usage
         voice="alloy",  # Selected voice for audio playback
         input=text  # Text to convert to speech
      ) as response:
         response.stream_to_file(speech_file_path) # Save audio to the specified file

   try:
      while True:
         msg = ""
         msg = input(f'\033[1;30m{"intput: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')
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

         # print("Run completed with status: " + run.status)

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
                        print(f'{label:>10} >>> {value}')
                        text_to_speech(value)
                        p=subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        p.wait()
                  break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)

----------------------------------------------

**Code Explanation**

Hier sind die wichtigsten Stellen im Code, auf die Sie achten sollten:

.. code-block:: python
   :emphasize-lines: 5,6

   import openai
   from keys import OPENAI_API_KEY
   import readline # optimize keyboard input, only need to import
   import sys
   import subprocess
   from pathlib import Path


Die Bibliothek ``subprocess`` dient zum Ausführen von Systemkommandos – hier, um die Audiodatei abzuspielen. 

Die Bibliothek ``pathlib`` stellt plattformübergreifende Hilfsmittel zum Arbeiten mit Dateipfaden bereit.


.. code-block:: python

   os.system("fusion_hat enable_speaker")

Diese Zeile aktiviert Lautsprecher und Mikrofon auf dem Fusion HAT.



.. code-block:: python

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",
         voice="alloy",
         input=text
      ) as response:
         response.stream_to_file(speech_file_path)


Diese Funktion implementiert die Text-zu-Sprache-Ausgabe (TTS) mit der TTS-API von OpenAI (``audio.speech``-Modul). 
Sie wandelt den Eingabetext in Audio um und speichert ihn als MP3-Datei.

Der ``speech``-Endpunkt erwartet drei zentrale Eingaben:

* ``text``: Der in Audio umzuwandelnde Text.
* ``model``: Für Echtzeitanwendungen wird das latenzarme ``tts-1`` empfohlen. Für höhere Qualität steht ``tts-1-hd`` zur Verfügung. Beachten Sie, dass ``tts-1`` in bestimmten Situationen Rauschen erzeugen kann.
* ``voice``: Legt die verwendete Stimme fest. Verfügbare Optionen sind u. a. „alloy“, „echo“, „fable“, „onyx“, „nova“ und „shimmer“. Wählen Sie eine Stimme, die zum gewünschten Ton passt.

Die Funktion speichert den resultierenden Audiostream mit ``response.stream_to_file`` als ``speech.mp3`` im aktuellen Verzeichnis.


.. code-block:: python
   :emphasize-lines: 8,9,10

   for message in messages.data:
      if message.role == 'assistant':
         for block in message.content:
            if block.type == 'text':
               label = assistant.name
               value = block.text.value
               print(f'{label:>10} >>> {value}')
               text_to_speech(value)
               p=subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
               p.wait()
         break # only last reply

* ``text_to_speech``: Wandelt die Antwort des Assistenten in Audio um und speichert sie als ``speech.mp3``.
* ``subprocess.Popen``: Startet einen Subprozess, der die Audiodatei mit ``mplayer`` abspielt.
* ``p.wait()``: Stellt sicher, dass das Programm bis zum Ende der Wiedergabe wartet.


Dieses Setup sorgt dafür, dass der Chatbot sowohl in Textform als auch per Sprachausgabe reagiert – für ein ansprechendes Nutzererlebnis.


-------------------------------------------


**Error Handling**

Bei der Integration von Text-to-Speech (TTS) in Ihr Raspberry-Pi-Projekt können Fehler auftreten, die Leistung und Nutzererlebnis beeinträchtigen. Sorgfältiges Fehlermanagement ist entscheidend, um die Anwendung robust und zuverlässig zu halten. Nachfolgend häufige Probleme und wirksame Gegenmaßnahmen:

1. TTS API Errors

``Problem``: Probleme durch die TTS-API, z. B. überschrittene Ratenlimits, fehlerhafte Nutzung des API-Schlüssels oder unerwartete Serverfehler.

``Solution``: Platzieren Sie API-Aufrufe in ``try/except`` -Blöcken, um Ausnahmen abzufangen und Fallbacks bzw. Wiederholungen zu implementieren.


.. code-block:: python

   def text_to_speech(text):
      tts_path = Path(__file__).parent / "tts_output.mp3"
      try:
         with client.audio.speech.create(
               model="tts-1",
               voice="alloy",
               input=text
         ) as response:
               response.save_to_path(tts_path)
               subprocess.run(["mplayer", str(tts_path)], check=True)
      except openai.Error as e:
         print(f"Failed to generate speech: {e}")
         # Handle specific errors or implement a retry mechanism

2. Audio Playback Issues

``Problem``: Wiedergabefehler aufgrund fehlerhafter Audiokonfiguration, nicht unterstützter Formate oder Problemen mit mplayer.

``Solution``: Prüfen Sie die Audioeinstellungen und Abhängigkeiten. Fangen Sie ``subprocess``-Fehler ab und protokollieren Sie sie für die Analyse.


.. code-block:: python

   def play_audio(file_path):
      try:
         subprocess.run(["mplayer", file_path], check=True)
      except subprocess.CalledProcessError as e:
         print(f"Failed to play audio: {e}")
         # Check audio output settings or file existence

3. Network Connectivity Issues

``Problem``: Wie bei allen Cloud-Diensten können Netzwerkprobleme Anfragen scheitern lassen.

``Solution``: Implementieren Sie Retry-Logik mit exponentiellem Backoff für netzwerkbedingte Ausnahmen.


.. code-block:: python

   import time

   def reliable_request(call, *args, **kwargs):
      max_attempts = 5
      for attempt in range(max_attempts):
         try:
               return call(*args, **kwargs)
         except requests.ConnectionError:
               wait = 2 ** attempt
               print(f"Connection failed, retrying in {wait} seconds...")
               time.sleep(wait)
      raise Exception("Failed to connect after several attempts")

4. Resource Limitation Handling

``Problem``: Rechenintensive Vorgänge wie TTS können den Raspberry Pi auslasten.

``Solution``: Beobachten und optimieren Sie die Ressourcennutzung. Setzen Sie ggf. auf leichtere Modelle oder optimierte Einstellungen und informieren Sie Nutzerinnen/Nutzer bei Verzögerungen.


.. code-block:: python

   if sys.getsizeof(response.content) > some_threshold:
      print("Processing large data, this may take a while...")
      # Optionally, adjust parameters or simplify tasks

5. Handling Invalid Inputs

``Problem``: Nicht-Text-Eingaben oder leere Strings führen zu Fehlern oder unerwartetem Verhalten.

``Solution``: Validieren Sie Eingaben vor der TTS-Verarbeitung.


.. code-block:: python

   def validate_input(input_text):
      if not isinstance(input_text, str) or not input_text.strip():
         raise ValueError("Input must be a non-empty string")


Mit einer umfassenden Fehlerbehandlung erhöhen Sie die Zuverlässigkeit Ihres sprachfähigen Chatbots und verbessern das Nutzererlebnis durch klare Rückmeldungen und ein fehlertolerantes Verhalten – für eine professionellere, robustere Anwendung.