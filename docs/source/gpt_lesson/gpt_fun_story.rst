2.1 Story Teller
==========================

Dieses Python-Skript integriert OpenAIs GPT mit Hardwarekomponenten wie einem Taster und einer Kamera, um auf Basis eines Buchcover-Fotos ein interaktives Erzählerlebnis zu erzeugen. 

Das Programm wartet darauf, dass die Nutzerin oder der Nutzer einen Taster drückt.





When pressed:

#. Es wird ein Foto des Buchcovers aufgenommen.

#. Das Foto wird an das GPT-Modell von OpenAI gesendet, das eine Handlungszusammenfassung erzeugt.

#. Die Geschichte wird in Sprache umgewandelt und wiedergegeben.


----------------------------------------------

**Features**

* Interaktives Erlebnis: Nutzerinnen und Nutzer interagieren über einen Taster und erhalten visuelles sowie akustisches Feedback.

* KI-gestütztes Storytelling: GPT interpretiert das Buchcover und liefert eine kreative Zusammenfassung.

* Sprachausgabe: Die generierte Geschichte wird vorgelesen – das erhöht Zugänglichkeit und Engagement.

---------------------------------------------



**What You’ll Need**

Die folgenden Komponenten werden für dieses Projekt benötigt:


.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT INTRODUCTION
        - PURCHASE LINK

    *   - :ref:`cpn_breadboard`
        - |link_breadboard_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|   
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------


**Circuit Diagram**


.. image:: img/fzz/gpt_story_bb.png
   :width: 800
   :align: center


----------------------------------------------

**Running the Example**


Der gesamte Beispielcode dieses Tutorials befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_storyteller.py 


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
   from pathlib import Path
   import subprocess
   from fusion_hat import Pin
   from picamera2 import Picamera2

   os.system("fusion_hat enable_speaker")

   # Initialize OpenAI client
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   # Initialize hardware components
   button = Pin(17, Pin.IN, Pin.PULL_DOWN)
   camera = Picamera2()

   # Function to capture a photo
   def capture_photo():
      """
      Capture a photo using the Picamera2 and save it as 'my_photo.jpg'.
      """
      try:
         print(f'\033[1;30m{"Shooting photo..."}\033[0m')
         # Set preview configuration
         camera.configure(camera.preview_configuration)
         camera.start()
         camera.capture_file("my_photo.jpg")
         camera.stop()
         story_talking()
      except Exception as e:
         print(f"Error capturing photo: {e}")

   # Function for text-to-speech conversion
   def text_to_speech(text):
      """
      Convert text to speech using OpenAI's TTS model.
      """
      speech_file_path = Path(__file__).parent / "speech.mp3"
      try:
         with client.audio.speech.with_streaming_response.create(
               model="tts-1", voice="alloy", input=text
         ) as response:
               response.stream_to_file(speech_file_path)
         subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
      except Exception as e:
         print(f"Error in Text-to-Speech: {e}")

   # Function to send the photo and get a story from GPT
   def story_talking():
      """
      Send the captured photo to GPT and receive a story about the book.
      """
      print(f'\033[1;30m{"GPT reading..."}\033[0m')
      try:
         # Upload the photo to OpenAI
         file = client.files.create(
               file=open("my_photo.jpg", "rb"), purpose="vision"
         )

         # Send user message and photo to GPT
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=[
                  {"type": "text", "text": "What is this book about?"},
                  {"type": "image_file", "image_file": {"file_id": file.id}},
               ],
         )

         # Run the assistant and get the response
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
                              print(f"Assistant >>> {response}")
                              text_to_speech(response)
                              return
      except Exception as e:
         print(f"Error in story_talking: {e}")

   # Create OpenAI assistant
   assistant = client.beta.assistants.create(
      name="Storyteller Bot",
      instructions=(
         "You are a storyteller. When given a book cover image, "
         "provide a brief story summary as if you were telling a bedtime story."
      ),
      model="gpt-4o-mini",
   )

   # Create a conversation thread
   thread = client.beta.threads.create()

   button.when_activated = capture_photo

   try:
      print(f'\033[1;30m{"Waiting for button press to capture photo..."}\033[0m')
      print(f'\033[1;30m{"Tap any key to exit..."}\033[0m')
      import signal
      signal.pause()  # Use signal.pause() on Unix to keep the script running
   finally:
      # Clean up resources
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up. Exiting.")



----------------------------------------------


**Code Explanation**

1. Import Necessary Libraries

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import readline  # Optimize keyboard input
   import sys
   import os
   from pathlib import Path
   import subprocess
   from fusion_hat import Pin
   from picamera2 import Picamera2

* ``openai``: Schnittstelle zu OpenAIs GPT- und Whisper-Modellen.
* ``fusion_hat``: Verarbeitung des Tastendrucks zum Auslösen der Aufnahme.
* ``picamera2``: Steuerung der Raspberry-Pi-Kamera für Fotos.
* ``subprocess``: Abspielen der Audiodateien für die Sprachausgabe.


2. Initialize OpenAI Client and Hardware

.. code-block:: python

   client = openai.OpenAI(api_key=OPENAI_API_KEY)

Richtet den OpenAI-Client mit dem bereitgestellten API-Schlüssel für den Zugriff auf GPT- und Whisper-Modelle ein.

.. code-block:: python

   button = Pin(17, Pin.IN, Pin.PULL_DOWN)
   camera = Picamera2()

Der an GPIO-Pin 17 angeschlossene Taster startet den Aufnahmevorgang. Die Instanz ``Picamera2`` steuert die Raspberry-Pi-Kamera.


3. Capture Photo

.. code-block:: python

   def capture_photo():
      """
      Capture a photo using the Picamera2 and save it as 'my_photo.jpg'.
      """
      try:
         print(f'\033[1;30m{"Shooting photo..."}\033[0m')
         # Set preview configuration
         camera.configure(camera.preview_configuration)
         camera.start()
         camera.capture_file("my_photo.jpg")
         camera.stop()
      except Exception as e:
         print(f"Error capturing photo: {e}")

* Konfiguriert die Vorschau der Kamera.
* Startet die Kamera und nimmt ein Foto auf.
* Speichert das Bild als `my_photo.jpg`.

4. Text-to-Speech Conversion

.. code-block:: python

   def text_to_speech(text):
      """
      Convert text to speech using OpenAI's TTS model.
      """
      speech_file_path = Path(__file__).parent / "speech.mp3"
      try:
         with client.audio.speech.with_streaming_response.create(
               model="tts-1", voice="alloy", input=text
         ) as response:
               response.stream_to_file(speech_file_path)
         subprocess.Popen("mplayer speech.mp3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
      except Exception as e:
         print(f"Error in Text-to-Speech: {e}")

* Wandelt die GPT-Antwort mit dem Text-zu-Sprache-Modell (``speech.mp3``) in Audio um.
* Gibt die Audiodatei per ``mplayer`` wieder.


5. Interact with GPT for Storytelling

Die Funktion ``story_talking()``:

.. code-block:: python

   file = client.files.create(
      file=open("my_photo.jpg", "rb"), purpose="vision"
   )

Foto hochladen: Das aufgenommene Bild (``my_photo.jpg``) wird zur Verarbeitung an OpenAI gesendet.


.. code-block:: python

   message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=[
            {"type": "text", "text": "What is this book about?"},
            {"type": "image_file", "image_file": {"file_id": file.id}},
      ],
   )

Benutzeranfrage senden: Die Nachricht wird zusammen mit dem Foto an den Assistenten übermittelt.

.. code-block:: python

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
                        print(f"Assistant >>> {response}")
                        text_to_speech(response)
                        return

Verarbeitung der GPT-Antwort: GPT erzeugt eine Zusammenfassung der Geschichte, die ausgegeben und anschließend vorgelesen wird.

6. OpenAI Assistant Configuration

.. code-block:: python

   assistant = client.beta.assistants.create(
      name="Storyteller Bot",
      instructions=(
         "You are a storyteller. When given a book cover image, "
         "provide a brief story summary as if you were telling a bedtime story."
      ),
      model="gpt-4o-mini",
   )

Definiert die Rolle des Assistenten und stellt sicher, dass Antworten für Storytelling geeignet formuliert sind.


7. Event Loop

.. code-block:: python

   try:
      while True:
         print(f'\033[1;30m{"Waiting for button press to capture photo..."}\033[0m')
         button.wait_for_press()
         capture_photo()
         story_talking()
   finally:
      # Clean up resources
      button.close()
      client.beta.assistants.delete(assistant.id)
      print("Resources cleaned up. Exiting.")

* Wartet auf einen Tastendruck.
* Nimmt bei Tastendruck ein Foto auf.
* Sendet das Foto an GPT für das Storytelling.
* Spielt die generierte Geschichte per TTS ab.
* Der finally-Block sorgt für sauberes Aufräumen.


----------------------------------------------


**Debugging Tips**

1. Camera Issues: 
   
   * Stellen Sie sicher, dass die Raspberry-Pi-Kamera aktiviert und korrekt angeschlossen ist. Prüfen Sie die Kameraeinstellungen mit raspi-config.

2. Incomplete Book Cover in Photo:
   
   * Da dieses Projekt keinen Vorschaubildschirm nutzt, achten Sie vor dem Tastendruck auf die richtige Positionierung des Buches:
      
      * Platzieren Sie das Buch in konstantem Abstand und Winkel zur Kamera.
      * Verwenden Sie eine feste Halterung oder Führung, damit das Cover vollständig ins Bild passt.
      * Testen Sie verschiedene Setups, um die optimale Position für reproduzierbare Ergebnisse zu finden.
   
   * Wenn weiterhin Beschnittprobleme auftreten, ziehen Sie für die Einrichtung einen angeschlossenen Bildschirm oder ein externes Gerät zur Kontrolle der Ausrichtung in Betracht.
