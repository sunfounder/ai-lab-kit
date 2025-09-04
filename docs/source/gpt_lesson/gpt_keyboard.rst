.. _gpt_easy_keyboard:

1.3 Real-Time Interaction
==========================

Dieses Beispiel zeigt einen einfachen Chatbot, der in Echtzeit mit Nutzern interagiert, Eingaben verarbeitet und generierte Antworten zurückgibt. Es demonstriert, wie die OpenAI-API verwendet wird, um Textnachrichten zu senden und zu empfangen.

----------------------------------------------

**Running the Example**

Der gesamte in diesen Lektionen verwendete Beispielcode befindet sich im Verzeichnis ``ai-explorer-lab-kit``. 
Sie können das Beispiel mit den folgenden Schritten ausführen:


.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy_keyboard.py


----------------------------------------------

**Code**

Der vollständige Beispielcode lautet:

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY

   import readline # Verbessert die Kommandozeileneingabe, z. B. durch Textnavigation und Verlauf.
   import sys # Bietet Zugriff auf systemspezifische Parameter und Funktionen.


   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions="You are a chat bot, you answer people question to help them. ",
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()

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
                  break # only last reply

   finally:
      client.beta.assistants.delete(assistant.id)
      print("\n Delete Assistant ID")

----------------------------------------------

**Code Explanation**

Dieses Beispiel baut auf :ref:`gpt_easy` auf und enthält zwei wesentliche Änderungen:

1.  Hinzufügen der Tastatureingabe

   .. code-block:: python
      :emphasize-lines: 4,5,18,19,20,21,22

      import openai
      from keys import OPENAI_API_KEY

      import readline # Verbessert die Kommandozeileneingabe, z. B. durch Textnavigation und Verlauf.
      import sys # Bietet Zugriff auf systemspezifische Parameter und Funktionen.

      # gets API Key from environment variable OPENAI_API_KEY
      client = openai.OpenAI(api_key=OPENAI_API_KEY)

      assistant = client.beta.assistants.create(
         ...
      )

      thread = client.beta.threads.create()

      try:
         while True:
            msg = ""
            msg = input(f'\033[1;30m{"intput: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')
            if msg == False or msg == "":
               print() # new line
               continue

            ...

   Die Bibliothek ``readline`` erweitert die interaktive Eingabe in Unix-ähnlichen Umgebungen. Sie ermöglicht Funktionen wie Verlauf und Autovervollständigung, was die Bedienung deutlich komfortabler macht. Die Bibliothek ``sys`` wird hier genutzt, um systemspezifische Eingabe-Codierungen zu berücksichtigen und so Plattformkompatibilität sicherzustellen.

   In der Hauptschleife wird die Nutzereingabe verarbeitet und an den Assistenten gesendet. Leere Eingaben werden ignoriert.

   Zentrale Zeile für die Eingabeverarbeitung:

   .. code-block:: python

      msg = input(f'\033[1;30m{"input: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')


   Erklärung:

   * ``input()`` : Liest eine Zeile Tastatureingabe.
   * ``f'\033[1;30m{"input: "}\033[0m'`` : Zeigt eine farbig formatierte Eingabeaufforderung im Terminal.

      * ``\033[1;30m`` : ANSI-Sequenz zur Darstellung von grauem, fett formatiertem Text.
      * ``\033[0m`` : Setzt die Textformatierung zurück.

   * ``.encode()`` und ``.decode()``: Konvertieren Eingaben in die systemeigene Standardkodierung (z. B. UTF-8) und zurück, um plattformübergreifende Kompatibilität zu gewährleisten.


2.  Verbesserung der Ausgabe

   .. code-block:: python

      while True:

         ...

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

   In der Hauptschleife werden Informationen empfangen und ausgegeben. ``messages`` enthält sämtliche Nachrichten innerhalb der Konversation. Da beim Durchlaufen mehrere Nachrichten zurückgegeben werden, sorgt ``break`` dafür, dass nur die jeweils letzte Nachricht des jeweiligen Absenders ausgegeben wird.

-----------------------------------------------------

**Error Handling**

Effektives Fehlermanagement ist entscheidend, um die Zuverlässigkeit und Benutzerfreundlichkeit einer Echtzeit-Chatbot-Anwendung sicherzustellen. Bei der Integration der OpenAI-API in Raspberry-Pi-Projekten können verschiedene Fehler auftreten, die Leistung und Ausgabe beeinflussen. So lassen sich typische Szenarien behandeln:

1. API-Verbindungsfehler

``Problem``: Fehler beim Verbindungsaufbau zur OpenAI-API, verursacht durch Netzwerkprobleme, falsche API-Schlüssel oder Serverausfälle.

``Solution``: Implementieren Sie Wiederholungen mit exponentiellem Backoff. Nutzen Sie try-except-Blöcke, um Verbindungsfehler abzufangen, und versuchen Sie nach kurzer Wartezeit erneut. Stellen Sie sicher, dass Ihr API-Schlüssel korrekt konfiguriert und gültig ist.

.. code-block:: python

   import time import requests

   def send_request(data): 
      retry_count = 0 
      while retry_count < 5: 
         try: 
            response = client.beta.threads.messages.create(**data) 
            return response
         except requests.exceptions.ConnectionError: 
            time.sleep(2 ** retry_count) # Exponentielles Backoff 
            retry_count += 1 
         except openai.Error as e: 
            print(f"API Error: {e}") 
            break 
      else: 
         print("Failed to connect to OpenAI after several attempts.")

2. Rate-Limits und Quoten

``Problem``: Überschreitung von API-Limits oder Quoten, resultierend in HTTP-429-Fehlern (Too Many Requests).

``Solution``: Überwachen Sie Ihre API-Nutzung genau und implementieren Sie ggf. eigene Limits, um Überlastungen zu vermeiden. Fangen Sie Statuscodes 429 explizit ab und pausieren Sie Anfragen.

.. code-block:: python

   def handle_api_call(data):
      try:
         response = send_request(data)
         if response.status_code == 429:
               print("Rate limit exceeded. Waiting before retrying...")
               time.sleep(60)  # Wartezeit von 1 Minute vor erneutem Versuch
               return send_request(data)
         return response
      except Exception as e:
         print(f"Unhandled exception: {e}")

3. Ungültige Anfragen

``Problem``: Übermittlung fehlerhafter Daten oder Parameter an die API, was zu HTTP-400-Fehlern (Bad Request) führt.

``Solution``: Validieren Sie alle Eingaben, bevor diese an die API gesendet werden. Geben Sie dem Nutzer klare Fehlermeldungen zurück, falls das Eingabeformat nicht den Anforderungen entspricht.

.. code-block:: python

   def validate_input(user_input):
      if not user_input.strip():
         raise ValueError("Input cannot be empty.")
      # Zusätzliche Validierung nach Eingabetyp

   try:
      user_input = input("Input: ")
      validate_input(user_input)
      data = {'thread_id': thread.id, 'role': 'user', 'content': user_input}
      response = send_request(data)
      print("Response received:", response.data)
   except ValueError as ve:
      print(ve)

4. Unerwartete Fehler behandeln

``Problem``: Auftreten unvorhergesehener Fehler, die keiner typischen Kategorie entsprechen.

``Solution``: Verwenden Sie einen allgemeinen Exception-Handler als letzte Instanz, um Fehler abzufangen und zu protokollieren. So kann die Anwendung auch bei unvorhergesehenen Problemen stabil weiterlaufen.

.. code-block:: python

   try:
      # Attempt to execute API call
      response = handle_api_call(data)
      print("Assistant response:", response.data)
   except Exception as e:
      print(f"An unexpected error occurred: {e}")

Die Umsetzung dieser Fehlerbehandlungsstrategien trägt dazu bei, dass Ihr Chatbot auch bei gängigen Betriebsproblemen reaktionsfähig und robust bleibt. Testen Sie diese Szenarien frühzeitig in der Entwicklung, um Ihre Ansätze zu verfeinern und die Nutzererfahrung zu verbessern.

