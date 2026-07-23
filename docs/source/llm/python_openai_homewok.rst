.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

(Exemple) Correction de devoirs avec camera panoramique
=====================================================

**Introduction**

Ce projet cree un **Assistant de correction de devoirs IA** interactif qui combine la vision par ordinateur, l'intelligence artificielle et la robotique. Le systeme :

1. **Capture des photos** de questions de devoirs manuscrites ou imprimees en utilisant une camera Raspberry Pi
2. **Analyse le contenu** en utilisant le modele de vision GPT-4 d'OpenAI pour determiner si les reponses sont correctes
3. **Fournit un retour physique** via les mouvements d'un pantilt controle par servomoteurs :

   - *Hochement* pour les reponses correctes
   - *Secouement* pour les reponses incorrectes

4. **Utilise une interaction simple** declenchee par une seule pression de bouton

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Cette demonstration montre comment l'IA peut interagir avec le monde physique, creant ainsi un outil pedagogique engageant qui fournit un retour visuel immediat sur l'exactitude des devoirs.

Vous pouvez utiliser d'autres modules LLM et composants materielles pour construire vos propres dispositifs d'apprentissage assisted par IA. Voir :

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**Ce dont vous aurez besoin**

Les composants suivants sont necessaires pour ce projet :

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPOSANT
        - LIEN D'ACHAT
    *   - :ref:`cpn_servo`
        - |link_servo_buy|
    *   - Pantilt
        -
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-
    *   - Echantillon de devoir (imprime ou manuscrit)
        - \-

----------------------------------------------

**Configuration materielle**

Pour utiliser le module camera facilement, :ref:`assemble_fusion_hat_pan_tilt` est recommande.

   .. note::

     L'assemblage du pantilt peut obstruer certaines broches, il est donc recommande de ne l'assembler que lors de l'utilisation de la camera, ou de le placer a l'exterieur apres assemblage.


   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Executer le code**

#. Creez un echantillon de devoir :

   - Ecrivez ou imprimez un probleme mathematique simple avec la reponse
   - Exemple : "5 + 3 = 8" (correct) ou "5 + 3 = 7" (incorrect)
   - Assurez-vous d'une ecriture ou impression claire

#. Executez le programme :

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. Suivez les instructions a l'ecran :

   - Positionnez le devoir sous la camera
   - Appuyez sur le bouton utilisateur (USR) du Fusion HAT+
   - Observez la reponse du servomoteur

#. Resultat attendu :

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

**Code**

Voici le script Python complet pour la Demonstration de correction de devoirs :


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

**Comprendre le code**

1. Configuration et installation du LLM

   Le systeme utilise OpenAI GPT-4o avec des capacites de vision pour analyser les images :

   .. code-block:: python

      # Import and initialize the LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

      # Set specific instructions for consistent responses
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)

      # Limit conversation history to manage tokens
      llm.set_max_messages(5)

2. Initialisation du materiel

   Trois composants materielles sont initialises : les servomoteurs, la camera et le bouton :

   .. code-block:: python

      # Servo control for pan-tilt mechanism
      pan_servo = Servo(PAN_CHANNEL)   # Channel 2 for horizontal movement
      tilt_servo = Servo(TILT_CHANNEL) # Channel 3 for vertical movement

      # Camera setup with preview
      camera = Picamera2()
      camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
      camera.configure(camera_config)
      camera.start_preview(Preview.QT)
      camera.start()

      # User button for interaction
      user_button = UserButton()

3. Fonctions d'animation des servomoteurs

   Mouvements naturels pour hocher et secouer la tete :

   .. code-block:: python

      def nod_head():
          """Nodding head movement for 'correct' answers"""
          tilt_servo.angle(15)    # Look down
          time.sleep(0.2)
          tilt_servo.angle(-10)   # Look up
          time.sleep(0.2)
          tilt_servo.angle(TILT_CENTER)  # Return to center

      def shake_head():
          """Shaking head movement for 'incorrect' answers"""
          pan_servo.angle(-20)    # Look left
          time.sleep(0.15)
          pan_servo.angle(20)     # Look right
          time.sleep(0.15)
          pan_servo.angle(-15)    # Look left again
          time.sleep(0.15)
          pan_servo.angle(PAN_CENTER)  # Return to center

4. Capture d'image et analyse IA

   Le flux de travail principal de correction :

   .. code-block:: python

      def grade_homework():
          # Capture image from camera
          img_path = './homework.jpg'
          camera.capture_file(img_path)

          # Send image to LLM with specific prompt
          prompt = "Look at this homework question and answer..."
          response = llm.prompt(prompt, image_path=img_path)
          response_text = response.strip().upper()

          # Interpret response and trigger appropriate servo movement
          if "INCORRECT" in response_text:
              shake_head()
          elif "CORRECT" in response_text:
              nod_head()

5. Gestion des evenements du bouton

   Systeme de rappel simple pour l'interaction utilisateur :

   .. code-block:: python

      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()

      # Assign callback to button
      user_button.set_on_click(on_button_click)

6. Boucle d'application principale

   Boucle principale minimale qui attend les pressions de bouton :

   .. code-block:: python

      def main():
          print("Waiting for button press...")
          user_button.set_on_click(on_button_click)

          # Keep program running until interrupted
          try:
              while True:
                  time.sleep(0.1)  # Low CPU usage wait
          except KeyboardInterrupt:
              print("\nDemo stopped by user")

7. Nettoyage des ressources

   Procedure d'arret appropriee :

   .. code-block:: python

      def cleanup():
          # Return servos to neutral position
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)

          # Stop camera
          camera.stop()

----------------------------------------------

**Depannage**

- Pas de module nomme ``picamera2``

  Installez la bibliotheque requise :

  .. code-block:: bash

     sudo apt update
     sudo apt install python3-picamera2

- Camera non detectee

  1. Verifiez la connexion de la camera : assurez-vous que le cable ruban est correctement insere
  2. Verifiez que la camera est activee : ``sudo raspi-config`` → Interface Options → Camera
  3. Testez la camera independamment : ``libcamera-hello``

- Les servomoteurs ne bougent pas

  1. Verifiez les connexions d'alimentation : les servomoteurs necessitent du 5V
  2. Verifiez que les canaux des servomoteurs correspondent au code (Canaux 2 et 3)
  3. Testez les servomoteurs independamment avec des commandes d'angle simples

- L'IA ne repond pas ou erreur

  1. Verifiez que la cle API dans ``secret.py`` est correcte
  2. Verifiez la connexion Internet : ``ping 8.8.8.8``
  3. Assurez-vous d'avoir des credits dans votre compte OpenAI
  4. Verifiez que le modele "gpt-4o" est disponible dans votre compte

- Mouvements incorrects des servomoteurs

  1. Verifiez si les servomoteurs panoramique et d'inclinaison sont intervertis
  2. Ajustez les valeurs d'angle dans les fonctions ``nod_head()`` et ``shake_head()``
  3. Verifiez les positions centrales des servomoteurs (peuvent necessiter un etalonnage)

- Image trop floue ou trop sombre

  1. Assurez-vous d'un eclairage adequat sur le devoir
  2. Ajustez la mise au point de la camera si elle est reglable
  3. Positionnez la camera a 15-30 cm du papier
  4. Utilisez un stylo/marqueur a contraste eleve pour l'ecriture manuscrite

- Le bouton ne repond pas

  1. Verifiez si la LED du bouton utilisateur s'allume lorsqu'on appuie
  2. Verifiez que le rappel du bouton est enregistre
  3. Testez le bouton avec une simple instruction d'affichage

- L'IA renvoie une reponse inattendue

  1. Verifiez le formatage de l'invite dans le code
  2. Assurez-vous que l'image montre clairement la question ET la reponse
  3. Testez d'abord avec des problemes arithmetiques tres simples

----------------------------------------------


Cette demonstration de correction de devoirs montre comment les modeles de vision IA peuvent interagir avec du materiel physique pour creer des experiences educatives engageantes, melangeant l'intelligence numerique avec des mecanismes de retour tangibles !