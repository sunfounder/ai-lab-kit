.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_health_assistant:

(Exemple) Assistant sante IA avec surveillance de temperature
=========================================================

**Introduction**


Ce projet cree un **Assistant sante IA** intelligent qui combine la detection de temperature corporelle avec l'interaction vocale pour fournir des evaluations personnalisees. Le systeme integre :

1. **Detection de temperature par thermistance** pour une mesure precise de la temperature corporelle
2. **Reconnaissance vocale** pour comprendre les symptomes et questions de l'utilisateur
3. **Analyse santee par IA** utilisant OpenAI GPT pour l'evaluation medicale
4. **Retour vocal par synthese vocale** fournissant des recommandations audibles
5. **Surveillance en temps reel** avec conversion continue de la temperature

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Health_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

L'assistant sante mesure la temperature corporelle via un circuit a thermistance, analyse la lecture avec l'IA et fournit des conseils appropries base sur les plages de temperature medicales etablies.


* :ref:`py_online_llm`
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
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

**Schema de cablage**

Connectez les composants au Fusion HAT+ comme suit :

.. image:: img/fzz/health_assistant_bb.png
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
      sudo python3 llm_openai_health.py

#. Verifiez le resultat

   Lorsque le programme demarre, il vous invite a parler. Il estimera ensuite votre temperature
   corporelle et fournira des conseils de sante.

   Sortie console typique :

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

#. Scenarios d'exemple

   * Temperature normale (36,5°C) :

     .. code-block:: text

        User: "How's my temperature?"
        AI: "Your body temperature is 36.5°C, which is within the normal range. You're
        doing well, but continue to monitor how you feel."

   * Fievre elevee (39,2°C) :

     .. code-block:: text

        User: "I have a headache and feel hot"
        AI: "Your body temperature is 39.2°C, indicating a high fever. Please rest
        immediately, stay hydrated, and consider seeking medical advice as soon as possible."

   * Temperature basse (34,2°C) :

     .. code-block:: text

        User: "I feel cold and shivering"
        AI: "Your body temperature is 34.2°C, which is below normal and may indicate
        hypothermia. Please warm up immediately with blankets and warm drinks."


**Code**

Voici le script Python complet pour l'Assistant sante IA :

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

**Comprendre le code**

1. Initialisation du capteur de temperature

   La thermistance est connectee au canal ADC A3 :

   .. code-block:: python

      thermistor = ADC('A3')

   Ceci lit les valeurs analogiques de 0 a 4095 representant les niveaux de tension.

2. Conversion de temperature Steinhart-Hart

   La thermistance utilise l'equation de Steinhart-Hart pour un calcul precis de la temperature :

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

3. Verification des erreurs du capteur

   Le code inclut une detection d'erreur de base :

   .. code-block:: python

      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue

   Ceci detecte si la thermistance est deconnectee ou en court-circuit.

4. Configuration de la reconnaissance vocale

   Le STT et le TTS sont configures pour l'anglais :

   .. code-block:: python

      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. Construction de l'entree contextuelle

   Les donnees de temperature sont combinees avec la question de l'utilisateur :

   .. code-block:: python

      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"

   Format : ``"thermistor: 37.2, message: I feel dizzy"``

6. Logique de classification medicale

   Les instructions de l'IA definissent les plages de temperature :

   .. code-block:: python

      # Temperature ranges for medical assessment:
      # < 35.0°C: Hypothermia warning
      # 35.0-37.5°C: Normal range
      # 37.5-38.5°C: Mild fever
      # > 38.5°C: High fever

7. Traitement vocal en temps reel

   Le systeme affiche les resultats partiels de reconnaissance :

   .. code-block:: python

      for result in stt.listen(stream=True):
          if result["done"]:
              # Final recognition
              print(f"final: {result['final']}")
          else:
              # Partial recognition
              print(f"partial: {result['partial']}", end="", flush=True)

8. Reponse IA en continu

   La reponse de l'IA est diffusee et prononcee simultanement :

   .. code-block:: python

      response = llm.prompt(input_text, stream=True)
      string = ""

      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word

      tts.say(string)  # Speak complete response

9. Formatage de la temperature

   La temperature est formatee avec une decimale :

   .. code-block:: python

      f"thermistor: {current_temp:.1f}"

   Cela garantit une precision constante (par ex., 36,5°C au lieu de 36,512345°C).

10. Affichage console clair

    Utilise les codes d'echappement ANSI pour une sortie propre :

    .. code-block:: python

        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

    - ``\r`` : Retour au debut de la ligne
    - ``\x1b[K`` : Effacement jusqu'a la fin de la ligne
    - Empeche le chevauchement du texte pendant le streaming

----------------------------------------------

**Depannage**

- Lectures de temperature imprecises

  - Verifiez le cablage de la thermistance : configuration correcte du diviseur de tension
  - Verifiez la valeur de la resistance : doit correspondre a la resistance nominale de la thermistance
  - Calibrez avec une source de temperature connue
  - Verifiez la tension de reference ADC (doit etre stable a 3,3 V)

- Pas de reconnaissance vocale

  - Testez le microphone : ``arecord --duration=3 test.wav && aplay test.wav``
  - Verifiez la selection du peripherique audio dans l'initialisation STT
  - Assurez-vous que le bruit de fond est minimal
  - Parlez clairement et a un rythme modere

- L'IA ne repond pas

  - Verifiez la connexion Internet
  - Verifiez la cle API OpenAI dans ``secret.py``
  - Assurez-vous que la facturation est activee sur le compte OpenAI
  - Verifiez si les limites de taux de l'API sont depassees

- La temperature saute de maniere erratique

  - Ajoutez un filtrage logiciel : moyenne mobile des lectures
  - Verifiez les connexions desserrees
  - Ajoutez un condensateur (0,1 µF) aux bornes de la thermistance pour reduire le bruit
  - Assurez-vous que la thermistance a un bon contact thermique

- La synthese vocale ne fonctionne pas

  - Testez la sortie audio : ``speaker-test -t sine -f 440``
  - Verifiez le parametre de langue : ``tts.set_lang('en-US')``
  - Verifiez le volume : ``alsamixer``
  - Reexecutez le script de configuration audio : ``sudo /opt/setup_fusion_hat_audio.sh``

- La lecture du capteur affiche 0 ou 4095

  - Verifiez le cablage : la thermistance peut etre en court-circuit (0) ou ouverte (4095)
  - Verifiez le calcul du diviseur de tension
  - Testez l'ADC avec une source de tension connue
  - Verifiez le canal ADC (doit etre A3)

**Avertissement medical et de securite**

.. warning::

   Ce projet est uniquement destine a des fins educatives et de demonstration.
   Il **n'est PAS** un dispositif medical et ne doit **PAS** etre utilise pour un diagnostic ou un traitement medical reel.

#. Consignes de securite

   * Pas pour usage medical : ne vous fiez pas a ce systeme pour des decisions de sante ou de traitement.
   * Situations d'urgence : demandez toujours une aide medicale professionnelle pour les symptomes graves.
   * Limitations de precision : la precision de la thermistance est limitee par rapport aux thermometres medicaux.
   * Etalonnage requis : un etalonnage regulier avec un thermometre medical est essentiel.
   * Supervision necessaire : la supervision d'un adulte est recommandee lorsqu'il est utilise a des fins educatives.

#. Quand consulter un medecin

   Consultez un professionnel de sante si l'un des cas suivants se produit :

   * Temperature > 39,5°C (103,1°F) chez l'adulte
   * Temperature > 38,0°C (100,4°F) chez les nourrissons de moins de 3 mois
   * Fievre durant plus de 3 jours
   * Difficultes respiratoires ou douleurs thoraciques
   * Mal de tete severe ou raideur de la nuque
   * Confusion ou convulsions



----------------------------------------------

Cet Assistant sante IA demontre comment la technologie des capteurs, l'interaction vocale et l'intelligence artificielle peuvent travailler ensemble pour creer des outils de surveillance de sante accessibles, tout en soulignant l'importance d'une consultation medicale professionnelle pour les problemes de sante graves !