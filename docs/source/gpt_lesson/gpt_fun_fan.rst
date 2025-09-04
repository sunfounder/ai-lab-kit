2.12 Sprachgesteuerter Ventilator
================================================

Dieses Projekt ist ein sprachgesteuerter Drehzahlregler für einen Ventilator, der mit der OpenAI-API betrieben wird. Nutzer können per Sprachbefehl die Geschwindigkeit eines Motors steuern, der als Ventilator dient. Das System verwendet ein Mikrofon für die Spracheingabe, einen Motortreiber zur Regulierung der Geschwindigkeit sowie einen Summer für akustisches Feedback. Durch die Spracherkennung, die Verarbeitung der Befehle mittels KI und die dynamische Anpassung der Geschwindigkeit wird eine nahtlose Interaktion gewährleistet.

----------------------------------------------


**Features**

- **Sprachgesteuerte Ventilatorgeschwindigkeit**: Nutzer können den Ventilator per Sprachbefehl schneller, langsamer oder ganz ausschalten.
- **Echtzeit-Geschwindigkeitsregelung**: Das System stellt sicher, dass die Geschwindigkeit stets im gültigen Bereich (0–100 %) bleibt.
- **Touch-Sensor zur manuellen Erhöhung**: Ein berührungsempfindlicher Sensor ermöglicht die manuelle Anpassung der Geschwindigkeit.
- **Akustisches Feedback über Summer**: Gibt ein Signalton für Benutzerinteraktionen aus.
- **KI-gestützte Befehlsverarbeitung**: OpenAI GPT-4 interpretiert die Sprachbefehle und erzeugt JSON-formatierte Antworten.
- **Sprach-zu-Text-Umwandlung**: Nutzt OpenAIs Whisper-Modell zur Spracherkennung.
- **Dynamische Geräuschunterdrückung**: Passt sich Hintergrundgeräuschen an, um die Erkennung zu verbessern.

----------------------------------------------

**What You’ll Need**

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK


    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_buzzer`
        - |link_passive_buzzer_buy|
    *   - :ref:`cpn_transistor`
        - |link_transistor_buy|
    *   - :ref:`cpn_motor`
        - |link_motor_buy|
    *   - :ref:`cpn_touch_switch`
        - |link_touch_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -


----------------------------------------------


**Wiring Diagram**


.. image:: img/fzz/gpt_fan_bb.png
   :width: 800
   :align: center

----------------------------------------------

**Running the Example**


Der gesamte Beispielcode zu diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_fan.py 

----------------------------------------------

**Code**


.. raw:: html

   <run></run>
   
.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import sys
   import os
   import time
   import speech_recognition as sr
   from fusion_hat import Motor,PWM,Pin,Buzzer

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   os.system("fusion_hat enable_speaker")

   TTS_OUTPUT_FILE = 'tts_output.mp3'


   instructions_text = '''
   You are a fan control assistant. Your task is to interpret the user's speech input and adjust the motor speed accordingly.

   ### Input Format:
   "current speed: [value], message: [user command]"

   ### Output Guidelines:
   1. If the user requests a speed change, provide a response in JSON format:
      {"speed": <new_speed>, "message": "<response text>"}
   2. If the user does not mention speed, acknowledge their input and provide relevant information.
   3. Ensure the new speed stays within a 0-100 range.
   4. If the user asks about the current speed, return a friendly status update.

   ### Example Inputs & Outputs:

   **Example 1:**
   Input: "current speed: 30, message: increase speed"
   Output: {"speed": 40, "message": "Speed increased to 40%."}

   **Example 2:**
   Input: "current speed: 100, message: stop the motor"
   Output: {"speed": 0, "message": "Fan stopped."}

   **Example 3:**
   Input: "current speed: 50, message: What is my current speed?"
   Output: {"speed": 50, "message": "Your current speed is 50%."}
   '''

   # assistant=client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
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

   motor = Motor('M0')
   touch_sensor = Pin(17, Pin.IN, pull = Pin.PULL_DOWN) 
   buzzer = Buzzer(Pin(4))
   speed = 0

   def beep():
      buzzer.on()
      time.sleep(0.1)
      buzzer.off()

   last_triggered = 0 

   def speed_up():
      global speed,last_triggered
      if time.time() - last_triggered < 0.5:  # 500ms debounce
         return
      last_triggered = time.time()
      speed += 10
      beep()
      if speed > 100:
         motor.stop()
         speed = 0
      else:
         motor.speed(speed)


   touch_sensor.when_activated = speed_up

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

         # Convert recorded audio to text
         msg = speech_to_text(audio)

         if msg == False or msg == "":
               print() # new line
               continue
         
         beep()

         send_message= "current speed:"+ str(speed) + "message:" + msg

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
                              # print(f"Raw AI Response: {value}")
                              try:
                                 value = eval(value)
                              except Exception as e:
                                 value = str(value)
                              if isinstance(value, dict):
                                 if 'speed' in value:
                                       speed = value['speed']
                                 else:
                                       speed = -1
                                 if 'message' in value:
                                       text = value['message']
                                 else :
                                       text = ''
                              else:
                                 speed = -1
                                 text = value

                              print(f'{label:>10} >>> {text} {speed}')

                              if speed >= 0:
                                 motor.speed(speed)

                     break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)
      buzzer.off()
      motor.stop()

----------------------------------------------


**Code Explanation**

Dieses Projekt besteht aus mehreren zentralen Funktionskomponenten:

1. **Initialisierung und Setup:**

   - Importiert die erforderlichen Bibliotheken, darunter OpenAI für die KI-Verarbeitung und ``speech_recognition`` für die Spracheingabe.
   - Richtet den OpenAI-Client mithilfe des ``OPENAI_API_KEY`` ein.
   - Aktiviert das Mikrofon mit ``os.system("fusion_hat enable_speaker")``.
   - Initialisiert die Hardwarekomponenten wie Motor, Summer und Touch-Sensor.

2. **Spracherkennung**:

   - Wandelt aufgezeichnetes Audio mithilfe des Whisper-Modells von OpenAI in Text um.
   - Unterstützt mehrere Sprachen (``zh``, ``en``).

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

3. **Touch-Sensor-Steuerung (``speed_up``):**

   - Ermöglicht die manuelle Anpassung der Geschwindigkeit über einen Berührungssensor.
   - Entprell-Logik verhindert unbeabsichtigte Mehrfachauslösungen.
   - Erhöht die Geschwindigkeit pro Berührung um 10 % und setzt sie bei Überschreiten von 100 % auf 0 zurück.

   .. code-block:: python

       def speed_up():
           global speed, last_triggered
           if time.time() - last_triggered < 0.5:
               return
           last_triggered = time.time()
           speed += 10
           beep()
           if speed > 100:
               motor.stop()
               speed = 0
           else:
               motor.speed(speed)

4. **Verarbeitung von Sprachbefehlen:**

   - Zeichnet die Spracheingabe des Nutzers auf und wandelt sie in Text um.
   - Sendet den transkribierten Text zusammen mit der aktuellen Geschwindigkeit an den OpenAI-Assistenten.
   - Die KI liefert eine JSON-Antwort mit der neuen Geschwindigkeit und einer passenden Textnachricht zurück.

   .. code-block:: python

       send_message= "current speed:"+ str(speed) + "message:" + msg
       message = client.beta.threads.messages.create(
           thread_id=thread.id,
           role="user",
           content=send_message,
       )
       run = client.beta.threads.runs.create_and_poll(
           thread_id=thread.id,
           assistant_id=assistant.id,
       )

5. **Verarbeitung der KI-Antwort:**

   - Extrahiert Geschwindigkeit und Nachricht aus der JSON-Antwort der KI.
   - Passt die Motordrehzahl entsprechend an.

   .. code-block:: python

       for message in messages.data:
           if message.role == 'assistant':
               for block in message.content:
                   if block.type == 'text':
                       value = eval(block.text.value)
                       if isinstance(value, dict):
                           speed = value.get('speed', -1)
                           text = value.get('message', '')
                       print(f'BOT >>> {text} {speed}')
                       if speed >= 0:
                           motor.speed(speed)

6. **Fehlerbehandlung und Aufräumen:**

   - Unterdrückt ALSA-Warnmeldungen, um unnötige Fehlerausgaben zu vermeiden.
   - Stellt sicher, dass der OpenAI-Assistent gelöscht und die Hardware beim Beenden zurückgesetzt wird.

   .. code-block:: python

       finally:
           client.beta.assistants.delete(assistant.id)
           buzzer.off()
           motor.stop()

----------------------------------------------

**Debugging Tips**

- **Spracherkennung funktioniert nicht?**

  - Erhöhen Sie die Dauer von ``recognizer.adjust_for_ambient_noise(source)``, wenn Hintergrundgeräusche stören.

- **Ventilatorgeschwindigkeit wird nicht aktualisiert?**

  - Überprüfen Sie das Antwortformat der OpenAI-API, um sicherzustellen, dass das JSON korrekt geparst wird.
  - Vergewissern Sie sich, dass ``motor.speed(speed)`` mit dem erwarteten Wert ausgeführt wird.

- **Touch-Sensor reagiert nicht?**

  - Fügen Sie Debug-Ausgaben in ``speed_up()`` hinzu, um zu prüfen, ob der Sensor ausgelöst wird.
  - Stellen Sie sicher, dass die Pull-Down-Konfiguration für den GPIO-Pin korrekt ist.

- **Summer gibt keinen Ton aus?**

  - Prüfen Sie, ob ``buzzer.on()`` und ``buzzer.off()`` korrekt aufgerufen werden.
  - Stellen Sie sicher, dass der GPIO-Ausgang für den Summer aktiviert ist.

