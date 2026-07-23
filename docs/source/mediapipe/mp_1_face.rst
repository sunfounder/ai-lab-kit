.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face:

1. Détection Faciale
===============================

Cette section présente comment utiliser le module **MediaPipe Face Mesh** sur un **Raspberry Pi** pour la détection faciale en temps réel et le dessin du maillage de points de repère faciaux.

.. image:: img/mp_face_mesh_demo.png
   :width: 500
   :align: center

MediaPipe est un framework de pipeline d'apprentissage machine multiplateforme développé par Google, supportant le traitement en temps réel de flux vidéo et d'images. Le module Face Mesh est un modèle fourni par MediaPipe pour la détection faciale en temps réel et le suivi des points de repère, qui peut être utilisé pour construire diverses applications de reconnaissance et d'interaction faciales.

Comparé à la détection Haar d'OpenCV, MediaPipe utilise un modèle d'apprentissage profond pour la détection, offrant :

- Une précision plus élevée
- Une meilleure robustesse face à l'éclairage et aux angles
- Le support du suivi des points de repère faciaux (468 points)
- Une intégration transparente avec OpenCV, permettant de dessiner directement les résultats de détection sur les flux vidéo.

------------------------
1. Exécuter le Code
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face.py

#. Après avoir exécuté le script, OpenCV ouvre une fenêtre intitulée « Show Video » et affiche le flux vidéo en direct capturé par la caméra Raspberry Pi.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/media_1.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   * Si un visage apparaît devant la caméra, le programme le détecte et dessine un maillage détaillé des points de repère faciaux sur le visage en temps réel. Le maillage suit les mouvements du visage en douceur lorsque la personne bouge, cligne des yeux ou change d'expression.
   * Si aucun visage n'est détecté, la fenêtre continue d'afficher le flux normal de la caméra sans points de repère.

   Le flux vidéo continue de fonctionner jusqu'à ce que l'utilisateur quitte le programme.
   Pour quitter le programme, appuyez sur q au clavier.
   La caméra s'arrête et toutes les ressources OpenCV sont libérées automatiquement.

------------------------
2. Code d'Exemple
------------------------

Le code complet est présenté ci-dessous :

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize the mp_face_mesh model
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,          # Set to False for video streams
       max_num_faces=1,                  # Maximum number of faces to detect
       refine_landmarks=True,           # Whether to refine landmarks
       min_detection_confidence=0.5     # Detection confidence threshold
   )

   # Open Raspberry Pi camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()               # XRGB8888 → BGRA
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert BGR to RGB (MediaPipe requires RGB)
       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

       # Face detection and landmark tracking
       results = face.process(frame)

       # Convert RGB back to BGR (for OpenCV display)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       # Draw detected facial landmarks
       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le programme, vous verrez le flux en direct de la caméra, et un maillage facial sera automatiquement dessiné lorsqu'un visage est détecté.

-----------------------------
3. Explication des Étapes Clés
-----------------------------

#. Importer les bibliothèques

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import mediapipe.python.solutions.face_mesh as mp_face_mesh
      import mediapipe.python.solutions.drawing_utils as drawing
      import mediapipe.python.solutions.drawing_styles as drawing_styles

   Ces bibliothèques sont utilisées pour :

   - Contrôler la caméra Raspberry Pi
   - Traiter et afficher les images
   - Détecter les points de repère faciaux

#. Initialiser FaceMesh

   .. code-block:: python

      face = mp_face_mesh.FaceMesh(
          static_image_mode=False,
          max_num_faces=1,
          refine_landmarks=True,
          min_detection_confidence=0.5
      )

   Cela crée le modèle de détection faciale.
   Il suit un visage en continu en mode vidéo.

#. Démarrer la caméra

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"},
      )
      picam2.configure(config)
      picam2.start()

   La caméra commence à diffuser en résolution 640x480.

#. Capturer des images dans une boucle

   .. code-block:: python

      while True:
          frame_bgra = picam2.capture_array()
          frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Chaque boucle capture une image et convertit le format pour OpenCV.

#. Détecter les points de repère faciaux

   .. code-block:: python

      frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
      results = face.process(frame)

   L'image est convertie en RGB.
   MediaPipe analyse l'image et détecte les points de repère faciaux.

#. Dessiner le maillage facial

   .. code-block:: python

      if results.multi_face_landmarks:
          drawing.draw_landmarks(
              image=frame,
              landmark_list=results.multi_face_landmarks[0],
              connections=mp_face_mesh.FACEMESH_TESSELATION
          )

   Si un visage est détecté, un maillage est dessiné dessus.

#. Afficher le résultat et quitter

   .. code-block:: python

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
          break

   Appuyez sur ``q`` pour arrêter le programme.
   La caméra se ferme automatiquement.

---------------------------------------------
4. Problèmes Courants et Dépannage
---------------------------------------------

* La caméra ne s'ouvre pas

  * Assurez-vous que le câble de la caméra CSI est inséré correctement
  * Activez l'interface de la caméra :

    ``sudo raspi-config`` → Interface Options → Camera

  * Redémarrez le Raspberry Pi après l'activation

* Le programme démarre lentement

  La première exécution charge le modèle MediaPipe, ce qui peut prendre quelques secondes.
  C'est normal. Les exécutions suivantes seront plus rapides.

* Détection instable / À la traîne

  * Réduisez la résolution de la caméra (par exemple, 320x240)
  * Désactivez ``refine_landmarks`` pour réduire l'utilisation du CPU
  * Fermez les autres programmes en cours d'exécution

* Aucun module nommé ``mediapipe``

  Installez MediaPipe :

  .. code-block:: bash

     pip install mediapipe

  Assurez-vous d'utiliser un système Raspberry Pi OS 64 bits.

-----------------------------
5. Résumé
-----------------------------

- MediaPipe FaceMesh utilise un modèle d'apprentissage profond pour réaliser une détection faciale de haute précision sur Raspberry Pi
- S'intègre très étroitement avec OpenCV
- Convient pour des scénarios comme la reconnaissance d'expressions, le suivi d'avatar, les applications AR
- Plus robuste et plus facile à étendre que les caractéristiques Haar traditionnelles

La section suivante présentera **comment utiliser les points de repère Face Mesh** pour une analyse et une interaction simples des caractéristiques faciales.