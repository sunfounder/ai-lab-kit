.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(Esempio) Decodificatore di Codice Morse basato su AI
========================================================

**Introduzione**

Questo progetto crea un intelligente **Decodificatore di Codice Morse** che utilizza l'AI per interpretare i modelli di temporizzazione delle pressioni dei pulsanti. Il sistema acquisisce dati di temporizzazione precisi e sfrutta GPT di OpenAI per decodificare messaggi in codice Morse in tempo reale. Il decodificatore offre:

1. **Input basato sulla temporizzazione** che cattura i tempi precisi di pressione e rilascio
2. **Decodifica basata su AI** utilizzando GPT per interpretare i modelli punto/linea
3. **Indicatore Visivo** con LED che mostra lo stato di decodifica attivo
4. **Interfaccia a due pulsanti** pulsanti di input e controllo separati
5. **Feedback in Tempo Reale** che mostra i dati di temporizzazione durante l'inserimento

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Il sistema registra la durata delle pressioni dei pulsanti, invia i dati di temporizzazione all'AI per l'interpretazione e decodifica accuratamente sequenze di codice Morse come il segnale universale di soccorso "SOS".

Puoi combinare input sensibili alla temporizzazione con l'interpretazione AI per vari sistemi di codifica. Vedi:

* :ref:`py_online_llm`

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_button`
        - |link_button_buy| (x2)
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schema di Collegamento**

Collega i componenti al Raspberry Pi come segue:

.. image:: img/fzz/morse_decoder_bb.png
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
      sudo python3 llm_openai_morse_decoder.py

#. Prova un semplice messaggio in codice Morse (esempio: "SOS")

   Dopo l'avvio del programma, premi il pulsante start/stop per iniziare la registrazione.
   Poi premi il pulsante Morse per inserire punti (pressioni brevi) e linee (pressioni lunghe).

   Quando hai finito, premi di nuovo il pulsante start/stop per fermare la registrazione e decodificare il messaggio.

#. Controlla l'output della console

   La console mostrera' i timestamp di pressione/rilascio e l'AI analizzera' i dati di temporizzazione
   e produrra' il messaggio decodificato.

   **Output tipico della console durante l'inserimento di "SOS":**

   .. code-block:: text

      To decode the Morse code message based on the button press times provided, we need to interpret the duration of each press. Typically, a short press (dot) is around 0.2 to 0.3 seconds, while a long press (dash) is about 0.5 seconds or longer. Let's analyze the press durations:

      1. `1767773542.1257536` to `1767773542.285196` - Duration: ~0.16 seconds - Dot (.)
      2. `1767773542.4936137` to `1767773542.6315389` - Duration: ~0.14 seconds - Dot (.)
      3. `1767773542.9092748` to `1767773543.0543947` - Duration: ~0.15 seconds - Dot (.)
      4. `1767773544.2299025` to `1767773544.5774245` - Duration: ~0.35 seconds - Dash (-)
      5. `1767773545.1017563` to `1767773545.4954002` - Duration: ~0.39 seconds - Dash (-)
      6. `1767773546.11932` to `1767773546.5881057` - Duration: ~0.47 seconds - Dash (-)
      7. `1767773547.824543` to `1767773547.9534554` - Duration: ~0.13 seconds - Dot (.)
      8. `1767773548.1879761` to `1767773548.2895174` - Duration: ~0.10 seconds - Dot (.)
      9. `1767773548.5281847` to `1767773548.6453152` - Duration: ~0.12 seconds - Dot (.)

      Now let's decode the sequence into letters using Morse code:

      - `...` (Dot Dot Dot) = S
      - `---` (Dash Dash Dash) = O
      - `...` (Dot Dot Dot) = S

      Putting it all together, the decoded message is "SOS".

#. Comprendi il flusso di lavoro

   1. Avvia registrazione: premi il pulsante start/stop (GPIO 17) e il LED si ACCENDE
   2. Inserisci codice Morse: usa il pulsante Morse (GPIO 22) per punti e linee
   3. Display in tempo reale: la console mostra i timestamp di pressione/rilascio
   4. Ferma e decodifica: premi di nuovo il pulsante start/stop e il LED si SPEGNE
   5. Analisi AI: i dati di temporizzazione vengono inviati a GPT di OpenAI per l'interpretazione
   6. Output decodificato: l'AI stampa il messaggio decodificato

**Codice**

Ecco lo script Python completo per il Decodificatore di Codice Morse basato su AI:

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.pin import Pin
   import random, time

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup GPIO pins
   morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   led = Pin(27, Pin.OUT)  # Indicator LED on GPIO 27

   # Store the morse code events with timing data
   morse_events = []
   input_active = False  # Flag to indicate if input is active

   # Setup LLM with Morse code decoding instructions
   INSTRUCTIONS = "You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it."

   WELCOME = "Hello, I am a Morse code decoder. Please press the button to start decoding. When you are done, press the button again to stop."

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

   # Send the morse code timing data to the AI for decoding
   def decode_and_print():
       global morse_events

       # Convert timing events to string for AI processing
       input_text = str(morse_events)

       # Get response from AI with streaming
       response = llm.prompt(input_text, stream=True)

       # Print streaming response
       for next_word in response:
           if next_word:
               print(next_word, end="", flush=True)

       print("")  # New line after complete response

       morse_events = []  # Clear the morse code events for next message

   # Morse code input handling variables
   start_time = 0

   # Function called when morse input button is pressed
   def morse_input_pressed():
       global start_time
       start_time = time.time()
       morse_events.append(('pressed', start_time))
       print(f" Pressed at {start_time} -", end="")

   # Function called when morse input button is released
   def morse_input_released():
       global morse_events, start_time
       release_time = time.time()

       # Debounce: ignore releases within 0.1 seconds
       if release_time - start_time < 0.1:
           return

       morse_events.append(('released', release_time))
       print(f" {release_time}")

   # Start/stop button handler
   def handle_start_stop():
       global input_active, morse_events

       if input_active:
           # Stop recording and decode
           led.off()
           print("Input stopped and decoded.")
           decode_and_print()
           input_active = False
       else:
           # Start recording new message
           input_active = True
           morse_events.clear()  # Clear previous events
           led.on()
           print("Input started.")

   # Add event listeners to buttons
   start_stop_button.when_activated = handle_start_stop
   morse_input.when_activated = morse_input_pressed
   morse_input.when_deactivated = morse_input_released

   # Main program loop
   try:
       while True:
           time.sleep(0.1)
   except KeyboardInterrupt:
       pass


----------------------------------------------

**Comprensione del Codice**

1. Configurazione dei Pin GPIO

   Tre pin GPIO sono configurati per scopi diversi:

   .. code-block:: python

      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)

   - Tempo di rimbalzo (0.05s): Previene rilevamenti multipli dal rimbalzo meccanico dell'interruttore
   - Pull-down: Garantisce un segnale LOW pulito quando il pulsante non e' premuto
   - Funzioni separate: I pulsanti di input e controllo prevengono input accidentali

2. Memorizzazione dei Dati di Temporizzazione

   Gli eventi di pressione/rilascio vengono memorizzati con timestamp precisi:

   .. code-block:: python

      morse_events = []  # Lista vuota per memorizzare gli eventi

      # Ogni evento memorizzato come tupla: ('pressed'/'released', timestamp)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. Meccanismo di Debounce

   Previene attivazioni false dal rimbalzo dell'interruttore:

   .. code-block:: python

      def morse_input_released():
          if release_time - start_time < 0.1:  # 100ms debounce
              return  # Ignora rilasci molto brevi

          morse_events.append(('released', release_time))

4. Gestione dello Stato

   Il sistema utilizza un flag per tracciare lo stato di registrazione:

   .. code-block:: python

      input_active = False  # Inizialmente non in registrazione

      def handle_start_stop():
          if input_active:
              # Ferma registrazione e decodifica
              input_active = False
          else:
              # Avvia registrazione
              input_active = True
              morse_events.clear()  # Cancella dati precedenti

5. Indicatore Visivo

   Il LED fornisce feedback visivo dello stato di registrazione:

   .. code-block:: python

      def handle_start_stop():
          if input_active:
              led.off()  # LED SPENTO quando non registra
          else:
              led.on()   # LED ACCESO quando registra

6. Costruzione del Prompt AI

   I dati di temporizzazione vengono convertiti in stringa per l'elaborazione AI:

   .. code-block:: python

      input_text = str(morse_events)

      # Esempio di formato inviato all'AI:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. Risposta in Streaming

   La risposta dell'AI viene elaborata e visualizzata in tempo reale:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. Architettura Basata su Eventi

   Gli eventi dei pulsanti attivano callback immediate:

   .. code-block:: python

      # Assegna funzioni callback agli eventi dei pulsanti
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. Precisione di Temporizzazione

   Utilizza ``time.time()`` per una temporizzazione precisa al microsecondo:

   .. code-block:: python

      start_time = time.time()  # Ora corrente in secondi dall'epoca

      # Calcola la durata della pressione:
      duration = release_time - start_time

10. Cancellazione dei Dati

    Dopo la decodifica, la lista degli eventi viene cancellata per il messaggio successivo:

    .. code-block:: python

        def decode_and_print():
            # ... elabora eventi ...
            morse_events = []  # Cancella per il messaggio successivo

----------------------------------------------

**Standard di Temporizzazione del Codice Morse**

* Temporizzazione Standard (basata sulla parola PARIS):

  - Punto: 1 unita'
  - Linea: 3 unita'
  - Spazio intra-carattere (tra punti/linee): 1 unita'
  - Spazio inter-carattere (tra lettere): 3 unita'
  - Spazio tra parole: 7 unita'

* Implementazione Pratica:

  - Punto: < 0.3 secondi (pressione breve)
  - Linea: > 0.5 secondi (pressione lunga)
  - Tra elementi: < 0.5 secondi di pausa
  - Tra lettere: 0.5-1.5 secondi di pausa
  - Tra parole: > 1.5 secondi di pausa

* Lettere Comuni del Codice Morse:

  - A: . -- (punto-linea)
  - B: -- . . . (linea-punto-punto-punto)
  - C: -- . -- . (linea-punto-linea-punto)
  - S: . . . (punto-punto-punto)
  - O: -- -- -- (linea-linea-linea)

----------------------------------------------

**Risoluzione dei Problemi**

- Le pressioni dei pulsanti non vengono registrate

  - Controlla il cablaggio: GPIO 22/17 al pulsante, altro lato a massa
  - Verifica la configurazione pull-down
  - Prova con uno script semplice: ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``
  - Controlla l'impostazione del tempo di rimbalzo (0.05s potrebbe essere troppo alto)

- Il LED non si accende

  - Verifica la polarita' del LED: anodo (gamba lunga) a GPIO 27 attraverso un resistore
  - Controlla il valore del resistore (220 ohm raccomandato)
  - Prova il LED direttamente: ``Pin(27, Pin.OUT).on()`` dovrebbe accendere il LED
  - Assicurati che la connessione di massa sia completa

- I dati di temporizzazione sembrano errati

  - Controlla l'orologio di sistema: comando ``date``
  - Riduci il tempo di debounce se troppo sensibile
  - Aggiungi istruzioni print per verificare l'esecuzione delle callback
  - Prova con durate di pressione consistenti

- L'AI non decodifica correttamente

  - Controlla la chiave API e la connessione Internet
  - Esamina i dati di temporizzazione inviati all'AI (stampa ``morse_events``)
  - Assicurati che le durate di pressione siano consistenti (punti brevi, linee lunghe)
  - Aggiungi pause piu' chiare tra le lettere

- Attivazioni multiple da una singola pressione

  - Aumenta il parametro bounce_time (prova 0.1s)
  - Controlla il rimbalzo meccanico dell'interruttore
  - Aggiungi debounce hardware con un condensatore
  - Verifica che il pulsante sia cablato correttamente

- Il sistema non risponde a start/stop

  - Controlla se un'altra callback sta interferendo
  - Verifica la logica del flag ``input_active``
  - Aggiungi print di debug in ``handle_start_stop()``
  - Assicurati che nessun altro processo stia usando GPIO

- Risposta AI troppo lenta

  - Controlla la velocita' della connessione Internet
  - Riduci il numero di eventi (messaggi piu' brevi)
  - Considera l'uso della decodifica locale come alternativa
  - Implementa un timeout per le risposte AI

- Impossibile distinguere punti da linee

  - Esercitati con una temporizzazione consistente
  - Regola la soglia nelle istruzioni AI
  - Aggiungi pre-elaborazione locale prima di inviare all'AI
  - Usa feedback visivo durante l'inserimento

----------------------------------------------


Questo decodificatore di codice Morse basato su AI dimostra come i dati di temporizzazione precisi combinati con il riconoscimento intelligente di pattern possano rivitalizzare e modernizzare i metodi di comunicazione storici, rendendoli accessibili ed educativi per le nuove generazioni!
