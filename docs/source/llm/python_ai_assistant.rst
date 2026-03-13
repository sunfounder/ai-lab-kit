.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. AI-Sprachassistent
===========================

In dieser Lektion verwandeln Sie Ihr Fusion HAT+ in einen **sprachgesteuerten AI-Assistenten**.  
Mit dem bereitgestellten Code wird der Roboter: **auf ein Aktivierungswort warten**, Ihre Sprache mit Vosk **transkribieren**, sie an ein **OpenAI LLM** senden und anschließend mit **Piper TTS antworten**.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Voice_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----

Bevor Sie beginnen
---------------------------------

Stellen Sie sicher, dass Sie Folgendes vorbereitet haben:

* :ref:`test_piper` — Piper-Sprachausgabe funktioniert (z. B. können Sie „Hello“ abspielen).  
* :ref:`test_vosk` — Vosk-STT funktioniert für Ihre Sprache (z. B. ``en-us``).  
* :ref:`py_online_llm` — Ihr **OpenAI API-Schlüssel** ist in ``secret.py`` als ``OPENAI_API_KEY`` gespeichert.  
* Ein funktionierendes **Mikrofon** und **Lautsprecher** am Fusion HAT+.  
* Eine stabile Netzwerkverbindung (das LLM läuft online).

----

Beispiel ausführen
-------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**Vom Code verwendete Konfiguration:**

* LLM: **OpenAI** (``gpt-4o-mini``)  
* TTS: **Piper** (``en_US-ryan-low``)  
* STT: **Vosk** (``en-us``)  
* Aktivierungswort: ``"hey buddy"``  
* Tastatureingabe: **aktiviert** (optionale manuelle Eingabe)  
* Bildmodus: **aktiviert** (``WITH_IMAGE=True``) — erfordert ein multimodales LLM, falls Sie später Bilder verwenden möchten

**Ablauf:**

1. Der Assistent zeigt eine Begrüßungsnachricht mit dem Aktivierungswort an.  
2. Er lauscht auf **„hey buddy“**.  
3. Nach der Aktivierung wird Ihre Sprache transkribiert (Vosk → Text).  
4. Der Text wird an **OpenAI (gpt-4o-mini)** gesendet, um eine Antwort zu generieren.  
5. Die Antwort wird mit **Piper** (``en_US-ryan-low``) gesprochen.

**Beispielinteraktion**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What’s the capital of Italy?
   Robot: The capital of Italy is Rome.

Code
-----------------

.. code-block:: python

  from fusion_hat.voice_assistant import VoiceAssistant
  from fusion_hat.llm import OpenAI as LLM
  from secret import OPENAI_API_KEY as API_KEY

  llm = LLM(
      api_key=API_KEY,
      model="gpt-4o-mini",
  )

  # Robot name
  NAME = "Buddy"

  # Enable image, need to set up a multimodal language model
  WITH_IMAGE = True

  # Set models and languages
  LLM_MODEL = "gpt-4o-mini"
  TTS_MODEL = "en_US-ryan-low"
  STT_LANGUAGE = "en-us"

  # Enable keyboard input
  KEYBOARD_ENABLE = True

  # Enable wake word
  WAKE_ENABLE = True
  WAKE_WORD = [f"hey {NAME.lower()}"]
  # Set wake word answer, set empty to disable
  ANSWER_ON_WAKE = "Hi there"

  # Welcome message
  WELCOME = f"Hi, I'm {NAME}. Wake me up with: " + ", ".join(WAKE_WORD)

  # Set instructions
  INSTRUCTIONS = f"""
  You are a helpful assistant, named {NAME}.
  """

  va = VoiceAssistant(
      llm,
      name=NAME,
      with_image=WITH_IMAGE,
      tts_model=TTS_MODEL,
      stt_language=STT_LANGUAGE,
      keyboard_enable=KEYBOARD_ENABLE,
      wake_enable=WAKE_ENABLE,
      wake_word=WAKE_WORD,
      answer_on_wake=ANSWER_ON_WAKE,
      welcome=WELCOME,
      instructions=INSTRUCTIONS,
  )

  if __name__ == "__main__":
      va.run()

**Code-Erklärung:**

* ``OpenAI(..., model="gpt-4o-mini")`` — Verwendet **OpenAI** als einziges LLM in dieser Lektion.  
* ``NAME`` / ``WAKE_WORD`` — Personalisieren den Assistenten („Buddy“, „hey buddy“).  
* ``WITH_IMAGE=True`` — Aktiviert den Bildmodus im Assistenten (hier ohne Bild-Ein-/Ausgabe-Logik).  
* ``TTS_MODEL="en_US-ryan-low"`` — Piper-Stimme für die Sprachausgabe.  
* ``STT_LANGUAGE="en-us"`` — Vosk-Sprache für die Spracherkennung.  
* ``KEYBOARD_ENABLE=True`` — Ermöglicht optionale manuelle Texteingabe während des Debuggings.  
* ``WELCOME`` / ``INSTRUCTIONS`` — Startmeldung und Assistenten-Persona/System-Prompt.  
* ``va.run()`` — Startet die Hauptschleife: **Aktivieren → Zuhören → LLM → Sprechen**.


Zu anderen LLMs oder TTS wechseln
----------------------------------------------

Sie können problemlos zu anderen LLMs, TTS-Systemen oder STT-Sprachen wechseln, indem Sie nur wenige Änderungen vornehmen:

* Unterstützte LLMs:

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — Unterstützte Sprachen von **Piper TTS** prüfen.  
* :ref:`test_vosk` — Unterstützte Sprachen von **Vosk STT** prüfen.  

Zum Wechseln passen Sie einfach die Initialisierung im Code an:

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key="YOUR_KEY", model="gemini-pro")

   # Set models and languages
   TTS_MODEL = "en_US-ryan-low"
   STT_LANGUAGE = "en-us"



----

Fehlerbehebung
-----------------------------

* **Roboter reagiert nicht auf das Aktivierungswort**

  - Prüfen Sie, ob das Mikrofon funktioniert.  
  - Stellen Sie sicher, dass ``WAKE_ENABLE = True`` gesetzt ist.  
  - Passen Sie das Aktivierungswort an Ihre Aussprache an.  
  - Reduzieren Sie Hintergrundgeräusche und sprechen Sie deutlich.

* **Kein Ton aus dem Lautsprecher**

  - Prüfen Sie den Namen des TTS-Modells (z. B. ``en_US-ryan-low``).  
  - Testen Sie Piper oder Espeak manuell.  
  - Überprüfen Sie Lautsprecheranschluss und Lautstärke.

* **API-Schlüssel-Fehler oder Timeout**

  - Prüfen Sie Ihren Schlüssel in ``secret.py``.  
  - Stellen Sie sicher, dass Ihre Netzwerkverbindung stabil ist.  
  - Bestätigen Sie, dass das LLM-Modell unterstützt wird (z. B. ``gpt-4o-mini``).

* **Aktivierungswort funktioniert, aber keine Antwort**

  - Prüfen Sie, ob die STT-Sprache zu Ihrem Akzent passt.  
  - Stellen Sie sicher, dass das Modell korrekt heruntergeladen wurde.  
  - Aktivieren Sie Debug-Logs, um zu prüfen, ob STT korrekt läuft.

* **TTS funktioniert, aber keine LLM-Antwort**

  - Prüfen Sie, ob der API-Schlüssel gültig ist.  
  - Überprüfen Sie Modellname und LLM-Konfiguration.  
  - Stellen Sie sicher, dass eine Internetverbindung besteht.