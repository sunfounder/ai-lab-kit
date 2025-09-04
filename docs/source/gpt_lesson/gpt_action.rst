.. _gpt_easy_action:


1.7 Take Action
==========================

In den letzten Jahren hat die Konvergenz von Künstlicher Intelligenz (KI) und dem Internet of Things (IoT) eine Revolution in der Smart-Home-Technologie ausgelöst. Durch die Integration von KI-Fähigkeiten mit physischen Geräten lassen sich hochgradig interaktive und reaktionsfähige Umgebungen schaffen. Dieses Tutorial zeigt, wie OpenAI genutzt werden kann, um ein physisches Gerät – konkret eine RGB-LED – über natürliche Sprachbefehle zu steuern. Eine solche Integration ebnet den Weg für intelligente Systeme, die den Alltag bereichern, indem sie auf Sprachbefehle reagieren, beispielsweise zur Anpassung der Beleuchtung je nach Stimmung oder Tageszeit.

Die Möglichkeit, Geräte mithilfe von KI zu steuern, bietet nicht nur Komfort, sondern auch personalisierte Nutzererlebnisse. Dieses Projekt bildet eine ausgezeichnete Grundlage für die weitere Erkundung im Bereich Smart Home, in dem sich Geräte nahtlos an individuelle Vorlieben und Umweltbedingungen anpassen können.


Dieses Tutorial demonstriert, wie OpenAI eingesetzt werden kann, um einen Raspberry Pi in ein Steuerzentrum für eine RGB-LED-Lampe zu verwandeln. Der Prozess umfasst das Verstehen der Benutzerbefehle durch OpenAI und deren Übersetzung in konkrete Anweisungen, die die Farben und das Verhalten der LED steuern. Dieses Beispiel lässt sich zu komplexeren Szenarien im Smart-Home-Bereich erweitern, wie etwa sprachgesteuerte Temperaturregelung, Sicherheitssysteme oder sogar die Koordination mehrerer Geräte.

Am Ende dieses Tutorials wirst du in der Lage sein, eine KI-gestützte Schnittstelle aufzubauen, die natürliche Sprache interpretiert und mit physischer Hardware interagiert. Dies ist ein wichtiger Schritt hin zur Entwicklung fortschrittlicher Systeme, wie man sie in modernen Smart-Home-Umgebungen findet.

----------------------------------------------

**What You’ll Need**

Die folgenden Komponenten werden für dieses Projekt benötigt:


.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK

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

Der gesamte in diesem Kurs verwendete Beispielcode befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Gehe wie folgt vor, um das Beispiel auszuführen:


.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy_action.py

----------------------------------------------

**Code**

Hier ist der vollständige Beispielcode:


.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   from pathlib import Path

   import readline # optimize keyboard input, only need to import
   import sys
   import os
   import subprocess

   from fusion_hat import RGB_LED,PWM

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
      - `color`: A list of three floating-point values representing the RGB color components (each between 0 and 255).
      - `message`: A textual response to the user.

   **Example JSON Output**:
   {
   "color": [125, 100, 50],
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

   # Initialize an RGB LED.
   rgb_led = RGB_LED(PWM('P0'), PWM('P1'), PWM('P2'),common=RGB_LED.CATHODE)



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
      client.beta.assistants.delete(assistant.id)



----------------------------------------------

**Code Explanation**


In diesem Abschnitt werden die neuen Funktionen hervorgehoben,  
darunter die Steuerung einer physischen RGB-Lampe sowie das Parsen der vom Assistant zurückgegebenen JSON-Daten.  
Details zur Ansteuerung von RGB-Lampen findest du unter :ref:`1.1.2_py`.  
Im Folgenden liegt der Fokus auf dem Parsen von JSON und dessen wichtigsten Aspekten.


.. code-block:: python
   :emphasize-lines: 40-55

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
   "color": [125, 100, 50],
   "message": "Setting a warm and relaxing light for you."
   }
   '''

   # assistant=client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)
   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4-1106-preview",
   )

   try:
      while True:
         ...
         if run.status == "completed":
            ...
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
                        ...
                  break # only last reply


Der hervorgehobene Teil des Codes ist entscheidend, um sinnvolle Informationen aus den Antworten des Assistants zu extrahieren.  
Hierbei werden JSON-Strings geparst, um ``color`` (RGB-Werte) und ``message`` (Textnachricht) zu erhalten, mit denen das Licht gesteuert und Sprachausgaben generiert werden.

.. code-block:: python

   try:
      value = eval(value)  # Versuch, den String in eine Python-Datenstruktur zu parsen
   except Exception as e:
      value = str(value)  # Falls das Parsen fehlschlägt, den Originalstring behalten

``eval(value)`` versucht, den JSON-String der KI in ein Python-Dictionary umzuwandeln.

* **Example Input:** ``'{"color": [125, 100, 50], "message": "Setting a warm light."}'``
* **Example Output:** ``{'color': [125, 100, 50], 'message': 'Setting a warm light.'}``


Wenn das Parsen fehlschlägt (z. B. bei ungültigem JSON), wird der Originalstring beibehalten,  
um Abstürze zu vermeiden und die Fehlersuche zu erleichtern.


.. code-block:: python

   if isinstance(value, dict):

Dies stellt sicher, dass das Ergebnis ein Dictionary ist und somit korrekt formatiertes JSON vom Assistant zurückgegeben wurde.  
Falls die Antwort kein Dictionary ist, greift eine Fallback-Logik.



.. code-block:: python

   if 'color' in value:
      color = list(value['color'])
   else:
      color = [0,0,0]

Hier wird das Feld ``color`` aus dem Dictionary extrahiert.  
Ist es vorhanden, werden die Werte in eine Liste konvertiert, um die RGB-Lampe direkt zu steuern.  
Fehlt es, wird der Standardwert ``[0, 0, 0]`` gesetzt (Lampe aus).


.. code-block:: python

   if 'message' in value:
      text = value['message']
   else :
      text = ''

Hier wird das Feld ``message`` extrahiert. Falls es fehlt, wird ein leerer String zurückgegeben,  
was bedeutet, dass keine Nachricht für die Sprachausgabe vorliegt.


.. code-block:: python

   else:
      color = [0,0,0]
      text = value

Falls ``value`` kein Dictionary ist (z. B. Fehlermeldung oder unstrukturierter Text),  
wird standardmäßig das Licht ausgeschaltet (``[0, 0, 0]``), und der rohe Output als Nachricht für Debugging oder Benutzerhinweise verwendet.

Insgesamt ist das JSON-Parsen die zentrale Logik in diesem Beispiel,  
da es sicherstellt, dass die Ausgabe des Assistants korrekt interpretiert wird, um die RGB-Lampe zu steuern und Sprachausgabe zu erzeugen.


----------------------------------------------

**Debugging Tips**

In diesem Abschnitt findest du praktische Hinweise zur Fehlersuche bei typischen Problemen, die während der Arbeit an diesem Projekt auftreten können.  
Mit diesen Tipps stellst du sicher, dass dein Setup wie vorgesehen funktioniert und eventuelle Fehler effizient diagnostiziert werden können.

1. **Wenn die RGB-Lampe nicht funktioniert:**


   - **Verkabelung prüfen:** Achte darauf, dass alle Kabel sicher verbunden sind und die GPIO-Pins korrekt konfiguriert wurden. Lockere Verbindungen sind eine häufige Fehlerquelle.
   - **Pin-Konfiguration verifizieren:** Überprüfe, ob ``RGBLED(red=23, green=24, blue=25)`` im Code den tatsächlich genutzten GPIO-Pins entspricht.
   - **LED testen:** Tausche die LED aus, um ein defektes Bauteil auszuschließen.

2. **Wenn die Ausgabe der KI nicht im JSON-Format ist:**

   - **Anweisungen überprüfen:** Stelle sicher, dass im ``instructions_text`` eindeutig angegeben ist, dass die Ausgabe im JSON-Format erfolgen soll.
   - **Rohdaten inspizieren:** Verwende ``print(f"Raw AI Response: {value}")`` unmittelbar nach Empfang der Antwort, um das Format zu überprüfen.
   - **JSON validieren:** Wenn du JSON manuell verarbeitest, prüfe, ob der String gültiges JSON ist. Tools wie JSONLint helfen beim Validieren und Formatieren.

3. **Wenn Text-to-Speech nicht funktioniert:**

   - **MP3-Dateierstellung prüfen:** Stelle sicher, dass die Funktion ``text_to_speech`` MP3-Dateien korrekt erzeugt. Überprüfe Dateipfad und Zugriffsrechte.
   - **Audioausgabe testen:** Achte darauf, dass die Audioausgabe des Raspberry Pi korrekt eingerichtet ist und die Lautstärke hoch genug ist.
   - **MPlayer-Installation verifizieren:** Stelle sicher, dass ``mplayer`` korrekt installiert ist. Falls nötig, installiere es mit ``sudo apt install mplayer`` neu.

4. **Allgemeine Software-Fehlersuche:**

   - **Logs überwachen:** Behalte Log-Dateien im Blick, um Fehlerhinweise zu erhalten. Mit ``tail -f /var/log/syslog`` kannst du System-Logs in Echtzeit anzeigen.
   - **Software aktualisieren:** Stelle sicher, dass dein Raspberry Pi und alle zugehörigen Programme auf dem neuesten Stand sind. Nutze ``sudo apt update`` und ``sudo apt upgrade`` zur Aktualisierung.
   - **API-Nutzung prüfen:** Achte darauf, dass deine API-Aufrufe innerhalb der Nutzungslimits liegen und der API-Schlüssel korrekt ist.
