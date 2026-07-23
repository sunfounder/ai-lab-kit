.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. Synthese vocale avec Espeak et Pico2Wave
=================================================

Dans cette lecon, nous allons utiliser deux moteurs de synthese vocale (TTS) integres sur Raspberry Pi — **Espeak** et **Pico2Wave** — pour faire parler le Fusion HAT+.

Ces deux moteurs sont simples et fonctionnent hors ligne, mais leur rendu sonore est assez different :

* **Espeak** : tres leger et rapide, mais la voix est robotique. Vous pouvez regler la vitesse, la hauteur tonale et le volume.
* **Pico2Wave** : produit une voix plus naturelle et plus fluide qu'Espeak, mais offre moins d'options de configuration.

Vous entendrez la difference au niveau de la **qualite vocale** et des **fonctionnalites**.

----

1. Tester Espeak
--------------------

Espeak est un moteur TTS leger inclus dans Raspberry Pi OS.
Sa voix est robotique, mais il est hautement configurable : vous pouvez regler le volume, la hauteur tonale, la vitesse et bien plus.

**Executer le programme**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * Vous devriez entendre le Fusion HAT+ dire : "Hello! I'm Espeak TTS."
  * Essayez de modifier les parametres dans le code pour experimenter comment ``amp``, ``speed``, ``gap`` et ``pitch`` affectent le son.

**Code**

.. code-block:: python

  from fusion_hat.tts import Espeak

  # Create Espeak TTS instance
  tts = Espeak()
  # Set amplitude 0-200, default 100
  tts.set_amp(200)
  # Set speed 80-260, default 150
  tts.set_speed(150)
  # Set gap 0-200, default 1
  tts.set_gap(1)
  # Set pitch 0-99, default 80
  tts.set_pitch(80)

  tts.say("Hello! I'm Espeak TTS.")

**Explication du code :**

* ``tts.set_amp()`` — Controle le volume (0-200).
* ``tts.set_speed()`` — Ajuste la vitesse de parole (80-260).
* ``tts.set_gap()`` — Definit l'espace entre les mots (0-200).
* ``tts.set_pitch()`` — Definit la hauteur tonale (0-99).
* ``tts.say()`` — Convertit le texte en parole et le joue.

**Conseil :** Essayez d'augmenter la hauteur tonale et la vitesse pour rendre la voix du robot plus joyeuse, ou de les baisser pour la rendre plus serieuse.

----


2. Tester Pico2Wave
---------------------

Pico2Wave produit une voix **plus naturelle et plus humaine** qu'Espeak.
Il est tres facile a utiliser, mais moins flexible — vous ne pouvez que **changer la langue**, pas la hauteur tonale, la vitesse ou le volume.
Cela fait de Pico2Wave un excellent choix lorsque vous souhaitez une parole claire et fluide sans trop de configuration.

**Executer le programme**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* Vous devriez entendre le Fusion HAT+ dire : "Hello! I'm Pico2Wave TTS."
* Essayez de changer la langue (par exemple, ``fr-FR`` pour le francais) et ecoutez comment la voix change.

**Code**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**Explication du code :**

* ``tts.set_lang()`` — Definit la langue de sortie pour la synthese vocale.

  - ``en-US`` (par defaut)
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` — Convertit le texte en parole et le joue immediatement.


----

Depannage
-------------------

* **Pas de son lors de l'execution d'Espeak ou Pico2Wave**

  * Verifiez que vos enceintes/casque sont branches et que le volume n'est pas coupe.
  * Effectuez un test rapide dans le terminal :

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  Si vous n'entendez rien, le probleme vient de la sortie audio, pas de votre code Python.

* **La voix d'Espeak semble trop rapide ou trop robotique**

  * Essayez d'ajuster les parametres dans votre code :

    .. code-block:: python

       tts.set_speed(120)   # plus lent
       tts.set_pitch(60)    # hauteur differente

* **Permission refusee lors de l'execution du code**

  * Essayez d'executer avec ``sudo`` :

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

Comparaison : Espeak vs Pico2Wave
-------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Fonctionnalite
     - Espeak
     - Pico2Wave
   * - Qualite vocale
     - Robotique, synthetique
     - Plus naturelle, humaine
   * - Langues
     - Anglais par defaut
     - Moins, mais les courantes
   * - Reglages
     - Oui (vitesse, hauteur, etc.)
     - Non (langue uniquement)
   * - Performances
     - Tres rapide, leger
     - Legerement plus lent, plus lourd