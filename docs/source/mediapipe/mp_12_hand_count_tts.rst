.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_tts:

12. TTS-Sprachausgabe zu MediaPipe-Projekten hinzufügen
========================================================

-----------------------------------------------------------------
1. Übersicht
-----------------------------------------------------------------

In :ref:`mp_hand_count` (Abschnitt 5) haben wir ein Programm zur
Handgesten-Zählung erstellt, das die Anzahl der erhobenen Finger
auf dem Bildschirm anzeigt.

In diesem Abschnitt gehen wir einen Schritt weiter:
**Text-to-Speech (TTS) Sprachausgabe hinzufügen**,
sodass der Raspberry Pi die erkannte Fingeranzahl *aussprechen* kann —
das macht das Projekt interaktiver und zugänglicher.

.. image:: img/mp_hand_count.png
   :align: center

Diese Lektion behandelt nicht nur das Fingerzählen —
sie vermittelt ein **allgemeines Muster**, um TTS zu *jedem*
MediaPipe- oder OpenCV-Projekt hinzuzufügen.

Am Ende dieser Lektion wissen Sie, wie man:

- Die Fusion HAT+ TTS-Engine initialisiert und konfiguriert
- TTS per Tastendruck mit Entprellschutz auslöst
- Visuelles Feedback hinzufügt, während das System spricht
- Dieses Muster auf eigene Computer-Vision-Projekte anwendet


-----------------------------------------------------------------
2. Funktionsweise
-----------------------------------------------------------------

Das Programm baut auf der Handzähl-Pipeline auf und fügt eine
TTS-Schicht hinzu, die per Tastendruck aktiviert wird:

1. **MediaPipe Hands** für die Echtzeit-Handerkennung initialisieren.
2. Die **Fusion HAT+ TTS-Engine** (Espeak) initialisieren.
3. Videobilder erfassen und Finger erkennen (wie zuvor).
4. Warten, bis der Benutzer die ``t``-Taste drückt.
5. Beim Tastendruck die aktuelle Fingeranzahl in eine gesprochene
   Nachricht umwandeln.
6. **Entprelllogik** verwenden, um schnelle Wiederholungen zu vermeiden.
7. Einen **visuellen Blitz** auf dem Bildschirm anzeigen, während
   TTS spricht.
8. Die Sprachausgabe erfolgt über den Fusion HAT+ Lautsprecher.

Das zentrale Designprinzip ist:

    *TTS wird als nicht-blockierende Schicht hinzugefügt —*
    die Erkennung läuft kontinuierlich, und die Sprachausgabe wird nur
    dann ausgelöst, wenn der Benutzer sie anfordert.

Dieses Muster hält die Video-Pipeline flüssig und fügt bei Bedarf
Sprachausgabe hinzu.


-----------------------------------------------------------------
3. Das Fusion HAT+ TTS-Modul
-----------------------------------------------------------------

Die ``fusion_hat``-Bibliothek bietet eine einfache, einheitliche
Schnittstelle für mehrere TTS-Engines. In diesem Projekt verwenden
wir **Espeak** — eine leichte Offline-Engine, die gut auf dem
Raspberry Pi funktioniert.

**Grundlegende Verwendung:**

.. code-block:: python

    from fusion_hat.tts import Espeak

    # TTS-Instanz erstellen
    tts = Espeak()

    # Stimme konfigurieren
    tts.set_amp(200)       # Lautstärke: 0-200 (Standard 100)
    tts.set_speed(150)     # Geschwindigkeit: 80-260 (Standard 150)
    tts.set_pitch(80)      # Tonhöhe: 0-99 (Standard 80)

    # Sprechen
    tts.say("Hallo!")

Drei Parameter ermöglichen die Anpassung der Stimme:

- **amp** (Amplitude) — steuert die Lautstärke. Höher = lauter.
- **speed** — Sprechgeschwindigkeit in Wörtern pro Minute. 150 ist normal.
- **pitch** — Tonhöhe der Stimme. 80 ist der Standard; niedrigere Werte
  klingen tiefer.

.. note::

   Fusion HAT+ unterstützt auch **Piper** (neural, offline)
   und **OpenAI TTS** (online, natürliche Stimmen).
   Siehe :ref:`tts_piper_openai` für weitere Optionen.


-----------------------------------------------------------------
4. Schlüsseldesign: TTS in einer Video-Schleife
-----------------------------------------------------------------

Beim Hinzufügen von TTS zu einer Echtzeit-Video-Pipeline gibt es
einige wichtige Designüberlegungen. Gehen wir sie der Reihe nach durch.

--------------------------------------------------
4.1 Auslösung per Tastendruck
--------------------------------------------------

Anstatt bei jedem Frame zu sprechen (was chaotisch wäre),
verwenden wir eine Taste als Auslöser:

.. code-block:: python

    key = cv2.waitKey(1) & 0xff
    if key == ord('t'):
        tts.say(message)

Die ``t``-Taste ist leicht zu merken (*t* für *talk*).
Sie können jede beliebige Taste verwenden — ``Leertaste`` für
freihändige Bedienung oder einen GPIO-Taster für physische Eingabe.

--------------------------------------------------
4.2 Entprellschutz
--------------------------------------------------

Ohne Schutz würde das Gedrückthalten der ``t``-Taste TTS dutzende
Male pro Sekunde auslösen, was zu überlappender und unverständlicher
Sprachausgabe führt.

**Lösung: Zeitbasierte Entprellung.**

.. code-block:: python

    DEBOUNCE_INTERVAL = 1.5  # Sekunden
    last_tts_time = 0

    # In der Schleife:
    if key == ord('t'):
        now = time.time()
        if now - last_tts_time > DEBOUNCE_INTERVAL:
            last_tts_time = now
            tts.say(message)

Nach jeder TTS-Auslösung werden weitere Auslöser für 1,5 Sekunden
ignoriert. Dies gibt der Sprachausgabe genug Zeit, um zu enden,
bevor die nächste beginnt.

--------------------------------------------------
4.3 Die Nachricht zusammenstellen
--------------------------------------------------

Die Fingeranzahl (eine Ganzzahl) muss in einen natürlich klingenden
Satz umgewandelt werden:

.. code-block:: python

    if total_fingers == 0:
        message = "no fingers detected"
    elif total_fingers == 1:
        message = "one finger detected"
    else:
        message = f"{total_fingers} fingers detected"

Die Verwendung von ``"one"`` anstelle von ``"1"`` stellt sicher,
dass Espeak es natürlich ausspricht. Für Zahlen größer als eins
funktioniert die Ziffernform gut mit Espeak.

--------------------------------------------------
4.4 Visuelles Feedback (Grüner Rand-Blitz)
--------------------------------------------------

Während das System spricht, fügen wir eine visuelle Anzeige hinzu,
damit der Benutzer weiß, dass die Sprachausgabe läuft:

.. code-block:: python

    tts_flash_until = now + 1.0   # 1 Sekunde lang blinken

    # Später in der Schleife:
    if tts_triggered and time.time() < tts_flash_until:
        cv2.rectangle(frame, (0, 0), (w-1, h-1), (0, 255, 0), 8)
        cv2.putText(frame, "Speaking...", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

Ein **grüner Rand** erscheint um das Bild und eine
**"Speaking..."**-Beschriftung wird eingeblendet. Beide
verschwinden automatisch nach 1 Sekunde.

Diese Rückmeldung ist wichtig, weil:

- TTS einen Moment braucht — der Benutzer muss wissen,
  dass das System seinen Befehl gehört hat.
- Der Rand verschwindet, wenn die Ausgabe beendet ist,
  sodass er die normale Nutzung nicht stört.


-----------------------------------------------------------------
5. Code ausführen
-----------------------------------------------------------------

.. important::

   Stellen Sie vor dem Start sicher, dass:

   * Das Fusion HAT+ montiert und der Lautsprecher angeschlossen ist
   * Sie auf den Raspberry Pi Desktop zugreifen können
   * Das Code-Paket installiert ist
   * MediaPipe und OpenCV installiert sind

   Detaillierte Anweisungen finden Sie unter :ref:`mediapipe_install`
   und :ref:`opencv_install`.

#. Öffnen Sie das Terminal und geben Sie folgenden Befehl ein:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts.py

#. Nach dem Start des Programms:

   - Ein Fenster mit dem Titel „MediaPipe Hand Count + TTS" öffnet sich
     und zeigt das Live-Kamerabild.
   - Halten Sie Ihre Hand vor die Kamera — die Fingeranzahl erscheint
     in der oberen linken Ecke.
   - *Drücken Sie die* ``t``\ *-Taste* — das System spricht die aktuelle
     Fingeranzahl über den Fusion HAT+ Lautsprecher.
   - Ein grüner Rand blinkt während der Sprachausgabe auf dem Bildschirm.

   .. hint::

      Versuchen Sie, verschiedene Anzahlen von Fingern zu zeigen und
      jedes Mal ``t`` zu drücken. Sie sollten hören: „one finger detected",
      „three fingers detected" usw.

   Drücken Sie ``q``, um das Programm zu beenden.


--------------------------------------------------
6. Vollständiger Code
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
7. Code-Erklärung
--------------------------------------------------

Gehen wir den Code Abschnitt für Abschnitt durch, mit Fokus auf das,
was im Vergleich zum grundlegenden Handzähl-Programm neu ist.

--------------------------------------------------
7.1 Importe und Initialisierung
--------------------------------------------------

.. code-block:: python

   from fusion_hat.tts import Espeak
   import time

   tts = Espeak()
   tts.set_amp(200)
   tts.set_speed(150)
   tts.set_pitch(80)

Zwei neue Importe und ein TTS-Initialisierungsblock sind die ersten
Ergänzungen. ``Espeak()`` erstellt die TTS-Engine, und die drei
``set_*``-Aufrufe konfigurieren die Stimme.

Der ``import time`` wird für das Entprell-Timing benötigt.

--------------------------------------------------
7.2 Entprell-Konstanten und Zustandsvariablen
--------------------------------------------------

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5

   last_tts_time = 0
   tts_triggered = False
   tts_flash_until = 0

Vier neue Variablen werden eingeführt:

- ``DEBOUNCE_INTERVAL`` — verhindert TTS-Spam (Sekunden).
- ``last_tts_time`` — zeichnet auf, wann TTS zuletzt ausgelöst wurde.
- ``tts_triggered`` — Flag für den visuellen Blitz-Effekt.
- ``tts_flash_until`` — Zeitstempel, wann der Blitz enden soll.

--------------------------------------------------
7.3 Tastenbehandlung mit Entprellung
--------------------------------------------------

.. code-block:: python

   key = cv2.waitKey(1) & 0xff

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           tts_triggered = True
           tts_flash_until = now + 1.0

           if total_fingers == 0:
               message = "no fingers detected"
           elif total_fingers == 1:
               message = "one finger detected"
           else:
               message = f"{total_fingers} fingers detected"

           tts.say(message)

Dies ist die zentrale TTS-Ergänzung. Gehen wir sie Schritt für Schritt durch:

1. **Tastenerkennung** — ``ord('t')`` prüft, ob ``t`` gedrückt wurde.

2. **Entprellsperre** — ``time.time() - last_tts_time > DEBOUNCE_INTERVAL``
   stellt sicher, dass seit der letzten Auslösung mindestens 1,5 Sekunden
   vergangen sind. Wenn nicht genug Zeit vergangen ist, wird der
   Tastendruck ignoriert.

3. **Zustand aktualisieren** — Wenn die Sperre durchlässig ist, zeichnen
   wir die aktuelle Zeit auf und setzen den Blink-Timer.

4. **Nachricht erstellen** — Die Fingeranzahl wird in einen
   menschenlesbaren Satz umgewandelt.

5. **Sprechen** — ``tts.say(message)`` sendet den Text an den Lautsprecher.

.. note::

   ``tts.say()`` ist **nicht-blockierend** — das Programm verarbeitet
   weiterhin Videobilder, während die Sprachausgabe im Hintergrund läuft.

--------------------------------------------------
7.4 Visuelles Feedback
--------------------------------------------------

.. code-block:: python

   if tts_triggered and time.time() < tts_flash_until:
       h, w = frame.shape[:2]
       thickness = 8
       cv2.rectangle(frame, (0, 0), (w - 1, h - 1), (0, 255, 0), thickness)
       cv2.putText(frame, "Speaking...", (10, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
   else:
       tts_triggered = False

- Ein grüner Rand (8 Pixel dick) wird um das gesamte Bild gezeichnet.
- Eine gelbe „Speaking..."-Beschriftung erscheint unter der Fingeranzahl.
- Beide bleiben 1 Sekunde lang bestehen und verschwinden dann automatisch.
- Wenn der Blink-Timer abläuft, wird ``tts_triggered`` auf ``False``
  zurückgesetzt — bereit für die nächste Auslösung.

Dieses Muster ist wiederverwendbar — Sie können das gleiche Feedback
zu jedem Projekt hinzufügen, das TTS auslöst.


-----------------------------------------------------------------
8. Erweiterungsideen: Dieses Muster auf andere Projekte anwenden
-----------------------------------------------------------------

Das hier erlernte TTS-Integrationsmuster ist **generisch**.
Sie können Sprachausgabe zu jedem MediaPipe-, OpenCV- oder YOLO-Projekt
hinzufügen, indem Sie diesen Schritten folgen:

**Schritt 1: TTS importieren und initialisieren**

.. code-block:: python

   from fusion_hat.tts import Espeak
   tts = Espeak()
   tts.set_amp(200)

**Schritt 2: Entprell-Variablen hinzufügen (vor der Schleife)**

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5
   last_tts_time = 0

**Schritt 3: Tastengesteuerte TTS hinzufügen (innerhalb der Schleife)**

.. code-block:: python

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           # Nachricht aus Erkennungsergebnissen erstellen
           tts.say(your_message)

Hier sind einige Ideen zur Anwendung dieses Musters:

- **MediaPipe Gesichtserkennung** (:ref:`mp_face`)
  → „Gesicht in der Bildmitte erkannt"

- **MediaPipe Pose** (:ref:`mp_pose`)
  → „Beide Arme gehoben" oder „Kniebeuge erkannt — gute Form!"

- **OpenCV Farbverfolgung** (:ref:`play_with_opencv`)
  → „Rotes Objekt bewegt sich nach links" oder „Ziel erfasst"

- **YOLO Objekterkennung** (:ref:`play_with_yolo`)
  → „Person erkannt" oder „Zwei Autos im Blickfeld"

- **Hardware-Integration**
  → Ersetzen Sie die ``t``-Taste durch einen GPIO-Taster über
  ``fusion_hat`` für eine vollständig freihändige Bedienung.


-----------------------------------------------------------------
9. Fehlerbehebung
-----------------------------------------------------------------

- **Kein Ton aus dem Lautsprecher**

  Stellen Sie sicher, dass der Fusion HAT+ Lautsprecher richtig
  angeschlossen und die Lautstärke nicht stummgeschaltet ist.
  Versuchen Sie einen einfachen TTS-Test:

  .. code-block:: bash

     sudo python3 -c "from fusion_hat.tts import Espeak; Espeak().say('test')"

  Wenn Sie „test" hören, funktioniert die TTS-Engine.

- **TTS wird beim Gedrückthalten der Taste zu oft ausgelöst**

  Erhöhen Sie ``DEBOUNCE_INTERVAL`` auf einen größeren Wert,
  z. B. ``2.0`` oder ``2.5`` Sekunden.

  Wenn Sie nur eine einzige Auslösung pro Tastendruck möchten
  (keine Wiederholung beim Halten), verfolgen Sie den Tastenzustand
  über Frames hinweg und lösen Sie nur bei der *steigenden Flanke*
  aus (Übergang von nicht-gedrückt zu gedrückt).

- **Sprachausgabe klingt zu schnell oder unklar**

  Reduzieren Sie die Geschwindigkeit: ``tts.set_speed(120)``.

  Passen Sie die Tonhöhe für Klarheit an: ``tts.set_pitch(70)``.

- **Sprachausgabe überlappt mit vorheriger Ausgabe**

  Espeak auf dem Fusion HAT+ reiht Sprachausgabe standardmäßig in
  eine Warteschlange ein. Wenn Sie laufende Sprachausgabe abbrechen
  möchten, bevor neue beginnt, können Sie eine kurze Verzögerung
  einfügen oder eine andere TTS-Engine verwenden.

- **Visueller Blitz erscheint nicht**

  Überprüfen Sie, ob ``tts_triggered`` innerhalb des Entprell-Blocks
  auf ``True`` gesetzt wird und ob ``tts_flash_until`` auf
  ``time.time() + 1.0`` gesetzt wird.


-----------------------------------------------------------------
10. Zusammenfassung
-----------------------------------------------------------------

- Diese Lektion hat gezeigt, wie man **TTS-Sprachausgabe** zu einem
  MediaPipe Computer-Vision-Projekt hinzufügt.
- Die Fusion HAT+ ``Espeak``-Engine bietet eine einfache,
  Offline-TTS-Lösung auf dem Raspberry Pi.
- **Behandelte Schlüssel-Designmuster**:

  - Auslösung von TTS per Tastendruck (nicht bei jedem Frame)
  - **Entprellschutz** zur Vermeidung von Sprachüberlappung
  - **Visuelles Feedback** (grüner Rand-Blitz) für Benutzerbewusstsein
  - Umwandlung von Erkennungsergebnissen in natürliche gesprochene Nachrichten

- Diese Muster sind **projektunabhängig** — Sie können sie auf jedes
  OpenCV-, MediaPipe- oder YOLO-Projekt anwenden, um Sprachausgabe
  hinzuzufügen.
- Das Hinzufügen von Sprache macht Ihre Projekte zugänglicher und
  freihändig bedienbar und eröffnet Möglichkeiten für
  Assistenztechnologie-Anwendungen und interaktive Installationen.
