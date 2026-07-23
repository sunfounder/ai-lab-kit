.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_blindfolded_watermelon_game:

(Exemple) Jeu de ecrasement de pastque yeux bandes
====================================================

**Introduction**

Ce projet cree un jeu interactif **d'ecrasement de pastque les yeux bandes** ou les joueurs naviguent sur une grille de 20×20 metres a l'aide d'un joystick tout en se fiant a un assistant IA pour les directives directionnelles. Le systeme integre :

1. **Commandes joystick** pour le deplacement du joueur sur les axes X/Y
2. **Guidage par IA** utilisant OpenAI GPT-4
3. **Retour vocal par synthese vocale** utilisant Pico2Wave
4. **Generation aleatoire de cibles** pour le placement des pastques
5. **Bouton interactif** pour les actions d'ecrasement

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Blindfolded_Watermelon_Smashing_Game.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Le joueur commence au centre (0,0) et doit trouver une pastque placee aleatoirement en utilisant uniquement les directives audio de l'assistant IA, creant ainsi une experience de jeu sensorielle engageante.

Vous pouvez combiner divers peripheriques d'entree avec des modules LLM pour creer des jeux IA interactifs. Voir :

* :ref:`py_online_llm`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_joystick`

----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
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

**Schema de cablage**

Connectez les composants au Fusion HAT+ comme suit :

.. image:: img/fzz/watermelon_game_bb.png
   :width: 80%
   :align: center

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai



----------------------------------------------

**Executer l'exemple**

#. Executez le code

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_blindfolded_game.py

#. Jouez au jeu

   Apres le demarrage du script, le jeu placera aleatoirement une pastque sur le terrain de 20×20 metres.
   Utilisez le joystick pour vous deplacer pas a pas, et ecoutez l'assistant IA pour les directives directionnelles.

   Lorsque vous pensez avoir atteint la position de la pastque, appuyez sur le bouton pour ecraser.
   Si vos coordonnees correspondent exactement a celles de la pastque, vous gagnez la partie.

#. Comprendre les mecaniques du jeu

   * Systeme de coordonnees :

     - Le terrain de jeu est une grille de 20×20 metres
     - Les coordonnees vont de (-10,-10) a (10,10)
     - X positif = Est, X negatif = Ouest
     - Y positif = Sud, Y negatif = Nord (axe Y inverse)
     - Le centre est (0,0)

   * Regles de deplacement :

     - Joystick droite → X+1 (Est)
     - Joystick gauche → X-1 (Ouest)
     - Joystick haut → Y-1 (Nord)
     - Joystick bas → Y+1 (Sud)
     - Chaque mouvement change la position de 1 metre

   * Condition de victoire :

     - Le joueur doit etre aux coordonnees exactes de la pastque
     - Appuyez sur le bouton pour "ecraser" a la position actuelle
     - Une correspondance exacte termine le jeu avec un message de victoire

   * Role de l'assistant IA :

     - Recoit les coordonnees du joueur et de la pastque
     - Fournit des directives cardinales (N, NE, E, SE, S, SO, O, NO)
     - Donne une approximation de distance en metres
     - Garde les reponses breves pour la lecture audio


**Code**

Voici le script Python complet pour le Jeu d'ecrasement de pastque les yeux bandes :

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

**Comprendre le code**

1. Configuration de la synthese vocale

   Le jeu utilise Pico2Wave pour le retour audio :

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')

   Ceci convertit les reponses textuelles de l'IA en instructions parlées en anglais.

2. Gestion des entrees du joystick

   Le joystick utilise deux canaux ADC pour la lecture des axes X et Y :

   .. code-block:: python

      x_axis = ADC('A1')  # Horizontal movement
      y_axis = ADC('A0')  # Vertical movement

      def MAP(x, in_min, in_max, out_min, out_max):
          return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

      # Convert 0-4095 ADC reading to -100 to 100 range
      x_val = MAP(x_axis.read(), 0, 4095, -100, 100)
      y_val = MAP(y_axis.read(), 0, 4095, -100, 100)

3. Configuration du bouton avec interruption

   Le bouton utilise un rappel d'interruption pour une reponse immediate :

   .. code-block:: python

      btn_pin = Pin(17, mode=Pin.IN, pull=Pin.PULL_UP, bounce_time=0.05)

      def activate():
          global smash_tips
          smash_tips = True

      btn_pin.when_activated = activate

   Lorsqu'il est presse, il definit ``smash_tips`` a ``True``, declenchant l'action d'ecrasement dans la boucle principale.

4. Configuration du LLM OpenAI

   L'assistant IA est configure avec des instructions de jeu specifiques :

   .. code-block:: python

      INSTRUCTIONS = "This is a blindfolded watermelon-smashing game..."
      WELCOME = "Hello, I am Blindfolded Watermelon Smashing Game Assistant..."

      llm = OpenAI(
          api_key=OPENAI_API_KEY,
          model="gpt-4o",
      )

      llm.set_max_messages(20)       # Keep conversation history
      llm.set_instructions(INSTRUCTIONS)  # Set game rules
      llm.set_welcome(WELCOME)       # Set initial greeting

5. Gestion de l'etat du jeu

   Le jeu maintient les positions du joueur et de la cible :

   .. code-block:: python

      # Random watermelon placement
      watermelon_x, watermelon_y = random.randint(-10, 10), random.randint(-10, 10)

      # Player starts at center
      player_x, player_y = 0, 0

      # Movement thresholds (80% joystick deflection)
      if x_val > 80:
          player_x += 1      # Move right
      elif x_val < -80:
          player_x -= 1      # Move left

      if y_val > 80:
          player_y -= 1      # Move up (negative Y)
      elif y_val < -80:
          player_y += 1      # Move down (positive Y)

6. Action d'ecrasement et reponse IA

   Lorsque le bouton est presse, le jeu verifie un coup ou demande un guidage IA :

   .. code-block:: python

      if smash_tips:
          smash_tips = False
          print("Smash!")

          if (player_x, player_y) == (watermelon_x, watermelon_y):
              print("Target hit!")
              tts.say("Target hit!")
              break  # Game ends
          else:
              # Send positions to AI for guidance
              input_text = f"Watermelon position: ({watermelon_x}, {watermelon_y}), Player position: ({player_x}, {player_y})"

              # Get streaming response from AI
              response = llm.prompt(input_text, stream=True)
              string = ""

              for next_word in response:
                  if next_word:
                      string += next_word

              print("AI: " + string)
              tts.say(string)  # Speak the guidance

7. Traitement de la reponse en continu

   La reponse de l'IA est traitee mot par mot pour un affichage potentiel en temps reel :

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              # Uncomment to display words as they arrive
              # print(next_word, end="", flush=True)
              string += next_word

8. Logique de deplacement avec zone morte

   Le joystick a une zone morte de 80 unites pour empecher les mouvements accidentels :

   .. code-block:: python

      # Only move when joystick is pushed >80% in any direction
      # This prevents drifting from center position
      if x_val > 80:    # Right
      elif x_val < -80: # Left

      if y_val > 80:    # Up
      elif y_val < -80: # Down

9. Structure de la boucle de jeu

   La boucle principale du jeu en continu :

   1. Lit la position du joystick
   2. Met a jour les coordonnees du joueur si le joystick est pousse
   3. Verifie la pression du bouton d'ecrasement
   4. Traite les reponses IA lorsque necessaire
   5. Fournit un retour audio via TTS

----------------------------------------------

**Depannage**

- Pas de reponse du joystick

  - Verifiez les connexions ADC : A0 pour l'axe Y, A1 pour l'axe X
  - Verifiez l'alimentation : VCC vers 3,3 V, GND vers la masse
  - Testez la lecture ADC : ``print(x_axis.read())`` devrait afficher 0-4095
  - Assurez-vous que le joystick est centre (devrait lire ~2048)


- Pas d'audio du TTS

  - Verifiez la sortie audio : ``sudo raspi-config`` → **System Options** → **Audio**
  - Testez le haut-parleur : ``speaker-test -t sine -f 440``
  - Assurez-vous que Pico2Wave est installe : ``pico2wave --help``
  - Verifiez le volume : ``alsamixer``
  - Reexecutez le script de configuration audio : ``sudo /opt/setup_fusion_hat_audio.sh``

- Erreurs API OpenAI

  - Verifiez la cle API dans ``secret.py``
  - Verifiez la connexion Internet : ``ping 8.8.8.8``
  - Assurez-vous que la facturation est activee sur le compte OpenAI
  - Verifiez que le modele "gpt-4o" est disponible pour votre compte

- Le joueur se deplace trop vite/lentement

  - Ajustez le seuil de mouvement (actuellement 80) : plus eleve = plus de deplacement du joystick necessaire
  - Modifiez l'increment de mouvement (actuellement 1) : passez a 0,5 pour un controle plus fin
  - Ajustez le temps de pause (actuellement 0,3 s) : plus long = reponse de mouvement plus lente


- Reponses IA trop longues

  - Insistez sur la brievete dans INSTRUCTIONS
  - Ajoutez "Respond in 10 words or less" aux instructions
  - Implementez une verification de la longueur des reponses dans le code

----------------------------------------------

Ce jeu de pastque les yeux bandes demontre comment les controles physiques, le guidage IA et le retour audio peuvent creer une experience de jeu sensorielle engageante qui defie la conscience spatiale et les competences d'ecoute !