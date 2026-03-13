.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. Verbindung mit Online-LLMs
================================

In dieser Lektion lernen wir, wie Sie Ihr Fusion HAT+ (oder Ihren Raspberry Pi) mit verschiedenen **Online-Large-Language-Models (LLMs)** verbinden.  
Jeder Anbieter benötigt einen API-Schlüssel und bietet unterschiedliche Modelle zur Auswahl an.  

Wir behandeln dabei Schritt für Schritt:

* wie Sie Ihre API-Schlüssel sicher erstellen und speichern,
* wie Sie ein Modell auswählen, das zu Ihren Anforderungen passt,
* wie Sie unseren Beispielcode ausführen, um mit den Modellen zu chatten.

Gehen wir die einzelnen Anbieter nacheinander durch.

----

OpenAI
----------

OpenAI bietet leistungsstarke Modelle wie **GPT-4o** und **GPT-4.1**, die sowohl für Text- als auch für Vision-Aufgaben verwendet werden können.  

So richten Sie es ein:

.. start_setup_openai

**API-Schlüssel erstellen und speichern**

#. Gehen Sie zu |link_openai_platform| und melden Sie sich an. Klicken Sie auf der Seite **API keys** auf **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Füllen Sie die Angaben aus (Owner, Name, Project und gegebenenfalls Berechtigungen) und klicken Sie dann auf **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Sobald der Schlüssel erstellt wurde, kopieren Sie ihn sofort — später wird er nicht noch einmal angezeigt. Falls Sie ihn verlieren, müssen Sie einen neuen erstellen.

   .. image:: img/llm_openai_copy.png

#. Erstellen Sie in Ihrem Projektordner (zum Beispiel: ``/``) eine Datei mit dem Namen ``secret.py``:

   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel wie folgt in die Datei ein:

   .. code-block:: python
   
       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Abrechnung aktivieren und Modelle prüfen**

#. Bevor Sie den Schlüssel verwenden, öffnen Sie in Ihrem OpenAI-Konto die Seite **Billing**, hinterlegen Sie Ihre Zahlungsdaten und laden Sie ein kleines Guthaben auf.  

   .. image:: img/llm_openai_billing.png

#. Wechseln Sie anschließend zur Seite **Limits**, um zu prüfen, welche Modelle für Ihr Konto verfügbar sind, und kopieren Sie die genaue Modell-ID für die Verwendung im Code.  

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**Mit Beispielcode testen**

#. Öffnen Sie unseren Beispielcode:

   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` in das gewünschte Modell (zum Beispiel ``gpt-4o``):

   .. code-block:: python
   
      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )
  
   Speichern Sie die Datei und beenden Sie den Editor (``Ctrl+X``, dann ``Y``, dann ``Enter``).  

#. Führen Sie abschließend den Test aus:

   .. code-block:: bash
   
       sudo python3 llm_test.py
   
Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

----

Gemini
------------------

Gemini ist Googles Familie von AI-Modellen. Sie ist schnell und eignet sich hervorragend für allgemeine Aufgaben.

**API-Schlüssel erstellen und speichern**

#. Melden Sie sich bei |link_google_ai| an und gehen Sie anschließend zur Seite **API Keys**.

   .. image:: img/llm_gemini_get.png

#. Klicken Sie oben rechts auf die Schaltfläche **Create API key**.

   .. image:: img/llm_gemini_create.png

#. Sie können einen Schlüssel für ein bestehendes Projekt oder für ein neues Projekt erstellen.

   .. image:: img/llm_gemini_choose.png

#. Kopieren Sie den generierten API-Schlüssel.

   .. image:: img/llm_gemini_copy.png

#. Wechseln Sie in Ihren Projektordner:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie den Schlüssel ein:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**Verfügbare Modelle prüfen**

Gehen Sie zur offiziellen Seite |link_gemini_model|. Dort finden Sie eine Liste der Modelle, deren genaue API-IDs sowie die jeweiligen Einsatzbereiche.

   .. image:: img/llm_gemini_model.png

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` auf das gewünschte Modell (zum Beispiel ``gemini-2.5-flash``):

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. Speichern Sie die Datei und führen Sie sie aus:

   .. code-block:: bash

       sudo python3 llm_test.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

----

Qwen
------------------

Qwen ist eine Familie großer Sprach- und multimodaler Modelle von Alibaba Cloud.  
Diese Modelle unterstützen Textgenerierung, logisches Schlussfolgern und multimodales Verständnis (z. B. Bildanalyse).

**API-Schlüssel erstellen**

Um Qwen-Modelle aufzurufen, benötigen Sie einen **API Key**.  
Die meisten internationalen Benutzer sollten die **DashScope International (Model Studio)** Konsole verwenden.  
Benutzer in Festlandchina können stattdessen die **Bailian (百炼)** Konsole verwenden.

* **Für internationale Benutzer**

  #. Öffnen Sie die offizielle Seite |link_qwen_inter| auf **Alibaba Cloud**.  
  #. Melden Sie sich an oder erstellen Sie ein **Alibaba Cloud**-Konto.  
  #. Navigieren Sie zu **Model Studio** (Region Singapore oder Beijing auswählen).  
    
      * Wenn oben auf der Seite eine Meldung „Activate Now“ erscheint, klicken Sie darauf, um Model Studio zu aktivieren und das kostenlose Kontingent zu erhalten (nur Singapore).  
      * Die Aktivierung ist kostenlos — Kosten entstehen erst, wenn das kostenlose Kontingent aufgebraucht ist.  
      * Wenn keine Aktivierungsmeldung erscheint, ist der Dienst bereits aktiv. 
  
  #. Öffnen Sie die Seite **Key Management**. Klicken Sie im Tab **API Key** auf **Create API Key**.  
  #. Kopieren Sie den API-Schlüssel nach der Erstellung und bewahren Sie ihn sicher auf.  
  
    .. image:: img/llm_qwen_api_key.png
        :width: 800
  
  .. note::
     Benutzer aus Hongkong, Macau und Taiwan sollten ebenfalls die Option **International (Model Studio)** wählen.
  
* **Für Benutzer in Festlandchina**

  Wenn Sie sich in Festlandchina befinden, können Sie stattdessen die **Alibaba Cloud Bailian (百炼)** Konsole verwenden:
  
  #. Melden Sie sich bei |link_aliyun| (Bailian-Konsole) an und führen Sie die Kontoverifizierung durch.  
  #. Wählen Sie **Create API Key**. Wenn eine Meldung erscheint, dass Modellservices nicht aktiviert sind, klicken Sie auf **Activate**, stimmen Sie den Bedingungen zu und aktivieren Sie das kostenlose Kontingent. Danach wird die Schaltfläche **Create API Key** verfügbar.  
  
     .. image:: img/llm_qwen_aliyun_create.png
  
  #. Klicken Sie erneut auf **Create API Key**, überprüfen Sie Ihr Konto und klicken Sie anschließend auf **Confirm**.  
  
     .. image:: img/llm_qwen_aliyun_confirm.png
  
  #. Nach der Erstellung kopieren Sie Ihren API-Schlüssel.  
  
     .. image:: img/llm_qwen_aliyun_copy.png

**API-Schlüssel speichern**

#. Wechseln Sie in Ihren Projektordner:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel wie folgt ein:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
        
        QWEN_API_KEY = "sk-xxx"

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` auf das gewünschte Modell (zum Beispiel ``qwen-plus``):

   .. code-block:: python
   
      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model="qwen-plus",
      )

#. Führen Sie das Programm aus:

   .. code-block:: bash
   
       sudo python3 llm_test.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.


Grok (xAI)
------------------
Grok ist die konversationelle AI von xAI, entwickelt vom Team um Elon Musk. Sie können über die xAI API darauf zugreifen.

**API-Schlüssel erstellen und speichern**

#. Registrieren Sie sich hier: |link_grok_ai|. Laden Sie zunächst Guthaben auf Ihr Konto — andernfalls funktioniert die API nicht.

#. Öffnen Sie die Seite **API Keys** und klicken Sie auf **Create API key**.  

   .. image:: img/llm_grok_create.png

#. Geben Sie einen Namen für den Schlüssel ein und klicken Sie anschließend auf **Create API key**. 

   .. image:: img/llm_grok_name.png

#. Kopieren Sie den generierten Schlüssel und bewahren Sie ihn sicher auf. 

   .. image:: img/llm_grok_copy.png

#. Wechseln Sie in Ihren Projektordner:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel wie folgt ein:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
        
        GROK_API_KEY = "xai-xxx"

**Verfügbare Modelle prüfen**

Gehen Sie zur Seite **Models** in der xAI-Konsole. Dort sehen Sie alle Modelle, die für Ihr Team verfügbar sind, zusammen mit ihren genauen API-IDs — verwenden Sie diese IDs in Ihrem Code.

   .. image:: img/llm_grok_model.png

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` auf das gewünschte Modell (zum Beispiel ``grok-4-latest``):

   .. code-block:: python
   
      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. Führen Sie das Programm aus:

   .. code-block:: bash
   
       sudo python3 llm_test.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

----

DeepSeek
------------------

DeepSeek ist ein chinesischer LLM-Anbieter, der leistungsfähige Modelle zu vergleichsweise niedrigen Kosten anbietet.

**API-Schlüssel erstellen und speichern**

#. Melden Sie sich bei |link_deepseek| an. 

#. Wählen Sie im Menü oben rechts **API Keys → Create API Key**. 

   .. image:: img/llm_deepseek_create.png

#. Geben Sie einen Namen ein, klicken Sie auf **Create** und kopieren Sie anschließend den Schlüssel.

   .. image:: img/llm_deepseek_copy.png

#. Wechseln Sie in Ihren Projektordner:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel hinzu:

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**Abrechnung aktivieren**

Sie müssen Ihr Konto zunächst aufladen. Beginnen Sie am besten mit einem kleinen Betrag (z. B. ¥10 RMB). 

   .. image:: img/llm_deepseek_chognzhi.png

**Verfügbare Modelle**

Zum Zeitpunkt der Erstellung (2025-09-12) bietet DeepSeek folgende Modelle an:  

* ``deepseek-chat``  
* ``deepseek-reasoner``  

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` auf das gewünschte Modell (zum Beispiel ``deepseek-chat``):

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

#. Führen Sie das Programm aus:

   .. code-block:: bash
   
       sudo python3 llm_test.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

----

Doubao
------------------
Doubao ist die AI-Modellplattform von ByteDance (Volcengine Ark).

**API-Schlüssel erstellen und speichern**

#. Melden Sie sich bei |link_doubao| an.

#. Scrollen Sie im linken Menü nach unten zu **API Key Management → Create API Key**. 

   .. image:: img/llm_doubao_create.png

#. Wählen Sie einen Namen und klicken Sie auf **Create**.  

   .. image:: img/llm_doubao_name.png

#. Klicken Sie auf das Symbol **Show API Key** und kopieren Sie den Schlüssel. 

   .. image:: img/llm_doubao_copy.png

#. Wechseln Sie in Ihren Projektordner:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie Ihren Schlüssel hinzu:

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**Modell auswählen**

#. Gehen Sie zum Model-Marketplace und wählen Sie ein Modell aus.  

   .. image:: img/llm_doubao_model_select.png

#. Wählen Sie zum Beispiel **Doubao-seed-1.6** und klicken Sie anschließend auf **API 接入**. 

   .. image:: img/llm_doubao_model.png

#. Wählen Sie Ihren API-Key aus und klicken Sie auf **Use API**. 

   .. image:: img/llm_doubao_use_api.png

#. Klicken Sie auf **Enable Model**. 

   .. image:: img/llm_doubao_kaitong.png

#. Bewegen Sie den Mauszeiger über die Modell-ID, um sie zu kopieren. 

   .. image:: img/llm_doubao_copy_id.png

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Ersetzen Sie den Inhalt durch den folgenden Code und ändern Sie ``model="xxx"`` auf das gewünschte Modell (zum Beispiel ``doubao-seed-1-6-250615``):

   .. code-block:: python
   
      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. Führen Sie das Programm aus:

   .. code-block:: bash
   
       sudo python3 llm_test.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

General
--------------

Dieses Projekt unterstützt die Verbindung zu mehreren LLM-Plattformen über eine einheitliche Schnittstelle.  
Integriert sind derzeit:

* **OpenAI** (ChatGPT / GPT-4o, GPT-4, GPT-3.5)  
* **Gemini** (Google AI Studio / Vertex AI)  
* **Grok** (xAI)  
* **DeepSeek**  
* **Qwen (通义千问)**  
* **Doubao (豆包)**  

Darüber hinaus können Sie **jeden anderen LLM-Dienst verwenden, der mit dem OpenAI-API-Format kompatibel ist**.  
Für solche Plattformen müssen Sie Ihren **API-Key** und die korrekte **base_url** manuell konfigurieren.

**API-Schlüssel erstellen und speichern**

#. Besorgen Sie sich einen **API-Key** von der Plattform, die Sie verwenden möchten. (Weitere Informationen finden Sie in der jeweiligen offiziellen Konsole.)  

#. Erstellen Sie in Ihrem Projektordner eine neue Datei:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. Fügen Sie Ihren Schlüssel in ``secret.py`` ein:

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   Halten Sie Ihren API-Key geheim. Laden Sie ``secret.py`` nicht in öffentliche Repositories hoch.

**Mit Beispielcode testen**

#. Öffnen Sie die Testdatei:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. Ersetzen Sie den Inhalt der Python-Datei durch das folgende Beispiel und tragen Sie die korrekte ``base_url`` sowie das gewünschte ``model`` für Ihre Plattform ein:

   .. note::

      Zu ``base_url``:  
      Wir unterstützen das **OpenAI-API-Format** sowie jede API, die **kompatibel** dazu ist.  
      Jeder Anbieter hat seine eigene ``base_url``. Bitte prüfen Sie dazu die jeweilige Dokumentation.  

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

#. Führen Sie das Programm aus:

   .. code-block:: bash

      sudo python3 llm_others.py



