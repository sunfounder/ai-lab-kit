.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _tts_piper_openai:

2. TTS con Piper y OpenAI
========================================================

En la lección anterior, exploramos **Espeak** y **Pico2Wave**, dos motores TTS offline simples en Raspberry Pi.
Ahora, demos un gran paso adelante y probemos dos **opciones TTS más avanzadas** que ofrecen **mayor calidad de voz** y más flexibilidad:

* **Piper** — un motor TTS rápido basado en redes neuronales que funciona **completamente offline** en Raspberry Pi.
* **OpenAI TTS** — un servicio online que proporciona voces **muy naturales y humanas**, perfecto para un habla expresiva.

Estos motores harán que tu Fusion HAT+ suene más realista y vivo.

----

.. _test_piper:

1. Probando Piper
------------------

Piper es un **motor TTS neuronal offline**, lo que significa que no necesitas conexión a internet una vez instalado el modelo.
Soporta múltiples **idiomas** y **voces**, lo que lo convierte en una opción potente para el habla integrada.

**Ejecutar el programa**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 tts_piper.py

* La primera vez que lo ejecutes, el **modelo de voz** seleccionado se descargará automáticamente.
* Luego deberías escuchar al Fusion HAT+ decir: ``Hello! I'm Piper TTS.``
* Puedes cambiar de voz o idioma llamando a ``set_model()`` con un nombre de modelo diferente.

**Código**

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

**Explicación del código:**

* ``available_countrys()`` — Lista todos los idiomas compatibles.
* ``available_models()`` — Lista los modelos disponibles para un idioma específico.
* ``set_model()`` — Establece el modelo de voz. Si el modelo no está instalado, se descargará automáticamente.
* ``say()`` — Convierte texto a voz y lo reproduce inmediatamente.

💡 **Consejo:** Prueba diferentes modelos para comparar velocidad, claridad y acentos. Algunos modelos son más ligeros (más rápidos), mientras que otros tienen mayor fidelidad.

----

2. Probando OpenAI TTS
-------------------------------

**Obtén y guarda tu clave API**

#. Ve a |link_openai_platform| e inicia sesión. En la página de **API keys**, haz clic en **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Completa los detalles (Owner, Name, Project y permisos si es necesario), luego haz clic en **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Una vez creada la clave, cópiala de inmediato — no podrás verla de nuevo. Si la pierdes, deberás generar una nueva.

   .. image:: img/llm_openai_copy.png

#. En tu carpeta del proyecto (por ejemplo: ``/``), crea un archivo llamado ``secret.py``:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Pega tu clave en el archivo así:

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**Ejecutar el programa**

.. code-block:: bash

  cd ~/ai-lab-kit/llm
  sudo python3 tts_openai.py

* El programa se conectará al servicio TTS de OpenAI, y el Fusion HAT+ hablará usando una **salida de voz natural y expresiva**.
* Puedes cambiar **estilos de voz** y añadir **instrucciones** para controlar el tono y la expresión (por ejemplo, triste, dramático, juguetón).
* Esto hace que OpenAI TTS sea ideal para robots interactivos, narración de cuentos o asistentes educativos.


**Código**

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


**Explicación del código:**

* ``OpenAI_TTS()`` — Inicializa el motor TTS de OpenAI usando tu clave API.
* ``set_model()`` — Selecciona el modelo TTS (por ejemplo, ``gpt-4o-mini-tts``).
* ``set_voice()`` — Elige una voz específica (por ejemplo, ``alloy``).
* ``say(text)`` — Convierte el texto a voz y lo reproduce.
* ``say(text, instructions=...)`` — Añade **instrucciones de tono expresivo**, permitiéndote controlar el estilo del habla dinámicamente.

**Ejemplo:**

- "say it sadly" → tono suave y emocional
- "say it dramatically" → entrega audaz y expresiva
- "say it excitedly" → tono entusiasta

----

Solución de problemas
-------------------

* **No module named 'secret'**

  Esto significa que ``secret.py`` no está en la misma carpeta que tu archivo Python.
  Mueve ``secret.py`` al mismo directorio donde ejecutas el script, por ejemplo:

  .. code-block:: bash

     ls ~/
     # Make sure you see both: secret.py and your .py file

* **OpenAI: Invalid API key / 401**

  * Verifica que hayas pegado la clave completa (comienza con ``sk-``) y que no tenga espacios o saltos de línea adicionales.
  * Asegúrate de que tu código la importe correctamente:

    .. code-block:: python

       from secret import OPENAI_API_KEY

  * Confirma el acceso a la red en tu Pi (prueba ``ping api.openai.com``).

* **OpenAI: Quota exceeded / billing error**

  * Es posible que necesites añadir crédito o aumentar la cuota en el panel de OpenAI.
  * Intenta de nuevo después de resolver el problema de la cuenta/facturación.

* **Piper: tts.say() se ejecuta pero no hay sonido**

  * Asegúrate de que un modelo de voz esté realmente presente:

    .. code-block:: bash

       ls ~/.local/share/piper/voices

  * Confirma que el nombre del modelo coincida exactamente en el código:

    .. code-block:: python

       tts.set_model("en_US-amy-low")

  * Verifica el dispositivo/salida de audio y el volumen en tu Pi (``alsamixer``), y que los altavoces estén conectados y encendidos.

* **ALSA / errores de dispositivo de sonido (por ejemplo, "Audio device busy" o "No such file or directory")**

  * Cierra otros programas que estén usando audio.
  * Reinicia la Pi si el dispositivo permanece ocupado.
  * Para salida HDMI vs. jack de auriculares, selecciona el dispositivo correcto en la configuración de audio de Raspberry Pi OS.

* **Permiso denegado al ejecutar Python**

  * Prueba con ``sudo`` si tu entorno lo requiere:

    .. code-block:: bash

       sudo python3 tts_piper.py

Comparación de Motores TTS
-------------------------

.. list-table:: Comparación de características: Espeak vs Pico2Wave vs Piper vs OpenAI TTS
   :header-rows: 1
   :widths: 18 18 20 22 22

   * - Elemento
     - Espeak
     - Pico2Wave
     - Piper
     - OpenAI TTS
   * - Se ejecuta en
     - Integrado en Raspberry Pi (offline)
     - Integrado en Raspberry Pi (offline)
     - Raspberry Pi / PC (offline, necesita modelo)
     - Nube (online, necesita clave API)
   * - Calidad de voz
     - Robótica
     - Más natural que Espeak
     - Natural (TTS neuronal)
     - Muy natural / similar a humana
   * - Controles
     - Velocidad, tono, volumen
     - Controles limitados
     - Elegir diferentes voces/modelos
     - Elegir modelo y voces
   * - Idiomas
     - Muchos (la calidad varía)
     - Conjunto limitado
     - Muchas voces/idiomas disponibles
     - Mejor en inglés (otros varían según disponibilidad)
   * - Latencia / velocidad
     - Muy rápido
     - Rápido
     - Tiempo real en Pi 4/5 con modelos "low"
     - Dependiente de la red (generalmente baja latencia)
   * - Configuración
     - Mínima
     - Mínima
     - Descargar modelos ``.onnx`` + ``.onnx.json``
     - Crear clave API, instalar cliente
   * - Mejor para
     - Pruebas rápidas, indicaciones básicas
     - Voz offline ligeramente mejor
     - Proyectos locales con mejor calidad
     - Máxima calidad, opciones de voz variadas