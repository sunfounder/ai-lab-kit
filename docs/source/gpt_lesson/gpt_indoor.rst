.. _gpt_easy:


1.1 Ein einfaches Gespräch
=======================================

Dieses Beispiel zeigt, wie Sie mit der Python-Bibliothek von OpenAI einen Chatbot erstellen und in einem kurzen Dialog mit ihm interagieren können.

----------------------------------------------



**Running the Example**

Der gesamte Beispielcode für diese Lektionen befindet sich im Verzeichnis ``ai-explorer-lab-kit``. Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:

.. code-block:: shell

   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_easy.py

----------------------------------------------

**Code**

Hier ist der vollständige Beispielcode:

.. raw:: html

   <run></run>

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY

   # gets API Key from environment variable OPENAI_API_KEY
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions="You are an Assistant, you answer people's questions to help them.",
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()

   message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content="Who are you?",
   )

   run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant.id,
   )

   if run.status == "completed":
      messages = client.beta.threads.messages.list(thread_id=thread.id)

      for message in messages:
         assert message.content[0].type == "text"
         print({"role": message.role, "message": message.content[0].text.value})

      client.beta.assistants.delete(assistant.id)


----------------------------------------------

**Code Explanation**

Wir unterteilen den Code in mehrere Abschnitte und erläutern jeweils kurz den Zweck.

1. **Creating and Configuring the Client**

   Zunächst wird ein API-Client erstellt und mit Ihrem API-Schlüssel konfiguriert. Der Client übernimmt die Kommunikation mit den OpenAI-Servern, sendet Anfragen und empfängt Antworten.

   .. code-block:: python

      import openai
      from keys import OPENAI_API_KEY

      # gets API Key from environment variable OPENAI_API_KEY
      client = openai.OpenAI(api_key=OPENAI_API_KEY)

2. **Creating the Assistant**

   Als Nächstes wird ein Assistant angelegt.

   Ein Assistant ist eine spezialisierte KI, die OpenAI-Modelle nutzt, um Aufgaben per natürlicher Sprachverarbeitung auszuführen. Assistants lassen sich auf konkrete Anwendungsszenarien zuschneiden.

   .. code-block:: python

      assistant = client.beta.assistants.create(
         name="BOT",
         instructions="You are an Assistant, you answer people's questions to help them.",
         model="gpt-4-1106-preview",
      )

   Hier verwenden wir den `client`, um einen Assistant namens „BOT“ zu erstellen. Er soll Nutzern helfen, indem er Fragen beantwortet, und nutzt das aktuelle GPT-4-Modell.



   **Using Models**

   Sie können mit fortgeschrittenen Modellen wie GPT-4o, GPT-4 oder GPT-3.5 interagieren, die für verschiedene Textgenerationsaufgaben ausgelegt sind. Stand Dezember 2024 sind u. a. folgende Modelle verfügbar:

   .. list-table::
      :widths: 20 80
      :header-rows: 1

      * - Modell
        - Beschreibung
      * - GPT-4o
        - Flaggschiffmodell mit hoher „Intelligenz“ für komplexe, mehrstufige Aufgaben.
      * - GPT-4o mini
        - Leichtgewichtiges, schnelles Modell für einfache, schnelle Aufgaben.
      * - o1-preview und o1-mini
        - Mit Reinforcement Learning trainierte Modelle für fortgeschrittenes Reasoning.
      * - GPT-4
        - Frühere Hochleistungsmodelle.
      * - GPT-3.5 Turbo
        - Schnelles, kostengünstiges Modell für einfache Aufgaben.
      * - DALL·E
        - Bildgenerierung und -bearbeitung aus natürlichsprachigen Prompts.
      * - TTS
        - Wandelt Text in natürlich klingende Sprache um.
      * - Whisper
        - Transkribiert Audio zu Text.
      * - Embeddings
        - Repräsentiert Text als numerische Vektoren.
      * - Moderation
        - Erkennt potenziell sensible oder unsichere Inhalte.

   .. note:: Siehe https://platform.openai.com/docs/models für Details zu verfügbaren Modellen und ihren Fähigkeiten.


3. **Creating a Conversation Thread**

   .. code-block:: python

      thread = client.beta.threads.create()

   Erstellen Sie einen Conversation Thread, der eine unabhängige Sitzung mit dem Assistant darstellt. Jeder Thread bewahrt den Kontext für mehrstufige Dialoge. Später können Sie über ``thread.id`` auf ihn verweisen.

4. **Sending a Message**

   .. code-block:: python

      message = client.beta.threads.messages.create(
         thread_id=thread.id,
         role="user",
         content="Who are you?",
      )

   Senden Sie innerhalb des Threads eine Nachricht an den Assistant.  
   Nachrichten enthalten typischerweise folgende Parameter:

   * ``thread_id=thread.id``: Verknüpft die Nachricht mit einem bestimmten Thread.
   * ``role="user"``: Kennzeichnet die Nachricht als Nutzereingabe. Weitere Rollen sind:

      * ``user``: Nutzer-Nachrichten.
      * ``assistant``: Antworten des Assistants.
      * ``system``: Systemkontext und -vorgaben.

   * ``content="Who are you?"``: Der eigentliche Nachrichtentext.

   In der Praxis senden Sie mehrere Nachrichten in einer Schleife, um komplexere Dialoge abzubilden.

5. **Executing the Conversation**

   .. code-block:: python

      run = client.beta.threads.runs.create_and_poll(
         thread_id=thread.id,
         assistant_id=assistant.id,
      )

   Mit ``create_and_poll`` starten Sie die Verarbeitung der Nutzeranfragen durch den Assistant. Wichtige Parameter:
   
   * ``thread_id=thread.id``: Legt den Thread für diese Ausführung fest.
   * ``assistant_id=assistant.id``: Bestimmt, welcher Assistant reagieren soll.

   Mögliche Statuswerte:

   * ``completed``: Die Verarbeitung war erfolgreich.
   * ``in_progress``: Verarbeitung läuft; etwas Geduld.
   * ``failed``: Bei der Verarbeitung ist ein Fehler aufgetreten.

   Für mehr Kontrolle können Sie ``create`` und ``poll`` getrennt verwenden, z. B. für asynchrones oder gestuftes Processing.

6. **Checking the Results**

   .. code-block:: python

      if run.status == "completed":
         messages = client.beta.threads.messages.list(thread_id=thread.id)

   Wenn die Ausführung abgeschlossen ist, holen Sie alle Nachrichten im Thread ab. Wichtige Felder jeder Nachricht:
   
   * ``role``: Rolle des Senders (``user``, ``assistant`` oder ``system``).
   * ``content``: Inhalt der Nachricht, meist als Textblock (``type="text"``).

   .. code-block:: python

      for message in messages:
         assert message.content[0].type == "text"
         print({"role": message.role, "message": message.content[0].text.value})

   Durchlaufen Sie alle Nachrichten und geben Sie Rolle und Textinhalt aus.

   .. code-block:: python

      client.beta.assistants.delete(assistant.id)

   Nach Abschluss der Unterhaltung löschen Sie den Assistant, um Ressourcen freizugeben. Das Löschen macht zugehörige Threads unbrauchbar; lassen Sie den Assistant aktiv, wenn er weiter genutzt wird, und sorgen Sie dann für ein sinnvolles Thread- und Ressourcenmanagement.



--------------------------------------------



**Troubleshooting Common Issues**

Bei der Arbeit mit der OpenAI-API und der Entwicklung von Chatbots auf einem Raspberry Pi können typische Probleme auftreten. Dieser Abschnitt hilft mit schnellen Lösungsansätzen, damit Ihre Anwendungen reibungslos laufen.


1. **API Key Errors**

``Problem``: Sie erhalten Fehlermeldungen zum API-Schlüssel wie „Invalid API Key“ oder „API Key not found“.

``Solution``: Prüfen Sie, ob der Schlüssel korrekt in der Datei ``keys.py`` oder als Umgebungsvariable eingetragen ist. Achten Sie auf Tippfehler oder Leerzeichen. Falls das Problem bleibt, erzeugen Sie auf der OpenAI-Plattform einen neuen Schlüssel und aktualisieren die Konfiguration.

2. **Network Issues**

``Problem``: Das Gerät kann OpenAI-Server nicht zuverlässig erreichen; Timeouts/Verbindungsfehler treten auf.

``Solution``: Überprüfen Sie die Internetverbindung des Raspberry Pi. Bei WLAN auf stabile Signalstärke achten; ggf. LAN verwenden. Prüfen Sie außerdem, ob Firewalls oder Netzrichtlinien den Zugriff auf OpenAI blockieren.

3. **Model Limitations**

``Problem``: Die Antworten entsprechen nicht den Erwartungen oder das Modell versteht komplexe Anfragen nicht.

``Solution``: Vergewissern Sie sich, dass Sie ein passendes Modell einsetzen (für komplexe Aufgaben z. B. GPT-4). Überarbeiten Sie zudem Anweisungen und Kontext des Assistants – präzise, knappe Vorgaben verbessern die Ergebnisse.

4. **Python Dependency Issues**

``Problem``: Fehler bei Installation oder Ausführung von Python-Abhängigkeiten.

``Solution``: Prüfen Sie die Kompatibilität aller Pakete mit Ihrer Python-Version. Nutzen Sie eine virtuelle Umgebung, um Konflikte zu vermeiden. Bei anhaltenden Problemen Abhängigkeiten (oder Python) neu installieren.
