.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_ai_health_assistant:

(Beispiel) AI-Gesundheitsassistent mit Temperaturüberwachung
=======================================================================

**Einführung**


Dieses Projekt erstellt einen intelligenten **AI-Gesundheitsassistenten**, der Körpertemperaturmessung mit Sprachinteraktion kombiniert, um personalisierte Gesundheitseinschätzungen zu liefern. Das System integriert:

1. **Thermistorbasierte Temperaturmessung** für eine präzise Erfassung der Körpertemperatur
2. **Spracherkennung** zum Verstehen von Symptomen und Anfragen des Benutzers
3. **AI-gestützte Gesundheitsanalyse** mit OpenAI GPT zur medizinischen Einschätzung
4. **Text-to-Speech-Feedback** für hörbare Gesundheitsempfehlungen
5. **Echtzeitüberwachung** mit kontinuierlicher Temperaturumrechnung

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Ai_Health_Assistant.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Der Gesundheitsassistent misst die Körpertemperatur über eine Thermistorschaltung, analysiert den Messwert mit AI und gibt auf Grundlage etablierter medizinischer Temperaturbereiche passende Gesundheitshinweise.


* :ref:`py_online_llm` 
* :ref:`py_stt_whisper`
* :ref:`tts_espeak_pico2wave`
* :ref:`py_thermistor`


----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
    *   - :ref:`cpn_thermistor`
        - |link_thermistor_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy| (10kΩ)
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schaltplan**

Verbinden Sie die Komponenten wie folgt mit dem Fusion HAT+:

.. image:: img/fzz/health_assistant_bb.png
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
      sudo python3 llm_openai_health.py

#. Ergebnis prüfen

   Wenn das Programm startet, werden Sie aufgefordert zu sprechen. Anschließend schätzt es Ihre Körpertemperatur
   und gibt passende Gesundheitshinweise aus.

   Typische Konsolenausgabe:

   .. code-block:: text

      Hello, I am a health assistant. Please hold your thermometer and I will assess your
      body temperature based on the thermistor reading. If you feel unwell, please provide
      your symptoms and I will provide appropriate health advice.

      Say something
      partial: I feel
      partial: I feel very
      partial: I feel very warm
      final: I feel very warm and tired

      Your body temperature is 38.7°C, which indicates a mild fever. Please rest, stay
      hydrated, and monitor your symptoms. If the fever persists or worsens, consider
      seeking medical attention.

#. Beispiel-Szenarien

   * Normale Temperatur (36.5°C):

     .. code-block:: text

        User: "How's my temperature?"
        AI: "Your body temperature is 36.5°C, which is within the normal range. You're
        doing well, but continue to monitor how you feel."

   * Hohes Fieber (39.2°C):

     .. code-block:: text

        User: "I have a headache and feel hot"
        AI: "Your body temperature is 39.2°C, indicating a high fever. Please rest
        immediately, stay hydrated, and consider seeking medical advice as soon as possible."

   * Niedrige Temperatur (34.2°C):

     .. code-block:: text

        User: "I feel cold and shivering"
        AI: "Your body temperature is 34.2°C, which is below normal and may indicate
        hypothermia. Please warm up immediately with blankets and warm drinks."


**Code**

Hier ist das vollständige Python-Skript für den AI-Gesundheitsassistenten:

.. raw:: html

   <run></run>

.. code-block:: python
   
   
   from fusion_hat.llm import OpenAI
   from secret import OPENAI_API_KEY
   import time
   from fusion_hat.stt import STT
   from fusion_hat.adc import ADC
   import math
   from fusion_hat.tts import Pico2Wave
   
   # Setup Text-to-Speech and Speech-to-Text
   tts = Pico2Wave()
   tts.set_lang('en-US')
   stt = STT(language="en-us")
   
   # Register OpenAI API
   # openai.com
   
   # Export your openai api key with :LLM_API_KEY
   # export LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
   
   # Setup ADC for thermistor reading on channel A3
   thermistor = ADC('A3')
   
   # Setup LLM with health assessment instructions
   INSTRUCTIONS = '''
   You are a health assistant. Your task is to assess the user's body temperature based on the thermistor reading and provide appropriate health advice.
   
   The thermistor reading represents body temperature in Celsius.
   
   ### Input Format:
   "thermistor: [value], message: [user query]"
   
   ### Output Guidelines:
   1. If temperature < 35.0°C, warn about hypothermia and suggest warming up.
   2. If 35.0°C ≤ temperature ≤ 37.5°C, confirm normal temperature and reassure the user.
   3. If 37.5°C < temperature ≤ 38.5°C, indicate mild fever and suggest rest and hydration.
   4. If temperature > 38.5°C, alert about high fever and recommend medical attention.
   5. Include the temperature value in your response to justify your assessment.
   6. Your reply should be brief and concise, no more than two sentences.
   
   ### Example Input:
   thermistor: 39.0, message: I feel unwell.
   
   ### Example Output:
   Your body temperature is 39.0°C, which indicates a high fever. Please rest, stay hydrated, and consider seeking medical advice if symptoms persist.
   '''
   
   WELCOME = "Hello, I am a health assistant. Please hold your thermometer and I will assess your body temperature based on the thermistor reading. If you feel unwell, please provide your symptoms and I will provide appropriate health advice."
   
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
   
   # Function to read and convert thermistor value to temperature
   def temperature():
       while True:
           # Read analog value (0-4095)
           analogVal = thermistor.read()
           
           # Calculate voltage across thermistor
           Vr = 3.3 * float(analogVal) / 4095
           
           # Check for sensor issues
           if 3.3 - Vr < 0.1:
               print("Please check the sensor")
               continue
           
           # Calculate thermistor resistance
           Rt = 10000 * Vr / (3.3 - Vr)
           
           # Convert resistance to temperature using Steinhart-Hart equation
           # B = 3950 (thermistor coefficient), R0 = 10000Ω at 25°C
           temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
           
           # Convert from Kelvin to Celsius
           Cel = temp - 273.15
           
           return Cel
   
   # Main loop for voice interaction
   while True:
       print("Say something")
       
       # Listen for speech input
       for result in stt.listen(stream=True):
           if result["done"]:
               # Print final recognized text
               print(f"\r\x1b[Kfinal: {result['final']}")
               
               # Measure temperature and combine with user query
               current_temp = temperature()
               input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"
               
               # Get response from LLM with streaming
               response = llm.prompt(input_text, stream=True)
               
               # Collect the full response
               string = ""
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       string += next_word
               
               # Speak the response
               tts.say(string)
               print("")  # New line after response
               
           else:
               # Print partial recognition results
               print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)

----------------------------------------------

**Code verstehen**

1. Initialisierung des Temperatursensors

   Der Thermistor ist mit dem ADC-Kanal A3 verbunden:
   
   .. code-block:: python
   
      thermistor = ADC('A3')
      
   Dadurch werden analoge Werte von 0–4095 gelesen, die Spannungspegel repräsentieren.

2. Temperaturumrechnung mit der Steinhart-Hart-Gleichung

   Der Thermistor verwendet die Steinhart-Hart-Gleichung für eine präzise Temperaturberechnung:
   
   .. code-block:: python
   
      # Analogen Wert lesen (0–4095)
      analogVal = thermistor.read()
      
      # In Spannung umrechnen (0–3.3 V)
      Vr = 3.3 * float(analogVal) / 4095
      
      # Thermistorwiderstand mit Spannungsteilerformel berechnen
      Rt = 10000 * Vr / (3.3 - Vr)
      
      # Steinhart-Hart-Gleichung: 1/T = 1/T0 + 1/B * ln(R/R0)
      temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
      
      # Kelvin in Celsius umrechnen
      Cel = temp - 273.15

3. Sensor-Fehlerprüfung

   Der Code enthält eine grundlegende Fehlererkennung:
   
   .. code-block:: python
   
      if 3.3 - Vr < 0.1:
          print("Please check the sensor")
          continue
      
   Damit wird erkannt, ob der Thermistor getrennt oder kurzgeschlossen ist.

4. Einrichtung der Spracherkennung

   Sowohl STT als auch TTS sind für Englisch konfiguriert:
   
   .. code-block:: python
   
      tts = Pico2Wave()
      tts.set_lang('en-US')
      stt = STT(language="en-us")

5. Aufbau der kontextbezogenen Eingabe

   Die Temperaturdaten werden mit der Benutzeranfrage kombiniert:
   
   .. code-block:: python
   
      current_temp = temperature()
      input_text = f"thermistor: {current_temp:.1f}, message: {result['final']}"
      
   Format: ``"thermistor: 37.2, message: I feel dizzy"``

6. Medizinische Klassifikationslogik

   Die AI-Anweisungen definieren Temperaturbereiche:
   
   .. code-block:: python
   
      # Temperaturbereiche für medizinische Einschätzung:
      # < 35.0°C: Warnung vor Unterkühlung
      # 35.0–37.5°C: Normalbereich
      # 37.5–38.5°C: Leichtes Fieber
      # > 38.5°C: Hohes Fieber

7. Sprachverarbeitung in Echtzeit

   Das System zeigt Teilergebnisse der Spracherkennung an:
   
   .. code-block:: python
   
      for result in stt.listen(stream=True):
          if result["done"]:
              # Endgültige Erkennung
              print(f"final: {result['final']}")
          else:
              # Teilweise Erkennung
              print(f"partial: {result['partial']}", end="", flush=True)

8. Gestreamte AI-Antwort

   Die AI-Antwort wird gestreamt und anschließend gesprochen:
   
   .. code-block:: python
   
      response = llm.prompt(input_text, stream=True)
      string = ""
      
      for next_word in response:
          if next_word:
              print(next_word, end="", flush=True)
              string += next_word
      
      tts.say(string)  # Vollständige Antwort sprechen

9. Temperaturformatierung

   Die Temperatur wird auf eine Dezimalstelle formatiert:
   
   .. code-block:: python
   
      f"thermistor: {current_temp:.1f}"
      
   Dadurch wird eine konsistente Genauigkeit sichergestellt (z. B. 36.5°C statt 36.512345°C).

10. Saubere Konsolenausgabe

    Verwendet ANSI-Escape-Codes für eine übersichtliche Ausgabe:
    
    .. code-block:: python
    
        print(f"\r\x1b[Kpartial: {result['partial']}", end="", flush=True)
        
    - ``\r``: Zum Anfang der Zeile zurückkehren  
    - ``\x1b[K``: Bis zum Zeilenende löschen  
    - Verhindert überlappenden Text während der Streaming-Ausgabe

----------------------------------------------

**Fehlerbehebung**

- Temperaturmessung ungenau

  - Überprüfen Sie die Verdrahtung des Thermistors: korrekte Spannungsteiler-Konfiguration
  - Prüfen Sie den Widerstandswert: sollte zum Nennwiderstand des Thermistors passen
  - Kalibrieren Sie mit einer bekannten Temperaturquelle
  - Überprüfen Sie die Referenzspannung des ADC (sollte stabil bei 3.3 V liegen)

- Keine Spracherkennung

  - Mikrofon testen: ``arecord --duration=3 test.wav && aplay test.wav``
  - Audiogerät bei der STT-Initialisierung überprüfen
  - Hintergrundgeräusche möglichst reduzieren
  - Deutlich und in moderatem Tempo sprechen

- AI antwortet nicht

  - Internetverbindung überprüfen
  - OpenAI-API-Schlüssel in ``secret.py`` kontrollieren
  - Sicherstellen, dass im OpenAI-Konto die Abrechnung aktiviert ist
  - Prüfen, ob API-Ratenlimits überschritten wurden

- Temperatur springt stark

  - Softwarefilter hinzufügen, z. B. gleitenden Mittelwert
  - Lose Verbindungen prüfen
  - Kondensator (0.1µF) parallel zum Thermistor zur Rauschunterdrückung hinzufügen
  - Sicherstellen, dass der Thermistor guten thermischen Kontakt hat

- Text-to-Speech funktioniert nicht

  - Audioausgabe testen: ``speaker-test -t sine -f 440``
  - Spracheinstellung prüfen: ``tts.set_lang('en-US')``
  - Lautstärke prüfen: ``alsamixer``
  - Audio-Setup-Skript erneut ausführen: ``sudo /opt/setup_fusion_hat_audio.sh``

- Sensorwert zeigt 0 oder 4095

  - Verdrahtung prüfen: Thermistor könnte kurzgeschlossen (0) oder offen (4095) sein
  - Berechnung des Spannungsteilers überprüfen
  - ADC mit bekannter Spannung testen
  - ADC-Kanal prüfen (sollte A3 sein)

**Sicherheits- und medizinischer Hinweis**

.. warning::

   Dieses Projekt dient ausschließlich **zu Bildungs- und Demonstrationszwecken**.  
   Es ist **KEIN medizinisches Gerät** und darf **NICHT** für echte medizinische Diagnosen oder Behandlungen verwendet werden.

#. Sicherheitsrichtlinien

   * Nicht für medizinische Nutzung: Treffen Sie keine Gesundheits- oder Behandlungsentscheidungen auf Grundlage dieses Systems.
   * Notfälle: Bei ernsthaften Symptomen immer professionelle medizinische Hilfe suchen.
   * Genauigkeitsgrenzen: Thermistoren sind weniger genau als medizinische Thermometer.
   * Kalibrierung erforderlich: Regelmäßige Kalibrierung mit einem medizinischen Thermometer ist notwendig.
   * Aufsicht empfohlen: Bei Nutzung zu Bildungszwecken wird die Aufsicht durch Erwachsene empfohlen.

#. Wann Sie medizinische Hilfe suchen sollten

   Suchen Sie professionelle medizinische Hilfe, wenn eines der folgenden Symptome auftritt:

   * Temperatur > 39.5°C (103.1°F) bei Erwachsenen
   * Temperatur > 38.0°C (100.4°F) bei Säuglingen unter 3 Monaten
   * Fieber länger als 3 Tage
   * Atembeschwerden oder Brustschmerzen
   * Starke Kopfschmerzen oder Nackensteifigkeit
   * Verwirrtheit oder Krampfanfälle

----------------------------------------------

Dieser AI-Gesundheitsassistent zeigt, wie Sensortechnologie, Sprachinteraktion und künstliche Intelligenz zusammenarbeiten können, um zugängliche Gesundheitsüberwachungssysteme zu erstellen – während gleichzeitig die Bedeutung professioneller medizinischer Beratung bei ernsthaften Gesundheitsproblemen betont wird.