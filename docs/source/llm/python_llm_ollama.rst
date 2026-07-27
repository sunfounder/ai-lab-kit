.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Visión y Texto con Ollama
================================

En esta lección, aprenderás a usar **Ollama**, una herramienta para ejecutar modelos de lenguaje grande y visión localmente.
Te mostraremos cómo instalar Ollama, descargar un modelo y conectar Fusion HAT+ a él.

Con esta configuración, Fusion HAT+ puede tomar una foto con la cámara y el modelo **verá y dirá** —
puedes hacer cualquier pregunta sobre la imagen, y el modelo responderá en lenguaje natural.

.. _download_ollama:

1. Instalar Ollama (LLM) y Descargar Modelo
-------------------------------------------------

Puedes elegir dónde instalar **Ollama**:

* En tu Raspberry Pi (ejecución local)
* O en otro ordenador (Mac/Windows/Linux) en la **misma red local**

**Modelos recomendados según el hardware**

Puedes elegir cualquier modelo disponible en |link_ollama_hub|.
Los modelos vienen en diferentes tamaños (3B, 7B, 13B, 70B...).
Los modelos más pequeños se ejecutan más rápido y requieren menos memoria, mientras que los modelos más grandes ofrecen mejor calidad pero necesitan hardware potente.

Consulta la tabla a continuación para decidir qué tamaño de modelo se adapta a tu dispositivo.

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - Tamaño del modelo
     - RAM Mínima Requerida
     - Hardware Recomendado
   * - ~3B parámetros
     - 8GB (16GB mejor)
     - Raspberry Pi 5 (16GB) o PC/Mac de gama media
   * - ~7B parámetros
     - 16GB+
     - Pi 5 (16GB, apenas usable) o PC/Mac de gama media
   * - ~13B parámetros
     - 32GB+
     - PC de escritorio / Mac con mucha RAM
   * - 30B+ parámetros
     - 64GB+
     - Estación de trabajo / Servidor / GPU recomendado
   * - 70B+ parámetros
     - 128GB+
     - Servidor de alta gama con múltiples GPUs

**Instalar en Raspberry Pi**

Si quieres ejecutar Ollama directamente en tu Raspberry Pi:

* Usa un **Raspberry Pi OS de 64 bits**
* Muy recomendado: **Raspberry Pi 5 (16GB RAM)**

Ejecuta los siguientes comandos:

.. code-block:: bash

   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull a lightweight model (good for testing)
   ollama pull llama3.2:3b

   # Quick run test (type 'hi' and press Enter)
   ollama run llama3.2:3b

   # Serve the API (default port 11434)
   # Tip: set OLLAMA_HOST=0.0.0.0 to allow access from LAN
   OLLAMA_HOST=0.0.0.0 ollama serve

**Instalar en Mac / Windows / Linux (Aplicación de escritorio)**

1. Descarga e instala Ollama desde |link_ollama|

   .. image:: img/llm_ollama_download.png

2. Abre la aplicación Ollama, ve al **Model Selector** y usa la barra de búsqueda para encontrar un modelo. Por ejemplo, escribe ``llama3.2:3b`` (un modelo pequeño y ligero para empezar).

   .. image:: img/llm_ollama_choose.png

3. Después de que la descarga se complete, escribe algo simple como "Hi" en la ventana de chat. Ollama comenzará a descargarlo automáticamente cuando lo uses por primera vez.

   .. image:: img/llm_olama_llama_download.png

4. Ve a **Settings** → activa **Expose Ollama to the network**. Esto permite que tu Raspberry Pi se conecte a través de la LAN.

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   Si ves un error como:

   ``Error: model requires more system memory ...``

   El modelo es demasiado grande para tu máquina.
   Usa un **modelo más pequeño** o cambia a un ordenador con más RAM.

2. Probar Ollama
--------------

Una vez que Ollama esté instalado y tu modelo esté listo, puedes probarlo rápidamente con un bucle de chat mínimo.

**Establecer dirección IP**

#. Abre el script de ejemplo:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. Actualiza los parámetros según sea necesario:

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``: Actualiza tanto ``ip`` como ``model`` según tu configuración.

     * ``ip``: Si Ollama se ejecuta en la **misma Pi**, usa ``localhost``. Si Ollama se ejecuta en otro ordenador en tu LAN, activa **Expose to network** en Ollama y establece ``ip`` como la IP LAN de ese ordenador.
     * ``model``: Debe coincidir exactamente con el nombre del modelo que descargaste/activaste en Ollama.


**Ejecutar el programa**

  .. code-block:: bash

      cd ~/ai-lab-kit/llm
      sudo python3 llm_ollama.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

   * Puedes elegir **cualquier modelo** disponible en |link_ollama_hub|, pero se recomiendan modelos más pequeños (por ejemplo, ``moondream:1.8b``, ``phi3:mini``) si solo tienes 8–16GB de RAM.
   * Asegúrate de que el modelo que especificas en el código coincida con el modelo que ya has descargado en Ollama.
   * Escribe ``exit`` o ``quit`` para detener el programa.
   * Si no puedes conectarte, asegúrate de que Ollama esté ejecutándose y que ambos dispositivos estén en la misma LAN si estás usando un host remoto.

**Código**

.. code-block:: python

   from fusion_hat.llm import Ollama

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   # Change this to your computer IP, if you run it on your pi, then change it to localhost
   llm = Ollama(
      ip="localhost",
      model="llama3.2:3b"
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Response without stream
      # response = llm.prompt(input_text)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


3. Visión con Ollama
--------------------------

En esta demo, la cámara de la Pi toma una foto **cada vez que escribes una pregunta**.
El programa envía **tu texto escrito + la nueva foto** a un modelo de visión local a través de Ollama,
y luego transmite la respuesta del modelo en texto plano.
Esta es una base mínima de "ver y contar" que puedes ampliar luego con comprobaciones de color/rostro/QR.

**Antes de comenzar**

#. Abre la aplicación **Ollama** (o ejecuta el servicio) y asegúrate de tener un **modelo con capacidad de visión** descargado.

   * Si tienes suficiente memoria (≥16GB RAM), puedes probar ``llava:7b``.
   * Si solo tienes **8GB RAM**, prefiere un modelo más pequeño como ``moondream:1.8b`` o ``granite3.2-vision:2b``.

   .. image:: img/llm_ollama_image_model.png

**Ejecutar la Demo**

#. Ve a la carpeta de ejemplos y ejecuta el script:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. Qué sucede cuando se ejecuta:

   * El programa imprime una línea de bienvenida y espera tu entrada (``>>>``).
   * **Cada vez que escribes algo** (por ejemplo, "hello", "Is there yellow?", "Any faces?", "What is on the desk?"), ocurre lo siguiente:

     * **captura una foto** desde la cámara de la Pi (guardada en ``/tmp/llm-img.jpg``),
     * **envía tu texto + la foto** al modelo de visión a través de Ollama,
     * **transmite de vuelta** la respuesta del modelo a la terminal.

   * Escribe ``exit`` o ``quit`` para finalizar el programa.

**Código**

.. code-block:: python

   from fusion_hat.llm import Ollama
   from picamera2 import Picamera2
   import time

   '''
   You need to setup ollama first, see llm_local.py

   You need at leaset 8GB RAM to run llava:7b large multimodal model
   '''

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   llm = Ollama(
      ip="localhost",          # e.g., "192.168.100.145" if remote
      model="llava:7b"         # change to "moondream:1.8b" or "granite3.2-vision:2b" for 8GB RAM
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   # Init camera
   camera = Picamera2()
   config = camera.create_still_configuration(
      main={"size": (1280, 720)},
   )
   camera.configure(config)
   camera.start()
   time.sleep(2)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Capture image
      img_path = '/tmp/llm-img.jpg'
      camera.capture_file(img_path)

      # Response without stream
      # response = llm.prompt(input_text, image_path=img_path)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True, image_path=img_path)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


Solución de problemas
---------------


* **Recibo un error como: `model requires more system memory ...`.**

  * Esto significa que el modelo es demasiado grande para tu dispositivo.
  * Usa un modelo más pequeño como ``moondream:1.8b`` o ``granite3.2-vision:2b``.
  * O cambia a una máquina con más RAM y expón Ollama a la red.

* **El código no puede conectarse a Ollama (connection refused).**

  Verifica lo siguiente:

  * Asegúrate de que Ollama se esté ejecutando (``ollama serve`` o la aplicación de escritorio está abierta).
  * Si usas un ordenador remoto, activa **Expose to network** en la configuración de Ollama.
  * Vuelve a verificar que ``ip="..."`` en tu código coincida con la IP LAN correcta.
  * Confirma que ambos dispositivos estén en la misma red local.

* **Mi cámara Pi no captura nada.**

  * Verifica que ``Picamera2`` esté instalado y funcionando con un script de prueba simple.
  * Comprueba que el cable de la cámara esté correctamente conectado y habilitado en ``raspi-config``.
  * Asegúrate de que tu script tenga permiso para escribir en la ruta de destino (``/tmp/llm-img.jpg``).

* **La salida es demasiado lenta.**

  * Los modelos más pequeños responden más rápido, pero con respuestas más simples.
  * Puedes reducir la resolución de la cámara (por ejemplo, 640×480 en lugar de 1280×720) para acelerar el procesamiento de imágenes.
  * Cierra otros programas en tu Pi para liberar CPU y RAM.