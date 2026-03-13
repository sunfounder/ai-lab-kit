.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_homework_grading_demo:

(Beispiel) Demo zur Hausaufgabenkorrektur mit Pan-Tilt-Kamera
==============================================================================

**Einführung**

Dieses Projekt erstellt einen interaktiven **AI-Hausaufgabenkorrektur-Assistenten**, der Computer Vision, künstliche Intelligenz und Robotik kombiniert. Das System:

1. **Erfasst Fotos** von handschriftlichen oder gedruckten Hausaufgaben mit einer Raspberry-Pi-Kamera
2. **Analysiert den Inhalt** mit dem Vision-Modell GPT-4 von OpenAI, um zu bestimmen, ob die Antworten korrekt sind
3. **Gibt physisches Feedback** über servogesteuerte Pan-Tilt-Kopfbewegungen:

   - *Nickt* bei richtigen Antworten
   - *Schüttelt den Kopf* bei falschen Antworten
   
4. **Verwendet eine einfache Interaktion**, die durch einen einzigen Tastendruck ausgelöst wird

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Homework_Grading_Demo.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Diese Demo zeigt, wie AI mit der physischen Welt interagieren kann, und schafft so ein anschauliches Lernwerkzeug, das sofortiges visuelles Feedback zur Richtigkeit von Hausaufgaben gibt.

Sie können auch andere LLM-Module und Hardwarekomponenten verwenden, um eigene AI-gestützte Lernsysteme zu entwickeln. Siehe:

* :ref:`py_online_llm`
* :ref:`cpn_servo`
* :ref:`cpn_camera_module`

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
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
    *   - Hausaufgabenbeispiel (gedruckt oder handschriftlich)
        - \-

----------------------------------------------

**Hardware-Einrichtung**

Für eine komfortable Nutzung des Kameramoduls wird :ref:`assemble_fusion_hat_pan_tilt` empfohlen.

   .. note:: 
     
     Durch die Montage des Pan-Tilt-Moduls können einige Pins verdeckt werden. Daher wird empfohlen, es nur bei Verwendung der Kamera zu montieren oder es nach der Montage außen anzubringen.
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Code ausführen**

#. Hausaufgabenbeispiel erstellen:

   - Schreiben oder drucken Sie eine einfache Mathematikaufgabe mit Antwort
   - Beispiel: "5 + 3 = 8" (richtig) oder "5 + 3 = 7" (falsch)
   - Achten Sie auf gut lesbare Handschrift oder einen klaren Druck

#. Programm starten:
   
   .. code-block:: bash
   
      cd ~/ai-lab-kit/llm
      python3 llm_openai_homework.py

#. Anweisungen auf dem Bildschirm folgen:

   - Positionieren Sie die Hausaufgabe unter der Kamera
   - Drücken Sie die User-Taste (USR) auf dem Fusion HAT+
   - Beobachten Sie die Reaktion des Servos

#. Erwartete Ausgabe:
   
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

**Code**

Hier ist das vollständige Python-Skript für die Demo zur Hausaufgabenkorrektur:

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

**Code verstehen**

1. LLM-Konfiguration und Einrichtung

   Das System verwendet OpenAIs GPT-4o mit Vision-Funktionen zur Bildanalyse:
   
   .. code-block:: python
   
      # LLM importieren und initialisieren
      from fusion_hat.llm import OpenAI
      llm = OpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")
      
      # Spezifische Anweisungen für konsistente Antworten festlegen
      INSTRUCTIONS = """You are a homework grading assistant..."""
      llm.set_instructions(INSTRUCTIONS)
      
      # Gesprächsverlauf begrenzen, um Tokens zu sparen
      llm.set_max_messages(5)

2. Hardware-Initialisierung

   Drei Hardwarekomponenten werden initialisiert: Servos, Kamera und Taste:
   
   .. code-block:: python
   
      # Servosteuerung für das Pan-Tilt-System
      pan_servo = Servo(PAN_CHANNEL)   # Kanal 2 für horizontale Bewegung
      tilt_servo = Servo(TILT_CHANNEL) # Kanal 3 für vertikale Bewegung
      
      # Kameraeinrichtung mit Vorschau
      camera = Picamera2()
      camera_config = camera.create_preview_configuration(main={"size": (1280, 720)})
      camera.configure(camera_config)
      camera.start_preview(Preview.QT)
      camera.start()
      
      # User-Taste für Interaktion
      user_button = UserButton()

3. Servo-Animationsfunktionen

   Natürlich wirkende Bewegungen zum Nicken und Kopfschütteln:
   
   .. code-block:: python
   
      def nod_head():
          """Kopf-Nicken für 'richtige' Antworten"""
          tilt_servo.angle(15)    # Nach unten schauen
          time.sleep(0.2)
          tilt_servo.angle(-10)   # Nach oben schauen
          time.sleep(0.2)
          tilt_servo.angle(TILT_CENTER)  # Zurück zur Mitte
      
      def shake_head():
          """Kopf-Schütteln für 'falsche' Antworten"""
          pan_servo.angle(-20)    # Nach links schauen
          time.sleep(0.15)
          pan_servo.angle(20)     # Nach rechts schauen
          time.sleep(0.15)
          pan_servo.angle(-15)    # Noch einmal nach links
          time.sleep(0.15)
          pan_servo.angle(PAN_CENTER)  # Zurück zur Mitte

4. Bildaufnahme und AI-Analyse

   Der Hauptablauf für die Bewertung:
   
   .. code-block:: python
   
      def grade_homework():
          # Bild von der Kamera aufnehmen
          img_path = './homework.jpg'
          camera.capture_file(img_path)
          
          # Bild mit spezifischem Prompt an das LLM senden
          prompt = "Look at this homework question and answer..."
          response = llm.prompt(prompt, image_path=img_path)
          response_text = response.strip().upper()
          
          # Antwort interpretieren und entsprechende Servo-Bewegung auslösen
          if "INCORRECT" in response_text:
              shake_head()
          elif "CORRECT" in response_text:
              nod_head()

5. Ereignisbehandlung der Taste

   Einfaches Callback-System für die Benutzerinteraktion:
   
   .. code-block:: python
   
      def on_button_click():
          print("Button pressed - Starting grading process")
          grade_homework()
      
      # Callback der Taste zuweisen
      user_button.set_on_click(on_button_click)

6. Hauptanwendungsschleife

   Minimale Hauptschleife, die auf Tastendruck wartet:
   
   .. code-block:: python
   
      def main():
          print("Waiting for button press...")
          user_button.set_on_click(on_button_click)
          
          # Programm läuft weiter, bis es unterbrochen wird
          try:
              while True:
                  time.sleep(0.1)  # Warten mit geringer CPU-Auslastung
          except KeyboardInterrupt:
              print("\nDemo stopped by user")

7. Ressourcenbereinigung

   Ordnungsgemäßes Herunterfahren:
   
   .. code-block:: python
   
      def cleanup():
          # Servos in Neutralposition zurücksetzen
          tilt_servo.angle(TILT_CENTER)
          pan_servo.angle(PAN_CENTER)
          
          # Kamera stoppen
          camera.stop()

----------------------------------------------

**Fehlerbehebung**

- Kein Modul namens ``picamera2``

  Installieren Sie die benötigte Bibliothek:
  
  .. code-block:: bash
     
     sudo apt update
     sudo apt install python3-picamera2

- Kamera wird nicht erkannt

  1. Kameraverbindung prüfen: sicherstellen, dass das Flachbandkabel korrekt eingesetzt ist
  2. Kamera aktivieren: ``sudo raspi-config`` → Interface Options → Camera
  3. Kamera separat testen: ``libcamera-hello``

- Servos bewegen sich nicht

  1. Stromversorgung prüfen: Servos benötigen 5V
  2. Überprüfen, ob die Servo-Kanäle mit dem Code übereinstimmen (Kanäle 2 und 3)
  3. Servos separat mit einfachen Winkelbefehlen testen

- AI reagiert nicht oder gibt Fehler aus

  1. Prüfen, ob der API-Schlüssel in ``secret.py`` korrekt ist
  2. Internetverbindung testen: ``ping 8.8.8.8``
  3. Sicherstellen, dass Ihr OpenAI-Konto über Guthaben verfügt
  4. Prüfen, ob das Modell „gpt-4o“ in Ihrem Konto verfügbar ist

- Falsche Servo-Bewegungen

  1. Prüfen, ob Pan- und Tilt-Servo vertauscht sind
  2. Winkelwerte in ``nod_head()`` und ``shake_head()`` anpassen
  3. Servo-Mittelposition überprüfen (möglicherweise Kalibrierung erforderlich)

- Bild zu unscharf oder zu dunkel

  1. Für ausreichende Beleuchtung der Hausaufgabe sorgen
  2. Kamerafokus einstellen (falls möglich)
  3. Kamera etwa 15–30 cm über dem Papier positionieren
  4. Für Handschrift einen gut sichtbaren Stift oder Marker verwenden

- Taste reagiert nicht

  1. Prüfen, ob die LED der User-Taste beim Drücken aufleuchtet
  2. Sicherstellen, dass das Callback korrekt registriert ist
  3. Taste mit einem einfachen ``print``-Testskript prüfen

- AI liefert unerwartete Antworten

  1. Prompt-Formatierung im Code überprüfen
  2. Sicherstellen, dass im Bild sowohl Aufgabe als auch Antwort klar sichtbar sind
  3. Zunächst sehr einfache Rechenaufgaben testen

----------------------------------------------

Diese Demo zur Hausaufgabenkorrektur zeigt, wie AI-Vision-Modelle mit physischer Hardware interagieren können, um spannende Lernerfahrungen zu schaffen, bei denen digitale Intelligenz mit greifbarem Feedback kombiniert wird.