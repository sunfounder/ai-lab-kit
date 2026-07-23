.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. Assistant vocal IA
===========================

Cette lecon transforme votre Fusion HAT+ en un **assistant vocal IA**.
Avec le code fourni, le robot va : **attendre un mot d'eveil**, **retranscrire votre parole** avec Vosk, l'envoyer a un **LLM OpenAI**, et **repondre vocalement** avec Piper TTS.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Voice_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----

Avant de commencer
----------------

Assurez-vous d'avoir :

* :ref:`test_piper` — La voix Piper fonctionne (par exemple, vous pouvez jouer "Hello").
* :ref:`test_vosk` — Le STT Vosk fonctionne pour votre langue (par ex., ``en-us``).
* :ref:`py_online_llm` — Votre **cle API OpenAI** enregistree dans ``secret.py`` sous ``OPENAI_API_KEY``.
* Un **microphone** et un **haut-parleur** fonctionnels sur le Fusion HAT+.
* Une connexion reseau stable (le LLM est en ligne).

----

Executer l'exemple
---------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**Configuration utilisee par le code :**

* LLM : **OpenAI** (``gpt-4o-mini``)
* TTS : **Piper** (``en_US-ryan-low``)
* STT : **Vosk** (``en-us``)
* Mot d'eveil : ``"hey buddy"``
* Saisie clavier : **activee** (saisie manuelle optionnelle)
* Mode image : **active** (``WITH_IMAGE=True``) — necessite un LLM multimodal si vous decidez d'utiliser des images plus tard

**Ce qui se passe :**

1. L'assistant affiche un message de bienvenue avec la phrase d'eveil.
2. Il ecoute le mot **"hey buddy"**.
3. Apres l'eveil, votre parole est retranscrite (Vosk → texte).
4. Le texte est envoye a **OpenAI (gpt-4o-mini)** pour une reponse.
5. La reponse est prononcee avec **Piper** (``en_US-ryan-low``).

**Exemple d'interaction**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What's the capital of Italy?
   Robot: The capital of Italy is Rome.

Code
-----------------

.. code-block:: python

  from fusion_hat.voice_assistant import VoiceAssistant
  from fusion_hat.llm import OpenAI as LLM
  from secret import OPENAI_API_KEY as API_KEY

  llm = LLM(
      api_key=API_KEY,
      model="gpt-4o-mini",
  )

  # Robot name
  NAME = "Buddy"

  # Enable image, need to set up a multimodal language model
  WITH_IMAGE = True

  # Set models and languages
  LLM_MODEL = "gpt-4o-mini"
  TTS_MODEL = "en_US-ryan-low"
  STT_LANGUAGE = "en-us"

  # Enable keyboard input
  KEYBOARD_ENABLE = True

  # Enable wake word
  WAKE_ENABLE = True
  WAKE_WORD = [f"hey {NAME.lower()}"]
  # Set wake word answer, set empty to disable
  ANSWER_ON_WAKE = "Hi there"

  # Welcome message
  WELCOME = f"Hi, I'm {NAME}. Wake me up with: " + ", ".join(WAKE_WORD)

  # Set instructions
  INSTRUCTIONS = f"""
  You are a helpful assistant, named {NAME}.
  """

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

  if __name__ == "__main__":
      va.run()

**Explication du code :**

* ``OpenAI(..., model="gpt-4o-mini")`` — Utilise **OpenAI** comme seul LLM dans cette lecon.
* ``NAME`` / ``WAKE_WORD`` — Personnalisez l'assistant ("Buddy", "hey buddy").
* ``WITH_IMAGE=True`` — Active le mode image dans l'assistant (aucune logique d'entree/sortie d'image incluse ici).
* ``TTS_MODEL="en_US-ryan-low"`` — Voix Piper utilisee pour les reponses.
* ``STT_LANGUAGE="en-us"`` — Langue Vosk pour la reconnaissance.
* ``KEYBOARD_ENABLE=True`` — Permet une saisie manuelle optionnelle pendant le debogage.
* ``WELCOME`` / ``INSTRUCTIONS`` — Message de demarrage et personnalite de l'assistant / invite systeme.
* ``va.run()`` — Demarre la boucle : **eveil → ecoute → LLM → parole**.


Passer a d'autres LLM ou TTS
------------------------------

Vous pouvez facilement passer a d'autres LLM, TTS ou langues STT avec seulement quelques modifications :

* LLM pris en charge :

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — Consultez les langues prises en charge par **Piper TTS**.
* :ref:`test_vosk` — Consultez les langues prises en charge par **Vosk STT**.

Pour changer, modifiez simplement la partie d'initialisation dans le code :

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key="YOUR_KEY", model="gemini-pro")

   # Set models and languages
   TTS_MODEL = "en_US-ryan-low"
   STT_LANGUAGE = "en-us"



----

Depannage
-----------------------------

* **Le robot ne repond pas au mot d'eveil**

  - Verifiez si le microphone fonctionne.
  - Assurez-vous que ``WAKE_ENABLE = True``.
  - Ajustez le mot d'eveil en fonction de votre prononciation.
  - Reduisez le bruit de fond et parlez clairement.

* **Pas de son provenant du haut-parleur**

  - Verifiez le nom du modele TTS (par ex., ``en_US-ryan-low``).
  - Testez Piper ou Espeak manuellement.
  - Verifiez la connexion du haut-parleur et le volume.

* **Erreur de cle API ou delai d'attente**

  - Verifiez votre cle dans ``secret.py``.
  - Assurez-vous que votre connexion reseau est stable.
  - Confirmez que le modele LLM est pris en charge (par ex., ``gpt-4o-mini``).

* **Le mot d'eveil fonctionne mais pas de reponse**

  - Verifiez si la langue STT correspond a votre accent.
  - Assurez-vous que le modele a ete telecharge correctement.
  - Essayez d'afficher des journaux de debogage pour confirmer que le STT fonctionne.

* **Le TTS fonctionne mais pas de reponse du LLM**

  - Verifiez si la cle API est valide.
  - Verifiez le nom du modele et les parametres LLM.
  - Assurez-vous de la connectivite Internet.