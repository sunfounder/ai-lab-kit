.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose_squat:

8. Compteur de Squats
===============================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans le chapitre précédent, nous avons implémenté l'estimation de base de la pose humaine.
Ce chapitre s'appuie sur cette base pour implémenter un simple
**Compteur de Squats** en utilisant MediaPipe Pose.

C'est un exemple pratique combinant :

- La détection de pose
- La reconnaissance d'actions
- Le comptage en temps réel

Il peut être utilisé dans les systèmes de fitness intelligents,
les assistants d'entraînement à domicile ou les applications d'analyse de mouvement.

.. image:: img/mp_pose_s2.png
   :alt: Exemple de comptage de squats
   :align: center


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le compteur de squats est implémenté en utilisant la logique suivante :

1. Utiliser MediaPipe Pose pour détecter 33 points clés corporels.
2. Sélectionner les articulations clés (Épaule, Hanche, Cheville).
3. Utiliser les coordonnées y normalisées pour estimer la hauteur de la hanche.
4. Définir des seuils supérieur et inférieur (par exemple, 0,55 et 0,45).
5. Utiliser une machine à états simple pour détecter la transition :
   "debout → accroupi → debout".
6. Incrémenter le compteur lorsqu'un cycle complet de squat est terminé.
7. Afficher le nombre de squats et la valeur actuelle de la hanche à l'écran.

.. note::

   - Cet exemple n'utilise pas le calcul d'angle articulaire.
   - Il repose sur des coordonnées normalisées pour réduire le calcul.
   - La méthode est légère et adaptée au Raspberry Pi.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_squat.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_8.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'une personne se tient devant la caméra :

   - MediaPipe Pose détecte 33 points de repère corporels en temps réel.
   - Un squelette complet du corps est dessiné à l'écran.
   - Le système calcule en continu la position relative de la hanche (HipRel).

   Lorsque vous effectuez des squats :

   - Lorsque vous descendez et que votre hanche dépasse le seuil inférieur (DOWN_TH),
     le système marque que vous êtes en position « basse ».
   - Lorsque vous vous relevez et que la hanche dépasse le seuil supérieur (UP_TH),
     le compteur de squats augmente de 1.

   L'écran affiche :

   - ``Squats: N`` — le nombre total de squats effectués.
   - ``HipRel: value`` — la position normalisée actuelle de la hanche utilisée pour la détection.

   Le compteur n'augmente qu'après un cycle de mouvement complet
   (debout → accroupi → debout), empêchant le comptage en double.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.


-----------------------------
4. Code Complet
-----------------------------

Voici l'implémentation complète du compteur de squats :

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,
      model_complexity=1,
      enable_segmentation=True,
   )

   # ---- Count and threshold ----
   squat_count = 0
   in_bottom = False
   DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
   UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame_rgb)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If pose is detected, draw landmarks and connections on the frame
      if results.pose_landmarks:
         drawing.draw_landmarks(
               frame,
               results.pose_landmarks,
               mp_pose.POSE_CONNECTIONS,
               landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

         # Count squat without using hip angle
         lms = results.pose_landmarks.landmark
         # left 11-23-27 (shoulder, hip, ankle)
         # right 12-24-28 (shoulder, hip, ankle)
         idx_sets = [(11,23,27), (12,24,28)]
         hip_rel_list = []

         for sh, hp, an in idx_sets:
               try:
                  y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                  base = abs(y_an - y_sh)  # Distance between shoulder and ankle
                  if base > 1e-6:
                     hip_rel = (y_hp - y_sh) / base  # Position of hip relative to shoulder, 0.5 means hip is in the middle, 0 means hip is at the top, 1 means hip is at the bottom
                     hip_rel_list.append(hip_rel)
               except IndexError:
                  pass

         if hip_rel_list:
               hip_rel = min(hip_rel_list)  # Choose the smaller one, which is more stable
               # State machine:
               # from low -> mark "in_bottom";
               # from back to high -> count +1
               if not in_bottom and hip_rel >= DOWN_TH:
                  in_bottom = True
               elif in_bottom and hip_rel <= UP_TH:
                  squat_count += 1
                  in_bottom = False

               # Display
               cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
               cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le script, le système :

- Détecte le squelette humain ;
- Calcule la position relative de la hanche ;
- Compte +1 lorsqu'un cycle complet de « squat » à « debout » est terminé ;
- Affiche **Squats: N** et la valeur HipRel actuelle à l'écran en temps réel.

-----------------------------------------------
5. Conception des Coordonnées et de l'État
-----------------------------------------------

Nous utilisons les 6 points clés suivants (3 de chaque côté) :

.. list-table::
   :header-rows: 1

   * - Point clé
     - Index
     - Description
   * - Épaule
     - 11 (Gauche) / 12 (Droite)
     - Référence supérieure
   * - Hanche
     - 23 (Gauche) / 24 (Droite)
     - Élément central pour calculer la position du squat
   * - Cheville
     - 27 (Gauche) / 28 (Droite)
     - Référence inférieure

.. image:: img/mp_pose_s1.png
   :alt: Points clés MediaPipe Pose
   :align: center

**Formule de calcul de la Valeur Relative de la Hanche (Hip Relative) :**

.. math::

   hip\_rel = \frac{hip_y - shoulder_y}{ankle_y - shoulder_y}

- Une hip_rel plus grande signifie plus proche du sol (c'est-à-dire en train de s'accroupir).
- Une hip_rel plus petite signifie debout.

Nous définissons deux seuils :

- **DOWN_TH = 0.55** : Considéré comme entrant dans la position basse du squat
- **UP_TH = 0.45** : Considéré comme revenu à la position debout

Utiliser une simple machine à états pour un comptage fiable :

.. code-block:: python

   if hip_rel >= DOWN_TH:
       in_bottom = True
   if in_bottom and hip_rel <= UP_TH:
       squat_count += 1
       in_bottom = False

----------------------------------------------------
6. Réglage des Paramètres et Optimisation
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Paramètre
     - Description
     - Suggestion d'ajustement
   * - DOWN_TH
     - Seuil d'action du squat
     - Une valeur plus élevée nécessite un squat plus profond pour compter
   * - UP_TH
     - Seuil d'action debout
     - Une valeur plus basse nécessite de se tenir plus droit
   * - model_complexity
     - Complexité du modèle Pose
     - Utilisez 1 pour une vitesse plus rapide
   * - Résolution
     - Affecte la fréquence d'images et la précision
     - Recommandé 640×480

.. tip::
   Pour les personnes de différentes tailles, des seuils adaptatifs ou une calibration personnalisée peuvent être utilisés pour un comptage plus précis.

---------------------------------------------------------
7. Dépannage
---------------------------------------------------------

- Comptage inexact

  Si le comptage des squats n'est pas précis, les valeurs de seuil peuvent ne pas correspondre à la position de votre corps ou à l'angle de la caméra.

  Essayez d'afficher ``hip_rel`` en temps réel et ajustez ``DOWN_TH`` et ``UP_TH`` en conséquence.
  Assurez-vous également que votre forme de squat est cohérente et clairement visible.

- Personne non détectée

  Si le corps n'est pas détecté, améliorez les conditions d'éclairage et évitez les arrière-plans complexes.

  Assurez-vous de vous tenir entièrement dans le cadre et de faire face à la caméra directement.

- Latence élevée

  Si la réponse vidéo est lente, réduisez ``model_complexity`` à 1 et abaissez la résolution de la caméra (par exemple, 640×480 ou 320×240).

  Fermez les programmes d'arrière-plan inutiles pour améliorer les performances.

-----------------------------
8. Résumé
-----------------------------

- Implémentation d'un **compteur de squats en temps réel** utilisant les points clés Pose + machine à états ;
- Aucun calcul d'angle complexe nécessaire, haute efficacité opérationnelle ;
- Adapté au Raspberry Pi ou à d'autres applications sur appareils embarqués ;
- Extensions futures possibles :

  - Détection de pompes/abdominaux
  - Enregistrement et visualisation des données
  - Guidage rythmique automatique et retour d'entraînement