.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

9. Suivi d'Objets Rouges avec Caméra sur Support Motorisé
=============================================================

Le suivi d'objets combiné au contrôle mécanique constitue la base de nombreuses applications en robotique et en vision par ordinateur.
Dans ce chapitre, nous allons créer un système qui **détecte les objets rouges en temps réel et contrôle les servos du support motorisé** pour maintenir l'objet centré dans le champ de la caméra.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_9.mp4" type="video/mp4">
          Votre navigateur ne supporte pas la balise vidéo.
      </video>

Cela étend la détection de couleur de base en un système de suivi actif capable de suivre des objets en mouvement de manière autonome.

.. image:: img/color_track.png
   :alt: Aperçu du système de suivi avec caméra sur support motorisé
   :align: center


1. Objectif et Approche
-------------------------

- Utiliser **Picamera2** pour capturer des images vidéo en temps réel
- Détecter les objets rouges à l'aide de **l'espace colorimétrique HSV** et du filtrage morphologique
- Implémenter un algorithme de **suivi simple à 4 directions** basé sur la position de l'objet
- Contrôler les **servos panoramique et d'inclinaison** pour maintenir l'objet centré
- Afficher des **informations de débogage en temps réel** et l'état du suivi
- Fournir des **paramètres ajustables** pour affiner le comportement du suivi


2. Exécuter le Code
--------------------

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
        python3 cv_9_track_color.py

3. Résultat d'Exécution
---------------------------------

Lorsque le programme s'exécute correctement, vous devriez voir :

**1. Fenêtre OpenCV :**

- « Red Object Tracking » : Affiche le flux de la caméra avec la superposition de suivi

**2. Éléments visuels dans la fenêtre de suivi :**

- Croix jaune au centre de l'image
- Rectangle bleu montrant la zone morte (zone sans mouvement)
- Cercle rouge marquant le centre de l'objet détecté
- Ligne verte reliant l'objet au centre de l'image
- Informations en temps réel superposées :

  - Coordonnées de la position de l'objet
  - Angles actuels des servos
  - Mode de suivi (Simple 4-Direction)
  - Pas de mouvement et paramètres de zone morte

**3. Sortie console :**

- FPS (images par seconde)
- Positions actuelles des servos
- État de la détection d'objet
- Ajustements du pas de mouvement

**4. Comportement des servos :**

- Les servos se déplacent par pas fixes pour maintenir les objets rouges centrés
- Aucun mouvement lorsque l'objet est dans la zone morte
- Les servos retournent à la position centrale lorsque la touche 'r' est pressée


**Contrôles :**

- Appuyez sur **'q'** pour quitter le programme
- Appuyez sur **'r'** pour réinitialiser les servos à la position centrale
- Appuyez sur **'+'** pour augmenter la vitesse de déplacement
- Appuyez sur **'-'** pour diminuer la vitesse de déplacement

4. Code Complet
-------------------------------

Voici le programme Python complet pour le suivi d'objets rouges :

.. code-block:: python

   #!/usr/bin/env python3
   """
   Red Object Tracking with Pan-Tilt Camera
   """

   import cv2
   import numpy as np
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2

   # ========== SERVO SETTINGS ==========
   # Servo channels
   PAN_CHANNEL = 2    # Horizontal servo
   TILT_CHANNEL = 3   # Vertical servo

   # Servo angle limits (adjust according to your hardware)
   PAN_MIN = -90      # Maximum left rotation
   PAN_MAX = 90       # Maximum right rotation
   TILT_MIN = -45     # Maximum down rotation
   TILT_MAX = 45      # Maximum up rotation

   # Initial position (center)
   PAN_CENTER = 0
   TILT_CENTER = 0

   # ========== CAMERA SETTINGS ==========
   FRAME_WIDTH = 640
   FRAME_HEIGHT = 480
   CENTER_X = FRAME_WIDTH // 2
   CENTER_Y = FRAME_HEIGHT // 2

   # ========== COLOR DETECTION SETTINGS ==========
   # Red color range in HSV (two ranges for red)
   LOWER_RED1 = np.array([0, 100, 80])     # Lower range for red
   UPPER_RED1 = np.array([10, 255, 255])   # Upper range for red
   LOWER_RED2 = np.array([170, 100, 80])   # Lower range for red (wrap-around)
   UPPER_RED2 = np.array([180, 255, 255])  # Upper range for red (wrap-around)

   # Morphology kernel for noise removal
   KERNEL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

   # Minimum contour area to consider (adjust based on object size)
   MIN_CONTOUR_AREA = 500

   # ========== TRACKING SETTINGS ==========
   # Deadzone around center (pixels) - no movement inside this zone
   DEADZONE_X = 50    # Horizontal deadzone
   DEADZONE_Y = 50    # Vertical deadzone

   # Movement step size in degrees (how much to move each frame)
   MOVE_STEP = 2      # Degrees to move per adjustment

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Red Object Tracking System...")

   # Initialize servos
   print("Setting up servos...")
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center the servos initially
   print("Centering servos...")
   pan_servo.angle(PAN_CENTER)
   tilt_servo.angle(TILT_CENTER)
   time.sleep(1)  # Wait for servos to move to center

   # Current servo positions
   current_pan = PAN_CENTER
   current_tilt = TILT_CENTER

   # Initialize camera
   print("Setting up camera...")
   picam2 = Picamera2()

   # Configure camera for OpenCV
   config = picam2.create_preview_configuration(
       main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "XRGB8888"}
   )
   picam2.configure(config)
   picam2.start()

   print("Camera started. Looking for red objects...")
   print("Press 'q' to quit the program")
   print("-" * 50)

   def simple_tracking(x, y):
       """
       Simple 4-direction tracking algorithm
       Args:
           x: Object x-coordinate (None if not found)
           y: Object y-coordinate (None if not found)
       Returns:
           pan_move, tilt_move: Degrees to move each servo (+/-)
       """
       # If no object detected, don't move
       if x is None or y is None:
           return 0, 0

       pan_move = 0
       tilt_move = 0

       # Check if object is left of center (outside deadzone)
       if x < CENTER_X - DEADZONE_X:
           # Object is left, move camera right (positive pan)
           pan_move = MOVE_STEP
       # Check if object is right of center (outside deadzone)
       elif x > CENTER_X + DEADZONE_X:
           # Object is right, move camera left (negative pan)
           pan_move = -MOVE_STEP

       # Check if object is above center (outside deadzone)
       if y < CENTER_Y - DEADZONE_Y:
           # Object is up, move camera down (negative tilt)
           tilt_move = -MOVE_STEP
       # Check if object is below center (outside deadzone)
       elif y > CENTER_Y + DEADZONE_Y:
           # Object is down, move camera up (positive tilt)
           tilt_move = MOVE_STEP

       return pan_move, tilt_move

   def update_servo_position(pan_move, tilt_move):
       """
       Update servo positions with limits checking
       Args:
           pan_move: Degrees to move pan servo (+/-)
           tilt_move: Degrees to move tilt servo (+/-)
       Returns:
           current_pan, current_tilt: New servo positions
       """
       global current_pan, current_tilt

       # Calculate new positions
       new_pan = current_pan + pan_move
       new_tilt = current_tilt + tilt_move

       # Apply angle limits to prevent hardware damage
       new_pan = max(min(new_pan, PAN_MAX), PAN_MIN)
       new_tilt = max(min(new_tilt, TILT_MAX), TILT_MIN)

       # Move servos only if position changed
       if new_pan != current_pan:
           pan_servo.angle(new_pan)
           current_pan = new_pan

       if new_tilt != current_tilt:
           tilt_servo.angle(new_tilt)
           current_tilt = new_tilt

       return current_pan, current_tilt

   def find_red_object(frame):
       """
       Detect red object in frame using HSV color space
       Args:
           frame: Input BGR image frame
       Returns:
           center_x, center_y: Coordinates of largest red object, or (None, None)
           mask: Binary mask showing detected red areas
       """
       # Convert BGR to HSV color space (better for color detection)
       hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

       # Create masks for red color (red wraps around 0 in HSV)
       mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)   # Lower red range
       mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)   # Upper red range
       mask = cv2.bitwise_or(mask1, mask2)                # Combine both ranges

       # Apply morphological operations to clean up noise
       mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, KERNEL, iterations=1)
       mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL, iterations=2)

       # Find contours in the mask
       contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

       # Return if no contours found
       if not contours:
           return None, None, mask

       # Find the largest contour (assume it's our target)
       largest_contour = max(contours, key=cv2.contourArea)
       area = cv2.contourArea(largest_contour)

       # Filter by minimum area to ignore small noise
       if area < MIN_CONTOUR_AREA:
           return None, None, mask

       # Calculate center of the contour using image moments
       M = cv2.moments(largest_contour)
       if M["m00"] == 0:  # Prevent division by zero
           return None, None, mask

       center_x = int(M["m10"] / M["m00"])
       center_y = int(M["m01"] / M["m00"])

       return center_x, center_y, mask

   def draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle):
       """
       Draw debugging information on the frame for visualization
       Args:
           frame: Frame to draw on
           object_x, object_y: Object coordinates
           mask: Detection mask
           pan_angle, tilt_angle: Current servo angles
       Returns:
           frame: Frame with debug drawings
       """
       # Draw center crosshair
       cv2.line(frame, (CENTER_X - 20, CENTER_Y), (CENTER_X + 20, CENTER_Y), (0, 255, 255), 2)
       cv2.line(frame, (CENTER_X, CENTER_Y - 20), (CENTER_X, CENTER_Y + 20), (0, 255, 255), 2)
       cv2.circle(frame, (CENTER_X, CENTER_Y), 5, (0, 255, 255), -1)

       # Draw deadzone rectangle
       cv2.rectangle(frame,
                    (CENTER_X - DEADZONE_X, CENTER_Y - DEADZONE_Y),
                    (CENTER_X + DEADZONE_X, CENTER_Y + DEADZONE_Y),
                    (255, 255, 0), 1)

       # Draw object center if detected
       if object_x is not None and object_y is not None:
           cv2.circle(frame, (object_x, object_y), 10, (0, 0, 255), -1)
           cv2.line(frame, (CENTER_X, CENTER_Y), (object_x, object_y), (0, 255, 0), 2)

           # Display position information
           pos_text = f"Position: ({object_x}, {object_y})"
           cv2.putText(frame, pos_text, (10, 30),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

       # Display servo angles
       angle_text = f"Pan: {pan_angle:+03.0f}, Tilt: {tilt_angle:+03.0f}"
       cv2.putText(frame, angle_text, (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

       # Display tracking mode
       cv2.putText(frame, "Mode: Simple 4-Direction", (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Display movement step
       step_text = f"Step: {MOVE_STEP}, Deadzone: {DEADZONE_X}px"
       cv2.putText(frame, step_text, (10, 120),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

       # Draw quit instruction
       cv2.putText(frame, "Press 'q' to quit, 'r' to reset", (10, FRAME_HEIGHT - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

       return frame

   def cleanup():
       """
       Clean up resources before exiting
       """
       print("\nCleaning up...")

       # Center servos before stopping
       print("Centering servos...")
       pan_servo.angle(PAN_CENTER)
       tilt_servo.angle(TILT_CENTER)
       time.sleep(0.5)

       # Stop camera
       print("Stopping camera...")
       picam2.stop()

       # Close OpenCV windows
       cv2.destroyAllWindows()
       print("System shutdown complete.")

   # ========== MAIN LOOP ==========
   def main():
       """
       Main tracking loop
       """
       frame_count = 0
       start_time = time.time()
       global MOVE_STEP
       global current_pan, current_tilt
       try:
           while True:
               # Capture frame from camera
               frame_bgra = picam2.capture_array()
               frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

               # Find red object in frame
               obj_x, obj_y, mask = find_red_object(frame_bgr)

               # Use simple tracking algorithm to determine movement
               pan_move, tilt_move = simple_tracking(obj_x, obj_y)

               # Update servo positions
               pan_angle, tilt_angle = update_servo_position(pan_move, tilt_move)

               # Draw debugging information
               frame_display = draw_debug_info(frame_bgr, obj_x, obj_y, mask, pan_angle, tilt_angle)

               # Display frames
               cv2.imshow("Red Object Tracking", frame_display)

               # Calculate and display FPS every 30 frames
               frame_count += 1
               if frame_count % 30 == 0:
                   elapsed_time = time.time() - start_time
                   fps = frame_count / elapsed_time
                   print(f"FPS: {fps:.1f} | Pan: {pan_angle:+03.0f}° | Tilt: {tilt_angle:+03.0f}° | "
                         f"Object: {'Found' if obj_x else 'Not found'}")

               # Check for user input
               key = cv2.waitKey(1) & 0xFF
               if key == ord('q'):
                   print("\nQuit command received.")
                   break
               elif key == ord('r'):
                   # Reset to center position
                   print("Resetting to center...")
                   pan_servo.angle(PAN_CENTER)
                   tilt_servo.angle(TILT_CENTER)
                   current_pan = PAN_CENTER
                   current_tilt = TILT_CENTER
                   time.sleep(0.5)
               elif key == ord('+'):
                   # Increase movement speed
                   MOVE_STEP = min(MOVE_STEP + 0.5, 5)
                   print(f"Movement step increased to {MOVE_STEP}°")
               elif key == ord('-'):
                   # Decrease movement speed
                   MOVE_STEP = max(MOVE_STEP - 0.5, 0.5)
                   print(f"Movement step decreased to {MOVE_STEP}°")

       except KeyboardInterrupt:
           print("\nProgram interrupted.")

       finally:
           cleanup()

   # ========== PROGRAM START ==========
   if __name__ == "__main__":
       print("=" * 60)
       print("RED OBJECT TRACKING WITH PAN-TILT CAMERA")
       print("=" * 60)
       print("System will:")
       print("1. Detect red objects using OpenCV")
       print("2. Move servos in 4 directions to keep object centered")
       print("3. Display tracking information")
       print("\nControls:")
       print("  Press 'q' to quit")
       print("  Press 'r' to reset servos to center")
       print("  Press '+' to increase movement speed")
       print("  Press '-' to decrease movement speed")
       print("\nTracking Logic:")
       print(f"  Deadzone: {DEADZONE_X}px around center (no movement)")
       print(f"  Movement: {MOVE_STEP}° per adjustment")
       print("  Left object \342\206\222 Move right (+pan)")
       print("  Right object \342\206\222 Move left (-pan)")
       print("  Up object \342\206\222 Move down (-tilt)")
       print("  Down object \342\206\222 Move up (+tilt)")
       print("=" * 60)

       main()


5. Explication du Code
----------------------------------

#. ``simple_tracking(x, y)``

   Cette fonction décide comment les servos doivent se déplacer en fonction de la position de l'objet détecté.

   - Si aucun objet n'est détecté (``x`` ou ``y`` est ``None``), elle retourne ``(0, 0)`` (aucun mouvement).
   - Si l'objet est en dehors de la zone morte, elle retourne un petit pas de mouvement :

     - Objet à gauche  → ``pan_move = +MOVE_STEP``
     - Objet à droite → ``pan_move = -MOVE_STEP``
     - Objet en haut   → ``tilt_move = -MOVE_STEP``
     - Objet en bas    → ``tilt_move = +MOVE_STEP``

   La zone morte empêche la caméra de trembler lorsque l'objet est déjà près du centre.

#. ``update_servo_position(pan_move, tilt_move)``

   Cette fonction met à jour les angles des servos panoramique/inclinaison en toute sécurité.

   - Ajoute le pas de mouvement aux angles actuels des servos.
   - Limite les angles aux limites de sécurité (``PAN_MIN/PAN_MAX`` et ``TILT_MIN/TILT_MAX``).
   - Envoie les commandes aux servos uniquement lorsque l'angle change réellement.

   Cela protège le matériel contre la sur-rotation.

#. ``find_red_object(frame)``

   Cette fonction détecte le plus grand objet rouge dans l'image de la caméra.

   Étapes principales :

   - Convertit l'image de BGR vers HSV.
   - Crée un masque binaire pour les pixels rouges en utilisant deux plages HSV.
   - Nettoie le masque à l'aide de la morphologie (OPEN + CLOSE).
   - Trouve les contours et sélectionne le plus grand.
   - Filtre les petites taches avec ``MIN_CONTOUR_AREA``.
   - Utilise les moments d'image pour calculer le centre de l'objet.

   Elle retourne :

   - ``center_x, center_y`` : la position du centre de l'objet (ou ``None, None``)
   - ``mask`` : le masque binaire montrant les zones rouges

#. ``draw_debug_info(frame, object_x, object_y, mask, pan_angle, tilt_angle)``

   Cette fonction dessine des informations de suivi utiles sur l'image vidéo, notamment :

   - Croix de centrage
   - Rectangle de zone morte
   - Position de l'objet détecté
   - Angles des servos (panoramique et inclinaison)
   - Mode de suivi et taille de pas
   - Instructions clés

   Cela permet de voir facilement comment le traqueur fonctionne.

#. ``cleanup()``

   Cette fonction arrête le système en toute sécurité avant de quitter.

   - Ramène les servos à la position centrale.
   - Arrête la caméra.
   - Ferme toutes les fenêtres OpenCV.

   Cela empêche la caméra de rester dans une position étrange.

#. ``main()``

   C'est la boucle principale de suivi.

   Chaque itération effectue :

   - Capturer une image de la caméra.
   - Détecter l'objet rouge.
   - Décider comment déplacer les servos.
   - Mettre à jour les angles des servos.
   - Dessiner les informations de débogage.
   - Afficher la fenêtre de résultat.

   Elle supporte également les contrôles en cours d'exécution :

   - ``q`` pour quitter
   - ``r`` pour réinitialiser les servos
   - ``+`` / ``-`` pour ajuster la vitesse de suivi

   Le programme appelle toujours ``cleanup()`` dans le bloc ``finally`` pour garantir un arrêt sûr.


6. Paramètres Clés et Réglage
----------------------------

#. Paramètres de Détection des Couleurs

   .. code-block:: python

      # HSV thresholds for red detection
      LOWER_RED1 = np.array([0, 100, 80])     # [Hue, Saturation, Value]
      UPPER_RED1 = np.array([10, 255, 255])
      LOWER_RED2 = np.array([170, 100, 80])
      UPPER_RED2 = np.array([180, 255, 255])

      # Minimum object size
      MIN_CONTOUR_AREA = 500

   Conseils de réglage :

   - Ajustez les valeurs de Teinte pour différentes couleurs
   - Augmentez les minimums de Saturation/Valeur dans les environnements lumineux
   - Ajustez ``MIN_CONTOUR_AREA`` en fonction de la taille attendue de l'objet

#. Paramètres de Suivi

   .. code-block:: python

      # Deadzone size (pixels)
      DEADZONE_X = 50    # Larger = less jitter, but less precision
      DEADZONE_Y = 50

      # Movement step size (degrees)
      MOVE_STEP = 2      # Larger = faster tracking, but may overshoot

   Conseils de réglage :

   - Commencez avec une zone morte plus grande (50-100 px) pour un fonctionnement stable
   - Ajustez MOVE_STEP en fonction des besoins de suivi (0,5-5°)
   - Utilisez les touches '+' et '-' pour ajuster la vitesse pendant l'exécution

#. Paramètres des Servos

   .. code-block:: python

      # Servo limits (calibrate for your hardware)
      PAN_MIN = -90   # Maximum left
      PAN_MAX = 90    # Maximum right
      TILT_MIN = -45  # Maximum down
      TILT_MAX = 45   # Maximum up

   .. note:: Calibrez ces valeurs pour votre matériel spécifique afin d'éviter tout dommage.


7. Problèmes Courants et Dépannage
------------------------------------

* Le servo ne bouge pas

  - **Cause** : L'objet est dans la zone morte ou MIN_CONTOUR_AREA est trop élevé
  - **Solution** : Vérifiez la position de l'objet, réduisez MIN_CONTOUR_AREA ou diminuez la zone morte

* Mouvement du servo trop lent

  - **Cause** : MOVE_STEP trop petit
  - **Solution** : Appuyez sur la touche '+' pour augmenter la vitesse de déplacement

* Mouvement du servo trop saccadé

  - **Cause** : MOVE_STEP trop grand
  - **Solution** : Appuyez sur la touche '-' pour diminuer la vitesse de déplacement

* Fausse détection d'objet

  - **Cause** : Seuils HSV trop larges ou problèmes d'éclairage
  - **Solution** : Ajustez les plages HSV, améliorez l'éclairage, augmentez MIN_CONTOUR_AREA

* Faible FPS (moins de 10 FPS)

  - **Cause** : Surcharge de traitement ou paramètres de la caméra
  - **Solution** : Réduisez la résolution de l'image, simplifiez le dessin de débogage

8. Extensions et Fonctionnalités Avancées
------------------------------------

#. Suivi d'Objets Multiples

   .. code-block:: python

      # Instead of taking the largest contour:
      for contour in contours:
          if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
              # Track multiple objects

#. Retour au Contrôle Proportionnel

   .. code-block:: python

      # Re-implement proportional control if desired
      KP_PAN = 0.3
      pan_move = -x_error * KP_PAN / CENTER_X

#. Ajustement de la Vitesse Basé sur la Taille de l'Objet

   .. code-block:: python

      # Adjust movement speed based on object size
      object_size = cv2.contourArea(largest_contour)
      if object_size > 1000:  # Large object
          adjusted_step = MOVE_STEP * 0.5  # Move slower
      else:  # Small object
          adjusted_step = MOVE_STEP * 1.5  # Move faster

#. Journalisation et Enregistrement des Données

   .. code-block:: python

      # Record tracking data for analysis
      with open('tracking_log.csv', 'a') as f:
          f.write(f"{time.time()},{obj_x},{obj_y},{pan_angle},{tilt_angle}\n")

#. Diffusion en Réseau

   .. code-block:: python

      # Stream video over network
      import socket
      # Add network streaming code


9. Résultats d'Apprentissage
---------------------

Après avoir terminé ce projet, vous devriez comprendre :

1. **Vision par ordinateur** : Détection de couleur en temps réel et suivi d'objets
2. **Systèmes de contrôle** : Implémentation d'un algorithme de suivi simple à 4 directions
3. **Intégration matérielle** : Interface entre caméras et servos avec le Raspberry Pi
4. **Contrôle interactif** : Ajustement des paramètres en temps réel pendant le fonctionnement
5. **Conception système** : Architecture simplifiée d'un système de suivi

Ce projet fournit une base pour des applications plus avancées comme le suivi de visage, la navigation autonome et les systèmes d'automatisation industrielle. L'approche simplifiée à 4 directions le rend plus facile à comprendre et à modifier pour différentes applications.