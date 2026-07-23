.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. Connexion aux LLM en ligne
================================

Dans cette lecon, nous allons apprendre a connecter votre Fusion HAT+ (ou Raspberry Pi) a differents **grands modeles de langage (LLM) en ligne**.
Chaque fournisseur necessite une cle API et propose differents modeles parmi lesquels choisir.

Nous allons voir comment :

* Creer et enregistrer vos cles API en toute securite.
* Choisir un modele adapte a vos besoins.
* Executer notre code d'exemple pour discuter avec les modeles.

Procedons etape par etape pour chaque fournisseur.

----

OpenAI
----------

OpenAI fournit des modeles puissants comme **GPT-4o** et **GPT-4.1** qui peuvent etre utilises pour des taches de texte et de vision.

Voici comment le configurer :

.. start_setup_openai

**Obtenir et enregistrer votre cle API**

#. Rendez-vous sur |link_openai_platform| et connectez-vous. Sur la page **API keys**, cliquez sur **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Remplissez les details (Owner, Name, Project et permissions si necessaire), puis cliquez sur **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Une fois la cle creee, copiez-la immediatement — vous ne pourrez plus la voir. Si vous la perdez, vous devrez en generer une nouvelle.

   .. image:: img/llm_openai_copy.png

#. Dans votre dossier de projet (par exemple : ``/``), creez un fichier ``secret.py`` :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Collez votre cle dans le fichier comme ceci :

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Activer la facturation et verifier les modeles**

#. Avant d'utiliser la cle, allez dans la page **Billing** de votre compte OpenAI, ajoutez vos coordonnees de paiement et approvisionnez un petit montant de credits.

   .. image:: img/llm_openai_billing.png

#. Ensuite, allez dans la page **Limits** pour verifier quels modeles sont disponibles pour votre compte et copiez l'ID exact du modele a utiliser dans votre code.

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**Tester avec le code d'exemple**

#. Ouvrez notre exemple de code :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``gpt-4o``) :

   .. code-block:: python

      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )

   Sauvegardez et quittez (``Ctrl+X``, puis ``Y``, puis ``Enter``).

#. Enfin, lancez le test :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

----

Gemini
------------------

Gemini est la famille de modeles d'IA de Google. Il est rapide et excellent pour les taches polyvalentes.

**Obtenir et enregistrer votre cle API**

#. Connectez-vous a |link_google_ai|, puis allez dans la page API Keys.

   .. image:: img/llm_gemini_get.png

#. Cliquez sur le bouton **Create API key** dans le coin superieur droit.

   .. image:: img/llm_gemini_create.png

#. Vous pouvez creer une cle pour un projet existant ou un nouveau projet.

   .. image:: img/llm_gemini_choose.png

#. Copiez la cle API generee.

   .. image:: img/llm_gemini_copy.png

#. Dans votre dossier de projet :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Collez la cle :

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**Verifier les modeles disponibles**

Rendez-vous sur la page officielle |link_gemini_model|, vous y verrez la liste des modeles, leurs ID API exacts et le cas d'usage pour lequel chacun est optimise.

   .. image:: img/llm_gemini_model.png

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``gemini-2.5-flash``) :

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. Sauvegardez et executez :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

----

Qwen
------------------

Qwen est une famille de modeles de langage et multimodaux fournis par Alibaba Cloud.
Ces modeles prennent en charge la generation de texte, le raisonnement et la comprehension multimodale (comme l'analyse d'images).

**Obtenir une cle API**

Pour appeler les modeles Qwen, vous avez besoin d'une **cle API**.
La plupart des utilisateurs internationaux doivent utiliser la console **DashScope International (Model Studio)**.
Les utilisateurs de Chine continentale peuvent utiliser la console **Bailian (百炼)**.

* **Pour les utilisateurs internationaux**

  #. Rendez-vous sur la page officielle |link_qwen_inter| de **Alibaba Cloud**.
  #. Connectez-vous ou creez un compte **Alibaba Cloud**.
  #. Accedez a **Model Studio** (choisissez la region Singapour ou Pekin).

      * Si une invite "Activate Now" apparait en haut de la page, cliquez dessus pour activer Model Studio et recevoir le quota gratuit (Singapour uniquement).
      * L'activation est gratuite — vous ne serez facture qu'apres utilisation de votre quota gratuit.
      * Si aucune invite d'activation n'apparait, le service est deja actif.

  #. Allez dans la page **Key Management**. Dans l'onglet **API Key**, cliquez sur **Create API Key**.
  #. Apres la creation, copiez votre cle API et conservez-la en lieu sur.

    .. image:: img/llm_qwen_api_key.png
        :width: 800

  .. note::
     Les utilisateurs de Hong Kong, Macao et Taiwan doivent egalement choisir l'option **International (Model Studio)**.

* **Pour les utilisateurs de Chine continentale**

  Si vous etes en Chine continentale, vous pouvez utiliser la console **Alibaba Cloud Bailian (百炼)** :

  #. Connectez-vous a |link_aliyun| (console Bailian) et completez la verification du compte.
  #. Selectionnez **Create API Key**. Si un message indique que les services de modele ne sont pas actives, cliquez sur **Activate**, acceptez les conditions et reclamez votre quota gratuit. Apres l'activation, le bouton **Create API Key** sera active.

     .. image:: img/llm_qwen_aliyun_create.png

  #. Cliquez a nouveau sur **Create API Key**, verifiez votre compte, puis cliquez sur **Confirm**.

     .. image:: img/llm_qwen_aliyun_confirm.png

  #. Une fois creee, copiez votre cle API.

     .. image:: img/llm_qwen_aliyun_copy.png

**Enregistrer votre cle API**

#. Dans votre dossier de projet :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Collez votre cle comme ceci :

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        QWEN_API_KEY = "sk-xxx"

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``qwen-plus``) :

   .. code-block:: python

      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model="qwen-plus",
      )

#. Executez avec :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

Grok (xAI)
------------------
Grok est l'IA conversationnelle de xAI, creee par l'equipe d'Elon Musk. Vous pouvez vous y connecter via l'API xAI.

**Obtenir et enregistrer votre cle API**

#. Inscrivez-vous pour un compte ici : |link_grok_ai|. Ajoutez d'abord des credits a votre compte — sinon l'API ne fonctionnera pas.

#. Allez dans la page API Keys, cliquez sur **Create API key**.

   .. image:: img/llm_grok_create.png

#. Saisissez un nom pour la cle, puis cliquez sur **Create API key**.

   .. image:: img/llm_grok_name.png

#. Copiez la cle generee et conservez-la en lieu sur.

   .. image:: img/llm_grok_copy.png

#. Dans votre dossier de projet :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Collez votre cle comme ceci :

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        GROK_API_KEY = "xai-xxx"

**Verifier les modeles disponibles**

Rendez-vous dans la page Models de la console xAI. Vous y verrez tous les modeles disponibles pour votre equipe, ainsi que leurs ID API exacts — utilisez ces IDs dans votre code.

   .. image:: img/llm_grok_model.png

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``grok-4-latest``) :

   .. code-block:: python

      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. Executez avec :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

----

DeepSeek
------------------

DeepSeek est un fournisseur de LLM chinois qui propose des modeles abordables et performants.

**Obtenir et enregistrer votre cle API**

#. Connectez-vous a |link_deepseek|.

#. Dans le menu en haut a droite, selectionnez **API Keys → Create API Key**.

   .. image:: img/llm_deepseek_create.png

#. Saisissez un nom, cliquez sur **Create**, puis copiez la cle.

   .. image:: img/llm_deepseek_copy.png

#. Dans votre dossier de projet :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Ajoutez votre cle :

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**Activer la facturation**

Vous devez d'abord recharger votre compte. Commencez avec un petit montant (comme ¥10 RMB).

   .. image:: img/llm_deepseek_chognzhi.png

**Modeles disponibles**

Au moment de la redaction (12/09/2025), DeepSeek propose :

* ``deepseek-chat``
* ``deepseek-reasoner``

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``deepseek-chat``) :

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

#. Executez :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

----

Doubao
------------------
Doubao est la plateforme de modeles d'IA de ByteDance (Volcengine Ark).

**Obtenir et enregistrer votre cle API**

#. Connectez-vous a |link_doubao|.

#. Dans le menu de gauche, faites defiler jusqu'a **API Key Management → Create API Key**.

   .. image:: img/llm_doubao_create.png

#. Choisissez un nom et cliquez sur **Create**.

   .. image:: img/llm_doubao_name.png

#. Cliquez sur l'icone **Show API Key** et copiez-la.

   .. image:: img/llm_doubao_copy.png

#. Dans votre dossier de projet :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Ajoutez votre cle :

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**Choisir un modele**

#. Rendez-vous sur le marketplace de modeles et choisissez un modele.

   .. image:: img/llm_doubao_model_select.png

#. Par exemple, choisissez **Doubao-seed-1.6**, puis cliquez sur **API 接入**.

   .. image:: img/llm_doubao_model.png

#. Selectionnez votre cle API et cliquez sur **Use API**.

   .. image:: img/llm_doubao_use_api.png

#. Cliquez sur **Enable Model**.

   .. image:: img/llm_doubao_kaitong.png

#. Survolez l'ID du modele pour le copier.

   .. image:: img/llm_doubao_copy_id.png

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Remplacez le contenu par le code ci-dessous, et mettez a jour ``model="xxx"`` avec le modele souhaite (par exemple, ``doubao-seed-1-6-250615``) :

   .. code-block:: python

      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. Executez avec :

   .. code-block:: bash

       sudo python3 llm_test.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

General
--------------

Ce projet prend en charge la connexion a plusieurs plateformes LLM via une interface unifiee.
Nous avons une compatibilite integree avec :

* **OpenAI** (ChatGPT / GPT-4o, GPT-4, GPT-3.5)
* **Gemini** (Google AI Studio / Vertex AI)
* **Grok** (xAI)
* **DeepSeek**
* **Qwen (通义千问)**
* **Doubao (豆包)**

De plus, vous pouvez vous connecter a **tout autre service LLM compatible avec le format d'API OpenAI**.
Pour ces plateformes, vous devrez obtenir manuellement votre **cle API** et le **base_url** correct.

**Obtenir et enregistrer votre cle API**

#. Obtenez une **cle API** aupres de la plateforme que vous souhaitez utiliser. (Consultez la console officielle de chaque plateforme pour plus de details.)

#. Dans votre dossier de projet, creez un nouveau fichier :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. Ajoutez votre cle dans ``secret.py`` :

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   Gardez votre cle API privee. Ne telechargez pas ``secret.py`` dans des depots publics.

**Tester avec le code d'exemple**

#. Ouvrez le fichier de test :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. Remplacez le contenu d'un fichier Python par l'exemple suivant, et remplissez le ``base_url`` et ``model`` corrects pour votre plateforme :

   .. note::

      A propos de ``base_url`` :
      Nous prenons en charge le **format d'API OpenAI**, ainsi que toute API **compatible** avec celui-ci.
      Chaque fournisseur a son propre ``base_url``. Veuillez consulter leur documentation.

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

#. Executez le programme :

   .. code-block:: bash

      sudo python3 llm_others.py