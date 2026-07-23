.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_book_cover_analyzer:

(Exemple) Expert en livres
===========================

**Introduction**

Dans ce projet, vous allez construire un **analyseur de couvertures de livres alimente par l'IA** qui utilise la vision par ordinateur et le traitement du langage naturel pour identifier des livres a partir de leurs couvertures. Le systeme capture des images de couvertures de livres avec une camera Raspberry Pi, les envoie a un modele LLM (ici nous utilisons le modele de vision GPT-4o d'OpenAI) pour analyse, et fournit un retour audio sur le titre, l'auteur, le resume et la reception du livre en utilisant la synthese vocale.

Le projet combine plusieurs technologies :

- Capture d'image avec Picamera2
- Analyse d'image avec les capacites de vision de GPT-4o
- Synthese vocale pour les reponses audio
- LED RGB pour le retour visuel d'etat
- Bouton physique pour une interaction intuitive

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Book_Expert.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Pour utiliser les autres modeles LLM, veuillez vous referer a :ref:`py_online_llm` .

----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
    *   - Module camera Raspberry Pi
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_rgb_led`
        - |link_rgb_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Livre (pour le test)
        - \-

----------------------------------------------

**Schema de cablage**

#. Pour utiliser le module camera facilement, :ref:`assemble_fusion_hat_pan_tilt` est recommande.

   .. note::

     L'assemblage du pantilt peut obstruer certaines broches, il est donc recommande de ne l'assembler que lors de l'utilisation de la camera, ou de le placer a l'exterieur apres assemblage.


   .. image:: ../quick_start/img/gimbal_assemble.png

#. Connectez les composants au Fusion HAT+ comme suit :

   .. image:: img/fzz/llm_book_bb.png
      :width: 80%
      :align: center

#. Le bouton utilisateur est deja integre au Fusion HAT+ et ne necessite pas de cablage supplementaire. Il se trouve pres du port BATTERIE.*

   .. image:: img/3.1_user_button.png
      :width: 50%

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

**Executer l'exemple**

#. Accedez au bureau du Raspberry Pi :

   * :ref:`remote_desktop`: Utilisez **VNC** pour une experience de bureau complete.
   * |link_rpi_connect|: Utilisez **Raspberry Pi Connect** pour acceder a votre Pi en toute securite depuis n'importe quel navigateur.

#. Ouvrez un terminal et allez dans le dossier du code :

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_bookexpert.py

#. Lorsque le script s'execute :

   * Une fenetre d'apercu de la camera s'ouvre
   * La LED RGB s'allume en bleu, indiquant l'etat de pret
   * Placez une couverture de livre devant la camera
   * Appuyez sur le bouton USR du Fusion HAT+ (qui se trouve pres du port BATTERIE)
   * Le systeme va :

     1. Capturer une photo (la LED devient jaune)
     2. Analyser avec l'IA (la LED devient violette)
     3. Prononcer l'analyse (la LED devient verte)
     4. Revenir a l'etat de pret (la LED devient bleue)
     5. Si une erreur se produit, la LED devient rouge

   * Les photos sont enregistrees dans ``~/Pictures/book_covers/``
   * Appuyez sur Ctrl+C pour quitter

----------------------------------------------

**Code**

Voici le script Python complet pour l'Analyseur de couvertures de livres IA :

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
               print(f"\n Capturing photo: {filepath}")

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

**Comprendre le code**

1. Initialisation de la camera

   La bibliotheque Picamera2 fournit une interface moderne pour le controle de la camera Raspberry Pi, prenant en charge la capture d'image et l'apercu.

   .. code-block:: python

      self.camera = Picamera2()
      self.camera.configure(self.camera.create_preview_configuration(main={"size": (800, 600)}))

      # Start preview and camera
      self.camera.start_preview(Preview.QT)
      self.camera.start()

2. Capture d'image avec securite des threads

   La methode capture_photo utilise des verrous de threading pour empecher les captures simultanees et garantit un nommage correct des fichiers.

   .. code-block:: python

      def capture_photo(self):
          with self.photo_lock:
              filepath = self.pictures_dir / f"book_cover_{self.photo_index:03d}.jpg"
              self.camera.capture_file(str(filepath))
              self.photo_index += 1
              return str(filepath)

3. Analyse IA de la vision

   Le systeme utilise les capacites de vision de GPT-4o pour analyser les couvertures de livres. Deux methodes (streaming et non-streaming) sont implementees pour la robustesse.

   .. code-block:: python

      def analyze_book_cover(self, image_path):
          prompt_text = "Please analyze this book cover..."

          # Method 1: Non-streaming response
          response = self.llm.prompt(prompt_text, image_path=image_path)

          # Method 2: Fallback to streaming if needed
          stream_response = self.llm.prompt(prompt_text, stream=True, image_path=image_path)

4. Synthese vocale

   L'API TTS d'OpenAI convertit l'analyse de l'IA en parole naturelle avec des options de voix configurables.

   .. code-block:: python

      self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
      self.tts.set_voice(self.tts.Voice.ALLOY)

      def speak_response(self, text):
          clean_text = re.sub(r'[*_\[\]()#]', '', text)  # Remove markdown
          self.tts.say(clean_text, instructions="speak clearly and warmly")

5. Systeme de retour d'etat

   La LED RGB fournit un retour visuel tout au long du processus en utilisant un code couleur :

   .. code-block:: python

      def set_led_color(self, color_name):
          color_map = {
              "red": (255, 0, 0),      # Error
              "green": (0, 255, 0),    # Success
              "blue": (0, 0, 255),     # Ready
              "yellow": (255, 255, 0), # Capturing
              "purple": (255, 0, 255), # Processing
          }
          self.rgb_led.color(color_map[color_name])

6. Gestion des evenements du bouton

   Le bouton utilisateur declenche l'ensemble du flux de travail d'analyse via un rappel d'evenement.

   .. code-block:: python

      def button_handler(self):
          # 1. Capture photo
          image_path = self.capture_photo()
          # 2. Analyze with AI
          analysis = self.analyze_book_cover(image_path)
          # 3. Speak the analysis
          self.speak_response(analysis)

      # Set callback
      self.btn.set_on_click(self.button_handler)

7. Gestion des fichiers

   Les photos sont automatiquement organisees dans des dossiers avec une numerotation sequentielle.

   .. code-block:: python

      self.real_user = os.getenv("SUDO_USER") or os.getlogin()
      self.user_home = f"/home/{self.real_user}"
      self.pictures_dir = Path(self.user_home) / "Pictures" / "book_covers"
      self.pictures_dir.mkdir(parents=True, exist_ok=True)

----------------------------------------------

**Depannage**

- Erreur "Camera not detected"

  - Assurez-vous que le cable ruban de la camera est correctement insere (contacts dores orientes dans le bon sens)
  - Executez ``sudo raspi-config`` et activez l'interface camera
  - Redemarrez apres avoir active la camera

- "No preview window appears"

  - Assurez-vous d'executer le programme sur un Raspberry Pi avec un environnement de bureau
  - Pour un fonctionnement sans tete, supprimez ou modifiez le code d'apercu
  - Verifiez si vous avez suffisamment de memoire GPU allouee

- "OpenAI API error"

  - Verifiez que votre cle API dans ``secret.py`` est correcte et dispose de credits suffisants
  - Verifiez la connectivite Internet : ``ping 8.8.8.8``
  - Assurez-vous que votre compte a acces a GPT-4o et a l'API TTS

- "TTS audio not playing"

  - Verifiez si la sortie audio est configuree : ``sudo raspi-config`` → **System Options** → **Audio**
  - Testez l'audio avec : ``speaker-test -t sine -f 440``
  - Assurez-vous que votre haut-parleur/casque est connecte a la bonne prise audio

- "Button press not detected"

  - Verifiez si la LED du bouton utilisateur s'allume lorsqu'on appuie
  - Assurez-vous que le Fusion HAT+ est correctement installe sur les broches GPIO
  - Verifiez que le rappel du bouton est correctement defini

- "Image analysis returns generic responses"

  - Assurez-vous d'un bon eclairage lors de la capture des couvertures de livres
  - Positionnez la couverture du livre bien droite dans le cadre de la camera
  - Essayez d'abord avec des livres bien connus pour une meilleure reconnaissance
  - Nettoyez l'objectif de la camera s'il est flou

----------------------------------------------

Ce projet demontre la puissante combinaison de la vision par ordinateur, du traitement du langage naturel et de l'informatique physique pour creer un systeme intelligent d'analyse de livres. Il montre comment l'IA peut enrichir les interactions quotidiennes avec des objets physiques comme les livres, rendant l'information plus accessible et engageante !