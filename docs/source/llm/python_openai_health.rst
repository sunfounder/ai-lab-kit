.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_health_assistant:

(Ejemplo) Asistente de Salud IA con Monitorización de Temperatura
=========================================================

**Introducción**


Este proyecto crea un inteligente **Asistente de Salud IA** que combina la detección de temperatura corporal con interacción por voz para proporcionar evaluaciones de salud personalizadas. El sistema integra:

1. **Detección de temperatura con termistor** para una medición precisa de la temperatura corporal
2. **Reconocimiento de voz** para comprender los síntomas y consultas del usuario
3. **Análisis de salud con IA** usando OpenAI GPT para evaluación médica
4. **Retroalimentación por voz (TTS)** proporcionando recomendaciones de salud audibles
5. **Monitorización en tiempo real** con conversión continua de temperatura

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Health_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

El asistente de salud mide la temperatura corporal a través de un circuito termistor, analiza la lectura con IA y proporciona consejos de salud adecuados basados en rangos de temperatura médicos establecidos.


* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
    *   - :ref:`cpn_thermistor`
        - |link_thermistor_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy| (10kΩ)
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Diagrama de Conexión**

Conecta los componentes al Fusion HAT+ de la siguiente manera:

.. image:: img/fzz/health_assistant_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Ejecutar el Ejemplo**

#. Ejecuta el Código

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_health.py

#. Verifica el Resultado

   Cuando el programa se inicia, te pedirá que hables. Luego estimará tu temperatura
   corporal y proporcionará consejos de salud.

   Salida típica de la consola:

   .. code-block:: text

      Hello, I am a health assistant. Please hold your thermometer and I will assess your
      body temperature based on the thermistor reading. If you feel unwell, please provide
      your symptoms and I will provide appropriate health advice.

      Say something
      partial: I feel
      partial: I feel very
      partial: I feel very warm
      final: I feel very warm and tired

      Your body temperature is 38.7°C, which indicates a mild fever. Please rest, stay
      hydrated, and monitor your symptoms. If the fever persists or worsens, consider
      seeking medical attention.

#. Escenarios de Ejemplo

   * Temperatura Normal (36.5°C):

     .. code-block:: text

        User: "How's my temperature?"
        AI: "Your body temperature is 36.5°C, which is within the normal range. You're
        doing well, but continue to monitor how you feel."

   * Fiebre Alta (39.2°C):

     .. code-block:: text

        User: "I have a headache and feel hot"
        AI: "Your body temperature is 39.2°C, indicating a high fever. Please rest
        immediately, stay hydrated, and consider seeking medical advice as soon as possible."

   * Temperatura Baja (34.2°C):

     .. code-block:: text

        User: "I feel cold and shivering"
        AI: "Your body temperature is 34.2°C, which is below normal and may indicate
        hypothermia. Please warm up immediately with blankets and warm drinks."


**Código**

Aquí está el script completo en Python para el Asistente de Salud IA:

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   import time
   from fusion_hat.stt import STT
   from fusion_hat.adc import ADC
   import math
   from fusion_hat.tts import Pico2Wave

   # Setup Text-to-Speech and Speech-to-Text
   tts = Pico2Wave()
   tts.set_lang('en-US')
   stt = STT(language="en-us")

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup ADC for thermistor reading on channel A3
   thermistor = ADC('A3')

   # Setup LLM with health assessment instructions
   INSTRUCTIONS = '''
   You are a health assistant. Your task is to assess the user's body temperature based on the thermistor reading and provide appropriate health advice.

   The thermistor reading represents body temperature in Celsius.

   ### Input Format:
   "thermistor: [value], message: [user query]"

   ### Output Guidelines:
   1. If temperature < 35.0°C, warn about hypothermia and suggest warming up.
   2. If 35.0°C ≤ temperature ≤ 37.5°C, confirm normal temperature and reassure the user.
   3. If 37.5°C < temperature ≤ 38.5°C, indicate mild fever and suggest rest and hydration.
   4. If temperature > 38.5°C, alert about high fever and recommend medical attention.
   5. Include the temperature value in your response to justify your assessment.
   6. Your reply should be brief and concise, no more than two sentences.

   ### Example Input:
   thermistor: 39.0, message: I feel unwell.

   ### Example Output:
   Your body temperature is 39.0°C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
   '''

   WELCOME = "Hello, I am a health assistant. Please hold your thermometer and I will assess your body temperature based on the thermistor reading. If you feel unwell, please provide your symptoms and I will provide appropriate health advice."

   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o",
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   # Function to read and convert thermistor value to temperature
   def temperature():
       while True:
           # Read analog value (0-4095)
           analogVal = thermistor.read()

           # Calculate voltage across thermistor
           Vr = 3.3 * float(analogVal) / 4095

           # Check for sensor issues
           if 3.3 - Vr < 0.1:
               print("Please check the sensor")
               continue

           # Calculate thermistor resistance
           Rt = 10000 * Vr / (3.3 - Vr)

           # Convert resistance to temperature using Steinhart-Hart equation
           # B = 3950 (thermistor coefficient), R0 = 10000Ω at 25°C
           temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))

           # Convert from Kelvin to Celsius
           Cel = temp - 273.15

           return Cel

   # Main loop for voice interaction
   while True:
       print("Say something")

       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")

               # Measure temperature and combine with user query
               current_temp = temperature()
               input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

               # Get response from LLM with streaming
               response = llm.prompt(input_text, stream=True)

               # Collect the full response
               string = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       string += next_word

               # Speak the response
               tts.say(string)
               print("")  # New line after response

           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**Entendiendo el Código**

1. Inicialización del Sensor de Temperatura

   El termistor está conectado al canal ADC A3:

   .. code-block:: python

      thermistor = ADC('A3')

   Esto lee valores analógicos de 0-4095 que representan niveles de voltaje.

2. Conversión de Temperatura Steinhart-Hart

   El termistor usa la ecuación de Steinhart-Hart para un cálculo preciso de temperatura:

   .. code-block:: python

      # Read analog value (0-4095)
      analogVal = thermistor.read()

      # Convert to voltage (0-3.3V)
      Vr = 3.3 * float(analogVal) / 4095

      # Calculate thermistor resistance using voltage divider formula
      Rt = 10000 * Vr / (3.3 - Vr)

      # Steinhart-Hart equation: 1/T = 1/T0 + 1/B * ln(R/R0)
      temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))

      # Convert Kelvin to Celsius
      Cel = temp - 273.15

3. Verificación de Errores del Sensor

   El código incluye detección básica de errores:

   .. code-block:: python

      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue

   Esto detecta si el termistor está desconectado o en cortocircuito.

4. Configuración del Reconocimiento de Voz

   Tanto STT como TTS están configurados para inglés:

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. Construcción de Entrada Contextual

   Los datos de temperatura se combinan con la consulta del usuario:

   .. code-block:: python

      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

   Formato: ``"thermistor: 37.2, message: I feel dizzy"``

6. Lógica de Clasificación Médica

   Las instrucciones de la IA definen rangos de temperatura:

   .. code-block:: python

      # Temperature ranges for medical assessment:
      # < 35.0°C: Hypothermia warning
      # 35.0-37.5°C: Normal range
      # 37.5-38.5°C: Mild fever
      # > 38.5°C: High fever

7. Procesamiento de Voz en Tiempo Real

   El sistema muestra resultados de reconocimiento parcial:

   .. code-block:: python

      for result in stt.listen(stream=True):
          if result["done"]:
              # Final recognition
              print(f"final: {result['final']}")
          else:
              # Partial recognition
              print(f"partial: {result['partial']}", end="", flush=True)

8. Respuesta de IA en Streaming

   La respuesta de la IA se transmite y se reproduce simultáneamente:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word

      tts.say(string)  # Speak complete response

9. Formato de Temperatura

   La temperatura se formatea con un decimal:

   .. code-block:: python

      f"thermistor: {current_temp:.1f}"

   Esto garantiza una precisión consistente (por ejemplo, 36.5°C en lugar de 36.512345°C).

10. Pantalla de Consola Limpia

    Usa códigos de escape ANSI para una salida limpia:

    .. code-block:: python

        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

    - ``\r``: Retorno al inicio de la línea
    - ``\x1b[K``: Borrar hasta el final de la línea
    - Evita la superposición de texto durante el streaming

----------------------------------------------

**Solución de problemas**

- Lecturas de temperatura inexactas

  - Verifica el cableado del termistor: configuración correcta del divisor de voltaje
  - Verifica el valor de la resistencia: debe coincidir con la resistencia nominal del termistor
  - Calibra con una fuente de temperatura conocida
  - Verifica el voltaje de referencia del ADC (debe ser 3.3V estable)

- No hay reconocimiento de voz

  - Prueba el micrófono: ``arecord --duration=3 test.wav && aplay test.wav``
  - Verifica la selección del dispositivo de audio en la inicialización de STT
  - Asegúrate de que el ruido de fondo sea mínimo
  - Habla claramente y a un ritmo moderado

- La IA no responde

  - Verifica la conexión a internet
  - Verifica la clave API de OpenAI en ``secret.py``
  - Asegúrate de que la facturación esté habilitada en la cuenta de OpenAI
  - Verifica si se excedieron los límites de velocidad de la API

- La temperatura salta erráticamente

  - Añade filtrado por software: media móvil de lecturas
  - Verifica conexiones sueltas
  - Añade un condensador (0.1µF) a través del termistor para reducir el ruido
  - Asegúrate de que el termistor tenga buen contacto térmico

- El text-to-speech no funciona

  - Prueba la salida de audio: ``speaker-test -t sine -f 440``
  - Verifica la configuración de idioma: ``tts.set_lang('en-US')``
  - Verifica el volumen: ``alsamixer``
  - Re-ejecuta el script de configuración de audio: ``sudo /opt/setup_fusion_hat_audio.sh``

- La lectura del sensor muestra 0 o 4095

  - Verifica el cableado: el termistor puede estar en cortocircuito (0) o abierto (4095)
  - Verifica el cálculo del divisor de voltaje
  - Prueba el ADC con una fuente de voltaje conocida
  - Verifica el canal ADC (debe ser A3)

**Aviso de Seguridad y Médico**

.. warning::

   Este proyecto es solo con fines educativos y de demostración.
   **NO** es un dispositivo médico y **NO** debe utilizarse para diagnósticos o tratamientos médicos reales.

#. Pautas de seguridad

   * No para uso médico: No confíes en este sistema para ninguna decisión de salud o tratamiento.
   * Situaciones de emergencia: Siempre busca ayuda médica profesional para síntomas graves.
   * Limitaciones de precisión: La precisión del termistor es limitada en comparación con los termómetros médicos.
   * Calibración requerida: La calibración regular contra un termómetro médico es esencial.
   * Supervisión necesaria: Se recomienda supervisión de un adulto cuando se use con fines educativos.

#. Cuándo buscar atención médica

   Busca ayuda médica profesional si ocurre alguna de las siguientes condiciones:

   * Temperatura > 39.5°C (103.1°F) en adultos
   * Temperatura > 38.0°C (100.4°F) en bebés menores de 3 meses
   * Fiebre que dura más de 3 días
   * Dificultad para respirar o dolor en el pecho
   * Dolor de cabeza intenso o rigidez en el cuello
   * Confusión o convulsiones



----------------------------------------------

¡Este Asistente de Salud IA demuestra cómo la tecnología de sensores, la interacción por voz y la inteligencia artificial pueden trabajar juntas para crear herramientas accesibles de monitoreo de salud, al tiempo que enfatiza la importancia de la consulta médica profesional para problemas de salud graves!