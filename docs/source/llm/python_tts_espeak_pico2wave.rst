.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. TTS con Espeak e Pico2Wave
=================================================

In questa lezione, useremo due motori di sintesi vocale (TTS) integrati su Raspberry Pi -- **Espeak** e **Pico2Wave** -- per far parlare il Fusion HAT+.

Questi due motori sono entrambi semplici e funzionano offline, ma suonano in modo molto diverso:

* **Espeak**: molto leggero e veloce, ma la voce e' robotica. Puoi regolare velocita', tonalita' e volume.
* **Pico2Wave**: produce una voce piu' fluida e naturale rispetto a Espeak, ma ha meno opzioni configurabili.

Sentirai la differenza nella **qualita' della voce** e nelle **funzionalita'**.

----

1. Test di Espeak
--------------------

Espeak e' un motore TTS leggero incluso in Raspberry Pi OS.
La sua voce suona robotica, ma e' altamente configurabile: puoi regolare volume, tonalita', velocita' e altro.

**Esegui il programma**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * Dovresti sentire il Fusion HAT+ dire: "Hello! I'm Espeak TTS."
  * Prova a cambiare i parametri di regolazione nel codice per sperimentare come ``amp``, ``speed``, ``gap`` e ``pitch`` influenzano il suono.

**Codice**

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

**Spiegazione del codice:**

* ``tts.set_amp()`` -- Controlla il volume (0-200).
* ``tts.set_speed()`` -- Regola la velocita' di pronuncia (80-260).
* ``tts.set_gap()`` -- Imposta lo spazio tra le parole (0-200).
* ``tts.set_pitch()`` -- Imposta la tonalita' (0-99).
* ``tts.say()`` -- Converte il testo in parlato e lo riproduce.

Suggerimento: Prova ad aumentare tonalita' e velocita' per far sembrare il robot allegro, o abbassarle per farlo sembrare serio.

----


2. Test di Pico2Wave
---------------------

Pico2Wave produce una voce **piu' naturale e simile a quella umana** rispetto a Espeak.
E' molto facile da usare, ma meno flessibile -- puoi solo **cambiare la lingua**, non la tonalita', la velocita' o il volume.
Questo rende Pico2Wave un'ottima scelta quando desideri un parlato chiaro e fluido senza troppa configurazione.

**Esegui il programma**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* Dovresti sentire il Fusion HAT+ dire: "Hello! I'm Pico2Wave TTS."
* Prova a cambiare la lingua (ad esempio, ``es-ES`` per spagnolo) e ascolta come cambia la voce.

**Codice**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**Spiegazione del codice:**

* ``tts.set_lang()`` -- Imposta la lingua di output per la sintesi vocale.

  - ``en-US`` (predefinito)
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` -- Converte il testo in parlato e lo riproduce immediatamente.


----

Risoluzione dei Problemi
-------------------------

* **Nessun suono durante l'esecuzione di Espeak o Pico2Wave**

  * Controlla che gli altoparlanti/cuffie siano collegati e il volume non sia muto.
  * Esegui un rapido test nel terminale:

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  Se non senti nulla, il problema e' l'uscita audio, non il tuo codice Python.

* **La voce di Espeak suona troppo veloce o troppo robotica**

  * Prova a regolare i parametri nel tuo codice:

    .. code-block:: python

       tts.set_speed(120)   # piu' lento
       tts.set_pitch(60)    # diversa tonalita'

* **Permesso negato durante l'esecuzione del codice**

  * Prova a eseguire con ``sudo``:

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

Confronto: Espeak vs Pico2Wave
-------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Caratteristica
     - Espeak
     - Pico2Wave
   * - Qualita' voce
     - Robotica, sintetica
     - Piu' naturale, simile a umana
   * - Lingue
     - Inglese predefinito
     - Meno, ma comuni
   * - Regolabile
     - Si' (velocita', tonalita', ecc.)
     - No (solo lingua)
   * - Prestazioni
     - Molto veloce, leggero
     - Leggermente piu' lento, piu' pesante
