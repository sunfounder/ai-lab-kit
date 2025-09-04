.. _gpt_easy_feel:

1.6 How Does It Feel?
============================

In der schnelllebigen Technologiewelt eröffnet die Verknüpfung von Künstlicher Intelligenz (KI) mit realen Sensoren eine Fülle an Möglichkeiten für intelligentere und reaktionsfähigere Umgebungen. Dieses Kapitel zeigt, wie KI traditionelle Grenzen überschreiten und direkt mit der physischen Umgebung interagieren kann, um Entscheidungsprozesse und Nutzererlebnisse zu verbessern.

Durch den Einsatz von Sensoren wie Fotowiderständen, die das Umgebungslicht messen, kann KI Umgebungsbedingungen in Echtzeit verstehen und darauf reagieren. Dabei geht es nicht nur um Datenverarbeitung, sondern um ein kontextbezogenes Verständnis der Welt. Eine mit Lichtsensoren integrierte KI kann beispielsweise die Beleuchtung zu Hause automatisch anpassen, Sicherheitssysteme verbessern oder den Energieverbrauch anhand von Echtzeitdaten optimieren.

Die potenziellen Anwendungsfälle sind vielfältig. Von intuitiveren, ansprechenden Smart-Home-Lösungen bis hin zu Systemen, die sich an wechselnde Umgebungsbedingungen im Sinne von Barrierefreiheit oder Effizienz anpassen – die Möglichkeiten sind nahezu grenzenlos. Am Ende dieses Kapitels wirst du verstehen, wie du die Leistungsfähigkeit von KI und Sensoren wie dem Fotowiderstand nutzt, um Anwendungen zu entwickeln, die nicht nur reagieren, sondern den Bedarf der Nutzer auf Basis ihrer unmittelbaren Umgebung antizipieren.

Anhand praxisnaher Beispiele führt dich dieses Kapitel durch das Einrichten deines Raspberry Pi zur Erfassung von Umgebungsdaten und deren Nutzung, um KI-Entscheidungen zu beeinflussen. Dieser Ansatz fügt Projekten eine Ebene der Interaktivität hinzu und hilft zugleich, zu entmystifizieren, wie KI im Alltag angewendet werden kann, um Technik nützlicher und reaktionsfreudiger zu machen.


----------------------------------------------

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
    *   - :ref:`cpn_photoresistor`
        - |link_photoresistor_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------


**Diagram**


.. image:: img/fzz/gpt_feel_bb.png
   :width: 800
   :align: center


----------------------------------------------


**Running the Example**

Der gesamte in diesem Kurs verwendete Beispielcode befindet sich im Verzeichnis ``ai-explorer-lab-kit``. Folge den nachstehenden Schritten, um dieses Beispiel auszuführen:


.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy_feel.py

----------------------------------------------

**Code**

Nachfolgend der vollständige Beispielcode:


.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   from pathlib import Path

   import readline # optimize keyboard input, only need to import
   import sys
   import os
   import subprocess
   from fusion_hat import ADC

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)
   os.system("fusion_hat enable_speaker")

   TTS_OUTPUT_FILE = 'tts_output.mp3'

   # Set up the photoresistor 
   photoresistor = ADC('A0')

   instructions_text = '''
   You are a light assistant. Your task is to determine if the current light conditions are suitable for reading based on the photosensor value provided by the user. 

   The photosensor value range is:
   - 0: Brightest
   - 4095: Darkest

   Input Format:
   "photoresistor: [value], message: [user query]"

   Output Guidelines:
   1. If the light is sufficient for reading (e.g., value <= 2000), respond positively.
   2. If the light is too dim (e.g., value > 2000), suggest increasing brightness.
   3. Include the sensor value in your response to explain your reasoning.

   Example Input:
   photoresistor: 150, message: Is the light good for reading?

   Example Output:
   Yes, the light is suitable for reading. A value of 150 indicates moderate brightness.

   '''


   assistant = client.beta.assistants.create(
      name="BOT",
      instructions=instructions_text,
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()

   def text_to_speech(text):
      speech_file_path = Path(__file__).parent / "speech.mp3"
      # print(speech_file_path)
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

         text_send="photoresistor:" +str(photoresistor.read()) +" , message: " + msg

         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=text_send,
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
                              text = block.text.value
                              print(f'{label:>10} >>> {text}')
                     break # only last reply

               for message in messages.data:
                  if message.role == 'assistant':
                     for block in message.content:
                           if block.type == 'text':
                              label = assistant.name
                              text = block.text.value
                              print(f'{label:>10} >>> {text}')
                              text_to_speech(text)
                                                   break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)




----------------------------------------------


**Code Explanation**

Dieses Beispiel baut auf :ref:`gpt_easy_tts` auf; der wesentliche Unterschied ist die Integration des ``ADC``-Moduls. Zu den wichtigsten Änderungen gehören die folgenden:

.. code-block:: python
   :emphasize-lines: 3,8,18,23

   import openai
   ...
   from fusion_hat import ADC

   ...

   # Set up the photoresistor 
   photoresistor = ADC('A0')

   ...

   try:
      while True:
         msg = input(f'\033[1;30m{"Input: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')
         if msg == False or msg == "":
            continue

         text_send="photoresistor:" +str(photoresistor.read()) +" , message: " + msg

         message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=text_send,
         )

Der Fotowiderstand ist ein Sensor, dessen Widerstand sich mit der Umgebungshelligkeit ändert. Über den Fusion HAT wird sein analoges Signal in einen digitalen Wert umgesetzt, den die KI verarbeiten kann. Weitere Einzelheiten zur Verwendung des ADC-Moduls findest du unter :ref:`2.2.1_py`.

In diesem Projekt erhält die KI den Messwert des Fotowiderstands zusammen mit einer Nutzeranfrage und kann so beurteilen, ob die Umgebung zum Lesen geeignet ist.

----------------------------------------------

**Crafting Effective AI Instructions**

Ein gut formuliertes ``instructions_text`` ist entscheidend, um das Verhalten der KI zu steuern und sicherzustellen, dass sie korrekt sowohl mit dem Nutzer als auch mit den Sensordaten interagiert. Das ``instructions_text`` dient der KI als Vorgabe: Es legt ihre Rolle fest, wie Eingaben zu interpretieren sind und wie Ergebnisse zu kommunizieren sind. Nachfolgend findest du Schritte und Überlegungen für wirksame Anweisungen:

1. **Define the AI's Role Clearly**

Beginne damit, ausdrücklich zu benennen, was die KI tun soll. So lässt sich der Rest der Anweisungen um diesen Zweck herum strukturieren. Zum Beispiel:

- "You are a light assistant. Your primary task is to assess ambient light conditions and provide recommendations for reading comfort based on the sensor data received."

2. **Specify Input and Output Formats**

Klarheit darüber, welche Eingaben die KI erhält und welche Ausgaben erwartet werden, ist wesentlich. Lege Format und Datentypen eindeutig fest:

- **Input Format**: Gib an, wie die Eingabe aussieht, z. B. „You will receive input in the format: ``photoresistor: [value], message: [user query]``.“

- **Output Format**: Beschreibe den Aufbau der Antwort, z. B. „Respond with a direct statement about the lighting condition followed by a suggestion if necessary.“

3. **Provide Context and Parameters**

Vermittle den Kontext, in dem die KI arbeitet, einschließlich relevanter Schwellwerte oder Parameter:

- "Consider light levels suitable for reading as any value from 0 to 100, where 0 is the brightest and 100 still acceptable. Values above 100 should trigger a suggestion to increase lighting."

4. **Use Examples to Guide Expectations**

Verwende Beispiele, um das erwartete Verhalten zu zeigen. Das klärt nicht nur die Anforderungen, sondern hilft auch beim Debuggen:

- **Example Input**: "photoresistor: 80, message: Is the lighting adequate for reading?"

- **Example Output**: "Yes, the light level is adequate for reading. A value of 80 is comfortably bright."

5. **Set Guidelines for Tone and Style**

Der Kommunikationsstil beeinflusst das Nutzererlebnis. Lege Ton und Stil fest:

- "Respond in a friendly and professional tone. Prioritize clarity and brevity in your recommendations."

6. **Highlight Constraints and Prohibitions**

Formuliere klar, was vermieden werden soll:

- "Avoid giving advice that could be construed as medical, such as commenting on the health effects of lighting conditions."

7. **Encourage Feedback Incorporation**

Ermutige die KI, Feedback einzuholen, um die Genauigkeit im Zeitverlauf zu verbessern:

- "Ask users for feedback on your recommendations to improve accuracy and user satisfaction."

**Iterative Refinement**

- Fordere die Nutzer auf, die Anweisungen anhand realer Interaktionen zu testen und zu verfeinern. Reale Nutzung liefert oft entscheidende Einsichten, die die Leistung und Zuverlässigkeit der KI deutlich steigern.

Durch das Befolgen dieser Schritte lässt sich ein ``instructions_text`` erstellen, das den KI-Einsatz wirksam steuert, die Funktionalität verbessert und sicherstellt, dass die KI ihre Aufgaben präzise erfüllt. So verbessert sich die Interaktion zwischen KI und Nutzer, und die Fähigkeiten der KI werden genutzt, um sinnvolle, kontextgerechte Antworten zu liefern.


-------------------------------------------------

**Troubleshooting**

Die Integration von Sensoren in KI-Systeme – insbesondere auf hardwareseitig eingeschränkten Plattformen wie dem Raspberry Pi – kann eine Reihe von Herausforderungen mit sich bringen. Nachfolgend häufige Probleme und effektive Maßnahmen zur Fehlersuche:

1. **Incorrect Sensor Readings**

**Problem:** Der Sensor (z. B. ein Fotowiderstand) liefert ungenaue Messwerte oder zeigt ständig Maximal- bzw. Minimalwerte an.

**Solutions:**

- **Check Connections**: Prüfe alle Verbindungen gemäß Schaltplan. Lockere Leitungen verursachen häufig inkonsistente Messwerte.
- **Verify Component Integrity**: Teste den Sensor – sofern möglich – separat mit einem Multimeter, um seine Funktion zu überprüfen.
- **Adjust Calibration**: Manche Sensoren benötigen eine Kalibrierung. Sieh in der Dokumentation nach und passe ggf. die Softwareparameter an.



2. **Software Bugs**

**Problem:** Das Programm stürzt ab oder verhält sich unerwartet.

**Solutions:**

- **Debugging Output**: Füge vor und nach kritischen Operationen Ausgaben ein, um den Fehlerpunkt einzugrenzen.
- **Code Review**: Überprüfe den Code auf syntaktische und logische Fehler. Achte besonders auf die Datenweitergabe zwischen Funktionen.
- **Environment Issues**: Prüfe Python-Version und Bibliotheken. Inkompatibilitäten können zu unerwartetem Verhalten führen.

3. **AI Model Does Not Respond Appropriately**

**Problem:** Das KI-Modell erzeugt auf Basis der Sensordaten keine geeigneten Antworten.

**Solutions:**

- **Review AI Instructions**: Stelle sicher, dass die Anweisungen klar beschreiben, wie die Sensordaten zu interpretieren sind und wie darauf zu reagieren ist.
- **Data Format**: Prüfe, ob die Sensordaten vor dem Senden korrekt formatiert sind. Falsche Formate oder Typen führen zu unpassendem Verhalten.
- **Model Limitations**: Berücksichtige Modellgrenzen. Manche Modelle benötigen Feintuning oder spezielles Training für individuelle Szenarien.

4. **Audio Output Issues**

**Problem:** Bei KI-Antworten ist kein Ton zu hören oder die Audioqualität ist schlecht.

**Solutions:**


- **Volume Settings**: Prüfe die Lautstärkeeinstellungen des Raspberry Pi – möglicherweise sind sie stummgeschaltet oder zu niedrig.
- **Audio Drivers**: Verifiziere, dass die passenden Audiotreiber installiert sind und keine Konflikte mit anderer Software bestehen.

Wenn du diese Punkte systematisch abarbeitest, reduzierst du Ausfallzeiten und Frustration. Denke daran: Fehlersuche ist häufig ein iterativer Prozess – Geduld und methodisches Vorgehen sind der Schlüssel zu einer erfolgreichen Diagnose und Behebung.
