.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_tts:

12. Añadiendo Transmisión de Voz TTS a Proyectos MediaPipe
===========================================================

-----------------------------------------------------------------
1. Descripción General
-----------------------------------------------------------------

En :ref:`mp_hand_count` (Sección 5), construimos un programa
de conteo de gestos de mano que muestra el número de dedos levantados en pantalla.

En esta sección, iremos un paso más allá:
**añadir transmisión de voz de Texto a Voz (TTS)**
para que la Raspberry Pi pueda *decir* en voz alta el conteo de dedos detectado —
haciendo el proyecto más interactivo y accesible.

.. image:: img/mp_hand_count.png
   :align: center

Esta lección no se trata solo de contar dedos —
enseña un **patrón general** para añadir TTS a *cualquier*
proyecto de MediaPipe u OpenCV.

Al final de esta lección, sabrás cómo:

- Inicializar y configurar el motor TTS de Fusion HAT+
- Activar TTS con una tecla con protección antirrebote
- Añadir retroalimentación visual mientras el sistema habla
- Aplicar este patrón a tus propios proyectos de visión artificial


-----------------------------------------------------------------
2. Cómo Funciona
-----------------------------------------------------------------

El programa se basa en el pipeline de conteo de manos y añade una capa TTS
que se activa mediante una tecla:

1. Inicializar **MediaPipe Hands** para la detección de manos en tiempo real.
2. Inicializar el **motor TTS de Fusion HAT+** (Espeak).
3. Capturar fotogramas de video y detectar dedos (igual que antes).
4. Esperar a que el usuario presione la tecla ``t``.
5. Al presionar la tecla, convertir el conteo de dedos actual en un mensaje hablado.
6. Usar **lógica antirrebote** para evitar activaciones repetidas rápidas.
7. Mostrar un **destello visual** en pantalla mientras el TTS está hablando.
8. El habla se reproduce a través del altavoz de Fusion HAT+.

La idea clave de diseño es:

    *El TTS se añade como una capa no bloqueante —*
    la detección se ejecuta continuamente, y el habla solo se activa
    cuando el usuario lo solicita.

Este patrón mantiene el pipeline de video fluido mientras añade
salida de voz bajo demanda.


-----------------------------------------------------------------
3. El Módulo TTS de Fusion HAT+
-----------------------------------------------------------------

La biblioteca ``fusion_hat`` proporciona una interfaz simple y unificada
para varios motores TTS. En este proyecto, usamos **Espeak** —
un motor ligero sin conexión que funciona bien en Raspberry Pi.

**Uso básico:**

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

Tres parámetros te permiten personalizar la voz:

- **amp** (amplitud) — controla el volumen. Más alto = más fuerte.
- **speed** — velocidad de habla en palabras por minuto. 150 es normal.
- **pitch** — tono de la voz. 80 es el predeterminado; valores más bajos suenan más graves.

.. note::

   Fusion HAT+ también es compatible con **Piper** (neuronal, sin conexión)
   y **OpenAI TTS** (en línea, voces naturales).
   Consulta :ref:`tts_piper_openai` para opciones más avanzadas.


-----------------------------------------------------------------
4. Diseño Clave: Añadir TTS a un Bucle de Video
-----------------------------------------------------------------

Al añadir TTS a un pipeline de video en tiempo real, hay algunas
consideraciones de diseño importantes. Revisemos cada una.

--------------------------------------------------
4.1 Activación por Tecla
--------------------------------------------------

En lugar de hablar en cada fotograma (lo que sería caótico),
usamos una tecla como activador:

.. code-block:: python

    key = cv2.waitKey(1) & 0xff
    if key == ord('t'):
        tts.say(message)

La tecla ``t`` se elige porque es fácil de recordar
(*t* de *talk*). Puedes usar cualquier tecla — ``space`` para
control manos libres en el piso, o un botón GPIO para entrada física.

--------------------------------------------------
4.2 Protección Antirrebote
--------------------------------------------------

Sin protección, mantener presionada la tecla ``t`` activaría
el TTS docenas de veces por segundo, superponiendo el habla y
haciéndolo ininteligible.

**Solución: antirrebote basado en tiempo.**

.. code-block:: python

    DEBOUNCE_INTERVAL = 1.5  # seconds
    last_tts_time = 0

    # In the loop:
    if key == ord('t'):
        now = time.time()
        if now - last_tts_time > DEBOUNCE_INTERVAL:
            last_tts_time = now
            tts.say(message)

Después de cada activación de TTS, las siguientes activaciones se ignoran
durante 1.5 segundos. Esto le da al habla suficiente tiempo para terminar
antes de que comience la siguiente.

--------------------------------------------------
4.3 Construcción del Mensaje
--------------------------------------------------

El conteo de dedos (un entero) debe convertirse en
una frase con sonido natural:

.. code-block:: python

    if total_fingers == 0:
        message = "no fingers detected"
    elif total_fingers == 1:
        message = "one finger detected"
    else:
        message = f"{total_fingers} fingers detected"

Usar ``"one"`` en lugar de ``"1"`` asegura que Espeak lo pronuncie
de forma natural. Para números mayores que uno, la forma de dígito
funciona bien con Espeak.

--------------------------------------------------
4.4 Retroalimentación Visual (Destello de Borde Verde)
--------------------------------------------------

Mientras el sistema está hablando, añadimos un indicador visual
para que el usuario sepa que el habla está en progreso:

.. code-block:: python

    tts_flash_until = now + 1.0   # flash for 1 second

    # Later in the loop:
    if tts_triggered and time.time() < tts_flash_until:
        cv2.rectangle(frame, (0, 0), (w-1, h-1), (0, 255, 0), 8)
        cv2.putText(frame, "Speaking...", (10, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

Un **borde verde** aparece alrededor del fotograma y una
etiqueta **"Speaking..."** se muestra. Ambos desaparecen automáticamente
después de 1 segundo.

Este bucle de retroalimentación es importante porque:

- El TTS toma un momento para completarse — el usuario necesita saber
  que el sistema escuchó su comando.
- El borde desaparece cuando termina, para que no interfiera
  con el uso normal.


-----------------------------------------------------------------
5. Ejecutar el Código
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

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts.py

#. Después de ejecutar el programa:

   - Se abre una ventana titulada "MediaPipe Hand Count + TTS",
     mostrando la transmisión de la cámara en vivo.
   - Levanta tu mano hacia la cámara — el conteo de dedos aparece
     en la esquina superior izquierda.
   - *Presiona la tecla* ``t`` — el sistema dice el conteo de dedos
     actual a través del altavoz de Fusion HAT+.
   - Un borde verde parpadea en la pantalla mientras habla.

   .. hint::

      Intenta mostrar diferentes números de dedos y presiona ``t``
      cada vez. Deberías oír: "one finger detected",
      "three fingers detected", etc.

   Presiona ``q`` para salir del programa.


--------------------------------------------------
6. Código Completo
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
7. Explicación del Código
--------------------------------------------------

Repasemos el código sección por sección, centrándonos en
lo que es nuevo en comparación con el programa básico de conteo de manos.

--------------------------------------------------
7.1 Importaciones e Inicialización
--------------------------------------------------

.. code-block:: python

   from fusion_hat.tts import Espeak
   import time

   tts = Espeak()
   tts.set_amp(200)
   tts.set_speed(150)
   tts.set_pitch(80)

Dos nuevas importaciones y un bloque de inicialización TTS son las primeras
adiciones. ``Espeak()`` crea el motor TTS, y las tres
llamadas ``set_*`` configuran la voz.

El ``import time`` es necesario para la temporización antirrebote.

--------------------------------------------------
7.2 Constantes Antirrebote y Variables de Estado
--------------------------------------------------

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5

   last_tts_time = 0
   tts_triggered = False
   tts_flash_until = 0

Se introducen cuatro nuevas variables:

- ``DEBOUNCE_INTERVAL`` — evita el spam de TTS (segundos).
- ``last_tts_time`` — registra cuándo se activó TTS por última vez.
- ``tts_triggered`` — bandera para el efecto de destello visual.
- ``tts_flash_until`` — marca de tiempo de cuándo debe terminar el destello.

--------------------------------------------------
7.3 Manejo de Teclas con Antirrebote
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

Esta es la adición central de TTS. Vamos a desglosarla:

1. **Detección de tecla** — ``ord('t')`` verifica si se presionó ``t``.

2. **Puerta antirrebote** — ``time.time() - last_tts_time > DEBOUNCE_INTERVAL``
   asegura que hayan pasado al menos 1.5 segundos desde la última activación.
   Si no ha pasado suficiente tiempo, la pulsación de tecla se ignora.

3. **Actualizar estado** — Cuando la puerta se abre, registramos la hora
   actual y establecemos el temporizador de destello.

4. **Construir mensaje** — El conteo de dedos se convierte en una
   oración legible para humanos.

5. **Hablar** — ``tts.say(message)`` envía el texto al altavoz.

.. note::

   ``tts.say()`` es **no bloqueante** — el programa continúa
   procesando fotogramas de video mientras el habla se reproduce en segundo plano.

--------------------------------------------------
7.4 Retroalimentación Visual
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

- Se dibuja un borde verde (8 píxeles de grosor) alrededor de todo el fotograma.
- Una etiqueta amarilla "Speaking..." aparece debajo del conteo de dedos.
- Ambos persisten durante 1 segundo, luego desaparecen automáticamente.
- Cuando el temporizador de destello expira, ``tts_triggered`` se restablece a ``False``,
  listo para la siguiente activación.

Este patrón es reutilizable — puedes añadir la misma retroalimentación
a cualquier proyecto que active TTS.


-----------------------------------------------------------------
8. Ideas de Extensión: Aplicando Este Patrón a Otros Proyectos
-----------------------------------------------------------------

El patrón de integración TTS que aprendiste aquí es **genérico**.
Puedes añadir transmisión de voz a cualquier proyecto de MediaPipe, OpenCV o YOLO
siguiendo estos pasos:

**Paso 1: Importar e inicializar TTS**

.. code-block:: python

   from fusion_hat.tts import Espeak
   tts = Espeak()
   tts.set_amp(200)

**Paso 2: Añadir variables antirrebote (antes del bucle)**

.. code-block:: python

   DEBOUNCE_INTERVAL = 1.5
   last_tts_time = 0

**Paso 3: Añadir TTS activado por tecla (dentro del bucle)**

.. code-block:: python

   if key == ord('t'):
       now = time.time()
       if now - last_tts_time > DEBOUNCE_INTERVAL:
           last_tts_time = now
           # Build your message from detection results
           tts.say(your_message)

Aquí hay algunas ideas para aplicar este patrón:

- **Detección facial de MediaPipe** (:ref:`mp_face`)
  → "Face detected at center of frame"

- **Pose de MediaPipe** (:ref:`mp_pose`)
  → "Both arms raised" o "Squat detected — good form!"

- **Seguimiento de color OpenCV** (:ref:`play_with_opencv`)
  → "Red object moving left" o "Target locked"

- **Detección de objetos YOLO** (:ref:`play_with_yolo`)
  → "Person detected" o "Two cars in view"

- **Integración de hardware**
  → Reemplaza la tecla ``t`` con una pulsación de botón GPIO a través de
  ``fusion_hat`` para una experiencia completamente manos libres.


-----------------------------------------------------------------
9. Solución de Problemas
-----------------------------------------------------------------

- **No hay sonido del altavoz**

  Asegúrate de que el altavoz Fusion HAT+ esté correctamente conectado y
  el volumen no esté silenciado. Intenta ejecutar una prueba TTS simple:

  .. code-block:: bash

     sudo python3 -c "from fusion_hat.tts import Espeak; Espeak().say('test')"

  Si escuchas "test", el motor TTS está funcionando.

- **El TTS se activa demasiadas veces al mantener presionada la tecla**

  Aumenta ``DEBOUNCE_INTERVAL`` a un valor mayor,
  por ejemplo ``2.0`` o ``2.5`` segundos.

  Si deseas solo una activación por pulsación de tecla
  (sin repetición al mantener presionada), rastrea el estado de la tecla entre fotogramas
  y solo dispara en el *flanco ascendente* (transición de la tecla de
  no presionada a presionada).

- **El habla suena demasiado rápida o poco clara**

  Reduce la velocidad: ``tts.set_speed(120)``.

  Ajusta el tono para mayor claridad: ``tts.set_pitch(70)``.

- **El habla se superpone con el habla anterior**

  Espeak en Fusion HAT+ encola el habla por defecto.
  Si deseas cancelar el habla en curso antes de comenzar un nuevo discurso,
  puedes añadir un pequeño retardo o usar un motor TTS diferente.

- **El destello visual no aparece**

  Verifica que ``tts_triggered`` esté establecido en ``True`` dentro del
  bloque antirrebote y que ``tts_flash_until`` esté establecido en
  ``time.time() + 1.0``.


-----------------------------------------------------------------
10. Resumen
-----------------------------------------------------------------

- Esta lección demostró cómo **añadir transmisión de voz TTS**
  a un proyecto de visión artificial con MediaPipe.
- El motor ``Espeak`` de Fusion HAT+ proporciona una solución TTS
  simple y sin conexión en Raspberry Pi.
- **Patrones de diseño clave** cubiertos:

  - Activar TTS mediante una tecla (no en cada fotograma)
  - **Protección antirrebote** para evitar superposición de habla
  - **Retroalimentación visual** (destello de borde verde) para conciencia del usuario
  - Convertir resultados de detección en mensajes hablados naturales

- Estos patrones son **agnósticos al proyecto** — puedes aplicarlos
  a cualquier proyecto de OpenCV, MediaPipe o YOLO para añadir salida de voz.
- Añadir voz hace que tus proyectos sean más accesibles y
  manos libres, abriendo la puerta a aplicaciones de tecnología de asistencia
  e instalaciones interactivas.
