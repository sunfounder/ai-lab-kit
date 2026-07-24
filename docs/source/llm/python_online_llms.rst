.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. Connessione a LLM Online
================================

In questa lezione, impareremo come connettere il tuo Fusion HAT+ (o Raspberry Pi) a diversi **modelli linguistici di grandi dimensioni (LLM) online**.
Ogni fornitore richiede una chiave API e offre diversi modelli tra cui puoi scegliere.

Vedremo come:

* Creare e salvare le tue chiavi API in modo sicuro.
* Scegliere un modello che si adatti alle tue esigenze.
* Eseguire il nostro codice di esempio per chattare con i modelli.

Procediamo passo dopo passo per ogni fornitore.

----

OpenAI
----------

OpenAI fornisce modelli potenti come **GPT-4o** e **GPT-4.1** che possono essere utilizzati sia per attività testuali che visive.

Ecco come configurarlo:

.. start_setup_openai

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

**Abilita la fatturazione e controlla i modelli**

#. Prima di usare la chiave, vai alla pagina **Billing** nel tuo account OpenAI, aggiungi i dettagli di pagamento e ricarica una piccola quantita' di crediti.

   .. image:: img/llm_openai_billing.png

#. Poi vai alla pagina **Limits** per verificare quali modelli sono disponibili per il tuo account e copia l'ID esatto del modello da usare nel tuo codice.

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**Test con codice di esempio**

#. Apri il nostro codice di esempio:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model="xxx"`` con il modello desiderato (ad esempio, ``gpt-4o``):

   .. code-block:: python

      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )

   Salva ed esci (``Ctrl+X``, poi ``Y``, poi ``Enter``).

#. Infine, esegui il test:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

----

Gemini
------------------

Gemini e’ la famiglia di modelli AI di Google. E’ veloce e ottimo per attività di uso generale.

**Ottieni e salva la tua chiave API**

#. Accedi a |link_google_ai|, poi vai alla pagina API Keys.

   .. image:: img/llm_gemini_get.png

#. Clicca sul pulsante **Create API key** nell’angolo in alto a destra.

   .. image:: img/llm_gemini_create.png

#. Puoi creare una chiave per un progetto esistente o uno nuovo.

   .. image:: img/llm_gemini_choose.png

#. Copia la chiave API generata.

   .. image:: img/llm_gemini_copy.png

#. Nella cartella del tuo progetto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Incolla la chiave:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**Controlla i modelli disponibili**

Vai alla pagina ufficiale |link_gemini_model|, qui vedrai l’elenco dei modelli, i loro ID API esatti e per quale caso d’uso ciascuno e’ ottimizzato.

   .. image:: img/llm_gemini_model.png

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model="xxx"`` con il modello desiderato (ad esempio, ``gemini-2.5-flash``):

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. Salva ed esegui:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

----

Qwen
------------------

Qwen e' una famiglia di modelli linguistici e multimodali di grandi dimensioni fornita da Alibaba Cloud.
Questi modelli supportano la generazione di testo, il ragionamento e la comprensione multimodale (come l'analisi delle immagini).

**Ottieni una chiave API**

Per chiamare i modelli Qwen, hai bisogno di una **chiave API**.
La maggior parte degli utenti internazionali dovrebbe usare la console **DashScope International (Model Studio)**.
Gli utenti della Cina continentale possono invece usare la console **Bailian (百炼)**.

* **Per utenti internazionali**

  #. Vai alla pagina ufficiale |link_qwen_inter| su **Alibaba Cloud**.
  #. Accedi o crea un account **Alibaba Cloud**.
  #. Naviga a **Model Studio** (scegli la regione Singapore o Pechino).

      * Se appare un prompt “Activate Now” nella parte superiore della pagina, cliccarlo per attivare Model Studio e ricevere la quota gratuita (solo Singapore).
      * L'attivazione e' gratuita -- ti verra' addebitato solo dopo aver utilizzato la quota gratuita.
      * Se non appare alcun prompt di attivazione, il servizio e' gia' attivo.

  #. Vai alla pagina **Key Management**. Nella scheda **API Key**, clicca su **Create API Key**.
  #. Dopo la creazione, copia la tua chiave API e conservala al sicuro.

    .. image:: img/llm_qwen_api_key.png
        :width: 800

  .. note::
     Gli utenti di Hong Kong, Macao e Taiwan dovrebbero anche scegliere l'opzione **International (Model Studio)**.

* **Per utenti della Cina continentale**

  Se sei nella Cina continentale, puoi invece usare la console **Alibaba Cloud Bailian (百炼)**:

  #. Accedi a |link_aliyun| (console Bailian) e completa la verifica dell'account.
  #. Seleziona **Create API Key**. Se viene richiesto che i servizi del modello non sono attivati, clicca su **Activate**, accetta i termini e richiedi la tua quota gratuita. Dopo l'attivazione, il pulsante **Create API Key** sara' abilitato.

     .. image:: img/llm_qwen_aliyun_create.png

  #. Clicca di nuovo su **Create API Key**, controlla il tuo account, poi clicca su **Confirm**.

     .. image:: img/llm_qwen_aliyun_confirm.png

  #. Una volta creata, copia la tua chiave API.

     .. image:: img/llm_qwen_aliyun_copy.png

**Salva la tua chiave API**

#. Nella cartella del tuo progetto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Incolla la tua chiave in questo modo:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        QWEN_API_KEY = “sk-xxx”

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model=”xxx”`` con il modello desiderato (ad esempio, ``qwen-plus``):

   .. code-block:: python

      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = “You are a helpful assistant.”
      WELCOME = “Hello, I am a helpful assistant. How can I help you?”

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model=”qwen-plus”,
      )

#. Esegui con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

Grok (xAI)
------------------
Grok e’ l’AI conversazionale di xAI, creata dal team di Elon Musk. Puoi connetterti tramite l’API xAI.

**Ottieni e salva la tua chiave API**

#. Registrati per un account qui: |link_grok_ai|. Aggiungi prima alcuni crediti al tuo account -- altrimenti l’API non funzionera’.

#. Vai alla pagina API Keys, clicca su **Create API key**.

   .. image:: img/llm_grok_create.png

#. Inserisci un nome per la chiave, poi clicca su **Create API key**.

   .. image:: img/llm_grok_name.png

#. Copia la chiave generata e conservala al sicuro.

   .. image:: img/llm_grok_copy.png

#. Nella cartella del tuo progetto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Incolla la tua chiave in questo modo:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        GROK_API_KEY = "xai-xxx"

**Controlla i modelli disponibili**

Vai alla pagina Models nella console xAI. Qui puoi vedere tutti i modelli disponibili per il tuo team, insieme ai loro ID API esatti -- usa questi ID nel tuo codice.

   .. image:: img/llm_grok_model.png

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model="xxx"`` con il modello desiderato (ad esempio, ``grok-4-latest``):

   .. code-block:: python

      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. Esegui con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

----

DeepSeek
------------------

DeepSeek e' un fornitore LLM cinese che offre modelli convenienti e capaci.

**Ottieni e salva la tua chiave API**

#. Accedi a |link_deepseek|.

#. Nel menu in alto a destra, seleziona **API Keys -> Create API Key**.

   .. image:: img/llm_deepseek_create.png

#. Inserisci un nome, clicca su **Create**, poi copia la chiave.

   .. image:: img/llm_deepseek_copy.png

#. Nella cartella del tuo progetto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Aggiungi la tua chiave:

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**Abilita la fatturazione**

Dovrai prima ricaricare il tuo account. Inizia con un piccolo importo (come ¥10 RMB).

   .. image:: img/llm_deepseek_chognzhi.png

**Modelli disponibili**

Al momento della scrittura (2025-09-12), DeepSeek offre:

* ``deepseek-chat``
* ``deepseek-reasoner``

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model="xxx"`` con il modello desiderato (ad esempio, ``deepseek-chat``):

   .. code-block:: python

      from fusion_hat.llm import Deepseek
      from secret import DEEPSEEK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Deepseek(
         api_key=DEEPSEEK_API_KEY,
         model="deepseek-chat",
         max_messages=20,
      )

#. Esegui:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

----

Doubao
------------------
Doubao e' la piattaforma di modelli AI di ByteDance (Volcengine Ark).

**Ottieni e salva la tua chiave API**

#. Accedi a |link_doubao|.

#. Nel menu a sinistra, scorri fino a **API Key Management -> Create API Key**.

   .. image:: img/llm_doubao_create.png

#. Scegli un nome e clicca su **Create**.

   .. image:: img/llm_doubao_name.png

#. Clicca sull'icona **Show API Key** e copiala.

   .. image:: img/llm_doubao_copy.png

#. Nella cartella del tuo progetto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Aggiungi la tua chiave:

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**Scegli un modello**

#. Vai al marketplace dei modelli e scegli un modello.

   .. image:: img/llm_doubao_model_select.png

#. Ad esempio, scegli **Doubao-seed-1.6**, poi clicca su **API 接入**.

   .. image:: img/llm_doubao_model.png

#. Seleziona la tua chiave API e clicca su **Use API**.

   .. image:: img/llm_doubao_use_api.png

#. Clicca su **Enable Model**.

   .. image:: img/llm_doubao_kaitong.png

#. Passa il mouse sopra l'ID del modello per copiarlo.

   .. image:: img/llm_doubao_copy_id.png

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Sostituisci il contenuto con il codice seguente e aggiorna ``model="xxx"`` con il modello desiderato (ad esempio, ``doubao-seed-1-6-250615``):

   .. code-block:: python

      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. Esegui con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ora puoi chattare con Fusion HAT+ direttamente dal terminale.

Generale
--------------

Questo progetto supporta la connessione a piattaforme LLM multiple attraverso un’interfaccia unificata.
Abbiamo compatibilita’ integrata con:

* **OpenAI** (ChatGPT / GPT-4o, GPT-4, GPT-3.5)
* **Gemini** (Google AI Studio / Vertex AI)
* **Grok** (xAI)
* **DeepSeek**
* **Qwen (通义千问)**
* **Doubao (豆包)**

Inoltre, puoi connetterti a **qualsiasi altro servizio LLM compatibile con il formato API OpenAI**.
Per queste piattaforme, dovrai ottenere manualmente la tua **chiave API** e il corretto **base_url**.

**Ottieni e salva la tua chiave API**

#. Ottieni una **chiave API** dalla piattaforma che desideri utilizzare. (Vedi la console ufficiale di ciascuna piattaforma per i dettagli.)

#. Nella cartella del tuo progetto, crea un nuovo file:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. Aggiungi la tua chiave in ``secret.py``:

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   Mantieni la tua chiave API privata. Non caricare ``secret.py`` su repository pubblici.

**Test con codice di esempio**

#. Apri il file di test:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. Sostituisci il contenuto di un file Python con il seguente esempio e inserisci il corretto ``base_url`` e ``model`` per la tua piattaforma:

   .. note::

      Informazioni su ``base_url``:
      Supportiamo il **formato API OpenAI**, cosi’ come qualsiasi API **compatibile** con esso.
      Ogni fornitore ha il proprio ``base_url``. Controlla la loro documentazione.

   .. code-block:: python

      from fusion_hat.llm import LLM
      from secret import API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = LLM(
         base_url = f"",
         api_key=API_KEY,
         model="",
      )

#. Esegui il programma:

   .. code-block:: bash

      sudo python3 llm_others.py



