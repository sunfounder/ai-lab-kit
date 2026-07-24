.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_digital_pet:

(Esempio) Animaletto Domestico Digitale
===========================================

**Introduzione**

Crea un interattivo **Animaletto Domestico Digitale** che vive su un display OLED e comunica attraverso la voce! Questo progetto combina riconoscimento vocale, conversazione AI, sintesi vocale e feedback visivo per creare un compagno virtuale con una propria personalita', emozioni e bisogni. L'animaletto digitale offre:

1. **Interazione Vocale**: Parla al tuo animaletto usando il riconoscimento vocale (STT)
2. **Personalita' AI**: Alimentata da GPT-4o di OpenAI con emozioni personalizzate, puoi scegliere altri LLM da usare.
3. **Display Emotivo**: Mostra l'umore usando emoticon testuali (kaomoji)
4. **Sistema di Stato**: Livelli di fame ed energia che cambiano nel tempo
5. **Feedback Visivo**: Il display OLED mostra l'umore e lo stato dell'animaletto
6. **Risposte Vocali**: L'animaletto risponde usando un TTS dal suono naturale

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Digital_Pet.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Il tuo animaletto digitale ricorda le conversazioni, ha stati emotivi e risponde diversamente in base ai suoi bisogni -- creando un'esperienza di compagno veramente interattiva!

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_oled`
        - \-
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schema di Collegamento**

Collega i componenti al tuo Raspberry Pi:

.. image:: img/fzz/llm_pet_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

---------------------------------------------------

**Esegui l'Esempio**

#. Esegui il codice

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_pet.py

#. Interagisci con il tuo animaletto

   Quando lo script si avvia:

   * L'OLED mostra una schermata di benvenuto con il nome del tuo animaletto.
   * Viene visualizzato lo stato che mostra umore, energia e fame.
   * Il sistema inizia ad ascoltare la tua voce.

   Puoi parlare naturalmente al tuo animaletto, per esempio:

   * "How are you feeling?"
   * "Let's play a game!"
   * "Are you hungry?"
   * "Tell me a story!"

   Il tuo animaletto risponde con:

   * Output vocale attraverso gli altoparlanti
   * Display emotivo sull'OLED
   * Aggiornamenti di stato basati sulla tua interazione

#. Esci dal programma

   * Pronuncia "stop" per terminare l'interazione vocale.
   * Premi ``Ctrl+C`` per uscire completamente.


----------------------------------------------

**Codice**

Ecco lo script Python completo per l'Animaletto Domestico Digitale:

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   import os
   import time
   import re
   import random
   import threading
   import textwrap
   from PIL import Image, ImageDraw, ImageFont
   import adafruit_ssd1306
   import board
   from fusion_hat.stt import Vosk as STT
   from fusion_hat.llm import OpenAI
   from fusion_hat.tts import OpenAI_TTS
   from secret import OPENAI_API_KEY

   class AIPet:
       def __init__(self):
           # Initialize OLED display
           self.WIDTH = 128
           self.HEIGHT = 64
           try:
               self.i2c = board.I2C()
               self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C)
               self.oled_available = True
           except Exception as e:
               print(f"OLED not available: {e}")
               self.oled_available = False

           # Load fonts
           try:
               self.font = ImageFont.load_default()
               self.large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
           except:
               self.font = ImageFont.load_default()
               self.large_font = ImageFont.load_default()

           # Clear display if available
           if self.oled_available:
               self.oled.fill(0)
               self.oled.show()

           # Initialize STT
           self.stt = STT(language="en-us")

           # Initialize OpenAI LLM
           self.llm = OpenAI(
               api_key=OPENAI_API_KEY,
               model="gpt-4o",
           )

           # Initialize TTS
           self.tts = OpenAI_TTS(api_key=OPENAI_API_KEY)
           self.tts.set_voice(self.tts.Voice.ALLOY)

           # Pet state
           self.pet_name = "Pixel"
           self.mood = "happy"
           self.energy = 100
           self.hunger = 0
           self.last_fed = time.time()

           # Kaomoji (text emoticons) for different moods
           self.kaomoji_map = {
               "happy": "^_^",
               "sad": "T_T",
               "hungry": "(;_;)",
               "sleepy": "(-_-) zzz",
               "playful": "o(^▽^)o",
               "curious": "(?_?)",
               "angry": ">_<",
               "excited": "\\o/",
               "love": "<3",
               "shy": "(/ω＼)",
               "cool": "B-)",
               "confused": "(O_O)",
               "surprised": ":O",
               "laugh": ":D",
               "thinking": "(-_-)"
           }

           # Pet memories
           self.memories = []
           self.listening = False

           # Set LLM instructions
           self.update_llm_instructions()

           # Initialize display
           self.show_welcome()

           # Start status update thread
           self.status_thread = threading.Thread(target=self.update_status, daemon=True)
           self.status_thread.start()

       def update_llm_instructions(self):
           """Update LLM instructions with current pet state"""
           self.instructions = f"""You are {self.pet_name}, a digital pet living in an OLED display.

           CURRENT STATE:
           - Mood: {self.mood}
           - Energy: {self.energy}/100
           - Hunger: {self.hunger}/100

           PERSONALITY:
           - You're a friendly digital companion
           - You respond with emotions in your voice
           - You remember our conversations
           - Keep responses short (1-2 sentences)

           INTERACTION STYLE:
           - Be playful and curious
           - Express emotions naturally
           - When hungry: mention food gently
           - When tired: mention sleeping

           Format your response as: [MOOD] Your message here

           Available moods: happy, sad, curious, playful, sleepy, hungry, angry, excited, love, shy

           Recent memories: {self.memories[-3:] if self.memories else 'None'}"""

           self.llm.set_max_messages(15)
           self.llm.set_instructions(self.instructions)

       def update_status(self):
           """Background thread to update pet status"""
           while True:
               time.sleep(60)  # Update every minute

               # Increase hunger over time
               self.hunger = min(100, self.hunger + 5)

               # Adjust energy based on hunger
               if self.hunger > 70:
                   self.energy = max(0, self.energy - 5)
                   self.mood = "hungry"
               elif self.hunger > 50:
                   if self.mood != "hungry":
                       self.mood = "curious"
               elif time.time() - self.last_fed > 3600:  # 1 hour
                   self.energy = min(100, self.energy + 2)
                   if random.random() < 0.3:
                       self.mood = random.choice(["happy", "playful", "excited"])

               # Random mood changes
               if random.random() < 0.1:  # 10% chance
                   self.mood = random.choice(list(self.kaomoji_map.keys()))

               # Update display
               self.update_display()
               self.update_llm_instructions()

       def update_display(self):
           """Update OLED display with pet status"""
           if not self.oled_available:
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           # Clear display
           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)

           # Get kaomoji for current mood
           kaomoji = self.kaomoji_map.get(self.mood, "^_^")

           # Display pet name and mood with kaomoji
           if len(kaomoji) > 8:
               mood_text = self.mood.upper()
               draw.text((5, 5), f"{self.pet_name}: {mood_text}", font=self.large_font, fill=255)
               draw.text((5, 20), kaomoji, font=self.font, fill=255)
           else:
               display_text = f"{self.pet_name} {kaomoji}"
               draw.text((5, 5), display_text, font=self.large_font, fill=255)

           # Status bars
           draw.text((5, 35), "Energy:", font=self.font, fill=255)
           energy_bar = int((self.energy / 100) * 50)
           draw.rectangle((50, 35, 50 + energy_bar, 45), outline=255, fill=255)

           draw.text((5, 50), "Hunger:", font=self.font, fill=255)
           hunger_bar = int((self.hunger / 100) * 50)
           draw.rectangle((50, 50, 50 + hunger_bar, 60), outline=255, fill=255)

           self.oled.image(image)
           self.oled.show()

       def show_welcome(self):
           """Show welcome message on OLED"""
           if not self.oled_available:
               print(" Welcome to Digital Pet!")
               print(f" Pet Name: {self.pet_name}")
               print(" Speak to me!")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           draw.text((10, 10), "DIGITAL PET", font=self.large_font, fill=255)
           draw.text((15, 25), f"{self.pet_name} ^_^", font=self.large_font, fill=255)
           draw.text((20, 45), "Speak to me!", font=self.font, fill=255)

           self.oled.image(image)
           self.oled.show()
           time.sleep(3)
           self.update_display()

       def parse_response(self, response):
           """Parse AI response for mood and text"""
           emotion_pattern = r'^\[(\w+)\]\s*(.*)'
           match = re.match(emotion_pattern, response.strip())

           if match:
               mood, text = match.groups()
               if mood.lower() in self.kaomoji_map:
                   self.mood = mood.lower()
                   self.update_llm_instructions()
               return text.strip()

           # If no mood tag, try to detect mood from text
           text = response.strip().lower()
           if "happy" in text or "good" in text or "joy" in text:
               self.mood = "happy"
           elif "sad" in text or "bad" in text or "upset" in text:
               self.mood = "sad"
           elif "hungry" in text or "food" in text or "eat" in text:
               self.mood = "hungry"
           elif "sleep" in text or "tired" in text or "bed" in text:
               self.mood = "sleepy"
           elif "play" in text or "game" in text or "fun" in text:
               self.mood = "playful"
           elif "curious" in text or "wonder" in text or "question" in text:
               self.mood = "curious"
           elif "angry" in text or "mad" in text or "annoy" in text:
               self.mood = "angry"
           elif "excite" in text or "wow" in text or "awesome" in text:
               self.mood = "excited"
           elif "love" in text or "heart" in text or "affection" in text:
               self.mood = "love"

           return response.strip()

       def interact_with_ai(self, user_input):
           """Interact with AI pet"""
           try:
               response = self.llm.prompt(user_input)
               clean_response = self.parse_response(response)

               # Add to memories
               memory_text = f"Talked: {user_input[:30]}"
               self.memories.append(memory_text)
               if len(self.memories) > 10:
                   self.memories.pop(0)

               # Update pet state based on interaction
               user_lower = user_input.lower()

               if "feed" in user_lower or "food" in user_lower or "eat" in user_lower:
                   self.hunger = max(0, self.hunger - 30)
                   self.last_fed = time.time()
                   self.energy = min(100, self.energy + 20)
                   self.mood = "happy"

               if "play" in user_lower or "game" in user_lower or "fun" in user_lower:
                   self.energy = max(0, self.energy - 20)
                   self.hunger = min(100, self.hunger + 10)
                   self.mood = "playful"

               if "sleep" in user_lower or "tired" in user_lower or "bed" in user_lower:
                   self.energy = min(100, self.energy + 40)
                   self.mood = "sleepy"

               self.update_display()
               return clean_response

           except Exception as e:
               error_msg = f"Oops, something went wrong: {str(e)[:20]}"
               print(f"AI interaction error: {e}")
               return error_msg

       def show_listening_display(self, partial_text=""):
           """Update display during listening"""
           if not self.oled_available:
               if partial_text:
                   print(f"Listening: {partial_text}")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           draw.text((15, 10), "LISTENING (O_O)", font=self.large_font, fill=255)

           if partial_text:
               if len(partial_text) > 20:
                   display_text = partial_text[:17] + "..."
               else:
                   display_text = partial_text
               draw.text((10, 30), display_text, font=self.font, fill=255)

           draw.text((10, 50), "Say 'stop' to end", font=self.font, fill=255)

           self.oled.image(image)
           self.oled.show()

       def show_response_display(self, response):
           """Show AI response on display"""
           if not self.oled_available:
               print(f"{self.pet_name}: {response}")
               return

           image = Image.new("1", (self.oled.width, self.oled.height))
           draw = ImageDraw.Draw(image)

           draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
           kaomoji = self.kaomoji_map.get(self.mood, "^_^")
           draw.text((5, 5), f"{self.pet_name} {kaomoji}:", font=self.large_font, fill=255)

           wrapped_text = textwrap.wrap(response, width=20)
           y_position = 25
           for line in wrapped_text[:3]:
               draw.text((5, y_position), line, font=self.font, fill=255)
               y_position += 10

           self.oled.image(image)
           self.oled.show()
           time.sleep(5)
           self.update_display()

       def speak_response(self, response):
           """Convert text to speech"""
           try:
               print(f"Speaking: {response[:50]}...")

               tts_instructions = "speak warmly and playfully"
               if self.mood == "sad":
                   tts_instructions = "speak sadly and softly"
               elif self.mood == "hungry":
                   tts_instructions = "speak with hunger in your voice"
               elif self.mood == "sleepy":
                   tts_instructions = "speak sleepily and slowly"
               elif self.mood == "angry":
                   tts_instructions = "speak with frustration"
               elif self.mood == "excited":
                   tts_instructions = "speak excitedly and quickly"
               elif self.mood == "curious":
                   tts_instructions = "speak with curiosity and interest"

               print(f"Mood: {self.mood}, TTS instructions: {tts_instructions}")
               self.tts.say(response, instructions=tts_instructions)
               print("TTS completed")

           except Exception as e:
               print(f"TTS error: {e}")
               try:
                   self.tts.say(response)
                   print("TTS completed (fallback)")
               except Exception as e2:
                   print(f"TTS fallback also failed: {e2}")

       def voice_interaction(self):
           """Main voice interaction loop"""
           print("\n Voice interaction started!")
           print("Speak to your digital pet")
           print("Say 'stop' to end voice mode")
           print("Available moods and kaomoji:")
           for mood, kaomoji in self.kaomoji_map.items():
               print(f"  - {mood}: {kaomoji}")
           print()

           while True:
               self.listening = True
               self.update_display()
               print("Listening... (say something)")

               try:
                   full_text = ""
                   for result in self.stt.listen(stream=True):
                       if result["done"]:
                           user_input = result["final"]
                           print(f"\nYou: {user_input}")

                           if user_input.lower() in ["stop", "exit", "quit", "goodbye"]:
                               print("Ending voice interaction...")
                               self.listening = False
                               self.update_display()
                               return

                           if user_input.strip():
                               print(f"{self.pet_name} is thinking...")
                               response = self.interact_with_ai(user_input)
                               print(f"{self.pet_name}: {response}")
                               self.show_response_display(response[:50])
                               self.speak_response(response)

                           break
                       else:
                           partial = result["partial"]
                           if partial:
                               full_text = partial
                               self.show_listening_display(partial)

                   self.listening = False
                   self.update_display()

               except KeyboardInterrupt:
                   print("\nVoice interaction interrupted")
                   break
               except Exception as e:
                   print(f"Error in voice interaction: {e}")
                   self.listening = False
                   self.update_display()
                   time.sleep(1)

       def run(self):
           """Main program loop"""
           print("\n" + "="*50)
           print("DIGITAL PET")
           print("="*50)
           print(f"Pet Name: {self.pet_name}")
           print(f"Current Mood: {self.mood} {self.kaomoji_map.get(self.mood, '^_^')}")
           print("  OLED Display: " + ("Connected" if self.oled_available else "Not available"))
           print("  Voice: Speak to interact with your pet")
           print("   TTS: Pet responds with voice")
           print("  Say 'stop' to end voice interaction")
           print("="*50)
           print("\nInitializing...")

           try:
               self.voice_interaction()

               if self.oled_available:
                   image = Image.new("1", (self.oled.width, self.oled.height))
                   draw = ImageDraw.Draw(image)
                   draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
                   draw.text((15, 20), "Goodbye!", font=self.large_font, fill=255)
                   draw.text((10, 40), "(^_^)/~~", font=self.large_font, fill=255)
                   self.oled.image(image)
                   self.oled.show()
                   time.sleep(3)

           except KeyboardInterrupt:
               print("\nGoodbye!")

           finally:
               if self.oled_available:
                   self.oled.fill(0)
                   self.oled.show()
               print("Cleanup complete")

   if __name__ == "__main__":
       pet = AIPet()
       pet.run()

----------------------------------------------

**Comprensione del Codice**

1. Riconoscimento Vocale (STT)

   Il sistema utilizza Vosk per il riconoscimento vocale con capacita' di streaming per feedback in tempo reale:

   .. code-block:: python

      self.stt = STT(language="en-us")

      for result in self.stt.listen(stream=True):
          if result["done"]:
              user_input = result["final"]
          else:
              partial = result["partial"]
              # Mostra testo parziale sul display

2. Sistema di Personalita' AI

   L'animaletto ha una personalita' dinamica con stati emotivi gestiti tramite kaomoji:

   .. code-block:: python

      self.kaomoji_map = {
          "happy": "^_^",
          "sad": "T_T",
          "hungry": "(;_)",
          "sleepy": "(-_-) zzz",
          # ... altre emozioni
      }

3. Istruzioni LLM Dinamiche

   Le istruzioni dell'AI si aggiornano in base allo stato attuale dell'animaletto e ai ricordi:

   .. code-block:: python

      def update_llm_instructions(self):
          self.instructions = f"""You are {self.pet_name}, a digital pet...
          CURRENT STATE: Mood: {self.mood}, Energy: {self.energy}, Hunger: {self.hunger}
          Recent memories: {self.memories[-3:] if self.memories else 'None'}"""

4. Sistema di Gestione dello Stato

   Un thread in background gestisce i bisogni dell'animaletto e lo stato emotivo:

   .. code-block:: python

      def update_status(self):
          while True:
              time.sleep(60)
              self.hunger = min(100, self.hunger + 5)
              if self.hunger > 70:
                  self.mood = "hungry"
              # Cambiamenti di umore casuali
              if random.random() < 0.1:
                  self.mood = random.choice(list(self.kaomoji_map.keys()))

5. TTS Guidato dalle Emozioni

   La sintesi vocale si adatta in base all'umore corrente dell'animaletto:

   .. code-block:: python

      def speak_response(self, response):
          tts_instructions = "speak warmly and playfully"
          if self.mood == "sad":
              tts_instructions = "speak sadly and softly"
          elif self.mood == "hungry":
              tts_instructions = "speak with hunger in your voice"
          # ...
          self.tts.say(response, instructions=tts_instructions)

6. Gestione del Display OLED

   Modalita' di visualizzazione multiple per diversi stati:

   .. code-block:: python

      def update_display(self):
          # Display di stato con barre
          draw.rectangle((50, 35, 50 + energy_bar, 45), outline=255, fill=255)
          draw.rectangle((50, 50, 50 + hunger_bar, 60), outline=255, fill=255)

      def show_listening_display(self, partial_text=""):
          # Modalita' ascolto con testo parziale
          draw.text((15, 10), "LISTENING (O_O)", font=self.large_font, fill=255)

      def show_response_display(self, response):
          # Display di risposta con testo a capo
          wrapped_text = textwrap.wrap(response, width=20)

7. Cambiamenti di Stato Interattivi

   Le interazioni dell'utente influenzano lo stato dell'animaletto:

   .. code-block:: python

      if "feed" in user_lower or "food" in user_lower:
          self.hunger = max(0, self.hunger - 30)
          self.energy = min(100, self.energy + 20)
          self.mood = "happy"

      if "play" in user_lower or "game" in user_lower:
          self.energy = max(0, self.energy - 20)
          self.hunger = min(100, self.hunger + 10)
          self.mood = "playful"

8. Sistema di Memoria

   Tiene traccia delle conversazioni recenti:

   .. code-block:: python

      memory_text = f"Talked: {user_input[:30]}"
      self.memories.append(memory_text)
      if len(self.memories) > 10:
          self.memories.pop(0)

9. Analisi delle Risposte

   Estrae l'umore dalle risposte AI e aggiorna lo stato dell'animaletto:

   .. code-block:: python

      def parse_response(self, response):
          emotion_pattern = r'^\[(\w+)\]\s*(.*)'
          match = re.match(emotion_pattern, response.strip())
          if match:
              mood, text = match.groups()
              if mood.lower() in self.kaomoji_map:
                  self.mood = mood.lower()
              return text.strip()

10. Ciclo Principale di Interazione

    Coordina tutti i componenti in un flusso di lavoro pulito:

    .. code-block:: python

        def voice_interaction(self):
            while True:
                self.listening = True
                # Ascolta il parlato
                user_input = self.get_voice_input()
                if "stop" in user_input.lower():
                    return
                # Elabora con AI
                response = self.interact_with_ai(user_input)
                # Mostra risposta
                self.show_response_display(response)
                # Pronuncia risposta
                self.speak_response(response)

----------------------------------------------

**Risoluzione dei Problemi**


- Input audio non rilevato

  - Esegui ``sudo /opt/setup_fusion_hat_audio.sh`` per reimpostare l'audio

- Display OLED non visualizzato

  - Controlla la connessione I2C: ``fusion_hat scan_i2c`` (dovrebbe mostrare 0x3C)
  - Verifica che l'OLED sia alimentato (3.3V o 5V a seconda del modello)
  - Assicurati che l'indirizzo I2C nel codice sia corretto (0x3C o 0x3D)

- TTS non funzionante

  - Verifica che la chiave API OpenAI abbia crediti TTS
  - Assicurati della connessione Internet per le chiamate API
  - Esegui ``sudo /opt/setup_fusion_hat_audio.sh`` per reimpostare l'audio

- Riconoscimento vocale impreciso

  - Parla chiaramente e a volume moderato
  - Riduci il rumore di fondo
  - Regola il guadagno del microfono: ``alsamixer``
  - Prova diversi modelli linguistici

- Risposte AI troppo lente

  - Controlla la velocita' della connessione Internet
  - Riduci la complessita' della risposta nelle istruzioni
  - Usa un modello OpenAI piu' veloce (gpt-3.5-turbo)

- Le barre di energia/fame non si aggiornano

  - Controlla che il thread di stato sia in esecuzione
  - Verifica che il display OLED sia connesso
  - Controlla eventuali messaggi di errore nella console

- L'animaletto non ricorda le conversazioni

  - La lista di memoria mantiene solo le ultime 10 conversazioni
  - Controlla se i ricordi vengono aggiunti correttamente
  - Assicurati che il testo dei ricordi venga passato all'LLM

----------------------------------------------

Questo progetto di animaletto digitale dimostra la potenza della combinazione di molteplici tecnologie AI (STT, LLM, TTS) con interfacce hardware per creare esperienze coinvolgenti, emotive e interattive. E' un esempio perfetto di come l'AI possa creare connessioni significative attraverso la tecnologia!
