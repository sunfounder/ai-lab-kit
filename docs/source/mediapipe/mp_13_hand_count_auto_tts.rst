.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_auto_tts:

13. TTS Automatique sans Contact — Diffusion Vocale Mains Libres
==================================================================

-----------------------------------------------------------------
1. Aperçu
-----------------------------------------------------------------

Dans :ref:`mp_hand_count_tts` (Section 12), nous avons construit un programme
de comptage de gestes de la main où l'utilisateur appuie sur la touche ``t`` pour déclencher
une diffusion vocale TTS.

Dans cette section, nous franchissons une nouvelle étape : **supprimer complètement le clavier.**
Le système détecte désormais *automatiquement* lorsque vous maintenez un geste de la main
stable et prononce le nombre de doigts — sans touches, sans boutons,
complètement sans contact.

.. image:: img/mp_hand_count.png
   :align: center

Cette leçon introduit un **schéma de machine à états** pour l'interaction
sans contact — une technique que vous pouvez appliquer aux projets d'accessibilité,
aux installations mains libres et à tout scénario où la saisie au clavier
n'est pas pratique.

À la fin de cette leçon, vous saurez comment :

- Concevoir une machine à états pour le suivi de la présence de la main
- Détecter la *stabilité* d'un geste sur plusieurs images
- Utiliser une temporisation de maintien pour éviter les faux déclenchements
- Détecter automatiquement quand une main entre ou quitte le cadre
- Fournir un retour visuel multi-étapes (inactif → détecté → stable → parole)
- Afficher une barre de progression pour le compte à rebours de la temporisation


-----------------------------------------------------------------
2. Comment ça Fonctionne
-----------------------------------------------------------------

Le programme remplace le déclencheur clavier par un **déclencheur automatique
basé sur la stabilité**. Voici le pipeline :

1. Initialiser **MediaPipe Hands** pour la détection de la main en temps réel.
2. Initialiser le **moteur TTS de Fusion HAT+** (Espeak).
3. Capturer des images vidéo et détecter les doigts (comme avant).
4. Alimenter le **détecteur de stabilité** avec le nombre de doigts — une fenêtre
   glissante qui vérifie si le nombre est resté le même
   sur plusieurs images consécutives.
5. Une fois le nombre confirmé stable, démarrer une **temporisation de maintien**.
6. Si l'utilisateur maintient le même geste pendant 2,5 secondes, la TTS se déclenche
   automatiquement.
7. Si la main quitte le cadre, le système prononce « hand left the frame »
   après un court délai.
8. Une **barre de progression** et une **bordure multicolore** montrent l'état
   actuel en un coup d'œil.

L'idée de conception clé est :

    *La main stable de l'utilisateur remplace le clavier —*
    le système surveille l'*intention* (rester immobile) plutôt que
    de réagir à chaque geste fugace.

Ceci rend le projet entièrement mains libres et accessible — idéal pour
les technologies d'assistance, les expositions interactives ou les situations où
l'utilisateur ne peut pas atteindre un clavier.


-----------------------------------------------------------------
3. Concepts de Conception Clés
-----------------------------------------------------------------

**3.1 Machine à États pour le Suivi de la Main**

Le programme suit la présence de la main comme un **état**, pas seulement une
valeur par image. Une classe ``HandTrackingState`` encapsule
toutes les variables d'état.

**3.2 Détection de Stabilité**

Un comptage de doigts sur une seule image n'est pas fiable — le nombre peut
varier à cause du bruit de la caméra ou d'un léger mouvement de la main. Pour éviter
les faux déclenchements, nous utilisons une **fenêtre glissante** des comptages récents.

**3.3 Déclenchement Automatique avec Temporisation de Maintien**

La stabilité seule ne suffit pas — l'utilisateur doit *maintenir* le geste
assez longtemps pour démontrer son intention. Trois barrières protègent contre
les faux déclenchements :

1. **Intervalle minimum** — au moins 4 secondes entre deux événements TTS.
2. **Durée de maintien** — le geste doit être maintenu stable pendant 2,5 secondes.
3. **Protection de répétition** — le même comptage ne sera pas prononcé à nouveau avant 8 secondes.

**3.4 Détection de Sortie de la Main**

Lorsque l'utilisateur retire sa main de la caméra, le système détecte
et prononce une notification.

-----------------------------------------------------------------
4. Exécuter le Code
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts_without_tap.py

#. Après avoir exécuté le programme :

   - Une fenêtre intitulée « MediaPipe Hand Detection + AUTO TTS (Touchless Mode) » s'ouvre,
     montrant le flux en direct de la caméra.
   - Levez la main devant la caméra — le nombre de doigts apparaît
     dans le coin supérieur gauche.
   - *Gardez votre main immobile* — regardez la bordure passer du gris
     au cyan puis au vert, et la barre de progression se remplir.
   - Après 2,5 secondes de maintien du même geste, le système
     prononce automatiquement le nombre de doigts.
   - Retirez votre main de la caméra — après un moment, le système
     dit « hand left the frame ».

   Appuyez sur ``q`` pour quitter le programme.

-----------------------------------------------------------------
5. Code Complet
-----------------------------------------------------------------

.. code-block:: python

   """
   MediaPipe Hand Detection + Auto TTS (Touchless Mode)
   ====================================================
   Detects fingers via webcam in real time. Automatically speaks the finger count
   when a stable hand gesture is maintained for a certain duration.

   No keyboard input required for triggering TTS.

   Usage:
       python mp_hand_count_auto_tts.py

   Controls:
       'q'  - quit
   """

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   from fusion_hat.tts import Espeak
   import time
   from collections import deque


   # ======================== Init TTS ========================
   tts = Espeak()
   tts.set_amp(200)       # volume 0-200, default 100
   tts.set_speed(150)     # speed 80-260, default 150
   tts.set_pitch(80)      # pitch 0-99, default 80

   # ======================== Init MediaPipe Hands ========================
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5,
       min_tracking_confidence=0.5
   )

   # ======================== Init Camera ========================
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   # ======================== Constants ========================
   FINGER_TIPS = [4, 8, 12, 16, 20]
   FINGER_DIPS = [2, 6, 10, 14, 18]

   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable before speaking
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves
   NO_HAND_COOLDOWN = 5.0          # seconds without hand before suppressing repeats
   FRAME_HISTORY_SIZE = 10         # for stability detection

   COLOR_IDLE = (128, 128, 128)    # gray
   COLOR_DETECTED = (255, 255, 0)  # cyan
   COLOR_STABLE = (0, 255, 0)      # green
   COLOR_SPEAKING = (0, 255, 0)    # bright green

   print("=" * 60)
   print("  MediaPipe Hand Detection + AUTO TTS (Touchless Mode)")
   print("  No keyboard needed - just show a stable hand gesture")
   print("  Press 'q' to quit")
   print("=" * 60)

   # ======================== State Management ========================
   class HandTrackingState:
       def __init__(self):
           self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
           self.current_fingers = 0
           self.stable_fingers = -1
           self.stable_start_time = 0
           self.is_stable = False
           self.hand_present = False
           self.hand_absent_start_time = 0
           self.last_tts_time = 0
           self.last_tts_message = ""
           self.last_no_hand_tts_time = 0

   state = HandTrackingState()

   def get_finger_count(hand_landmarks):
       """Count fingers for a single hand (right hand logic)"""
       landmarks = hand_landmarks.landmark
       finger_count = 0

       # Thumb: extended when x_tip > x_dip (right hand)
       if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
           finger_count += 1

       # Other four fingers: tip is above dip when extended (smaller y)
       for i in range(1, 5):
           if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
               finger_count += 1

       return finger_count

   def update_stability(new_count):
       """Update stability state based on finger count history"""
       state.finger_history.append(new_count)

       if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
           recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
           if all(c == new_count for c in recent_counts):
               if not state.is_stable or state.current_fingers != new_count:
                   state.is_stable = True
                   state.stable_start_time = time.time()
                   state.current_fingers = new_count
                   return True
       else:
           state.is_stable = False

       state.current_fingers = new_count
       return False

   def should_trigger_tts():
       """Check if conditions are met for auto TTS"""
       now = time.time()

       if now - state.last_tts_time < MIN_TTS_INTERVAL:
           return False

       if not state.hand_present or not state.is_stable:
           return False

       hold_time = now - state.stable_start_time
       if hold_time < HOLD_DURATION_REQUIRED:
           return False

       if state.stable_fingers == state.current_fingers:
           if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
               return False

       return True

   def trigger_tts():
       """Execute TTS for current finger count"""
       now = time.time()
       count = state.current_fingers

       if count == 0:
           message = "no fingers detected"
       elif count == 1:
           message = "one finger detected"
       else:
           message = f"{count} fingers detected"

       if message == state.last_tts_message and now - state.last_tts_time < 3.0:
           return False

       print(f"[TTS] {message} (held for {HOLD_DURATION_REQUIRED}s)")
       tts.say(message)

       state.last_tts_time = now
       state.last_tts_message = message
       state.stable_fingers = count

       return True

   def trigger_hand_exit_tts():
       """Say hand has left the frame"""
       now = time.time()
       if now - state.last_tts_time >= MIN_TTS_INTERVAL:
           print("[TTS] hand left the frame")
           tts.say("hand left the frame")
           state.last_tts_time = now
           state.last_tts_message = "hand left"

   def get_border_color():
       """Determine border color based on current state"""
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

   # ======================== Main Loop ========================
   frame_count = 0
   speaking_flash_until = 0

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       total_fingers = 0
       has_hand = False

       if hands_detected.multi_hand_landmarks:
           has_hand = True
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )
               finger_count = get_finger_count(hand_landmarks)
               total_fingers = max(total_fingers, finger_count)

       # ---- Update state machine ----
       now = time.time()

       if has_hand:
           if not state.hand_present:
               state.hand_present = True
               state.is_stable = False
               state.finger_history.clear()
               print("[INFO] Hand detected")
           state.hand_absent_start_time = now
       else:
           if state.hand_present:
               state.hand_present = False
               state.is_stable = False
               state.stable_fingers = -1
               state.finger_history.clear()
               if now - state.last_tts_time >= MIN_TTS_INTERVAL:
                   trigger_hand_exit_tts()

       if has_hand:
           update_stability(total_fingers)
           if should_trigger_tts():
               if trigger_tts():
                   speaking_flash_until = now + 0.8
                   state.speaking_until = speaking_flash_until

       # ---- Display information ----
       cv2.putText(frame, f"Fingers: {total_fingers}", (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

       if not has_hand:
           status_text = "Status: No hand detected"
           status_color = (128, 128, 128)
       elif state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               remaining = HOLD_DURATION_REQUIRED - (now - state.stable_start_time)
               status_text = f"Status: Hold gesture ({remaining:.1f}s to speak)"
               status_color = (255, 255, 0)
           else:
               status_text = "Status: Ready to speak!"
               status_color = (0, 255, 0)
       else:
           status_text = "Status: Detecting... keep hand still"
           status_color = (0, 200, 200)

       cv2.putText(frame, status_text, (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

       # ---- Visual border feedback ----
       h, w = frame.shape[:2]
       thickness = 6

       if now < speaking_flash_until:
           border_color = (0, 255, 0)
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)
           cv2.putText(frame, "SPEAKING...", (w - 180, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
       else:
           border_color = get_border_color()
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)

       # ---- Progress bar ----
       if has_hand and state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           bar_width = int(w * 0.4)
           bar_height = 8
           bar_x = w - bar_width - 10
           bar_y = 10
           filled_width = int(bar_width * hold_progress)
           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                        (60, 60, 60), -1)
           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                        (0, 255, 0), -1)

       # ---- Key handling ----
       key = cv2.waitKey(1) & 0xff
       if key == ord('q'):
           break

       cv2.imshow("MediaPipe Hand Detection + AUTO TTS (Touchless Mode)", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")

-----------------------------------------------------------------
6. Résumé
-----------------------------------------------------------------

- Cette leçon a démontré comment **supprimer le déclencheur clavier**
  et construire un système TTS entièrement sans contact.
- Le projet utilise une **machine à états** (classe ``HandTrackingState``)
  pour suivre la présence de la main, la stabilité du geste et la temporisation TTS.
- **Schémas de conception clés** abordés :

  - **Détection de stabilité** — fenêtre glissante des comptages de doigts
    pour confirmer que l'utilisateur maintient un geste stable
  - **Temporisation de maintien** — exiger 2,5 secondes de stabilité
    avant de déclencher la TTS, remplaçant la pression de touche par l'*intention*
  - **Détection automatique de sortie** — prononcer « hand left the frame »
    lorsque la main disparaît
  - **Retour visuel multi-étapes** — bordure colorée
    (gris → cyan → vert) plus une barre de progression pour l'état
    en temps réel

- Ces schémas sont **indépendants du projet** — vous pouvez appliquer
  l'approche machine à états + détection de stabilité à n'importe quel
  projet de vision par ordinateur nécessitant une interaction sans contact.