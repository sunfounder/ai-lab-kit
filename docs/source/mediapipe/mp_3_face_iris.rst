.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_iris:

3. Contours Faciaux et Détection de l'Iris
=====================================================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans les sections précédentes, nous avons implémenté la détection de base du maillage facial
et une reconnaissance simple des émotions.

Cette section se concentre sur les méthodes de connexion de caractéristiques détaillées
fournies par MediaPipe FaceMesh :

- ``FACEMESH_CONTOURS`` — Dessine les lignes de contour du visage
  (bords du visage et limites extérieures des caractéristiques)

- ``FACEMESH_IRISES`` — Dessine les régions de l'iris des deux yeux

En dessinant uniquement les contours et les régions de l'iris, la visualisation devient
plus propre et plus légère. Ceci est utile pour :

- L'extraction de caractéristiques faciales
- Le suivi oculaire
- Le suivi de la pupille
- L'interaction par le regard

.. image:: img/mp_face_iris.png
   :align: center

------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme effectue les étapes suivantes :

1. Initialiser le modèle MediaPipe FaceMesh.
2. Capturer des images vidéo de la caméra Raspberry Pi.
3. Convertir l'image au format RGB (requis par MediaPipe).
4. Dessiner les lignes de contour du visage en utilisant ``FACEMESH_CONTOURS``.
5. Dessiner les points de repère de l'iris en utilisant ``FACEMESH_IRISES``.
6. Afficher uniquement les zones clés pour une visualisation plus claire.

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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_face_iris.py

#. Après avoir exécuté le programme, une fenêtre vidéo intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_3.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Lorsqu'un visage apparaît devant la caméra :

   - MediaPipe détecte les points de repère faciaux en temps réel.
   - Seules les lignes de contour du visage sont dessinées (contour du visage, sourcils, lèvres, etc.).
   - Les régions de l'iris des deux yeux sont mises en évidence avec des connexions circulaires de points de repère.

   Contrairement au maillage facial complet, l'écran montre uniquement les contours clés et les caractéristiques de l'iris, rendant la visualisation plus propre et moins encombrée.

   Au fur et à mesure que l'utilisateur bouge la tête ou les yeux :

   - Les lignes de contour suivent le visage en douceur.
   - Les points de repère de l'iris suivent le mouvement des yeux en temps réel.

   Si aucun visage n'est détecté, la fenêtre continue d'afficher le flux normal de la caméra sans annotations.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.

-----------------------------
4. Code Complet
-----------------------------

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2
   import mediapipe.python.solutions.face_mesh as mp_face_mesh
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles

   # Initialize FaceMesh model
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
   # picam2.start_preview(Preview.QTGL) # Enable if hardware preview is needed
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
            # Draw facial contours
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_CONTOURS,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            # Draw iris features
            drawing.draw_landmarks(
                  image=frame,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )

      cv2.imshow("Show Video", frame)
      if cv2.waitKey(1) & 0xff == ord('q'):
         break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le programme, seuls les contours faciaux et les régions de l'iris des deux yeux seront affichés à l'écran.

-----------------------------
5. Explication des Étapes Clés
-----------------------------

Le code de cette section est presque identique à
:ref:`mp_face`.

La principale différence réside dans la méthode de dessin utilisée
à l'intérieur de la boucle principale. La fonction ``draw_landmarks()``
est appelée deux fois :

- Une fois avec ``FACEMESH_CONTOURS``
- Une fois avec ``FACEMESH_IRISES``

Vous pouvez commenter l'un ou l'autre bloc de dessin
pour observer la différence dans l'effet visuel.

------------------------------------------------------------

``FACEMESH_CONTOURS``

- Un ensemble de connexions fourni par MediaPipe.
- Dessine principalement :

  - Le contour facial extérieur
  - Les bords des yeux
  - Le contour du nez
  - Les contours des lèvres

Cette méthode produit une visualisation simplifiée,
facilitant l'observation des changements de contour du visage.

------------------------------------------------------------

``FACEMESH_IRISES``

- Dessine les régions de l'iris des deux yeux.
- Inclut les points clés de l'iris et les lignes de connexion circulaires.
- Utile pour :

  - Le suivi oculaire
  - Le suivi de la pupille
  - La détection du regard

------------------------------------------------------------

``landmark_drawing_spec=None``

- Désactive le dessin des points de repère individuels.
- Seules les lignes de connexion sont affichées,
  ce qui donne un effet visuel plus propre.

Si vous souhaitez afficher à la fois les points et les lignes,
définissez un ``DrawingSpec`` personnalisé.

------------------------------------------------------------

``drawing_styles.get_default_face_mesh_contours_style()``

- Retourne le style de dessin de contour par défaut.

``drawing_styles.get_default_face_mesh_iris_connections_style()``

- Retourne le style de ligne de connexion de l'iris par défaut.


------------------------------------------------------------
6. Dépannage
------------------------------------------------------------

- Iris non détecté

  Si l'iris n'est pas détecté, l'éclairage peut être insuffisant,
  le visage peut être trop loin de la caméra,
  ou ``refine_landmarks`` peut ne pas être activé.

  Améliorez l'éclairage, rapprochez-vous de la caméra,
  et assurez-vous que ``refine_landmarks=True`` est défini
  lors de l'initialisation de FaceMesh.

- Lignes de contour instables

  Si les lignes de contour semblent instables,
  la confiance de détection peut être trop faible,
  ou l'éclairage et les mouvements de tête peuvent affecter le suivi.

  Essayez d'augmenter ``min_detection_confidence``,
  d'améliorer l'éclairage et de garder les mouvements de tête plus lents et plus doux.

- Latence élevée

  Si la réponse vidéo semble lente,
  la résolution peut être trop élevée
  ou ``refine_landmarks`` peut consommer des ressources supplémentaires.

  Réduisez la résolution (par exemple, 320x240),
  ou désactivez ``refine_landmarks`` si la détection de l'iris n'est pas nécessaire.

-----------------------------
7. Résumé
-----------------------------

- ``FACEMESH_CONTOURS`` et ``FACEMESH_IRISES`` sont deux méthodes de connexion importantes fournies par MediaPipe.
- Comparés au dessin de maillage complet, ils sont plus légers et plus intuitifs, adaptés aux scénarios d'interaction pratiques.
- Le prochain chapitre présentera comment utiliser ces fonctionnalités pour le suivi du regard et la détection de clignement.