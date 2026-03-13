.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. TTS mit Piper und OpenAI
========================================================

In der vorherigen Lektion haben wir **Espeak** und **Pico2Wave** kennengelernt – zwei einfache Offline-TTS-Engines auf dem Raspberry Pi.  
Nun gehen wir einen großen Schritt weiter und probieren zwei **fortgeschrittenere TTS-Optionen** aus, die **höhere Sprachqualität** und mehr Flexibilität bieten:

* **Piper** — eine schnelle, neuronale TTS-Engine, die **vollständig offline** auf dem Raspberry Pi läuft.  
* **OpenAI TTS** — ein Online-Dienst, der **sehr natürliche und menschenähnliche Stimmen** bereitstellt, ideal für ausdrucksstarke Sprachausgabe.

Mit diesen Engines klingt Ihr Fusion HAT+ deutlich realistischer und lebendiger.

----

.. _test_piper:

1. Piper testen
------------------

Piper ist eine **neuronale Offline-TTS-Engine**, das heißt, nach der Installation des Modells wird **keine Internetverbindung mehr benötigt**.  
Sie unterstützt mehrere **Sprachen** und **Stimmen**, was sie zu einer leistungsstarken Lösung für eingebettete Sprachsysteme macht.

**Programm ausführen**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* Beim ersten Start wird das ausgewählte **Sprachmodell** automatisch heruntergeladen.  
* Anschließend hören Sie den Fusion HAT+ sagen: ``Hello! I'm Piper TTS.``  
* Sie können Stimmen oder Sprachen wechseln, indem Sie ``set_model()`` mit einem anderen Modellnamen aufrufen.

**Code**

.. code-block:: python

  from fusion_hat.tts import Piper

  tts = Piper()

  # Unterstützte Sprachen auflisten
  print(tts.available_countrys())

  # Modelle für Englisch (en_us) anzeigen
  print(tts.available_models('en_us'))

  # Ein Sprachmodell auswählen (wird automatisch heruntergeladen, falls noch nicht vorhanden)
  tts.set_model("en_US-amy-low")

  # Text sprechen
  tts.say("Hello! I'm Piper TTS.")

**Code-Erklärung:**

* ``available_countrys()`` — Listet alle unterstützten Sprachen auf.  
* ``available_models()`` — Listet verfügbare Modelle für eine bestimmte Sprache auf.  
* ``set_model()`` — Legt das Sprachmodell fest. Falls es noch nicht installiert ist, wird es automatisch heruntergeladen.  
* ``say()`` — Wandelt Text in Sprache um und gibt ihn sofort wieder.

💡 **Tipp:** Probieren Sie verschiedene Modelle aus, um Geschwindigkeit, Klarheit und Akzente zu vergleichen. Einige Modelle sind leichter (schneller), während andere eine höhere Klangqualität bieten.

----

2. OpenAI TTS testen
-------------------------------

**API-Schlüssel erstellen und speichern**

#. Gehen Sie zu |link_openai_platform| und melden Sie sich an. Klicken Sie auf der Seite **API keys** auf **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Füllen Sie die Details aus (Owner, Name, Project und gegebenenfalls Berechtigungen) und klicken Sie dann auf **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Sobald der Schlüssel erstellt wurde, kopieren Sie ihn sofort — danach kann er nicht mehr angezeigt werden. Wenn Sie ihn verlieren, müssen Sie einen neuen Schlüssel generieren.

   .. image:: img/llm_openai_copy.png

#. Erstellen Sie in Ihrem Projektordner (z. B. ``/``) eine Datei namens ``secret.py``:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel in die Datei ein:

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Programm ausführen**

.. code-block:: bash
  
  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* Das Programm verbindet sich mit dem OpenAI-TTS-Dienst, und der Fusion HAT+ spricht mit **natürlicher, ausdrucksstarker Stimme**.  
* Sie können **Stimmstile ändern** und **Anweisungen hinzufügen**, um Ton und Ausdruck zu steuern (z. B. traurig, dramatisch, verspielt).  
* Dadurch eignet sich OpenAI TTS ideal für interaktive Roboter, Storytelling oder Lernassistenten.

**Code**

.. code-block:: python

  from fusion_hat.tts import OpenAI_TTS
  from secret import OPENAI_API_KEY

  # Export your OpenAI_API_KEY before running the script
  # export OPENAI_API_KEY="sk-proj-xxxxxx"

  tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
  # tts.set_model('tts-1')
  tts.set_voice('alloy')
  tts.set_model('gpt-4o-mini-tts')

  msg = "Hello! I'm OpenAI TTS."
  print(f"Say: {msg}")
  tts.say(msg)

  msg = "with instructions, I can say word sadly"
  instructions = "say it sadly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)

  msg = "or say something dramaticly."
  instructions = "say it dramaticly"
  print(f"Say: {msg}, with instructions: '{instructions}'")
  tts.say(msg, instructions=instructions)


**Code explanation:**

* ``OpenAI_TTS()`` — Initialisiert die OpenAI-TTS-Engine mit Ihrem API-Schlüssel.  
* ``set_model()`` — Wählt das TTS-Modell aus (z. B. ``gpt-4o-mini-tts``).  
* ``set_voice()`` — Wählt eine bestimmte Stimme aus (z. B. ``alloy``).  
* ``say(text)`` — Wandelt den Text in Sprache um und spielt ihn ab.  
* ``say(text, instructions=...)`` — Fügt **Anweisungen für den Ausdruckston** hinzu, sodass Sie den Sprachstil dynamisch steuern können.

**Beispiel:** 

- „say it sadly“ → weicher, emotionaler Ton  
- „say it dramatically“ → kraftvolle, ausdrucksstarke Betonung  
- „say it excitedly“ → enthusiastischer Ton

----

Troubleshooting
-------------------

* **No module named 'secret'**

  Das bedeutet, dass sich ``secret.py`` nicht im selben Ordner wie Ihre Python-Datei befindet.  
  Verschieben Sie ``secret.py`` in das gleiche Verzeichnis, in dem Sie das Skript ausführen, z. B.:

  .. code-block:: bash

     ls ~/
     # Stellen Sie sicher, dass sowohl secret.py als auch Ihre .py-Datei vorhanden sind

* **OpenAI: Invalid API key / 401**

  * Prüfen Sie, ob Sie den vollständigen Schlüssel eingefügt haben (beginnt mit ``sk-``) und keine zusätzlichen Leerzeichen oder Zeilenumbrüche vorhanden sind.
  * Stellen Sie sicher, dass Ihr Code den Schlüssel korrekt importiert:

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * Prüfen Sie die Netzwerkverbindung Ihres Raspberry Pi (z. B. ``ping api.openai.com``).  

* **OpenAI: Quota exceeded / billing error**

  * Möglicherweise müssen Sie im OpenAI-Dashboard **Abrechnung hinzufügen** oder Ihr **Kontingent erhöhen**.
  * Versuchen Sie es erneut, nachdem das Problem mit Konto oder Abrechnung behoben wurde.

* **Piper: tts.say() läuft, aber kein Ton**

  * Stellen Sie sicher, dass tatsächlich ein Sprachmodell vorhanden ist:

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * Prüfen Sie, ob der Modellname im Code exakt übereinstimmt:

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * Prüfen Sie das Audio-Ausgabegerät und die Lautstärke auf Ihrem Pi (``alsamixer``), und stellen Sie sicher, dass Lautsprecher angeschlossen und eingeschaltet sind.

* **ALSA- / Audiogeräte-Fehler (z. B. „Audio device busy“ oder „No such file or directory“)**

  * Schließen Sie andere Programme, die Audio verwenden.
  * Starten Sie den Raspberry Pi neu, wenn das Gerät weiterhin blockiert ist.
  * Wählen Sie bei HDMI- oder Kopfhörerausgabe das richtige Gerät in den Audioeinstellungen von Raspberry Pi OS.

* **Permission denied beim Ausführen von Python**

  * Versuchen Sie es mit ``sudo``, falls Ihre Umgebung dies erfordert:

    .. code-block:: bash

       sudo python3 tts_piper.py

Comparison of TTS Engines
-------------------------

.. list-table:: Feature comparison: Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - Item
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - Runs on
     - In Raspberry Pi integriert (offline)
     - In Raspberry Pi integriert (offline)
     - Raspberry Pi / PC (offline, benötigt Modell)
     - Cloud (online, benötigt API-Schlüssel)
   * - Voice quality
     - Robotisch
     - Natürlicher als Espeak
     - Natürlich (neuronales TTS)
     - Sehr natürlich / menschenähnlich
   * - Controls
     - Geschwindigkeit, Tonhöhe, Lautstärke
     - Begrenzte Einstellungen
     - Auswahl verschiedener Stimmen/Modelle
     - Auswahl von Modell und Stimme
   * - Languages
     - Viele (Qualität variiert)
     - Begrenzte Auswahl
     - Viele Stimmen und Sprachen verfügbar
     - Am besten in Englisch (andere je nach Verfügbarkeit)
   * - Latency / speed
     - Sehr schnell
     - Schnell
     - Echtzeit auf Pi 4/5 mit „low“-Modellen
     - Netzwerkabhängig (meist geringe Latenz)
   * - Setup
     - Minimal
     - Minimal
     - ``.onnx`` + ``.onnx.json`` Modelle herunterladen
     - API-Schlüssel erstellen, Client installieren
   * - Best for
     - Schnelle Tests, einfache Sprachmeldungen
     - Etwas bessere Offline-Stimme
     - Lokale Projekte mit höherer Qualität
     - Höchste Qualität, umfangreiche Stimmoptionen