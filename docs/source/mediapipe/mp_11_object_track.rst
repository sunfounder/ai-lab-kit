.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. Suivi d'Objets avec Caméra sur Support Motorisé
=====================================================

------------------------------------------------------------
1. Aperçu
------------------------------------------------------------

Dans ce chapitre, nous étendons la détection d'objets MediaPipe
pour construire un **système de suivi d'objets** simple
à l'aide d'une plateforme à servos panoramique/inclinaison.

Le système détecte un objet cible spécifié
(par exemple, une « banane »)
et ajuste automatiquement deux servos
pour maintenir l'objet centré dans le champ de la caméra.

.. image:: img/mp_object_track.png
   :width: 500
   :align: center

Ce projet combine :

- La détection d'objets en temps réel
- Le contrôle de moteurs servo
- La logique de suivi proportionnel
- La superposition de retour visuel

Il démontre comment la vision par ordinateur peut directement piloter
du matériel physique en temps réel.


------------------------------------------------------------
2. Comment ça Fonctionne
------------------------------------------------------------

Le système de suivi suit ces étapes :

1. Initialiser les servos panoramique et d'inclinaison à la position centrale.
2. Configurer la caméra Raspberry Pi pour la diffusion vidéo.
3. Charger le modèle EfficientDet Lite0 pour la détection d'objets.
4. Détecter les objets dans chaque image à l'aide de MediaPipe Tasks.
5. Identifier l'objet cible (par exemple, « banana »).
6. Calculer le décalage de l'objet par rapport au centre de l'image.
7. Ajuster les angles des servos à l'aide d'un contrôle proportionnel.
8. Afficher les guides de suivi et l'état à l'écran.

Cet exemple montre comment le retour visuel
peut être utilisé pour contrôler dynamiquement le mouvement du matériel.

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

       sudo python3 ~/ai-lab-kit/mediapipe/mp_track_object.py

#. Après avoir exécuté le programme, la fenêtre de la caméra s'ouvre et commence la détection d'objets en temps réel.

   .. raw:: html

         <video width="300" loop muted controls>
             <source src="../_static/video/object_tracking.mp4" type="video/mp4">
             Votre navigateur ne supporte pas la balise vidéo.
         </video>

   Le système recherche l'objet cible spécifié (par défaut : ``banana``).
   Un réticule jaune est affiché au centre de l'écran comme point de référence.

   Lorsque l'objet cible apparaît dans l'image :

   - MediaPipe détecte l'objet à l'aide du modèle EfficientDet Lite0.
   - Le centre de la boîte englobante détectée est calculé.
   - Si l'objet est en dehors de la zone morte centrale, les servos panoramique et d'inclinaison se déplacent par pas.
   - La caméra tourne physiquement pour maintenir l'objet près du centre de l'image.
   - Une boîte de suivi verte est dessinée autour de l'objet.
   - L'écran affiche :

     - ``Tracking banana`` (statut)
     - Les angles actuels des servos (Pan / Tilt)

   Lorsque l'objet n'est pas détecté :

   - Les servos cessent de bouger.
   - Le texte de statut devient ``No banana found`` (affiché en rouge).

   La logique de suivi utilise un contrôle de zone morte simple à 4 directions :
   les servos ne bougent que lorsque l'objet est suffisamment loin du centre,
   empêchant les tremblements.

   Appuyez sur ``q`` pour arrêter le programme.

   Lors de la sortie :

   - Les deux servos retournent à la position centrale.
   - La caméra s'arrête.
   - La fenêtre d'affichage se ferme.
   - Un message est affiché : ``Tracking stopped. Servos centered.``

-----------------------------
4. Code Complet
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3

   import cv2
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2
   from pathlib import Path

   # MediaPipe imports
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Configuration --------------------
   TARGET = "banana"      # Object to track
   W, H = 640, 480           # Camera resolution
   CX, CY = W // 2, H // 2   # Center coordinates
   SCORE_THRESHOLD = 0.3     # Detection confidence threshold
   DEADZONE = 50             # Pixels from center before moving

   print(f"Tracking: {TARGET}")

   # -------------------- Servo Initialization --------------------
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)     # Allow servos to reach position

   # -------------------- Camera Initialization --------------------
   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))
   cam.start()
   time.sleep(2)     # Allow camera to stabilize

   # -------------------- MediaPipe Detector Setup --------------------
   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")

   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

   detector = vision.ObjectDetector.create_from_options(options)

   print("Ready. Press 'q' to quit")

   # -------------------- Tracking Logic --------------------
   def simple_track(x, y):
       """Basic 4-direction tracking with deadzone"""
       if x is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Left/right movement decision
       if x < CX - DEADZONE:
           pan_move = 1          # Move right
       elif x > CX + DEADZONE:
           pan_move = -1         # Move left

       # Up/down movement decision
       if y < CY - DEADZONE:
           tilt_move = -1        # Move down
       elif y > CY + DEADZONE:
           tilt_move = 1         # Move up

       return pan_move, tilt_move

   # -------------------- Main Tracking Loop --------------------
   pan_pos = 0   # Current pan angle (-90° to +90°)
   tilt_pos = 0  # Current tilt angle (-45° to +45°)

   try:
       while True:
           # Capture frame from camera
           frame = cam.capture_array()
           frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

           # Convert to RGB for MediaPipe
           rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

           # Detect objects in frame
           detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

           # Search for target object
           obj_x = obj_y = None
           for detection in detections.detections:
               for category in detection.categories:
                   # Case-insensitive search for target
                   if TARGET.lower() in str(category.category_name).lower():
                       bbox = detection.bounding_box
                       # Calculate object center
                       obj_x = bbox.origin_x + bbox.width // 2
                       obj_y = bbox.origin_y + bbox.height // 2
                       break

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

               # Draw tracking box around object
               cv2.rectangle(frame,
                            (obj_x - 30, obj_y - 30),
                            (obj_x + 30, obj_y + 30),
                            (0, 255, 0), 2)
               status = f"Tracking {TARGET}"
               color = (0, 255, 0)  # Green for tracking
           else:
               status = f"No {TARGET} found"
               color = (0, 0, 255)  # Red for not found

           # Draw center crosshair for reference
           cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
           cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)

           # Display status information
           cv2.putText(frame, status, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
           cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}",
                      (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
           cv2.putText(frame, "Press 'q' to quit", (10, 90),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

           # Show video window
           cv2.imshow(f"Track: {TARGET}", frame)

           # Exit on 'q' key press
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break

   finally:
       # -------------------- Cleanup --------------------
       pan.angle(0)      # Return to center
       tilt.angle(0)     # Return to center
       time.sleep(0.5)   # Allow movement
       cam.stop()        # Stop camera
       cv2.destroyAllWindows()  # Close display
       print("Tracking stopped. Servos centered.")

-----------------------------
5. Explication du Code
-----------------------------

**Section de Configuration**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET`` : Catégorie d'objet à suivre (doit être dans les classes du jeu de données COCO) ;
- ``W, H`` : Résolution de la caméra - équilibrée entre vitesse et détails ;
- ``CX, CY`` : Coordonnées du centre de l'image pour la référence de suivi ;
- ``SCORE_THRESHOLD`` : Confiance minimale pour une détection valide ;
- ``DEADZONE`` : Distance du centre avant le début du mouvement du servo (réduit les tremblements).

**Initialisation des Servos**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` et ``Servo(3)`` correspondent aux canaux sur Fusion HAT ;
- ``.angle(0)`` centre les servos à la position 0° ;
- ``time.sleep(1)`` garantit que les servos atteignent la position avant de continuer.

**Configuration de la Caméra**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- Utilise la bibliothèque Picamera2 pour une API caméra moderne ;
- Le format ``XRGB8888`` fournit des canaux couleur 8 bits ;
- ``time.sleep(2)`` permet au capteur de la caméra de se stabiliser.

**Détecteur MediaPipe**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- Charge le modèle EfficientDet Lite0 depuis le même répertoire ;
- ``RunningMode.VIDEO`` optimisé pour le traitement continu d'images ;
- ``detect_for_video()`` nécessite un horodatage pour chaque image.

**Fonction de Suivi**

.. code-block:: python

   def simple_track(x, y):
       if x < CX - DEADZONE:
           pan_move = 1      # Object left → move right
       elif x > CX + DEADZONE:
           pan_move = -1     # Object right → move left

       if y < CY - DEADZONE:
           tilt_move = -1    # Object up → move down
       elif y > CY + DEADZONE:
           tilt_move = 1     # Object down → move up

- Contrôle proportionnel simple (pas un vrai PID) ;
- La zone morte empêche les tremblements du servo pour les petits mouvements ;
- Retourne des valeurs de mouvement de -1, 0 ou 1 pour chaque axe.

**Traitement de la Boucle Principale**

.. code-block:: python

   # Object detection
   detections = detector.detect_for_video(mp_image, int(time.time() * 1000))

   # Find target object
   for detection in detections.detections:
       for category in detection.categories:
           if TARGET.lower() in str(category.category_name).lower():
               bbox = detection.bounding_box
               obj_x = bbox.origin_x + bbox.width // 2
               obj_y = bbox.origin_y + bbox.height // 2

1. Convertir l'image au format MediaPipe ;
2. Exécuter la détection d'objets avec l'horodatage actuel ;
3. Rechercher l'objet cible dans les détections (insensible à la casse) ;
4. Calculer les coordonnées du centre de l'objet.

**Logique de Contrôle des Servos**

.. code-block:: python

   if obj_x is not None:
       pan_move, tilt_move = simple_track(obj_x, obj_y)
       pan_pos += pan_move
       tilt_pos += tilt_move

       # Enforce safe angle limits
       pan_pos = max(-90, min(90, pan_pos))
       tilt_pos = max(-45, min(45, tilt_pos))

       pan.angle(pan_pos)
       tilt.angle(tilt_pos)

1. Obtenir les commandes de mouvement de la fonction de suivi ;
2. Mettre à jour les accumulateurs de position ;
3. Limiter les positions aux limites mécaniques ;
4. Envoyer les nouveaux angles aux servos.

**Retour Visuel**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)

   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)

   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- Boîte verte : Objet actuellement suivi ;
- Réticule jaune : Référence du centre de l'image ;
- Texte de statut : État de suivi et angles des servos.

**Routine de Nettoyage**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- Ramène les servos à la position centrale ;
- Arrête la capture de la caméra ;
- Ferme les fenêtres OpenCV ;
- S'exécute même en cas d'erreur (``try...finally``).

------------------------------------------------------
6. Options de Configuration
------------------------------------------------------

**Changer l'Objet Cible**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**Ajustement des Paramètres de Suivi**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive

   # Faster, more responsive tracking
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**Limites de Plage des Servos**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**Réglage des Performances**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing

   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. Considérations sur les Performances
------------------------------------------------------

.. list-table:: Facteurs de Performance
   :header-rows: 1

   * - Facteur
     - Effet sur les Performances
     - Recommandation
   * - Résolution de la Caméra
     - Plus élevée = détection plus lente
     - 640x480 bon équilibre
   * - Seuil de Détection
     - Plus bas = plus de détections mais plus de faux positifs
     - 0,3-0,5 optimal
   * - Taille de la Zone Morte
     - Plus grande = plus fluide mais moins réactive
     - 40-60 pixels
   * - Vitesse du Servo
     - Plus rapide = plus réactif mais peut dépasser
     - Envisagez un contrôle d'accélération
   * - Taille du Modèle
     - Lite0 le plus rapide, Lite2 le plus précis
     - Lite0 pour le suivi en temps réel

**Performances attendues :**

- **Raspberry Pi 4:** 8-15 FPS en 640x480
- **Latence de détection :** 100-200ms
- **Temps de réponse du servo :** 50-100ms par degré
- **Latence totale du système :** 200-400ms

------------------------------------------------------
8. Guide de Dépannage
------------------------------------------------------

.. list-table:: Problèmes Courants et Solutions
   :header-rows: 1

   * - Problème
     - Cause Possible
     - Solution
   * - Aucune détection d'objet
     - Objet pas dans les classes COCO
     - Utilisez des noms d'objets supportés
   * - Mouvement du servo saccadé
     - Zone morte trop petite
     - Augmentez DEADZONE à 60-80
   * - Dépassement du servo
     - Pas de mouvement trop grand
     - Changez pan_move de 1 à 0,5
   * - Faible FPS
     - Résolution trop élevée
     - Réduisez à 320x240
   * - Caméra ne fonctionne pas
     - Caméra non activée
     - Exécutez ``sudo raspi-config``
   * - Les servos ne bougent pas
     - Câblage ou alimentation incorrect
     - Vérifiez les connexions et l'alimentation
   * - Objet perdu fréquemment
     - Seuil trop élevé
     - Réduisez SCORE_THRESHOLD à 0,2
   * - Direction de suivi incorrecte
     - Orientation du servo inversée
     - Échangez les signes de pan_move

**Conseils de débogage :**

1. **Testez les servos séparément :**

   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **Vérifiez la détection d'objets :**

   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **Vérifiez les coordonnées de l'objet :**

   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **Surveillez la fréquence d'images :**

   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. Modifications Avancées
------------------------------------------------------

**1. Implémentation du Contrôle PID**

.. code-block:: python

   class PIDController:
       def __init__(self, kp=0.1, ki=0.01, kd=0.05):
           self.kp, self.ki, self.kd = kp, ki, kd
           self.prev_error = 0
           self.integral = 0

       def update(self, error, dt=1.0):
           self.integral += error * dt
           derivative = (error - self.prev_error) / dt
           output = self.kp*error + self.ki*self.integral + self.kd*derivative
           self.prev_error = error
           return output

**2. Suivi d'Objets Multiples**

.. code-block:: python

   # Track closest object
   best_dist = float('inf')
   best_obj = None
   for detection in detections.detections:
       bbox = detection.bounding_box
       obj_x = bbox.origin_x + bbox.width // 2
       obj_y = bbox.origin_y + bbox.height // 2
       dist = ((obj_x - CX)**2 + (obj_y - CY)**2)**0.5
       if dist < best_dist:
           best_dist = dist
           best_obj = (obj_x, obj_y)

**3. Vitesse Proportionnelle à la Distance**

.. code-block:: python

   def adaptive_track(x, y):
       if x is None:
           return 0, 0

       # Calculate distance from center
       dx = x - CX
       dy = y - CY

       # Speed proportional to distance (with deadzone)
       pan_move = 0
       tilt_move = 0

       if abs(dx) > DEADZONE:
           pan_move = dx * 0.02  # 2% of distance per frame

       if abs(dy) > DEADZONE:
           tilt_move = dy * 0.02

       return pan_move, tilt_move

**4. Mémoire d'Objet (Suivi Inertiel)**

.. code-block:: python

   # Keep tracking briefly when object lost
   OBJECT_TIMEOUT = 10  # frames
   lost_counter = 0

   if obj_x is not None:
       last_x, last_y = obj_x, obj_y
       lost_counter = 0
   elif lost_counter < OBJECT_TIMEOUT:
       obj_x, obj_y = last_x, last_y  # Use last known position
       lost_counter += 1

------------------------------------------------------
10. Applications et Extensions
------------------------------------------------------

**Applications Éducatives :**

- Principes de robotique et d'automatisation
- Fondamentaux de la vision par ordinateur
- Systèmes de contrôle (P vs PID)
- Conception de systèmes en temps réel

**Applications Pratiques :**

- Suivi automatique pour caméra de sécurité
- Automatisation de caméra de visioconférence
- Observation de la faune
- Technologie d'assistance pour le suivi

**Projets d'Extension :**

1. **Interface Web :** Contrôle à distance via navigateur
2. **Positions Prédéfinies :** Sauvegarder/charger des positions de suivi courantes
3. **Apprentissage d'Objets :** Entraînement sur des objets personnalisés
4. **Multi-caméra :** Coordonner plusieurs unités de suivi
5. **Intégration Cloud :** Télécharger les données de suivi pour analyse
6. **Retour Audio :** Annoncer l'état du suivi
7. **Contrôle Gestuel :** Utiliser des gestes de la main pour contrôler le suivi

-----------------------------
11. Sécurité et Bonnes Pratiques
-----------------------------

1. **Sécurité Mécanique :**

   - Fixez toutes les pièces mobiles
   - Utilisez une gestion des câbles
   - Évitez les points de pincement
   - Définissez des limites d'angle raisonnables

2. **Sécurité Électrique :**

   - Utilisez une alimentation externe pour les servos
   - Assurez une mise à la terre appropriée
   - Évitez de surcharger l'alimentation
   - Utilisez des fils de calibre approprié

3. **Sécurité Logicielle :**

   - Incluez toujours le centrage des servos à la sortie
   - Implémentez un mécanisme d'arrêt d'urgence
   - Enregistrez les erreurs pour le débogage
   - Validez les entrées et les limites

4. **Sécurité Opérationnelle :**

   - Restez à l'écart du mécanisme en mouvement
   - Surveillez la surchauffe
   - Effectuez des vérifications de maintenance régulières
   - Ayez une capacité de contournement manuel

-----------------------------
12. Résumé
-----------------------------

Ce chapitre a démontré un système complet de suivi d'objets utilisant :

1. **MediaPipe Tasks** pour une détection d'objets fiable
2. **Des servos panoramique/inclinaison** pour le suivi physique
3. **Un contrôle proportionnel simple** pour la logique de mouvement
4. **OpenCV** pour le retour visuel et l'affichage

Le système fournit une base pour des applications de suivi plus avancées et démontre des concepts clés en vision par ordinateur en temps réel, systèmes de contrôle et programmation Python embarquée.

En modifiant l'objet cible, en ajustant les paramètres et en étendant la logique de contrôle, ce système peut être adapté à diverses applications, des démonstrations éducatives aux solutions d'automatisation pratiques.

**Prochaines étapes :**

- Implémenter le contrôle PID pour un suivi plus fluide
- Ajouter une mémoire d'objet pour la gestion d'occultation temporaire
- Créer une interface Web pour la surveillance à distance
- Intégrer avec des systèmes domotiques
- Entraîner des modèles de détection d'objets personnalisés