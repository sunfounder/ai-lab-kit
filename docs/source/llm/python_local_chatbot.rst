.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. Chatbot de Voz Local
===========================

En esta lección, combinarás todo lo que has aprendido — **reconocimiento de voz (STT)**,
**text-to-speech (TTS)** y un **LLM local (Ollama)** — para construir un **chatbot de voz**
completamente offline que se ejecuta en tu Fusion HAT+.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Local_Voice_Chatbot.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

El flujo de trabajo es simple:

#. **Escuchar** — El micrófono captura tu voz y la transcribe con **Vosk**.
#. **Pensar** — El texto se envía a un **LLM** local ejecutándose en Ollama (por ejemplo, ``llama3.2:3b``).
#. **Hablar** — El chatbot responde en voz alta usando **Piper TTS**.

Esto crea un **robot conversacional manos libres** que puede entender y responder en tiempo real.

----

Antes de comenzar
----------------

Asegúrate de haber preparado lo siguiente:

* Has probado **Piper TTS** (:ref:`test_piper`) y elegido un modelo de voz que funcione.
* Has probado **Vosk STT** (:ref:`test_vosk`) y elegido el paquete de idioma correcto (por ejemplo, ``en-us``).
* Has instalado **Ollama** (:ref:`download_ollama`) en tu Pi u otro ordenador, y descargado un modelo como ``llama3.2:3b`` (o uno más pequeño como ``moondream:1.8b`` si la memoria es limitada).

----

Ejecutar el Código
--------------

#. Abre el script de ejemplo:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano local_voice_chatbot.py

#. Actualiza los parámetros según sea necesario:

   * ``stt = Vosk(language="en-us")``: Cambia esto para que coincida con tu acento/paquete de idioma (por ejemplo, ``en-us``, ``zh-cn``, ``es``).
   * ``tts.set_model("en_US-amy-low")``: Reemplázalo con el modelo de voz de Piper que verificaste en :ref:`test_piper`.
   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``: Actualiza tanto ``ip`` como ``model`` según tu configuración.

     * ``ip``: Si Ollama se ejecuta en la **misma Pi**, usa ``localhost``. Si Ollama se ejecuta en otro ordenador en tu LAN, activa **Expose to network** en Ollama y establece ``ip`` como la IP LAN de ese ordenador.
     * ``model``: Debe coincidir exactamente con el nombre del modelo que descargaste/activaste en Ollama.

#. Ejecuta el script:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo python3 local_voice_chatbot.py

#. Después de ejecutarlo, deberías ver:

   * El bot te saluda con un mensaje de bienvenida hablado.
   * Espera la entrada de voz.
   * Vosk transcribe tu voz a texto.
   * El texto se envía a Ollama, que transmite una respuesta.
   * La respuesta se limpia (eliminando el razonamiento oculto) y Piper la dice en voz alta.
   * Detén el programa en cualquier momento con ``Ctrl+C``.

----

Código
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
               print("\n🎤 Listening... (Press Ctrl+C to stop)")

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

Análisis del Código
-------------

**Importaciones y configuración global**

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

Importa los tres subsistemas que construiste anteriormente:
**Vosk** para speech-to-text (STT), **Ollama** para el LLM, y **Piper** para text-to-speech (TTS).



**Inicializar STT (Vosk)**

.. code-block:: python

   stt = Vosk(language="en-us")

Carga el modelo de Vosk para inglés de EE.UU.
Cambia el código de idioma (por ejemplo, ``zh-cn``, ``es``) para que coincida con tu paquete de voz y obtener mejor precisión.



**Inicializar TTS (Piper)**

.. code-block:: python

   tts = Piper()
   tts.set_model("en_US-amy-low")

Crea un motor Piper y selecciona una voz específica.
Elige un modelo que hayas probado en :ref:`test_piper`. Las voces de menor calidad son más rápidas y usan menos CPU.



**Instrucciones del LLM y mensaje de bienvenida**

.. code-block:: python

   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

Dos decisiones clave de experiencia de usuario:

* Mantén las **respuestas cortas y directas** (ayuda con la claridad del TTS).
* Prohíbe explícitamente las etiquetas ocultas de "cadena de pensamiento" para reducir salidas ruidosas.



**Conectar a Ollama y establecer el alcance de la conversación**

.. code-block:: python

   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

* ``ip="localhost"`` asume que el servidor Ollama se ejecuta en la misma Pi. Si se ejecuta en otra máquina de la LAN, pon la **IP LAN** de ese ordenador y activa *Expose to network* en Ollama.
* ``set_max_messages(20)`` mantiene un historial conversacional corto. Reduce este valor si la memoria/latencia es ajustada.

**Eliminar razonamiento/etiquetas ocultas antes de hablar**

.. code-block:: python

   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

Algunos modelos pueden emitir etiquetas de estilo interno (por ejemplo, ``<think>...``).
Esta función las elimina para que tu TTS **solo** pronuncie la respuesta final.

**Consejo:** Si ves otros artefactos en pantalla (porque transmites tokens sin procesar), esta función ya asegura que la **salida hablada** se mantenga limpia.

**Bucle principal: saludar una vez, luego escuchar → pensar → hablar**

.. code-block:: python

   print(WELCOME)
   tts.say(WELCOME)

Saluda al usuario a través de la terminal y el altavoz. Ocurre una vez al inicio.

**Escuchar (STT en streaming con resultados parciales en vivo)**

.. code-block:: python

   print("\n🎤 Listening... (Press Ctrl+C to stop)")

   text = ""
   for result in stt.listen(stream=True):
       if result["done"]:
           text = result["final"].strip()
           print(f"[YOU] {text}")
       else:
           print(f"[YOU] {result['partial']}", end="\r", flush=True)

* ``stream=True`` produce transcripciones **parciales** para retroalimentación inmediata y una transcripción **final** cuando termina el enunciado.
* El texto final reconocido se almacena en ``text`` y se imprime una vez.

**Guardia:** Si no se reconoció nada, se omite la llamada al LLM:

.. code-block:: python

   if not text:
       print("[INFO] Nothing recognized. Try again.")
       time.sleep(0.1)
       continue

Esto evita enviar indicaciones vacías al modelo (ahorra tiempo y tokens).

**Pensar (LLM) con impresión en streaming**

.. code-block:: python

   reply_accum = ""
   response = llm.prompt(text, stream=True)
   for next_word in response:
       if next_word:
           print(next_word, end="", flush=True)
           reply_accum += next_word
   print("")

* Envía la transcripción final al LLM local e **imprime los tokens a medida que llegan** para baja latencia.
* Mientras tanto, acumulas la respuesta completa en ``reply_accum`` para el post-procesamiento.

**Nota:** Si prefieres **no** mostrar los tokens sin procesar, establece ``stream=False`` y simplemente imprime la cadena final.

**Hablar (limpiar primero, luego TTS una vez)**

.. code-block:: python

   clean = strip_thinking(reply_accum)
   if clean:
       tts.say(clean)
   else:
       tts.say("Sorry, I didn't catch that.")

* Limpia el texto final para eliminar etiquetas ocultas, luego **habla exactamente una vez**.
* Mantener el TTS en una sola pasada evita indicaciones repetidas como "[LLM] / [SAY]".


**Salida y finalización**

.. code-block:: python

   except KeyboardInterrupt:
       print("\n[INFO] Stopping...")
   finally:
       tts.say("Goodbye!")
       print("Bye.")

Usa **Ctrl+C** para detener. El bot dice un breve adiós para señalar una salida limpia.


----

Solución de problemas y preguntas frecuentes
---------------------

* **El modelo es demasiado grande (error de memoria)**

  Usa un modelo más pequeño como ``moondream:1.8b`` o ejecuta Ollama en un ordenador más potente.

* **Sin respuesta de Ollama**

  Asegúrate de que Ollama se esté ejecutando (``ollama serve`` o la aplicación de escritorio abierta). Si es remoto, activa **Expose to network** y verifica la dirección IP.

* **Vosk no reconoce el habla**

  Verifica que tu micrófono funcione. Prueba otro paquete de idioma (``zh-cn``, ``es``, etc.) si es necesario.

* **Piper silencioso o errores**

  Confirma que el modelo de voz elegido esté descargado y probado en :ref:`test_piper`.

* **Respuestas demasiado largas o fuera de tema**

  Edita ``INSTRUCTIONS`` para añadir: **"Keep answers short and to the point."**