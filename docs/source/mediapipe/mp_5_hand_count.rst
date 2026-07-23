.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count:

5. Comptage de Gestes de la Main
==================================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans la section précédente, nous avons implémenté la détection de la main en temps réel
et la visualisation des points de repère.

Cette section étend cette fonctionnalité en utilisant
les positions des points de repère des doigts pour compter le nombre de
doigts levés (0 à 5).

En analysant les positions relatives du bout des doigts
et de leurs articulations correspondantes, nous pouvons déterminer
si chaque doigt est étendu.

.. image:: img/mp_hand_count.png
   :align: center


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme suit ces étapes :

1. Initialiser le modèle MediaPipe Hands.
2. Capturer des images vidéo de la caméra Raspberry Pi.
3. Détecter 21 points de repère de la main en temps réel.
4. Comparer les coordonnées du bout des doigts avec leurs articulations proximales.
5. Déterminer si chaque doigt est étendu.
6. Compter le nombre de doigts levés.
7. Afficher le résultat sur l'image vidéo.

Cette méthode est :

- Légère et efficace
- Adaptée au Raspberry Pi
- Une base pour le contrôle gestuel et les systèmes interactifs

------------------------
3. Exécuter le Code
------------------------

.. important::


   Avant de commencer, assurez-vous :

   * Que le support motorisé est assemblé
   * Que vous pouvez accéder au bureau du Raspberry Pi
   * Que le package de code est installé
   * Que Fusion HAT+ est installé et configuré
   * Qu'OpenCV est installé

   Pour les instructions détaillées, voir :ref:`opencv_install`.

#. Ouvrez le terminal et entrez la commande suivante :

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_5.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'une main apparaît devant la caméra :

   - MediaPipe détecte la main en temps réel.
   - 21 points de repère et lignes de connexion sont dessinés sur la main.
   - Le programme analyse les positions du bout des doigts et des articulations.
   - Le nombre de doigts levés (0 à 5) est calculé.

   Le nombre de doigts détecté est affiché dans le coin supérieur gauche
   de l'écran comme suit :

      Fingers: X

   Au fur et à mesure que vous étendez ou pliez vos doigts, le nombre se met
   à jour instantanément en temps réel.

   Si aucune main n'est détectée, seul le flux normal de la caméra
   est affiché sans comptage de doigts.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.



-----------------------------
4. Code Complet
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Hands model
   hands = mp_hands.Hands(
      static_image_mode=False,  # Set to False for processing video frames
      max_num_hands=2,           # Maximum number of hands to detect
      min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Finger tips and dips
   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for hand detection and tracking
      hands_detected = hands.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections on the frame
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
               )


               # Count the number of fingers raised (right hand)
               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Check if thumb is up
               if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                  finger_count += 1

               # Check if the other fingers are up
               for i in range(1, 5):
                  if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                     finger_count += 1

               # Display the number of fingers raised
               cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Dans chaque itération de la boucle, il détermine si chacun des 5 doigts est étendu et compte le nombre de doigts étendus. Par exemple :

- ✊ Tous les doigts fermés → Compte 0
- ☝️ Index étendu → Compte 1
- ✌️ Index + Majeur → Compte 2
- 🖐️ Les cinq doigts ouverts → Compte 5

--------------------------------------------------------------
5. Logique de Détection et Extensions
--------------------------------------------------------------

MediaPipe Hands retourne 21 points de repère.
Nous utilisons les positions du bout des doigts et des articulations pour déterminer
si chaque doigt est étendu.

.. code-block:: python

   finger_tips = [4, 8, 12, 16, 20]
   finger_dips = [2, 6, 10, 14, 18]

- ``finger_tips`` → Indices du bout des doigts
  (Pouce=4, Index=8, Majeur=12, Annulaire=16, Auriculaire=20)

- ``finger_dips`` → Articulations proximales correspondantes
  (Pouce=2, Index=6, Majeur=10, Annulaire=14, Auriculaire=18)

------------------------------------------------------------

Logique de comptage des doigts :

.. code-block:: python

   landmarks = hand_landmarks.landmark
   finger_count = 0

   # Check thumb (right hand)
   if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
       finger_count += 1

   # Check other four fingers
   for i in range(1, 5):
       if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
           finger_count += 1

   cv2.putText(frame, f"Fingers: {finger_count}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

Explication de la logique :

- **Pouce** → Comparer ``tip.x`` et ``dip.x`` (pour la main droite).
- **Autres doigts** → Comparer ``tip.y`` et ``dip.y``.
- Si le bout du doigt est au-dessus (ou vers l'extérieur) de l'articulation,
  le doigt est considéré comme étendu.
- Chaque condition satisfaite augmente le compteur de ``+1``.

------------------------------------------------------------

Conseils d'extension :

- Pour supporter les deux mains gauche et droite,
  utilisez ``hands_detected.multi_handedness`` pour déterminer le type de main,
  et inversez la comparaison de l'axe x du pouce en conséquence.

- Cette logique peut être étendue pour implémenter :

  - La reconnaissance du geste OK
  - La détection du pouce levé
  - L'interaction pierre–papier–ciseaux
  - Des contrôles gestuels personnalisés

------------------------------------------------------------
6. Dépannage
------------------------------------------------------------

- Détection du pouce inexacte

  La détection du pouce peut être inexacte car la logique diffère pour les mains gauche et droite. La comparaison horizontale utilisée pour le pouce dépend de l'orientation de la main.

  Utilisez ``multi_handedness`` pour déterminer si la main détectée est gauche ou droite, et ajustez la logique de détection du pouce en conséquence.

- Détection instable

  Si le comptage des doigts semble instable, l'éclairage peut être insuffisant ou l'arrière-plan peut être encombré.

  Améliorez les conditions d'éclairage et utilisez un arrière-plan simple pour augmenter la stabilité de la détection.

- Latence élevée

  Si la réponse semble lente, la résolution peut être trop élevée ou le CPU peut être surchargé.

  Réduisez la résolution (par exemple, 320x240) et fermez les processus d'arrière-plan inutiles. Vous pouvez également simplifier la logique de comptage des doigts si nécessaire.


-----------------------------
7. Résumé
-----------------------------

- En utilisant MediaPipe Hands, nous pouvons rapidement implémenter la **reconnaissance de gestes en temps réel**.
- Cette section a implémenté le **comptage de gestes numériques** basé sur les positions du bout des doigts, posant les bases pour la reconnaissance de gestes personnalisés.
- En s'adaptant aux mains gauche/droite et en élargissant les règles de jugement, des scénarios interactifs plus complexes peuvent être réalisés.