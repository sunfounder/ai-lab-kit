.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_book_cover_analyzer:

(Esempio) Esperto di Libri
===============================

**Introduzione**

In questo progetto, costruirai un **analizzatore di copertine di libri basato su AI** che utilizza la visione artificiale e l'elaborazione del linguaggio naturale per identificare libri dalle loro copertine. Il sistema acquisisce immagini di copertine usando una fotocamera Raspberry Pi, le invia a un modello LLM (qui usiamo il modello di visione GPT-4o di OpenAI) per l'analisi, e fornisce feedback audio sul titolo, l'autore, il riepilogo e l'accoglienza del libro utilizzando la sintesi vocale.

Il progetto combina piu' tecnologie:

- Acquisizione fotocamera con Picamera2
- Analisi delle immagini con le capacita' visive di GPT-4o
- Conversione testo-parola per risposte audio
- LED RGB per feedback visivo di stato
- Pulsante fisico per interazione intuitiva

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Book_Expert.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Per usare altri modelli LLM, consulta :ref:`py_online_llm` .

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - Modulo Fotocamera Raspberry Pi
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Libro (per test)
        - \-

----------------------------------------------

**Schema di Collegamento**

#. Per usare il modulo fotocamera comodamente, si raccomanda :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

     L'assemblaggio del pan-tilt potrebbe oscurare alcuni pin, quindi si consiglia di assemblarlo solo quando si utilizza la fotocamera, o di posizionarlo all'esterno dopo l'assemblaggio.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Collega i componenti al Fusion HAT+ come segue:

   .. image:: img/fzz/llm_book_bb.png
      :width: 80%
      :align: center

#. Il pulsante utente e' gia' integrato nel Fusion HAT+ e non richiede cablaggio aggiuntivo. Si trova vicino alla porta BATTERIA.*

   .. image:: img/3.1_user_button.png
      :width: 50%

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

**Esecuzione dell'Esempio**

#. Accedi al desktop del Raspberry Pi:

   * :ref:`remote_desktop`: Usa **VNC** per un'esperienza desktop completa.
   * |link_rpi_connect|: Usa **Raspberry Pi Connect** per accedere al tuo Pi in modo sicuro da qualsiasi browser.

#. Apri un Terminale e vai alla cartella del codice:

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_bookexpert.py

#. Quando lo script viene eseguito:

   * Si aprira' una finestra di anteprima della fotocamera
   * Il LED RGB si illuminera' di blu, indicando lo stato di pronto
   * Posiziona una copertina di libro davanti alla fotocamera
   * Premi il pulsante USR sul Fusion HAT+ (che si trova vicino alla porta BATTERIA)
   * Il sistema:

     1. Acquisira' una foto (LED diventa giallo)
     2. Analizzera' con AI (LED diventa viola)
     3. Pronuncera' l'analisi (LED diventa verde)
     4. Tornera' allo stato di pronto (LED diventa blu)
     5. Se si verifica un errore, il LED diventera' rosso

   * Le foto vengono salvate in ``~/Pictures/book_covers/``
   * Premi Ctrl+C per uscire

----------------------------------------------

**Codice**

Ecco lo script Python completo per l'Analizzatore di Copertine di Libri AI:

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import os
   import time
   import re
   import base64
   import threading
   from pathlib import Path
   from picamera2 import Picamera2, Preview
   from fusion_hat.user_button import UserButton
   from fusion_hat.modules import RGB_LED
   from fusion_hat.pwm import PWM
   from fusion_hat.llm import OpenAI
   from fusion_hat.tts import OpenAI_TTS
   from secret import OPENAI_API_KEY

   class BookCoverAnalyzer:
       def __init__(self):
           # Initialize LED for status feedback
           self.rgb_led = RGB_LED(PWM(0), PWM(1), PWM(2), common=RGB_LED.CATHODE)
           self.set_led_color("blue")  # Ready state

           # Initialize OpenAI LLM for image analysis
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",  # GPT-4o supports image input
           )

           # Initialize TTS for audio responses
           self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
           self.tts.set_voice(self.tts.Voice.ALLOY)

           # Initialize camera
           self.camera = Picamera2()
           self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))

           # Initialize button
           self.btn = UserButton()

           # Set up directories
           self.real_user = os.getenv("SUDO_USER") or os.getlogin()
           self.user_home = f"/home/{self.real_user}"
           self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
           self.pictures_dir.mkdir(parents=True, exist_ok=True)

           # Threading locks
           self.photo_lock = threading.Lock()
           self.photo_index = 1

           # Set LLM instructions
           self.instructions = """You are a book expert. Analyze book covers that are sent to you.

           When you receive a book cover image, provide:
           1. Book title (if identifiable from cover)
           2. Author (if identifiable from cover)
           3. Brief summary of what the book is about (50 words)
           4. Overall rating/reception (e.g., "Highly acclaimed", "Classic", "Popular", etc.)

           Keep your response under 100 words total.
           Speak in a friendly, informative tone suitable for an audio response.

           If the image is not a book cover or is unclear, politely say you can't identify it and ask for another photo."""

           self.llm.set_max_messages(10)
           self.llm.set_instructions(self.instructions)

       def set_led_color(self, color_name):
           """Set RGB LED color for status feedback"""
           color_map = {
               "red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "yellow": (255, 255, 0),
               "purple": (255, 0, 255),
               "white": (255, 255, 255),
               "off": (0, 0, 0),
           }

           if color_name in color_map:
               self.rgb_led.color(color_map[color_name])

       def capture_photo(self):
           """Capture a photo and return the filepath"""
           with self.photo_lock:
               filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
               print(f"\n📸 Capturing photo: {filepath}")

               # LED feedback: yellow for capturing
               self.set_led_color("yellow")

               # Capture image
               self.camera.capture_file(str(filepath))

               # Increment counter for next photo
               self.photo_index += 1

               print("Photo captured successfully")
               return str(filepath)

       def analyze_book_cover(self, image_path):
           """Send book cover image to OpenAI for analysis"""
           print("\n Analyzing book cover...")

           # LED feedback: purple for processing
           self.set_led_color("purple")

           try:
               # use fusion_hat.llm's prompt method to process the image
               prompt_text = "Please analyze this book cover and tell me about the book. Provide: 1) Book title if identifiable, 2) Author if identifiable, 3) Brief summary, 4) Overall rating/reception. Keep under 100 words."

               print("Sending to AI for analysis...")

               # method1: non-streaming response
               response = self.llm.prompt(prompt_text, image_path=image_path)

               # if the response is a string, use it directly
               if isinstance(response, str):
                   analysis = response
               else:
                   # if response is not a string, try to convert it to a string
                   analysis = str(response)

               print(f"\n Analysis:\n{analysis}")

               # LED feedback: green for success
               self.set_led_color("green")

               return analysis

           except Exception as e:
               print(f"Error analyzing image: {e}")
               print(f"Error type: {type(e)}")

               # method2: streaming response
               try:
                   print("Trying stream method...")
                   stream_response = self.llm.prompt(prompt_text, stream=True, image_path=image_path)

                   # receive the stream response
                   analysis_parts = []
                   for next_word in stream_response:
                       if next_word:
                           analysis_parts.append(next_word)

                   analysis = ''.join(analysis_parts)
                   print(f"\n Analysis (stream):\n{analysis}")

                   # LED feedback: green for success
                   self.set_led_color("green")
                   return analysis

               except Exception as e2:
                   print(f"Stream method also failed: {e2}")

                   # LED feedback: red for error
                   self.set_led_color("red")
                   return "Sorry, I couldn't analyze the book cover. Please make sure the book cover is clearly visible and try again."

       def speak_response(self, text):
           """Convert text to speech"""
           print("\nSpeaking response...")

           # Clean up text for TTS (remove markdown, etc.)
           clean_text = re.sub(r'[*_\[\]()#]', '', text)

           # Speak with friendly instructions
           self.tts.say(clean_text, instructions="speak clearly and warmly")
           print("Response spoken")

           # Return to ready state
           self.set_led_color("blue")

       def button_handler(self):
           """Handle button press: capture photo, analyze, and speak"""
           print("\n" + "="*50)
           print("Processing request...")

           # Step 1: Capture photo
           try:
               image_path = self.capture_photo()
           except Exception as e:
               print(f"Failed to capture photo: {e}")
               self.set_led_color("red")
               self.tts.say("Sorry, I couldn't take a photo. Please try again.")
               self.set_led_color("blue")
               return

           # Step 2: Analyze with AI
           analysis = self.analyze_book_cover(image_path)

           # Step 3: Speak the analysis
           self.speak_response(analysis)

           print(f"Complete! Photo saved at: {image_path}")
           print("="*50 + "\n")

       def run(self):
           """Main program loop"""
           # Set button callback
           self.btn.set_on_click(self.button_handler)

           # Start camera preview
           print("Starting camera preview...")
           self.camera.start_preview(Preview.QT)
           self.camera.start()

           # LED feedback: blue for ready
           self.set_led_color("blue")

           print("\n" + "="*50)
           print("BOOK COVER ANALYZER")
           print("="*50)
           print("\nReady to analyze book covers!")
           print("Press the USR button to capture and analyze a book cover")
           print("I will speak the analysis aloud")
           print("LED colors:")
           print("   Blue: Ready")
           print("   Yellow: Capturing photo")
           print("   Purple: Analyzing with AI")
           print("   Green: Analysis successful")
           print("   Red: Error occurred")
           print(f"Photos saved to: {self.pictures_dir}")
           print("Press Ctrl+C to exit")
           print("="*50 + "\n")

           try:
               # Keep program running
               while True:
                   time.sleep(0.1)

           except KeyboardInterrupt:
               print("\nExiting...")

           finally:
               # Cleanup
               self.camera.stop_preview()
               self.camera.close()
               self.set_led_color("off")
               print("Cleanup complete")

   if __name__ == "__main__":
       analyzer = BookCoverAnalyzer()
       analyzer.run()

----------------------------------------------

**Comprensione del Codice**

1. Inizializzazione della Fotocamera

   La libreria Picamera2 fornisce un'interfaccia moderna per il controllo della fotocamera Raspberry Pi, supportando sia l'acquisizione di immagini che l'anteprima.

   .. code-block:: python

      self.camera = Picamera2()
      self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))

      # Avvia anteprima e fotocamera
      self.camera.start_preview(Preview.QT)
      self.camera.start()

2. Acquisizione Immagini con Thread Safety

   Il metodo capture_photo utilizza lock di threading per prevenire acquisizioni simultanee multiple e garantisce una corretta denominazione dei file.

   .. code-block:: python

      def capture_photo(self):
          with self.photo_lock:
              filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
              self.camera.capture_file(str(filepath))
              self.photo_index += 1
              return str(filepath)

3. Analisi Visiva AI

   Il sistema utilizza le capacita' visive di GPT-4o per analizzare le copertine dei libri. Due metodi (streaming e non-streaming) sono implementati per robustezza.

   .. code-block:: python

      def analyze_book_cover(self, image_path):
          prompt_text = "Please analyze this book cover..."

          # Metodo 1: Risposta non in streaming
          response = self.llm.prompt(prompt_text, image_path=image_path)

          # Metodo 2: Fallback allo streaming se necessario
          stream_response = self.llm.prompt(prompt_text, stream=True, image_path=image_path)

4. Conversione Testo-Parola

   L'API TTS di OpenAI converte l'analisi dell'AI in un parlato dal suono naturale con opzioni vocali configurabili.

   .. code-block:: python

      self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
      self.tts.set_voice(self.tts.Voice.ALLOY)

      def speak_response(self, text):
          clean_text = re.sub(r'[*_\[\]()#]', '', text)  # Rimuovi markdown
          self.tts.say(clean_text, instructions="speak clearly and warmly")

5. Sistema di Feedback di Stato

   Il LED RGB fornisce feedback visivo durante tutto il processo utilizzando codici colore:

   .. code-block:: python

      def set_led_color(self, color_name):
          color_map = {
              "red": (255, 0, 0),      # Errore
              "green": (0, 255, 0),    # Successo
              "blue": (0, 0, 255),     # Pronto
              "yellow": (255, 255, 0), # Acquisizione
              "purple": (255, 0, 255), # Elaborazione
          }
          self.rgb_led.color(color_map[color_name])

6. Gestione degli Eventi del Pulsante

   Il pulsante utente attiva l'intero flusso di lavoro di analisi attraverso una callback di evento.

   .. code-block:: python

      def button_handler(self):
          # 1. Acquisisci foto
          image_path = self.capture_photo()
          # 2. Analizza con AI
          analysis = self.analyze_book_cover(image_path)
          # 3. Pronuncia l'analisi
          self.speak_response(analysis)

      # Imposta callback
      self.btn.set_on_click(self.button_handler)

7. Gestione dei File

   Le foto vengono automaticamente organizzate in cartelle con numerazione sequenziale.

   .. code-block:: python

      self.real_user = os.getenv("SUDO_USER") or os.getlogin()
      self.user_home = f"/home/{self.real_user}"
      self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
      self.pictures_dir.mkdir(parents=True, exist_ok=True)

----------------------------------------------

**Risoluzione dei Problemi**

- Errore "Camera not detected"

  - Assicurati che il cavo a nastro della fotocamera sia inserito correttamente (contatti dorati rivolti nella direzione corretta)
  - Esegui ``sudo raspi-config`` e abilita l'interfaccia della fotocamera
  - Riavvia dopo aver abilitato la fotocamera

- "No preview window appears"

  - Assicurati di essere in esecuzione su un Raspberry Pi con ambiente desktop
  - Per il funzionamento headless, rimuovi o modifica il codice di anteprima
  - Controlla se hai sufficiente memoria GPU allocata

- "OpenAI API error"

  - Verifica che la tua chiave API in ``secret.py`` sia corretta e abbia crediti sufficienti
  - Controlla la connettivita' Internet: ``ping 8.8.8.8``
  - Assicurati che il tuo account abbia accesso a GPT-4o e all'API TTS

- "TTS audio not playing"

  - Controlla se l'uscita audio e' configurata: ``sudo raspi-config`` -> **System Options** -> **Audio**
  - Prova l'audio con: ``speaker-test -t sine -f 440``
  - Assicurati che altoparlante/cuffie siano collegati al jack audio corretto

- "Button press not detected"

  - Controlla se il LED del pulsante utente si accende quando premuto
  - Assicurati che Fusion HAT+ sia correttamente inserito sui pin GPIO
  - Verifica che la callback del pulsante sia impostata correttamente

- "Image analysis returns generic responses"

  - Assicura una buona illuminazione durante l'acquisizione delle copertine
  - Posiziona la copertina del libro direttamente nel fotogramma della fotocamera
  - Prova prima con libri ben noti per un migliore riconoscimento
  - Pulisci l'obiettivo della fotocamera se e' sfocato

----------------------------------------------

Questo progetto dimostra la potente combinazione di visione artificiale, elaborazione del linguaggio naturale e computing fisico per creare un sistema intelligente di analisi dei libri. Mostra come l'AI possa migliorare le interazioni quotidiane con oggetti fisici come i libri, rendendo le informazioni piu' accessibili e coinvolgenti!
