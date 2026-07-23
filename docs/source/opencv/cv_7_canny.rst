.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

7. Détection de Contours avec Canny
=================================================

Dans ce chapitre, nous allons capturer une vidéo en temps réel avec Raspberry Pi + Picamera2 et effectuer une détection de contours avec l’**algorithme Canny** d’OpenCV.
La détection de contours est une partie fondamentale de la vision par ordinateur, et l’algorithme Canny est largement considéré comme l’une des méthodes les plus stables et robustes au bruit.

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_7.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

1. Que fait l’Algorithme Canny ?
--------------------------------------------------

Dans les images, les **contours** correspondent généralement aux endroits où l’intensité (niveaux de gris) change fortement, comme :

- Les contours d’objets
- Les limites entre les régions claires et sombres
- Les lignes structurelles

Le but de la détection de contours Canny est de :

- **Extraire précisément les informations de contour** tout en réduisant les interférences inutiles ;
- Fournir une base fiable pour la **détection de contours**, la **segmentation d’objets** et la **reconnaissance géométrique** (par exemple, cercles, rectangles) ;
- En vision robotique, il est souvent utilisé pour la **détection de chemin** et la **reconnaissance d’obstacles**.

.. image:: img/opencv_canny.png
   :alt: Illustration de la détection de contours Canny
   :align: center


2. Exécuter le Code
------------------------

.. important::

   Avant de commencer, assurez-vous :

   * Que le support motorisé est assemblé
   * Que vous pouvez accéder au bureau du Raspberry Pi
   * Que le package de code est installé
   * Que Fusion HAT+ est installé et configuré
   * Qu’OpenCV est installé

   Pour les instructions détaillées, voir :ref:`opencv_install`.

#. Ouvrez le terminal et entrez la commande suivante :

   .. code-block:: bash

      cd ~/ai-lab-kit/opencv_python
      python3 cv_7_canny.py

   .. tip::

      Nous fournissons également ``cv_7_canny_video.py`` pour traiter des fichiers vidéo, et ``cv_7_canny_conbine.py`` pour combiner la capture en temps réel avec la vidéo (vue combinée).

#. Lorsque vous exécutez le programme, deux fenêtres OpenCV apparaîtront :

   * **Camera** – affiche l’image en direct de la caméra
   * **Canny Edges** – affiche les contours détectés en temps réel

   Vous pouvez ajuster les seuils de détection de contours à l’aide des curseurs.
   Appuyez sur **q** ou fermez une fenêtre pour quitter le programme.

3. Complete Code
---------------------------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2

   # Empty callback function for trackbars (required by OpenCV API)
   def _noop(x):
      pass

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()

   # Create a preview configuration:
   # size: resolution of the camera image
   # format: XRGB8888 (4-channel image, similar to BGRA)
   picam2.configure(
      picam2.create_preview_configuration(
         main={"size": (640, 480), "format": "XRGB8888"}
      )
   )

   # Start the camera
   picam2.start()

   # -----------------------------
   # Create OpenCV windows
   # -----------------------------
   WIN_CAM = "Camera"        # window for original image
   WIN_EDGE = "Canny Edges"  # window for edge detection result

   cv2.namedWindow(WIN_CAM)
   cv2.namedWindow(WIN_EDGE)

   # -----------------------------
   # Create trackbars to tune Canny thresholds
   # -----------------------------
   # low_th: lower threshold for Canny
   # high_th: higher threshold for Canny
   cv2.createTrackbar("low_th",  WIN_EDGE, 50, 255, _noop)
   cv2.createTrackbar("high_th", WIN_EDGE, 150, 255, _noop)

   print("Press 'q' to exit")

   # -----------------------------
   # Main loop
   # -----------------------------
   while True:
      # Capture one frame from the camera (BGRA format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for OpenCV processing
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert the frame to grayscale
      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

      # Apply Gaussian blur to reduce noise
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

      # Read current threshold values from trackbars
      low_th = cv2.getTrackbarPos("low_th", WIN_EDGE)
      high_th = cv2.getTrackbarPos("high_th", WIN_EDGE)

      # Ensure high_th is always larger than low_th
      if high_th <= low_th:
         high_th = low_th + 1
         cv2.setTrackbarPos("high_th", WIN_EDGE, high_th)

      # Perform Canny edge detection
      edges = cv2.Canny(blurred, low_th, high_th)

      # Show original camera image
      cv2.imshow(WIN_CAM, frame_bgr)

      # Show edge detection result
      cv2.imshow(WIN_EDGE, edges)

      # Process GUI events and keyboard input
      key = cv2.waitKey(1) & 0xFF

      # Press 'q' to exit the program
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
         break

   # -----------------------------
   # Cleanup
   # -----------------------------
   picam2.stop()             # Stop the camera
   cv2.destroyAllWindows()   # Close all OpenCV windows

4. Explication du Code
---------------------------------
#. Définir une fonction de rappel pour les curseurs :

   .. code-block:: python

      def _noop(x):
          pass

   Les curseurs OpenCV nécessitent une fonction de rappel.
   Nous n’avons rien à faire à l’intérieur, donc une fonction vide suffit.

#. Initialiser Picamera2 et définir le format d’aperçu :

   .. code-block:: python

      picam2 = Picamera2()
      picam2.configure(
          picam2.create_preview_configuration(
              main={“size”: (640, 480), “format”: “XRGB8888”}
          )
      )
      picam2.start()

   Cela démarre la caméra Raspberry Pi en 640x480.
   ``XRGB8888`` est un format 4 canaux, donc les images sont de type BGRA.

#. Créer deux fenêtres OpenCV :

   .. code-block:: python

      WIN_CAM = “Camera”
      WIN_EDGE = “Canny Edges”

      cv2.namedWindow(WIN_CAM)
      cv2.namedWindow(WIN_EDGE)

   Une fenêtre montre l’image originale de la caméra, et l’autre montre le résultat des contours Canny.

#. Créer des curseurs pour ajuster les seuils Canny en temps réel :

   .. code-block:: python

      cv2.createTrackbar(“low_th”,  WIN_EDGE, 50, 255, _noop)
      cv2.createTrackbar(“high_th”, WIN_EDGE, 150, 255, _noop)

   - ``low_th`` : seuil inférieur pour Canny.
   - ``high_th`` : seuil supérieur pour Canny.

   Vous pouvez faire glisser ces curseurs pour modifier la sensibilité de la détection de contours.

#. Capturer une image et la convertir pour le traitement OpenCV :

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   La sortie de la caméra est 4 canaux, nous la convertissons donc en BGR standard à 3 canaux.

#. Convertir en niveaux de gris et flouter l’image :

   .. code-block:: python

      gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
      blurred = cv2.GaussianBlur(gray, (5, 5), 0)

   - Canny fonctionne sur des images en niveaux de gris.
   - Le flou gaussien réduit le bruit, ce qui aide à éviter de détecter trop de faux contours.

#. Lire les valeurs des curseurs et les maintenir valides :

   .. code-block:: python

      low_th = cv2.getTrackbarPos(“low_th”, WIN_EDGE)
      high_th = cv2.getTrackbarPos(“high_th”, WIN_EDGE)

      if high_th <= low_th:
          high_th = low_th + 1
          cv2.setTrackbarPos(“high_th”, WIN_EDGE, high_th)

   Canny s’attend à ce que ``high_th`` soit plus grand que ``low_th``.
   Ce bloc corrige automatiquement les valeurs si l’utilisateur les rapproche trop.

#. Exécuter la détection de contours Canny :

   .. code-block:: python

      edges = cv2.Canny(blurred, low_th, high_th)

   Canny met en évidence les contours forts dans l’image.
   Des seuils plus bas détectent généralement plus de contours, mais aussi plus de bruit.

#. Afficher les deux fenêtres :

   .. code-block:: python

      cv2.imshow(WIN_CAM, frame_bgr)
      cv2.imshow(WIN_EDGE, edges)

   La fenêtre de gauche montre le flux en direct de la caméra, et l’autre montre les contours détectés.

#. Conditions de sortie (appuyer sur ``q`` ou fermer la fenêtre) :

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord(“q”):
          break

      if (cv2.getWindowProperty(WIN_CAM, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_EDGE, cv2.WND_PROP_VISIBLE) < 1):
          break

   Cela permet aux débutants d’arrêter le programme de deux manières : le clavier ou la fermeture de la fenêtre.

#. Nettoyage :

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Arrêtez toujours la caméra et fermez toutes les fenêtres OpenCV pour libérer les ressources.

5. Pourquoi Canny est-il Utile ?
--------------------------

La sortie de Canny est bien adaptée aux tâches de vision ultérieures :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Application
     - Description
   * - Détection de contours
     - Utilisez ``cv2.findContours`` sur la sortie Canny pour obtenir les formes des objets
   * - Segmentation d’objets
     - Utilisez les contours comme base pour séparer la cible de l’arrière-plan
   * - Reconnaissance de formes
     - Combinez avec les transformées de Hough pour détecter des cercles, des lignes, etc.
   * - Navigation robotique
     - Détection du sol, des routes, des contours d’obstacles pour aider à la planification
   * - OCR / Localisation de cibles
     - Les régions de texte, les QR codes, les marqueurs ont souvent des caractéristiques de contour nettes

Canny n’est pas seulement « esthétique » — c’est le **point d’entrée** vers un pipeline de vision plus large.


6. Conseils de Sélection des Seuils
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 70 30 30 70

   * - Scénario
     - low_th
     - high_th
     - Remarques
   * - Éclairage intérieur stable
     - 50
     - 150
     - Cas général, résultats stables
   * - Lumière forte et contraste élevé
     - 100
     - 200
     - Augmentez les seuils pour réduire les faux contours
   * - Faible luminosité, bruité
     - 30
     - 100
     - Abaissez les seuils pour conserver plus de détails
   * - Contours très flous
     - 20
     - 80
     - Abaissez encore les seuils pour rendre les contours plus sensibles

Utilisez les curseurs pour trouver rapidement une plage appropriée, puis intégrez-la en dur dans votre programme.


7. Exercices Avancés
---------------------

- Utilisez ``cv2.findContours`` sur la sortie Canny pour dessiner les limites des objets.
- Modifiez la taille du noyau gaussien et observez comment la précision des contours change.
- Essayez différents seuils sous une lumière faible/forte pour comprendre les effets du double seuillage.
- Utilisez la carte de contours pour la détection de formes avec ``cv2.HoughLines`` (lignes) ou ``cv2.HoughCircles`` (cercles).
