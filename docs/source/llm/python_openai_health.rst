.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_health_assistant:

(Esempio) Assistente Sanitario AI con Monitoraggio della Temperatura
======================================================================

**Introduzione**


Questo progetto crea un intelligente **Assistente Sanitario AI** che combina il rilevamento della temperatura corporea con l'interazione vocale per fornire valutazioni sanitarie personalizzate. Il sistema integra:

1. **Rilevamento della Temperatura tramite Termistore** per la misurazione accurata della temperatura corporea
2. **Riconoscimento Vocale** per comprendere i sintomi e le richieste dell'utente
3. **Analisi Sanitaria basata su AI** utilizzando GPT di OpenAI per la valutazione medica
4. **Feedback vocale** che fornisce raccomandazioni sanitarie udibili
5. **Monitoraggio in tempo reale** con conversione continua della temperatura

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Health_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

L'assistente sanitario misura la temperatura corporea attraverso un circuito termistore, analizza la lettura con AI e fornisce consigli sanitari appropriati basati su intervalli di temperatura medici consolidati.


* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_thermistor`
        - |link_thermistor_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy| (10kohm)
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schema di Collegamento**

Collega i componenti al Fusion HAT+ come segue:

.. image:: img/fzz/health_assistant_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Esegui l'Esempio**

#. Esegui il codice

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_health.py

#. Controlla il risultato

   Quando il programma si avvia, ti chiedera' di parlare. Stimera' poi la tua temperatura corporea e fornira' consigli sanitari.

   Output tipico della console:

   .. code-block:: text

      Hello, I am a health assistant. Please hold your thermometer and I will assess your
      body temperature based on the thermistor reading. If you feel unwell, please provide
      your symptoms and I will provide appropriate health advice.

      Say something
      partial: I feel
      partial: I feel very
      partial: I feel very warm
      final: I feel very warm and tired

      Your body temperature is 38.7 C, which indicates a mild fever. Please rest, stay
      hydrated, and monitor your symptoms. If the fever persists or worsens, consider
      seeking medical attention.

#. Scenari di Esempio

   * Temperatura Normale (36.5 C):

     .. code-block:: text

        User: "How's my temperature?"
        AI: "Your body temperature is 36.5 C, which is within the normal range. You're
        doing well, but continue to monitor how you feel."

   * Febbre Alta (39.2 C):

     .. code-block:: text

        User: "I have a headache and feel hot"
        AI: "Your body temperature is 39.2 C, indicating a high fever. Please rest
        immediately, stay hydrated, and consider seeking medical advice as soon as possible."

   * Temperatura Bassa (34.2 C):

     .. code-block:: text

        User: "I feel cold and shivering"
        AI: "Your body temperature is 34.2 C, which is below normal and may indicate
        hypothermia. Please warm up immediately with blankets and warm drinks."


**Codice**

Ecco lo script Python completo per l'Assistente Sanitario AI:

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
   1. If temperature < 35.0 C, warn about hypothermia and suggest warming up.
   2. If 35.0 C <= temperature <= 37.5 C, confirm normal temperature and reassure the user.
   3. If 37.5 C < temperature <= 38.5 C, indicate mild fever and suggest rest and hydration.
   4. If temperature > 38.5 C, alert about high fever and recommend medical attention.
   5. Include the temperature value in your response to justify your assessment.
   6. Your reply should be brief and concise, no more than two sentences.

   ### Example Input:
   thermistor: 39.0, message: I feel unwell.

   ### Example Output:
   Your body temperature is 39.0 C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
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
           # B = 3950 (thermistor coefficient), R0 = 10000 Ohm at 25 C
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

**Comprensione del Codice**

1. Inizializzazione del Sensore di Temperatura

   Il termistore e' collegato al canale ADC A3:

   .. code-block:: python

      thermistor = ADC('A3')

   Questo legge valori analogici da 0-4095 che rappresentano i livelli di tensione.

2. Conversione Steinhart-Hart della Temperatura

   Il termistore utilizza l'equazione di Steinhart-Hart per un calcolo accurato della temperatura:

   .. code-block:: python

      # Leggi valore analogico (0-4095)
      analogVal = thermistor.read()

      # Converti in tensione (0-3.3V)
      Vr = 3.3 * float(analogVal) / 4095

      # Calcola la resistenza del termistore usando la formula del partitore di tensione
      Rt = 10000 * Vr / (3.3 - Vr)

      # Equazione di Steinhart-Hart: 1/T = 1/T0 + 1/B * ln(R/R0)
      temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))

      # Converti Kelvin in Celsius
      Cel = temp - 273.15

3. Controllo Errori del Sensore

   Il codice include un rilevamento di errori di base:

   .. code-block:: python

      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue

   Questo rileva se il termistore e' disconnesso o in corto.

4. Configurazione del Riconoscimento Vocale

   Sia STT che TTS sono configurati per l'inglese:

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. Costruzione dell'Input Contestuale

   I dati della temperatura sono combinati con la richiesta dell'utente:

   .. code-block:: python

      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

   Formato: ``"thermistor: 37.2, message: I feel dizzy"``

6. Logica di Classificazione Medica

   Le istruzioni AI definiscono gli intervalli di temperatura:

   .. code-block:: python

      # Intervalli di temperatura per la valutazione medica:
      # < 35.0 C: Avviso ipotermia
      # 35.0-37.5 C: Intervallo normale
      # 37.5-38.5 C: Febbre lieve
      # > 38.5 C: Febbre alta

7. Elaborazione Vocale in Tempo Reale

   Il sistema mostra i risultati di riconoscimento parziali:

   .. code-block:: python

      for result in stt.listen(stream=True):
          if result["done"]:
              # Riconoscimento finale
              print(f"final: {result['final']}")
          else:
              # Riconoscimento parziale
              print(f"partial: {result['partial']}", end="", flush=True)

8. Risposta AI in Streaming

   La risposta AI viene trasmessa in streaming e pronunciata simultaneamente:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word

      tts.say(string)  # Pronuncia la risposta completa

9. Formattazione della Temperatura

   La temperatura e' formattata con una cifra decimale:

   .. code-block:: python

      f"thermistor: {current_temp:.1f}"

   Questo garantisce una precisione costante (ad esempio, 36.5 C invece di 36.512345 C).

10. Display Console Pulito

    Utilizza codici di escape ANSI per un output pulito:

    .. code-block:: python

        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

    - ``\r``: Ritorno a inizio riga
    - ``\x1b[K``: Cancella a fine riga
    - Previene la sovrapposizione del testo durante lo streaming

----------------------------------------------

**Risoluzione dei Problemi**

- Letture di temperatura inaccurate

  - Controlla il cablaggio del termistore: configurazione corretta del partitore di tensione
  - Verifica il valore del resistore: deve corrispondere alla resistenza nominale del termistore
  - Calibra con una fonte di temperatura nota
  - Controlla la tensione di riferimento ADC (dovrebbe essere 3.3V stabile)

- Nessun riconoscimento vocale

  - Prova il microfono: ``arecord --duration=3 test.wav && aplay test.wav``
  - Controlla la selezione del dispositivo audio nell'inizializzazione STT
  - Assicurati che il rumore di fondo sia minimo
  - Parla chiaramente e a ritmo moderato

- L'AI non risponde

  - Controlla la connessione Internet
  - Verifica la chiave API OpenAI in ``secret.py``
  - Assicurati che la fatturazione sia abilitata sull'account OpenAI
  - Controlla se i limiti di velocita' API sono stati superati

- La temperatura varia in modo erratico

  - Aggiungi filtro software: media mobile delle letture
  - Controlla eventuali connessioni allentate
  - Aggiungi un condensatore (0.1 uF) attraverso il termistore per la riduzione del rumore
  - Assicurati che il termistore abbia un buon contatto termico

- La sintesi vocale non funziona

  - Prova l'uscita audio: ``speaker-test -t sine -f 440``
  - Verifica l'impostazione della lingua: ``tts.set_lang('en-US')``
  - Controlla il volume: ``alsamixer``
  - Esegui nuovamente lo script di configurazione audio: ``sudo /opt/setup_fusion_hat_audio.sh``

- La lettura del sensore mostra 0 o 4095

  - Controlla il cablaggio: il termistore potrebbe essere in corto (0) o aperto (4095)
  - Verifica il calcolo del partitore di tensione
  - Prova l'ADC con una fonte di tensione nota
  - Controlla il canale ADC (dovrebbe essere A3)

**Avvertenza Sanitaria e Medica**

.. warning::

   Questo progetto e' solo a scopo educativo e dimostrativo.
   NON e' un dispositivo medico e NON deve essere utilizzato per diagnosi o trattamenti medici reali.

#. Linee guida di sicurezza

   * Non per uso medico: Non affidarti a questo sistema per qualsiasi decisione sanitaria o terapeutica.
   * Emergenze: Cerca sempre assistenza medica professionale per sintomi gravi.
   * Limitazioni di precisione: La precisione del termistore e' limitata rispetto ai termometri medici.
   * Calibrazione richiesta: La calibrazione regolare rispetto a un termometro medico e' essenziale.
   * Supervisione necessaria: La supervisione di un adulto e' raccomandata quando usato per scopi educativi.

#. Quando cercare assistenza medica

   Cerca assistenza medica professionale se si verifica uno dei seguenti:

   * Temperatura > 39.5 C (103.1 F) negli adulti
   * Temperatura > 38.0 C (100.4 F) nei neonati sotto i 3 mesi
   * Febbre che dura piu' di 3 giorni
   * Difficolta' respiratorie o dolore al petto
   * Forte mal di testa o torcicollo
   * Confusione o convulsioni



----------------------------------------------

Questo Assistente Sanitario AI dimostra come la tecnologia dei sensori, l'interazione vocale e l'intelligenza artificiale possano lavorare insieme per creare strumenti di monitoraggio sanitario accessibili, enfatizzando al contempo l'importanza della consultazione medica professionale per problemi di salute seri!
