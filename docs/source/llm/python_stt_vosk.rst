.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _py_stt_whisper:
.. _test_vosk:

3. STT con Vosk (Offline)
==============================================

Vosk es un motor ligero de speech-to-text (STT) que soporta muchos idiomas y funciona completamente **offline** en Raspberry Pi.
Solo necesitas acceso a internet una vez para descargar un modelo de idioma. Después de eso, todo funciona sin conexión de red.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

En esta lección, vamos a:

* Verificar el micrófono en Raspberry Pi.
* Instalar y probar Vosk con un modelo de idioma elegido.


.. start_mic


Ejecutar el programa
--------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

La primera vez que ejecutes este código con un nuevo idioma, Vosk:

* **Descargará automáticamente el modelo de idioma** (por defecto, la versión pequeña).
* **Imprimirá la lista de idiomas compatibles**.
* Comenzará a **escuchar** la entrada de audio a través del micrófono.

Verás algo como esto en la terminal:

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

Esto significa:

   * El archivo del modelo (``vosk-model-small-en-us-0.15``) se ha descargado.
   * La lista de idiomas compatibles se ha impreso.
   * El sistema ahora está escuchando — di algo en el micrófono del Fusion HAT+, y el texto reconocido aparecerá en la terminal.

**Consejos:**

* Mantén el micrófono a unos **15–30 cm** de distancia para una mejor precisión.
* Elige un **modelo que coincida con tu idioma y acento**.
* Usa un entorno silencioso para mejorar el reconocimiento.

Código
---------------

.. code-block:: python

   from fusion_hat.stt import Vosk as STT

   stt = STT(language="en-us")

   while True:
      print("Say something")
      for result in stt.listen(stream=True):
         if result["done"]:
               print(f"final:   {result['final']}")
         else:
               print(f"partial: {result['partial']}", end="\r", flush=True)


**Explicación del código:**

* ``stt.listen(stream=True)`` — Inicia el reconocimiento de voz en streaming y produce resultados intermedios mientras hablas.
* ``result["partial"]`` — Muestra el **texto reconocido en tiempo real** (se actualiza continuamente).
* ``result["final"]`` — Muestra la **oración final reconocida** cuando dejas de hablar.
* El bucle se ejecuta continuamente, permitiendo **transcripción en tiempo real manos libres**.

Consejo: Este modo de streaming es perfecto para **asistentes de voz**, **control por comandos** o **transcripción en vivo**.

Solución de problemas
-----------------

* **No such file or directory (al ejecutar `arecord`)**

  Puede que hayas usado el número de tarjeta/dispositivo incorrecto.
  Ejecuta:

  .. code-block:: bash

     arecord -l

  y reemplaza ``1,0`` con los números mostrados para tu micrófono USB.


* **Vosk no reconoce el habla**

  * Asegúrate de que el **código de idioma** coincida con tu modelo (por ejemplo, ``en-us`` para inglés, ``zh-cn`` para chino).
  * Mantén el micrófono a 15–30 cm de distancia y evita el ruido de fondo.
  * Habla claramente y despacio.

* **Alta latencia / reconocimiento lento**

  * La descarga automática por defecto es un **modelo pequeño** (más rápido, pero menos preciso).
  * Si sigue siendo lento, cierra otros programas para liberar CPU.

.. end_mic