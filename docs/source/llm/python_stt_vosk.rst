.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _py_stt_whisper:
.. _test_vosk:

3. Reconnaissance vocale avec Vosk (hors ligne)
==============================================

Vosk est un moteur leger de reconnaissance vocale (STT) qui prend en charge de nombreuses langues et fonctionne entierement **hors ligne** sur Raspberry Pi.
Vous n'avez besoin d'un acces Internet qu'une seule fois pour telecharger un modele de langue. Ensuite, tout fonctionne sans connexion reseau.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Dans cette lecon, nous allons :

* Verifier le microphone sur Raspberry Pi.
* Installer et tester Vosk avec un modele de langue choisi.


.. start_mic


Executer le programme
--------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

La premiere fois que vous executerez ce code avec une nouvelle langue, Vosk va :

* **Telecharger automatiquement le modele de langue** (par defaut, la version legere).
* **Afficher la liste des langues prises en charge**.
* Commencer a **ecouter** l'entree audio via le microphone.

Vous verrez quelque chose comme ceci dans le terminal :

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

Cela signifie :

   * Le fichier du modele (``vosk-model-small-en-us-0.15``) a ete telecharge.
   * La liste des langues prises en charge a ete affichee.
   * Le systeme ecoute maintenant — dites quelque chose dans le microphone du Fusion HAT+, et le texte reconnu apparaitra dans le terminal.

**Conseils :**

* Maintenez le microphone a environ **15-30 cm** pour une meilleure precision.
* Choisissez un **modele qui correspond a votre langue et votre accent**.
* Utilisez un environnement silencieux pour ameliorer la reconnaissance.

Code
---------------

.. code-block:: python

   from fusion_hat.stt import Vosk as STT

   stt = STT(language="en-us")

   while True:
      print("Say something")
      for result in stt.listen(stream=True):
         if result["done"]:
               print(f"final:   {result['final']}")
         else:
               print(f"partial: {result['partial']}", end="\r", flush=True)


**Explication du code :**

* ``stt.listen(stream=True)`` — Demarre la reconnaissance vocale en continu et produit des resultats intermediaires pendant que vous parlez.
* ``result["partial"]`` — Affiche le **texte reconnu en temps reel** (mis a jour en continu).
* ``result["final"]`` — Affiche la **phrase finale reconnue** lorsque vous arretez de parler.
* La boucle s'execute en continu, permettant une **transcription en temps reel mains libres**.

**Conseil :** Ce mode de streaming est parfait pour les **assistants vocaux**, le **controle par commandes** ou la **transcription en direct**.

Depannage
-----------------

* **No such file or directory (lors de l'execution de `arecord`)**

  Vous avez peut-etre utilise le mauvais numero de carte/peripherique.
  Executez :

  .. code-block:: bash

     arecord -l

  et remplacez ``1,0`` par les numeros affiches pour votre microphone USB.


* **Vosk ne reconnait pas la parole**

  * Assurez-vous que le **code de langue** correspond a votre modele (par ex., ``en-us`` pour l'anglais, ``fr`` pour le francais).
  * Maintenez le microphone a 15-30 cm et evitez le bruit de fond.
  * Parlez clairement et lentement.

* **Latence elevee / reconnaissance lente**

  * Le telechargement automatique par defaut est un **petit modele** (plus rapide, mais moins precis).
  * Si c'est encore lent, fermez les autres programmes pour liberer le CPU.

.. end_mic