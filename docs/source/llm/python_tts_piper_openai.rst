.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. Synthese vocale avec Piper et OpenAI
========================================================

Dans la lecon precedente, nous avons decouvert **Espeak** et **Pico2Wave**, deux moteurs TTS hors ligne simples sur Raspberry Pi.
Maintenant, passons a la vitesse superieure et essayons deux **options TTS plus avancees** offrant une **meilleure qualite vocale** et plus de flexibilite :

* **Piper** — un moteur TTS rapide base sur un reseau de neurones qui fonctionne **completement hors ligne** sur Raspberry Pi.
* **OpenAI TTS** — un service en ligne qui fournit des voix **tres naturelles et humaines**, parfait pour une parole expressive.

Ces moteurs rendront votre Fusion HAT+ plus realiste et vivant.

----

.. _test_piper:

1. Tester Piper
------------------

Piper est un **moteur TTS neuronal hors ligne**, ce qui signifie que vous n'avez pas besoin de connexion Internet une fois le modele installe.
Il prend en charge plusieurs **langues** et **voix**, ce qui en fait une option puissante pour la parole integree.

**Executer le programme**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* La premiere fois que vous l'executerez, le **modele vocal** selectionne sera telecharge automatiquement.
* Vous devriez ensuite entendre le Fusion HAT+ dire : ``Hello! I'm Piper TTS.``
* Vous pouvez changer de voix ou de langue en appelant ``set_model()`` avec un nom de modele different.

**Code**

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

**Explication du code :**

* ``available_countrys()`` — Liste toutes les langues prises en charge.
* ``available_models()`` — Liste les modeles disponibles pour une langue specifique.
* ``set_model()`` — Definit le modele vocal. Si le modele n'est pas installe, il sera telecharge automatiquement.
* ``say()`` — Convertit le texte en parole et le joue immediatement.

**Conseil :** Essayez differents modeles pour comparer la vitesse, la clarte et les accents. Certains modeles sont plus legers (plus rapides), tandis que d'autres offrent une meilleure fidelite.

----

2. Tester OpenAI TTS
-------------------------------

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

**Executer le programme**

.. code-block:: bash

  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* Le programme se connectera au service TTS d'OpenAI, et le Fusion HAT+ parlera avec une **voix naturelle et expressive**.
* Vous pouvez changer les **styles de voix** et ajouter des **instructions** pour controler le ton et l'expression (par exemple, triste, dramatique, enjouee).
* Cela rend OpenAI TTS ideal pour les robots interactifs, les recits ou les assistants educatifs.


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


**Explication du code :**

* ``OpenAI_TTS()`` — Initialise le moteur TTS OpenAI avec votre cle API.
* ``set_model()`` — Selectionne le modele TTS (par ex., ``gpt-4o-mini-tts``).
* ``set_voice()`` — Choisit une voix specifique (par ex., ``alloy``).
* ``say(text)`` — Convertit le texte en parole et le joue.
* ``say(text, instructions=...)`` — Ajoute des **instructions de ton expressif**, vous permettant de controler dynamiquement le style de parole.

**Exemple :**

- "say it sadly" → ton doux et emotionnel
- "say it dramatically" → rendition audacieuse et expressive
- "say it excitedly" → ton enthousiaste

----

Depannage
-------------------

* **Pas de module nomme 'secret'**

  Cela signifie que ``secret.py`` n'est pas dans le meme dossier que votre fichier Python.
  Deplacez ``secret.py`` dans le meme repertoire ou vous executez le script, par ex. :

  .. code-block:: bash

     ls ~/
     # Make sure you see both: secret.py and your .py file

* **OpenAI : Cle API invalide / 401**

  * Verifiez que vous avez colle la cle complete (commence par ``sk-``) et qu'il n'y a pas d'espaces/sauts de ligne supplementaires.
  * Assurez-vous que votre code l'importe correctement :

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * Confirmez l'acces reseau sur votre Pi (essayez ``ping api.openai.com``).

* **OpenAI : Quota depasse / erreur de facturation**

  * Vous devrez peut-etre ajouter des credits ou augmenter le quota dans le tableau de bord OpenAI.
  * Reessayez apres avoir resolu le probleme de compte/facturation.

* **Piper : tts.say() s'execute mais pas de son**

  * Assurez-vous qu'un modele vocal est bien present :

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * Confirmez que le nom du modele correspond exactement dans le code :

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * Verifiez le peripherique/volume de sortie audio sur votre Pi (``alsamixer``), et que les enceintes sont connectees et alimentees.

* **Erreurs ALSA / peripherique audio (par ex., "Audio device busy" ou "No such file or directory")**

  * Fermez les autres programmes utilisant l'audio.
  * Redemarrez le Pi si le peripherique reste occupe.
  * Pour la sortie HDMI vs prise casque, selectionnez le bon peripherique dans les parametres audio de Raspberry Pi OS.

* **Permission refusee lors de l'execution de Python**

  * Essayez avec ``sudo`` si votre environnement l'exige :

    .. code-block:: bash

       sudo python3 tts_piper.py

Comparaison des moteurs TTS
-------------------------

.. list-table:: Comparaison des fonctionnalites : Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - Element
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - Fonctionne sur
     - Integre a Raspberry Pi (hors ligne)
     - Integre a Raspberry Pi (hors ligne)
     - Raspberry Pi / PC (hors ligne, necessite un modele)
     - Cloud (en ligne, necessite une cle API)
   * - Qualite vocale
     - Robotique
     - Plus naturelle qu'Espeak
     - Naturelle (TTS neuronal)
     - Tres naturelle / humaine
   * - Controles
     - Vitesse, hauteur, volume
     - Controles limites
     - Choisir differentes voix/modeles
     - Choisir le modele et la voix
   * - Langues
     - Nombreuses (qualite variable)
     - Ensemble limite
     - Nombreuses voix/langues disponibles
     - Meilleur en anglais (autres selon disponibilite)
   * - Latence / vitesse
     - Tres rapide
     - Rapide
     - Temps reel sur Pi 4/5 avec modeles "low"
     - Dependant du reseau (generalement faible latence)
   * - Configuration
     - Minimale
     - Minimale
     - Telecharger les modeles ``.onnx`` + ``.onnx.json``
     - Creer une cle API, installer le client
   * - Ideal pour
     - Tests rapides, invites de base
     - Voix hors ligne legerement meilleure
     - Projets locaux avec meilleure qualite
     - Qualite maximale, options vocales riches