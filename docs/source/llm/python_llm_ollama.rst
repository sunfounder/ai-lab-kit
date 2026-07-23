.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Texte, vision et dialogue avec Ollama
================================

Dans cette lecon, vous apprendrez a utiliser **Ollama**, un outil pour executer localement des grands modeles de langage et de vision.
Nous allons vous montrer comment installer Ollama, telecharger un modele et connecter le Fusion HAT+ a celui-ci.

Avec cette configuration, le Fusion HAT+ peut prendre une photo avec la camera et le modele pourra **voir et decrire** —
vous pouvez poser n'importe quelle question sur l'image, et le modele repondra en langage naturel.

.. _download_ollama:

1. Installer Ollama (LLM) et telecharger un modele
-------------------------------------------------

Vous pouvez choisir ou installer **Ollama** :

* Sur votre Raspberry Pi (execution locale)
* Ou sur un autre ordinateur (Mac/Windows/Linux) dans le **meme reseau local**

**Modeles recommandes selon le materiel**

Vous pouvez choisir n'importe quel modele disponible sur |link_ollama_hub|.
Les modeles existent en differentes tailles (3B, 7B, 13B, 70B...).
Les modeles plus petits s'executent plus rapidement et necessitent moins de memoire, tandis que les modeles plus grands offrent une meilleure qualite mais necessitent un materiel puissant.

Consultez le tableau ci-dessous pour decider quelle taille de modele correspond a votre appareil.

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - Taille du modele
     - RAM minimale requise
     - Materiel recommande
   * - ~3B parametres
     - 8 Go (16 Go mieux)
     - Raspberry Pi 5 (16 Go) ou PC/Mac moyen
   * - ~7B parametres
     - 16 Go+
     - Pi 5 (16 Go, juste utilisable) ou PC/Mac moyen
   * - ~13B parametres
     - 32 Go+
     - PC de bureau / Mac avec RAM elevee
   * - 30B+ parametres
     - 64 Go+
     - Station de travail / Serveur / GPU recommande
   * - 70B+ parametres
     - 128 Go+
     - Serveur haut de gamme avec plusieurs GPU

**Installer sur Raspberry Pi**

Si vous souhaitez executer Ollama directement sur votre Raspberry Pi :

* Utilisez un **Raspberry Pi OS 64 bits**
* Fortement recommande : **Raspberry Pi 5 (16 Go RAM)**

Executez les commandes suivantes :

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

**Installer sur Mac / Windows / Linux (application de bureau)**

1. Telechargez et installez Ollama depuis |link_ollama|

   .. image:: img/llm_ollama_download.png

2. Ouvrez l'application Ollama, allez dans le **Model Selector** et utilisez la barre de recherche pour trouver un modele. Par exemple, tapez ``llama3.2:3b`` (un petit modele leger pour commencer).

   .. image:: img/llm_ollama_choose.png

3. Une fois le telechargement termine, tapez quelque chose de simple comme "Hi" dans la fenetre de chat, Ollama commencera automatiquement a le telecharger lors de la premiere utilisation.

   .. image:: img/llm_olama_llama_download.png

4. Allez dans **Settings** → activez **Expose Ollama to the network**. Cela permet a votre Raspberry Pi de s'y connecter via le reseau local.

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   Si vous voyez une erreur comme :

   ``Error: model requires more system memory ...``

   Le modele est trop gros pour votre machine.
   Utilisez un **modele plus petit** ou passez a un ordinateur avec plus de RAM.

2. Tester Ollama
--------------

Une fois Ollama installe et votre modele pret, vous pouvez le tester rapidement avec une boucle de chat minimale.

**Definir l'adresse IP**

#. Ouvrez le script d'exemple :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. Mettez a jour les parametres selon vos besoins :

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")`` : Mettez a jour ``ip`` et ``model`` selon votre configuration.

     * ``ip`` : Si Ollama fonctionne sur le **meme Pi**, utilisez ``localhost``. Si Ollama fonctionne sur un autre ordinateur de votre LAN, activez **Expose to network** dans Ollama et definissez ``ip`` avec l'adresse IP LAN de cet ordinateur.
     * ``model`` : Doit correspondre exactement au nom du modele que vous avez telecharge/active dans Ollama.


**Executer le programme**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 llm_ollama.py

Vous pouvez maintenant discuter avec le Fusion HAT+ directement depuis le terminal.

   * Vous pouvez choisir **n'importe quel modele** disponible sur |link_ollama_hub|, mais les modeles plus petits (par ex., ``moondream:1.8b``, ``phi3:mini``) sont recommandes si vous n'avez que 8-16 Go de RAM.
   * Assurez-vous que le modele que vous specifiez dans le code correspond au modele que vous avez deja telecharge dans Ollama.
   * Tapez ``exit`` ou ``quit`` pour arreter le programme.
   * Si vous ne pouvez pas vous connecter, assurez-vous qu'Ollama est en cours d'execution et que les deux appareils sont sur le meme LAN si vous utilisez un hote distant.

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


3. Vision et dialogue avec Ollama
--------------------------

Dans cette demo, la camera Pi prend une photo **a chaque fois que vous tapez une question**.
Le programme envoie **votre texte saisi + la nouvelle photo** a un modele de vision local via Ollama,
puis diffuse la reponse du modele en anglais clair.
Il s'agit d'une base minimale de "voir et decrire" que vous pourrez ensuite etendre avec des verification de couleur/visage/QR.

**Avant de commencer**

#. Ouvrez l'application **Ollama** (ou lancez le service) et assurez-vous qu'un **modele compatible vision** est telecharge.

   * Si vous avez suffisamment de memoire (>=16 Go RAM), vous pouvez essayer ``llava:7b``.
   * Si vous n'avez que **8 Go RAM**, preferez un modele plus petit comme ``moondream:1.8b`` ou ``granite3.2-vision:2b``.

   .. image:: img/llm_ollama_image_model.png

**Executer la demo**

#. Allez dans le dossier d'exemple et executez le script :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. Ce qui se passe lors de l'execution :

   * Le programme affiche une ligne de bienvenue et attend votre saisie (``>>>``).
   * **Chaque fois que vous tapez quelque chose** (par ex., "hello", "Is there yellow?", "Any faces?", "What is on the desk?"), il :

     * **prend une photo** avec la camera Pi (enregistree dans ``/tmp/llm-img.jpg``),
     * **envoie votre texte + la photo** au modele de vision via Ollama,
     * **retourne en continu** la reponse du modele dans le terminal.

   * Tapez ``exit`` ou ``quit`` pour terminer le programme.

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


Depannage
---------------


* **J'obtiens une erreur du type : `model requires more system memory ...`.**

  * Cela signifie que le modele est trop gros pour votre appareil.
  * Utilisez un modele plus petit comme ``moondream:1.8b`` ou ``granite3.2-vision:2b``.
  * Ou passez a une machine avec plus de RAM et exposez Ollama au reseau.

* **Le code ne peut pas se connecter a Ollama (connexion refusee).**

  Verifiez les points suivants :

  * Assurez-vous qu'Ollama est en cours d'execution (``ollama serve`` ou l'application de bureau est ouverte).
  * Si vous utilisez un ordinateur distant, activez **Expose to network** dans les parametres Ollama.
  * Rev-erifiez que ``ip="..."`` dans votre code correspond a la bonne adresse IP LAN.
  * Confirmez que les deux appareils sont sur le meme reseau local.

* **Ma camera Pi ne capture rien.**

  * Verifiez que ``Picamera2`` est installe et fonctionne avec un script de test simple.
  * Verifiez que le cable de la camera est correctement branche et active dans ``raspi-config``.
  * Assurez-vous que votre script a la permission d'ecrire dans le chemin de destination (``/tmp/llm-img.jpg``).

* **La sortie est trop lente.**

  * Les modeles plus petits repondent plus vite, mais avec des reponses plus simples.
  * Vous pouvez reduire la resolution de la camera (par ex., 640x480 au lieu de 1280x720) pour accelerer le traitement d'image.
  * Fermez les autres programmes sur votre Pi pour liberer du CPU et de la RAM.