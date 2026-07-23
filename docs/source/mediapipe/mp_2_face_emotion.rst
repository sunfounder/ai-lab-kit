.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_emotion:

2. Détection d'Émotions
===============================================

-----------------------------
1. Aperçu
-----------------------------

Dans cette section, nous étendons la détection Face Mesh pour effectuer
une reconnaissance de base des émotions.

Au lieu d'utiliser des modèles d'apprentissage profond, cette méthode utilise
la géométrie des points de repère faciaux (rapports des yeux et de la bouche) pour classer
les expressions en temps réel.

.. image:: img/mp_face_emotion_happy.png
   :align: center

Émotions reconnaissables :

- 😮 Surpris
- 😀 Heureux
- 😢 Triste
- 😠 En colère
- 😐 Neutre

-----------------------------
2. Comment ça Fonctionne
-----------------------------

Le programme suit ces étapes :

1. Utiliser ``Picamera2`` + ``MediaPipe FaceMesh`` pour obtenir 468 points de repère.
2. Sélectionner les points caractéristiques clés autour des yeux et de la bouche.
3. Calculer les rapports normalisés :

   - Ouverture des yeux
   - Largeur de la bouche
   - Ouverture de la bouche

4. Comparer les valeurs avec des seuils prédéfinis.
5. Afficher l'émotion détectée à l'aide d'OpenCV.

Avantages de cette approche :

- Rapide et léger (adapté au Raspberry Pi)
- Aucun réseau neuronal requis
- Facile à ajuster les seuils

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

        sudo python3 ~/ai-lab-kit/mediapipe/mp_face_emotion.py

#. Après avoir exécuté le programme, une fenêtre vidéo s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_2.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'un visage apparaît devant la caméra, le système :

   - Détecte 468 points de repère faciaux en temps réel
   - Calcule les rapports d'ouverture des yeux et d'ouverture de la bouche
   - Classifie l'expression faciale actuelle

   L'étiquette d'émotion détectée (comme ``Happy``, ``Surprised``, ``Sad``, ``Angry`` ou ``Neutral``) est affichée sur l'écran vidéo.

   Au fur et à mesure que l'utilisateur change d'expression faciale, l'étiquette d'émotion se met à jour instantanément.

   Si aucun visage n'est détecté, le programme continue d'afficher le flux normal de la caméra sans étiquette d'émotion.

   Appuyez sur ``q`` pour quitter le programme. La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.


-----------------------------
4. Code Complet
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   import numpy as np

   # --------- Emotion judgment auxiliary function ---------
   def euclidean(p1, p2):
       return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

   def classify_emotion(landmarks):
       """
       landmarks: results.multi_face_landmarks[0].landmark (length ~468)
       Returns (label, details_dict)
       """
       # Keypoint Index (MediaPipe 468 points)
       L_EYE_TOP, L_EYE_BOT = 159, 145
       R_EYE_TOP, R_EYE_BOT = 386, 374
       L_EYE_CENTER, R_EYE_CENTER = 33, 263
       MOUTH_LEFT, MOUTH_RIGHT = 61, 291
       LIP_UP, LIP_DOWN = 13, 14

       # Normalization scale: distance between left and right eye centers
       io = euclidean(landmarks[L_EYE_CENTER], landmarks[R_EYE_CENTER])
       if io < 1e-6:
           return "Neutral", {}

       mouth_width = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT]) / io
       mouth_open  = euclidean(landmarks[LIP_UP], landmarks[LIP_DOWN]) / io
       eye_open_L  = euclidean(landmarks[L_EYE_TOP], landmarks[L_EYE_BOT]) / io
       eye_open_R  = euclidean(landmarks[R_EYE_TOP], landmarks[R_EYE_BOT]) / io
       eye_open    = 0.5 * (eye_open_L + eye_open_R)

       # --------- Simple threshold rules (adjustable) ---------
       if mouth_open > 0.08 and eye_open > 0.055:
           label = "Surprised"
       elif mouth_width > 0.48 and mouth_open > 0.035:
           label = "Happy"
       elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
           label = "Sad"
       elif mouth_open < 0.02 and eye_open < 0.028:
           label = "Angry"
       else:
           label = "Neutral"

       details = {
           "mouth_width": round(mouth_width, 3),
           "mouth_open": round(mouth_open, 3),
           "eye_open": round(eye_open, 3),
       }
       return label, details

   # Initialize FaceMesh
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       results = face.process(frame)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

               # --------- Emotion detection ---------
               label, metrics = classify_emotion(face_landmarks.landmark)

               # Draw emotion label on the frame
               cv2.putText(frame, f"Emotion: {label}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

               # Debug information
               dbg = f"mw:{metrics.get('mouth_width',0)} mo:{metrics.get('mouth_open',0)} eo:{metrics.get('eye_open',0)}"
               cv2.putText(frame, dbg, (20, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après l'exécution, la catégorie d'émotion reconnue sera affichée en temps réel sur le flux de la caméra, ainsi que des informations de débogage comprenant la largeur de la bouche, l'ouverture de la bouche, l'ouverture des yeux, etc.

-----------------------------
5. Explication des Étapes Clés
-----------------------------

#. Sélectionner les points clés

   .. code-block:: python

      # Keypoint Index (MediaPipe 468 points)
      L_EYE_TOP, L_EYE_BOT = 159, 145
      R_EYE_TOP, R_EYE_BOT = 386, 374
      L_EYE_CENTER, R_EYE_CENTER = 33, 263
      MOUTH_LEFT, MOUTH_RIGHT = 61, 291
      LIP_UP, LIP_DOWN = 13, 14

   Ces indices correspondent à :

   - 159, 145 → Bords supérieur et inférieur de l'œil gauche
   - 386, 374 → Bords supérieur et inférieur de l'œil droit
   - 33, 263 → Centres des yeux (utilisés pour la normalisation)
   - 61, 291 → Coins de la bouche
   - 13, 14 → Points médians des lèvres supérieure et inférieure

   .. image:: img/mp_face_point.jpg
      :align: center

#. Normaliser les distances

   Pour réduire l'influence de la distance de la caméra,
   utilisez la distance entre les deux centres des yeux
   comme échelle de normalisation.

   .. code-block:: python

      def euclidean(p1, p2):
          return np.linalg.norm(
              np.array([p1.x, p1.y]) -
              np.array([p2.x, p2.y])
          )

      io = euclidean(
          landmarks[L_EYE_CENTER],
          landmarks[R_EYE_CENTER]
      )

#. Calculer les caractéristiques géométriques

   .. code-block:: python

      mouth_width = euclidean(
          landmarks[MOUTH_LEFT],
          landmarks[MOUTH_RIGHT]
      ) / io

      mouth_open = euclidean(
          landmarks[LIP_UP],
          landmarks[LIP_DOWN]
      ) / io

      eye_open_L = euclidean(
          landmarks[L_EYE_TOP],
          landmarks[L_EYE_BOT]
      ) / io

      eye_open_R = euclidean(
          landmarks[R_EYE_TOP],
          landmarks[R_EYE_BOT]
      ) / io

      eye_open = 0.5 * (eye_open_L + eye_open_R)

   Caractéristiques calculées :

   - ``mouth_width`` → Largeur horizontale de la bouche
   - ``mouth_open`` → Ouverture verticale de la bouche
   - ``eye_open`` → Ouverture moyenne des yeux

#. Classifier l'émotion à l'aide de seuils

   .. code-block:: python

      if mouth_open > 0.08 and eye_open > 0.055:
          label = "Surprised"
      elif mouth_width > 0.48 and mouth_open > 0.035:
          label = "Happy"
      elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
          label = "Sad"
      elif mouth_open < 0.02 and eye_open < 0.028:
          label = "Angry"
      else:
          label = "Neutral"

   Règles d'émotion (seuils empiriques) :

   - Surpris → Bouche et yeux grands ouverts
   - Heureux → Bouche large, yeux normaux
   - Triste / En colère → Bouche et yeux principalement fermés
   - Neutre → Ne correspond pas aux autres conditions

-----------------------------------------------------
6. Ajustement des Seuils et Robustesse
-----------------------------------------------------

- Les seuils comme ``0.08``, ``0.035``, ``0.018`` sont basés sur des valeurs empiriques en résolution 640x480.
- Si la caméra est plus proche ou la résolution différente, ajustez les seuils en utilisant les informations de débogage (mw/mo/eo).
- La logique de jugement des émotions peut être modifiée pour être plus complexe ou utiliser des modèles entraînés pour une précision plus élevée, comme le calcul de la position relative des coins de la bouche, la forme de la bouche, etc.

------------------------------------------------------------
7. Dépannage
------------------------------------------------------------

- La reconnaissance des émotions n'est pas sensible

  Les seuils peuvent ne pas correspondre à la distance actuelle de la caméra.
  Ajustez les valeurs ``mouth_open`` et ``eye_open``.

- Latence de détection

  La résolution peut être trop élevée.
  Réduisez la résolution ou désactivez ``refine_landmarks``.

- Impossible de reconnaître l'émotion

  L'éclairage peut être insuffisant ou l'angle du visage est de travers.
  Améliorez l'éclairage et faites face à la caméra directement.

-----------------------------
8. Résumé
-----------------------------

- Ce chapitre a implémenté la reconnaissance légère des émotions basée sur les **caractéristiques géométriques + points de repère FaceMesh**.
- Offre des avantages de **haute performance en temps réel** et de **seuils ajustables**.
- Peut être utilisé dans des projets comme l'art interactif, l'IHM, la détection d'état en classe/réunion.