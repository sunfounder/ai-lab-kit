.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Suivre des Objets avec le Support Motorisé
==================================================================


Dans les tutoriels précédents, nous avons appris à utiliser YOLO pour la détection d'objets sur Raspberry Pi. Cependant, la détection n'est que la première étape — si vous voulez que la caméra « suive » vraiment la cible, vous devez combiner la détection avec un contrôle mécanique.

Ce tutoriel vous guidera dans la construction d'un **système de suivi d'objets YOLO** qui réalise les objectifs suivants :

* Détection en temps réel d'objets spécifiques à l'aide de YOLO
* Calcul automatique de la déviation de position de la cible dans l'image
* Support motorisé commandé par servo pour maintenir la cible centrée dans l'image
* Prise en charge de la sauvegarde des images actuelles avec la touche ESPACE pour la collecte de données

Ici, nous suivons la cible de notre modèle personnalisé entraîné dans le tutoriel précédent — le mien est un bonhomme de neige. Vous pouvez également choisir d'autres modèles (comme yolov8n) pour suivre d'autres cibles (comme des personnes, des voitures, etc.).

.. image:: img/yolo_track.png

Figure : Système de suivi d'objets YOLO en action. Lorsque la cible se déplace, le support motorisé de la caméra suit automatiquement, maintenant la cible près du réticule jaune au centre de l'image. La boîte englobante verte marque la cible détectée.

**Scénarios d'application** :

* Surveillance intelligente : Suivi automatique des cibles suspectes
* Compagnon pour animaux : Laissez la caméra suivre les mouvements de votre animal
* Visioconférence : Maintenez automatiquement les intervenants centrés dans l'image
* Collecte de données : Capturez automatiquement des images multi-angles des cibles

Configuration Matérielle
---------------------------------------

Pour utiliser ce projet, vous devez assembler le support motorisé en suivant les instructions de :ref:`assemble_fusion_hat_pan_tilt`.

.. image:: ../quick_start/img/gimbal_assemble.png


Exécution du Code
----------------------------------------

1. **Modifier les paramètres de configuration**

   .. code-block:: bash

      cd ~/ai-lab-kit/yolo
      nano yolo_tracking.py

   Changez la variable ``TARGET`` au début du code pour l'objet que vous voulez suivre :

   .. code-block:: python

      TARGET = "person"     # Track a person
      # or
      TARGET = "snowman"    # Track a snowman

2. **Préparer le fichier de modèle**

   * Utilisez un modèle pré-entraîné : ``model = YOLO("yolov8n.pt")``
   * Utilisez un modèle personnalisé : ``model = YOLO("snowman.pt")``

3. **Sauvegardez et exécutez le code**

   .. code-block:: bash

      python3 yolo_tracking.py

4. **Instructions d'utilisation**

   * Après le démarrage du programme, la caméra commence à fonctionner automatiquement
   * Lorsqu'une cible est détectée, les servos tournent automatiquement pour maintenir la cible centrée dans l'image
   * Appuyez sur ``ESPACE`` pour sauvegarder l'image actuelle (pour collecter des données d'entraînement)
   * Appuyez sur ``ESC`` pour quitter le programme

Code
-----------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480         # Camera resolution
   CX, CY = W // 2, H // 2 # Center coordinates
   CONFIDENCE = 0.3        # Detection confidence threshold
   DEADZONE = 50           # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

   print(f"=== YOLO Tracking System ===")
   print(f"Target: {TARGET}")
   print(f"Confidence threshold: {CONFIDENCE}")
   print(f"Deadzone: {DEADZONE} pixels")

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

   # -------------------- Camera Initialization --------------------
   print("Initializing camera...")
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (W, H)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()
   time.sleep(2)

   print("\n=== System Ready ===")
   print("Controls:")
   print("  SPACE - Capture image (for dataset)")
   print("  ESC   - Exit")
   print("  (Auto-tracks object when detected)")
   print("==========================\n")

   # -------------------- Tracking Variables --------------------
   pan_pos = 0    # Current pan angle (-90 to 90)
   tilt_pos = 0   # Current tilt angle (-45 to 45)
   capture_count = 0

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

         # Process tracking if object found
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move

               # Limit servo angles to safe ranges
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))

               # Send commands to servos
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

         # Draw deadzone rectangle (visual reference)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")


Explication du Code
--------------

Voici le code complet de suivi d'objets YOLO. Nous allons analyser son principe de fonctionnement section par section.

**1. Importer les bibliothèques et les paramètres de configuration**

.. code-block:: python

   #!/usr/bin/env python3
   """
   YOLO-based Object Tracking for Raspberry Pi
   Tracks a specific object (e.g., person) using YOLO and controls servos
   Press SPACE to capture images for dataset, ESC to exit
   """

   from picamera2 import Picamera2
   from ultralytics import YOLO
   from fusion_hat.servo import Servo
   import cv2
   import time
   import os

   # -------------------- Configuration --------------------
   TARGET = "your_object"      # Object to track (class name)
   W, H = 640, 480             # Camera resolution
   CX, CY = W // 2, H // 2     # Center coordinates
   CONFIDENCE = 0.3            # Detection confidence threshold
   DEADZONE = 50               # Pixels from center before moving
   SAVE_DIR = "captured_images"  # Dataset save directory

   # Create save directory
   os.makedirs(SAVE_DIR, exist_ok=True)

Paramètres de configuration :

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Paramètre
     - Description
     - Valeur recommandée
   * - ``TARGET``
     - Nom de l'objet à suivre
     - « person », « snowman », « cup »
   * - ``W, H``
     - Résolution de la caméra
     - 640x480 (performances équilibrées)
   * - ``DEADZONE``
     - Plage de zone morte (pixels)
     - 50-100, empêche les tremblements fréquents
   * - ``CONFIDENCE``
     - Seuil de confiance de détection
     - 0.3-0.5
   * - ``SAVE_DIR``
     - Répertoire de sauvegarde des images
     - captured_images

**2. Initialiser les servos**

.. code-block:: python

   # -------------------- Servo Initialization --------------------
   print("Initializing servos...")
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)

Plages d'angle des servos :

* Servo panoramique (horizontal) : -90° à 90°, 0° est le centre
* Servo d'inclinaison (vertical) : -45° à 45°, 0° est le centre

**3. Charger le modèle YOLO**

.. code-block:: python

   # -------------------- YOLO Model Loading --------------------
   print("Loading YOLO model...")
   # Use YOLOv8n for best performance on Raspberry Pi
   model = YOLO("your_model.pt")
   print("Model loaded successfully")

Recommandations de sélection de modèle :

* Utilisez votre propre modèle entraîné : ``"snowman.pt"``, ``"my_pet.pt"``
* Utilisez un modèle pré-entraîné : ``"yolov8n.pt"`` (peut détecter 80 objets courants)

**4. Logique de détection et de suivi d'objets**

.. code-block:: python

   def simple_track(x, y):
      """
      Simple 4-direction tracking with deadzone
      Returns: (pan_move, tilt_move) where:
         pan_move: -1 (left), 0 (stop), 1 (right)
         tilt_move: -1 (down), 0 (stop), 1 (up)
      """
      if x is None or y is None:
         return 0, 0

      pan_move = 0
      tilt_move = 0

      # Horizontal movement (pan)
      if x < CX - DEADZONE:
         pan_move = 1           # Move right
      elif x > CX + DEADZONE:
         pan_move = -1          # Move left

      # Vertical movement (tilt)
      if y < CY - DEADZONE:
         tilt_move = -1         # Move down
      elif y > CY + DEADZONE:
         tilt_move = 1          # Move up

      return pan_move, tilt_move

   def find_target_detection(results, target_name):
      """
      Search YOLO detection results for target object
      Returns: (x_center, y_center, confidence) or (None, None, None)
      """
      if len(results[0].boxes) == 0:
         return None, None, None

      for box in results[0].boxes:
         class_id = int(box.cls[0])
         class_name = model.names[class_id]
         confidence = float(box.conf[0])

         # Case-insensitive partial match
         if target_name.lower() in class_name.lower():
               x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
               x_center = int((x1 + x2) / 2)
               y_center = int((y1 + y2) / 2)
               return x_center, y_center, confidence

      return None, None, None

Explication de la logique de suivi :

* **Mécanisme de zone morte** : Lorsque la cible est dans la zone morte près du centre de l'image, les servos ne bougent pas, empêchant les tremblements fréquents
* **Détermination de la direction** : Si la cible est à gauche du centre, tournez à droite ; si à droite du centre, tournez à gauche
* **Identification de la cible** : Trouvez l'objet à suivre en faisant correspondre les noms de classe

**5. Boucle principale**

.. code-block:: python

   # -------------------- Main Tracking Loop --------------------
   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Run YOLO detection
         results = model.predict(frame, imgsz=320, conf=CONFIDENCE, verbose=False)

         # Find target object
         obj_x, obj_y, obj_conf = find_target_detection(results, TARGET)

         # Process tracking if object found
         if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move

               # Limit servo angles to safe ranges
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))

               # Send commands to servos
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)

               # Draw detection box
               cv2.rectangle(frame, (obj_x - 30, obj_y - 30),
                           (obj_x + 30, obj_y + 30), (0, 255, 0), 2)
               cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 0), -1)

               status = f"{TARGET} detected: {obj_conf:.2f}"
               color = (0, 255, 0)
         else:
               status = f"No {TARGET} detected"
               color = (0, 0, 255)

         # Draw center crosshair and deadzone
         cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
         cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
         cv2.rectangle(frame, (CX - DEADZONE, CY - DEADZONE),
                        (CX + DEADZONE, CY + DEADZONE), (255, 255, 0), 1)

         # Display status information
         cv2.putText(frame, status, (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
         cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                     (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
         cv2.putText(frame, f"Captured: {capture_count} images", (10, 80),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         cv2.putText(frame, "SPACE=capture  ESC=exit", (10, 105),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         # Show video window
         cv2.imshow(f"YOLO Tracking - {TARGET}", frame)

         # Handle key presses
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key - capture image
               filename = f"{SAVE_DIR}/img_{capture_count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               capture_count += 1

               # Flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow(f"YOLO Tracking - {TARGET}", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key - exit
               print(f"\nExiting. Total captured: {capture_count} images")
               break

   finally:
      # -------------------- Cleanup --------------------
      print("Cleaning up...")
      pan.angle(0)      # Return to center
      tilt.angle(0)     # Return to center
      time.sleep(0.5)
      cv2.destroyAllWindows()
      picam2.stop()
      print("Tracking stopped. Servos centered.")

Optimisation des Performances
-----------------------------------------

Lors de l'exécution du système de suivi sur Raspberry Pi, les optimisations suivantes peuvent aider :

1. **Réduire la fréquence de détection** : Détectez toutes les 2-3 images, réutilisez les résultats de détection pour les autres images

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()
       if frame_count % 3 == 0:
           results = model.predict(frame, imgsz=320)
       frame_count += 1

2. **Réduire la région de détection** : Détectez uniquement dans les zones où la cible est susceptible d'apparaître

3. **Utiliser des modèles plus petits** : ``yolov8n.pt`` est le meilleur choix

4. **Ajuster la plage de zone morte** : Augmenter ``DEADZONE`` réduit les mouvements fréquents du servo

Questions Courantes
---------------------------------

**Q : Que faire si les servos ne bougent pas ?**

* Vérifiez si les servos sont correctement connectés
* Vérifiez que la bibliothèque fusion_hat est correctement installée

**Q : Que faire si la réponse du suivi est trop lente ?**

* Abaissez la résolution de la caméra (par exemple, 320x240)
* Réduisez la résolution de détection ``imgsz``
* Augmentez la plage de zone morte pour réduire les mouvements du servo

**Q : Que faire si la détection de la cible est instable ?**

* Ajustez le seuil ``CONFIDENCE`` (des valeurs plus basses détectent plus mais augmentent les faux positifs)
* Assurez un éclairage adéquat
* Utilisez un modèle entraîné personnalisé pour une meilleure spécificité

**Q : Comment ajuster la sensibilité du servo ?**

Modifiez la valeur du pas dans la fonction ``simple_track`` :

.. code-block:: python

   # Increase step size for faster servo movement
   pan_move = 2  # Originally 1
   tilt_move = 2

Fonctionnalités Étendues
-----------------------------------

**1. Ajouter le contrôle PID** (suivi plus fluide)

.. code-block:: python

   # Simplified PID controller example
   pan_error = CX - obj_x
   pan_output = pan_error * 0.05  # Proportional control
   pan_pos += int(pan_output)

**2. Enregistrer automatiquement la trajectoire de suivi**

.. code-block:: python

   # Record target position history
   trajectory = []
   trajectory.append((obj_x, obj_y))

**3. Envoyer des notifications lorsqu'une cible est détectée**

.. code-block:: python

   if obj_x is not None:
       # Send email or push notification
       pass

Résumé
---------------------

Grâce à ce tutoriel, vous avez appris :

* Comment combiner la détection d'objets YOLO avec le contrôle de servo
* Comment implémenter un système de suivi automatique basé sur la vision
* Comment utiliser les mécanismes de zone morte pour éviter les tremblements
* Comment collecter des données d'entraînement pendant le suivi

Ce système peut être largement appliqué dans des scénarios tels que la surveillance intelligente, la photographie automatisée et la vision robotique. Au fur et à mesure que les modèles YOLO évoluent, vous pouvez construire des systèmes de suivi encore plus intelligents — comme ajuster automatiquement le zoom en fonction de la taille de la cible, ou prédire le mouvement de la cible en fonction des trajectoires de mouvement.