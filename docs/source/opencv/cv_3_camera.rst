.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Capture d'Écran en Temps Réel avec la Caméra
================================================================

Dans les chapitres précédents, nous avons appris à lire et à lire des fichiers vidéo locaux.
Dans ce chapitre, nous allons aller plus loin en utilisant la **caméra Raspberry Pi** pour la capture vidéo en temps réel et en appliquant la **conversion d'espace colorimétrique** avec OpenCV.


1. Objectifs du Projet
-----------------------

.. raw:: html

      <video width="700" loop muted controls>
          <source src="../_static/video/Opencv_3.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

- Utiliser **Picamera2** pour capturer des images de la caméra en temps réel
- Convertir la sortie de la caméra du format BGRA au format BGR
- Utiliser OpenCV pour l'aperçu en temps réel
- Comprendre les caractéristiques et les cas d'utilisation de différents espaces colorimétriques

.. image:: img/opencv_camera.png
   :alt: Illustration de l'aperçu en temps réel de la caméra
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
      python3 cv_3_camera.py

#. Lorsque vous exécutez le programme, deux fenêtres OpenCV apparaîtront :

   * **BGR Frame** – montre l'image couleur en direct de la caméra
   * **GRAY Frame** – montre la version en niveaux de gris de la même image

   Vous pouvez quitter le programme de deux manières :

   * Appuyer sur la touche **q** du clavier
   * Fermer l'une des fenêtres en cliquant sur le bouton de fermeture (X)

   Après la sortie, la caméra arrête la diffusion et toutes les fenêtres OpenCV sont fermées.

3. Code d'Exemple
----------------

Voici l'exemple Python complet pour ce chapitre (``cv_3_camera.py``) :

.. code-block:: python

   # Import Picamera2 for Raspberry Pi Camera
   from picamera2 import Picamera2
   import cv2
   import time

   # Create a Picamera2 object
   picam2 = Picamera2()

   # Create a camera configuration
   # XRGB8888 is a 4-channel format (similar to BGRA)
   # size sets the resolution of the camera frame
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"}
   )

   # Apply the configuration to the camera
   picam2.configure(config)

   # Start the camera
   picam2.start()

   print("Streaming... press 'q' to quit")

   # Window names
   WINDOW_BGR = "BGR Frame"
   WINDOW_GRAY = "GRAY Frame"

   while True:
      # Capture one frame as a NumPy array (BGRA-like format)
      frame_bgra = picam2.capture_array()

      # Convert BGRA to BGR for normal color display
      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

      # Convert BGRA directly to grayscale
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

      # Display the color and grayscale frames
      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

      # Process GUI events and check keyboard input
      # Press 'q' to exit the loop
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
         break

      # Exit if the user closes any OpenCV window
      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
         cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
         break

      # Optional: limit frame rate to reduce CPU usage (about 30 FPS)
      time.sleep(1 / 30)

   # Stop the camera
   picam2.stop()

   # Close all OpenCV windows
   cv2.destroyAllWindows()

4. Explication du Code
-------------------

#. Importer les bibliothèques nécessaires :

   .. code-block:: python

      from picamera2 import Picamera2
      import cv2
      import time

   Picamera2 capture les images de la caméra Raspberry Pi, et OpenCV est utilisé pour la conversion et l'affichage des images.

#. Créer un objet Picamera2 et configurer la caméra :

   .. code-block:: python

      picam2 = Picamera2()

      config = picam2.create_preview_configuration(
          main={"size": (640, 480), "format": "XRGB8888"}
      )

      picam2.configure(config)
      picam2.start()

   Cela démarre la caméra en 640x480.
   ``XRGB8888`` est un format 4 canaux, donc chaque image capturée est de type BGRA.

#. Capturer une image en tant que tableau NumPy :

   .. code-block:: python

      frame_bgra = picam2.capture_array()

   Chaque boucle lit une image de la caméra.

#. Convertir l'image pour l'affichage :

   .. code-block:: python

      frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
      frame_gray = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2GRAY)

   - ``frame_bgr`` est utilisé pour l'affichage couleur normal.
   - ``frame_gray`` est une version en niveaux de gris de la même image.

#. Afficher les images dans deux fenêtres :

   .. code-block:: python

      cv2.imshow(WINDOW_BGR, frame_bgr)
      cv2.imshow(WINDOW_GRAY, frame_gray)

   Cela ouvre deux fenêtres OpenCV : l'une montre l'image couleur, l'autre montre l'image en niveaux de gris.

#. Conditions de sortie (appuyer sur ``q`` ou fermer une fenêtre) :

   .. code-block:: python

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
          break

      if (cv2.getWindowProperty(WINDOW_BGR, cv2.WND_PROP_VISIBLE) < 1 or
          cv2.getWindowProperty(WINDOW_GRAY, cv2.WND_PROP_VISIBLE) < 1):
          break

   - Appuyez sur ``q`` pour quitter.
   - Fermer l'une ou l'autre des fenêtres arrête également le programme en toute sécurité.

#. Limiter les FPS pour réduire l'utilisation du CPU :

   .. code-block:: python

      time.sleep(1 / 30)

   Cela ajoute un petit délai pour que la boucle tourne à environ 30 FPS, ce qui peut réduire la charge CPU sur le Raspberry Pi.

#. Arrêter la caméra et fermer les fenêtres OpenCV :

   .. code-block:: python

      picam2.stop()
      cv2.destroyAllWindows()

   Cela libère la caméra et ferme toutes les fenêtres OpenCV avant la sortie du programme.

5. L'Importance de la Conversion d'Espace Colorimétrique
---------------------------------------------------------------------------

Le format d'image brut fourni par la caméra peut ne pas toujours correspondre au format requis par OpenCV pour le traitement.
Dans cet exemple, Picamera2 produit des images au format **XRGB8888 (BGRA)**, tandis qu'OpenCV utilise principalement le format **BGR**.

Par conséquent, nous devons convertir l'image comme suit :

.. code-block:: python

   frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

Cela garantit que l'image est disposée dans l'ordre standard des canaux BGR utilisé par OpenCV, permettant un affichage et un traitement corrects.

Nous pouvons ensuite convertir l'image BGR en niveaux de gris pour un traitement ultérieur :

.. code-block:: python

   frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

Cela nous permet de transformer les images capturées par la caméra en un format adapté aux flux de traitement d'images OpenCV.

**Espaces Colorimétriques Courants et Cas d'Utilisation**

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Espace Colorimétrique
     - Caractéristiques
     - Cas d'Utilisation Typiques
   * - **BGR**
     - Format par défaut d'OpenCV
     - Affichage d'image, traitement de base, détection de contours
   * - **RGB**
     - Intuitif pour la perception humaine
     - Visualisation, entrée d'image pour l'apprentissage profond
   * - **GRAY**
     - Image en niveaux de gris à un seul canal
     - Détection d'objets, détection de contours, optimisation des performances
   * - **HSV**
     - Sépare la couleur de la luminosité
     - Détection de couleur, suivi d'objets, segmentation
   * - **YCrCb**
     - Sépare la luminance et la chrominance
     - Détection de visages, compression vidéo, robustesse à l'éclairage

Par exemple, **HSV** est souvent meilleur pour la **détection de couleur et le suivi d'objets**,
tandis que **YCrCb** est plus robuste pour la **reconnaissance faciale** ou les **scènes avec un éclairage variable**.

6. Extensions et Exercices
--------------------------------------------

- Essayez de convertir du BGR vers GRAY ou HSV et observez les résultats.

   Par exemple, utilisez :

   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)``
   - ``cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)``
   - et d'autres

- Testez différentes résolutions (par exemple, 1280x720) et observez l'effet sur la latence et la fréquence d'images.
- Combinez ce code avec l'exemple de lecture vidéo précédent pour implémenter la commutation entre un flux de caméra et une source vidéo.