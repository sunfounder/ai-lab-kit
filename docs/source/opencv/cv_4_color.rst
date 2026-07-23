.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


4. Détection de Couleur
=============================================

La détection de couleur est l'une des fonctions les plus fondamentales et pratiques en vision par ordinateur.
Dans ce chapitre, nous allons utiliser un code pas à pas et des explications pour **détecter les objets rouges à l'aide de l'espace colorimétrique HSV** et **dessiner des boîtes englobantes** autour d'eux.

Cela constitue la base pour des techniques de suivi d'objets plus avancées (comme CAMShift).

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_4.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

1. Objectif et Approche
--------------------------------------------

- Utiliser **Picamera2** pour capturer des images de la caméra en temps réel
- Convertir l'image de BGR vers l'espace colorimétrique HSV
- Utiliser ``cv2.inRange`` pour extraire les régions rouges
- Utiliser le filtrage morphologique pour supprimer le bruit
- Utiliser ``cv2.findContours`` pour trouver les contours des objets rouges
- Dessiner des boîtes englobantes autour des régions rouges détectées

.. image:: img/color_detection.png
   :alt: Illustration de la détection de couleur
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
      python3 cv_4_color.py

#. Lorsque vous exécutez le programme, deux fenêtres OpenCV apparaîtront à l'écran :

   * **Red Detection** – montre l'image en direct de la caméra avec des boîtes vertes autour des objets rouges détectés
   * **Red Mask** – montre l'image du masque binaire utilisé pour la détection de la couleur rouge

   Le programme capture en continu les images de la caméra Raspberry Pi et détecte les régions rouges en temps réel.
   Si un objet rouge est détecté, un rectangle vert et la valeur de la zone seront affichés sur l'image couleur.

   Vous pouvez quitter le programme de deux manières :

   * Appuyer sur la touche **q** du clavier
   * Fermer l'une des fenêtres OpenCV en cliquant sur le bouton de fermeture (X)

   Après la sortie, la caméra arrête la diffusion et toutes les fenêtres OpenCV sont fermées.

3. Code Complet
--------------

.. code-block:: python

   from picamera2 import Picamera2
   import cv2
   import numpy as np
   import time

   # -----------------------------
   # Camera setup
   # -----------------------------
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}  # 4-channel format (BGRA-like)
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   # -----------------------------
   # Red color range in HSV
   # (Red wraps around 0/180 in HSV, so we use two ranges)
   # -----------------------------
   LOWER_RED1 = np.array([0,   100, 80], dtype=np.uint8)
   UPPER_RED1 = np.array([10,  255, 255], dtype=np.uint8)
   LOWER_RED2 = np.array([170, 100, 80], dtype=np.uint8)
   UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

   # Morphology settings
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
   MIN_AREA = 800  # ignore small blobs

   # Window names
   WIN_RESULT = "Red Detection"
   WIN_MASK = "Red Mask"

   # Optional: limit FPS to reduce CPU usage (set to None to disable)
   TARGET_FPS = 30
   FRAME_INTERVAL = 1.0 / TARGET_FPS if TARGET_FPS else 0

   while True:
      loop_start = time.perf_counter()

      # Capture one frame (BGRA-like) and convert to BGR for OpenCV processing
      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGR to HSV
      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

      # Create red mask using two HSV ranges
      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

      # Morphological operations: remove noise + fill holes
      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

      # Find contours in the mask
      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      # Draw bounding boxes for valid red regions
      for cnt in contours:
         area = cv2.contourArea(cnt)
         if area < MIN_AREA:
               continue

         x, y, w, h = cv2.boundingRect(cnt)
         cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
         cv2.putText(
               frame_bgr,
               f"red area={int(area)}",
               (x, max(0, y - 6)),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5,
               (0, 255, 0),
               1,
               cv2.LINE_AA
         )

      # Show both windows
      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

      # Process GUI events + keyboard input
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any window (click X)
      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
         break

   # Cleanup
   picam2.stop()
   cv2.destroyAllWindows()


4. Explication du Code
--------------------------------

#. Initialiser Picamera2 et démarrer la diffusion :

   .. code-block:: python

      picam2 = Picamera2()
      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )
      picam2.configure(config)
      picam2.start()

   Cela configure la caméra en 640x480 et démarre le flux d'aperçu.
   ``XRGB8888`` est un format 4 canaux, donc les images capturées sont de type BGRA.

#. Convertir l'image capturée dans un format couramment utilisé par OpenCV :

   .. code-block:: python

      frame_bgra = picam2.capture_array()
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

   Picamera2 renvoie ici une image 4 canaux, nous la convertissons donc en BGR standard à 3 canaux pour le traitement.

#. Utiliser l'espace colorimétrique HSV pour une détection de couleur robuste :

   .. code-block:: python

      hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

   HSV sépare la couleur (Teinte) de la luminosité, ce qui rend la détection de couleur plus stable sous différents éclairages.

#. Définir deux plages HSV pour le rouge :

   .. code-block:: python

      mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
      mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
      mask = cv2.bitwise_or(mask1, mask2)

   Le rouge « s'enroule » autour de l'échelle de Teinte dans HSV OpenCV (près de 0 et près de 180), donc deux plages sont combinées pour couvrir tous les rouges.

#. Nettoyer le masque avec la morphologie (réduire le bruit et remplir les trous) :

   .. code-block:: python

      mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
      mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

   - **OPEN** supprime les petits points de bruit.
   - **CLOSE** remplit les petits trous à l'intérieur des régions rouges détectées.

#. Trouver les régions rouges et filtrer les petites taches :

   .. code-block:: python

      contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < MIN_AREA:
              continue

   Les contours sont détectés à partir du masque binaire.
   ``MIN_AREA`` ignore les petites régions rouges pour réduire les fausses détections.

#. Dessiner les boîtes englobantes et les étiquettes sur l'image de résultat :

   .. code-block:: python

      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame_bgr, f"red area={int(area)}", ...)

   Cela montre où OpenCV a trouvé des objets rouges, et affiche la zone de la tache détectée pour référence.

#. Afficher à la fois le résultat et le masque :

   .. code-block:: python

      cv2.imshow(WIN_RESULT, frame_bgr)
      cv2.imshow(WIN_MASK, mask)

   La **fenêtre de résultat** montre la vue de la caméra avec les boîtes, et la **fenêtre de masque** montre l'image binaire rouge uniquement.

#. Conditions de sortie (clavier + fermeture de fenêtre) :

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WIN_RESULT, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WIN_MASK, cv2.WND_PROP_VISIBLE) < 1):
          break

   Appuyez sur ``q`` pour quitter, ou fermez l'une des fenêtres pour sortir en toute sécurité.

#. Nettoyage :

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Arrêtez toujours la caméra et fermez les fenêtres OpenCV pour libérer les ressources.


5. Conseils de Réglage des Paramètres
-----------------------------

- ``LOWER_RED1 / UPPER_RED1`` : ajustez cette plage pour détecter d'autres couleurs.
  Par exemple, vert ≈ ``[35, 50, 50]`` à ``[85, 255, 255]``.

- ``KERNEL`` : des noyaux plus grands donnent un filtrage plus fort mais peuvent supprimer les petits objets.

- ``MIN_AREA`` : augmenter cette valeur filtre les petits contours bruyants ; la diminuer rend la détection plus sensible.

.. note::
   Vous pouvez commencer par n'afficher que le ``mask`` et ajuster les seuils jusqu'à ce que la région cible soit claire, puis poursuivre avec le reste du pipeline.




6. Extensions et Exercices
--------------------------

- Modifiez le seuil HSV pour détecter d'autres couleurs (par exemple, bleu ou vert).
- Expérimentez avec différents paramètres morphologiques dans des arrière-plans plus complexes.