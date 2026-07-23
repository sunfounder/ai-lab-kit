.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _mp_pose_segmentation:

9. Fond Vert
============================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Ce chapitre utilise la capacité de **segmentation de personne** de
MediaPipe Pose pour implémenter un simple **effet de fond vert**.

En séparant la personne de l'arrière-plan,
nous pouvons remplacer l'arrière-plan original par une couleur verte unie.
Cela permet :

- Les applications d'arrière-plan virtuel
- L'incrustation par chroma key (OBS / NLE)
- Les effets de diffusion en direct
- Le remplacement de scène de type AR

.. image:: img/mp_pose_green.png
   :align: center


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

L'effet de fond vert est implémenté en utilisant les étapes suivantes :

1. Initialiser le modèle Pose avec ``enable_segmentation=True``.
2. Pour chaque image, obtenir ``results.segmentation_mask``.
3. Le masque est une carte de probabilité à un seul canal (plage 0–1).
4. Appliquer un seuil (par exemple, 0,5) pour séparer le premier plan et l'arrière-plan.
5. Remplacer les pixels d'arrière-plan par du vert uni.
6. Optionnellement, appliquer un flou ou un filtrage morphologique pour lisser les bords.

Cette méthode est légère et s'exécute en temps réel sur Raspberry Pi,
tout en fournissant un exemple pratique de segmentation humaine.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation.py

   Si vous souhaitez utiliser MediaPipe Pose avec une vidéo enregistrée, vous pouvez exécuter la commande suivante :

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_pose_segmentation_video.py

#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_9.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Un curseur nommé ``Mask`` apparaît dans la même fenêtre. Il contrôle le seuil de segmentation (0–100), avec la valeur par défaut définie à 50 (0,5).

   Lorsqu'une personne apparaît devant la caméra :

   - MediaPipe Pose génère un ``segmentation_mask`` pour chaque image.
   - Les pixels dont les valeurs du masque sont supérieures au seuil sont traités comme le premier plan (personne).
   - Tous les autres pixels sont remplacés par un fond vert uni (effet de fond vert).

   Au fur et à mesure que vous déplacez le curseur ``Mask`` :

   - Augmenter le seuil ne conserve que la zone de premier plan la plus confiante (moins de fuite d'arrière-plan, mais peut couper certaines parties du corps).
   - Diminuer le seuil inclut plus de pixels comme premier plan (silhouette plus complète, mais peut inclure du bruit d'arrière-plan).

   Si aucun masque de segmentation n'est disponible, le programme affiche simplement le flux normal de la caméra sans remplacement d'arrière-plan.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.

-----------------------------
4. Code Complet
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.pose as mp_pose
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   import numpy as np
   GREEN = (0, 255, 0)  # Green color (BGR)

   # Initialize the Pose model
   pose = mp_pose.Pose(
      static_image_mode=False,  # Set to False for processing video frames
      model_complexity=1,
      enable_segmentation=True,
   )

   # Open the camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )

   picam2.configure(config)
   #picam2.start_preview(Preview.QTGL)
   picam2.start()

   print("Streaming... press 'q' to quit")


   # --- Utility: empty callback for trackbars ---
   def _noop(x):
      pass

   # Create Window
   cv2.namedWindow('Show Video')
   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


   while True:
      frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
      frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame from BGR to RGB (required by MediaPipe)
      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

      # Process the frame for pose detection and tracking
      results = pose.process(frame)

      # Convert the frame back from RGB to BGR (required by OpenCV)
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Cutout the green background
      if results.segmentation_mask is not None:
         # segmentation_mask is a single-channel [H, W] probability map.
         mask = results.segmentation_mask
         # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
         condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

         # Create a green background
         bg = np.full_like(frame, GREEN, dtype=np.uint8)

         # Use mask to keep the character and replace the background with green
         frame = np.where(condition, frame, bg)

      # Display the frame with annotations
      cv2.imshow("Show Video", frame)

      # Exit the loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   # Release the camera
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le script, la personne (premier plan) est conservée, et l'arrière-plan est remplacé par du vert uni.
Il peut être directement utilisé pour l'incrustation ultérieure avec **Chroma Key** dans OBS, Premiere, DaVinci Resolve, etc.

-------------------------------------
5. Explication des Points Clés
-------------------------------------

``segmentation_mask`` est une **image flottante à un seul canal** (plage 0~1) de la même taille que l'image d'entrée :

- Valeur **proche de 1** : Haute probabilité d'être **premier plan (personne)** ;
- Valeur **proche de 0** : Haute probabilité d'être **arrière-plan**.

L'approche habituelle consiste à définir un seuil **T** (par exemple, 0,5) et à créer un masque conditionnel :

.. code-block:: python

   condition = (mask > T)[..., None]

Ici, nous configurons un curseur pour ajuster le seuil en temps réel :

.. code-block:: python

   # Create a trackbar for threshold, default value is 50
   cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)

   while True:

      ...
      # Read the trackbar value
      threshold = cv2.getTrackbarPos('Mask', 'Show Video')

      # Create a condition mask
      condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

Ensuite, nous pouvons utiliser ``np.where(condition, frame, background)`` pour remplacer l'arrière-plan ; ici nous le remplaçons par du vert :

.. code-block:: python

   # Create a green background
   bg = np.full_like(frame, GREEN, dtype=np.uint8)

   # Use mask to keep the character and replace the background with green
   frame = np.where(condition, frame, bg)

----------------------------------------------------
6. Optimisation de l'Effet et des Bords
----------------------------------------------------

La binarisation directe peut provoquer des bords irréguliers ou de petits trous autour des cheveux et des bords des vêtements.
Un **léger post-traitement** peut améliorer les bords :

.. code-block:: python

   # Slight blur (soften edges)
   mask_blur = cv2.GaussianBlur(mask, (5, 5), 0)

   # Re-threshold (smoother foreground boundary)
   condition = (mask_blur > 0.5)[..., None]

   # Or perform morphological closing to fill small holes
   bin_mask = (mask > 0.5).astype(np.uint8) * 255
   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
   bin_mask = cv2.morphologyEx(bin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)
   condition = (bin_mask > 127)[..., None]

.. tip::

   - **Plage de valeur T recommandée 0,3~0,7** : Peut être abaissée dans les environnements sombres/modèles conservateurs ; peut être augmentée avec plus de bruit.
   - Ne rendez pas le noyau de flou trop grand, sinon la limite de la personne « laissera passer le vert ».

----------------------------------------------------
7. Utilisation d'un Arrière-Plan Personnalisé (Image/Vidéo)
----------------------------------------------------

Remplacer le vert uni par une image d'arrière-plan personnalisée :

.. code-block:: python

   bg_img = cv2.imread("background.jpg")
   bg_img = cv2.resize(bg_img, (frame.shape[1], frame.shape[0]))
   frame = np.where(condition, frame, bg_img)

Ou utiliser une autre vidéo comme arrière-plan (lire l'image suivante ``bg_frame``, redimensionner aux mêmes dimensions, puis remplacer).

----------------------------------------------------
8. Équilibre Performances et Qualité
----------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Élément
     - Impact
     - Suggestion
   * - Résolution
     - Une résolution plus élevée donne des bords plus fins mais une vitesse plus lente
     - Commencez par 640×480 ; augmentez si une image plus nette est nécessaire
   * - model_complexity
     - Plus élevé est plus précis mais plus lent
     - Recommandé 1~2 sur Raspberry Pi
   * - Force du post-traitement
     - Trop de flou/morphologie peut « avaler les bords/laisser passer le vert »
     - Petit noyau + peu d'itérations, observez l'effet de bord

------------------------------------------------------------
9. Dépannage
------------------------------------------------------------

- Bords irréguliers ou coutures visibles autour de la personne

  Cela se produit généralement parce que le masque est appliqué avec un seuil dur, ce qui crée des limites nettes.

  Essayez d'ajuster le seuil à l'aide du curseur ``Mask``. Pour des bords plus lisses, appliquez un petit flou au masque de segmentation ou utilisez une simple opération de fermeture morphologique avant la composition.

- Parties manquantes de la personne

  Si des parties du corps sont coupées, l'éclairage peut être trop faible, ou la couleur des vêtements peut se fondre dans l'arrière-plan.

  Améliorez l'éclairage, ajustez le seuil, et essayez d'utiliser un arrière-plan plus simple avec un contraste plus élevé avec le sujet.

- Faible fréquence d'images

  Si la vidéo semble lente, la résolution peut être trop élevée ou le modèle peut être trop complexe.

  Réduisez la résolution de la caméra (par exemple, 640×480 ou 320×240) et maintenez ``model_complexity`` à 1 pour de meilleures performances.

- Le vert déborde sur le sujet

  Si le fond vert apparaît sur le sujet, la limite de segmentation peut être inexacte, ou la couleur du sujet peut causer une confusion visuelle.

  Essayez de passer à une couleur de remplacement différente (bleu ou gris), ou remplacez l'arrière-plan par une image au lieu d'une couleur unie pour un résultat plus naturel.


-----------------------------
10. Résumé
-----------------------------

- En utilisant ``segmentation_mask``, nous pouvons rapidement réaliser le « détourage de personne + remplacement d'arrière-plan » ;
- Obtenez des bords plus naturels grâce à des seuils et un post-traitement léger ;
- Adapté aux arrière-plans virtuels, à l'incrustation pour diffusion en direct, à l'enseignement à distance, etc. ;
- Les prochaines étapes pourraient combiner le **squelette de pose** et la **segmentation** pour des effets plus interactifs (par exemple, remplacer uniquement l'arrière-plan, ne pas remplacer le squelette superposé au premier plan).