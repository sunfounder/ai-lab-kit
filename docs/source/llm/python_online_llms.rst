.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. Conectándose a LLMs Online
================================

En esta lección, aprenderemos a conectar tu Fusion HAT+ (o Raspberry Pi) a diferentes **Modelos de Lenguaje Grande (LLMs) online**.
Cada proveedor requiere una clave API y ofrece diferentes modelos entre los que puedes elegir.

Cubriremos cómo:

* Crear y guardar tus claves API de forma segura.
* Elegir un modelo que se adapte a tus necesidades.
* Ejecutar nuestro código de ejemplo para chatear con los modelos.

Vamos paso a paso con cada proveedor.

----

OpenAI
----------

OpenAI proporciona modelos potentes como **GPT-4o** y **GPT-4.1** que se pueden usar tanto para tareas de texto como de visión.

Aquí te mostramos cómo configurarlo:

.. start_setup_openai

**Obtén y guarda tu clave API**

#. Ve a |link_openai_platform| e inicia sesión. En la página de **API keys**, haz clic en **Create new secret key**.

   .. image:: img/llm_openai_create.png

#. Completa los detalles (Owner, Name, Project y permisos si es necesario), luego haz clic en **Create secret key**.

   .. image:: img/llm_openai_create_confirm.png

#. Una vez creada la clave, cópiala de inmediato — no podrás verla de nuevo. Si la pierdes, necesitarás generar una nueva.

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

**Habilitar facturación y verificar modelos**

#. Antes de usar la clave, ve a la página de **Billing** en tu cuenta de OpenAI, añade tus datos de pago y recarga una pequeña cantidad de crédito.

   .. image:: img/llm_openai_billing.png

#. Luego ve a la página de **Limits** para verificar qué modelos están disponibles para tu cuenta y copia el ID exacto del modelo para usar en tu código.

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**Probar con código de ejemplo**

#. Abre nuestro código de muestra:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``gpt-4o``):

   .. code-block:: python

      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )

   Guarda y sal (``Ctrl+X``, luego ``Y``, luego ``Enter``).

#. Finalmente, ejecuta la prueba:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

----

Gemini
------------------

Gemini es la familia de modelos de IA de Google. Es rápido y excelente para tareas de propósito general.

**Obtén y guarda tu clave API**

#. Inicia sesión en |link_google_ai|, luego ve a la página de API Keys.

   .. image:: img/llm_gemini_get.png

#. Haz clic en el botón **Create API key** en la esquina superior derecha.

   .. image:: img/llm_gemini_create.png

#. Puedes crear una clave para un proyecto existente o uno nuevo.

   .. image:: img/llm_gemini_choose.png

#. Copia la clave API generada.

   .. image:: img/llm_gemini_copy.png

#. En tu carpeta del proyecto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Pega la clave:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**Verificar modelos disponibles**

Ve a la página oficial de |link_gemini_model|, allí verás la lista de modelos, sus IDs exactos de API y para qué caso de uso está optimizado cada uno.

   .. image:: img/llm_gemini_model.png

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``gemini-2.5-flash``):

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. Guarda y ejecuta:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

----

Qwen
------------------

Qwen es una familia de modelos de lenguaje grande y multimodales proporcionada por Alibaba Cloud.
Estos modelos soportan generación de texto, razonamiento y comprensión multimodal (como análisis de imágenes).

**Obtener una clave API**

Para llamar a los modelos Qwen, necesitas una **clave API**.
La mayoría de los usuarios internacionales deben usar la consola **DashScope International (Model Studio)**.
Los usuarios de China continental pueden usar la consola **Bailian (百炼)**.

* **Para usuarios internacionales**

  #. Ve a la página oficial de |link_qwen_inter| en **Alibaba Cloud**.
  #. Inicia sesión o crea una cuenta de **Alibaba Cloud**.
  #. Navega a **Model Studio** (elige la región de Singapur o Pekín).

      * Si aparece un mensaje "Activate Now" en la parte superior de la página, haz clic para activar Model Studio y recibir la cuota gratuita (solo Singapur).
      * La activación es gratuita — solo se te cobrará después de usar tu cuota gratuita.
      * Si no aparece ningún mensaje de activación, el servicio ya está activo.

  #. Ve a la página de **Key Management**. En la pestaña **API Key**, haz clic en **Create API Key**.
  #. Después de crearla, copia tu clave API y guárdala de forma segura.

    .. image:: img/llm_qwen_api_key.png
        :width: 800

  .. note::
     Los usuarios de Hong Kong, Macao y Taiwán también deben elegir la opción **International (Model Studio)**.

* **Para usuarios de China continental**

  Si estás en China continental, puedes usar la consola **Alibaba Cloud Bailian (百炼)**:

  #. Inicia sesión en |link_aliyun| (consola Bailian) y completa la verificación de la cuenta.
  #. Selecciona **Create API Key**. Si aparece un mensaje indicando que los servicios del modelo no están activados, haz clic en **Activate**, acepta los términos y reclama tu cuota gratuita. Después de la activación, el botón **Create API Key** estará habilitado.

     .. image:: img/llm_qwen_aliyun_create.png

  #. Haz clic en **Create API Key** de nuevo, verifica tu cuenta y luego haz clic en **Confirm**.

     .. image:: img/llm_qwen_aliyun_confirm.png

  #. Una vez creada, copia tu clave API.

     .. image:: img/llm_qwen_aliyun_copy.png

**Guardar tu clave API**

#. En tu carpeta del proyecto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Pega tu clave así:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        QWEN_API_KEY = "sk-xxx"

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``qwen-plus``):

   .. code-block:: python

      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model="qwen-plus",
      )

#. Ejecuta con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

Grok (xAI)
------------------
Grok es la IA conversacional de xAI, creada por el equipo de Elon Musk. Puedes conectarte a través de la API de xAI.

**Obtén y guarda tu clave API**

#. Regístrate para obtener una cuenta aquí: |link_grok_ai|. Añade algunos créditos a tu cuenta primero — de lo contrario, la API no funcionará.

#. Ve a la página de API Keys, haz clic en **Create API key**.

   .. image:: img/llm_grok_create.png

#. Ingresa un nombre para la clave, luego haz clic en **Create API key**.

   .. image:: img/llm_grok_name.png

#. Copia la clave generada y guárdala de forma segura.

   .. image:: img/llm_grok_copy.png

#. En tu carpeta del proyecto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Pega tu clave así:

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        GROK_API_KEY = "xai-xxx"

**Verificar modelos disponibles**

Ve a la página Models en la consola de xAI. Aquí puedes ver todos los modelos disponibles para tu equipo, junto con sus IDs exactos de API — usa estos IDs en tu código.

   .. image:: img/llm_grok_model.png

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``grok-4-latest``):

   .. code-block:: python

      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. Ejecuta con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

----

DeepSeek
------------------

DeepSeek es un proveedor chino de LLM que ofrece modelos asequibles y capaces.

**Obtén y guarda tu clave API**

#. Inicia sesión en |link_deepseek|.

#. En el menú superior derecho, selecciona **API Keys → Create API Key**.

   .. image:: img/llm_deepseek_create.png

#. Ingresa un nombre, haz clic en **Create**, luego copia la clave.

   .. image:: img/llm_deepseek_copy.png

#. En tu carpeta del proyecto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Añade tu clave:

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**Habilitar facturación**

Necesitarás recargar tu cuenta primero. Comienza con una cantidad pequeña (como ¥10 RMB).

   .. image:: img/llm_deepseek_chognzhi.png

**Modelos disponibles**

En el momento de escribir esto (2025-09-12), DeepSeek ofrece:

* ``deepseek-chat``
* ``deepseek-reasoner``

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``deepseek-chat``):

   .. code-block:: python

      from fusion_hat.llm import Deepseek
      from secret import DEEPSEEK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Deepseek(
         api_key=DEEPSEEK_API_KEY,
         model="deepseek-chat",
         max_messages=20,
      )

#. Ejecuta:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

----

Doubao
------------------
Doubao es la plataforma de modelos de IA de ByteDance (Volcengine Ark).

**Obtén y guarda tu clave API**

#. Inicia sesión en |link_doubao|.

#. En el menú izquierdo, desplázate hacia abajo hasta **API Key Management → Create API Key**.

   .. image:: img/llm_doubao_create.png

#. Elige un nombre y haz clic en **Create**.

   .. image:: img/llm_doubao_name.png

#. Haz clic en el icono **Show API Key** y cópiala.

   .. image:: img/llm_doubao_copy.png

#. En tu carpeta del proyecto:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Añade tu clave:

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**Elegir un modelo**

#. Ve al marketplace de modelos y elige un modelo.

   .. image:: img/llm_doubao_model_select.png

#. Por ejemplo, elige **Doubao-seed-1.6**, luego haz clic en **API 接入**.

   .. image:: img/llm_doubao_model.png

#. Selecciona tu clave API y haz clic en **Use API**.

   .. image:: img/llm_doubao_use_api.png

#. Haz clic en **Enable Model**.

   .. image:: img/llm_doubao_kaitong.png

#. Pasa el ratón sobre el ID del modelo para copiarlo.

   .. image:: img/llm_doubao_copy_id.png

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. Reemplaza el contenido con el código a continuación, y actualiza ``model="xxx"`` con el modelo que desees (por ejemplo, ``doubao-seed-1-6-250615``):

   .. code-block:: python

      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. Ejecuta con:

   .. code-block:: bash

       sudo python3 llm_test.py

Ahora puedes chatear con Fusion HAT+ directamente desde la terminal.

General
--------------

Este proyecto soporta la conexión a múltiples plataformas LLM a través de una interfaz unificada.
Tenemos compatibilidad integrada con:

* **OpenAI** (ChatGPT / GPT-4o, GPT-4, GPT-3.5)
* **Gemini** (Google AI Studio / Vertex AI)
* **Grok** (xAI)
* **DeepSeek**
* **Qwen (通义千问)**
* **Doubao (豆包)**

Además, puedes conectarte a **cualquier otro servicio LLM que sea compatible con el formato de API de OpenAI**.
Para esas plataformas, necesitarás obtener manualmente tu **clave API** y la **base_url** correcta.

**Obtén y guarda tu clave API**

#. Obtén una **clave API** de la plataforma que quieras usar. (Consulta la consola oficial de cada plataforma para más detalles.)

#. En tu carpeta del proyecto, crea un nuevo archivo:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. Añade tu clave en ``secret.py``:

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   Mantén tu clave API privada. No subas ``secret.py`` a repositorios públicos.

**Probar con código de ejemplo**

#. Abre el archivo de prueba:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. Reemplaza el contenido de un archivo Python con el siguiente ejemplo, y completa la ``base_url`` y el ``model`` correctos para tu plataforma:

   .. note::

      Acerca de ``base_url``:
      Soportamos el **formato de API de OpenAI**, así como cualquier API que sea **compatible** con él.
      Cada proveedor tiene su propia ``base_url``. Consulta su documentación.

   .. code-block:: python

      from fusion_hat.llm import LLM
      from secret import API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = LLM(
         base_url = f"",
         api_key=API_KEY,
         model="",
      )

#. Ejecuta el programa:

   .. code-block:: bash

      sudo python3 llm_others.py