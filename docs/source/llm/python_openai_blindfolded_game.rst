.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_blindfolded_watermelon_game:

(Esempio) Gioco dello Schiacciamento dell'Anguria Bendato
=============================================================

**Introduzione**

Questo progetto crea un interattivo **Gioco dello Schiacciamento dell'Anguria Bendato** in cui i giocatori navigano in una griglia 20x20 metri usando un joystick mentre si affidano a un assistente AI per le indicazioni direzionali. Il sistema integra:

1. **Comandi joystick** per il movimento del giocatore sugli assi X/Y
2. **Guida basata su AI** utilizzando GPT-4 di OpenAI
3. **Feedback vocale** utilizzando Pico2Wave
4. **Generazione casuale dei bersagli** per il posizionamento dell'anguria
5. **Pulsante interattivo** per le azioni di schiacciamento

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Blindfolded_Watermelon_Smashing_Game.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Il giocatore parte dal centro (0,0) e deve trovare un'anguria posizionata casualmente usando solo indicazioni audio dall'assistente AI, creando un'esperienza di gioco coinvolgente a deprivazione sensoriale.

Puoi combinare vari dispositivi di input con moduli LLM per creare giochi AI interattivi. Vedi:

* :ref:`py_online_llm`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_joystick`

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_joystick`
        - \-
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schema di Collegamento**

Collega i componenti al Fusion HAT+ come segue:

.. image:: img/fzz/watermelon_game_bb.png
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
      sudo python3 llm_openai_blindfolded_game.py

#. Gioca

   Dopo l'avvio dello script, il gioco posizionera' casualmente un'anguria sul campo 20x20 metri.
   Usa il joystick per muoverti passo dopo passo e ascolta l'assistente AI per le indicazioni direzionali.

   Quando pensi di aver raggiunto la posizione dell'anguria, premi il pulsante per schiacciare.
   Se le tue coordinate corrispondono esattamente a quelle dell'anguria, vinci la partita.

#. Comprendi la meccanica del gioco

   * Sistema di Coordinate:

     - Il campo di gioco e' una griglia 20x20 metri
     - Le coordinate vanno da (-10,-10) a (10,10)
     - X positivo = Est, X negativo = Ovest
     - Y positivo = Sud, Y negativo = Nord (asse Y invertito)
     - Il punto centrale e' (0,0)

   * Regole di Movimento:

     - Joystick a destra -> X+1 (Est)
     - Joystick a sinistra -> X-1 (Ovest)
     - Joystick in su -> Y-1 (Nord)
     - Joystick in giu' -> Y+1 (Sud)
     - Ogni movimento cambia la posizione di 1 metro

   * Condizione di Vittoria:

     - Il giocatore deve essere alle coordinate esatte dell'anguria
     - Premi il pulsante per "schiacciare" nella posizione corrente
     - La corrispondenza esatta termina il gioco con un messaggio di vittoria

   * Ruolo dell'Assistente AI:

     - Riceve sia le coordinate del giocatore che quelle dell'anguria
     - Fornisce indicazioni direzionali cardinali (N, NE, E, SE, S, SW, W, NW)
     - Fornisce una stima della distanza in metri
     - Mantiene le risposte brevi per la riproduzione audio


**Codice**

Ecco lo script Python completo per il Gioco dello Schiacciamento dell'Anguria Bendato:

.. raw:: html

   <run></run>

.. code-block:: python


   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.adc import ADC
   from fusion_hat.pin import Pin
   from fusion_hat.tts import Pico2Wave
   import random, time

   # Register OpenAI API
   # openai.com

   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx

   # Setup TTS
   tts = Pico2Wave()
   tts.set_lang('en-US')

   # Setup Joystick
   btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)
   x_axis = ADC('A1')
   y_axis = ADC('A0')

   def MAP(x, in_min, in_max, out_min, out_max):
       """
       Map a value from one range to another.
       """
       return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

   def activate():
       global smash_tips
       smash_tips = True

   btn_pin.when_activated = activate

   # Setup LLM
   INSTRUCTIONS = "This is a blindfolded watermelon-smashing game. A point representing a watermelon is randomly generated within a 20x20 meter area with coordinates ranging from (-10,-10) to (10,10). The player starts from the origin (0,0) and moves using a joystick. Even if the player can't see anything, they press a button to perform a smash action. After smashing, you will receive the watermelon's and player's coordinates. You need to advise the player on the direction of the watermelon, like 'The watermelon is ten meters to your northeast.' If the smash coordinates match, the game ends. Your responses will be converted into speech via TTS, so please keep them brief, ideally within two sentences."

   WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant. Use the joystick to move and press the button to smash. I will guide you to find the watermelon. Good luck!"


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

   # Define the map size and the joystick pins
   watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)
   player_x, player_y = 0, 0
   smash_tips = False

   while True:
       x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
       y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

       if x_val > 80:
           player_x += 1
       elif x_val < -80:
           player_x -= 1

       if y_val > 80:
           player_y -= 1
       elif y_val < -80:
           player_y += 1

       # Debug positions (commented out in actual game)
       # print('Watermelon position: %d, %d  ' % (watermelon_x, watermelon_y))
       # print('Player position: %d, %d  ' % (player_x, player_y))

       time.sleep(0.3)

       if smash_tips:
           smash_tips = False
           print("Smash!")

           if (player_x, player_y) == (watermelon_x, watermelon_y):
               print("Target hit!")
               tts.say("Target hit!")
               break
           else:
               input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

               # Response with stream
               response = llm.prompt(input_text, stream=True)
               string = ""

               for next_word in response:
                   if next_word:
                       # print(next_word, end="", flush=True)  # Uncomment for streaming display
                       string += next_word

               # print("")  # New line after streaming
               print("AI: " + string)
               tts.say(string)

   print("Game over!")

----------------------------------------------

**Comprensione del Codice**

1. Configurazione della Sintesi Vocale

   Il gioco usa Pico2Wave per il feedback audio:

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')

   Questo converte le risposte testuali dell'AI in istruzioni vocali in inglese.

2. Gestione dell'Input Joystick

   Il joystick usa due canali ADC per la lettura degli assi X e Y:

   .. code-block:: python

      x_axis = ADC('A1')  # Movimento orizzontale
      y_axis = ADC('A0')  # Movimento verticale

      def MAP(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

      # Converti la lettura ADC 0-4095 nell'intervallo -100 a 100
      x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
      y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

3. Configurazione del Pulsante con Interrupt

   Il pulsante utilizza una callback di interrupt per la risposta immediata:

   .. code-block:: python

      btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)

      def activate():
          global smash_tips
          smash_tips = True

      btn_pin.when_activated = activate

   Quando premuto, imposta ``smash_tips`` a ``True``, attivando l'azione di schiacciamento nel ciclo principale.

4. Configurazione LLM OpenAI

   L'assistente AI e' configurato con istruzioni di gioco specifiche:

   .. code-block:: python

      INSTRUCTIONS = "This is a blindfolded watermelon-smashing game..."
      WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant..."

      llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      llm.set_max_messages(20)       # Mantiene la cronologia della conversazione
      llm.set_instructions(INSTRUCTIONS)  # Imposta le regole del gioco
      llm.set_welcome(WELCOME)       # Imposta il saluto iniziale

5. Gestione dello Stato del Gioco

   Il gioco mantiene le posizioni del giocatore e del bersaglio:

   .. code-block:: python

      # Posizionamento casuale dell'anguria
      watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)

      # Il giocatore parte dal centro
      player_x, player_y = 0, 0

      # Soglie di movimento (80% di deflessione del joystick)
      if x_val > 80:
          player_x += 1      # Muovi a destra
      elif x_val < -80:
          player_x -= 1      # Muovi a sinistra

      if y_val > 80:
          player_y -= 1      # Muovi su (Y negativo)
      elif y_val < -80:
          player_y += 1      # Muovi giu' (Y positivo)

6. Azione di Schiacciamento e Risposta AI

   Quando il pulsante viene premuto, il gioco verifica la corrispondenza o richiede assistenza AI:

   .. code-block:: python

      if smash_tips:
          smash_tips = False
          print("Smash!")

          if (player_x, player_y) == (watermelon_x, watermelon_y):
              print("Target hit!")
              tts.say("Target hit!")
              break  # Il gioco termina
          else:
              # Invia le posizioni all'AI per assistenza
              input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

              # Ottieni risposta in streaming dall'AI
              response = llm.prompt(input_text, stream=True)
              string = ""

              for next_word in response:
                  if next_word:
                      string += next_word

              print("AI: " + string)
              tts.say(string)  # Pronuncia le indicazioni

7. Elaborazione della Risposta in Streaming

   La risposta dell'AI viene elaborata parola per parola:

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              # Rimuovi il commento per visualizzare le parole mentre arrivano
              # print(next_word, end="", flush=True)
              string += next_word

8. Logica di Movimento con Zona Morta

   Il joystick ha una zona morta di 80 unita' per prevenire movimenti accidentali:

   .. code-block:: python

      # Muovi solo quando il joystick e' spinto >80% in qualsiasi direzione
      # Questo previene derive dalla posizione centrale
      if x_val > 80:    # Destra
      elif x_val < -80: # Sinistra

      if y_val > 80:    # Su
      elif y_val < -80: # Giu'

9. Struttura del Ciclo di Gioco

   Il ciclo principale del gioco continuamente:

   1. Legge la posizione del joystick
   2. Aggiorna le coordinate del giocatore se il joystick e' spinto
   3. Verifica la pressione del pulsante di schiacciamento
   4. Elabora le risposte dell'AI quando necessario
   5. Fornisce feedback audio tramite TTS

----------------------------------------------

**Risoluzione dei Problemi**

- Nessuna risposta dal joystick

  - Verifica le connessioni ADC: A0 per l'asse Y, A1 per l'asse X
  - Controlla l'alimentazione: VCC a 3.3V, GND a massa
  - Testa la lettura ADC: ``print(x_axis.read())`` dovrebbe mostrare 0-4095
  - Assicurati che il joystick sia centrato (dovrebbe leggere ~2048)


- Nessun audio dal TTS

  - Controlla l'uscita audio: ``sudo raspi-config`` -> **System Options** -> **Audio**
  - Prova l'altoparlante: ``speaker-test -t sine -f 440``
  - Assicurati che Pico2Wave sia installato: ``pico2wave --help``
  - Controlla il volume: ``alsamixer``
  - Esegui nuovamente lo script di configurazione audio: ``sudo /opt/setup_fusion_hat_audio.sh``

- Errori API OpenAI

  - Verifica la chiave API in ``secret.py``
  - Controlla la connessione Internet: ``ping 8.8.8.8``
  - Assicurati che la fatturazione sia abilitata sull'account OpenAI
  - Verifica che il modello "gpt-4o" sia disponibile per il tuo account

- Il giocatore si muove troppo veloce/lento

  - Regola la soglia di movimento (attualmente 80): piu' alto = maggiore deflessione del joystick necessaria
  - Modifica l'incremento di movimento (attualmente 1): cambia a 0.5 per un controllo piu' fine
  - Regola il tempo di pausa (attualmente 0.3s): piu' lungo = risposta di movimento piu' lenta


- Risposte AI troppo lunghe

  - Enfatizza la brevita' nelle INSTRUCTIONS
  - Aggiungi "Respond in 10 words or less" alle istruzioni
  - Implementa il controllo della lunghezza della risposta nel codice

----------------------------------------------

Questo gioco dell'anguria bendato dimostra come i controlli fisici, la guida AI e il feedback audio possano creare un'esperienza di gioco coinvolgente basata sui sensi che sfida la consapevolezza spaziale e le capacita' di ascolto!
