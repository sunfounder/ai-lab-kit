.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_auto_tts:

13. TTS Automático Sin Contacto — Transmisión de Voz Manos Libres
==================================================================

-----------------------------------------------------------------
1. Descripción General
-----------------------------------------------------------------

En :ref:`mp_hand_count_tts` (Sección 12), construimos un programa
de conteo de gestos de mano donde el usuario presiona la tecla ``t`` para activar
una transmisión de voz TTS.

En esta sección, damos el siguiente paso: **eliminar completamente el teclado.**
El sistema ahora *detecta automáticamente* cuando mantienes un gesto de mano
firme y dice el conteo de dedos — sin teclas, sin botones,
completamente sin contacto.

.. image:: img/mp_hand_count.png
   :align: center

Esta lección introduce un **patrón de máquina de estados** para la interacción
sin contacto — una técnica que puedes aplicar a proyectos de accesibilidad,
instalaciones manos libres y cualquier escenario donde la entrada por teclado
no sea práctica.

Al final de esta lección, sabrás cómo:

- Diseñar una máquina de estados para el seguimiento de presencia de manos
- Detectar la *estabilidad* del gesto a través de múltiples fotogramas
- Usar una puerta de duración de mantenimiento para evitar activaciones falsas
- Detectar automáticamente cuando una mano entra o sale del fotograma
- Proporcionar retroalimentación visual de múltiples etapas (inactivo → detectado → estable → hablando)
- Mostrar una barra de progreso para la cuenta regresiva de duración de mantenimiento


-----------------------------------------------------------------
2. Cómo Funciona
-----------------------------------------------------------------

El programa reemplaza el activador por teclado con un **activador automático
basado en estabilidad**. Aquí está el pipeline:

1. Inicializar **MediaPipe Hands** para la detección de manos en tiempo real.
2. Inicializar el **motor TTS de Fusion HAT+** (Espeak).
3. Capturar fotogramas de video y detectar dedos (igual que antes).
4. Alimentar el conteo de dedos en un **detector de estabilidad** — una ventana
   deslizante que verifica si el conteo se ha mantenido igual
   a través de múltiples fotogramas consecutivos.
5. Una vez que el conteo se confirma estable, iniciar un **temporizador de duración de mantenimiento**.
6. Si el usuario mantiene el mismo gesto durante 2.5 segundos, el TTS se activa
   automáticamente.
7. Si la mano sale del fotograma, el sistema dice "hand left the frame"
   después de un breve retardo.
8. Una **barra de progreso** y un **borde multicolor** muestran el estado
   actual de un vistazo.

La idea clave de diseño es:

    *La mano firme del usuario reemplaza el teclado —*
    el sistema observa la *intención* (mantenerse quieto) en lugar de
    reaccionar a cada gesto pasajero.

Esto hace que el proyecto sea completamente manos libres y accesible — ideal para
tecnología de asistencia, exhibiciones interactivas o situaciones donde
el usuario no puede alcanzar un teclado.


-----------------------------------------------------------------
3. Conceptos Clave de Diseño
-----------------------------------------------------------------

Añadir TTS activado automáticamente requiere una gestión de estado más
sofisticada que la versión con tecla. Revisemos cada
nuevo concepto.

--------------------------------------------------
3.1 Máquina de Estados para el Seguimiento de Manos
--------------------------------------------------

El programa rastrea la presencia de la mano como un **estado**, no solo un
valor por fotograma. Una clase ``HandTrackingState`` encapsula
todas las variables de estado:

.. code-block:: python

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

Al agrupar todas las variables de seguimiento en un solo objeto, el código
se mantiene organizado incluso cuando la lógica se vuelve más compleja.

La máquina de estados transiciona a través de estas fases:

- **Sin mano** — borde gris, estado inactivo
- **Mano detectada, aún no estable** — borde cian, mensaje "keep hand still"
- **Estable, manteniendo** — borde verde se llena, barra de progreso se anima
- **Hablando** — destello verde brillante, etiqueta "SPEAKING..."

--------------------------------------------------
3.2 Detección de Estabilidad
--------------------------------------------------

Un conteo de dedos de un solo fotograma no es fiable — el número puede
parpadear debido al ruido de la cámara o al movimiento leve de la mano. Para evitar
activaciones falsas, usamos una **ventana deslizante** de conteos recientes:

.. code-block:: python

    from collections import deque

    FRAME_HISTORY_SIZE = 10
    STABLE_FRAMES_REQUIRED = 5

    state.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)

    def update_stability(new_count):
        state.finger_history.append(new_count)

        if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
            recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
            if all(c == new_count for c in recent_counts):
                # Gesture is stable!
                state.is_stable = True
                state.stable_start_time = time.time()
                state.current_fingers = new_count
                return True

        state.current_fingers = new_count
        return False

El gesto se considera **estable** solo cuando los últimos 5 fotogramas
todos reportan el mismo conteo de dedos. Esto filtra parpadeos momentáneos
y asegura que el sistema solo hable cuando el usuario está
manteniendo intencionalmente un gesto.

--------------------------------------------------
3.3 Activación Automática con Duración de Mantenimiento
--------------------------------------------------

La estabilidad sola no es suficiente — el usuario debe *mantener* el gesto
el tiempo suficiente para demostrar intención:

.. code-block:: python

    HOLD_DURATION_REQUIRED = 2.5    # seconds
    MIN_TTS_INTERVAL = 4.0          # seconds between auto triggers

    def should_trigger_tts():
        now = time.time()

        # Minimum interval between TTS triggers
        if now - state.last_tts_time < MIN_TTS_INTERVAL:
            return False

        # Hand must be present and stable
        if not state.hand_present or not state.is_stable:
            return False

        # Must have been stable for the required hold duration
        hold_time = now - state.stable_start_time
        if hold_time < HOLD_DURATION_REQUIRED:
            return False

        # Don't repeat the same count too quickly
        if state.stable_fingers == state.current_fingers:
            if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
                return False

        return True

Tres puertas protegen contra activaciones falsas:

1. **Intervalo mínimo** — al menos 4 segundos entre dos eventos TTS.
2. **Duración de mantenimiento** — el gesto debe mantenerse firme durante 2.5 segundos.
3. **Protección de repetición** — el mismo conteo no se volverá a decir durante 8 segundos.

--------------------------------------------------
3.4 Detección de Salida de Mano
--------------------------------------------------

Cuando el usuario retira la mano de la cámara, el sistema
lo nota y dice una notificación:

.. code-block:: python

    HAND_EXIT_DELAY = 4.0  # seconds after hand leaves

    # When hand just left:
    if state.hand_present:
        state.hand_present = False
        state.is_stable = False
        state.stable_fingers = -1
        state.finger_history.clear()

        if now - state.last_tts_time >= MIN_TTS_INTERVAL:
            tts.say("hand left the frame")

El mensaje de salida solo se activa si ha pasado suficiente tiempo desde
el último evento TTS — evitando que interrumpa un
anuncio de conteo de dedos.

--------------------------------------------------
3.5 Construcción del Mensaje
--------------------------------------------------

La construcción del mensaje es idéntica a la versión con tecla:

.. code-block:: python

    if count == 0:
        message = "no fingers detected"
    elif count == 1:
        message = "one finger detected"
    else:
        message = f"{count} fingers detected"

.. note::

   A diferencia de la versión con tecla que suma dedos de ambas manos,
   esta versión usa ``max(total_fingers, finger_count)`` para elegir
   la mano con más dedos visibles. Esto produce resultados
   más fiables cuando ambas manos están en el fotograma.

--------------------------------------------------
3.6 Retroalimentación Visual de Múltiples Etapas
--------------------------------------------------

En lugar de un solo destello verde, esta versión proporciona un
**borde codificado por colores continuo** que refleja el estado actual:

.. code-block:: python

    COLOR_IDLE     = (128, 128, 128)   # gray   — no hand
    COLOR_DETECTED = (255, 255, 0)     # cyan   — hand seen, not yet stable
    COLOR_STABLE   = (0, 255, 0)       # green  — gesture stable, holding
    COLOR_SPEAKING = (0, 255, 0)       # bright green — TTS in progress

El color del borde transiciona suavemente de cian a verde a medida que
la duración de mantenimiento progresa, dando al usuario retroalimentación en tiempo real de
lo cerca que está de activar TTS.

**Barra de progreso**: Una pequeña barra en la esquina superior derecha se llena de
izquierda a derecha a medida que la duración de mantenimiento cuenta. Cuando llega al 100%,
el TTS se activa. Esto le da al usuario una cuenta regresiva visual clara.

**Texto de estado**: Una línea de estado debajo del conteo de dedos muestra
la fase actual:

- ``"Status: No hand detected"``
- ``"Status: Detecting... keep hand still"``
- ``"Status: Hold gesture (1.3s to speak)"``
- ``"Status: Ready to speak!"``


-----------------------------------------------------------------
4. Ejecutar el Código
-----------------------------------------------------------------

.. important::

   Antes de comenzar, asegúrate de:

   * El Fusion HAT+ está ensamblado y el altavoz está conectado
   * Puedes acceder al escritorio de Raspberry Pi
   * El paquete de código está instalado
   * MediaPipe y OpenCV están instalados

   Para obtener instrucciones detalladas, consulta :ref:`mediapipe_install` y :ref:`opencv_install`.

#. Abre la terminal e ingresa el siguiente comando:

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts_without_tap.py

#. Después de ejecutar el programa:

   - Se abre una ventana titulada "MediaPipe Hand Detection + AUTO TTS (Touchless Mode)",
     mostrando la transmisión de la cámara en vivo.
   - Levanta tu mano hacia la cámara — el conteo de dedos aparece
     en la esquina superior izquierda.
   - *Mantén tu mano quieta* — observa el borde cambiar de gris
     a cian a verde, y la barra de progreso llenarse.
   - Después de 2.5 segundos de mantener el mismo gesto, el sistema
     dice automáticamente el conteo de dedos.
   - Retira tu mano de la cámara — después de un momento, el sistema
     dice "hand left the frame."

   .. hint::

      Intenta mostrar diferentes números de dedos y manteniendo cada
      uno firme durante unos segundos. Deberías oír cada conteo
      dicho automáticamente. Observa cómo el color del borde y la
      barra de progreso te guían a través del proceso.

   Presiona ``q`` para salir del programa.


--------------------------------------------------
5. Código Completo
--------------------------------------------------

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
   # Finger tip and dip landmark indices
   FINGER_TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
   FINGER_DIPS = [2, 6, 10, 14, 18]   # corresponding middle joints

   # Auto TTS parameters
   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable before speaking
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves before saying "hand left"
   NO_HAND_COOLDOWN = 5.0          # seconds without hand before suppressing "no hand" repeats

   # Frame processing
   FRAME_HISTORY_SIZE = 10         # for stability detection

   # Border colors (BGR)
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
       # ---- 1. Capture frame ----
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # ---- 2. Convert to RGB for MediaPipe ----
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       # ---- 3. Convert back to BGR for OpenCV display ----
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # ---- 4. Detect hands and count fingers ----
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

       # ---- 5. Update state machine ----
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

       # ---- 6. Display information on screen ----
       display_text = f"Fingers: {total_fingers}"
       cv2.putText(frame, display_text, (10, 40),
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

       cv2.putText(frame, "Keep gesture still to auto-speak | 'q' to quit",
                   (10, frame.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

       # ---- 7. Visual border feedback ----
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

       # ---- 8. Progress bar for hold duration ----
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

       # ---- 9. Key handling ----
       key = cv2.waitKey(1) & 0xff

       if key == ord('q'):
           break

       # ---- 10. Show frame ----
       cv2.imshow("MediaPipe Hand Detection + AUTO TTS (Touchless Mode)", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")


--------------------------------------------------
6. Explicación del Código
--------------------------------------------------

Repasemos el código sección por sección, centrándonos en
lo que es nuevo en comparación con la versión con tecla de
:ref:`mp_hand_count_tts`.

--------------------------------------------------
6.1 Importaciones y Nuevas Dependencias
--------------------------------------------------

.. code-block:: python

   from collections import deque
   import time

La adición clave es ``deque`` — una cola doblemente terminada de
Python del módulo ``collections``. Proporciona una ventana deslizante
de tamaño fijo para la detección de estabilidad: cuando haces ``append``
a un ``deque(maxlen=N)``, los elementos antiguos se descartan
automáticamente, manteniendo solo los N valores más recientes.

Esto es perfecto para rastrear los últimos 5–10 conteos de dedos
sin gestión manual de listas.

--------------------------------------------------
6.2 Constantes y Configuración
--------------------------------------------------

.. code-block:: python

   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves
   NO_HAND_COOLDOWN = 5.0          # seconds before suppressing repeats
   FRAME_HISTORY_SIZE = 10         # for stability detection

   COLOR_IDLE     = (128, 128, 128)   # gray
   COLOR_DETECTED = (255, 255, 0)     # cyan
   COLOR_STABLE   = (0, 255, 0)       # green
   COLOR_SPEAKING = (0, 255, 0)       # bright green

Todos los parámetros de temporización y comportamiento se declaran como constantes nombradas
en la parte superior del archivo. Esto hace que el programa sea fácil de ajustar —
¿quieres un tiempo de mantenimiento más largo? Cambia ``HOLD_DURATION_REQUIRED``.
¿Quieres anuncios menos frecuentes? Aumenta ``MIN_TTS_INTERVAL``.

Los cuatro colores de borde definen un lenguaje visual:

- **Gris** — inactivo, no hay mano en el fotograma
- **Cian** — mano detectada, pero aún no estable
- **Verde** — el gesto es estable y se está manteniendo
- **Verde brillante** — hablando actualmente

--------------------------------------------------
6.3 Clase HandTrackingState
--------------------------------------------------

.. code-block:: python

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

Esta clase agrupa todas las variables de seguimiento en un solo objeto.
Cada variable tiene un rol específico:

- ``finger_history`` — ventana deslizante de conteos de dedos recientes
  (usada por el detector de estabilidad)
- ``current_fingers`` — el conteo de dedos para el fotograma actual
- ``stable_fingers`` — el último conteo estable confirmado que fue dicho
- ``stable_start_time`` — cuándo comenzó el período estable actual
- ``is_stable`` — si el gesto está actualmente confirmado como estable
- ``hand_present`` — si hay una mano actualmente en el fotograma
- ``hand_absent_start_time`` — cuándo salió la mano del fotograma por última vez
- ``last_tts_time`` — marca de tiempo del último evento TTS
- ``last_tts_message`` — el último mensaje dicho (para evitar repeticiones)
- ``last_no_hand_tts_time`` — marca de tiempo del último anuncio "no hand"

Se crea una única instancia de ``state`` globalmente, para que todas las funciones
auxiliares puedan leerla y modificarla sin pasar parámetros.

--------------------------------------------------
6.4 Función de Detección de Estabilidad
--------------------------------------------------

.. code-block:: python

   def update_stability(new_count):
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

Esta función es el corazón del sistema sin contacto. Así es como funciona:

1. **Añadir** el nuevo conteo de dedos a la ventana deslizante.
2. **Verificar** si tenemos suficientes fotogramas (al menos 5).
3. **Comparar** los últimos 5 fotogramas — si todos coinciden con el conteo
   actual, el gesto es estable.
4. **Registrar** la hora en que comenzó la estabilidad (``stable_start_time``)
   — esto es usado por el temporizador de duración de mantenimiento.
5. **Devolver** ``True`` en el fotograma donde la estabilidad se confirma
   por primera vez, ``False`` en caso contrario.

La expresión ``all(c == new_count for c in recent_counts)`` es
elegante: verifica que *todos* los valores en la ventana coincidan con el
conteo actual. Si incluso un fotograma difiere, la estabilidad se rompe.

--------------------------------------------------
6.5 Lógica de Activación Automática de TTS
--------------------------------------------------

.. code-block:: python

   def should_trigger_tts():
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

Esta función actúa como una **puerta** — todas las condiciones deben cumplirse
antes de que el TTS pueda activarse:

1. **Intervalo mínimo**: al menos 4 segundos desde el último TTS.
2. **Mano presente y estable**: el gesto debe estar confirmado como estable.
3. **Duración de mantenimiento**: el usuario debe haber mantenido el gesto durante
   al menos 2.5 segundos.
4. **Protección de repetición**: el mismo conteo de dedos no se volverá a decir
   durante 8 segundos (2x el intervalo mínimo).

.. tip::

   La duración de mantenimiento crea una *señal de intención* clara — los gestos
   momentáneos se ignoran, pero un mantenimiento deliberado activa el habla.
   Esta es la diferencia clave con el enfoque de tecla: la *paciencia* del
   usuario reemplaza la pulsación del botón.

--------------------------------------------------
6.6 Detección de Salida de Mano
--------------------------------------------------

.. code-block:: python

   # In the main loop:
   if has_hand:
       if not state.hand_present:
           # Hand just entered
           state.hand_present = True
           state.is_stable = False
           state.finger_history.clear()
           print("[INFO] Hand detected")
       state.hand_absent_start_time = now
   else:
       if state.hand_present:
           # Hand just left
           state.hand_present = False
           state.is_stable = False
           state.stable_fingers = -1
           state.finger_history.clear()
           if now - state.last_tts_time >= MIN_TTS_INTERVAL:
               trigger_hand_exit_tts()

Cuando la mano entra o sale del fotograma, el estado se restablece:

- La estabilidad se borra (``is_stable = False``)
- El historial de dedos se limpia (``history.clear()``)
- Si la mano acaba de salir, y ha pasado suficiente tiempo desde el
  último TTS, el sistema dice "hand left the frame"

Restablecer la estabilidad al entrar y salir evita que el estado obsoleto
se transfiera entre apariciones de manos.

--------------------------------------------------
6.7 Borde Multicolor y Barra de Progreso
--------------------------------------------------

.. code-block:: python

   def get_border_color():
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               # Smooth blend from cyan to green
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

El color del borde no es solo decorativo — es un indicador de estado
en tiempo real:

- **Sin mano** → borde gris
- **Mano detectada, no estable** → borde cian
- **Estable, aún manteniendo** → degradado suave de cian a verde
  a medida que la duración de mantenimiento progresa
- **Mantenimiento completo / hablando** → borde verde brillante

La **barra de progreso** funciona junto con el borde:

.. code-block:: python

   if has_hand and state.is_stable:
       hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
       bar_width = int(w * 0.4)
       bar_height = 8
       bar_x = w - bar_width - 10
       bar_y = 10
       filled_width = int(bar_width * hold_progress)

       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                    (60, 60, 60), -1)  # background
       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                    (0, 255, 0), -1)   # fill

Una barra gris oscura (40% del ancho del fotograma) se sitúa en la esquina superior derecha.
Un relleno verde la recorre a medida que el tiempo de mantenimiento progresa.
Cuando la barra está llena, el TTS se activa.

Juntos, el color del borde y la barra de progreso le dan al usuario
retroalimentación continua — siempre saben exactamente lo cerca que están
de activar el habla.


-----------------------------------------------------------------
7. Ideas de Extensión
-----------------------------------------------------------------

El patrón de TTS automático sin contacto abre muchas posibilidades:

- **Comunicación asistida** — Asigna gestos específicos a
  frases pregrabadas. Levanta 1 dedo para "yes", 2 para "no",
  3 para "help". El sistema dice la frase automáticamente.

- **Control de presentaciones manos libres** — Mantén un gesto para
  avanzar diapositivas o activar efectos de sonido durante una charla.

- **Exhibición interactiva de museo** — Los visitantes levantan dedos
  para escuchar datos sobre exhibiciones numeradas. Sin necesidad de tocar.

- **Integración con botón GPIO** — Añade un botón físico a través de
  ``fusion_hat`` GPIO que habilite/deshabilite el modo TTS automático,
  dando al usuario control manual sobre cuándo el sistema escucha.

- **Vocabulario de múltiples gestos** — Extiende el detector de estabilidad
  para reconocer una secuencia de gestos (ej., 1 dedo → 2 dedos
  → 3 dedos) como un "código de comando" que activa diferentes acciones.

- **Combinar con detección facial** — Anunciar automáticamente cuando un rostro
  entra o sale del fotograma: "Person detected" / "Person left."


-----------------------------------------------------------------
8. Solución de Problemas
-----------------------------------------------------------------

- **El TTS se activa con demasiada frecuencia o en gestos inestables**

  Aumenta ``STABLE_FRAMES_REQUIRED`` (ej., de 5 a 8) para
  requerir más fotogramas de consistencia antes de confirmar la estabilidad.

  Aumenta ``HOLD_DURATION_REQUIRED`` (ej., de 2.5 a 3.5)
  para requerir un mantenimiento más largo antes de hablar.

- **El TTS nunca se activa, incluso manteniendo firme**

  Asegúrate de que tu mano esté bien iluminada y claramente visible para la
  cámara. Verifica que ``min_detection_confidence`` no esté configurado
  demasiado alto (0.5 es un buen valor predeterminado).

  Verifica que el texto de estado en pantalla muestre "Ready to speak!"
  — si se queda en "Detecting..." o la barra de progreso nunca se
  llena, el detector de estabilidad puede no estar confirmando.

- **"Hand left the frame" se dice en momentos incorrectos**

  El mensaje de salida respeta ``MIN_TTS_INTERVAL`` — no se
  activa si acaba de ocurrir un anuncio de conteo de dedos. Si
  deseas que siempre hable, elimina la verificación de ``MIN_TTS_INTERVAL``
  de ``trigger_hand_exit_tts()``.

- **La barra de progreso no aparece**

  La barra de progreso solo aparece cuando ``has_hand`` es ``True``
  **y** ``state.is_stable`` es ``True``. Si alguna condición
  es falsa, la barra está oculta. Verifica el texto de estado para
  determinar qué condición está fallando.

- **El color del borde no cambia**

  Verifica que ``get_border_color()`` se esté llamando en cada
  fotograma y que las banderas ``state.hand_present`` y ``state.is_stable``
  se estén actualizando correctamente en el bucle principal.


-----------------------------------------------------------------
9. Resumen
-----------------------------------------------------------------

- Esta lección demostró cómo **eliminar el activador por teclado**
  y construir un sistema TTS automático completamente sin contacto.
- El proyecto utiliza una **máquina de estados** (clase ``HandTrackingState``)
  para rastrear la presencia de manos, la estabilidad del gesto y la temporización del TTS.
- **Patrones de diseño clave** cubiertos:

  - **Detección de estabilidad** — ventana deslizante de conteos de dedos
    para confirmar que el usuario está manteniendo un gesto firme
  - **Puerta de duración de mantenimiento** — requerir 2.5 segundos de estabilidad
    antes de activar el TTS, reemplazando la tecla con *intención*
  - **Detección automática de salida** — decir "hand left the frame"
    cuando la mano desaparece
  - **Retroalimentación visual de múltiples etapas** — borde codificado por colores
    (gris → cian → verde) más una barra de progreso para el estado
    en tiempo real
  - **Restablecimiento de estado al entrar/salir la mano** — limpiar el historial y
    la estabilidad para evitar que datos obsoletos se transfieran

- Estos patrones son **agnósticos al proyecto** — puedes aplicar el
  enfoque de máquina de estados + detección de estabilidad a cualquier proyecto
  de visión artificial que necesite interacción sin contacto.
- Combinar TTS automático con reconocimiento de gestos abre la puerta
  a tecnología de asistencia, sistemas de control manos libres e
  instalaciones interactivas.
