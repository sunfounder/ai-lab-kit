.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_gesture:


6. Reconnaissance de Gestes de la Main
==========================================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans le chapitre précédent, nous avons utilisé MediaPipe Hands
pour obtenir 21 points de repère de la main et visualiser le squelette de la main.

Ce chapitre présente **MediaPipe Tasks – Gesture Recognizer**,
qui peut directement produire des étiquettes de gestes sémantiques telles que :

- ``Thumb_Up``
- ``Open_Palm``
- ``Victory``
- ``Closed_Fist``

En combinant :

- ``Picamera2`` pour la capture vidéo
- ``MediaPipe Hands`` pour la visualisation des points de repère
- ``Gesture Recognizer`` pour la classification

nous pouvons réaliser une reconnaissance de gestes en temps réel
avec à la fois le rendu du squelette et l'affichage des étiquettes.

.. image:: img/mp_hang_gesture.png
   :alt: Gesture Recognizer
   :align: center


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme effectue les étapes suivantes :

1. Capturer des images vidéo avec ``Picamera2``.
2. (Optionnel) Utiliser ``MediaPipe Hands`` pour dessiner les points de repère.
3. Utiliser **MediaPipe Tasks – Gesture Recognizer** en mode ``VIDEO``.
4. Pour chaque main détectée, obtenir :

   - La liste des catégories de gestes (étiquette + confiance)
   - La latéralité (Gauche / Droite)
   - Les points de repère normalisés

5. Sélectionner le meilleur geste (top-1) et dessiner
   « étiquette + score de confiance »
   au-dessus de la main correspondante.

.. note::

   Ce chapitre utilise l'API **MediaPipe Tasks (0.10+)**.


------------------------------------------------------------
3. Modèle
------------------------------------------------------------

Gesture Recognizer nécessite un fichier de modèle :

``gesture_recognizer.task``

Le fichier de modèle est déjà inclus dans le répertoire d'exemple.
Veuillez utiliser la version fournie.

Le modèle intégré supporte les étiquettes de gestes suivantes :

- 0 → ``Unknown``
- 1 → ``Closed_Fist``
- 2 → ``Open_Palm``
- 3 → ``Pointing_Up``
- 4 → ``Thumb_Down``
- 5 → ``Thumb_Up``
- 6 → ``Victory``
- 7 → ``ILoveYou``

------------------------
4. Exécuter le Code
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_gesture.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_6.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'une ou deux mains apparaissent devant la caméra, le programme :

   - Détecte et dessine les 21 points de repère de la main et les lignes de connexion (squelette de la main) en temps réel.
   - Exécute le modèle Gesture Recognizer sur chaque image pour classer le geste.

   Si un geste est reconnu avec un score supérieur à ``SCORE_THRESHOLD`` (valeur par défaut 0,5), le programme affiche une étiquette près de la main correspondante, comprenant :

   - La latéralité (Gauche/Droite)
   - Le nom du geste (par exemple, ``Thumb_Up``, ``Open_Palm``, ``Victory``)
   - Le score de confiance (par exemple, ``0.87``)

   Une fine boîte englobante est également dessinée autour de la zone de la main pour rendre le placement de l'étiquette plus clair.

   Au fur et à mesure que vous changez de pose de la main, l'étiquette et le score du geste se mettent à jour en continu en temps réel.

   Si aucune main n'est détectée, ou si la confiance du geste est inférieure au seuil, seul le squelette de la main (ou le flux brut de la caméra) est affiché sans étiquettes de geste.

   Appuyez sur ``q`` pour quitter le programme. La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.


-----------------------------
5. Code Complet
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Import MediaPipe Tasks (Gesture Recognizer)
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   from pathlib import Path

   # --------------------- Settings ---------------------
   BASE_DIR = Path(__file__).resolve().parent
   GESTURE_MODEL_PATH = str(BASE_DIR / "gesture_recognizer.task")  # Path to the gesture model
   SCORE_THRESHOLD = 0.5                           # Show gestures above this score
   # ---------------------------------------------------

   # Initialize the Hands model (kept for landmark drawing)
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

   # Initialize Gesture Recognizer (VIDEO mode for streaming)
   BaseOptions = python.BaseOptions
   GestureRecognizerOptions = vision.GestureRecognizerOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=GESTURE_MODEL_PATH)
   gr_options = GestureRecognizerOptions(
       base_options=base_options,
       running_mode=RunningMode.VIDEO
   )
   recognizer = vision.GestureRecognizer.create_from_options(gr_options)

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # (Optional) helper to draw a label near a hand bounding box computed from landmarks
   def draw_gesture_label(frame_bgr, norm_landmarks, text, color=(0, 175, 255)):
       """
       norm_landmarks: list of 21 normalized landmarks (x,y in [0,1]).
       We compute a tight bbox to place the gesture text.
       """
       if not norm_landmarks:
           return
       h, w = frame_bgr.shape[:2]
       xs = [int(lm.x * w) for lm in norm_landmarks]
       ys = [int(lm.y * h) for lm in norm_landmarks]
       x1, y1 = max(0, min(xs)), max(0, min(ys))
       x2, y2 = min(w-1, max(xs)), min(h-1, max(ys))
       cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), color, 1)
       (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
       y_text = max(0, y1 - th - 6)
       cv2.rectangle(frame_bgr, (x1, y_text), (x1 + tw + 6, y_text + th + 6), color, -1)
       cv2.putText(frame_bgr, text, (x1 + 3, y_text + th + 2),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2, cv2.LINE_AA)

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert the frame from BGR to RGB (required by MediaPipe)
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # ---- A) Run legacy Hands (for landmark drawing you already have) ----
       hands_detected = hands.process(frame_rgb)

       # ---- B) Run Gesture Recognizer (direct gesture labels) ----
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
       ts_ms = int((cv2.getTickCount() / cv2.getTickFrequency()) * 1000)
       gesture_result = recognizer.recognize_for_video(mp_image, ts_ms)

       # Convert the frame back from RGB to BGR (required by OpenCV)
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

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

       # ---- C) Overlay gesture names on top of each detected hand ----
       if gesture_result and getattr(gesture_result, "gestures", None):
           for i, gesture_list in enumerate(gesture_result.gestures):
               if not gesture_list:
                   continue
               top = gesture_list[0]
               label = top.category_name  # e.g., "Thumb_Up"
               score = top.score or 0.0
               if score < SCORE_THRESHOLD:
                   continue

               hand_label = ""
               if gesture_result.handedness and i < len(gesture_result.handedness):
                   if gesture_result.handedness[i]:
                       hand_label = gesture_result.handedness[i][0].category_name or ""

               text = f"{hand_label} {label} ({score:.2f})".strip()

               hand_lms = None
               if gesture_result.hand_landmarks and i < len(gesture_result.hand_landmarks):
                   hand_lms = gesture_result.hand_landmarks[i]

               if hand_lms:
                   draw_gesture_label(frame, hand_lms, text)
               else:
                   cv2.putText(frame, text, (20, 40 + 30*i),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 175, 255), 2, cv2.LINE_AA)

       # Display the frame with annotations
       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   # Release the camera
   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le script, la fenêtre affichera le squelette de la main (optionnel) et les boîtes de texte des gestes. Lorsqu'un geste correspondant aux catégories du modèle est reconnu, il s'affichera au-dessus de la boîte englobante de la main correspondante :

- Main gauche/droite (latéralité)
- Nom du geste (par exemple, ``Thumb_Up``)
- Score de confiance (0~1)

-----------------------------
6. Explication du Code
-----------------------------

Cet exemple combine deux parties :

- **Hands (Solutions API)** : utilisé pour dessiner le squelette de la main (21 points de repère + connexions).
- **Gesture Recognizer (Tasks API)** : utilisé pour prédire une étiquette de geste comme ``Thumb_Up`` ou ``Open_Palm``.

**Flux général**

#. Initialiser Hands pour le dessin des points de repère (optionnel mais utile pour la visualisation).
#. Charger le modèle Gesture Recognizer (``gesture_recognizer.task``) et activer le mode ``VIDEO``.
#. Démarrer la caméra et traiter les images dans une boucle :

   - Convertir l'image en RGB (MediaPipe nécessite RGB).
   - Exécuter Hands pour dessiner le squelette.
   - Exécuter Gesture Recognizer pour obtenir ``étiquette + score`` pour chaque main.
   - Dessiner l'étiquette près de la main correspondante.

#. Appuyer sur ``q`` pour quitter et libérer les ressources.

**Points clés à comprendre**

- Fichier de modèle

  Gesture Recognizer nécessite ``gesture_recognizer.task``. Assurez-vous que le fichier de modèle est placé dans le même dossier que le script (ou mettez à jour le chemin).

- Le mode VIDEO nécessite des horodatages

  ``recognize_for_video()`` a besoin d'un horodatage en millisecondes qui augmente continuellement. Dans cet exemple, nous le générons en utilisant le temps tick d'OpenCV.

- Afficher les étiquettes avec un seuil de confiance

  Seuls les gestes avec un score >= ``SCORE_THRESHOLD`` sont affichés. Cela évite d'afficher des prédictions instables.

-----------------------------
7. Paramètres et Réglage
-----------------------------

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Suggestion
   * - ``SCORE_THRESHOLD``
     - Les gestes en dessous de ce score sont ignorés
     - Augmentez pour réduire les faux positifs ; diminuez pour améliorer le rappel
   * - ``max_num_hands``
     - Nombre de mains à détecter simultanément
     - 2 est suffisant pour la plupart des scénarios
   * - ``running_mode=VIDEO``
     - Mode flux vidéo, nécessite un horodatage
     - Continuez à utiliser (la reconnaissance en continu est plus stable)
   * - Résolution
     - Affecte la vitesse et la précision
     - Recommandé 640x480 ou moins sur Raspberry Pi pour de meilleurs FPS

-------------------------------------------------------
8. Dépannage
-------------------------------------------------------

- ``FileNotFoundError: gesture_recognizer.task``

  Cela signifie généralement que le chemin du fichier de modèle est incorrect.
  Assurez-vous que le fichier de modèle est placé dans le même répertoire que le script,
  ou mettez à jour ``GESTURE_MODEL_PATH`` en conséquence.

- ``ImportError: cannot import name 'vision'``

  Cette erreur indique que la version de MediaPipe est obsolète.
  Mettez à jour MediaPipe vers la version 0.10 ou ultérieure en utilisant :

  ``pip install --upgrade mediapipe``

- La catégorie reconnue diffère des attentes

  L'ensemble des catégories du modèle peut différer, ou les conditions d'éclairage peuvent affecter la reconnaissance.
  Essayez d'améliorer l'éclairage, de simplifier l'arrière-plan,
  ou de passer à une version de modèle différente.

- Faible fréquence d'images

  Les performances du Raspberry Pi peuvent être limitées.
  Réduisez la résolution, désactivez le dessin du squelette,
  ou fermez les processus d'arrière-plan inutiles.

-----------------------------
8. Résumé
-----------------------------

- **Gesture Recognizer** permet la reconnaissance de gestes sémantiques en temps réel sur Raspberry Pi ;
- Combiné avec le rendu du squelette **Hands**, c'est à la fois intuitif et facile à déboguer ;
- En ajustant les seuils et la résolution, un équilibre entre « stabilité / vitesse » peut être atteint ;
- Possibilités futures :

  - Mapper différents gestes à des commandes spécifiques (raccourcis, contrôle GPIO, etc.) ;
  - Entraîner des modèles de gestes personnalisés pour des scénarios spécifiques.