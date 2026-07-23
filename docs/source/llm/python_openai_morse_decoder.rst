.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(Exemple) Decodeur de code Morse alimente par l'IA
========================================

**Introduction**

Ce projet cree un **Decodeur de code Morse** intelligent qui utilise l'IA pour interpreter les motifs temporels des pressions de bouton. Le systeme capture des donnees de temporisation precises et utilise OpenAI GPT pour decoder les messages en code Morse en temps reel. Le decodeur propose :

1. **Entree basee sur la temporisation** capturant les instants precis d'appui et de relachement
2. **Decodage par IA** utilisant GPT pour interpreter les motifs point/trait
3. **Indicateur visuel** avec une LED montrant l'etat de decodage actif
4. **Interface a double bouton** boutons d'entree et de controle separes
5. **Retour en temps reel** affichant les donnees de temporisation pendant la saisie

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Le systeme enregistre les durees de pression des boutons, envoie les donnees de temporisation a l'IA pour interpretation et decode avec precision les sequences de code Morse comme le signal de detresse universel "SOS".

Vous pouvez combiner des entrees sensibles a la temporisation avec l'interpretation IA pour divers systemes de codage. Voir :

* :ref:`py_online_llm`

----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
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

**Schema de cablage**

Connectez les composants au Raspberry Pi comme suit :

.. image:: img/fzz/morse_decoder_bb.png
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
      sudo python3 llm_openai_morse_decoder.py

#. Essayez un message simple en code Morse (exemple : "SOS")

   Apres le demarrage du programme, appuyez sur le bouton demarrer/arreter pour commencer l'enregistrement.
   Ensuite, appuyez sur le bouton Morse pour saisir des points (appuis courts) et des traits (appuis longs).

   Lorsque vous avez termine, appuyez a nouveau sur le bouton demarrer/arreter pour arreter l'enregistrement et decoder le message.

#. Verifiez la sortie console

   La console affichera les horodatages d'appui/relachement, et l'IA analysera les donnees de temporisation
   et affichera le message decode.

   **Sortie console typique lors de la saisie de "SOS" :**

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

#. Comprendre le flux de travail

   1. Demarrer l'enregistrement : appuyez sur le bouton demarrer/arreter (GPIO 17) et la LED s'allume
   2. Saisir le code Morse : utilisez le bouton Morse (GPIO 22) pour les points et les traits
   3. Affichage en temps reel : la console montre les horodatages d'appui/relachement
   4. Arreter et decoder : appuyez a nouveau sur le bouton demarrer/arreter et la LED s'eteint
   5. Analyse IA : les donnees de temporisation sont envoyees a OpenAI GPT pour interpretation
   6. Sortie decodee : l'IA affiche le message decode

**Code**

Voici le script Python complet pour le Decodeur de code Morse alimente par l'IA :

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

**Comprendre le code**

1. Configuration des broches GPIO

   Trois broches GPIO sont configurees pour differents usages :

   .. code-block:: python

      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)

   - Temps d'anti-rebond (0,05 s) : empeche les detections multiples dues au rebond mecanique de l'interrupteur
   - Pull-down : garantit un signal LOW propre lorsque le bouton n'est pas presse
   - Fonctions separees : les boutons d'entree et de controle empechent les saisies accidentelles

2. Stockage des donnees de temporisation

   Les evenements d'appui/relachement sont stockes avec des horodatages precis :

   .. code-block:: python

      morse_events = []  # Empty list to store events

      # Each event stored as tuple: ('pressed'/'released', timestamp)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. Mecanisme d'anti-rebond

   Empeche les faux declenchements dus au rebond de l'interrupteur :

   .. code-block:: python

      def morse_input_released():
          if release_time - start_time < 0.1:  # 100ms debounce
              return  # Ignore very short releases

          morse_events.append(('released', release_time))

4. Gestion d'etat

   Le systeme utilise un indicateur pour suivre l'etat d'enregistrement :

   .. code-block:: python

      input_active = False  # Initially not recording

      def handle_start_stop():
          if input_active:
              # Stop recording and decode
              input_active = False
          else:
              # Start recording
              input_active = True
              morse_events.clear()  # Clear previous data

5. Indicateur visuel

   La LED fournit un retour visuel de l'etat d'enregistrement :

   .. code-block:: python

      def handle_start_stop():
          if input_active:
              led.off()  # LED OFF when not recording
          else:
              led.on()   # LED ON when recording

6. Construction de l'invite IA

   Les donnees de temporisation sont converties en chaine pour le traitement IA :

   .. code-block:: python

      input_text = str(morse_events)

      # Example format sent to AI:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. Reponse en continu

   La reponse de l'IA est traitee et affichee en temps reel :

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. Architecture pilotee par les evenements

   Les evenements de bouton declenchent des rappels immediats :

   .. code-block:: python

      # Assign callback functions to button events
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. Precision de temporisation

   Utilise ``time.time()`` pour une temporisation precise a la microseconde :

   .. code-block:: python

      start_time = time.time()  # Current time in seconds since epoch

      # Calculate press duration:
      duration = release_time - start_time

10. Effacement des donnees

    Apres le decodage, la liste d'evenements est effacee pour le message suivant :

    .. code-block:: python

        def decode_and_print():
            # ... process events ...
            morse_events = []  # Clear for next message

----------------------------------------------

**Normes de temporisation du code Morse**

* Temporisation standard (basee sur le mot PARIS) :

  - Point : 1 unite
  - Trait : 3 unites
  - Ecart intra-caractere (entre points/traits) : 1 unite
  - Ecart inter-caractere (entre lettres) : 3 unites
  - Ecart entre mots : 7 unites

* Implementation pratique :

  - Point : < 0,3 seconde (appui court)
  - Trait : > 0,5 seconde (appui long)
  - Entre elements : < 0,5 seconde de pause
  - Entre lettres : 0,5-1,5 seconde de pause
  - Entre mots : > 1,5 seconde de pause

* Lettres courantes en code Morse :

  - A : • — (point-trait)
  - B : — • • • (trait-point-point-point)
  - C : — • — • (trait-point-trait-point)
  - S : • • • (point-point-point)
  - O : — — — (trait-trait-trait)

----------------------------------------------

**Depannage**

- Les pressions de bouton ne sont pas enregistrees

  - Verifiez le cablage : GPIO 22/17 au bouton, autre cote a la masse
  - Verifiez la configuration du pull-down
  - Testez avec un script simple : ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``
  - Verifiez le reglage du temps d'anti-rebond (0,05 s peut etre trop eleve)

- La LED ne s'allume pas

  - Verifiez la polarite de la LED : anode (longue jambe) vers GPIO 27 via une resistance
  - Verifiez la valeur de la resistance (220Ω recommande)
  - Testez la LED directement : ``Pin(27, Pin.OUT).on()`` devrait allumer la LED
  - Assurez-vous que la connexion a la masse est complete

- Les donnees de temporisation semblent erronees

  - Verifiez l'horloge systeme : commande ``date``
  - Reduisez le temps d'anti-rebond s'il est trop sensible
  - Ajoutez des instructions d'affichage pour verifier l'execution du rappel
  - Testez avec des durees de pression coherentes

- L'IA ne decode pas correctement

  - Verifiez la cle API et la connexion Internet
  - Examinez les donnees de temporisation envoyees a l'IA (affichez ``morse_events``)
  - Assurez-vous de durees de pression coherentes (points courts, traits longs)
  - Ajoutez des pauses plus claires entre les lettres

- Declenchements multiples pour une seule pression

  - Augmentez le parametre bounce_time (essayez 0,1 s)
  - Verifiez le rebond mecanique de l'interrupteur
  - Ajoutez un anti-rebond materiel avec un condensateur
  - Verifiez que le bouton est correctement cble

- Le systeme ne repond pas au demarrage/arret

  - Verifiez si un autre rappel interfere
  - Verifiez la logique de l'indicateur ``input_active``
  - Ajoutez des debugs dans ``handle_start_stop()``
  - Assurez-vous qu'aucun autre processus n'utilise le GPIO

- Reponse IA trop lente

  - Verifiez la vitesse de la connexion Internet
  - Reduisez le nombre d'evenements (messages plus courts)
  - Envisagez d'utiliser un decodage local comme solution de repli
  - Implementez un delai d'attente pour les reponses IA

- Impossible de distinguer les points des traits

  - Entrainez-vous a une temporisation coherente
  - Ajustez le seuil dans les instructions de l'IA
  - Ajoutez un pretraitement local avant l'envoi a l'IA
  - Utilisez un retour visuel pendant la saisie

----------------------------------------------


Ce decodeur de code Morse alimente par l'IA demontre comment des donnees de temporisation precises combinees a la reconnaissance intelligente de motifs peuvent raviver et moderniser des methodes de communication historiques, les rendant accessibles et educatives pour les nouvelles generations !