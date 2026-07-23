.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. Suivi d'Objets avec MeanShift
=========================================

MeanShift est un algorithme classique de suivi d'objets basé sur l'histogramme.
Dans cette leçon, nous allons non seulement implémenter un exemple complet de **suivi MeanShift**, mais aussi expliquer **pourquoi** chaque étape est effectuée et **ce qui se passe sous le capot**.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

1. Qu'est-ce que MeanShift ?
-------------------------

MeanShift déplace itérativement une fenêtre en fonction de la densité de probabilité pour **trouver l'emplacement le plus probable de la cible**.

En termes simples :
Vous donnez d'abord à l'algorithme une « région cible initiale ». Il calcule les caractéristiques de couleur de cette région (par exemple, l'histogramme de couleur de la cible), puis dans chaque image suivante, il trouve la zone la plus similaire à cette couleur et y déplace le rectangle.

Ce processus ne repose pas sur l'apprentissage profond et ne nécessite aucun pré-entraînement. Il est très léger.

.. image:: img/opencv_meanshift.png
   :alt: Suivi MeanShift
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
      python3 cv_5_meanshift.py

#. Lorsque vous exécutez le programme, une fenêtre OpenCV nommée **MeanShift Tracker** apparaît et commence à lire le fichier vidéo ``sample2.mp4``.

   Un rectangle vert sera dessiné autour de l'objet cible et mis à jour en temps réel à l'aide de l'algorithme de suivi MeanShift.

   La fenêtre de suivi se déplacera au fur et à mesure que l'objet bouge dans la vidéo.

   Vous pouvez quitter le programme de deux manières :

   * Appuyer sur la touche **q** du clavier
   * Fermer la fenêtre en cliquant sur le bouton de fermeture (X)

   Après la sortie, la lecture vidéo s'arrête et toutes les fenêtres OpenCV sont fermées.

3. Code Complet
-----------------------

Voici le script complet de suivi MeanShift (``cv_5_meanshift.py``) :

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Explication
---------------------------

#. Ouvrir le fichier vidéo :

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Cela crée un objet de capture vidéo afin qu’OpenCV puisse lire les images du fichier.

#. Lire la première image et vérifier qu’elle fonctionne :

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   Le suivi MeanShift a besoin d’une image initiale pour apprendre ce qu’il doit suivre.

#. Définir la fenêtre de suivi initiale (l’objet que vous voulez suivre) :

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   Ce rectangle est la position de départ de la cible (ROI).
   Vous ajustez généralement ces valeurs pour correspondre à l’objet dans la première image.

#. Convertir la première image en HSV et extraire la ROI :

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV est couramment utilisé pour le suivi car le canal de Teinte décrit la couleur de manière plus cohérente que RGB/BGR.

#. Construire un masque pour ignorer les pixels faibles/invalides dans la ROI :

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   Cela filtre les pixels avec une saturation/valeur très faible (souvent des ombres ou du bruit), améliorant la stabilité du suivi.

#. Calculer et normaliser l’histogramme de la ROI (canal de Teinte) :

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - L’histogramme décrit la distribution des couleurs de la cible (Teinte).
   - La normalisation rend l’échelle de l’histogramme cohérente entre différents éclairages ou tailles de ROI.

#. Définir les critères de terminaison pour MeanShift :

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift s’arrêtera lorsque :
   - il atteint 15 itérations, ou
   - le déplacement de la fenêtre est inférieur à 2 pixels.

#. Définir un délai de lecture basé sur les FPS de la vidéo :

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Cela maintient la lecture proche de la vitesse vidéo d’origine.
   Si les FPS ne peuvent pas être lus, on utilise 30 FPS par défaut.

#. Convertir chaque image en HSV (pour le suivi) :

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   Le suivi est effectué en HSV pour correspondre à l’histogramme de Teinte de la cible.

#. Rétroprojection (trouver où la couleur cible est susceptible d’être) :

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   La rétroprojection produit une carte de probabilité : les zones claires sont plus susceptibles de correspondre à l’histogramme de la ROI.

#. Mettre à jour la fenêtre de suivi avec MeanShift :

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift déplace la fenêtre de suivi vers la zone de plus haute densité dans la carte de probabilité, mettant à jour la position de la cible image par image.

#. Dessiner le résultat du suivi :

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   Cela dessine le rectangle de suivi actuel sur l’image vidéo.

#. Afficher la fenêtre et les conditions de sortie :

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - Appuyez sur ``q`` pour quitter.
   - La fermeture de la fenêtre permet également de sortir en toute sécurité.

#. Libérer les ressources :

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Libérez toujours la vidéo et fermez les fenêtres pour libérer les ressources système.

5. MeanShift vs. CAMShift
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Caractéristique
     - MeanShift
     - CAMShift
   * - Taille de fenêtre
     - Fixe
     - Auto-adaptative (s’adapte à l’échelle de la cible)
   * - Rotation de la cible
     - Non supportée
     - Supportée
   * - Scénarios adaptés
     - Taille de cible relativement stable
     - La cible peut changer d’échelle/rotation
   * - Applications
     - Suivi simple, balles, marqueurs
     - Suivi pratique, surveillance, reconnaissance


6. Avancé : Sélectionner la ROI avec la Souris
--------------------------------------

Précédemment, nous avons utilisé des valeurs fixes :

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

C’est simple mais pas flexible.
Si vous changez de vidéo ou si la cible commence ailleurs, vous devez modifier le code.

OpenCV fournit ``cv2.selectROI`` pour **sélectionner la région cible interactivement sur la première image** avec la souris, et le programme obtiendra ``(x, y, w, h)`` automatiquement.

**Code d’initialisation modifié**

Exécutez ``cv_5_meanshift_auto.py`` pour le code modifié.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

Lorsque vous exécutez le programme, la première image de la vidéo sera affichée et vous serez invité à sélectionner une région d’intérêt (ROI) à l’aide de la souris.

Faites glisser la souris pour dessiner un rectangle autour de l’objet cible, puis appuyez sur **Entrée** ou **Espace** pour confirmer la sélection.
Appuyez sur **Esc** pour annuler la sélection.

Après avoir confirmé la ROI, une fenêtre nommée **MeanShift Tracker** apparaîtra.
L’objet sélectionné sera suivi avec une boîte englobante verte, et la boîte se déplacera au fur et à mesure que l’objet bouge dans la vidéo.

Pour arrêter le programme :

* Appuyez sur la touche **q** du clavier
* Ou fermez la fenêtre d’affichage avec le bouton de fermeture (X)

Après la sortie, la lecture vidéo s’arrête et toutes les fenêtres OpenCV sont fermées.

.. image:: img/opencv_meanshift_mouse.png
   :alt: Fenêtre de sélection interactive de la ROI
   :align: center

**Remarques**

``cv2.selectROI`` est le sélecteur de ROI interactif intégré d’OpenCV, idéal pour l’initialisation manuelle.
Il retourne ``(x, y, w, h)``, qui est totalement compatible avec ``track_window``, vous n’avez donc pas besoin de modifier la logique principale CAMShift/MeanShift.
Cela vous permet de réutiliser le même programme sur différentes vidéos et cibles.


7. Avancé II : Calcul Dynamique des Seuils HSV pour la ROI
--------------------------------------------------------------

Le fichier ``cv_5_meanshift.py`` d’origine utilise des seuils HSV définis manuellement, adaptés lorsque la couleur de la cible est fixe et l’éclairage stable.

.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

Si l’éclairage varie significativement ou si la couleur de la cible n’est pas fixe, les limites ``inRange`` codées en dur peuvent être sous-optimales.
Une approche plus intelligente consiste à **calculer automatiquement les limites inférieure/supérieure HSV à partir de la ROI sélectionnée**.

**Exemple : Calcul automatique des seuils HSV**

Exécutez ``cv_5_meanshift_auto.py`` pour le code modifié.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)


Lors de la sélection de cibles très sombres ou très lumineuses, vous n’avez plus besoin de modifier manuellement les seuils ; cela s’adapte également rapidement aux différents éclairages et couleurs.

.. note::

   - ``np.percentile`` (5 %–95 %) élimine les extrêmes (bords, ombres, hautes lumières, etc.) dans la ROI, améliorant la robustesse.
   - ``pad_h``, ``pad_s``, ``pad_v`` fournissent une tolérance pour que les petits changements de couleur soient encore capturés.
   - ``lower`` et ``upper`` sont les limites HSV dynamiques utilisées directement avec ``cv2.inRange``.


**Résumé**

- Utilisez ``cv2.selectROI`` pour une initialisation flexible de la cible.
- Utilisez ``np.percentile`` pour calculer automatiquement les limites HSV pour l’adaptabilité.
- Combiné avec ``cv2.inRange`` et CAMShift/MeanShift, cette approche reste stable sous des éclairages et des variations de cible difficiles.
