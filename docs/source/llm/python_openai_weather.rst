.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_smart_weather_station:

(Esempio) Stazione Meteorologica Intelligente
=================================================

**Introduzione**

Questo progetto crea una completa **Stazione Meteorologica Intelligente** che combina sensori ambientali locali con dati meteorologici globali e analisi AI. Il sistema integra:

1. **Dati da sensori locali** da DHT11 (temperatura/umidita') e LDR (sensore di luce)
2. **Previsioni meteorologiche globali** dall'API OpenWeather
3. **Analisi vocale basata su AI** utilizzando GPT di OpenAI e capacita' TTS
4. **Display visivo** su schermo OLED 128x64
5. **Pulsante interattivo** per approfondimenti meteorologici AI su richiesta

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Smart_Weather_Station.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

La stazione meteorologica confronta automaticamente le condizioni locali con i dati delle previsioni e fornisce raccomandazioni intelligenti attraverso l'output vocale, creando una soluzione completa di monitoraggio ambientale.

Puoi usare altri moduli LLM e moduli TTS per costruire i tuoi dispositivi intelligenti.
Vedi:

* :ref:`py_online_llm`
* :ref:`tts_espeak_pico2wave`
* :ref:`tts_piper_openai`

----------------------------------------------

**Cosa ti Servira'**

I seguenti componenti sono richiesti per questo progetto:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENTE
        - LINK D'ACQUISTO
    *   - :ref:`cpn_humiture_sensor`
        - |link_humiture_buy|
    *   - :ref:`cpn_photoresistor`
        - |link_photoresistor_buy|
    *   - :ref:`cpn_button`
        - |link_button_buy|
    *   - :ref:`cpn_oled`
        - \-
    *   - :ref:`cpn_fusion_hat`
        - \-
    *   - :ref:`cpn_wires`
        - |link_wires_buy|
    *   - :ref:`cpn_resistor`
        - |link_resistor_buy|
    *   - Raspberry Pi
        - \-

----------------------------------------------

**Schema di Collegamento**

Collega i componenti al Fusion HAT+ come segue:

.. image:: img/fzz/llm_weather_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

---------------------------------------------


**Ottieni le chiavi API OpenWeather**

|link_openweather| e' un servizio online, di proprieta' di OpenWeather Ltd, che fornisce dati meteorologici globali tramite API, inclusi dati meteo attuali, previsioni, nowcast e dati meteorologici storici per qualsiasi posizione geografica.

#. Visita |link_openweather| per accedere/creare un account.

    .. image:: img/OWM-1.png


#. Clicca sulla pagina API dalla barra di navigazione.

    .. image:: img/OWM-2.png


#. Trova **Current Weather Data** e clicca su Subscribe.

    .. image:: img/OWM-3.png


#. In **Current weather and forecasts collection**, sottoscrivi il servizio appropriato. Nel nostro progetto, Free e' sufficiente.

   .. image:: img/OWM-4.png


#. Copia la chiave dalla pagina **API keys**.

   .. image:: img/OWM-5.png

#. Apri il file ``secret.py`` con il seguente comando:

   .. raw:: html

      <run></run>

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Aggiungi la chiave API copiata:


   .. code-block:: shell
      :emphasize-lines: 1

      OPENWEATHER_API_KEY = "732exxxxxxxxxxxxxxxxxxxxx919b"


#. Premi ``Ctrl + X``, ``Y`` e poi ``Enter`` per salvare il file e uscire.


---------------------------------------------

**Esegui l'Esempio**

#. Esegui il codice

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_weather.py

#. Cosa vedrai dopo l'avvio dello script

   * L'OLED si accende e inizia a mostrare le informazioni meteorologiche.
   * Il programma stampa le informazioni di avvio nel terminale, inclusi la citta' di destinazione e il pin del pulsante.
   * L'OLED cambia automaticamente pagina ogni 10 secondi (3 pagine totali):

     - **Pagina 1: Sensori Locali** (DHT11 + LDR)
       Mostra temperatura locale, umidita' e livello di luce (con una piccola barra della luce).

     - **Pagina 2: Previsioni Meteo** (OpenWeather)
       Mostra la temperatura attuale, la descrizione del meteo e l'ora dell'ultimo aggiornamento.

     - **Pagina 3: Approfondimenti AI**
       Mostra le differenze tra le letture dei sensori locali e i dati OpenWeather, e uno stato di comfort semplice (ad esempio, Comodo / Caldo / Fresco / Umido / Secco).

#. Attiva l'analisi vocale AI

   Premi il pulsante sul **GPIO 27** per far generare all'AI una breve analisi in stile "meteorologo".

   * Il terminale stampera' una sezione ``AI Analysis``, includendo:

     - Letture locali (temperatura / umidita' / luce)
     - Meteo remoto (temperatura OpenWeather + descrizione)
     - Un breve riepilogo testuale generato dall'AI

   * L'OLED mostrera' temporaneamente **SPEAKING...**
   * L'analisi sara' pronunciata attraverso l'altoparlante usando OpenAI TTS

#. Comportamento dell'aggiornamento dei dati

   * I sensori locali si aggiornano circa ogni **2 secondi**.
   * I dati OpenWeather si aggiornano circa ogni **5 minuti**.
   * La lettura della luce viene livellata automaticamente per ridurre lo sfarfallio.

#. Ferma il programma

   * Premi ``Ctrl+C`` nel terminale per uscire.
   * L'OLED si spegne e il programma termina in modo sicuro.


----------------------------------------------

**Codice**

Ecco lo script Python completo per la Stazione Meteorologica Intelligente:

.. raw:: html

   <run></run>

.. code-block:: python

   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-

   """
   Smart Weather Station with AI Assistant
   - Reads local temperature & humidity from DHT11 on GPIO 17
   - Reads light level from LDR on ADC A0 (0..4095)
   - Fetches weather forecast from OpenWeather API
   - Provides AI voice analysis using OpenAI (triggered by button)
   - Displays all information on 128x64 SSD1306 OLED
   """

   import time
   import requests
   from datetime import datetime
   from statistics import mean
   from fusion_hat.modules import DHT11
   from fusion_hat.adc import ADC
   from fusion_hat.pin import Pin, Mode, Pull
   from PIL import Image, ImageDraw, ImageFont
   import adafruit_ssd1306
   import board
   from sunfounder_voice_assistant.tts import OpenAI_TTS
   from secret import OPENAI_API_KEY, OPENWEATHER_API_KEY
   from signal import pause

   # Configuration
   DHT_PIN = 17          # DHT11 uses GPIO 17
   LDR_CH = 0
   I2C_ADDR = 0x3C

   # OpenWeather API Configuration
   CITY_NAME = "Shanghai"
   COUNTRY_CODE = "CN"
   LATITUDE = 31.2304
   LONGITUDE = 121.4737
   UNITS = "metric"

   # Update intervals in seconds
   WEATHER_UPDATE_INTERVAL = 300
   SENSOR_UPDATE_INTERVAL = 2

   # GPIO Pins
   BUTTON_PIN = 27  # Button uses GPIO 27

   # OLED Setup
   WIDTH, HEIGHT = 128, 64
   i2c = board.I2C()
   oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=I2C_ADDR)
   oled.fill(0)
   oled.show()

   # Load fonts
   try:
       font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
       font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
       font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
   except:
       print("Warning: Using default font")
       font_small = ImageFont.load_default()
       font_medium = ImageFont.load_default()
       font_large = ImageFont.load_default()

   image = Image.new("1", (WIDTH, HEIGHT))
   draw = ImageDraw.Draw(image)

   # Sensors
   dht = DHT11(pin=DHT_PIN)
   ldr = ADC(LDR_CH)

   # Button for triggering AI analysis
   button = Pin(BUTTON_PIN, mode=Mode.IN, pull=Pull.DOWN)

   # OpenWeather API Class
   class WeatherAPI:
       def __init__(self, api_key, city, country_code, lat=None, lon=None):
           self.api_key = api_key
           self.city = city
           self.country_code = country_code
           self.lat = lat
           self.lon = lon
           self.current_weather = None
           self.forecast = None
           self.last_update = 0

       def get_weather_url(self):
           if self.lat and self.lon:
               return f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units={UNITS}"
           else:
               return f"https://api.openweathermap.org/data/2.5/weather?q={self.city},{self.country_code}&appid={self.api_key}&units={UNITS}"

       def get_forecast_url(self):
           if self.lat and self.lon:
               return f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&appid={self.api_key}&units={UNITS}"
           else:
               return f"https://api.openweathermap.org/data/2.5/forecast?q={self.city},{self.country_code}&appid={self.api_key}&units={UNITS}"

       def update_weather(self):
           try:
               # Current weather
               response = requests.get(self.get_weather_url(), timeout=10)
               if response.status_code == 200:
                   self.current_weather = response.json()
                   print(f"Weather API success: {self.current_weather['weather'][0]['description']}")
               else:
                   print(f"Weather API error: {response.status_code}")
                   return False

               # Forecast
               response = requests.get(self.get_forecast_url(), timeout=10)
               if response.status_code == 200:
                   self.forecast = response.json()

               self.last_update = time.time()
               return True

           except Exception as e:
               print(f"Weather API error: {e}")
               return False

       def get_temperature(self):
           if self.current_weather:
               return self.current_weather['main']['temp']
           return None

       def get_humidity(self):
           if self.current_weather:
               return self.current_weather['main']['humidity']
           return None

       def get_weather_description(self):
           if self.current_weather:
               return self.current_weather['weather'][0]['description'].title()
           return None

       def get_weather_condition(self):
           if self.current_weather:
               weather_id = self.current_weather['weather'][0]['id']
               if weather_id < 300:
                   return "TSTORM"
               elif weather_id < 600:
                   return "RAIN"
               elif weather_id < 700:
                   return "SNOW"
               elif weather_id == 800:
                   return "CLEAR"
               elif weather_id < 900:
                   return "CLOUDS"
               else:
                   return "OTHER"
           return "N/A"

       def get_forecast_summary(self):
           if not self.forecast or 'list' not in self.forecast:
               return "No forecast"

           forecasts = self.forecast['list'][:8]
           temps = [f['main']['temp'] for f in forecasts]
           min_temp = min(temps)
           max_temp = max(temps)

           conditions = {}
           for f in forecasts:
               condition = f['weather'][0]['main']
               conditions[condition] = conditions.get(condition, 0) + 1

           most_common = max(conditions, key=conditions.get)

           return f"{min_temp:.0f}-{max_temp:.0f}C {most_common}"

   # AI Weather Analyst Class
   class WeatherAI:
       def __init__(self, api_key):
           self.api_key = api_key
           self.tts = OpenAI_TTS(api_key=api_key)
           self.tts.set_voice(self.tts.Voice.ALLOY)
           self.is_speaking = False

       def analyze_weather(self, local_temp, local_hum, local_light, weather_data):
           temp_diff = abs(local_temp - weather_data.get('current_temp', local_temp)) if weather_data.get('current_temp') else 0

           if temp_diff > 3:
               accuracy = "significantly different from"
           elif temp_diff > 1:
               accuracy = "slightly different from"
           else:
               accuracy = "very close to"

           recommendations = []
           if local_hum > 80:
               recommendations.append("It's quite humid")
           elif local_hum < 30:
               recommendations.append("The air is dry")

           if local_light > 80:
               recommendations.append("It's bright here")
           elif local_light < 20:
               recommendations.append("It's quite dark")

           weather_desc = weather_data.get('weather_desc', '').lower()
           if 'rain' in weather_desc or 'drizzle' in weather_desc or 'thunderstorm' in weather_desc:
               recommendations.append("Don't forget an umbrella")
           elif 'clear' in weather_desc:
               recommendations.append("Great day to go outside")
           elif 'cloud' in weather_desc:
               recommendations.append("Partly cloudy today")

           rec_text = ". ".join(recommendations) + "." if recommendations else "Conditions are normal."

           analysis = f"Local sensors show {local_temp:.1f}C, which is {accuracy} the forecast. {rec_text}"
           return analysis

       def speak_analysis(self, analysis_text):
           if self.is_speaking:
               print("Already speaking, please wait...")
               return False

           try:
               self.is_speaking = True
               print(f"Speaking analysis: {analysis_text}")
               self.tts.say(analysis_text, instructions="speak clearly and professionally like a weather reporter")
               self.is_speaking = False
               return True
           except Exception as e:
               print(f"TTS error: {e}")
               self.is_speaking = False
               return False

   # Light sensor helper
   _light_window = []

   def light_percent(raw, min_val=0, max_val=4095):
       global _light_window

       _light_window.append(raw)
       if len(_light_window) > 5:
           _light_window.pop(0)

       smooth_raw = int(mean(_light_window))
       pct = (smooth_raw - min_val) / (max_val - min_val) * 100 if max_val > min_val else 50
       pct = max(0, min(100, pct))

       return int(pct), smooth_raw

   # Display Manager Class
   class DisplayManager:
       def __init__(self):
           self.current_page = 0
           self.num_pages = 3
           self.last_page_change = 0
           self.page_cycle_interval = 10

       def next_page(self):
           self.current_page = (self.current_page + 1) % self.num_pages
           self.last_page_change = time.time()

       def should_change_page(self):
           return time.time() - self.last_page_change > self.page_cycle_interval

       def draw_page(self, page_num, local_temp, local_hum, light_pct, weather_api, weather_ai):
           draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

           if page_num == 0:
               self._draw_local_sensors(local_temp, local_hum, light_pct)
           elif page_num == 1:
               self._draw_weather_forecast(weather_api)
           elif page_num == 2:
               self._draw_ai_insights(local_temp, local_hum, light_pct, weather_api)

           # Page indicator at bottom right
           indicator = f"{page_num+1}/{self.num_pages}"
           indicator_width = len(indicator) * 6
           draw.text((WIDTH - indicator_width - 2, HEIGHT - 10), indicator, font=font_small, fill=255)

       def _draw_local_sensors(self, temp, hum, light):
           # Title at top
           draw.text((2, 2), "LOCAL SENSORS", font=font_medium, fill=255)

           # Temperature - larger font on first line
           temp_text = f"Temp: {temp:.1f} C"
           draw.text((10, 18), temp_text, font=font_large, fill=255)

           # Humidity - second line
           hum_text = f"Humidity: {hum:.1f}%"
           draw.text((10, 38), hum_text, font=font_medium, fill=255)

           # Light with bar on same line
           light_text = f"Light: {light}%"
           draw.text((10, 53), light_text, font=font_small, fill=255)

           # Light bar positioned next to text, not overlapping
           bar_x = 60  # Position after "Light: XX%"
           bar_y = 55
           bar_width = 50
           bar_height = 4

           # Draw background bar
           draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), outline=255, fill=0)

           # Draw filled portion
           fill_width = int(bar_width * light / 100)
           if fill_width > 0:
               draw.rectangle((bar_x, bar_y, bar_x + fill_width, bar_y + bar_height), outline=0, fill=255)

       def _draw_weather_forecast(self, weather_api):
           draw.text((2, 2), "WEATHER", font=font_medium, fill=255)

           if not weather_api.current_weather:
               draw.text((10, 25), "No weather data", font=font_medium, fill=255)
               draw.text((10, 45), "Check connection", font=font_small, fill=255)
               return

           current_temp = weather_api.get_temperature()
           weather_desc = weather_api.get_weather_description()
           weather_cond = weather_api.get_weather_condition()

           # Temperature - large font
           if current_temp is not None:
               draw.text((10, 18), f"{current_temp:.0f} C", font=font_large, fill=255)

           # Weather description
           if weather_desc:
               desc_text = weather_desc[:15]
               draw.text((10, 38), desc_text, font=font_medium, fill=255)

           # Weather condition
           if weather_cond:
               draw.text((10, 53), weather_cond, font=font_small, fill=255)

           # Update time at top right
           if weather_api.last_update > 0:
               update_time = datetime.fromtimestamp(weather_api.last_update).strftime("%H:%M")
               update_text = f"Up: {update_time}"
               update_width = len(update_text) * 6
               draw.text((WIDTH - update_width - 2, 2), update_text, font=font_small, fill=255)

       def _draw_ai_insights(self, local_temp, local_hum, light_pct, weather_api):
           draw.text((2, 2), "AI INSIGHTS", font=font_medium, fill=255)

           api_temp = weather_api.get_temperature() if weather_api.current_weather else None
           api_hum = weather_api.get_humidity() if weather_api.current_weather else None

           line_y = 18

           # Temperature difference
           if api_temp is not None:
               temp_diff = local_temp - api_temp
               temp_symbol = "+" if temp_diff > 0 else "" if temp_diff == 0 else ""
               diff_text = f"Temp: {temp_symbol}{temp_diff:.1f}C"
               draw.text((10, line_y), diff_text, font=font_medium, fill=255)
               line_y += 15

           # Humidity difference
           if api_hum is not None:
               hum_diff = local_hum - api_hum
               hum_symbol = "+" if hum_diff > 0 else "" if hum_diff == 0 else ""
               diff_text = f"Hum: {hum_symbol}{hum_diff:.1f}%"
               draw.text((10, line_y), diff_text, font=font_medium, fill=255)
               line_y += 15

           # Comfort level
           comfort = "Normal"
           comfort_color = 255

           if 20 <= local_temp <= 25 and 40 <= local_hum <= 60:
               comfort = "Comfortable"
               comfort_color = 255
           elif local_temp > 28:
               comfort = "Warm"
               comfort_color = 255
           elif local_temp < 16:
               comfort = "Cool"
               comfort_color = 255
           elif local_hum > 70:
               comfort = "Humid"
               comfort_color = 255
           elif local_hum < 30:
               comfort = "Dry"
               comfort_color = 255

           draw.text((10, line_y), f"Feel: {comfort}", font=font_small, fill=comfort_color)

           # Button hint at bottom left
           draw.text((2, HEIGHT - 10), "Press BTN for AI", font=font_small, fill=255)

   # Main Application Class
   class SmartWeatherStation:
       def __init__(self):
           print("Initializing Smart Weather Station...")

           self.weather_api = WeatherAPI(OPENWEATHER_API_KEY, CITY_NAME, COUNTRY_CODE, LATITUDE, LONGITUDE)
           self.weather_ai = WeatherAI(OPENAI_API_KEY)
           self.display = DisplayManager()

           self.local_temp = 0.0
           self.local_hum = 0.0
           self.light_pct = 0
           self.raw_adc = 0

           self.last_weather_update = 0
           self.last_sensor_update = 0

           # Setup button callback
           button.when_activated = self._button_pressed

           # Initial readings
           self._update_sensors()
           self.weather_api.update_weather()

           print("Smart Weather Station ready!")
           print(f"City: {CITY_NAME}")
           print(f"Temperature unit: {UNITS}")
           print(f"Button on GPIO {BUTTON_PIN} for AI analysis")
           print("="*50)

       def _update_sensors(self):
           try:
               result = dht.read()
               if result:
                   hum, temp = result
                   self.local_hum = float(hum)
                   self.local_temp = float(temp)

               raw = ldr.read()
               self.light_pct, self.raw_adc = light_percent(raw)

               self.last_sensor_update = time.time()
               return True

           except Exception as e:
               print(f"Sensor error: {e}")
               return False

       def _update_weather(self):
           if time.time() - self.last_weather_update > WEATHER_UPDATE_INTERVAL:
               print("Updating weather data...")
               if self.weather_api.update_weather():
                   self.last_weather_update = time.time()
                   return True
           return False

       def _button_pressed(self):
           """Called when button is pressed"""
           print("\n" + "="*50)
           print("Button pressed! Triggering AI analysis...")
           print("="*50)

           # Update sensors first to get latest data
           self._update_sensors()

           # Get weather data
           api_temp = self.weather_api.get_temperature()

           if api_temp is None:
               print("No weather data available. Please wait for update.")
               return

           # Prepare weather data for analysis
           weather_data = {
               'current_temp': api_temp,
               'weather_desc': self.weather_api.get_weather_description(),
               'forecast_summary': self.weather_api.get_forecast_summary()
           }

           # Generate analysis
           analysis = self.weather_ai.analyze_weather(
               self.local_temp,
               self.local_hum,
               self.light_pct,
               weather_data
           )

           print(f"\nAI Analysis:")
           print(f"Local: {self.local_temp:.1f}C, {self.local_hum:.1f}%, Light: {self.light_pct}%")
           print(f"Remote: {api_temp}C, {self.weather_api.get_weather_description()}")
           print(f"Analysis: {analysis}")

           # Show "Speaking..." on display
           self._show_speaking_message()

           # Speak the analysis
           success = self.weather_ai.speak_analysis(analysis)

           if success:
               print("Analysis completed successfully!")
           else:
               print("Analysis failed or interrupted.")

           print("="*50)

       def _show_speaking_message(self):
           """Display a temporary "Speaking..." message"""
           draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
           draw.text((WIDTH//2 - 40, HEIGHT//2 - 10), "SPEAKING...", font=font_medium, fill=255)
           oled.image(image)
           oled.show()

       def run(self):
           print("\n" + "="*50)
           print("SMART WEATHER STATION")
           print("="*50)
           print("Display Pages:")
           print("1. Local Sensors (DHT11 + LDR)")
           print("2. Weather Forecast (OpenWeather)")
           print("3. AI Insights (Comparisons)")
           print("")
           print(f"Press button on GPIO {BUTTON_PIN} for AI voice analysis")
           print("Press Ctrl+C to exit")
           print("="*50 + "\n")

           try:
               while True:
                   current_time = time.time()

                   # Update sensors periodically
                   if current_time - self.last_sensor_update > SENSOR_UPDATE_INTERVAL:
                       self._update_sensors()

                   # Update weather data periodically
                   self._update_weather()

                   # Auto-cycle display pages
                   if self.display.should_change_page():
                       self.display.next_page()

                   # Draw current page
                   self.display.draw_page(
                       self.display.current_page,
                       self.local_temp,
                       self.local_hum,
                       self.light_pct,
                       self.weather_api,
                       self.weather_ai
                   )

                   # Update OLED display
                   oled.image(image)
                   oled.show()

                   # Small delay to prevent CPU overload
                   time.sleep(0.1)

           except KeyboardInterrupt:
               print("\nShutting down...")

           finally:
               # Cleanup
               oled.fill(0)
               oled.show()
               print("Smart Weather Station stopped.")

   # Main Entry Point
   if __name__ == "__main__":
       if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
           print("ERROR: Please set your OpenAI API key in secret.py")
           exit(1)

       if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your-openweather-api-key-here":
           print("ERROR: Please set your OpenWeather API key in secret.py")
           print("Get one at: https://openweathermap.org/api")
           exit(1)

       station = SmartWeatherStation()
       station.run()

----------------------------------------------

**Comprensione del Codice**

1. Integrazione dei Sensori

   Il sistema legge da due sensori locali:

   .. code-block:: python

      # DHT11 per temperatura e umidita'
      dht = DHT11(pin=DHT_PIN)
      result = dht.read()  # Restituisce (umidita', temperatura)

      # LDR (Resistore Dipendente dalla Luce) tramite ADC
      ldr = ADC(LDR_CH)
      raw = ldr.read()  # Restituisce valore 0-4095

2. Integrazione API OpenWeather

   La classe WeatherAPI gestisce le connessioni a OpenWeather per condizioni attuali e previsioni:

   .. code-block:: python

      class WeatherAPI:
          def update_weather(self):
              # Endpoint meteo attuale
              response = requests.get(self.get_weather_url(), timeout=10)
              self.current_weather = response.json()

              # Endpoint previsioni
              response = requests.get(self.get_forecast_url(), timeout=10)
              self.forecast = response.json()

3. Motore di Analisi AI

   La classe WeatherAI genera approfondimenti meteorologici intelligenti e li converte in parlato:

   .. code-block:: python

      class WeatherAI:
          def analyze_weather(self, local_temp, local_hum, local_light, weather_data):
              # Calcola la differenza di temperatura
              temp_diff = abs(local_temp - weather_data.get('current_temp', local_temp))

              # Genera raccomandazioni basate sulle condizioni
              recommendations = []
              if local_hum > 80:
                  recommendations.append("It's quite humid")

              # Combina in testo di analisi
              analysis = f"Local sensors show {local_temp:.1f}C..."
              return analysis

          def speak_analysis(self, analysis_text):
              self.tts.say(analysis_text, instructions="speak clearly...")

4. Sistema di Display Multi-Pagina

   DisplayManager gestisce tre pagine informative che ruotano automaticamente:

   .. code-block:: python

      class DisplayManager:
          def draw_page(self, page_num, ...):
              if page_num == 0:
                  self._draw_local_sensors(...)
              elif page_num == 1:
                  self._draw_weather_forecast(...)
              elif page_num == 2:
                  self._draw_ai_insights(...)

          def _draw_local_sensors(self, temp, hum, light):
              # Mostra temperatura, umidita' e livello di luce con barra di progresso

5. Gestione degli Eventi del Pulsante

   Il pulsante attiva l'analisi vocale AI quando premuto:

   .. code-block:: python

      button = Pin(BUTTON_PIN, mode=Mode.IN, pull=Pull.DOWN)
      button.when_activated = self._button_pressed

      def _button_pressed(self):
          # Aggiorna sensori, genera analisi e pronuncia
          analysis = self.weather_ai.analyze_weather(...)
          self.weather_ai.speak_analysis(analysis)

6. Livellamento dei Dati per il Sensore di Luce

   Il sensore di luce utilizza la media mobile per letture stabili:

   .. code-block:: python

      def light_percent(raw, min_val=0, max_val=4095):
          _light_window.append(raw)
          if len(_light_window) > 5:
              _light_window.pop(0)

          smooth_raw = int(mean(_light_window))  # Media mobile
          pct = (smooth_raw - min_val) / (max_val - min_val) * 100

7. Ciclo Principale dell'Applicazione

   La classe SmartWeatherStation coordina tutti i componenti con temporizzazione appropriata:

   .. code-block:: python

      def run(self):
          while True:
              # Aggiorna sensori ogni 2 secondi
              if time.time() - self.last_sensor_update > SENSOR_UPDATE_INTERVAL:
                  self._update_sensors()

              # Aggiorna meteo ogni 5 minuti
              self._update_weather()

              # Cambio pagina automatico ogni 10 secondi
              if self.display.should_change_page():
                  self.display.next_page()

              # Disegna pagina corrente
              self.display.draw_page(...)

----------------------------------------------

**Risoluzione dei Problemi**

- Errori "DHT11 read failed"

  - Assicura un cablaggio corretto: VCC (3.3V), DATA (GPIO 17), GND
  - Aggiungi un resistore pull-up da 10k ohm tra DATA e VCC
  - Tieni il sensore lontano da fonti di calore (il Raspberry Pi stesso puo' scaldarsi)
  - Prova ad aggiungere un piccolo ritardo tra le letture: ``time.sleep(2)``

- Errore API OpenWeather

  - Verifica che la tua chiave API sia corretta e non scaduta
  - Controlla la connessione Internet: ``ping 8.8.8.8``
  - Assicurati di usare il nome della citta' e il codice paese corretti
  - Il piano gratuito ha limiti di velocita' (60 chiamate/minuto, 1.000.000 chiamate/mese)

- Display OLED non visualizzato

  - Controlla la connessione I2C: ``sudo i2cdetect -y 1`` (dovrebbe mostrare 0x3C)
  - Verifica che l'OLED sia alimentato (3.3V o 5V a seconda del modello)
  - Assicurati dell'indirizzo I2C corretto (0x3C o 0x3D)

- Nessun suono dal TTS

  - Controlla la configurazione dell'uscita audio: ``sudo raspi-config`` -> **System Options** -> **Audio**
  - Prova l'audio: ``speaker-test -t sine -f 440``
  - Verifica che la chiave API OpenAI TTS abbia crediti sufficienti
  - Controlla la connettivita' Internet per le chiamate API

- Il pulsante non risponde

  - Verifica il cablaggio: pulsante tra GPIO 27 e GND
  - Controlla che il resistore pull-down sia configurato nel codice
  - Prova il pulsante con uno script semplice per verificarne la funzionalita'

- Letture di luce inaccurate

  - Calibra LDR regolando min_val e max_val in light_percent()
  - Copri completamente LDR per la lettura del valore minimo
  - Esponi alla luce intensa per la lettura del valore massimo
  - Assicurati che LDR non sia in ombra di altri componenti

- Dati meteo obsoleti

  - Aumenta WEATHER_UPDATE_INTERVAL per aggiornamenti piu' frequenti
  - Controlla se le chiamate API hanno successo (cerca messaggi di errore)
  - Verifica che l'ora di sistema sia corretta: ``date``

----------------------------------------------

Questa stazione meteorologica intelligente dimostra come i dati dei sensori locali, i servizi cloud e l'AI possano essere combinati per creare un sofisticato sistema di monitoraggio ambientale che fornisce approfondimenti utilizzabili e raccomandazioni intelligenti!
