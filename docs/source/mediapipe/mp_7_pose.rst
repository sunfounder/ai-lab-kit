.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_pose:


7. Estimation de la Pose Humaine
=============================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Après avoir implémenté la reconnaissance des mains et des gestes,
ce chapitre présente **MediaPipe Pose** —
un module d'estimation de pose humaine en temps réel, léger mais puissant.

Grâce à MediaPipe Pose, nous pouvons détecter **33 points de repère corporels**
en temps réel et dessiner le squelette complet du corps sur le flux vidéo.

.. image:: img/mp_pose.png
   :width: 400
   :align: center

Ce module peut être utilisé pour :

- La reconnaissance d'actions
- La correction de posture
- Le suivi de condition physique
- L'analyse de mouvement

------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme effectue les étapes suivantes :

1. Initialiser le modèle MediaPipe Pose
   (configurer la complexité du modèle et la segmentation optionnelle).
2. Capturer des images vidéo avec ``Picamera2``.
3. Convertir les images au format RGB (requis par MediaPipe).
4. Exécuter le modèle Pose pour obtenir 33 points clés corporels.
5. Dessiner les points clés et les connexions du squelette avec OpenCV.
6. Afficher le flux vidéo annoté en temps réel.

Ce chapitre pose les bases pour des tâches plus avancées
d'interaction homme-machine et d'analyse de mouvement corporel.


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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose.py

   Si vous souhaitez utiliser MediaPipe Pose avec une vidéo enregistrée, vous pouvez exécuter la commande suivante :

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_video.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_7.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'une personne apparaît devant la caméra :

   - MediaPipe Pose détecte 33 points de repère corporels en temps réel.
   - Un squelette complet du corps est dessiné sur l'image vidéo.
   - Les articulations clés telles que les épaules, les coudes, les poignets, les hanches, les genoux et les chevilles sont reliées par des lignes.

   Au fur et à mesure que la personne bouge :

   - Les points clés du squelette suivent le mouvement du corps en douceur.
   - Le squelette se met à jour en continu en temps réel.

   Si la segmentation d'arrière-plan est activée (``enable_segmentation=True``),
   le modèle calcule en interne un masque de segmentation, bien que dans cet exemple
   seul le squelette soit affiché.

   Si aucune personne n'est détectée, le programme affiche simplement le flux normal de la caméra sans annotations.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.

-----------------------------
4. Code Complet
-----------------------------

Voici un programme de base de détection de pose humaine :

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the Pose model
   pose = mp_pose.Pose(
       static_image_mode=False,  # False for processing video streams
       model_complexity=2,       # 0~2, higher is more accurate
       enable_segmentation=True, # Enable background segmentation (optional)
   )

   # Open the camera
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

      # Convert BGR to RGB (required by MediaPipe)
      frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Pose detection
      results = pose.process(frame_rgb)

      # Convert RGB back to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

      # If human body is detected, draw skeleton
      if results.pose_landmarks:
         drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
         )

      cv2.imshow("Show Video", frame)

      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le programme, le flux de la caméra affichera un squelette humain en temps réel, comprenant :

- 33 points clés
- Des lignes de connexion du squelette
- Le squelette suit le mouvement lorsque la personne bouge

-----------------------------
5. Explication du Code
-----------------------------

**1. Importer les bibliothèques**

.. code-block:: python

  from picamera2 import Picamera2, Preview
  import cv2
  import mediapipe.python.solutions.pose as mp_pose
  import mediapipe.python.solutions.drawing_utils as drawing
  import mediapipe.python.solutions.drawing_styles as drawing_styles

* **Picamera2**
  Contrôle la caméra Raspberry Pi, basée sur libcamera.

* **cv2 (OpenCV)**
  Utilisé pour la conversion d'espace colorimétrique (BGR↔RGB), les fenêtres d'affichage, le dessin graphique.

* **mediapipe.python.solutions.pose**
  Le **modèle Pose** de MediaPipe, qui peut détecter **33 points clés du corps complet** (tête, épaules, coudes, genoux, etc.), et peut retourner des masques de segmentation (humain vs. arrière-plan).

* **drawing_utils / drawing_styles**
  Les outils de dessin intégrés de MediaPipe et les définitions de style, utilisés pour dessiner les points clés et les lignes du squelette.

**2. Initialiser le modèle Pose**

.. code-block:: python

  pose = mp_pose.Pose(
      static_image_mode=False,  # Continuous video mode
      model_complexity=1,
      enable_segmentation=True,
  )

* ``static_image_mode=False`` : Indique que l'entrée est un flux vidéo continu, pas une image unique. Effectue un suivi après la détection initiale pour plus de rapidité. Généralement défini sur False.

* ``model_complexity=1`` : Complexité du modèle, 0=léger, 1=moyen, 2=haute précision (plus lent). Réglez sur 1 ou 2 si les performances du Raspberry Pi le permettent.

* ``enable_segmentation=True`` : Produit un masque de segmentation humaine, peut distinguer la personne au premier plan de l'arrière-plan. Quand il est True, active des effets comme le remplacement d'arrière-plan, l'incrustation. Cette utilisation sera expliquée dans la documentation suivante : :ref:`mp_pose_segmentation`

MediaPipe Pose retourne une structure de résultat incluant :

* ``pose_landmarks`` : 33 points clés ;
* ``pose_world_landmarks`` : Coordonnées 3D mondiales ;
* ``segmentation_mask`` : Carte de segmentation humaine.

**3. Ouvrir la caméra**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   picam2.start()

* Créer l'objet caméra ``Picamera2()``
* Définir la résolution **640x480**, le format de pixel ``"XRGB8888"`` (BGRA 4 canaux).
  Ce format a la meilleure compatibilité avec OpenCV, éliminant les étapes de décodage.
* Démarrer la caméra.

**4. Boucle principale : Traiter chaque image**

.. code-block:: python

   while True:
      frame_bgra = picam2.capture_array()               # Capture a frame from the camera (BGRA format)
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

1. Capturer l'image actuelle. Picamera2 retourne les images au format **BGRA** (Bleu Vert Rouge + Alpha) par défaut.
2. Convertir en **BGR** pour le traitement OpenCV ultérieur.

.. code-block:: python

   # Convert to RGB for MediaPipe
   frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
   results = pose.process(frame)

Les modèles MediaPipe **doivent utiliser RGB**.

* Appeler ``pose.process()`` pour la détection des points clés.
* ``results`` est un objet complexe qui peut contenir :

  * ``results.pose_landmarks`` : Points clés (33 points)
  * ``results.pose_world_landmarks`` : Coordonnées 3D
  * ``results.segmentation_mask`` : Masque de segmentation

.. code-block:: python

   # Convert back to BGR for OpenCV display
   frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

Reconvertir car ``imshow()`` d'OpenCV nécessite l'ordre BGR.

**5. Dessiner les points clés de la pose**

.. code-block:: python

   if results.pose_landmarks:
      drawing.draw_landmarks(
         frame,
         results.pose_landmarks,
         mp_pose.POSE_CONNECTIONS,
         landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
      )

Si un corps humain est détecté :

* ``results.pose_landmarks`` : Contient ``(x, y, z, visibility)`` pour chaque point clé.

  * ``x, y`` : Coordonnées normalisées (0~1)
  * ``z`` : Profondeur relative
  * ``visibility`` : Confiance du point clé (0~1)

* ``draw_landmarks`` explication des paramètres :

   * ``frame`` : Image sur laquelle dessiner (format BGR)
   * ``results.pose_landmarks`` : Points clés humains pour l'image actuelle
   * ``mp_pose.POSE_CONNECTIONS`` : Règles de connexion (quels points relier avec des lignes)
   * ``landmark_drawing_spec`` : Style de dessin des points
   * ``connection_drawing_spec`` : Style de dessin des lignes (peut être omis, utilise le style système par défaut)

Effet : Dessine le squelette (connexions pour la tête, les bras, les jambes) et les points clés (positions des articulations) sur l'image.

**6. Afficher l'image et logique de sortie**

.. code-block:: python

   cv2.imshow("Show Video", frame)

   if cv2.waitKey(1) & 0xff == ord('q'):
      break

Afficher chaque image dans la fenêtre ``"Show Video"``.
Quitter la boucle lorsque la touche 'q' est pressée.

**7. Libérer les ressources**

.. code-block:: python

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Arrêter l'aperçu, libérer la caméra, fermer toutes les fenêtres OpenCV.

-----------------------------
6. Présentation du Modèle Pose
-----------------------------

Le module MediaPipe Pose retourne **33 points clés**, couvrant des zones comme la tête, le torse, les bras et les jambes :

.. list-table::
   :header-rows: 1

   * - Partie du Corps
     - Index
   * - Nez
     - 0
   * - Épaule gauche/droite
     - 11 / 12
   * - Coude gauche/droit
     - 13 / 14
   * - Poignet gauche/droit
     - 15 / 16
   * - Hanche gauche/droite
     - 23 / 24
   * - Genou gauche/droit
     - 25 / 26
   * - Cheville gauche/droite
     - 27 / 28
   * - Extrémité du pied gauche/droit
     - 31 / 32

Ces points peuvent être utilisés pour le **jugement de posture**, le **comptage d'actions** (par exemple, squats, pompes, détection de poses de yoga), etc.

-----------------------------
7. Performances et Réglage
-----------------------------

.. list-table::
   :header-rows: 1

   * - Élément
     - Impact
     - Suggestion d'optimisation
   * - Résolution
     - Une résolution plus élevée augmente la précision mais aussi la latence
     - Utilisez 640x480 pour équilibrer performances et vitesse
   * - model_complexity
     - Améliore la précision de reconnaissance mais ralentit le calcul
     - Recommandé 1~2 pour Raspberry Pi
   * - segmentation
     - Augmente la charge GPU/CPU
     - Recommandé de désactiver si le remplacement d'arrière-plan n'est pas nécessaire

------------------------------------------------------------
8. Dépannage
------------------------------------------------------------

- Aucune personne détectée

  Si le programme s'exécute mais qu'aucune personne n'est détectée, assurez-vous que tout le corps est dans le cadre de la caméra. Évitez les forts contre-jours et améliorez les conditions d'éclairage. Maintenez une distance d'environ 1 à 2 mètres de la caméra pour de meilleurs résultats.

- La vidéo est lente ou saccadée

  Si la fréquence d'images est faible, essayez de réduire la résolution à 640x480 ou moins. Définissez ``model_complexity = 1`` pour de meilleures performances. Désactivez la segmentation si elle n'est pas nécessaire, et fermez les autres programmes d'arrière-plan pour libérer des ressources système.

- Erreur de segmentation

  La plupart des erreurs de segmentation sont causées par une incompatibilité entre l'architecture système et la wheel MediaPipe installée.

  Vérifiez l'architecture de votre système :

  .. code-block:: bash

     uname -m

  La sortie doit être ``aarch64``.

  Si vous voyez ``armv7l`` ou ``armhf``, vous utilisez Raspberry Pi OS 32 bits, qui n'est pas compatible avec la wheel officielle de MediaPipe.

  Vous pouvez également vérifier en Python :

  .. code-block:: python

     import platform
     print(platform.machine())

  Le résultat doit également être ``aarch64``.

- Utilisation d'aarch64 mais toujours une erreur de segmentation

  Cela peut se produire si certains noyaux TensorFlow Lite XNNPACK ne sont pas entièrement compatibles avec votre build MediaPipe.

  Solutions possibles :

  - Utilisez ``model_complexity = 1`` (recommandé dans ce tutoriel).
  - Assurez-vous que MediaPipe est installé dans le bon environnement virtuel.
  - Installez une wheel optimisée pour Raspberry Pi comme ``mediapipe-bin`` (version PINTO0309).

- ``model_complexity = 2`` plante mais ``1`` fonctionne

  La complexité 2 charge un modèle plus grand qui peut déclencher des optimisations CPU avancées. Sur Raspberry Pi, certains noyaux TensorFlow Lite optimisés peuvent ne pas être entièrement supportés. La complexité 1 évite ces noyaux et est généralement plus stable et plus rapide sur Raspberry Pi.



-----------------------------
9. Résumé
-----------------------------

- Ce chapitre a implémenté la **détection de squelette humain en temps réel** basée sur MediaPipe Pose ;
- Pose fournit 33 points clés, utilisables dans des domaines comme le fitness, l'analyse de posture, la reconnaissance d'actions ;
- En ajustant la résolution et la complexité du modèle, un fonctionnement fluide peut être atteint sur Raspberry Pi ;
- Sur la base de ces points clés, nous pouvons ensuite développer :

  - La reconnaissance d'actions (par exemple, « lever la main », « s'accroupir »)
  - L'évaluation de posture (par exemple, « La posture assise est-elle correcte ? »)
  - Le contrôle interactif humain.