.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_tts:

12. Ajout de la Synthèse Vocale TTS aux Projets MediaPipe
=============================================================

-----------------------------------------------------------------
1. Aperçu
-----------------------------------------------------------------

Dans :ref:`mp_hand_count` (Section 5), nous avons construit un programme
de comptage de gestes de la main qui affiche le nombre de doigts levés à l'écran.

Dans cette section, nous allons aller plus loin :
**ajouter la synthèse vocale (Text-to-Speech - TTS)**
pour que le Raspberry Pi puisse *prononcer* à voix haute le nombre de doigts détecté —
rendant le projet plus interactif et accessible.

.. image:: img/mp_hand_count.png
   :align: center

Cette leçon ne concerne pas seulement le comptage de doigts —
elle enseigne un **schéma général** pour ajouter la TTS à *n'importe quel*
projet MediaPipe ou OpenCV.

À la fin de cette leçon, vous saurez comment :

- Initialiser et configurer le moteur TTS de Fusion HAT+
- Déclencher la TTS sur une pression de touche avec protection anti-rebond
- Ajouter un retour visuel pendant que le système parle
- Appliquer ce schéma à vos propres projets de vision par ordinateur


-----------------------------------------------------------------
2. Comment ça Fonctionne
-----------------------------------------------------------------

Le programme s'appuie sur le pipeline de comptage des mains et ajoute une couche TTS
qui est activée par une pression de touche :

1. Initialiser **MediaPipe Hands** pour la détection de la main en temps réel.
2. Initialiser le **moteur TTS de Fusion HAT+** (Espeak).
3. Capturer des images vidéo et détecter les doigts (comme avant).
4. Attendre que l'utilisateur appuie sur la touche ``t``.
5. Sur pression de touche, convertir le nombre actuel de doigts en un message parlé.
6. Utiliser une **logique anti-rebond** pour éviter les déclenchements rapides répétés.
7. Afficher un **flash visuel** à l'écran pendant que la TTS parle.
8. La parole est émise via le haut-parleur Fusion HAT+.

L'idée de conception clé est :

    *La TTS est ajoutée comme une couche non bloquante —*
    la détection s'exécute en continu, et la parole n'est déclenchée
    que lorsque l'utilisateur le demande.

Ce schéma maintient le pipeline vidéo fluide tout en ajoutant
une sortie vocale à la demande.


-----------------------------------------------------------------
3. Le Module TTS Fusion HAT+
-----------------------------------------------------------------

La bibliothèque ``fusion_hat`` fournit une interface simple et unifiée
pour plusieurs moteurs TTS. Dans ce projet, nous utilisons **Espeak** —
un moteur hors ligne léger qui fonctionne bien sur Raspberry Pi.

**Utilisation de base :**

.. code-block:: python

    from fusion_hat.tts import Espeak

    # Create TTS instance
    tts = Espeak()

    # Configure voice
    tts.set_amp(200)       # volume: 0-200 (default 100)
    tts.set_speed(150)     # speed: 80-260 (default 150)
    tts.set_pitch(80)      # pitch: 0-99 (default 80)

    # Speak
    tts.say("Hello!")

Trois paramètres permettent de personnaliser la voix :

- **amp** (amplitude) — contrôle le volume. Plus élevé = plus fort.
- **speed** — vitesse de parole en mots par minute. 150 est normal.
- **pitch** — hauteur de la voix. 80 est la valeur par défaut ; des valeurs plus basses donnent un son plus grave.

.. note::

   Fusion HAT+ supporte également **Piper** (neural, hors ligne)
   et **OpenAI TTS** (en ligne, voix naturelles).
   Voir :ref:`tts_piper_openai` pour des options plus avancées.


-----------------------------------------------------------------
4. Conception Clé : Ajouter la TTS à une Boucle Vidéo
-----------------------------------------------------------------

Lors de l'ajout de la TTS à un pipeline vidéo en temps réel, il y a quelques
considérations de conception importantes. Examinons chacune d'elles.

--------------------------------------------------
4.1 Déclenchement par Pression de Touche
--------------------------------------------------

Plutôt que de parler à chaque image (ce qui serait chaotique),
nous utilisons une touche du clavier comme déclencheur :

.. code-block:: python

    key = cv2.waitKey(1) & 0xff
    if key == ord('t'):
        tts.say(message)

La touche ``t`` est choisie car elle est facile à retenir
(*t* pour *talk*). Vous pouvez utiliser n'importe quelle touche — ``space`` pour
un contrôle mains libres au sol, ou un bouton GPIO pour une entrée physique.

--------------------------------------------------
4.2 Protection Anti-Rebond
--------------------------------------------------

Sans protection, maintenir la touche ``t`` enfoncée déclencherait
la TTS des dizaines de fois par seconde, avec des chevauchements de parole
la rendant incompréhensible.

**Solution : anti-rebond basé sur le temps.**

.. code-block:: python

    DEBOUNCE_INTERVAL = 1.5  # seconds
    last_tts_time = 0

    # In the loop:
    if key == ord('t'):
        now = time.time()
        if now - last_tts_time > DEBOUNCE_INTERVAL:
            last_tts_time = now
            tts.say(message)

Après chaque déclenchement TTS, les déclenchements suivants sont ignorés
pendant 1,5 seconde. Cela donne suffisamment de temps à la parole pour se terminer
avant que la suivante ne commence.

--------------------------------------------------
4.3 Construction du Message
--------------------------------------------------

Le nombre de doigts (un entier) doit être converti en
une phrase naturelle :

.. code-block:: python

    if total_fingers == 0:
        message = "no fingers detected"
    elif total_fingers == 1:
        message = "one finger detected"
    else:
        message = f"{total_fingers} fingers detected"

--------------------------------------------------
4.4 Retour Visuel (Flash de Bordure Verte)
--------------------------------------------------

Pendant que le système parle, nous ajoutons un indicateur visuel
pour que l'utilisateur sache que la parole est en cours :

.. code-block:: python

    tts_flash_until = now + 1.0   # flash for 1 second

    # Later in the loop:
    if tts_triggered and time.time() < tts_flash_until:
        cv2.rectangle(frame, (0, 0), (w-1, h-1), (0, 255, 0), 8)
        cv2.putText(frame, "Speaking...", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

Une **bordure verte** apparaît autour de l'image et une
étiquette **« Speaking...»** est affichée. Les deux disparaissent automatiquement
après 1 seconde.


-----------------------------------------------------------------
5. Exécuter le Code
-----------------------------------------------------------------

.. important::

   Avant de commencer, assurez-vous :

   * Que Fusion HAT+ est assemblé et que le haut-parleur est connecté
   * Que vous pouvez accéder au bureau du Raspberry Pi
   * Que le package de code est installé
   * Que MediaPipe et OpenCV sont installés

   Pour les instructions détaillées, voir :ref:`mediapipe_install` et :ref:`opencv_install`.

#. Ouvrez le terminal et entrez la commande suivante :

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts.py

#. Après avoir exécuté le programme :

   - Une fenêtre intitulée « MediaPipe Hand Count + TTS » s'ouvre,
     montrant le flux en direct de la caméra.
   - Levez la main devant la caméra — le nombre de doigts apparaît
     dans le coin supérieur gauche.
   - *Appuyez sur la touche* ``t`` — le système prononce le nombre
     de doigts actuel via le haut-parleur Fusion HAT+.
   - Une bordure verte clignote à l'écran pendant la parole.

   Appuyez sur ``q`` pour quitter le programme.


--------------------------------------------------
6. Code Complet
--------------------------------------------------

.. code-block:: python

   """
   MediaPipe Hand Detection + TTS Demo
   ====================================
   Detects fingers via webcam in real time. Press the 't' key to speak the
   current finger count using TTS.

   Usage:
       python mp_hand_count_tts.py

   Controls:
       't'  - speak the detected finger count via TTS
       'q'  - quit
   """

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   from fusion_hat.tts import Espeak
   import time


   # ======================== Init TTS ========================
   tts = Espeak()
   tts.set_amp(200)       # volume 0-200, default 100
   tts.set_speed(150)     # speed 80-260, default 150
   tts.set_pitch(80)      # pitch 0-99, default 80

   # ======================== Init MediaPipe Hands ========================
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5
   )

   # ======================== Init Camera ========================
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   # ======================== Constants ========================
   # Finger tip and dip landmark indices
   FINGER_TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
   FINGER_DIPS = [2, 6, 10, 14, 18]   # corresponding middle joints

   # Minimum interval (seconds) between TTS triggers to avoid spamming
   DEBOUNCE_INTERVAL = 1.5

   print("=" * 55)
   print("  MediaPipe Hand Count + TTS")
   print("  Press 't' to speak count | 'q' to quit")
   print("=" * 55)

   # ======================== Main Loop ========================
   last_tts_time = 0          # timestamp of last TTS trigger
   tts_triggered = False      # whether TTS was just fired (for visual flash)
   tts_flash_until = 0        # how long the flash should last

   while True:
       # ---- 1. Capture frame ----
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # ---- 2. Convert to RGB for MediaPipe ----
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       # ---- 3. Convert back to BGR for OpenCV display ----
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # ---- 4. Count fingers (right hand only) ----
       total_fingers = 0

       if hands_detected.multi_hand_landmarks:
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               # Draw hand skeleton
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

               landmarks = hand_landmarks.landmark
               finger_count = 0

               # Thumb: extended when x_tip > x_dip (right hand)
               if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
                   finger_count += 1

               # Other four fingers: tip is above dip when extended (smaller y)
               for i in range(1, 5):
                   if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
                       finger_count += 1

               total_fingers += finger_count

       # ---- 5. Display finger count on screen ----
       display_text = f"Fingers: {total_fingers}"
       cv2.putText(frame, display_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

       # ---- 6. Key handling ----
       key = cv2.waitKey(1) & 0xff

       # 't' key: trigger TTS (with debounce)
       if key == ord('t'):
           now = time.time()
           if now - last_tts_time > DEBOUNCE_INTERVAL:
               last_tts_time = now
               tts_triggered = True
               tts_flash_until = now + 1.0  # flash for 1 second

               if total_fingers == 0:
                   message = "no fingers detected"
               elif total_fingers == 1:
                   message = "one finger detected"
               else:
                   message = f"{total_fingers} fingers detected"

               print(f"[TTS] {message}")
               tts.say(message)

       # 'q' key: quit
       if key == ord('q'):
           break

       # ---- 7. Visual feedback while speaking (green border flash) ----
       if tts_triggered and time.time() < tts_flash_until:
           h, w = frame.shape[:2]
           thickness = 8
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 255, 0), thickness)
           cv2.putText(frame, "Speaking...", (10, 75),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
       else:
           tts_triggered = False

       # ---- 8. Show controls hint at bottom ----
       cv2.putText(frame, "Press 't' to speak count | 'q' to quit",
                   (10, frame.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

       # ---- 9. Show frame ----
       cv2.imshow("MediaPipe Hand Count + TTS", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")


--------------------------------------------------
7. Explication du Code
--------------------------------------------------

Le modèle d'intégration TTS que vous avez appris ici est **générique**.
Vous pouvez ajouter la diffusion vocale à n'importe quel projet MediaPipe, OpenCV ou YOLO
en suivant ces étapes :

**Étape 1 : Importer et initialiser la TTS**

.. code-block:: python

   from fusion_hat.tts import Espeak
   tts = Espeak()
   tts.set_amp(200)

**Étape 2 : Ajouter des variables anti-rebond (avant la boucle)**

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5
   last_tts_time = 0

**Étape 3 : Ajouter la TTS déclenchée par touche (dans la boucle)**

.. code-block:: python

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           tts.say(your_message)


-----------------------------------------------------------------
8. Dépannage
-----------------------------------------------------------------

- **Aucun son du haut-parleur**

  Assurez-vous que le haut-parleur Fusion HAT+ est correctement connecté et
  que le volume n'est pas coupé. Essayez d'exécuter un simple test TTS :

  .. code-block:: bash

     sudo python3 -c "from fusion_hat.tts import Espeak; Espeak().say('test')"

  Si vous entendez « test », le moteur TTS fonctionne.

- **La TTS se déclenche trop de fois en maintenant la touche**

  Augmentez ``DEBOUNCE_INTERVAL`` à une valeur plus grande,
  par exemple ``2.0`` ou ``2.5`` secondes.

- **La parole semble trop rapide ou peu claire**

  Réduisez la vitesse : ``tts.set_speed(120)``.
  Ajustez la hauteur pour plus de clarté : ``tts.set_pitch(70)``.


-----------------------------------------------------------------
9. Résumé
-----------------------------------------------------------------

- Cette leçon a démontré comment **ajouter la diffusion vocale TTS**
  à un projet de vision par ordinateur MediaPipe.
- Le moteur ``Espeak`` de Fusion HAT+ fournit une solution TTS simple
  et hors ligne sur Raspberry Pi.
- **Schémas de conception clés** abordés :

  - Déclenchement de la TTS par pression de touche (pas à chaque image)
  - **Protection anti-rebond** pour éviter le chevauchement de la parole
  - **Retour visuel** (flash de bordure verte) pour la sensibilisation de l'utilisateur
  - Conversion des résultats de détection en messages parlés naturels

- Ces schémas sont **indépendants du projet** — vous pouvez les appliquer
  à n'importe quel projet OpenCV, MediaPipe ou YOLO pour ajouter une sortie vocale.