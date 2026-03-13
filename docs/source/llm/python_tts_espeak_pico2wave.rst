.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. TTS mit Espeak und Pico2Wave
=================================================

In dieser Lektion verwenden wir zwei integrierte Text-to-Speech-Engines (TTS) auf dem Raspberry Pi — **Espeak** und **Pico2Wave** — um den Fusion HAT+ sprechen zu lassen.  

Diese beiden Engines sind einfach zu verwenden und laufen vollständig offline, klingen jedoch deutlich unterschiedlich:

* **Espeak**: sehr leichtgewichtig und schnell, aber die Stimme klingt eher robotisch. Geschwindigkeit, Tonhöhe und Lautstärke lassen sich anpassen.  
* **Pico2Wave**: erzeugt eine weichere und natürlichere Stimme als Espeak, bietet jedoch weniger Konfigurationsmöglichkeiten.  

Sie werden den Unterschied sowohl in der **Sprachqualität** als auch in den **Funktionen** hören.  

----

1. Espeak testen
--------------------

Espeak ist eine leichtgewichtige TTS-Engine, die bereits im Raspberry Pi OS enthalten ist.  
Die Stimme klingt zwar robotisch, ist jedoch sehr gut konfigurierbar: Sie können Lautstärke, Tonhöhe, Geschwindigkeit und mehr anpassen.  

**Programm ausführen**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * Sie sollten hören, wie der Fusion HAT+ sagt: „Hello! I'm Espeak TTS.“
  * Versuchen Sie, die Parameter im Code zu verändern, um zu sehen, wie ``amp``, ``speed``, ``gap`` und ``pitch`` den Klang beeinflussen.

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

  tts.say("Hello! I’m Espeak TTS.")

**Code-Erklärung:**

* ``tts.set_amp()`` — Steuert die Lautstärke (0–200).  
* ``tts.set_speed()`` — Passt die Sprechgeschwindigkeit an (80–260).  
* ``tts.set_gap()`` — Legt den Abstand zwischen Wörtern fest (0–200).  
* ``tts.set_pitch()`` — Legt die Tonhöhe fest (0–99).  
* ``tts.say()`` — Wandelt Text in Sprache um und gibt ihn wieder.

💡 **Tipp:** Versuchen Sie, Tonhöhe und Geschwindigkeit zu erhöhen, um den Roboter fröhlicher klingen zu lassen, oder sie zu senken, um eine ernstere Stimme zu erzeugen.

----


2. Pico2Wave testen
---------------------

Pico2Wave erzeugt im Vergleich zu Espeak eine **natürlichere und menschenähnlichere Stimme**.  
Es ist sehr einfach zu verwenden, aber weniger flexibel — Sie können **nur die Sprache ändern**, nicht jedoch Tonhöhe, Geschwindigkeit oder Lautstärke.  
Dadurch eignet sich Pico2Wave hervorragend, wenn Sie eine klare und flüssige Sprachausgabe ohne viele Einstellungen benötigen.

**Programm ausführen**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* Sie sollten hören, wie der Fusion HAT+ sagt: „Hello! I'm Pico2Wave TTS.“  
* Versuchen Sie, die Sprache zu ändern (zum Beispiel ``es-ES`` für Spanisch) und hören Sie, wie sich die Stimme verändert.  

**Code**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT
  
  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**Code explanation:**

* ``tts.set_lang()`` — Legt die Ausgabesprache für die Sprachsynthese fest.

  - ``en-US`` (Standard)
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` — Wandelt den Text in Sprache um und spielt ihn sofort ab.  


----

Troubleshooting
-------------------

* **Kein Ton beim Ausführen von Espeak oder Pico2Wave**

  * Prüfen Sie, ob Lautsprecher oder Kopfhörer angeschlossen sind und die Lautstärke nicht stummgeschaltet ist.  
  * Führen Sie einen kurzen Test im Terminal aus:

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  Wenn Sie nichts hören, liegt das Problem an der Audioausgabe und nicht am Python-Code.

* **Die Espeak-Stimme klingt zu schnell oder zu robotisch**

  * Versuchen Sie, die Parameter im Code anzupassen:

    .. code-block:: python

       tts.set_speed(120)   # langsamer
       tts.set_pitch(60)    # andere Tonhöhe

* **Permission denied beim Ausführen des Codes**

  * Versuchen Sie, das Programm mit ``sudo`` auszuführen:

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

Comparison: Espeak vs Pico2Wave
-------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Feature
     - Espeak
     - Pico2Wave
   * - Voice quality
     - Robotisch, synthetisch
     - Natürlicher, menschenähnlicher
   * - Languages
     - Standardmäßig Englisch
     - Weniger, aber gängige Sprachen
   * - Adjustable
     - Ja (Geschwindigkeit, Tonhöhe usw.)
     - Nein (nur Sprache)
   * - Performance
     - Sehr schnell, leichtgewichtig
     - Etwas langsamer, schwerer