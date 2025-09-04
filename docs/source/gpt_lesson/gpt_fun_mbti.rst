2.7 MBTI-Persönlichkeitstest
======================================

In diesem Beispiel lernen Sie, wie Sie mit dem GPT-Modell von OpenAI und einem 4x4-Tastenfeld auf einem Raspberry Pi (oder vergleichbarer Hardware) einen einfachen MBTI-Persönlichkeitstest (Myers-Briggs Type Indicator) entwickeln.  

Die Nutzer beantworten Fragen, indem sie Tasten auf dem Keypad drücken, und der GPT-Assistent erstellt nach Beantwortung aller Fragen das entsprechende MBTI-Ergebnis.


----------------------------------------------

**Features**


1. **Eingabe über das Keypad**: Der Nutzer drückt eine Taste (1 bis 5), die angibt, in welchem Maß er einer Aussage zustimmt oder nicht zustimmt.  
2. **Das Programm sendet** diesen Tastendruck als Benutzereingabe an GPT.  
3. **GPT** gibt entweder die nächste Frage oder eine Zusammenfassung der bisherigen Ergebnisse zurück, gemäß den definierten Anweisungen.  
4. **Die Schleife** läuft so lange, bis alle 10 Fragen beantwortet sind und GPT eine abschließende MBTI-Auswertung erstellt.

----------------------------------------------


**Benötigte Komponenten**

Für dieses Projekt werden die folgenden Komponenten benötigt:


.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - KOMPONENTENBESCHREIBUNG
        - KAUFLINK

    *   - :ref:`cpn_keypad`
        - |link_keypad_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

----------------------------------------------

**Schaltplan**

.. image:: img/fzz/2.1.8_bb.png
   :width: 800
   :align: center


----------------------------------------------

**Beispiel ausführen**


Der gesamte Beispielcode in diesem Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_mbti.py 

----------------------------------------------

**Code**

.. raw:: html

   <run></run>

.. code-block:: python
      
   import openai
   from keys import OPENAI_API_KEY
   import sys
   from fusion_hat import Keypad

   # Initialize OpenAI client
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   instructions_text = '''
   You are an MBTI personality test assistant. Your role is to ask me a series of personality-related questions and assess my MBTI type based on my responses. Please follow these guidelines:

   1. **Rules Overview**: Before asking, briefly explain how the test works and how I should answer.
   2. **Numbered Questions**: Each question must be labeled with a number (e.g., “Question 1: …,” “Question 2: …”) for clarity.
   3. **Answer Format**: I will respond with a number from 1 to 5, where:
      - 1: Strongly disagree
      - 2: Disagree
      - 3: Neutral
      - 4: Agree
      - 5: Strongly agree
   4. **Question Count**: After I have answered 10 questions, please use my responses to generate my MBTI result and provide a concise explanation.
   5. **Style Requirements**: Maintain a concise, friendly tone without adding extraneous details.

   Once all 10 questions are answered, please provide a summary and give me the final MBTI result.
   '''

   # Create or retrieve the assistant
   assistant = client.beta.assistants.create(
      name="MBTI_Assistant",
      instructions=instructions_text,
      model="gpt-4-1106-preview",
   )

   # Create a conversation thread
   thread = client.beta.threads.create()


   def process_user_input(keypad, count):
      """
      Handles user input through the keypad or initiates the test.
      """
      if count == 0:
         return "10 questions to test personality! Let's go!", count + 1

      while True:
         pressed_keys = keypad.read()
         if pressed_keys:
               print(f"Key pressed: {pressed_keys}")
               return pressed_keys[0], count + 1


   try:
      # Configure rows, columns, and keypad layout
      rows_pins = [4, 17, 27, 22]
      cols_pins = [23, 24, 25, 12]
      keys = ["1", "2", "3", "A",
               "4", "5", "6", "B",
               "7", "8", "9", "C",
               "*", "0", "#", "D"]

      keypad = Keypad(rows_pins, cols_pins, keys)
      count = 0

      while count<=10:

         msg = ""
         msg, count = process_user_input(keypad, count)

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
                              print(f'{label:>10} >>> {value}')
                     break # only last reply

      input("\n Press enter for quit.")

   finally:
      client.beta.assistants.delete(assistant.id)
      print("\n Delete Assistant ID")

----------------------------------------------

**Code Erklärung**


1. **Import der Bibliotheken**

   * ``openai``: Schnittstelle zur OpenAI API.  
   * ``fusion_hat``: Verwaltung der GPIO-Pins für das Ansteuern der Keypad-Reihen und -Spalten.  
   * ``sys``: Zugriff auf systembezogene Funktionen, z. B. zur Verarbeitung von Kommandozeilenargumenten (hier nur am Rande genutzt).  

2. **Initialisierung des OpenAI-Clients**

   .. code-block:: python

      client = openai.OpenAI(api_key=OPENAI_API_KEY)

   Erstellt eine Clientinstanz unter Verwendung des API-Schlüssels aus der Datei ``keys.py``.

3. **Anweisungen für den GPT-Assistenten**

   .. code-block:: python

      instructions_text = '''
         ...
      '''
      assistant = client.beta.assistants.create(
         ...
      )

   * **instructions_text** beschreibt das gewünschte Verhalten des Assistenten.  
   * **create**: Erstellt einen GPT-Assistenten mit den angegebenen Instruktionen und Modellparametern.  

4. **Konversations-Thread**

   .. code-block:: python

      thread = client.beta.threads.create()

   Ein Konversationsthread speichert den Kontext zwischen Benutzereingaben und den Antworten des Assistenten.  


5. **Verarbeitung der Benutzereingaben**

   .. code-block:: python

      def process_user_input(keypad, count):
          ...

   * Falls ``count == 0``, wird eine Einleitung zurückgegeben, die den Test startet.  
   * Ansonsten liest die Funktion Tasteneingaben vom Keypad.  
   * Jede Eingabe wird zurückgegeben und der Zähler erhöht.  

6. **Hauptschleife**

   .. code-block:: python

      while count <= 10:
          msg, count = process_user_input(keypad, count)
          ...

   * Läuft solange, bis der Nutzer 10 Fragen beantwortet hat.  
   * Sendet jede Eingabe (``msg``) an den GPT-Assistenten und gibt die jeweilige Antwort zurück.  

7. **OpenAI-Assistant-Aufrufe**

   .. code-block:: python

      message = client.beta.threads.messages.create(...)
      run = client.beta.threads.runs.create_and_poll(...)

   * ``create``: Erstellt eine Benutzernachricht im Thread.  
   * ``create_and_poll``: Startet den Assistenten und wartet bis zur Fertigstellung.  

8. **Antwortverarbeitung**

   .. code-block:: python

      if run.status == "completed":
          messages = client.beta.threads.messages.list(thread_id=thread.id)
          ...

   * Durchläuft ``messages.data``, um die Antwort des Assistenten (``role == 'assistant'``) zu finden.  
   * Gibt die Benutzereingaben und Assistentenantworten aus.  

9. **Aufräumen**

   .. code-block:: python

      finally:
         client.beta.assistants.delete(assistant.id)
         print("\n Delete Assistant ID")

   * Löscht die Assistenteninstanz beim Beenden, um Ressourcen freizugeben.  

----------------------------------------------

**Debugging Tipps**

1. **Keypad reagiert nicht:**  

   * Stellen Sie sicher, dass die Reihen- und Spalten-Pins korrekt mit den GPIO-Pins verbunden sind.  
   * Prüfen Sie, ob die Bibliothek ``fusion_hat`` installiert und korrekt konfiguriert ist.  

2. **GPT-Assistent antwortet nicht:**  

   * Überprüfen Sie Ihren API-Schlüssel und die Assistenten-ID in ``keys.py``.  
   * Stellen Sie sicher, dass der Assistent erfolgreich erstellt wurde, indem Sie seinen Status mit ``client.beta.assistants.retrieve(assistant_id)`` prüfen.  

3. **Antwortformat von GPT fehlerhaft:**  

   * Wenn GPTs Antwort nicht dem erwarteten Format entspricht, nutzen Sie ``print(f"Raw Response: {value}")``, um die Rohdaten auszugeben.  
   * Überprüfen Sie die Anweisungen an GPT und stellen Sie sicher, dass das erwartete Ausgabeformat eindeutig definiert ist.  

4. **Allgemeine Fehlersuche:**  

   * Nutzen Sie Print-Ausgaben an kritischen Stellen im Code, um Variablen wie ``msg``, ``count`` und Assistentenantworten zu überprüfen.  
   * Ergänzen Sie Fehlerbehandlung, um unerwartete Probleme abzufangen und nützliche Debug-Informationen zu liefern.  
