.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

(Ejemplo) Demo de Corrección de Tareas con Cámara Pan-Tilt
=====================================================

**Introducción**

Este proyecto crea un interactivo **Asistente de Corrección de Tareas con IA** que combina visión por computadora, inteligencia artificial y robótica. El sistema:

1. **Captura fotos** de preguntas de tareas escritas a mano o impresas usando una cámara Raspberry Pi
2. **Analiza el contenido** usando el modelo de visión GPT-4o de OpenAI para determinar si las respuestas son correctas
3. **Proporciona retroalimentación física** a través de movimientos de un cabezal pan-tilt controlado por servos:

   - *Asiente* para respuestas correctas
   - *Niega* para respuestas incorrectas

4. **Usa interacción simple** activada por una sola pulsación de botón

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Esta demostración muestra cómo la IA puede interactuar con el mundo físico, creando una herramienta educativa atractiva que proporciona retroalimentación visual inmediata sobre la precisión de las tareas.

Puedes usar otros módulos LLM y componentes de hardware para construir tus propios dispositivos de aprendizaje asistidos por IA. Consulta:

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**Qué Necesitarás**

Los siguientes componentes son necesarios para este proyecto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - ENLACE DE COMPRA
    *   - :ref:`cpn_servo`
        - |link_servo_buy|
    *   - Pan-Tilt
        -
    *   - :ref:`cpn_camera_module`
        - |link_camera_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - Raspberry Pi
        - \-
    *   - Muestra de tarea (impresa o escrita a mano)
        - \-

----------------------------------------------

**Configuración del Hardware**

Para usar el módulo de cámara cómodamente, se recomienda :ref:`assemble_fusion_hat_pan_tilt`.

   .. note::

     El montaje del pan-tilt puede ocultar algunos pines, por lo que se recomienda ensamblarlo solo cuando se use la cámara, o colocarlo en la parte exterior después del ensamblaje.


   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Ejecutar el Código**

#. Crea una Muestra de Tarea:

   - Escribe o imprime un problema matemático simple con respuesta
   - Ejemplo: "5 + 3 = 8" (correcto) o "5 + 3 = 7" (incorrecto)
   - Asegúrate de que la letra o impresión sea clara

#. Ejecuta el Programa:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. Sigue las Instrucciones en Pantalla:

   - Coloca la tarea debajo de la cámara
   - Presiona el Botón de Usuario (USR) en el Fusion HAT+
   - Observa la respuesta del servo

#. Salida Esperada:

   .. code-block:: text

      HOMEWORK GRADING DEMO
      ==================================================
      Instructions:
      1. Place a homework question under the camera
      2. Make sure the question AND answer are visible
      3. Press the User Button (USR) on Fusion HAT to grade
      4. The camera will take a photo
      5. AI will grade the answer
      6. Servo will nod (correct) or shake (incorrect)
      ==================================================

      Waiting for button press...

      ==================================================
      Button pressed - Starting grading process

      Taking photo...
      Photo captured
      Sending to AI for grading...
      AI response: CORRECT
      Answer is correct - nodding head
      ==================================================

----------------------------------------------

**Código**

Aquí está el script completo en Python para la Demo de Corrección de Tareas:

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   """
   Homework Grading Demo with Pan-Tilt Camera
   Press User Button to take photo, LLM grades, servo nods or shakes
   """

   import time
   from fusion_hat.llm import OpenAI
   from fusion_hat.servo import Servo
   from fusion_hat.user_button import UserButton
   from picamera2 import Picamera2, Preview

   # ========== LLM SETTINGS ==========
   # Create a secret.py file with: OPENAI_API_KEY = "your-api-key-here"
   try:
       from secret import OPENAI_API_KEY
   except ImportError:
       print("ERROR: Please create a secret.py file with your OpenAI API key")
       print("Example content: OPENAI_API_KEY = 'sk-...'")
       exit()

   # LLM instructions for grading
   INSTRUCTIONS = """You are a homework grading assistant.
   When you see a photo of a homework question with an answer,
   determine if the answer is correct or incorrect.

   Respond with ONLY ONE WORD:
   - If the answer is CORRECT, respond: "CORRECT"
   - If the answer is INCORRECT, respond: "INCORRECT"

   Do not provide any other text, explanations, or justifications.
   Only respond with "CORRECT" or "INCORRECT"."""

   # Initialize LLM
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o"
   )

   # Set LLM settings
   llm.set_max_messages(5)
   llm.set_instructions(INSTRUCTIONS)

   # ========== HARDWARE SETTINGS ==========
   PAN_CHANNEL = 2      # Horizontal servo for shaking head
   TILT_CHANNEL = 3     # Vertical servo for nodding head

   # Servo center positions
   TILT_CENTER = 0      # Looking straight ahead
   PAN_CENTER = 0       # Center position

   # ========== INITIALIZE HARDWARE ==========
   print("Initializing Homework Grading Demo...")
   print("-" * 50)

   # Initialize servos
   pan_servo = Servo(PAN_CHANNEL)
   tilt_servo = Servo(TILT_CHANNEL)

   # Center servos
   tilt_servo.angle(TILT_CENTER)
   pan_servo.angle(PAN_CENTER)
   time.sleep(1)
   print("Servos ready")

   # Initialize camera
   camera = Picamera2()
   camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
   camera.configure(camera_config)
   camera.start_preview(Preview.QT)
   camera.start()
   time.sleep(2)
   print("Camera ready")

   # Initialize user button
   user_button = UserButton()
   print("User button ready")
   print("-" * 50)

   # ========== SERVO MOVEMENT FUNCTIONS ==========
   def nod_head():
       """
       Nodding head movement for "correct"
       """
       # Look down
       tilt_servo.angle(15)
       time.sleep(0.2)
       # Look up
       tilt_servo.angle(-10)
       time.sleep(0.2)
       # Return to center
       tilt_servo.angle(TILT_CENTER)

   def shake_head():
       """
       Shaking head movement for "incorrect"
       """
       # Look left
       pan_servo.angle(-20)
       time.sleep(0.15)
       # Look right
       pan_servo.angle(20)
       time.sleep(0.15)
       # Look left again
       pan_servo.angle(-15)
       time.sleep(0.15)
       # Return to center
       pan_servo.angle(PAN_CENTER)

   # ========== GRADING FUNCTION ==========
   def grade_homework():
       """
       Main grading function: take photo, send to LLM, move servo
       """
       print("\nTaking photo...")

       # Capture image
       img_path = './homework.jpg'
       camera.capture_file(img_path)
       print("Photo captured")

       # Send to LLM for grading
       print("Sending to AI for grading...")

       prompt = "Look at this homework question and answer. Is the answer correct? Respond with only one word: 'CORRECT' or 'INCORRECT'."

       response = llm.prompt(prompt, image_path=img_path)
       response_text = response.strip().upper()

       print(f"AI response: {response_text}")

       # Move servo based on response
       if "INCORRECT" in response_text:
           print("Answer is incorrect - shaking head")
           shake_head()
       elif "CORRECT" in response_text:
           print("Answer is correct - nodding head")
           nod_head()
       else:
           print(f"Unexpected response: {response_text}")

   # ========== BUTTON CALLBACK ==========
   def on_button_click():
       """
       Called when user button is pressed
       """
       print("\n" + "=" * 50)
       print("Button pressed - Starting grading process")
       grade_homework()
       print("=" * 50)

   # ========== MAIN DEMO ==========
   def main():
       """
       Main demo function
       """
       print("\nHOMEWORK GRADING DEMO")
       print("=" * 50)
       print("Instructions:")
       print("1. Place a homework question under the camera")
       print("2. Make sure the question AND answer are visible")
       print("3. Press the User Button (USR) on Fusion HAT to grade")
       print("4. The camera will take a photo")
       print("5. AI will grade the answer")
       print("6. Servo will nod (correct) or shake (incorrect)")
       print("=" * 50)
       print("\nWaiting for button press...")

       # Set button callback
       user_button.set_on_click(on_button_click)

       # Keep program running
       try:
           while True:
               time.sleep(0.1)
       except KeyboardInterrupt:
           print("\nDemo stopped by user")

   # ========== CLEANUP ==========
   def cleanup():
       """
       Clean up resources
       """
       print("\nCleaning up...")

       # Return servos to center
       tilt_servo.angle(TILT_CENTER)
       pan_servo.angle(PAN_CENTER)

       # Stop camera
       camera.stop()

       print("Demo ended")

   # ========== RUN DEMO ==========
   if __name__ == "__main__":
       try:
           main()
       finally:
           cleanup()

----------------------------------------------

**Entendiendo el Código**

1. Configuración del LLM

   El sistema usa GPT-4o de OpenAI con capacidades de Visión para analizar imágenes:

   .. code-block:: python

      # Import and initialize the LLM
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

      # Set specific instructions for consistent responses
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)

      # Limit conversation history to manage tokens
      llm.set_max_messages(5)

2. Inicialización del Hardware

   Se inicializan tres componentes de hardware: servos, cámara y botón:

   .. code-block:: python

      # Servo control for pan-tilt mechanism
      pan_servo = Servo(PAN_CHANNEL)   # Channel 2 for horizontal movement
      tilt_servo = Servo(TILT_CHANNEL) # Channel 3 for vertical movement

      # Camera setup with preview
      camera = Picamera2()
      camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
      camera.configure(camera_config)
      camera.start_preview(Preview.QT)
      camera.start()

      # User button for interaction
      user_button = UserButton()

3. Funciones de Animación de Servos

   Movimientos de apariencia natural para asentir y negar:

   .. code-block:: python

      def nod_head():
          """Nodding head movement for 'correct' answers"""
          tilt_servo.angle(15)    # Look down
          time.sleep(0.2)
          tilt_servo.angle(-10)   # Look up
          time.sleep(0.2)
          tilt_servo.angle(TILT_CENTER)  # Return to center

      def shake_head():
          """Shaking head movement for 'incorrect' answers"""
          pan_servo.angle(-20)    # Look left
          time.sleep(0.15)
          pan_servo.angle(20)     # Look right
          time.sleep(0.15)
          pan_servo.angle(-15)    # Look left again
          time.sleep(0.15)
          pan_servo.angle(PAN_CENTER)  # Return to center

4. Captura de Imagen y Análisis con IA

   El flujo de trabajo principal de corrección:

   .. code-block:: python

      def grade_homework():
          # Capture image from camera
          img_path = './homework.jpg'
          camera.capture_file(img_path)

          # Send image to LLM with specific prompt
          prompt = "Look at this homework question and answer..."
          response = llm.prompt(prompt, image_path=img_path)
          response_text = response.strip().upper()

          # Interpret response and trigger appropriate servo movement
          if "INCORRECT" in response_text:
              shake_head()
          elif "CORRECT" in response_text:
              nod_head()

5. Manejo de Eventos del Botón

   Sistema simple de devolución de llamada para la interacción del usuario:

   .. code-block:: python

      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()

      # Assign callback to button
      user_button.set_on_click(on_button_click)

6. Bucle Principal de la Aplicación

   Bucle principal mínimo que espera las pulsaciones de botón:

   .. code-block:: python

      def main():
          print("Waiting for button press...")
          user_button.set_on_click(on_button_click)

          # Keep program running until interrupted
          try:
              while True:
                  time.sleep(0.1)  # Low CPU usage wait
          except KeyboardInterrupt:
              print("\nDemo stopped by user")

7. Limpieza de Recursos

   Procedimiento de apagado adecuado:

   .. code-block:: python

      def cleanup():
          # Return servos to neutral position
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)

          # Stop camera
          camera.stop()

----------------------------------------------

**Solución de problemas**

- No module named ``picamera2``

  Instala la librería requerida:

  .. code-block:: bash

     sudo apt update
     sudo apt install python3-picamera2

- Cámara no detectada

  1. Verifica la conexión de la cámara: asegúrate de que el cable plano esté insertado correctamente
  2. Verifica que la cámara esté habilitada: ``sudo raspi-config`` → Interface Options → Camera
  3. Prueba la cámara de forma independiente: ``libcamera-hello``

- Servos no se mueven

  1. Verifica las conexiones de alimentación: los servos necesitan alimentación de 5V
  2. Verifica que los canales de los servos coincidan con el código (Canales 2 y 3)
  3. Prueba los servos de forma independiente con comandos de ángulo simples

- La IA no responde o da error

  1. Verifica que la clave API en ``secret.py`` sea correcta
  2. Verifica la conexión a internet: ``ping 8.8.8.8``
  3. Asegúrate de tener créditos en tu cuenta de OpenAI
  4. Verifica que el modelo "gpt-4o" esté disponible en tu cuenta

- Movimientos incorrectos de los servos

  1. Verifica si los servos pan y tilt están intercambiados
  2. Ajusta los valores de ángulo en las funciones ``nod_head()`` y ``shake_head()``
  3. Verifica las posiciones centrales de los servos (pueden necesitar calibración)

- Imagen demasiado borrosa u oscura

  1. Asegúrate de tener iluminación adecuada sobre la tarea
  2. Ajusta el enfoque de la cámara si es ajustable
  3. Coloca la cámara a 15-30 cm del papel
  4. Usa un bolígrafo/marcador de alto contraste para la escritura a mano

- El botón no responde

  1. Verifica si el LED del Botón de Usuario se enciende al presionarlo
  2. Verifica que la devolución de llamada del botón esté registrada
  3. Prueba el botón con una declaración de impresión simple

- La IA devuelve una respuesta inesperada

  1. Verifica el formato del prompt en el código
  2. Asegúrate de que la imagen muestre claramente la pregunta Y la respuesta
  3. Prueba primero con problemas aritméticos muy simples

----------------------------------------------


¡Esta demo de corrección de tareas muestra cómo los modelos de visión de IA pueden interactuar con hardware físico para crear experiencias educativas atractivas, combinando la inteligencia digital con mecanismos de retroalimentación tangible!