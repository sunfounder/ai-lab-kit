2.9 DigiPet
===================

Dieses Python-Skript verbindet OpenAIs GPT-API mit einer 8x8-LED-Matrix sowie Audio-Ein-/Ausgabe, um ein interaktives elektronisches Haustier zu simulieren. Das „Pet“ hört der Stimme des Nutzers zu, reagiert mit einem Gesichtsausdruck auf der LED-Matrix und gibt seine Antwort per Sprachausgabe wieder.

----------------------------------------------

**Features**

1. Speech-to-Text Conversion:

   * Erfasst Nutzereingaben über ein Mikrofon und wandelt sie mit dem Whisper-Modell von OpenAI in Text um.

2. Text-to-Speech Output:

   * Wandelt die Textantwort des Assistenten mithilfe des TTS-Modells von OpenAI in Sprache um.

3. 8x8 LED Matrix Display:

   * Zeigt je nach Antwort des Assistenten Gesichtsausdrücke oder Muster, die die „Emotionen“ des Bots darstellen.

4. Dynamic Interactions:

   * Erzeugt einen Gesprächsfluss mit einer personalisierten, animierten Nutzererfahrung.

----------------------------------------------

**What You’ll Need**

Die folgenden Komponenten werden für dieses Projekt benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK

    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_dot_matrix`
        - |link_led_matrix_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------

**Diagram**

.. image:: img/fzz/1.1.6_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Running the Example**

Der gesamte Beispielcode zu diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``. 
Führe die folgenden Schritte aus, um das Beispiel zu starten:

.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_digipet.py 
    
----------------------------------------------

**Code**

.. raw:: html

   <run></run>

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import speech_recognition as sr

   from fusion_hat import LedMatrix
   from pathlib import Path
   import subprocess
   import sys
   import os


   # Initialize OpenAI client
   client = openai.OpenAI(api_key=OPENAI_API_KEY)
   os.system("fusion_hat enable_speaker")

   # Initialize hardware components
   rgb_matrix = LedMatrix(rotate=0)
   recognizer = sr.Recognizer()


   # Functions for speech-to-text and text-to-speech
   def speech_to_text(audio_file):
      """
      Convert speech audio to text using OpenAI Whisper model.
      """
      from io import BytesIO
      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "record.wav"

      try:
         transcription = client.audio.transcriptions.create(
               model="whisper-1",
               file=wav_data,
               language=["zh", "en"]
         )
         return transcription.text
      except Exception as e:
         print(f"Error in Speech-to-Text: {e}")
         return ""


   def text_to_speech(text):
      """
      Convert text to speech using OpenAI's TTS model.
      """
      speech_file_path = Path(__file__).parent / "speech.mp3"
      try:
         with client.audio.speech.with_streaming_response.create(
               model="tts-1",
               voice="alloy",
               input=text
         ) as response:
               response.stream_to_file(speech_file_path)
         p=subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
         p.wait()
      except Exception as e:
         print(f"Error in Text-to-Speech: {e}")
         return None


   # Redirect ALSA errors to null
   def redirect_error_to_null():
      devnull = os.open(os.devnull, os.O_WRONLY)
      old_stderr = os.dup(2)
      sys.stderr.flush()
      os.dup2(devnull, 2)
      os.close(devnull)
      return old_stderr


   def cancel_redirect_error(old_stderr):
      os.dup2(old_stderr, 2)
      os.close(old_stderr)


   # Create an OpenAI assistant
   assistant = client.beta.assistants.create(
      name="Electronic Pet Bot",
      instructions=(
         "You are an electronic pet robot with an 8x8 LED matrix as your face. "
         "When interacting with the user, provide a JSON output with a 'pattern' for the face "
         "and a 'message' for interaction. Example JSON: "
         '{"pattern": [0b00111100, 0b01000010, 0b10100101, 0b10000001, 0b10100101, 0b10011001, 0b01000010, 0b00111100], '
         '"message": "Hello, nice to meet you!"}'
      ),
      model="gpt-4o-mini",
      response_format="auto",
   )

   # Create a conversation thread
   thread = client.beta.threads.create()

   try:
      while True:
         print(f'\033[1;30m{"Listening..."}\033[0m')
         old_stderr = redirect_error_to_null()
         with sr.Microphone(chunk_size=8192) as source:
               cancel_redirect_error(old_stderr)
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)

         print(f'\033[1;30m{"Processing audio..."}\033[0m')
         user_message = speech_to_text(audio)
         if not user_message:
               print("No input detected. Please try again.")
               continue

         # Send the user's message to the assistant
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=user_message,
         )

         run = client.beta.threads.runs.create_and_poll(
               thread_id=thread.id,
               assistant_id=assistant.id,
         )

         # Process the assistant's response
         if run.status == "completed":
               messages = client.beta.threads.messages.list(thread_id=thread.id)
               for message in messages.data:
                  if message.role == "assistant":
                     for block in message.content:
                           if block.type == "text":
                              try:
                                 response = eval(block.text.value)
                                 pattern = response.get("pattern", [])
                                 assistant_message = response.get("message", "")
                                 if pattern:
                                       rgb_matrix.display_pattern(pattern) 
                                 if assistant_message:
                                       print(f"Bot: {assistant_message}")
                                       text_to_speech(assistant_message)
                              except Exception as e:
                                 print(f"Error in processing assistant response: {e}")
                     break

   finally:
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up.")

----------------------------------------------

**Code Explanation**

1. Initialization

.. code-block:: python

   # Initialize OpenAI client
   client = openai.OpenAI(api_key=OPENAI_API_KEY)
   os.system("fusion_hat enable_speaker")

   # Initialize hardware components
   rgb_matrix = LedMatrix(rotate=0)
   recognizer = sr.Recognizer()

* Initialisiert den OpenAI-Client mit einem API-Schlüssel.
* Richtet die 8x8-LED-Matrix über die ``LedMatrix``-Klasse ein.
* Konfiguriert den Spracherkenner für Audioeingaben.

2. Speech-to-Text Conversion

.. code-block:: python

   def speech_to_text(audio_file):
      from io import BytesIO
      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "record.wav"

      transcription = client.audio.transcriptions.create(
         model="whisper-1",
         file=wav_data,
         language=["zh", "en"]
      )
      return transcription.text

* Erfasst Audioeingaben und wandelt sie mit dem Whisper-Modell in Text um.
* Unterstützt mehrsprachige Eingaben (zh für Chinesisch, en für Englisch).

3. Text-to-Speech Conversion

.. code-block:: python

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      with client.audio.speech.with_streaming_response.create(
         model="tts-1",
         voice="alloy",
         input=text
      ) as response:
         response.stream_to_file(speech_file_path)
      return speech_file_path

* Wandelt die Textantwort des Assistenten mit dem TTS-Modell in eine MP3-Datei um.
* Gibt den Dateipfad zur Wiedergabe zurück.


4. Error Handling for ALSA


.. code-block:: python

   def redirect_error_to_null():
      devnull = os.open(os.devnull, os.O_WRONLY)
      old_stderr = os.dup(2)
      os.dup2(devnull, 2)
      return old_stderr

   def cancel_redirect_error(old_stderr):
      os.dup2(old_stderr, 2)
      os.close(old_stderr)

* Leitet ALSA-Fehler nach /dev/null um, um übermäßige Fehlermeldungen bei der Mikrofoninitialisierung zu vermeiden.
* Stellt die Standard-Fehlerausgabe nach der Initialisierung wieder her.

5. Assistant Creation

.. code-block:: python

   assistant = client.beta.assistants.create(
      name="Electronic Pet Bot",
      instructions=(
         "You are an electronic pet robot with an 8x8 LED matrix as your face. "
         "Provide JSON output with a 'pattern' for the face and a 'message' for interaction. "
      ),
      model="gpt-4o-mini",
      response_format="auto",
   )

Konfiguriert den GPT-Assistenten so, dass er eine JSON-Struktur zurückgibt mit:

* einem Schlüssel ``pattern`` für die Anzeige auf der LED-Matrix,
* sowie ``message`` für die textliche und gesprochene Antwort.


6. Conversation Flow

.. code-block:: python

   thread = client.beta.threads.create()

   while True:
      old_stderr = redirect_error_to_null()
      with sr.Microphone(chunk_size=8192) as source:
         cancel_redirect_error(old_stderr)
         recognizer.adjust_for_ambient_noise(source)
         audio = recognizer.listen(source)

      user_message = speech_to_text(audio)
      if not user_message:
         continue

      message = client.beta.threads.messages.create(
         thread_id=thread.id,
         role="user",
         content=user_message,
      )

      run = client.beta.threads.runs.create_and_poll(
         thread_id=thread.id,
         assistant_id=assistant.id,
      )

* Wartet fortlaufend auf Spracheingaben über das Mikrofon.
* Wandelt die Nutzersprache in Text um und sendet sie an den Assistenten.
* Wartet auf die Antwort des Assistenten und verarbeitet diese.

7. Response Handling

.. code-block:: python

   if run.status == "completed":
      messages = client.beta.threads.messages.list(thread_id=thread.id)
      for message in messages.data:
         if message.role == "assistant":
               for block in message.content:
                  if block.type == "text":
                     response = eval(block.text.value)
                     pattern = response.get("pattern", [])
                     assistant_message = response.get("message", "")
                     if pattern:
                           display_pattern(device, pattern)
                     if assistant_message:
                           speech_path = text_to_speech(assistant_message)
                           if speech_path:
                              subprocess.Popen(
                                 ["mplayer", str(speech_path)],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                              ).wait()

* Liest die JSON-Antwort des Assistenten aus und extrahiert ``pattern`` und ``message``.
* Zeigt das Muster auf der LED-Matrix an.
* Gibt die Textantwort per TTS und externem Audioplayer wieder.

8. Cleanup

.. code-block:: python

   finally:
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up.")

Sorgt für die ordnungsgemäße Freigabe von Ressourcen, einschließlich dem Löschen der Assistenteninstanz.


----------------------------------------------

**Debugging Tips**

1. Probleme bei der Spracherkennung:

   * Umgebungsgeräusche minimieren, um die Erkennung zu verbessern.

2. LED-Matrix zeigt keine Muster:

   * Verdrahtung und Anschlüsse des LED-Matrix-Moduls prüfen.
   * Sicherstellen, dass pattern eine gültige Liste aus 8 Ganzzahlen ist.

3. Audiowiedergabe funktioniert nicht:

   * Prüfen, ob mplayer installiert ist (sudo apt install mplayer).

4. OpenAI-API-Fehler:

   * Gültigkeit des API-Schlüssels und stabile Internetverbindung sicherstellen.
   * Rohausgaben des Assistenten ausgeben, um ungültiges JSON zu debuggen.
