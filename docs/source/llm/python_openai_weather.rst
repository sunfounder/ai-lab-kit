.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_smart_weather_station:

(Beispiel) Intelligente Wetterstation
=============================================

**Einführung**

Dieses Projekt erstellt eine umfassende **intelligente Wetterstation**, die lokale Umweltsensoren mit globalen Wetterdaten und AI-Analyse kombiniert. Das System integriert:

1. **Lokale Sensordaten** von DHT11 (Temperatur/Luftfeuchtigkeit) und LDR (Lichtsensor)
2. **Globale Wettervorhersagen** über die OpenWeather-API
3. **AI-gestützte Sprachanalyse** mit den GPT- und TTS-Funktionen von OpenAI
4. **Visuelle Anzeige** auf einem 128x64-OLED-Display
5. **Interaktive Taste** für spontane, AI-generierte Wetterauswertungen

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Smart_Weather_Station.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Die Wetterstation vergleicht automatisch lokale Bedingungen mit Vorhersagedaten und liefert intelligente Empfehlungen per Sprachausgabe. So entsteht eine vollständige Lösung zur Umgebungsüberwachung.

Sie können auch andere LLM- und TTS-Module verwenden, um Ihre eigenen intelligenten Geräte zu entwickeln.  
Siehe:

* :ref:`py_online_llm` 
* :ref:`tts_espeak_pico2wave` 
* :ref:`tts_piper_openai`

----------------------------------------------

**Was Sie benötigen**

Für dieses Projekt werden die folgenden Komponenten benötigt:

.. list-table::
    :widths: 30 20
    :header-rows: 1

    *   - COMPONENT
        - PURCHASE LINK
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

**Schaltplan**

Verbinden Sie die Komponenten wie folgt mit dem Fusion HAT+:

.. image:: img/fzz/llm_weather_bb.png
   :width: 80%
   :align: center


----------------------------------------------

.. include:: python_online_llms.rst
   :start-after: start_setup_openai
   :end-before: end_setup_openai

---------------------------------------------


**OpenWeather-API-Schlüssel abrufen**

|link_openweather| ist ein Onlinedienst der OpenWeather Ltd, der über eine API weltweite Wetterdaten bereitstellt, darunter aktuelle Wetterdaten, Vorhersagen, Nowcasts und historische Wetterdaten für jeden geografischen Ort.

#. Besuchen Sie |link_openweather| und melden Sie sich an bzw. erstellen Sie ein Konto.

    .. image:: img/OWM-1.png


#. Öffnen Sie über die Navigationsleiste die API-Seite.

    .. image:: img/OWM-2.png


#. Suchen Sie **Current Weather Data** und klicken Sie auf **Subscribe**.

    .. image:: img/OWM-3.png


#. Abonnieren Sie unter **Current weather and forecasts collection** den passenden Dienst. Für unser Projekt reicht die kostenlose Version völlig aus.

   .. image:: img/OWM-4.png


#. Kopieren Sie den Schlüssel von der Seite **API keys**.

   .. image:: img/OWM-5.png

#. Öffnen Sie die Datei ``secret.py`` mit folgendem Befehl:

   .. raw:: html

      <run></run>
   
   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. Fügen Sie den kopierten API-Schlüssel hinzu:

   
   .. code-block:: shell
      :emphasize-lines: 1

      OPENWEATHER_API_KEY = "732exxxxxxxxxxxxxxxxxxxxx919b"


#. Drücken Sie ``Ctrl + X``, ``Y`` und anschließend ``Enter``, um die Datei zu speichern und den Editor zu beenden.


---------------------------------------------

**Beispiel ausführen**

#. Code ausführen

   .. raw:: html

      <run></run>

   .. code-block:: shell

      cd ~/ai-lab-kit/llm
      sudo python3 llm_openai_weather.py

#. Was Sie nach dem Start des Skripts sehen

   * Das OLED schaltet sich ein und beginnt, Wetterinformationen anzuzeigen.
   * Das Programm gibt im Terminal Startinformationen aus, darunter die Zielstadt und den verwendeten Button-Pin.
   * Das OLED wechselt automatisch alle 10 Sekunden zwischen den Seiten (insgesamt 3 Seiten):

     - **Seite 1: Lokale Sensoren** (DHT11 + LDR)  
       Zeigt lokale Temperatur, Luftfeuchtigkeit und Lichtstärke an (einschließlich einer kleinen Lichtbalkenanzeige).

     - **Seite 2: Wettervorhersage** (OpenWeather)  
       Zeigt die aktuelle Temperatur, die Wetterbeschreibung und die letzte Aktualisierungszeit an.

     - **Seite 3: AI-Auswertung**  
       Zeigt die Unterschiede zwischen den lokalen Sensordaten und den OpenWeather-Daten sowie einen einfachen Komfortstatus an (z. B. Comfortable / Warm / Cool / Humid / Dry).

#. AI-Sprachanalyse auslösen

   Drücken Sie die Taste an **GPIO 27**, damit die AI eine kurze Analyse im Stil eines „Wetterreporters“ erstellt.

   * Im Terminal wird ein Abschnitt ``AI Analysis`` ausgegeben, einschließlich:

     - Lokale Messwerte (Temperatur / Luftfeuchtigkeit / Licht)
     - Externe Wetterdaten (OpenWeather-Temperatur + Beschreibung)
     - Eine kurze, von der AI erzeugte Zusammenfassung

   * Das OLED zeigt vorübergehend **SPEAKING...**
   * Die Analyse wird über den Lautsprecher mit OpenAI TTS gesprochen

#. Aktualisierungsverhalten der Daten

   * Die lokalen Sensoren werden etwa alle **2 Sekunden** aktualisiert.
   * Die OpenWeather-Daten werden etwa alle **5 Minuten** aktualisiert.
   * Der Lichtwert wird automatisch geglättet, um Flackern zu reduzieren.

#. Programm beenden

   * Drücken Sie im Terminal ``Ctrl+C``, um das Programm zu beenden.
   * Das OLED wird gelöscht und das Programm wird sicher beendet.


----------------------------------------------

**Code**

Hier ist das vollständige Python-Skript für die intelligente Wetterstation:

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

**Code verstehen**

1. Sensorintegration

   Das System liest Daten von zwei lokalen Sensoren aus:
   
   .. code-block:: python
   
      # DHT11 für Temperatur und Luftfeuchtigkeit
      dht = DHT11(pin=DHT_PIN)
      result = dht.read()  # Gibt (humidity, temperature) zurück
      
      # LDR (lichtabhängiger Widerstand) über ADC
      ldr = ADC(LDR_CH)
      raw = ldr.read()  # Gibt einen Wert von 0–4095 zurück

2. OpenWeather-API-Integration

   Die Klasse ``WeatherAPI`` verwaltet die Verbindung zu OpenWeather für aktuelle Wetterbedingungen und Vorhersagen:
   
   .. code-block:: python
   
      class WeatherAPI:
          def update_weather(self):
              # Endpoint für aktuelles Wetter
              response = requests.get(self.get_weather_url(), timeout=10)
              self.current_weather = response.json()
              
              # Endpoint für Vorhersage
              response = requests.get(self.get_forecast_url(), timeout=10)
              self.forecast = response.json()

3. AI-Analyse-Engine

   Die Klasse ``WeatherAI`` erzeugt intelligente Wetteranalysen und wandelt diese in Sprache um:
   
   .. code-block:: python
   
      class WeatherAI:
          def analyze_weather(self, local_temp, local_hum, local_light, weather_data):
              # Temperaturdifferenz berechnen
              temp_diff = abs(local_temp - weather_data.get('current_temp', local_temp))
              
              # Empfehlungen basierend auf den Bedingungen erstellen
              recommendations = []
              if local_hum > 80:
                  recommendations.append("It's quite humid")
              
              # Analyse-Text erstellen
              analysis = f"Local sensors show {local_temp:.1f}C..."
              return analysis
          
          def speak_analysis(self, analysis_text):
              self.tts.say(analysis_text, instructions="speak clearly...")

4. Mehrseitiges Display-System

   Der ``DisplayManager`` verwaltet drei Informationsseiten, die automatisch wechseln:
   
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
              # Temperatur, Luftfeuchtigkeit und Lichtstärke mit Fortschrittsbalken zeichnen

5. Button-Ereignisverarbeitung

   Beim Drücken der Taste wird eine AI-Sprachanalyse ausgelöst:
   
   .. code-block:: python
   
      button = Pin(BUTTON_PIN, mode=Mode.IN, pull=Pull.DOWN)
      button.when_activated = self._button_pressed
      
      def _button_pressed(self):
          # Sensoren aktualisieren, Analyse erstellen und sprechen
          analysis = self.weather_ai.analyze_weather(...)
          self.weather_ai.speak_analysis(analysis)

6. Daten-Glättung für den Lichtsensor

   Der Lichtsensor verwendet einen gleitenden Mittelwert für stabilere Messwerte:
   
   .. code-block:: python
   
      def light_percent(raw, min_val=0, max_val=4095):
          _light_window.append(raw)
          if len(_light_window) > 5:
              _light_window.pop(0)
          
          smooth_raw = int(mean(_light_window))  # Gleitender Durchschnitt
          pct = (smooth_raw - min_val) / (max_val - min_val) * 100

7. Hauptanwendungsschleife

   Die Klasse ``SmartWeatherStation`` koordiniert alle Komponenten mit korrektem Timing:
   
   .. code-block:: python
   
      def run(self):
          while True:
              # Sensoren alle 2 Sekunden aktualisieren
              if time.time() - self.last_sensor_update > SENSOR_UPDATE_INTERVAL:
                  self._update_sensors()
              
              # Wetterdaten alle 5 Minuten aktualisieren
              self._update_weather()
              
              # Seiten alle 10 Sekunden automatisch wechseln
              if self.display.should_change_page():
                  self.display.next_page()
              
              # Aktuelle Seite anzeigen
              self.display.draw_page(...)

----------------------------------------------

**Fehlerbehebung**

- Fehler „DHT11 read failed“

  - Verkabelung prüfen: VCC (3.3V), DATA (GPIO 17), GND  
  - Einen **10kΩ Pull-up-Widerstand** zwischen DATA und VCC hinzufügen  
  - Sensor von Wärmequellen fernhalten (Raspberry Pi kann selbst Wärme erzeugen)  
  - Kleine Verzögerung zwischen Messungen einfügen: ``time.sleep(2)``  

- OpenWeather-API-Fehler

  - Prüfen, ob der API-Schlüssel korrekt und gültig ist  
  - Internetverbindung testen: ``ping 8.8.8.8``  
  - Stadtname und Ländercode überprüfen  
  - Kostenlose API hat Limits (60 Aufrufe/Minute, 1.000.000 Aufrufe/Monat)

- OLED-Display zeigt nichts

  - I2C-Verbindung prüfen: ``sudo i2cdetect -y 1`` (sollte **0x3C** anzeigen)  
  - Prüfen, ob das OLED mit Strom versorgt wird (3.3V oder 5V je nach Modell)  
  - Richtige I2C-Adresse sicherstellen (0x3C oder 0x3D)

- Kein Ton bei TTS

  - Audioausgabe prüfen: ``sudo raspi-config`` → **System Options → Audio**  
  - Audiotest durchführen: ``speaker-test -t sine -f 440``  
  - Prüfen, ob der OpenAI-TTS-API-Schlüssel genügend Credits hat  
  - Internetverbindung für API-Aufrufe prüfen

- Button reagiert nicht

  - Verkabelung prüfen: Taste zwischen **GPIO 27** und **GND**  
  - Prüfen, ob Pull-down-Widerstand im Code aktiviert ist  
  - Taste mit einfachem Testskript überprüfen

- Ungenaue Lichtmessung

  - LDR kalibrieren, indem ``min_val`` und ``max_val`` in ``light_percent()`` angepasst werden  
  - LDR vollständig abdecken, um den Minimalwert zu bestimmen  
  - LDR hellem Licht aussetzen, um den Maximalwert zu bestimmen  
  - Sicherstellen, dass der LDR nicht im Schatten anderer Bauteile liegt

- Wetterdaten veraltet

  - ``WEATHER_UPDATE_INTERVAL`` erhöhen, um häufiger zu aktualisieren  
  - Prüfen, ob API-Aufrufe erfolgreich sind (Fehlermeldungen beachten)  
  - Systemzeit prüfen: ``date``

----------------------------------------------

Diese intelligente Wetterstation zeigt, wie **lokale Sensordaten**, **Cloud-Dienste** und **AI** kombiniert werden können, um ein fortschrittliches Umgebungsüberwachungssystem zu schaffen, das praktische Erkenntnisse und intelligente Empfehlungen liefert.