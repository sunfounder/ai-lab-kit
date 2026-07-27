.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ai_voice_assistant_car:

7. Asistente de Voz IA
===========================

Esta lección convierte tu Fusion HAT+ en un **asistente de IA basado en voz**.
Con el código proporcionado, el robot: **esperará una palabra de activación**, **transcribirá tu voz** con Vosk, la enviará a un **LLM de OpenAI** y **responderá hablando** usando Piper TTS.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Voice_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

----

Antes de comenzar
----------------

Asegúrate de tener:

* :ref:`test_piper` — La voz de Piper funciona (por ejemplo, puedes reproducir "Hello").
* :ref:`test_vosk` — Vosk STT funciona para tu idioma (por ejemplo, ``en-us``).
* :ref:`py_online_llm` — Tu **clave API de OpenAI** guardada en ``secret.py`` como ``OPENAI_API_KEY``.
* Un **micrófono** y **altavoz** funcionando en Fusion HAT+.
* Una conexión de red estable (el LLM es online).

----

Ejecutar el Ejemplo
---------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm/
   sudo python3 voice_assistant.py

**Configuración utilizada por el código:**

* LLM: **OpenAI** (``gpt-4o-mini``)
* TTS: **Piper** (``en_US-ryan-low``)
* STT: **Vosk** (``en-us``)
* Palabra de activación: ``"hey buddy"``
* Entrada por teclado: **habilitada** (entrada manual opcional)
* Modo imagen: **habilitado** (``WITH_IMAGE=True``) — requiere un LLM multimodal si decides usar imágenes después

**Qué sucede:**

1. El asistente muestra un mensaje de bienvenida con la frase de activación.
2. Escucha **"hey buddy"**.
3. Después de la activación, tu voz se transcribe (Vosk → texto).
4. El texto se envía a **OpenAI (gpt-4o-mini)** para obtener una respuesta.
5. La respuesta se pronuncia con **Piper** (``en_US-ryan-low``).

**Ejemplo de interacción**

.. code-block:: text

   You: Hey Buddy
   Robot: Hi there!

   You: What's the capital of Italy?
   Robot: The capital of Italy is Rome.

Código
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

**Explicación del código:**

* ``OpenAI(..., model="gpt-4o-mini")`` — Usa **OpenAI** como el único LLM en esta lección.
* ``NAME`` / ``WAKE_WORD`` — Personaliza el asistente ("Buddy", "hey buddy").
* ``WITH_IMAGE=True`` — Habilita el modo imagen en el asistente (no se incluye lógica de E/S de imágenes aquí).
* ``TTS_MODEL="en_US-ryan-low"`` — Voz de Piper utilizada para las respuestas.
* ``STT_LANGUAGE="en-us"`` — Idioma de Vosk para el reconocimiento.
* ``KEYBOARD_ENABLE=True`` — Permite la entrada de texto manual opcional durante la depuración.
* ``WELCOME`` / ``INSTRUCTIONS`` — Mensaje de inicio y personalidad del asistente/prompt del sistema.
* ``va.run()`` — Inicia el bucle: **activación → escuchar → LLM → hablar**.


Cambiar a Otros LLMs o TTS
------------------------------

Puedes cambiar fácilmente a otros LLMs, TTS o idiomas de STT con solo unas pocas modificaciones:

* LLMs compatibles:

  * OpenAI
  * Doubao
  * Deepseek
  * Gemini
  * Qwen
  * Grok

* :ref:`test_piper` — Verifica los idiomas compatibles de **Piper TTS**.
* :ref:`test_vosk` — Verifica los idiomas compatibles de **Vosk STT**.

Para cambiar, simplemente modifica la parte de inicialización en el código:

.. code-block:: python

   from fusion_hat.llm import Gemini as LLM
   llm = LLM(api_key="YOUR_KEY", model="gemini-pro")

   # Set models and languages
   TTS_MODEL = "en_US-ryan-low"
   STT_LANGUAGE = "en-us"



----

Solución de problemas
-----------------------------

* **El robot no responde a la palabra de activación**

  - Verifica si el micrófono funciona.
  - Asegúrate de que ``WAKE_ENABLE = True``.
  - Ajusta la palabra de activación para que coincida con tu pronunciación.
  - Reduce el ruido de fondo y habla claramente.

* **No hay sonido del altavoz**

  - Verifica el nombre del modelo TTS (por ejemplo, ``en_US-ryan-low``).
  - Prueba Piper o Espeak manualmente.
  - Verifica la conexión del altavoz y el volumen.

* **Error de clave API o tiempo de espera**

  - Verifica tu clave en ``secret.py``.
  - Asegúrate de que tu conexión de red sea estable.
  - Confirma que el modelo LLM sea compatible (por ejemplo, ``gpt-4o-mini``).

* **La palabra de activación funciona pero no hay respuesta**

  - Verifica si el idioma de STT coincide con tu acento.
  - Asegúrate de que el modelo se haya descargado correctamente.
  - Intenta imprimir registros de depuración para confirmar que STT se está ejecutando.

* **TTS funciona pero no hay respuesta del LLM**

  - Verifica si la clave API es válida.
  - Verifica el nombre del modelo y la configuración del LLM.
  - Asegúrate de la conectividad a internet.