.. _gpt_easy_stt:

1.5 Speech-to-Text Chatbot
===========================================

Dieses Beispiel baut auf :ref:`gpt_easy_tts` auf und erweitert den Chatbot so, dass er nicht nur sprechen, sondern auch gesprochene Nutzereingaben verstehen kann. Durch die Integration der OpenAI-Whisper-API für Speech-to-Text (STT) kann der Chatbot nun Spracheingaben annehmen und dialogorientierte Antworten liefern.


Speech-to-Text-Technologie ermöglicht Chatbots eine natürlichere und barriereärmere Interaktion mit Nutzerinnen und Nutzern. Das ist besonders nützlich für freihändige Bedienung, Accessibility-Anwendungen und Systeme für die Echtzeitkommunikation.

.. image:: img/fusionhat_mic.png


----------------------------------------------

**Running the Example**


Der gesamte in diesem Tutorial verwendete Beispielcode befindet sich im Verzeichnis ``ai-explorer-lab-kit``. 
Gehen Sie wie folgt vor, um das Beispiel auszuführen:


.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy_stt.py


----------------------------------------------

**Code**

Hier ist der vollständige Beispielcode:

.. raw:: html

   <run></run>

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import readline # optimize keyboard input, only need to import
   import sys
   import os
   import subprocess
   from pathlib import Path

   import speech_recognition as sr

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   TTS_OUTPUT_FILE = 'tts_output.mp3'

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions="You are a chat bot, you answer people question to help them.",
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()
   recognizer = sr.Recognizer()
   os.system("fusion_hat enable_speaker")


   # speech_recognition init
   # =================================================================
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
      # print(speech_file_path)
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",
         voice="alloy",
         input=text
      ) as response:
         response.stream_to_file(speech_file_path)

   try:
      while True:
         msg = ""
         # Notify user that recording has started
         print(f'\033[1;30m{"listening... "}\033[0m')
         # Redirect error messages to suppress ALSA warnings
         _stderr_back = redirect_error_2_null() 
         with sr.Microphone(chunk_size=8192) as source:
               # Restore standard error output
               cancel_redirect_error(_stderr_back)
               # Adjust for ambient noise to filter background sound
               recognizer.adjust_for_ambient_noise(source)
               # Record user speech
               audio = recognizer.listen(source)
         print(f'\033[1;30m{"stop listening... "}\033[0m')

         # Optional: Save and playback the recorded audio for debugging
         # This is for testing purposes and can be removed in production
         with open("stt-rec.wav", "wb") as f:
               f.write(audio.get_wav_data())
         os.system('play stt-rec.wav')

         # Convert recorded audio to text
         msg = speech_to_text(audio)

         if msg == False or msg == "":
               print() # new line
               continue

         # Pass the transcribed text to the chatbot
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=msg,
         )

         # Generate and process the assistant's response
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

Die wichtigsten Punkte aus dem Code:

.. code-block:: python

   import speech_recognition as sr
   import os

Die Bibliothek ``speech_recognition`` ist eine leistungsfähige und flexible Python-Bibliothek, um Audioeingaben 
von Mikrofonen oder Dateien zu erfassen und Spracherkennung durchzuführen. 

Die Bibliotheken ``os`` und ``subprocess`` dienen分别 für Dateioperationen bzw. das Ausführen von Systemkommandos.


.. code-block:: python

   os.system("fusion_hat enable_speaker")

Diese Zeile aktiviert Lautsprecher und Mikrofon auf dem Fusion HAT.


.. code-block:: python

   recognizer = sr.Recognizer()
   recognizer.dynamic_energy_adjustment_damping = 0.15
   recognizer.dynamic_energy_ratio = 1
   recognizer.operation_timeout = None 
   recognizer.pause_threshold = 1

Der Recognizer wird so konfiguriert, dass Audioeingaben robust verarbeitet werden. Die wichtigsten Parameter im Überblick:


.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   *  - Parameter
      - Standardwert
      - Beschreibung
   *  - energy_threshold
      - 300
      - Schwellwert zur Unterscheidung von Hintergrundgeräusch und Sprache. In lauter Umgebung erhöhen.
   *  - dynamic_energy_threshold
      - True
      - Passt den Schwellwert vor jeder Aufnahme automatisch an die Umgebungsgeräusche an.
   *  - dynamic_energy_adjustment_damping
      - 0.15
      - Bestimmt, wie schnell sich der dynamische Schwellwert verändert. Kleinere Werte reagieren schneller.
   *  - dynamic_energy_ratio
      - 1.5
      - Verhältnis des dynamischen Schwellwerts zum Umgebungslärm. Höhere Werte erfordern lautere Sprache.
   *  - pause_threshold
      - 0.8
      - Länge der Stille, nach der eine Äußerung als beendet gilt. Für längere Sprechpausen erhöhen.
   *  - operation_timeout
      - None 
      - Maximale Wartezeit für Erkennungsvorgänge. ``None`` bedeutet ohne Timeout.
   *  - phrase_threshold
      - 0.3
      - Dauer, nach der ein Sprachsegment als abgeschlossen gilt.
   *  - non_speaking_duration
      - 0.5
      - Erlaubt kurze Stille vor und nach der Sprache, um vollständige Phrasen zu erfassen.


.. code-block:: python

   def redirect_error_2_null():
      ...

   def cancel_redirect_error(old_stderr):
      ...

   while True:

      ...

      print(f'\033[1;30m{"listening... "}\033[0m')
      _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
      with sr.Microphone(chunk_size=8192) as source:
         cancel_redirect_error(_stderr_back) # restore error print
         recognizer.adjust_for_ambient_noise(source)
         audio = recognizer.listen(source)
      print(f'\033[1;30m{"stop listening... "}\033[0m')

Dieser Abschnitt der Hauptschleife verarbeitet die Spracheingabe in Echtzeit.

Bei der Mikrofonbenutzung können einige Geräte (z. B. Raspberry Pi) ALSA-Warnungen oder -Fehlermeldungen ausgeben. 
Diese beeinträchtigen die Programmlogik nicht. 
Zur Verbesserung der Nutzererfahrung unterdrücken ``redirect_error_2_null()`` und ``cancel_redirect_error()`` die Ausgaben temporär und stellen sie anschließend wieder her.

* ``with sr.Microphone(chunk_size=8192) as source:`` öffnet das Mikrofon als Audioquelle. Der Parameter ``chunk_size`` legt die Größe der pro Sekunde verarbeiteten Audio-Samples fest.
* Durch den ``with``-Block wird sichergestellt, dass die Ressource Mikrofon ordnungsgemäß geschlossen wird.
* ``recognizer.adjust_for_ambient_noise(source)`` nimmt kurz Umgebungsgeräusche auf, um den Schwellenwert dynamisch zu justieren.
* ``audio = recognizer.listen(source)`` zeichnet die Sprache auf und liefert ein ``audio``-Objekt mit den Audiodaten.

Die beiden ``print()``-Ausgaben informieren, wann die Aufnahme beginnt bzw. endet.


.. code-block:: python

   with open("stt-rec.wav", "wb") as f:
      f.write(audio.get_wav_data())
   os.system('play stt-rec.wav')

Damit wird die Aufnahme als WAV gespeichert und sofort wiedergegeben. 
Das ist beim Debugging hilfreich, um die Aufnahmequalität zu prüfen. 
In Produktionsumgebungen kann dieser Teil auskommentiert werden, um den Ablauf zu straffen.


.. code-block:: python

   msg = speech_to_text(audio)

.. code-block:: python

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


Um die aufgenommene Sprache zu transkribieren, ruft die Hauptschleife ``speech_to_text(audio)`` mit dem aufgenommenen ``audio``-Objekt auf.

Die Funktion nutzt das OpenAI-Modell ``whisper-1`` wie folgt:

* ``wav_data`` wird als In-Memory-``BytesIO``-Stream erzeugt – ideal für temporäres Puffern/Übertragen von Audiodaten.
* Dem Stream wird der virtuelle Dateiname ``"record.wav"`` zugewiesen, da ``whisper-1`` einen Dateinamen in den Metadaten erwartet.

Der Parameter ``language=['zh', 'en']`` gibt Chinesisch und Englisch als unterstützte Sprachen an. Whisper kann in der Praxis weitere Sprachen erkennen. Für automatische Spracherkennung kann ``language=None`` verwendet werden.

So bleibt der Chatbot flexibel im Umgang mit mehrsprachigen Eingaben und passt sich unterschiedlichen Nutzungsszenarien an.


----------------------------------------------



**Error Handling**

Robustes Fehlermanagement ist entscheidend für Zuverlässigkeit und Nutzerfreundlichkeit Ihres Speech-to-Text-Chatbots. Nachfolgend bewährte Strategien für typische Problemfälle:

1. **API Connection Errors**

**Problem:** Netzwerkprobleme oder fehlerhafte API-Konfiguration verhindern die Verbindung zu den OpenAI-Servern.

**Solution:** Setzen Sie auf Retry-Logik mit exponentiellem Backoff und fangen Sie netzwerkbezogene Ausnahmen ab. Stellen Sie sicher, dass die API-Schlüssel korrekt konfiguriert sind, und behandeln Sie Authentifizierungsfehler sauber.

.. code-block:: python

   import time
   import requests

   def reliable_api_call(callable, *args, **kwargs):
      retries = 5
      for i in range(retries):
         try:
               return callable(*args, **kwargs)
         except requests.exceptions.RequestException as e:
               wait = 2 ** i
               print(f"Network error: {e}, retrying in {wait} seconds...")
               time.sleep(wait)
         except openai.APIError as e:
               print(f"API error: {e}, check your API configuration.")
               break
      return None


2. **Misinterpretation of Silence**

**Problem:** Whisper transkribiert gelegentlich Stille als bedeutungsvolle Sprache.

**Solution:** Nutzen Sie Voice Activity Detection (VAD), um nur Abschnitte mit potenzieller Sprache zu verarbeiten. Justieren Sie außerdem die Empfindlichkeit des Recognizers, um Stille besser abzugrenzen.

.. code-block:: python

   import speech_recognition as sr

   def listen_and_filter_silence(recognizer, source):
      with sr.Microphone() as source:
         recognizer.adjust_for_ambient_noise(source)
         audio = recognizer.listen(source)
         if audio.frame_data:  # Prüfen, ob relevante Audiodaten vorhanden sind
               return audio
         else:
               print("Silence detected, ignoring input.")
               return None


3. **Whisper Transcription Errors**

**Problem:** Durch Umgebungslärm, Akzente oder erkannte Stille kann es zu Fehltranskriptionen kommen.

**Solution:** Implementieren Sie ein kurzes Feedback-Loop: Nutzerinnen und Nutzer können die Transkription bestätigen oder korrigieren. Dieses Feedback hilft, die Systemreaktionen zu verbessern.

.. code-block:: python

   def ask_for_feedback(transcribed_text):
      print(f"Transcribed: {transcribed_text}")
      user_correction = input("If this is incorrect, please type the correct text, or just press enter if it is correct: ")
      if user_correction:
         return user_correction
      else:
         return transcribed_text


4. **Audio Input Errors**

**Problem:** Falsch konfigurierte Mikrofone oder schlechte Audioqualität führen zu fehlender oder mangelhafter Erkennung.

**Solution:** Testen Sie regelmäßig die Mikrofoneinstellungen und stellen Sie klare Audioeingaben sicher. Nutzen Sie Diagnose-Hilfen, um Eingangspegel zu prüfen und anzupassen.

.. code-block:: python

   def test_microphone_settings():
      recognizer = sr.Recognizer()
      with sr.Microphone() as source:
         try:
               recognizer.adjust_for_ambient_noise(source)
               print("Microphone is properly configured.")
         except sr.RequestError as e:
               print(f"Microphone configuration error: {e}")
         except sr.UnknownValueError:
               print("Microphone setup failed, please check your audio device.")
