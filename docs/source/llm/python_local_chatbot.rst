.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. Assistant vocal local
===========================

Dans cette lecon, vous allez combiner tout ce que vous avez appris — **la reconnaissance vocale (STT)**,
**la synthese vocale (TTS)** et un **LLM local (Ollama)** — pour construire un **assistant vocal entierement hors ligne**
qui fonctionne sur votre Fusion HAT+.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Local_Voice_Chatbot.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Le fonctionnement est simple :

#. **Ecouter** — Le microphone capture votre parole et la retranscrit avec **Vosk**.
#. **Reflechir** — Le texte est envoye a un **LLM** local fonctionnant sur Ollama (par ex., ``llama3.2:3b``).
#. **Parler** — L'assistant repond a voix haute en utilisant **Piper TTS**.

Cela cree un **robot conversationnel mains libres** capable de comprendre et de repondre en temps reel.

----

Avant de commencer
----------------

Assurez-vous d'avoir prepare les elements suivants :

* Teste **Piper TTS** (:ref:`test_piper`) et choisi un modele vocal fonctionnel.
* Teste **Vosk STT** (:ref:`test_vosk`) et choisi le pack de langue adapte (par ex., ``en-us``).
* Installe **Ollama** (:ref:`download_ollama`) sur votre Pi ou un autre ordinateur, et telecharge un modele comme ``llama3.2:3b`` (ou un plus petit comme ``moondream:1.8b`` si la memoire est limitee).

----

Executer le code
--------------

#. Ouvrez le script d'exemple :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano local_voice_chatbot.py

#. Mettez a jour les parametres selon vos besoins :

   * ``stt = Vosk(language="en-us")`` : Modifiez ceci pour correspondre a votre accent/pack de langue (par ex., ``en-us``, ``fr``, ``es``).
   * ``tts.set_model("en_US-amy-low")`` : Remplacez par le modele vocal Piper que vous avez verifie dans :ref:`test_piper`.
   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")`` : Mettez a jour ``ip`` et ``model`` selon votre configuration.

     * ``ip`` : Si Ollama fonctionne sur le **meme Pi**, utilisez ``localhost``. Si Ollama fonctionne sur un autre ordinateur de votre LAN, activez **Expose to network** dans Ollama et definissez ``ip`` avec l'adresse IP LAN de cet ordinateur.
     * ``model`` : Doit correspondre exactement au nom du modele que vous avez telecharge/active dans Ollama.

#. Executez le script :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo python3 local_voice_chatbot.py

#. Apres l'execution, vous devriez voir :

   * Le bot vous accueille avec un message de bienvenue parle.
   * Il attend une entree vocale.
   * Vosk retranscrit votre parole en texte.
   * Le texte est envoye a Ollama, qui renvoie une reponse en continu.
   * La reponse est nettoyee (suppression du raisonnement cache) et prononcee a voix haute par Piper.
   * Arretez le programme a tout moment avec ``Ctrl+C``.

----

Code
----

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

   # Initialize speech recognition
   stt = Vosk(language="en-us")

   # Initialize TTS
   tts = Piper()
   tts.set_model("en_US-amy-low")

   # Instructions for the LLM
   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

   # Initialize Ollama connection
   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

   # Utility: clean hidden reasoning
   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

   def main():
       print(WELCOME)
       tts.say(WELCOME)

       try:
           while True:
               print("\n Listening... (Press Ctrl+C to stop)")

               # Collect final transcript from Vosk
               text = ""
               for result in stt.listen(stream=True):
                   if result["done"]:
                       text = result["final"].strip()
                       print(f"[YOU] {text}")
                   else:
                       print(f"[YOU] {result['partial']}", end="\r", flush=True)

               if not text:
                   print("[INFO] Nothing recognized. Try again.")
                   time.sleep(0.1)
                   continue

               # Query Ollama with streaming
               reply_accum = ""
               response = llm.prompt(text, stream=True)
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       reply_accum += next_word
               print("")

               # Clean and speak
               clean = strip_thinking(reply_accum)
               if clean:
                   tts.say(clean)
               else:
                   tts.say("Sorry, I didn't catch that.")

               time.sleep(0.05)

       except KeyboardInterrupt:
           print("\n[INFO] Stopping...")
       finally:
           tts.say("Goodbye!")
           print("Bye.")

   if __name__ == "__main__":
       main()

----

Analyse du code
-------------

**Imports et configuration globale**

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

Importe les trois sous-systemes que vous avez construits precedemment :
**Vosk** pour la reconnaissance vocale (STT), **Ollama** pour le LLM, et **Piper** pour la synthese vocale (TTS).



**Initialiser le STT (Vosk)**

.. code-block:: python

   stt = Vosk(language="en-us")

Charge le modele Vosk pour l'anglais americain.
Changez le code de langue (par ex., ``fr``, ``es``) pour correspondre a votre pack vocal pour une meilleure precision.



**Initialiser le TTS (Piper)**

.. code-block:: python

   tts = Piper()
   tts.set_model("en_US-amy-low")

Cree un moteur Piper et selectionne une voix specifique.
Choisissez un modele que vous avez teste dans :ref:`test_piper`. Les voix de moindre qualite sont plus rapides et utilisent moins de CPU.



**Instructions LLM et message de bienvenue**

.. code-block:: python

   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

Deux choix UX cles :

* Gardez les **reponses courtes et directes** (aide a la clarte du TTS).
* Interdisez explicitement les balises cachees de "chaine de pensee" pour reduire le bruit.



**Se connecter a Ollama et definir la portee de la conversation**

.. code-block:: python

   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

* ``ip="localhost"`` suppose que le serveur Ollama fonctionne sur le meme Pi. S'il fonctionne sur une autre machine du LAN, mettez l'**IP LAN** de cet ordinateur et activez *Expose to network* dans Ollama.
* ``set_max_messages(20)`` conserve un historique de conversation court. Reduisez-le si la memoire/la latence est limitee.

**Supprimer le raisonnement cache / les balises avant de parler**

.. code-block:: python

   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

Certains modeles peuvent emettre des balises internes (par ex., ``<think>...``).
Cette fonction les supprime pour que votre TTS **ne prononce que** la reponse finale.

**Conseil :** Si vous voyez d'autres artefacts a l'ecran (parce que vous diffusez des jetons bruts), cette fonction garantit deja que la sortie **parlee** reste propre.

**Boucle principale : accueillir une fois, puis ecouter → reflechir → parler**

.. code-block:: python

   print(WELCOME)
   tts.say(WELCOME)

Accueille l'utilisateur via le terminal et le haut-parleur. Se produit une fois au demarrage.

**Ecouter (STT en streaming avec resultats partiels en direct)**

.. code-block:: python

   print("\n Listening... (Press Ctrl+C to stop)")

   text = ""
   for result in stt.listen(stream=True):
       if result["done"]:
           text = result["final"].strip()
           print(f"[YOU] {text}")
       else:
           print(f"[YOU] {result['partial']}", end="\r", flush=True)

* ``stream=True`` produit des transcriptions **partielles** pour un retour immediat et une transcription **finale** lorsque l'utterance se termine.
* Le texte final reconnu est stocke dans ``text`` et affiche une fois.

**Garde :** Si rien n'a ete reconnu, vous sautez l'appel LLM :

.. code-block:: python

   if not text:
       print("[INFO] Nothing recognized. Try again.")
       time.sleep(0.1)
       continue

Cela evite d'envoyer des invites vides au modele (economise du temps et des jetons).

**Reflechir (LLM) avec impression en continu**

.. code-block:: python

   reply_accum = ""
   response = llm.prompt(text, stream=True)
   for next_word in response:
       if next_word:
           print(next_word, end="", flush=True)
           reply_accum += next_word
   print("")

* Envoie la transcription finale au LLM local et **affiche les jetons au fur et a mesure** pour une faible latence.
* Pendant ce temps, vous accumulez la reponse complete dans ``reply_accum`` pour le post-traitement.

**Remarque :** Si vous preferez **ne pas** afficher les jetons bruts, definissez ``stream=False`` et affichez simplement la chaine finale.

**Parler (nettoyer d'abord, puis TTS une seule fois)**

.. code-block:: python

   clean = strip_thinking(reply_accum)
   if clean:
       tts.say(clean)
   else:
       tts.say("Sorry, I didn't catch that.")

* Nettoie le texte final pour supprimer les balises cachees, puis **parle exactement une fois**.
* Garder le TTS a un seul passage evite les invites repetees comme "[LLM] / [SAY]".


**Sortie et arret**

.. code-block:: python

   except KeyboardInterrupt:
       print("\n[INFO] Stopping...")
   finally:
       tts.say("Goodbye!")
       print("Bye.")

Utilisez **Ctrl+C** pour arreter. Le bot dit un court aurevoir pour signaler un arret propre.


----

Depannage et FAQ
---------------------

* **Le modele est trop volumineux (erreur memoire)**

  Utilisez un modele plus petit comme ``moondream:1.8b`` ou executez Ollama sur un ordinateur plus puissant.

* **Pas de reponse d'Ollama**

  Assurez-vous qu'Ollama est en cours d'execution (``ollama serve`` ou application de bureau ouverte). Si a distance, activez **Expose to network** et verifiez l'adresse IP.

* **Vosk ne reconnait pas la parole**

  Verifiez que votre microphone fonctionne. Essayez un autre pack de langue (``fr``, ``es``, etc.) si necessaire.

* **Piper silencieux ou erreurs**

  Confirmez que le modele vocal choisi est telecharge et teste dans :ref:`test_piper`.

* **Reponses trop longues ou hors sujet**

  Modifiez ``INSTRUCTIONS`` pour ajouter : **"Keep answers short and to the point."**