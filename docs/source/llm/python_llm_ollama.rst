.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Dialogo Visivo e Testuale con Ollama
=============================================

In questa lezione imparerai come usare **Ollama**, uno strumento per eseguire modelli linguistici e di visione localmente.
Mostreremo come installare Ollama, scaricare un modello e connettere Fusion HAT+ ad esso.

Con questa configurazione, Fusion HAT+ puo' scattare una foto con la fotocamera e il modello **vede e racconta** —
puoi fare qualsiasi domanda sull'immagine e il modello rispondera' in linguaggio naturale.

.. _download_ollama:

1. Install Ollama (LLM) and Download Model
-------------------------------------------------

You can choose where to install **Ollama**:

* On your Raspberry Pi (local run)
* Or on another computer (Mac/Windows/Linux) in the **same local network**

**Recommended models vs hardware**

You can choose any model available on |link_ollama_hub|.
Models come in different sizes (3B, 7B, 13B, 70B...).
Smaller models run faster and require less memory, while larger models provide better quality but need powerful hardware.

Check the table below to decide which model size fits your device.

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - Model size
     - Min RAM Required
     - Recommended Hardware
   * - ~3B parameters
     - 8GB (16GB better)
     - Raspberry Pi 5 (16GB) or mid-range PC/Mac
   * - ~7B parameters
     - 16GB+
     - Pi 5 (16GB, just usable) or mid-range PC/Mac
   * - ~13B parameters
     - 32GB+
     - Desktop PC / Mac with high RAM
   * - 30B+ parameters
     - 64GB+
     - Workstation / Server / GPU recommended
   * - 70B+ parameters
     - 128GB+
     - High-end server with multiple GPUs

**Install on Raspberry Pi**

If you want to run Ollama directly on your Raspberry Pi:

* Use a **64-bit Raspberry Pi OS**
* Strongly recommended: **Raspberry Pi 5 (16GB RAM)**

Run the following commands:

.. code-block:: bash

   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull a lightweight model (good for testing)
   ollama pull llama3.2:3b

   # Quick run test (type 'hi' and press Enter)
   ollama run llama3.2:3b

   # Serve the API (default port 11434)
   # Tip: set OLLAMA_HOST=0.0.0.0 to allow access from LAN
   OLLAMA_HOST=0.0.0.0 ollama serve

**Install on Mac / Windows / Linux (Desktop App)**

1. Download and install Ollama from |link_ollama|

   .. image:: img/llm_ollama_download.png

2. Open the Ollama app, go to the **Model Selector**, and use the search bar to find a model. For example, type ``llama3.2:3b`` (a small and lightweight model to start with).

   .. image:: img/llm_ollama_choose.png

3. After the download is complete, type something simple like “Hi” in the chat window, Ollama will automatically start downloading it when you first use it.

   .. image:: img/llm_olama_llama_download.png

4. Go to **Settings** → enable **Expose Ollama to the network**. This allows your Raspberry Pi to connect to it over LAN.

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   If you see an error like:

   ``Error: model requires more system memory ...``

   The model is too large for your machine.
   Use a **smaller model** or switch to a computer with more RAM.

2. Test Ollama
--------------

Once Ollama is installed and your model is ready, you can quickly test it with a minimal chat loop.

**Set IP Address**

#. Open the example script:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. Update the parameters as needed:

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``: Update both ``ip`` and ``model`` to your own setup.

     * ``ip``: If Ollama runs on the **same Pi**, use ``localhost``. If Ollama runs on another computer in your LAN, enable **Expose to network** in Ollama and set ``ip`` to that computer's LAN IP.
     * ``model``: Must exactly match the model name you downloaded/activated in Ollama.


**Run the program**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 llm_ollama.py

Now you can chat with Fusion HAT+ directly from the terminal.

   * You can choose **any model** available on |link_ollama_hub|, but smaller models (e.g. ``moondream:1.8b``, ``phi3:mini``) are recommended if you only have 8–16GB RAM.
   * Make sure the model you specify in the code matches the model you have already pulled in Ollama.
   * Type ``exit`` or ``quit`` to stop the program.
   * If you cannot connect, ensure that Ollama is running and that both devices are on the same LAN if you are using a remote host.

**Code**

.. code-block:: python

   from fusion_hat.llm import Ollama
 
   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   # Change this to your computer IP, if you run it on your pi, then change it to localhost
   llm = Ollama(
      ip="localhost",
      model="llama3.2:3b"
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Response without stream
      # response = llm.prompt(input_text)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


3. Dialogo Visivo con Ollama
--------------------------

In questa demo, la fotocamera del Pi scatta una foto **ogni volta che digiti una domanda**.
Il programma invia **il testo digitato + la nuova foto** a un modello di visione locale tramite Ollama,
e poi trasmette in streaming la risposta del modello in chiaro italiano (o altra lingua).
Questa e’ una base minima “vedi e racconta” che puoi successivamente estendere con controlli di colore/volto/QR.

**Prima di Iniziare**

#. Apri l’app **Ollama** (o avvia il servizio) e assicurati di aver scaricato un **modello con capacita’ visive**.

   * Se hai abbastanza memoria (>=16GB RAM), puoi provare ``llava:7b``.
   * Se hai solo **8GB RAM**, preferisci un modello piu’ piccolo come ``moondream:1.8b`` o ``granite3.2-vision:2b``.

   .. image:: img/llm_ollama_image_model.png

**Esegui la Demo**

#. Vai alla cartella degli esempi ed esegui lo script:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. Cosa succede quando viene eseguito:

   * Il programma stampa una riga di benvenuto e attende il tuo input (``>>>``).
   * **Ogni volta che digiti qualcosa** (ad esempio, “hello”, “Is there yellow?”, “Any faces?”, “What is on the desk?”), esso:

     * **acquisisce una foto** dalla fotocamera del Pi (salvata in ``/tmp/llm-img.jpg``),
     * **invia il tuo testo + la foto** al modello di visione tramite Ollama,
     * **ritrasmette in streaming** la risposta del modello al terminale.

   * Digita ``exit`` o ``quit`` per terminare il programma.

**Code**

.. code-block:: python

   from fusion_hat.llm import Ollama
   from picamera2 import Picamera2
   import time

   '''
   You need to setup ollama first, see llm_local.py

   You need at leaset 8GB RAM to run llava:7b large multimodal model
   '''

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   llm = Ollama(
      ip="localhost",          # e.g., "192.168.100.145" if remote
      model="llava:7b"         # change to "moondream:1.8b" or "granite3.2-vision:2b" for 8GB RAM
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   # Init camera
   camera = Picamera2()
   config = camera.create_still_configuration(
      main={"size": (1280, 720)},
   )
   camera.configure(config)
   camera.start()
   time.sleep(2)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Capture image
      img_path = '/tmp/llm-img.jpg'
      camera.capture_file(img_path)

      # Response without stream
      # response = llm.prompt(input_text, image_path=img_path)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True, image_path=img_path)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


Risoluzione dei Problemi
---------------


* **Ricevo un errore come: `model requires more system memory ...`.**

  * Questo significa che il modello e' troppo grande per il tuo dispositivo.
  * Usa un modello piu' piccolo come ``moondream:1.8b`` o ``granite3.2-vision:2b``.
  * Oppure passa a una macchina con piu' RAM ed esponi Ollama alla rete.

* **Il codice non riesce a connettersi a Ollama (connessione rifiutata).**

  Controlla quanto segue:

  * Assicurati che Ollama sia in esecuzione (``ollama serve`` o l'app desktop aperta).
  * Se usi un computer remoto, abilita **Expose to network** nelle impostazioni di Ollama.
  * Verifica che ``ip="..."`` nel tuo codice corrisponda al corretto IP LAN.
  * Conferma che entrambi i dispositivi siano sulla stessa rete locale.

* **La mia fotocamera Pi non acquisisce nulla.**

  * Verifica che ``Picamera2`` sia installato e funzioni con un semplice script di test.
  * Controlla che il cavo della fotocamera sia collegato correttamente e abilitato in ``raspi-config``.
  * Assicurati che il tuo script abbia i permessi per scrivere nel percorso di destinazione (``/tmp/llm-img.jpg``).

* **L'output e' troppo lento.**

  * I modelli piu' piccoli rispondono piu' velocemente, ma con risposte piu' semplici.
  * Puoi ridurre la risoluzione della fotocamera (ad esempio, 640x480 invece di 1280x720) per accelerare l'elaborazione delle immagini.
  * Chiudi altri programmi sul Pi per liberare CPU e RAM.
  