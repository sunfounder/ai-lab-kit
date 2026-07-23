.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_object:


10. Détection d'Objets
======================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

En plus des modèles spécialisés pour le visage, les mains et la pose,
MediaPipe fournit également un **Détecteur d'Objets** polyvalent
basé sur TensorFlow Lite.

Ce chapitre montre comment utiliser le
modèle ``efficientdet_lite0.tflite`` sur Raspberry Pi
pour effectuer une détection d'objets en temps réel et visualiser les résultats
sur le flux de la caméra.

.. image:: img/mp_object.png
   :width: 500
   :align: center

Ce module peut être utilisé pour :

- Les démos de reconnaissance d'objets en temps réel
- La perception pour la domotique / la robotique
- La surveillance de sécurité simple
- Les projets de vision embarquée


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le programme effectue les étapes suivantes :

1. Initialiser le **ObjectDetector** de MediaPipe Tasks
   et charger le modèle ``efficientdet_lite0.tflite``.
2. Capturer des images du flux vidéo Picamera2.
3. Convertir chaque image en un objet ``mp.Image`` de MediaPipe.
4. Appeler ``detect_for_video`` pour exécuter la détection d'objets en temps réel.
5. Dessiner les boîtes englobantes et les étiquettes à l'aide d'OpenCV.
6. Limiter le nombre de détections affichées pour garder la sortie claire
   et maintenir des performances stables sur Raspberry Pi.

-----------------------------
3. Préparation du Modèle
-----------------------------

Cet exemple utilise le modèle **EfficientDet Lite0**
au format TensorFlow Lite (TFLite).

EfficientDet Lite0 est léger et optimisé pour
les appareils embarqués comme le Raspberry Pi.
Il offre un bon équilibre entre vitesse et précision.

Le fichier ``efficientdet_lite0.tflite`` est inclus dans le répertoire du projet
et peut être utilisé directement.

* `Page de téléchargement officielle du modèle <https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector#efficientdet-lite0_model_recommended>`_

Si une précision plus élevée est requise et que les performances du matériel le permettent,
vous pouvez passer à :

- EfficientDet Lite1
- EfficientDet Lite2

Vous pouvez également remplacer le modèle par votre propre modèle de détection d'objets
TFLite auto-entraîné, tant qu'il suit
les exigences de format du MediaPipe Tasks Object Detector.


------------------------
4. Exécuter le Code
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_object.py


#. Après avoir exécuté le programme, une fenêtre intitulée « Show Video » s'ouvre et affiche le flux en direct de la caméra.

   .. raw:: html

         <video width="500" loop muted controls>
             <source src="../_static/video/Media_10.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Pour chaque image vidéo, le modèle Object Detector (``efficientdet_lite0.tflite``) s'exécute en temps réel et recherche des objets reconnaissables dans la scène.

   Lorsque des objets sont détectés :

   - Une boîte englobante rectangulaire est dessinée autour de chaque objet.
   - Une étiquette et un score de confiance sont affichés au-dessus de la boîte au format ``nom: score`` (par exemple, ``person: 0.87``).
   - Seules les détections au-dessus de ``SCORE_THRESHOLD`` (valeur par défaut 0,5) sont affichées.
   - Pour garder l'affichage clair et maintenir les performances, le programme dessine jusqu'à ``MAX_DRAW`` détections (valeur par défaut 20) par image.

   Au fur et à mesure que la vue de la caméra change, les boîtes englobantes et les étiquettes se mettent à jour en continu en temps réel.

   Appuyez sur ``q`` pour quitter le programme.
   La caméra s'arrête et la fenêtre OpenCV se ferme automatiquement.

-----------------------------
5. Code Complet
-----------------------------

.. code-block:: python

   # STEP 1: Import the necessary modules.
   from picamera2 import Picamera2, Preview
   import cv2
   import numpy as np
   import time
   from pathlib import Path

   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Paths & basic settings --------------------
   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")  # Model path
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20  # Limit the number of drawn detections

   # -------------------- Helper: visualization --------------------
   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       img = bgr_image.copy()
       h, w = img.shape[:2]
       drawn = 0

       for det in detection_result.detections:
           bbox = det.bounding_box
           x1 = max(0, min(int(bbox.origin_x), w - 1))
           y1 = max(0, min(int(bbox.origin_y), h - 1))
           x2 = max(0, min(int(bbox.origin_x + bbox.width), w - 1))
           y2 = max(0, min(int(bbox.origin_y + bbox.height), h - 1))

           # top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw bounding box
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break
       return img

   # STEP 2: Initialize the detector
   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,
   )
   detector = vision.ObjectDetector.create_from_options(options)

   # STEP 3: Camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()
   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # Convert to RGB and wrap as mp.Image
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

       # STEP 4: Detect
       ts_ms = int(time.time() * 1000)
       detection_result = detector.detect_for_video(mp_image, ts_ms)

       # STEP 5: Visualize
       annotated = visualize(frame_bgr, detection_result)

       cv2.imshow("Show Video", annotated)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Après avoir exécuté le script, le flux de la caméra affichera :

- Des boîtes englobantes autour des objets détectés
- Des étiquettes de classification et des scores de confiance
- Une détection en temps réel (peut atteindre environ 10~20 FPS sur Raspberry Pi)

-----------------------------
6. Explication du Code
-----------------------------

**Configuration**

.. code-block:: python

   BASE_DIR = Path(__file__).resolve().parent
   TFLITE_MODEL_PATH = str(BASE_DIR / "efficientdet_lite0.tflite")
   SCORE_THRESHOLD = 0.5
   MAX_DRAW = 20

- ``SCORE_THRESHOLD`` contrôle la confiance minimale pour afficher les détections (appliqué dans le runtime Tasks).
- ``MAX_DRAW`` est une commodité d'interface pour limiter le nombre de boîtes que nous rendons par image.

**Imports**

.. code-block:: python

   from picamera2 import Picamera2, Preview
   import cv2, numpy as np, time
   from pathlib import Path
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

- ``mediapipe.tasks.python.vision`` héberge l'API **ObjectDetector** Tasks.
- Nous utilisons toujours OpenCV classique pour les fenêtres et le dessin.

**Aide à la visualisation**

.. code-block:: python

   def visualize(bgr_image: np.ndarray, detection_result) -> np.ndarray:
       """
       Draw bounding boxes and category labels on a BGR image.
       Compatible with MediaPipe Tasks ObjectDetector's detection_result.
       """
       img = bgr_image.copy()
       h, w = img.shape[:2]

       drawn = 0
       for det in detection_result.detections:
           bbox = det.bounding_box  # (origin_x, origin_y, width, height) in pixels
           x1 = int(bbox.origin_x); y1 = int(bbox.origin_y)
           x2 = int(bbox.origin_x + bbox.width); y2 = int(bbox.origin_y + bbox.height)

           # Clamp to frame bounds (defensive)
           x1 = max(0, min(x1, w - 1)); y1 = max(0, min(y1, h - 1))
           x2 = max(0, min(x2, w - 1)); y2 = max(0, min(y2, h - 1))

           # Top-1 category
           if det.categories:
               c = det.categories[0]
               name = c.category_name if c.category_name else "object"
               score = c.score if c.score is not None else 0.0
               caption = f"{name}: {score:.2f}"
           else:
               caption = "object"

           # Draw rectangle and caption
           cv2.rectangle(img, (x1, y1), (x2, y2), (0, 175, 255), 2)
           (tw, th), _ = cv2.getTextSize(caption, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
           cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), (0, 175, 255), -1)
           cv2.putText(img, caption, (x1 + 2, y1 - 4),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)

           drawn += 1
           if drawn >= MAX_DRAW:
               break

       return img

- Maintient la boucle principale propre.
- Évite de dépendre d'utilitaires « visualize » inexistants ; il fonctionne directement avec les sorties Tasks.

**Créer l'ObjectDetector**

.. code-block:: python

   BaseOptions = python.BaseOptions
   ObjectDetectorOptions = vision.ObjectDetectorOptions
   RunningMode = vision.RunningMode

   base_options = BaseOptions(model_asset_path=TFLITE_MODEL_PATH)
   options = ObjectDetectorOptions(
       base_options=base_options,
       score_threshold=SCORE_THRESHOLD,
       running_mode=RunningMode.VIDEO,  # VIDEO mode for streaming input
   )
   detector = vision.ObjectDetector.create_from_options(options)

- ``RunningMode.VIDEO`` est optimisé pour les flux et **nécessite des horodatages**.
- Le runtime Tasks gère en interne le redimensionnement/la normalisation de l'image pour vous.

**Configuration de la Caméra (Source de Diffusion)**

.. code-block:: python

   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

- 640×480 est un bon compromis entre FPS et précision sur Raspberry Pi.
- Picamera2 retourne du BGRA (``XRGB8888``) ; nous convertirons en BGR/RGB.

**Détection par Image**

.. code-block:: python

   frame_bgra = picam2.capture_array()
   frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
   frame_rgb  = cv2.cvtColor(frame_bgr,  cv2.COLOR_BGR2RGB)

   mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

   ts_ms = int(time.time() * 1000)  # monotonically increasing timestamp
   detection_result = detector.detect_for_video(mp_image, ts_ms)

- MediaPipe attend des tampons **RGB**.
- L'horodatage doit **augmenter à chaque image** ; utiliser ``time.time()*1000`` est suffisant pour cette démo.

**Rendu et Affichage**

.. code-block:: python

   annotated = visualize(frame_bgr, detection_result)
   cv2.imshow("Show Video", annotated)
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break

- L'aide retourne une image BGR prête pour l'affichage OpenCV.
- Appuyez sur ``q`` pour quitter la boucle.

**Nettoyage**

.. code-block:: python

   try:
       picam2.stop_preview()
   except Exception:
       pass
   picam2.stop()
   cv2.destroyAllWindows()

Libérez toujours la caméra et détruisez les fenêtres pour éviter de verrouiller le périphérique.

------------------------------------------------------
7. Performances et Applications
------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Direction d'optimisation
     - Effet
     - Suggestion
   * - Résolution
     - Une résolution plus élevée donne une image plus claire mais une vitesse plus lente
     - 640x480 est suffisant
   * - Sélection du modèle
     - Lite0 ~ Lite2
     - Lite0 est plus rapide, Lite2 est plus précis
   * - Dessin multi-objets
     - Trop d'objets provoquent de la latence
     - Utilisez ``MAX_DRAW`` pour limiter

------------------------------------------------------
8. Dépannage
------------------------------------------------------

- Aucun résultat de détection

  Si rien n'est détecté, le seuil de confiance peut être trop élevé.

  Essayez d'abaisser ``SCORE_THRESHOLD`` (par exemple, de 0,5 à 0,3) et testez à nouveau.

- Faible fréquence d'images

  Si la vidéo semble lente, le modèle ou la résolution peut être trop lourd pour le Raspberry Pi.

  Utilisez un modèle plus léger (``efficientdet_lite0.tflite``) et réduisez la résolution (par exemple, 640×480 ou 320×240). La fermeture d'autres processus d'arrière-plan peut également améliorer les performances.

- Décalage de la boîte de détection

  Si les boîtes englobantes semblent décalées ou sortent du cadre, cela est généralement dû à des problèmes de conversion de coordonnées.

  Assurez-vous que les coordonnées de la boîte englobante sont limitées aux limites de l'image. Cet exemple limite déjà ``x1, y1, x2, y2`` pour éviter un dessin hors limites.

- La détection semble chaotique

  Si trop d'objets sont détectés et que l'écran devient encombré, il peut être difficile de lire les résultats.

  Limitez le nombre de détections dessinées à l'aide de ``MAX_DRAW`` (par exemple, 10-20) pour garder la visualisation claire et stable.

-----------------------------
9. Résumé
-----------------------------

- Ce chapitre a implémenté une détection d'objets polyvalente basée sur MediaPipe Tasks ;
- A utilisé le modèle EfficientDet Lite0, équilibrant précision et performances ;
- Maîtrise de la méthode de visualisation des résultats de détection ;
- Peut être étendu à des modèles personnalisés (par exemple, fruits, véhicules, détection d'objets dangereux).