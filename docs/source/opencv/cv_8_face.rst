.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

8. Détection de Visages et d'Yeux
=================================================

Dans ce chapitre, nous allons utiliser Picamera2 du Raspberry Pi pour capturer une vidéo et appliquer les classifieurs à caractéristiques Haar d'OpenCV pour la **détection de visages et d'yeux en temps réel**.
Cette approche est légère et très pratique — idéale pour les débutants qui déploient sur un Raspberry Pi.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_8.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

1. Caractéristiques Haar et Principes de Détection
-----------------------------------------

1. Essence des Caractéristiques Haar

Les caractéristiques Haar sont une méthode classique de détection d'objets. Elles encodent des **schémas de différences de luminosité** dans des régions d'image pour déterminer si une région contient probablement un visage, des yeux, etc.

Exemples typiques de caractéristiques Haar :

- Les régions des yeux sont généralement plus sombres que le front au-dessus
- La luminosité est symétrique des deux côtés de l'arête du nez
- La zone sous la bouche montre souvent un schéma de contour net

.. image:: img/opencv_haar_f.png
   :alt: Illustration des caractéristiques Haar
   :align: center

OpenCV nécessite des classifieurs Haar pré-entraînés (fichiers ``.xml``). Ils sont déjà inclus dans le répertoire d'exemple — il suffit de les charger et de les utiliser.

2. Pipeline de Détection

   1. Charger le modèle Haar entraîné avec ``CascadeClassifier``
   2. Convertir la vidéo en temps réel en niveaux de gris (pour améliorer l'efficacité)
   3. Utiliser ``detectMultiScale`` pour détecter les régions de visages/yeux
   4. Dessiner des rectangles autour des cibles détectées

.. image:: img/opencv_haar_show.png
   :alt: Illustration du pipeline de détection
   :align: center


2. Exécuter le Code
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

      cd ~/ai-lab-kit/opencv_python
      python3 cv_8_haarcascade.py

   .. tip::

      Nous fournissons également ``cv_8_haarcascade_video.py`` pour détecter les visages et les yeux à partir d'un fichier vidéo.

#. Lorsque vous exécutez le programme, une fenêtre nommée **Raspberry Pi Camera - Face Detection** apparaît et affiche l'image en direct de la caméra Raspberry Pi.

   Les visages détectés dans le flux vidéo sont mis en évidence avec des **rectangles jaunes**, et chaque visage détecté est étiqueté (Visage 1, Visage 2, ...).
   Dans chaque région de visage détectée, le programme détecte également les yeux et les marque avec des **rectangles orange**.

   La détection fonctionne en temps réel, et les rectangles se déplaceront au fur et à mesure que la personne bouge devant la caméra.

   Pour arrêter le programme :

   * Appuyez sur la touche **q** du clavier
   * Ou fermez la fenêtre d'affichage avec le bouton de fermeture (X)

   Après la sortie, la caméra s'arrête et toutes les fenêtres OpenCV sont fermées.


3. Code Complet
-------------------


.. code-block:: python

   # Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
   import cv2
   from picamera2 import Picamera2
   from pathlib import Path

   # -----------------------------
   # Load Haar cascade classifiers
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent

   face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
   eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   # Check if cascade files are loaded correctly
   if face_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
   if eye_cascade.empty():
      raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   # -----------------------------
   # Initialize Picamera2
   # -----------------------------
   picam2 = Picamera2()

   # Video configuration (resolution can be adjusted)
   config = picam2.create_video_configuration(main={"size": (640, 480)})
   picam2.configure(config)
   picam2.start()

   WIN = "Raspberry Pi Camera - Face Detection"
   print("Camera started. Press 'q' to quit.")

   try:
      while True:
         # Capture a frame (Picamera2 typically provides RGB)
         frame_rgb = picam2.capture_array()

         # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
         gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

         # Improve contrast to make detection more stable under different lighting
         gray = cv2.equalizeHist(gray)

         # Detect faces
         faces = face_cascade.detectMultiScale(
               gray,
               scaleFactor=1.2,
               minNeighbors=5,
               minSize=(60, 60)
         )

         # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
         frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

         # Draw face and eye results
         for i, (x, y, w, h) in enumerate(faces, start=1):
               # Draw face rectangle + label
               cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
               cv2.putText(frame_bgr, f"Visage {i}", (x, max(0, y - 10)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

               # ROI for eye detection (search eyes only inside the detected face area)
               roi_gray = gray[y:y + h, x:x + w]
               roi_color = frame_bgr[y:y + h, x:x + w]

               eyes = eye_cascade.detectMultiScale(
                  roi_gray,
                  scaleFactor=1.2,
                  minNeighbors=8,
                  minSize=(20, 20)
               )

               # Draw up to 2 eyes (typical for a face)
               for (ex, ey, ew, eh) in eyes[:2]:
                  cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

         # Show the frame
         cv2.imshow(WIN, frame_bgr)

         # Handle keyboard input
         key = cv2.waitKey(1) & 0xFF
         if key == ord("q"):
               break

         # Exit if the user closes the window (click X)
         if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
               break

   finally:
      picam2.stop()
      cv2.destroyAllWindows()
      print("Caméra arrêtée.")

4. Explication du Code
----------------------

#. Importer les bibliothèques nécessaires :

   .. code-block:: python

      import cv2
      from picamera2 import Picamera2
      from pathlib import Path

   OpenCV est utilisé pour la détection et le dessin, Picamera2 est utilisé pour capturer les images de la caméra Raspberry Pi.

#. Obtenir le répertoire du script en cours :

   .. code-block:: python

      BASE_DIR = Path(__file__).resolve().parent

   Cela vous permet de charger les fichiers XML de cascade depuis le même dossier que le script Python.

#. Charger les classifieurs en cascade Haar (visage et yeux) :

   .. code-block:: python

      face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
      eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

   Les cascades Haar sont des modèles pré-entraînés capables de détecter les visages et les yeux.

#. Vérifier que les fichiers de cascade sont chargés correctement :

   .. code-block:: python

      if face_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
      if eye_cascade.empty():
          raise FileNotFoundError("Failed to load haarcascade_eye.xml")

   Si le chemin du fichier est incorrect ou si le fichier est manquant, ``CascadeClassifier`` sera vide.
   Ces vérifications vous aident à trouver le problème rapidement.

#. Initialiser la caméra et définir la résolution :

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_video_configuration(main={"size": (640, 480)})
      picam2.configure(config)
      picam2.start()

   Cela démarre la caméra en mode vidéo en 640x480.

#. Capturer des images en continu :

   .. code-block:: python

      frame_rgb = picam2.capture_array()

   Chaque boucle capture une image. Picamera2 renvoie généralement les images au format RGB.

#. Convertir en niveaux de gris (plus rapide pour la détection) :

   .. code-block:: python

      gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

   La détection visage/yeux fonctionne sur des images en niveaux de gris et est plus rapide qu'avec des images couleur.

#. Améliorer le contraste pour une détection plus stable :

   .. code-block:: python

      gray = cv2.equalizeHist(gray)

   L'égalisation d'histogramme peut améliorer les résultats de détection sous différentes conditions d'éclairage.

#. Détecter les visages dans l'image :

   .. code-block:: python

      faces = face_cascade.detectMultiScale(
          gray,
          scaleFactor=1.2,
          minNeighbors=5,
          minSize=(60, 60)
      )

   Cela retourne une liste de rectangles ``(x, y, w, h)`` pour tous les visages détectés.

   - ``scaleFactor`` contrôle le pas d'échelle de l'image (plus petit = plus précis mais plus lent).
   - ``minNeighbors`` réduit les faux positifs (plus élevé = plus strict).
   - ``minSize`` ignore les très petites détections.

#. Convertir RGB en BGR pour le dessin et l'affichage :

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

   Les fonctions de dessin d'OpenCV et ``imshow`` attendent du BGR pour les images couleur.

#. Dessiner les rectangles et étiquettes des visages :

   .. code-block:: python

      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
      cv2.putText(frame_bgr, f"Visage {i}", (x, max(0, y - 10)),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

   Cela dessine une boîte autour de chaque visage détecté et ajoute une étiquette comme « Visage 1 ».

#. Détecter les yeux à l'intérieur de chaque visage (ROI) :

   .. code-block:: python

      roi_gray = gray[y:y + h, x:x + w]
      roi_color = frame_bgr[y:y + h, x:x + w]

      eyes = eye_cascade.detectMultiScale(
          roi_gray,
          scaleFactor=1.2,
          minNeighbors=8,
          minSize=(20, 20)
      )

   ROI signifie « Région d'Intérêt ». Détecter les yeux uniquement dans la zone du visage est plus rapide et réduit les fausses détections.

#. Dessiner jusqu'à deux yeux :

   .. code-block:: python

      for (ex, ey, ew, eh) in eyes[:2]:
          cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

   Cela dessine des rectangles autour des deux premiers yeux détectés.

#. Afficher le résultat et gérer la sortie :

   .. code-block:: python

      cv2.imshow(WIN, frame_bgr)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
          break

   Appuyez sur ``q`` pour quitter, ou fermez la fenêtre pour sortir en toute sécurité.

#. Nettoyage (toujours exécuté) :

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   La caméra est arrêtée et toutes les fenêtres OpenCV sont fermées même si une erreur se produit.


5. Avantages et Inconvénients de la Détection Haar
--------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Avantages
     - Inconvénients
   * - Vitesse
     - Très rapide ; adapté au Raspberry Pi
     - -
   * - Précision
     - Fonctionne bien pour les visages de face
     - Sensible à la rotation et aux profils
   * - Éclairage
     - Bon sous un éclairage uniforme
     - Les performances chutent si trop lumineux/sombre
   * - Modèle
     - Taille de modèle petite ; facile à déployer
     - Moins précis que les méthodes d'apprentissage profond

Parce qu'elle est légère et rapide, la détection Haar reste très pratique sur les appareils embarqués.


6. Améliorations Courantes
----------------------

1. **Prétraitement de l'éclairage** : Appliquez l'égalisation d'histogramme ou CLAHE avant la détection pour améliorer les performances en faible luminosité.
2. **Détection multi-angle** : Chargez les classifieurs de visage de face et de profil pour détecter plus de poses.
3. **Plus de caractéristiques faciales** : Ajoutez des classifieurs Haar pour les yeux/bouche/nez pour enrichir la détection.
4. **Utiliser DNN au lieu de Haar** : OpenCV DNN + ResNet/MobileNet peut offrir une précision plus élevée (mais nécessite plus de calcul).



7. Exercices Avancés
---------------------

- Utilisez ``cv2.equalizeHist`` sur l'image en niveaux de gris pour améliorer la détection en faible luminosité.
- Ajoutez des classifieurs Haar pour la bouche ou le nez pour détecter plus de caractéristiques faciales.
- Enregistrez le processus de détection avec ``cv2.VideoWriter``.
- Combinez avec une sortie GPIO pour réaliser un projet Raspberry Pi : « allumer une LED lorsqu'un visage est détecté ».