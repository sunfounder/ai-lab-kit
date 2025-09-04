2.5 Kompositionsassistent
======================================

Dieses Beispiel zeigt, wie sich OpenAIs GPT-Modell mit GPIO-gesteuerter Hardware integrieren lässt, um einen interaktiven Assistenten für das Komponieren zu erstellen.

Der Assistent fordert Nutzer auf, drei Töne zu singen, etwa „do, re, mi“, die über ein Mikrofon aufgenommen werden. Mithilfe des Whisper-Modells von OpenAI zur Transkription und GPT zur Komposition erzeugt der Assistent anschließend eine Melodie auf Basis der gesungenen Töne. Die entstandene Melodie wird auf einem Summer abgespielt, während eine textuelle Beschreibung der Komposition ausgegeben wird – für ein kreatives und unterhaltsames Musikerlebnis.


----------------------------------------------

**Features**

1. **Voice Input**: Erfasst Sprachbefehle der Nutzer über ein Mikrofon.
2. **GPT-Powered Composition**: Erzeugt anhand der Eingaben des Nutzers eine Melodie mit GPT.
3. **Melody Playback**: Spielt die generierte Melodie auf einem tonalen Summer ab.
4. **LED Indicator**: Nutzt eine LED, um anzuzeigen, wann das System aktiv zuhört.
5. **Friendly Feedback**: Zeigt sowohl die generierte Melodie als auch eine textliche Antwort des Assistenten an.

----------------------------------------------

**What You’ll Need**

Die folgenden Komponenten werden für dieses Projekt benötigt:


.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - KOMPONENTENVORSTELLUNG
        - KAUFLINK

    *   - :ref:`cpn_breadboard`
        - |link_breadboard_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_buzzer`
        - |link_passive_buzzer_buy|
    *   - :ref:`cpn_transistor`
        - |link_transistor_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------


**Diagram**


.. image:: img/fzz/gpt_compose_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Running the Example**


Der gesamte Beispielcode zu diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``. 
Führe die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_compose.py 


----------------------------------------------


**Code**

.. raw:: html

   <run></run>
   
.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import readline # optimize keyboard input, only need to import
   import sys
   import os
   from time import sleep

   import speech_recognition as sr

   from fusion_hat import Buzzer,Pin,PWM

   os.system("fusion_hat enable_speaker")

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   # Speech recognizer
   recognizer = sr.Recognizer()

   def speech_to_text(audio_file):
      from io import BytesIO

      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "stt_output.wav"

      transcription = client.audio.transcriptions.create(
         model="whisper-1", 
         file=wav_data,
         language=['zh','en']
      )
      return transcription.text

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

   # Initialize hardware components
   buzzer = Buzzer('P0') 
   led = Pin(17, Pin.OUT)

   # Create an OpenAI assistant
   instructions_text = (
      "You are a music composition assistant. Based on three given notes, "
      "you must create a melody and provide it as a JSON dictionary. "
      "The JSON must include 'melody' (a list of tuples with notes and durations) "
      "and 'message' (a textual description). Example format: "
      "{\"melody\": [('C#4', 0.2), ('D4', 0.2), (None, 0.2)], \"message\": \"Your melody is ready.\"}"
   )

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4o",
   )

   thread = client.beta.threads.create()

   def play_tune(tune):
      """
      Play a musical tune using the buzzer.
      :param tune: List of tuples (note, duration), where each tuple represents a note and its duration.
      """
      for note, duration in tune:
         print(note)  # Output the current note being played
         buzzer.play(note,float(duration))  # Play the note on the buzzer
      buzzer.off()  # Stop playing after the tune is complete
      sleep(1)

   try:
      while True:
         # Listen to user input
         led.on()
         print(f'\033[1;30m{"listening... "}\033[0m')
         _stderr_back = redirect_error_2_null() # ignore error print to ignore ALSA errors
         with sr.Microphone(chunk_size=8192) as source:
               cancel_redirect_error(_stderr_back) # restore error print
               recognizer.adjust_for_ambient_noise(source)
               audio = recognizer.listen(source)
         print(f'\033[1;30m{"stop listening... "}\033[0m')
         led.off()

         # Convert audio to text
         msg = ""
         msg = speech_to_text(audio)
         if msg == False or msg == "":
               print("No valid input received.")
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
                              response = block.text.value
                              try:
                                 response_dict = eval(response)
                                 melody = response_dict.get('melody', [])
                                 text = response_dict.get('message', "No message provided.")
                                 print(f"{assistant.name:>10} >>>  {text}")
                                 play_tune(melody)
                              except Exception as e:
                                 print(f"Error processing assistant response: {e}")


                     break # only last reply

   finally:
      buzzer.off()
      client.beta.assistants.delete(assistant.id)



----------------------------------------------

**Code Explanation**


1. **Import Necessary Libraries**

.. code-block:: python
      
   import openai
   from keys import OPENAI_API_KEY
   import readline 
   import sys
   import os
   from time import sleep
   import speech_recognition as sr
   from fusion_hat import Buzzer,Pin,PWM

* ``openai``: Schnittstelle zu den GPT- und Whisper-Modellen von OpenAI.
* ``speech_recognition``: Erfasst und verarbeitet Audioeingaben.
* ``fusion_hat``: Steuert GPIO-Komponenten wie Summer und LED.


2. **Initialize OpenAI Client**

.. code-block:: python

   client = openai.OpenAI(api_key=OPENAI_API_KEY)

Der OpenAI-Client wird mit einem API-Schlüssel konfiguriert, um auf GPT- und Whisper-Modelle zuzugreifen.

3. **Define Helper Functions**

.. code-block:: python

   def speech_to_text(audio_file):
      from io import BytesIO
      wav_data = BytesIO(audio_file.get_wav_data())
      wav_data.name = "stt_output.wav"
      transcription = client.audio.transcriptions.create(
         model="whisper-1", 
         file=wav_data,
         language=['zh','en']
      )
      return transcription.text

Sprach-zu-Text-Umwandlung:

* Nutzt OpenAIs Whisper-Modell zur Transkription von Audio in Text.
* Unterstützt mehrere Sprachen (z. B. Chinesisch und Englisch).

.. code-block:: python

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

ALSA-Fehler unterdrücken: Verhindert unnötige Konsolenmeldungen während der Mikrofonverwendung.


.. code-block:: python

   def play_tune(tune):
      """
      Play a musical tune using the buzzer.
      :param tune: List of tuples (note, duration), where each tuple represents a note and its duration.
      """
      for note, duration in tune:
         print(note)  # Output the current note being played
         buzzer.play(note,float(duration))  # Play the note on the buzzer
      buzzer.off()  # Stop playing after the tune is complete
      sleep(1)

Melodie auf dem Summer abspielen:

* Nimmt eine Melodie als Liste von (Note, Dauer)-Tupeln entgegen.
* Spielt jeden Ton für die angegebene Dauer auf dem Summer.


4. **Configure Hardware Components**

.. code-block:: python
      
   # Initialize hardware components
   buzzer = Buzzer(PWM('P0')) 
   led = Pin(17, Pin.OUT)

Initialisiert die GPIO-Komponenten für Audiowiedergabe und Statusanzeige.


5. Create OpenAI Assistant

.. code-block:: python

   instructions_text = (
      "You are a music composition assistant. Based on three given notes, "
      "you must create a melody and provide it as a JSON dictionary. "
      "The JSON must include 'melody' (a list of tuples with notes and durations) "
      "and 'message' (a textual description). Example format: "
      "{\"melody\": [('C#4', 0.2), ('D4', 0.2), (None, 0.2)], \"message\": \"Your melody is ready.\"}"
   )

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4o",
   )

   thread = client.beta.threads.create()


Definiert einen Assistenten namens BOT mit klaren Anweisungen, um:

* Eingabetöne anzunehmen,
* eine Melodie im JSON-Format zu erzeugen,
* und eine textliche Beschreibung der Melodie bereitzustellen.


6. **Main Loop for Listening and Responding**

.. code-block:: python

   led.on()
   print(f'\033[1;30m{"listening... "}\033[0m')
   _stderr_back = redirect_error_2_null()
   with sr.Microphone(chunk_size=8192) as source:
      cancel_redirect_error(_stderr_back)
      recognizer.adjust_for_ambient_noise(source)
      audio = recognizer.listen(source)
   led.off()

Erfassung der Spracheingabe:

* Die LED leuchtet, solange das System zuhört.
* Erfasst und verarbeitet die Spracheingabe mit speech_recognition.


.. code-block:: python

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
                        response = block.text.value
                        try:
                           response_dict = eval(response)
                           melody = response_dict.get('melody', [])
                           text = response_dict.get('message', "No message provided.")
                           print(f"{assistant.name:>10} >>>  {text}")
                           play_tune(melody)
                        except Exception as e:
                           print(f"Error processing assistant response: {e}")

Verarbeitung der GPT-Antwort:

* Sendet den transkribierten Text an den GPT-Assistenten.
* Parst die JSON-Antwort, entnimmt die Melodie und spielt sie über den Summer ab.



7. **Cleanup Resources**

.. code-block:: python

   finally:
      buzzer.off()
      client.beta.assistants.delete(assistant.id)

Stellt sicher, dass die Hardware zurückgesetzt und OpenAI-Ressourcen freigegeben werden.



----------------------------------------------



**Debugging Tips**

1. Mikrofon nimmt nichts auf:

   * Prüfe, ob das Mikrofon korrekt angeschlossen ist.
   * Überprüfe die Mikrofonberechtigungen mit ``alsamixer`` oder in den Systemeinstellungen.

2. Summer spielt keine Töne:

   * GPIO-Pin-Belegung kontrollieren.
   * Sicherstellen, dass die Notennamen in der Melodie vom Summer unterstützt werden.

3. JSON-Parsing-Fehler:

   * Prüfen, ob die Antwort des Assistenten dem vorgegebenen JSON-Format entspricht.
   * Zusätzliche Debug-Ausgaben einfügen, um rohe GPT-Antworten anzuzeigen.

4. ALSA-Fehler in der Konsole:

   * Die Funktion ``redirect_error_2_null()`` verwenden, um ALSA-Meldungen zu unterdrücken.

5. Keine Antwort von GPT:

   * Internetverbindung prüfen.
   * Sicherstellen, dass der OpenAI-API-Schlüssel gültig ist und ausreichende Kontingente vorhanden sind.
