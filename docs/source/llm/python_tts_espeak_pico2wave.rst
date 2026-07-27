.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. TTS con Espeak y Pico2Wave
=================================================

En esta lección, usaremos dos motores de text-to-speech (TTS) integrados en Raspberry Pi — **Espeak** y **Pico2Wave** — para hacer que el Fusion HAT+ hable.

Estos dos motores son simples y funcionan sin conexión, pero suenan bastante diferentes:

* **Espeak**: muy ligero y rápido, pero la voz es robótica. Puedes ajustar la velocidad, el tono y el volumen.
* **Pico2Wave**: produce una voz más suave y natural que Espeak, pero tiene menos opciones de configuración.

Escucharás la diferencia en **calidad de voz** y **características**.

----

1. Probando Espeak
--------------------

Espeak es un motor TTS ligero incluido en Raspberry Pi OS.
Su voz suena robótica, pero es altamente configurable: puedes ajustar volumen, tono, velocidad y más.

**Ejecutar el programa**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * Deberías escuchar al Fusion HAT+ decir: "Hello! I'm Espeak TTS."
  * Intenta cambiar los parámetros de ajuste en el código para experimentar cómo afectan ``amp``, ``speed``, ``gap`` y ``pitch`` al sonido.

**Código**

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

**Explicación del código:**

* ``tts.set_amp()`` — Controla el volumen (0–200).
* ``tts.set_speed()`` — Ajusta la velocidad del habla (80–260).
* ``tts.set_gap()`` — Establece el espacio entre palabras (0–200).
* ``tts.set_pitch()`` — Define el tono (0–99).
* ``tts.say()`` — Convierte texto a voz y lo reproduce.

💡 **Consejo:** Intenta aumentar el tono y la velocidad para que el robot suene alegre, o reducirlos para que suene serio.

----


2. Probando Pico2Wave
---------------------

Pico2Wave produce una voz **más natural y humana** en comparación con Espeak.
Es muy fácil de usar, pero menos flexible — solo puedes **cambiar el idioma**, no el tono, la velocidad ni el volumen.
Esto hace que Pico2Wave sea una excelente elección cuando quieres un habla clara y suave sin demasiada configuración.

**Ejecutar el programa**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* Deberías escuchar al Fusion HAT+ decir: "Hello! I'm Pico2Wave TTS."
* Intenta cambiar el idioma (por ejemplo, ``es-ES`` para español) y escucha cómo cambia la voz.

**Código**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**Explicación del código:**

* ``tts.set_lang()`` — Establece el idioma de salida para la síntesis de voz.

  - ``en-US`` (predeterminado)
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` — Convierte el texto a voz y lo reproduce inmediatamente.


----

Solución de problemas
-------------------

* **Sin sonido al ejecutar Espeak o Pico2Wave**

  * Verifica que tus altavoces/auriculares estén conectados y el volumen no esté silenciado.
  * Ejecuta una prueba rápida en la terminal:

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  Si no escuchas nada, el problema está en la salida de audio, no en tu código Python.

* **La voz de Espeak suena demasiado rápida o robótica**

  * Intenta ajustar los parámetros en tu código:

    .. code-block:: python

       tts.set_speed(120)   # más lento
       tts.set_pitch(60)    # diferente tono

* **Permiso denegado al ejecutar el código**

  * Intenta ejecutar con ``sudo``:

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

Comparación: Espeak vs Pico2Wave
-------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Característica
     - Espeak
     - Pico2Wave
   * - Calidad de voz
     - Robótica, sintética
     - Más natural, similar a humana
   * - Idiomas
     - Inglés predeterminado
     - Menos, pero los comunes
   * - Ajustable
     - Sí (velocidad, tono, etc.)
     - No (solo idioma)
   * - Rendimiento
     - Muy rápido, ligero
     - Ligeramente más lento, más pesado