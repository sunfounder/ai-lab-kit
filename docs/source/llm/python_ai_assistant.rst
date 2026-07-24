.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. Assistente Vocale AI
===========================

Questa lezione trasforma il tuo Fusion HAT+ in un **assistente AI vocale**.
Con il codice fornito, il robot: **attende una parola di attivazione**, **trascrive il tuo parlato** con Vosk, lo invia a un **LLM OpenAI** e **risponde vocalmente** utilizzando Piper TTS.

.. raw:: html

      <video width=”500” loop muted controls>
          <source src=”../_static/video/Ai_Voice_Assistant.mp4” type=”video/mp4”>
          Your browser does not support the video tag.
      </video>

----

Prima di Iniziare
----------------

Assicurati di avere:

* :ref:`test_piper` — La voce Piper funziona (ad esempio, puoi riprodurre “Hello”).
* :ref:`test_vosk` — Vosk STT funziona per la tua lingua (ad esempio, ``en-us``).
* :ref:`py_online_llm` — La tua **chiave API OpenAI** salvata in ``secret.py`` come ``OPENAI_API_KEY``.
* Un **microfono** e un **altoparlante** funzionanti su Fusion HAT+.
* Una connessione di rete stabile (l’LLM è online).

----

Esegui l’Esempio
---------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**Configurazione utilizzata dal codice:**

* LLM: **OpenAI** (``gpt-4o-mini``)
* TTS: **Piper** (``en_US-ryan-low``)
* STT: **Vosk** (``en-us``)
* Parola di attivazione: ``”hey buddy”``
* Input da tastiera: **abilitato** (input manuale opzionale)
* Modalità immagine: **abilitata** (``WITH_IMAGE=True``) — richiede un LLM multimodale se decidi di usare immagini in seguito

**Cosa succede:**

1. L’assistente mostra un messaggio di benvenuto con la frase di attivazione.
2. Ascolta la parola **”hey buddy”**.
3. Dopo l’attivazione, il tuo parlato viene trascritto (Vosk → testo).
4. Il testo viene inviato a **OpenAI (gpt-4o-mini)** per una risposta.
5. La risposta viene pronunciata con **Piper** (``en_US-ryan-low``).

**Esempio di interazione**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What’s the capital of Italy?
   Robot: The capital of Italy is Rome.

Codice
-----------------

.. code-block:: python

  from fusion_hat.voice_assistant import VoiceAssistant
  from fusion_hat.llm import OpenAI as LLM
  from secret import OPENAI_API_KEY as API_KEY

  llm = LLM(
      api_key=API_KEY,
      model=”gpt-4o-mini”,
  )

  # Robot name
  NAME = “Buddy”

  # Enable image, need to set up a multimodal language model
  WITH_IMAGE = True

  # Set models and languages
  LLM_MODEL = “gpt-4o-mini”
  TTS_MODEL = “en_US-ryan-low”
  STT_LANGUAGE = “en-us”

  # Enable keyboard input
  KEYBOARD_ENABLE = True

  # Enable wake word
  WAKE_ENABLE = True
  WAKE_WORD = [f”hey {NAME.lower()}”]
  # Set wake word answer, set empty to disable
  ANSWER_ON_WAKE = “Hi there”

  # Welcome message
  WELCOME = f”Hi, I’m {NAME}. Wake me up with: “ + “, “.join(WAKE_WORD)

  # Set instructions
  INSTRUCTIONS = f”””
  You are a helpful assistant, named {NAME}.
  “””

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

  if __name__ == “__main__”:
      va.run()

**Spiegazione del codice:**

* ``OpenAI(..., model=”gpt-4o-mini”)`` — Utilizza **OpenAI** come unico LLM in questa lezione.
* ``NAME`` / ``WAKE_WORD`` — Personalizza l’assistente (“Buddy”, “hey buddy”).
* ``WITH_IMAGE=True`` — Abilita la modalità immagine nell’assistente (nessuna logica I/O immagine inclusa qui).
* ``TTS_MODEL=”en_US-ryan-low”`` — Voce Piper utilizzata per le risposte.
* ``STT_LANGUAGE=”en-us”`` — Lingua Vosk per il riconoscimento.
* ``KEYBOARD_ENABLE=True`` — Permette l’input manuale opzionale durante il debug.
* ``WELCOME`` / ``INSTRUCTIONS`` — Messaggio di avvio e prompt di sistema per l’assistente.
* ``va.run()`` — Avvia il ciclo: **attivazione → ascolto → LLM → risposta vocale**.


Passare ad Altri LLM o TTS
------------------------------

Puoi passare facilmente ad altri LLM, TTS o lingue STT con poche modifiche:

* LLM supportati:

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — Controlla le lingue supportate da **Piper TTS**.
* :ref:`test_vosk` — Controlla le lingue supportate da **Vosk STT**.

Per cambiare, modifica semplicemente la parte di inizializzazione nel codice:

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key=”YOUR_KEY”, model=”gemini-pro”)

   # Set models and languages
   TTS_MODEL = “en_US-ryan-low”
   STT_LANGUAGE = “en-us”



----

Risoluzione dei Problemi
-----------------------------

* **Il robot non risponde alla parola di attivazione**

  - Verifica che il microfono funzioni.
  - Assicurati che ``WAKE_ENABLE = True``.
  - Regola la parola di attivazione in base alla tua pronuncia.
  - Riduci il rumore di fondo e parla chiaramente.

* **Nessun suono dall’altoparlante**

  - Controlla il nome del modello TTS (ad esempio, ``en_US-ryan-low``).
  - Prova Piper o Espeak manualmente.
  - Verifica la connessione dell’altoparlante e il volume.

* **Errore della chiave API o timeout**

  - Controlla la tua chiave in ``secret.py``.
  - Assicurati che la connessione di rete sia stabile.
  - Conferma che il modello LLM sia supportato (ad esempio, ``gpt-4o-mini``).

* **La parola di attivazione funziona ma nessuna risposta**

  - Verifica che la lingua STT corrisponda al tuo accento.
  - Assicurati che il modello sia stato scaricato correttamente.
  - Prova a stampare i log di debug per confermare che STT sia in esecuzione.

* **TTS funziona ma nessuna risposta LLM**

  - Verifica che la chiave API sia valida.
  - Controlla il nome del modello e le impostazioni LLM.
  - Assicurati di avere connettività Internet. 



