.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. Lokaler Sprach-Chatbot
===========================

In dieser Lektion kombinieren Sie alles, was Sie bisher gelernt haben — **Spracherkennung (STT)**,  
**Text-to-Speech (TTS)** und ein **lokales LLM (Ollama)** —, um einen vollständig offline arbeitenden **Sprach-Chatbot**  
zu erstellen, der auf Ihrem Fusion HAT+ läuft.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Local_Voice_Chatbot.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

Der Ablauf ist einfach:

#. **Zuhören** — Das Mikrofon erfasst Ihre Sprache und transkribiert sie mit **Vosk**.  
#. **Denken** — Der Text wird an ein lokales **LLM** gesendet, das über Ollama läuft (z. B. ``llama3.2:3b``).  
#. **Sprechen** — Der Chatbot antwortet laut mit **Piper TTS**.  

So entsteht ein **freihändig nutzbarer Gesprächsroboter**, der Sie in Echtzeit verstehen und beantworten kann.

----

Bevor Sie beginnen
---------------------------------

Stellen Sie sicher, dass Sie Folgendes vorbereitet haben:

* **Piper TTS** getestet haben (:ref:`test_piper`) und ein funktionierendes Sprachmodell ausgewählt haben.  
* **Vosk STT** getestet haben (:ref:`test_vosk`) und das passende Sprachpaket gewählt haben (z. B. ``en-us``).  
* **Ollama** installiert haben (:ref:`download_ollama`) — entweder auf Ihrem Pi oder auf einem anderen Computer — und ein Modell wie ``llama3.2:3b`` heruntergeladen haben (oder ein kleineres wie ``moondream:1.8b``, falls der Speicher begrenzt ist).

----

Code ausführen
--------------

#. Öffnen Sie das Beispielskript:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano local_voice_chatbot.py

#. Passen Sie die Parameter bei Bedarf an:

   * ``stt = Vosk(language="en-us")``: Ändern Sie dies so, dass es zu Ihrem Akzent bzw. Sprachpaket passt (z. B. ``en-us``, ``zh-cn``, ``es``).  
   * ``tts.set_model("en_US-amy-low")``: Ersetzen Sie dies durch das Piper-Sprachmodell, das Sie in :ref:`test_piper` geprüft haben.  
   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``: Aktualisieren Sie sowohl ``ip`` als auch ``model`` entsprechend Ihrer Konfiguration.  

     * ``ip``: Wenn Ollama auf **demselben Pi** läuft, verwenden Sie ``localhost``. Wenn Ollama auf einem anderen Computer im lokalen Netzwerk läuft, aktivieren Sie in Ollama **Expose to network** und setzen ``ip`` auf die LAN-IP dieses Computers.  
     * ``model``: Muss exakt mit dem Modellnamen übereinstimmen, den Sie in Ollama heruntergeladen bzw. aktiviert haben.  

#. Führen Sie das Skript aus:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo python3 local_voice_chatbot.py

#. Nach dem Start sollten Sie Folgendes sehen:

   * Der Bot begrüßt Sie mit einer gesprochenen Willkommensnachricht.  
   * Er wartet auf Spracheingabe.  
   * Vosk transkribiert Ihre Sprache in Text.  
   * Der Text wird an Ollama gesendet, das die Antwort als Stream zurückgibt.  
   * Die Antwort wird bereinigt (versteckte Denkprozesse werden entfernt) und anschließend von Piper laut gesprochen.  
   * Sie können das Programm jederzeit mit ``Ctrl+C`` beenden.

----

Code
----

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

   # Initialize speech recognition
   stt = Vosk(language="en-us")

   # Initialize TTS
   tts = Piper()
   tts.set_model("en_US-amy-low")

   # Instructions for the LLM
   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

   # Initialize Ollama connection
   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

   # Utility: clean hidden reasoning
   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

   def main():
       print(WELCOME)
       tts.say(WELCOME)

       try:
           while True:
               print("\n🎤 Listening... (Press Ctrl+C to stop)")

               # Collect final transcript from Vosk
               text = ""
               for result in stt.listen(stream=True):
                   if result["done"]:
                       text = result["final"].strip()
                       print(f"[YOU] {text}")
                   else:
                       print(f"[YOU] {result['partial']}", end="\r", flush=True)

               if not text:
                   print("[INFO] Nothing recognized. Try again.")
                   time.sleep(0.1)
                   continue

               # Query Ollama with streaming
               reply_accum = ""
               response = llm.prompt(text, stream=True)
               for next_word in response:
                   if next_word:
                       print(next_word, end="", flush=True)
                       reply_accum += next_word
               print("")

               # Clean and speak
               clean = strip_thinking(reply_accum)
               if clean:
                   tts.say(clean)
               else:
                   tts.say("Sorry, I didn't catch that.")

               time.sleep(0.05)

       except KeyboardInterrupt:
           print("\n[INFO] Stopping...")
       finally:
           tts.say("Goodbye!")
           print("Bye.")

   if __name__ == "__main__":
       main()

----

Code-Analyse
-------------

**Importe und globale Initialisierung**

.. code-block:: python

   import re
   import time
   from fusion_hat.llm import Ollama
   from fusion_hat.stt import Vosk
   from fusion_hat.tts import Piper

Bindet die drei Untersysteme ein, die Sie zuvor verwendet haben:
**Vosk** für Speech-to-Text (STT), **Ollama** für das LLM und **Piper** für Text-to-Speech (TTS).



**STT initialisieren (Vosk)**

.. code-block:: python

   stt = Vosk(language="en-us")

Lädt das Vosk-Modell für US-Englisch.  
Ändern Sie den Sprachcode (z. B. ``zh-cn``, ``es``), damit er zu Ihrem Sprachpaket passt und eine bessere Erkennungsgenauigkeit erreicht wird.



**TTS initialisieren (Piper)**

.. code-block:: python

   tts = Piper()
   tts.set_model("en_US-amy-low")

Erstellt eine Piper-Engine und wählt eine bestimmte Stimme aus.  
Wählen Sie ein Modell, das Sie bereits in :ref:`test_piper` getestet haben. Stimmen mit geringerer Qualität sind schneller und benötigen weniger CPU-Leistung.



**LLM-Anweisungen und Begrüßungstext**

.. code-block:: python

   INSTRUCTIONS = (
       "You are a helpful assistant. Answer directly in plain English. "
       "Do NOT include any hidden thinking, analysis, or tags like <think>."
   )
   WELCOME = "Hello! I'm your voice chatbot. Speak when you're ready."

Hier gibt es zwei wichtige UX-Entscheidungen:

* Halten Sie die **Antworten kurz und direkt** (das verbessert die Verständlichkeit bei TTS).
* Verhindern Sie ausdrücklich versteckte „Chain-of-Thought“-Tags, um störende Ausgaben zu reduzieren.



**Mit Ollama verbinden und den Gesprächsumfang festlegen**

.. code-block:: python

   llm = Ollama(ip="localhost", model="llama3.2:3b")
   llm.set_max_messages(20)
   llm.set_instructions(INSTRUCTIONS)

* ``ip="localhost"`` setzt voraus, dass der Ollama-Server auf demselben Pi läuft. Wenn er auf einem anderen Gerät im lokalen Netzwerk läuft, tragen Sie die **LAN-IP** dieses Computers ein und aktivieren Sie in Ollama *Expose to network*.
* ``set_max_messages(20)`` begrenzt den Gesprächsverlauf auf eine kurze Historie. Reduzieren Sie diesen Wert, wenn Arbeitsspeicher oder Reaktionszeit knapp sind.

**Versteckte Denkprozesse / Tags vor der Sprachausgabe entfernen**

.. code-block:: python

   def strip_thinking(text: str) -> str:
       if not text:
           return ""
       text = re.sub(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"<\s*thinking[^>]*>.*?<\s*/\s*thinking\s*>", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"```(?:\s*thinking)?\s*.*?```", "", text, flags=re.DOTALL|re.IGNORECASE)
       text = re.sub(r"\[/?thinking\]", "", text, flags=re.IGNORECASE)
       return re.sub(r"\s+\n", "\n", text).strip()

Einige Modelle geben möglicherweise interne Tags aus (z. B. ``<think>…``).  
Diese Funktion entfernt solche Inhalte, damit Ihre TTS-Ausgabe **nur** die endgültige Antwort spricht.

**Tipp:** Wenn Sie andere Artefakte auf dem Bildschirm sehen (weil rohe Tokens gestreamt werden), sorgt diese Funktion bereits dafür, dass die **gesprochene** Ausgabe sauber bleibt.

**Hauptschleife: einmal begrüßen, dann zuhören → denken → sprechen**

.. code-block:: python

   print(WELCOME)
   tts.say(WELCOME)

Begrüßt den Benutzer über das Terminal und den Lautsprecher. Dies geschieht einmal beim Start.

**Zuhören (streamendes STT mit Live-Teilergebnissen)**

.. code-block:: python

   print("\n🎤 Listening... (Press Ctrl+C to stop)")

   text = ""
   for result in stt.listen(stream=True):
       if result["done"]:
           text = result["final"].strip()
           print(f"[YOU] {text}")
       else:
           print(f"[YOU] {result['partial']}", end="\r", flush=True)

* ``stream=True`` liefert **Teilergebnisse** für sofortiges Feedback und ein **Endergebnis**, sobald die Äußerung abgeschlossen ist.
* Der endgültig erkannte Text wird in ``text`` gespeichert und einmal ausgegeben.

**Schutzmechanismus:** Wenn nichts erkannt wurde, wird der LLM-Aufruf übersprungen:

.. code-block:: python

   if not text:
       print("[INFO] Nothing recognized. Try again.")
       time.sleep(0.1)
       continue

Dadurch werden keine leeren Eingaben an das Modell gesendet (das spart Zeit und Tokens).

**Denken (LLM) mit gestreamter Ausgabe**

.. code-block:: python

   reply_accum = ""
   response = llm.prompt(text, stream=True)
   for next_word in response:
       if next_word:
           print(next_word, end="", flush=True)
           reply_accum += next_word
   print("")

* Sendet den finalen Transkripttext an das lokale LLM und **gibt Tokens sofort aus**, sobald sie eintreffen, um eine geringe Latenz zu erreichen.
* Gleichzeitig wird die vollständige Antwort in ``reply_accum`` gesammelt, damit sie anschließend weiterverarbeitet werden kann.

**Hinweis:** Wenn Sie **keine** rohen Tokens anzeigen möchten, setzen Sie ``stream=False`` und geben nur den fertigen Text aus.

**Sprechen (zuerst bereinigen, dann TTS einmal ausführen)**

.. code-block:: python

   clean = strip_thinking(reply_accum)
   if clean:
       tts.say(clean)
   else:
       tts.say("Sorry, I didn't catch that.")

* Bereinigt den finalen Text, entfernt versteckte Tags und **spricht dann genau einmal**.  
* Wenn TTS nur einmal ausgeführt wird, werden wiederholte Ausgaben wie „[LLM] / [SAY]“ vermieden.


**Beenden und Aufräumen**

.. code-block:: python

   except KeyboardInterrupt:
       print("\n[INFO] Stopping...")
   finally:
       tts.say("Goodbye!")
       print("Bye.")

Verwenden Sie **Ctrl+C**, um das Programm zu beenden. Der Bot spricht zum Abschluss eine kurze Verabschiedung, um einen sauberen Programmende zu signalisieren.


----

Fehlerbehebung & FAQ
---------------------

* **Das Modell ist zu groß (Speicherfehler)**

  Verwenden Sie ein kleineres Modell wie ``moondream:1.8b`` oder führen Sie Ollama auf einem leistungsstärkeren Computer aus.  

* **Keine Antwort von Ollama**

  Stellen Sie sicher, dass Ollama läuft (``ollama serve`` oder Desktop-App geöffnet). Wenn Sie einen entfernten Rechner verwenden, aktivieren Sie **Expose to network** und prüfen Sie die IP-Adresse.  

* **Vosk erkennt Sprache nicht** 

  Überprüfen Sie, ob Ihr Mikrofon funktioniert. Versuchen Sie bei Bedarf ein anderes Sprachpaket (``zh-cn``, ``es`` usw.).  

* **Piper bleibt stumm oder meldet Fehler**  

  Stellen Sie sicher, dass das ausgewählte Sprachmodell heruntergeladen wurde und in :ref:`test_piper` getestet worden ist.  

* **Die Antworten sind zu lang oder weichen vom Thema ab**

  Bearbeiten Sie ``INSTRUCTIONS`` und fügen Sie hinzu: **„Keep answers short and to the point.“**  