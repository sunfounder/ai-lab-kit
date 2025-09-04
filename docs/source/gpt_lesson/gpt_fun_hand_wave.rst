2.6 Hand-Wave Interaktionssystem
======================================

Dieses Projekt ist ein Gesten-Interaktionssystem, das zwei Infrarot-Hindernissensoren verwendet, um Handbewegungen zu erkennen. Die erfassten Sensordaten werden an einen OpenAI-gestützten Assistenten gesendet, der anhand der Zeitdifferenz zwischen den Sensorauslösungen die Art der Handbewegung analysiert. Basierend auf dieser Analyse erzeugt der Assistent passende Antworten, z. B. das Erkennen einer Wischgeste und eine entsprechende Rückmeldung.


-----------------------------------

**Features**

- **Duale Infrarotsensor-Eingabe**: Erkennt Handbewegungen mit zwei im Abstand von 10 cm platzierten Sensoren.
- **Echtzeit-Gestenerkennung**: Bestimmt Richtung, Geschwindigkeit und Typ der Handbewegungen.
- **KI-gestützte Interpretation**: Sendet Sensordaten an OpenAI zur Analyse und Antwortgenerierung.
- **LED-Anzeige**: Signalisiert den Systemstatus während der Gestenerkennung.
- **Ereignisgesteuerte Ausführung**: Nutzt GPIO-Callbacks für effiziente Erkennung in Echtzeit.



-----------------------------------

**Was Sie benötigen**

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - KOMPONENTE
        - KAUFLINK

    *   - :ref:`cpn_avoid_module`
        - |link_obstacle_avoidance_buy|
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - Fusion HAT
        - 
    *   - Raspberry Pi Zero 2 W
        -

-----------------------------------

**Schaltplan**

.. image:: img/fzz/gpt_hand_wave_bb.png
   :width: 800
   :align: center


----------------------------------------------

**Beispiel ausführen**


Der gesamte Beispielcode für dieses Tutorial befindet sich im Verzeichnis ``ai-explorer-lab-kit``.  
Führen Sie die folgenden Schritte aus, um das Beispiel zu starten:


.. code-block:: shell
   
   cd ~/ai-explorer-lab-kit/gpt_example/
   sudo ~/my_venv/bin/python3 gpt_fun_hand_wave.py 


-----------------------------------

**Code**

.. raw:: html

   <run></run>

.. code-block:: python

   import openai
   from keys import OPENAI_API_KEY
   import time
   from fusion_hat import Pin
   from signal import pause

   # init openai
   client = openai.OpenAI(api_key=OPENAI_API_KEY)

   assistant = client.beta.assistants.create(
      name="BOT",
      instructions="You function as a gesture interaction device equipped with two infrared obstacle avoidance sensors positioned approximately 10 cm apart. You will receive trigger information from these sensors in the format: {('left', timestamp), ('right', timestamp)}. Based on the time difference between these triggers, determine if the user is waving their hand. Provide appropriate responses, such as 'You waved quickly from left to right, hello!' or 'You waved slowly twice on the left side, hello!'.",
      model="gpt-4-1106-preview",
   )

   thread = client.beta.threads.create()


   # setup GPIO
   sensor_left = Pin(17, Pin.IN, Pin.PULL_UP)
   sensor_right = Pin(22, Pin.IN, Pin.PULL_UP)
   led = Pin(27, Pin.OUT)  # indicate LED connect to GPIO 27
   led.on()

   # store timestamp of sensor triggered
   events = []

   def sensor_triggered(sensor_id):
      global events
      timestamp = time.time()
      events.append((sensor_id, timestamp))
      print(f"Sensor {sensor_id} triggered at {timestamp}")

      # when sensor triggered twice, analyze the hand wave
      if len(events) >= 2:
         analyze_hand_wave()

   def analyze_hand_wave():
      global events
      # insure the events list has at least two elements
      if len(events) < 2:
         return
      print("Start analyzing hand wave...")
      led.off()

      # send events to AI for decoding
      try:
         message = client.beta.threads.messages.create(
               thread_id=thread.id,
               role="user",
               content=str(events),
         )

         run = client.beta.threads.runs.create_and_poll(
               thread_id=thread.id,
               assistant_id=assistant.id,
         )

         # print("Run completed with status: " + run.status)

         if run.status == "completed":
               messages = client.beta.threads.messages.list(thread_id=thread.id)

               for message in messages.data:
                  if message.role == 'assistant':
                     for block in message.content:
                           if block.type == 'text':
                              decoded_message = block.text.value
                     break # only last reply

         print(f"Decoded Message: {decoded_message}")

         # clear events list
         events.clear()
         led.on()

      except Exception as e:
         print(f"Error in AI processing: {e}")

   # set sensor callbacks
   sensor_left.when_activated = lambda: sensor_triggered('left')
   sensor_right.when_activated = lambda: sensor_triggered('right')

   try:
      print("Press CTRL+C to exit.")
      pause()

   finally:
      print("Resources cleaned up. Exiting.")
      client.beta.assistants.delete(assistant.id)
      


-----------------------------------

**Code Explanation**

Dieses Projekt ist in mehrere zentrale Funktionsblöcke gegliedert:

1. **Initialisierung und Setup:**

   - Importiert die notwendigen Module, darunter ``openai`` für die KI-Verarbeitung und ``fusion_hat`` für die GPIO-Steuerung.
   - Initialisiert den OpenAI-API-Client mit ``OPENAI_API_KEY``.
   - Konfiguriert die GPIO-Pins für die linken und rechten Sensoren sowie eine LED-Anzeige.

2. **Sensor-Ereignisbehandlung**:

   - Jedes Mal, wenn ein Sensor auslöst, werden Zeitstempel und Sensor-ID in ``events`` gespeichert.
   - Sobald mindestens zwei Ereignisse registriert sind, wird ``analyze_hand_wave`` aufgerufen, um die Geste zu interpretieren.

   .. code-block:: python

       def sensor_triggered(sensor_id):
           global events
           timestamp = time.time()
           events.append((sensor_id, timestamp))
           print(f"Sensor {sensor_id} triggered at {timestamp}")

           if len(events) >= 2:
               analyze_hand_wave()

3. **Analyse der Handbewegung**:

   - Stellt sicher, dass mindestens zwei Sensorauslösungen vorliegen.
   - Sendet die aufgezeichneten Ereignisdaten an OpenAI zur Auswertung.
   - Empfängt und verarbeitet die KI-Antwort, die die erkannte Geste beschreibt.

   .. code-block:: python

       def analyze_hand_wave():
           global events
           if len(events) < 2:
               return
           print("Start analyzing hand wave...")
           led.off()

           try:
               message = client.beta.threads.messages.create(
                   thread_id=thread.id,
                   role="user",
                   content=str(events),
               )

               run = client.beta.threads.runs.create_and_poll(
                   thread_id=thread.id,
                   assistant_id=assistant.id,
               )

               if run.status == "completed":
                   messages = client.beta.threads.messages.list(thread_id=thread.id)
                   for message in messages.data:
                       if message.role == 'assistant':
                           for block in message.content:
                               if block.type == 'text':
                                   decoded_message = block.text.value
                           break
               print(f"Decoded Message: {decoded_message}")
               events.clear()
               led.on()
           except Exception as e:
               print(f"Error in AI processing: {e}")

4. **KI-Integration und Antwortverarbeitung:**

   - Nutzt OpenAIs GPT-4-Modell zur Analyse von Handbewegungsmustern.
   - Erkennt Charakteristika der Geste, z. B. Geschwindigkeit und Richtung.
   - Gibt eine passende Rückmeldung basierend auf den Bewegungsmustern aus.

5. **Systemschleife und Aufräumen:**

   - Verwendet ``pause()``, um das Programm dauerhaft laufen zu lassen.
   - Beim Beenden (z. B. mit ``CTRL+C``) werden die Ressourcen freigegeben und die OpenAI-Assistenteninstanz gelöscht.

   .. code-block:: python

       try:
           print("Press CTRL+C to exit.")
           pause()
       finally:
           print("Resources cleaned up. Exiting.")
           client.beta.assistants.delete(assistant.id)


-----------------------------------

**Debugging Tips**

- **Keine Sensorauslösung erkannt?**

  - Stellen Sie sicher, dass die Infrarotsensoren korrekt verkabelt und mit Strom versorgt sind.
  - Geben Sie Rohdaten der Sensoren aus, um deren Funktion zu überprüfen.

- **KI reagiert nicht?**

  - Überprüfen Sie, ob Ihr OpenAI-API-Schlüssel gültig und korrekt gesetzt ist.
  - Prüfen Sie die Netzwerkverbindung, um erfolgreiche API-Aufrufe sicherzustellen.

- **Gesten werden falsch interpretiert?**

  - Kontrollieren Sie, ob die Zeitstempel der Sensoren korrekt aufgezeichnet werden.
  - Vergrößern Sie den Abstand zwischen den Sensoren, wenn die Erkennung zu empfindlich reagiert.

- **LED schaltet nicht ein/aus?**

  - Vergewissern Sie sich, dass die GPIO-Pinbelegung mit der Hardware übereinstimmt.
  - Prüfen Sie, ob die Funktionen ``led.on()`` und ``led.off()`` korrekt aufgerufen werden.


