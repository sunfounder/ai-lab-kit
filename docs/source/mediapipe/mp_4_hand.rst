.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand:


4. Détection des Mains
===================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans la section précédente, nous avons implémenté la détection faciale
et le suivi des points de repère avec MediaPipe.

Cette section présente **MediaPipe Hands** —
un module de détection de points de repère de la main léger, stable et en temps réel.

Grâce à ce module, nous pouvons :

- Détecter jusqu'à deux mains simultanément
- Identifier 21 points de repère par main
- Visualiser les connexions du squelette de la main en temps réel

.. image:: img/mp_hand.png
   :alt: MediaPipe Hands
   :align: center


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme suit ces étapes :

1. Initialiser le modèle MediaPipe Hands.
2. Capturer des images de la caméra Raspberry Pi.
3. Convertir l'image au format RGB (requis par MediaPipe).
4. Détecter les points de repère de la main à l'aide du module Hands.
5. Dessiner les 21 points de repère et leurs lignes de connexion.
6. Afficher le flux vidéo annoté en temps réel.

Ce module sert de base pour :

- La reconnaissance de gestes
- Le comptage des doigts
- Les systèmes de contrôle interactifs
- L'interaction homme-machine sans contact

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_4.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'une ou deux mains apparaissent devant la caméra :

   - MediaPipe détecte chaque main en temps réel.
   - 21 points de repère sont identifiés sur chaque main.
   - Les points de repère sont reliés par des lignes pour former un squelette de la main.

   Si deux mains sont visibles, les deux mains sont suivies et
   annotées simultanément.

   Au fur et à mesure que l'utilisateur bouge les mains ou les doigts :

   - Les points de repère suivent le mouvement en douceur.
   - Le squelette de la main se met à jour en temps réel.

   Si aucune main n'est détectée, le programme affiche simplement
   le flux normal de la caméra sans annotations.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.

-----------------------------
4. Code Complet
-----------------------------

Le code d'exemple complet est le suivant :

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize Hands model
   hands = mp_hands.Hands(
       static_image_mode=False,    # Process real-time video frames
       max_num_hands=2,            # Maximum number of hands to detect
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   # picam2.start_preview(Preview.QTGL) # Optional hardware preview
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to RGB
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Detect hands
      hands_detected = hands.process(frame_rgb)

      # Convert RGB back to BGR for display
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If hands are detected, draw landmarks and connections
      if hands_detected.multi_hand_landmarks:
         for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                  frame,
                  hand_landmarks,
                  mp_hands.HAND_CONNECTIONS,
                  drawing_styles.get_default_hand_landmarks_style(),
                  drawing_styles.get_default_hand_connections_style(),
            )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le code, vous verrez dans le flux de la caméra :

- Si une ou deux mains sont détectées, cela montrera :

  - 21 points de repère de la main
  - Un squelette de connexion bleu
- Lorsque la main bouge, la détection la suivra en temps réel.

--------------------------------------------------------
5. Description des Points de Repère MediaPipe Hands
--------------------------------------------------------

MediaPipe Hands retourne **21 points de repère** pour chaque main, incluant des emplacements comme le poignet, la paume et le bout des doigts.

Les points de repère courants incluent :

.. list-table::
   :header-rows: 1

   * - Index
     - Nom
     - Emplacement
   * - 0
     - WRIST
     - Poignet
   * - 4 / 8 / 12 / 16 / 20
     - THUMB_TIP / INDEX_FINGER_TIP / MIDDLE_FINGER_TIP / RING_FINGER_TIP / PINKY_TIP
     - Bout des doigts respectifs
   * - 5~17
     - Joints
     - Articulations médianes des doigts respectifs
   * - 9
     - PALM_CENTER (approximatif)
     - Zone de la paume

.. image:: img/mp_hand_point.png
  :width: 400
  :alt: Illustration des points de repère MediaPipe Hands
  :align: center

.. note::
   Ces coordonnées sont des **coordonnées normalisées** et peuvent être converties en positions réelles en pixels en fonction de la résolution de l'image.
   Elles peuvent être utilisées pour calculer des angles et des distances, permettant la reconnaissance de gestes.

------------------------------------------------------------
6. Dépannage
------------------------------------------------------------

- Détection de la main instable

  La détection de la main peut devenir instable si l'éclairage est trop faible, l'arrière-plan est encombré ou la main bouge trop rapidement.

  Essayez d'améliorer l'éclairage, d'utiliser un arrière-plan simple et de bouger vos mains plus lentement et plus régulièrement.

- Aucune main détectée

  Si aucune main n'est détectée, l'angle de la caméra peut ne pas convenir, la main peut être trop loin de la caméra ou la résolution peut être trop faible.

  Ajustez la position de la caméra, rapprochez-vous et assurez-vous que la résolution est d'au moins 640x480.

- Latence élevée

  Si la réponse vidéo semble lente, le Raspberry Pi peut être surchargé ou la résolution peut être trop élevée.

  Réduisez la résolution (par exemple, 320x240) et fermez les processus d'arrière-plan inutiles.


-----------------------------
7. Résumé
-----------------------------

- MediaPipe Hands permet une **détection de la main en temps réel** stable sur le Raspberry Pi.
- Fournit 21 points de repère par main, adaptés pour :

  - La reconnaissance de gestes
  - Le contrôle virtuel
  - Le contrôle d'interface utilisateur interactif

- Ensuite, nous implémenterons la **reconnaissance de gestes personnalisés** basée sur ces points de repère.