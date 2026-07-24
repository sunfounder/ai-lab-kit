.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. TTS con Piper e OpenAI
========================================================

Nella lezione precedente, abbiamo esplorato **Espeak** e **Pico2Wave**, due semplici motori TTS offline su Raspberry Pi.
Ora, facciamo un grande passo avanti e proviamo due **opzioni TTS piu' avanzate** che offrono **maggiore qualita' vocale** e piu' flessibilita':

* **Piper** -- un motore TTS veloce basato su reti neurali che funziona **completamente offline** su Raspberry Pi.
* **OpenAI TTS** -- un servizio online che fornisce **voci molto naturali e simili a quelle umane**, perfetto per un parlato espressivo.

Questi motori faranno sembrare il tuo Fusion HAT+ piu' realistico e vivido.

----

.. _test_piper:

1. Test di Piper
------------------

Piper e' un **motore TTS neurale offline**, il che significa che non hai bisogno di una connessione Internet una volta installato il modello.
Supporta molteplici **lingue** e **voci**, rendendolo un'opzione potente per il parlato embedded.

**Esegui il programma**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* La prima volta che lo esegui, il **modello vocale** selezionato verra' scaricato automaticamente.
* Dovresti quindi sentire il Fusion HAT+ dire: ``Hello! I'm Piper TTS.``
* Puoi cambiare voci o lingue chiamando ``set_model()`` con un nome di modello diverso.

**Codice**

.. code-block:: python

  from fusion_hat.tts import Piper

  tts = Piper()

  # List supported languages
  print(tts.available_countrys())

  # List models for English (en_us)
  print(tts.available_models('en_us'))

  # Set a voice model (auto-download if not already present)
  tts.set_model("en_US-amy-low")

  # Say something
  tts.say("Hello! I'm Piper TTS.")

**Spiegazione del codice:**

* ``available_countrys()`` -- Elenca tutte le lingue supportate.
* ``available_models()`` -- Elenca i modelli disponibili per una lingua specifica.
* ``set_model()`` -- Imposta il modello vocale. Se il modello non e' installato, verra' scaricato automaticamente.
* ``say()`` -- Converte il testo in parlato e lo riproduce immediatamente.

Suggerimento: Prova diversi modelli per confrontare velocita', chiarezza e accenti. Alcuni modelli sono piu' leggeri (piu' veloci), mentre altri hanno una fedelta' maggiore.

----

2. Test di OpenAI TTS
-------------------------------

**Ottieni e salva la tua chiave API**

#. Vai su |link_openai_platform| e accedi. Nella pagina **API keys**, clicca su **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Compila i dettagli (Owner, Name, Project e permessi se necessario), poi clicca su **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Una volta creata la chiave, copiala immediatamente -- non potrai piu' vederla. Se la perdi, dovrai generar una nuova.

   .. image:: img/llm_openai_copy.png

#. Nella cartella del tuo progetto (ad esempio: ``/``), crea un file chiamato ``secret.py``:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Incolla la tua chiave nel file in questo modo:

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Esegui il programma**

.. code-block:: bash

  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* Il programma si connettera' al servizio TTS di OpenAI e Fusion HAT+ parlera' usando un **output vocale naturale ed espressivo**.
* Puoi cambiare **stili vocali** e aggiungere **istruzioni** per controllare tono ed espressione (ad esempio, triste, drammatico, giocoso).
* Questo rende OpenAI TTS ideale per robot interattivi, narrazione di storie o assistenti educativi.


**Codice**

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


**Spiegazione del codice:**

* ``OpenAI_TTS()`` -- Inizializza il motore TTS di OpenAI usando la tua chiave API.
* ``set_model()`` -- Seleziona il modello TTS (ad esempio, ``gpt-4o-mini-tts``).
* ``set_voice()`` -- Sceglie una voce specifica (ad esempio, ``alloy``).
* ``say(text)`` -- Converte il testo in parlato e lo riproduce.
* ``say(text, instructions=...)`` -- Aggiunge **istruzioni espressive sul tono**, permettendoti di controllare dinamicamente lo stile del parlato.

**Esempio:**

- "say it sadly" -> tono morbido ed emotivo
- "say it dramatically" -> consegna audace ed espressiva
- "say it excitedly" -> tono entusiasta

----

Risoluzione dei Problemi
-------------------------

* **Nessun modulo di nome 'secret'**

  Questo significa che ``secret.py`` non si trova nella stessa cartella del tuo file Python.
  Sposta ``secret.py`` nella stessa directory in cui esegui lo script, ad esempio:

  .. code-block:: bash

     ls ~/
     # Assicurati di vedere entrambi: secret.py e il tuo file .py

* **OpenAI: Chiave API non valida / 401**

  * Controlla di aver incollato la chiave completa (inizia con ``sk-``) e che non ci siano spazi/ritorni a capo extra.
  * Assicurati che il tuo codice la importi correttamente:

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * Conferma l'accesso alla rete sul tuo Pi (prova ``ping api.openai.com``).

* **OpenAI: Quota superata / errore di fatturazione**

  * Potresti dover aggiungere fatturazione o aumentare la quota nel pannello di controllo OpenAI.
  * Riprova dopo aver risolto il problema dell'account/fatturazione.

* **Piper: tts.say() viene eseguito ma nessun suono**

  * Assicurati che un modello vocale sia effettivamente presente:

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * Conferma che il nome del modello corrisponda esattamente nel codice:

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * Controlla il dispositivo/volume di uscita audio sul tuo Pi (``alsamixer``) e che gli altoparlanti siano collegati e accesi.

* **Errori ALSA / dispositivo audio (ad esempio, "Audio device busy" o "No such file or directory")**

  * Chiudi altri programmi che usano l'audio.
  * Riavvia il Pi se il dispositivo rimane occupato.
  * Per l'uscita HDMI vs. jack per cuffie, seleziona il dispositivo corretto nelle impostazioni audio di Raspberry Pi OS.

* **Permesso negato durante l'esecuzione di Python**

  * Prova con ``sudo`` se il tuo ambiente lo richiede:

    .. code-block:: bash

       sudo python3 tts_piper.py

Confronto dei Motori TTS
-------------------------

.. list-table:: Confronto delle caratteristiche: Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - Elemento
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - Esecuzione su
     - Integrato su Raspberry Pi (offline)
     - Integrato su Raspberry Pi (offline)
     - Raspberry Pi / PC (offline, necessita modello)
     - Cloud (online, necessita chiave API)
   * - Qualita' voce
     - Robotica
     - Piu' naturale di Espeak
     - Naturale (TTS neurale)
     - Molto naturale / simile a umana
   * - Controlli
     - Velocita', tonalita', volume
     - Controlli limitati
     - Scegli diverse voci/modelli
     - Scegli modello e voci
   * - Lingue
     - Molte (qualita' varia)
     - Set limitato
     - Molte voci/lingue disponibili
     - Migliore in inglese (altre variano per disponibilita')
   * - Latenza/velocita'
     - Molto veloce
     - Veloce
     - Tempo reale su Pi 4/5 con modelli "low"
     - Dipendente dalla rete (di solito bassa latenza)
   * - Configurazione
     - Minima
     - Minima
     - Scarica modelli ``.onnx`` + ``.onnx.json``
     - Crea chiave API, installa client
   * - Ideale per
     - Test rapidi, prompt di base
     - Voce offline leggermente migliore
     - Progetti locali con qualita' migliore
     - Massima qualita', ricche opzioni vocali
