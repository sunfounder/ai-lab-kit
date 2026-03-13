.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_morse_code_decoder:

(Beispiel) AI-gestützter Morsecode-Decoder
=========================================================

**Einführung**

Dieses Projekt erstellt einen intelligenten **Morsecode-Decoder**, der AI verwendet, um Zeitmuster von Tastendrücken zu interpretieren. Das System erfasst präzise Zeitdaten und nutzt OpenAIs GPT, um Morsecode-Nachrichten in Echtzeit zu dekodieren. Der Decoder bietet:

1. **Zeitbasierte Eingabe**, die genaue Druck- und Loslasszeiten erfasst
2. **AI-gestützte Dekodierung** mit GPT zur Interpretation von Punkt-/Strichmustern
3. **Visuellen Indikator** mit einer LED, die den aktiven Dekodierzustand anzeigt
4. **Dual-Button-Oberfläche** mit getrennten Tasten für Eingabe und Steuerung
5. **Echtzeit-Feedback**, das die Zeitdaten während der Eingabe anzeigt

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Powered_Morse_Code_Decoder.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Das System zeichnet die Dauer der Tastendrücke auf, sendet die Zeitdaten zur Interpretation an die AI und dekodiert Morsecode-Sequenzen wie das universelle Notsignal „SOS“ zuverlässig.

Sie können zeitkritische Eingaben mit AI-Interpretation für verschiedene Codierungssysteme kombinieren. Siehe:

* :ref:`py_online_llm` 

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_button`
        - |link_button_buy| (x2)
    *   - :ref:`cpn_led`
        - |link_led_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schaltplan**

Verbinden Sie die Komponenten wie folgt mit dem Raspberry Pi:

.. image:: img/fzz/morse_decoder_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

----------------------------------------------

**Beispiel ausführen**

#. Code ausführen

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_morse_decoder.py

#. Eine einfache Morsecode-Nachricht ausprobieren (Beispiel: "SOS")

   Nachdem das Programm gestartet wurde, drücken Sie die Start-/Stopp-Taste, um die Aufzeichnung zu beginnen.  
   Drücken Sie dann die Morse-Taste, um Punkte (kurze Tastendrücke) und Striche (lange Tastendrücke) einzugeben.

   Wenn Sie fertig sind, drücken Sie die Start-/Stopp-Taste erneut, um die Aufzeichnung zu beenden und die Nachricht zu dekodieren.

#. Konsolenausgabe prüfen

   Die Konsole zeigt die Zeitstempel für Tastendruck und Loslassen an, und die AI analysiert die Zeitdaten
   und gibt die dekodierte Nachricht aus.

   **Typische Konsolenausgabe bei der Eingabe von "SOS":**

   .. code-block:: text

      To decode the Morse code message based on the button press times provided, we need to interpret the duration of each press. Typically, a short press (dot) is around 0.2 to 0.3 seconds, while a long press (dash) is about 0.5 seconds or longer. Let's analyze the press durations:

      1. `1767773542.1257536` to `1767773542.285196` - Duration: ~0.16 seconds - Dot (.)
      2. `1767773542.4936137` to `1767773542.6315389` - Duration: ~0.14 seconds - Dot (.)
      3. `1767773542.9092748` to `1767773543.0543947` - Duration: ~0.15 seconds - Dot (.)
      4. `1767773544.2299025` to `1767773544.5774245` - Duration: ~0.35 seconds - Dash (-)
      5. `1767773545.1017563` to `1767773545.4954002` - Duration: ~0.39 seconds - Dash (-)
      6. `1767773546.11932` to `1767773546.5881057` - Duration: ~0.47 seconds - Dash (-)
      7. `1767773547.824543` to `1767773547.9534554` - Duration: ~0.13 seconds - Dot (.)
      8. `1767773548.1879761` to `1767773548.2895174` - Duration: ~0.10 seconds - Dot (.)
      9. `1767773548.5281847` to `1767773548.6453152` - Duration: ~0.12 seconds - Dot (.)

      Now let's decode the sequence into letters using Morse code:

      - `...` (Dot Dot Dot) = S
      - `---` (Dash Dash Dash) = O
      - `...` (Dot Dot Dot) = S

      Putting it all together, the decoded message is "SOS".

#. Den Ablauf verstehen

   1. Aufzeichnung starten: Drücken Sie die Start-/Stopp-Taste (GPIO 17), und die LED leuchtet auf
   2. Morsecode eingeben: Verwenden Sie die Morse-Taste (GPIO 22) für Punkte und Striche
   3. Echtzeitanzeige: Die Konsole zeigt Zeitstempel für Tastendruck und Loslassen
   4. Stoppen und dekodieren: Drücken Sie die Start-/Stopp-Taste erneut, und die LED erlischt
   5. AI-Analyse: Die Zeitdaten werden zur Interpretation an OpenAI GPT gesendet
   6. Dekodierte Ausgabe: Die AI gibt die dekodierte Nachricht aus

**Code**

Hier ist das vollständige Python-Skript für den AI-gestützten Morsecode-Decoder:

.. raw:: html

   <run></run>

.. code-block:: python
   
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   from fusion_hat.pin import Pin
   import random, time
   
   # Register OpenAI API
   # openai.com
   
   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
   
   # Setup GPIO pins
   morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
   led = Pin(27, Pin.OUT)  # Indicator LED on GPIO 27
   
   # Store the morse code events with timing data
   morse_events = []
   input_active = False  # Flag to indicate if input is active
   
   # Setup LLM with Morse code decoding instructions
   INSTRUCTIONS = "You are a Morse code decoder. Decode based on the button press time, interpreting short presses as dots and long presses as dashes. The message you receive may be a word or a sentence, please decode it and output it."
   
   WELCOME = "Hello, I am a Morse code decoder. Please press the button to start decoding. When you are done, press the button again to stop."
   
   llm = OpenAI(
       api_key=OPENAI_API_KEY,
       model="gpt-4o",
   )
   
   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)
   
   print(WELCOME)
   
   # Send the morse code timing data to the AI for decoding
   def decode_and_print():
       global morse_events
       
       # Convert timing events to string for AI processing
       input_text = str(morse_events)
       
       # Get response from AI with streaming
       response = llm.prompt(input_text, stream=True)
       
       # Print streaming response
       for next_word in response:
           if next_word:
               print(next_word, end="", flush=True)
       
       print("")  # New line after complete response
       
       morse_events = []  # Clear the morse code events for next message
   
   # Morse code input handling variables
   start_time = 0
   
   # Function called when morse input button is pressed
   def morse_input_pressed():
       global start_time
       start_time = time.time()  
       morse_events.append(('pressed', start_time))
       print(f" Pressed at {start_time} -", end="")
   
   # Function called when morse input button is released
   def morse_input_released():
       global morse_events, start_time
       release_time = time.time()  
       
       # Debounce: ignore releases within 0.1 seconds
       if release_time - start_time < 0.1:
           return
       
       morse_events.append(('released', release_time))
       print(f" {release_time}")
   
   # Start/stop button handler
   def handle_start_stop():
       global input_active, morse_events
       
       if input_active:
           # Stop recording and decode
           led.off()
           print("Input stopped and decoded.")
           decode_and_print()
           input_active = False
       else:
           # Start recording new message
           input_active = True
           morse_events.clear()  # Clear previous events
           led.on()
           print("Input started.")
   
   # Add event listeners to buttons
   start_stop_button.when_activated = handle_start_stop
   morse_input.when_activated = morse_input_pressed
   morse_input.when_deactivated = morse_input_released
   
   # Main program loop
   try:
       while True:
           time.sleep(0.1)
   except KeyboardInterrupt:
       pass


----------------------------------------------

**Code verstehen**

1. GPIO-Pin-Konfiguration

   Drei GPIO-Pins werden für unterschiedliche Zwecke konfiguriert:
   
   .. code-block:: python
   
      morse_input = Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      start_stop_button = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN, bounce_time=0.05)
      led = Pin(27, Pin.OUT)
   
   - Entprellzeit (0.05 s): Verhindert Mehrfachauslösungen durch mechanisches Prellen des Schalters  
   - Pull-down: Sorgt für ein stabiles LOW-Signal, wenn die Taste nicht gedrückt ist  
   - Getrennte Funktionen: Eingabe- und Steuertasten verhindern versehentliche Eingaben  

2. Speicherung der Zeitdaten

   Druck- und Loslassereignisse werden mit präzisen Zeitstempeln gespeichert:
   
   .. code-block:: python
   
      morse_events = []  # Leere Liste zur Speicherung der Ereignisse
      
      # Jedes Ereignis wird als Tupel gespeichert: ('pressed'/'released', Zeitstempel)
      morse_events.append(('pressed', 1767773542.1257536))
      morse_events.append(('released', 1767773542.285196))

3. Entprellmechanismus

   Verhindert Fehlauslösungen durch Prellen des Schalters:
   
   .. code-block:: python
   
      def morse_input_released():
          if release_time - start_time < 0.1:  # 100 ms Entprellung
              return  # Sehr kurze Signale ignorieren
          
          morse_events.append(('released', release_time))

4. Zustandsverwaltung

   Das System verwendet ein Flag, um den Aufzeichnungszustand zu verfolgen:
   
   .. code-block:: python
   
      input_active = False  # Anfangszustand: keine Aufzeichnung
      
      def handle_start_stop():
          if input_active:
              # Aufzeichnung stoppen und dekodieren
              input_active = False
          else:
              # Aufzeichnung starten
              input_active = True
              morse_events.clear()  # Vorherige Daten löschen

5. Visueller Indikator

   Die LED zeigt den Aufzeichnungsstatus visuell an:
   
   .. code-block:: python
   
      def handle_start_stop():
          if input_active:
              led.off()  # LED AUS, wenn nicht aufgezeichnet wird
          else:
              led.on()   # LED EIN während der Aufzeichnung

6. Erstellung des AI-Prompts

   Die Zeitdaten werden für die AI-Verarbeitung in einen String umgewandelt:
   
   .. code-block:: python
   
      input_text = str(morse_events)
      
      # Beispiel für das an die AI gesendete Format:
      # "[('pressed', 1767773542.1257536), ('released', 1767773542.285196), ...]"

7. Streaming-Antwort

   Die AI-Antwort wird in Echtzeit verarbeitet und angezeigt:
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)

8. Ereignisgesteuerte Architektur

   Tastenevents lösen sofort Callback-Funktionen aus:
   
   .. code-block:: python
   
      # Callback-Funktionen den Tastenereignissen zuweisen
      start_stop_button.when_activated = handle_start_stop
      morse_input.when_activated = morse_input_pressed
      morse_input.when_deactivated = morse_input_released

9. Zeitmessungsgenauigkeit

   Verwendet ``time.time()`` für Zeitmessungen mit hoher Genauigkeit:
   
   .. code-block:: python
   
      start_time = time.time()  # Aktuelle Zeit in Sekunden seit der Unix-Epoche
      
      # Dauer des Tastendrucks berechnen:
      duration = release_time - start_time

10. Daten zurücksetzen

    Nach der Dekodierung wird die Ereignisliste für die nächste Nachricht geleert:
    
    .. code-block:: python
    
        def decode_and_print():
            # ... Ereignisse verarbeiten ...
            morse_events = []  # Für nächste Nachricht zurücksetzen

----------------------------------------------

**Morsecode-Zeitstandards**

* Standardzeit (basierend auf dem Wort PARIS):

  - Punkt: 1 Einheit  
  - Strich: 3 Einheiten  
  - Abstand innerhalb eines Zeichens (zwischen Punkten/Strichen): 1 Einheit  
  - Abstand zwischen Buchstaben: 3 Einheiten  
  - Abstand zwischen Wörtern: 7 Einheiten  

* Praktische Umsetzung:

  - Punkt: < 0.3 Sekunden (kurzer Tastendruck)  
  - Strich: > 0.5 Sekunden (langer Tastendruck)  
  - Abstand zwischen Elementen: < 0.5 Sekunden Pause  
  - Abstand zwischen Buchstaben: 0.5–1.5 Sekunden Pause  
  - Abstand zwischen Wörtern: > 1.5 Sekunden Pause  

* Häufige Morsezeichen:

  - A: • — (Punkt-Strich)  
  - B: — • • • (Strich-Punkt-Punkt-Punkt)  
  - C: — • — • (Strich-Punkt-Strich-Punkt)  
  - S: • • • (Punkt-Punkt-Punkt)  
  - O: — — — (Strich-Strich-Strich)  

----------------------------------------------

**Fehlerbehebung**

- Tastendrücke werden nicht erkannt

  - Verkabelung prüfen: GPIO 22/17 zur Taste, andere Seite an Masse  
  - Pull-down-Konfiguration überprüfen  
  - Mit einfachem Skript testen: ``print(Pin(22, mode=Pin.IN, pull=Pin.PULL_DOWN).read())``  
  - Entprellzeit prüfen (0.05 s könnte zu hoch sein)

- LED leuchtet nicht

  - Polarität der LED prüfen: Anode (langes Bein) über Widerstand an GPIO 27  
  - Widerstandswert prüfen (220 Ω empfohlen)  
  - LED direkt testen: ``Pin(27, Pin.OUT).on()`` sollte LED einschalten  
  - Masseverbindung überprüfen

- Zeitdaten wirken falsch

  - Systemuhr prüfen: ``date``  
  - Entprellzeit reduzieren, wenn zu empfindlich  
  - Debug-Ausgaben hinzufügen, um Callback-Ausführung zu prüfen  
  - Gleichmäßige Tastendrücke testen

- AI dekodiert falsch

  - API-Schlüssel und Internetverbindung prüfen  
  - Gesendete Zeitdaten überprüfen (``print(morse_events)``)  
  - Konsistente Tastendrücke verwenden (Punkte kurz, Striche lang)  
  - Klarere Pausen zwischen Buchstaben machen

- Mehrfachauslösung bei einem Tastendruck

  - ``bounce_time`` erhöhen (z. B. 0.1 s)  
  - Mechanisches Prellen des Schalters prüfen  
  - Hardware-Entprellung mit Kondensator hinzufügen  
  - Verkabelung der Taste prüfen

- System reagiert nicht auf Start/Stopp

  - Prüfen, ob andere Callback-Funktionen stören  
  - Logik der Variable ``input_active`` überprüfen  
  - Debug-Ausgaben in ``handle_start_stop()`` hinzufügen  
  - Sicherstellen, dass kein anderer Prozess GPIO verwendet

- AI-Antwort zu langsam

  - Internetgeschwindigkeit prüfen  
  - Anzahl der Ereignisse reduzieren (kürzere Nachrichten)  
  - Lokale Dekodierung als Fallback verwenden  
  - Timeout für AI-Antwort implementieren

- Punkte und Striche schwer unterscheidbar

  - Gleichmäßiges Timing üben  
  - Schwellenwerte in den AI-Anweisungen anpassen  
  - Lokale Vorverarbeitung vor dem Senden an die AI hinzufügen  
  - Visuelles Feedback während der Eingabe verwenden

----------------------------------------------

Dieser AI-gestützte Morsecode-Decoder zeigt, wie präzise Zeitmessungen mit intelligenter Mustererkennung kombiniert werden können, um historische Kommunikationsmethoden neu zu beleben und sie für neue Generationen zugänglich und lehrreich zu machen.