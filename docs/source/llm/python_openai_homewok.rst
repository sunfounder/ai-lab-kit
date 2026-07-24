.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

(Esempio) Demo di Correzione dei Compiti con Fotocamera Pan-Tilt
===================================================================

**Introduzione**

Questo progetto crea un interattivo **Assistente AI per la Correzione dei Compiti** che combina visione artificiale, intelligenza artificiale e robotica. Il sistema:

1. **Acquisisce foto** di domande dei compiti scritte a mano o stampate usando una fotocamera Raspberry Pi
2. **Analizza il contenuto** usando il modello di visione GPT-4 di OpenAI per determinare se le risposte sono corrette
3. **Fornisce feedback fisico** attraverso movimenti del pan-tilt controllati da servo:

   - *Annuisce* per le risposte corrette
   - *Scuote la testa* per le risposte errate

4. **Utilizza interazione semplice** attivata da una singola pressione di un pulsante

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Questa dimostrazione mostra come l'AI possa interagire con il mondo fisico, creando uno strumento educativo coinvolgente che fornisce feedback visivo immediato sulla correttezza dei compiti.

Puoi usare altri moduli LLM e componenti hardware per costruire i tuoi dispositivi di apprendimento assistiti da AI. Vedi:

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_servo`
        - |link_servo_buy|
    *   - Pan-Tilt
        -
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-
    *   - Campione di compito (stampato o scritto a mano)
        - \-

----------------------------------------------

**Configurazione Hardware**

Per usare il modulo fotocamera comodamente, si raccomanda :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

     L'assemblaggio del pan-tilt potrebbe oscurare alcuni pin, quindi si consiglia di assemblarlo solo quando si utilizza la fotocamera, o di posizionarlo all'esterno dopo l'assemblaggio.


   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Esecuzione del Codice**

#. Crea un Campione di Compito:

   - Scrivi o stampa un semplice problema matematico con risposta
   - Esempio: "5 + 3 = 8" (corretto) o "5 + 3 = 7" (errato)
   - Assicurati una grafia o stampa chiara

#. Esegui il programma:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. Segui le Istruzioni a Schermo:

   - Posiziona il compito sotto la fotocamera
   - Premi il pulsante utente (USR) su Fusion HAT+
   - Osserva la risposta del servo

#. Output Previsto:

   .. code-block:: text

      HOMEWORK GRADING DEMO
      ==================================================
      Instructions:
      1. Place a homework question under the camera
      2. Make sure the question AND answer are visible
      3. Press the User Button (USR) on Fusion HAT to grade
      4. The camera will take a photo
      5. AI will grade the answer
      6. Servo will nod (correct) or shake (incorrect)
      ==================================================

      Waiting for button press...

      ==================================================
      Button pressed - Starting grading process

      Taking photo...
      Photo captured
      Sending to AI for grading...
      AI response: CORRECT
      Answer is correct - nodding head
      ==================================================

----------------------------------------------

**Codice**

Ecco lo script Python completo per la Demo di Correzione dei Compiti:


.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   """
   Homework Grading Demo with Pan-Tilt Camera
   Press User Button to take photo, LLM grades, servo nods or shakes
   """

   import time
   from fusion_hat.llm import OpenAI
   from fusion_hat.servo import Servo
   from fusion_hat.user_button import UserButton
   from picamera2 import Picamera2, Preview

   # ========== LLM SETTINGS ==========
   # Create a secret.py file with: OPENAI_API_KEY = "your-api-key-here"
   try:
       from secret import OPENAI_API_KEY
   except ImportError:
       print("ERROR: Please create a secret.py file with your OpenAI API key")
       print("Example content: OPENAI_API_KEY = 'sk-...'")
       exit()

   # LLM instructions for grading
   INSTRUCTIONS = """You are a homework grading assistant.
   When you see a photo of a homework question with an answer,
   determine if the answer is correct or incorrect.

   Respond with ONLY ONE WORD:
   - If the answer is CORRECT, respond: "CORRECT"
   - If the answer is INCORRECT, respond: "INCORRECT"

   Do not provide any other text, explanations, or justifications.
   Only respond with "CORRECT" or "INCORRECT"."""

   # Initialize LLM
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o"
   )

   # Set LLM settings
   llm.set_max_messages(5)
   llm.set_instructions(INSTRUCTIONS)

   # ========== HARDWARE SETTINGS ==========
   PAN_CHANNEL = 2      # Horizontal servo for shaking head
   TILT_CHANNEL = 3     # Vertical servo for nodding head

   # Servo center positions
   TILT_CENTER = 0      # Looking straight ahead
   PAN_CENTER = 0       # Center position

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Homework Grading Demo...")
   print("-" * 50)

   # Initialize servos
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center servos
   tilt_servo.angle(TILT_CENTER)
   pan_servo.angle(PAN_CENTER)
   time.sleep(1)
   print("Servos ready")

   # Initialize camera
   camera = Picamera2()
   camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
   camera.configure(camera_config)
   camera.start_preview(Preview.QT)
   camera.start()
   time.sleep(2)
   print("Camera ready")

   # Initialize user button
   user_button = UserButton()
   print("User button ready")
   print("-" * 50)

   # ========== SERVO MOVEMENT FUNCTIONS ==========
   def nod_head():
       """
       Nodding head movement for "correct"
       """
       # Look down
       tilt_servo.angle(15)
       time.sleep(0.2)
       # Look up
       tilt_servo.angle(-10)
       time.sleep(0.2)
       # Return to center
       tilt_servo.angle(TILT_CENTER)

   def shake_head():
       """
       Shaking head movement for "incorrect"
       """
       # Look left
       pan_servo.angle(-20)
       time.sleep(0.15)
       # Look right
       pan_servo.angle(20)
       time.sleep(0.15)
       # Look left again
       pan_servo.angle(-15)
       time.sleep(0.15)
       # Return to center
       pan_servo.angle(PAN_CENTER)

   # ========== GRADING FUNCTION ==========
   def grade_homework():
       """
       Main grading function: take photo, send to LLM, move servo
       """
       print("\nTaking photo...")

       # Capture image
       img_path = './homework.jpg'
       camera.capture_file(img_path)
       print("Photo captured")

       # Send to LLM for grading
       print("Sending to AI for grading...")

       prompt = "Look at this homework question and answer. Is the answer correct? Respond with only one word: 'CORRECT' or 'INCORRECT'."

       response = llm.prompt(prompt, image_path=img_path)
       response_text = response.strip().upper()

       print(f"AI response: {response_text}")

       # Move servo based on response
       if "INCORRECT" in response_text:
           print("Answer is incorrect - shaking head")
           shake_head()
       elif "CORRECT" in response_text:
           print("Answer is correct - nodding head")
           nod_head()
       else:
           print(f"Unexpected response: {response_text}")

   # ========== BUTTON CALLBACK ==========
   def on_button_click():
       """
       Called when user button is pressed
       """
       print("\n" + "=" * 50)
       print("Button pressed - Starting grading process")
       grade_homework()
       print("=" * 50)

   # ========== MAIN DEMO ==========
   def main():
       """
       Main demo function
       """
       print("\nHOMEWORK GRADING DEMO")
       print("=" * 50)
       print("Instructions:")
       print("1. Place a homework question under the camera")
       print("2. Make sure the question AND answer are visible")
       print("3. Press the User Button (USR) on Fusion HAT to grade")
       print("4. The camera will take a photo")
       print("5. AI will grade the answer")
       print("6. Servo will nod (correct) or shake (incorrect)")
       print("=" * 50)
       print("\nWaiting for button press...")

       # Set button callback
       user_button.set_on_click(on_button_click)

       # Keep program running
       try:
           while True:
               time.sleep(0.1)
       except KeyboardInterrupt:
           print("\nDemo stopped by user")

   # ========== CLEANUP ==========
   def cleanup():
       """
       Clean up resources
       """
       print("\nCleaning up...")

       # Return servos to center
       tilt_servo.angle(TILT_CENTER)
       pan_servo.angle(PAN_CENTER)

       # Stop camera
       camera.stop()

       print("Demo ended")

   # ========== RUN DEMO ==========
   if __name__ == "__main__":
       try:
           main()
       finally:
           cleanup()

----------------------------------------------

**Comprensione del Codice**

1. Configurazione e Impostazione LLM

   Il sistema utilizza GPT-4o di OpenAI con capacita' di visione per analizzare le immagini:

   .. code-block:: python

      # Importa e inizializza l'LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

      # Imposta istruzioni specifiche per risposte consistenti
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)

      # Limita la cronologia della conversazione per gestire i token
      llm.set_max_messages(5)

2. Inizializzazione Hardware

   Tre componenti hardware vengono inizializzati: servi, fotocamera e pulsante:

   .. code-block:: python

      # Controllo servo per meccanismo pan-tilt
      pan_servo = Servo(PAN_CHANNEL)   # Canale 2 per movimento orizzontale
      tilt_servo = Servo(TILT_CHANNEL) # Canale 3 per movimento verticale

      # Configurazione fotocamera con anteprima
      camera = Picamera2()
      camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
      camera.configure(camera_config)
      camera.start_preview(Preview.QT)
      camera.start()

      # Pulsante utente per l'interazione
      user_button = UserButton()

3. Funzioni di Animazione dei Servo

   Movimenti naturali per annuire e scuotere la testa:

   .. code-block:: python

      def nod_head():
          """Movimento di annuire per le risposte corrette"""
          tilt_servo.angle(15)    # Guarda in basso
          time.sleep(0.2)
          tilt_servo.angle(-10)   # Guarda in alto
          time.sleep(0.2)
          tilt_servo.angle(TILT_CENTER)  # Ritorna al centro

      def shake_head():
          """Movimento di scuotere la testa per le risposte errate"""
          pan_servo.angle(-20)    # Guarda a sinistra
          time.sleep(0.15)
          pan_servo.angle(20)     # Guarda a destra
          time.sleep(0.15)
          pan_servo.angle(-15)    # Guarda di nuovo a sinistra
          time.sleep(0.15)
          pan_servo.angle(PAN_CENTER)  # Ritorna al centro

4. Acquisizione Immagine e Analisi AI

   Il flusso di lavoro principale di correzione:

   .. code-block:: python

      def grade_homework():
          # Acquisisci immagine dalla fotocamera
          img_path = './homework.jpg'
          camera.capture_file(img_path)

          # Invia immagine all'LLM con prompt specifico
          prompt = "Look at this homework question and answer..."
          response = llm.prompt(prompt, image_path=img_path)
          response_text = response.strip().upper()

          # Interpreta la risposta e attiva il movimento appropriato del servo
          if "INCORRECT" in response_text:
              shake_head()
          elif "CORRECT" in response_text:
              nod_head()

5. Gestione degli Eventi del Pulsante

   Sistema semplice di callback per l'interazione utente:

   .. code-block:: python

      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()

      # Assegna callback al pulsante
      user_button.set_on_click(on_button_click)

6. Ciclo Principale dell'Applicazione

   Ciclo principale minimo che attende le pressioni dei pulsanti:

   .. code-block:: python

      def main():
          print("Waiting for button press...")
          user_button.set_on_click(on_button_click)

          # Mantieni il programma in esecuzione fino a interruzione
          try:
              while True:
                  time.sleep(0.1)  # Attesa a basso utilizzo CPU
          except KeyboardInterrupt:
              print("\nDemo stopped by user")

7. Pulizia delle Risorse

   Procedura di spegnimento corretta:

   .. code-block:: python

      def cleanup():
          # Riporta i servi in posizione neutrale
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)

          # Ferma la fotocamera
          camera.stop()

----------------------------------------------

**Risoluzione dei Problemi**

- Nessun modulo ``picamera2``

  Installa la libreria richiesta:

  .. code-block:: bash

     sudo apt update
     sudo apt install python3-picamera2

- Fotocamera non rilevata

  1. Controlla la connessione della fotocamera: assicurati che il cavo a nastro sia inserito correttamente
  2. Verifica che la fotocamera sia abilitata: ``sudo raspi-config`` -> Interface Options -> Camera
  3. Prova la fotocamera indipendentemente: ``libcamera-hello``

- I servi non si muovono

  1. Controlla le connessioni di alimentazione: i servi necessitano di 5V
  2. Verifica che i canali dei servi corrispondano al codice (Canali 2 e 3)
  3. Prova i servi indipendentemente con semplici comandi angolari

- L'AI non risponde o da' errore

  1. Verifica che la chiave API in ``secret.py`` sia corretta
  2. Controlla la connessione Internet: ``ping 8.8.8.8``
  3. Assicurati di avere crediti nel tuo account OpenAI
  4. Verifica che il modello "gpt-4o" sia disponibile nel tuo account

- Movimenti dei servi errati

  1. Controlla se i servi pan e tilt sono invertiti
  2. Regola i valori angolari nelle funzioni ``nod_head()`` e ``shake_head()``
  3. Verifica le posizioni centrali dei servi (potrebbero necessitare calibrazione)

- Immagine troppo sfocata o scura

  1. Assicura un'illuminazione adeguata sul compito
  2. Regola la messa a fuoco della fotocamera se regolabile
  3. Posiziona la fotocamera a 15-30 cm dal foglio
  4. Usa penna/marcatore ad alto contrasto per la scrittura a mano

- Il pulsante non risponde

  1. Controlla se il LED del pulsante utente si accende quando premuto
  2. Verifica che la callback del pulsante sia registrata
  3. Prova il pulsante con una semplice istruzione print

- L'AI restituisce risposte inaspettate

  1. Controlla la formattazione del prompt nel codice
  2. Assicurati che l'immagine mostri chiaramente domanda E risposta
  3. Prova prima con problemi aritmetici molto semplici

----------------------------------------------


Questa demo di correzione dei compiti mostra come i modelli di visione AI possano interagire con hardware fisico per creare esperienze educative coinvolgenti, fondendo l'intelligenza digitale con meccanismi di feedback tangibili!
