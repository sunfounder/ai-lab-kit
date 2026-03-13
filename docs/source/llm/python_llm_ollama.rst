.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

4. Text, Vision und Sprache mit Ollama
=================================================

In dieser Lektion lernen Sie, wie Sie **Ollama** verwenden – ein Werkzeug zum lokalen Ausführen großer Sprach- und Vision-Modelle.  
Wir zeigen Ihnen, wie Sie Ollama installieren, ein Modell herunterladen und Fusion HAT+ damit verbinden.  

Mit dieser Konfiguration kann Fusion HAT+ ein Kamerabild aufnehmen, und das Modell kann es **sehen und beschreiben** —  
Sie können beliebige Fragen zum Bild stellen, und das Modell antwortet in natürlicher Sprache.

.. _download_ollama:

1. Ollama (LLM) installieren und Modell herunterladen
------------------------------------------------------------------

Sie können selbst entscheiden, wo Sie **Ollama** installieren möchten: 

* Auf Ihrem Raspberry Pi (lokale Ausführung)  
* Oder auf einem anderen Computer (Mac/Windows/Linux) im **gleichen lokalen Netzwerk**  

**Empfohlene Modelle je nach Hardware**

Sie können jedes Modell verwenden, das auf |link_ollama_hub| verfügbar ist.  
Modelle gibt es in unterschiedlichen Größen (3B, 7B, 13B, 70B ...).  
Kleinere Modelle laufen schneller und benötigen weniger Speicher, während größere Modelle eine bessere Qualität liefern, dafür aber leistungsfähigere Hardware erfordern.

Die folgende Tabelle hilft Ihnen dabei, die passende Modellgröße für Ihr Gerät auszuwählen.

.. list-table::
   :header-rows: 1
   :widths: 20 20 40

   * - Modellgröße
     - Erforderlicher Mindest-RAM
     - Empfohlene Hardware
   * - ~3B Parameter
     - 8GB (16GB besser)
     - Raspberry Pi 5 (16GB) oder PC/Mac der Mittelklasse
   * - ~7B Parameter
     - 16GB+
     - Pi 5 (16GB, gerade noch nutzbar) oder PC/Mac der Mittelklasse
   * - ~13B Parameter
     - 32GB+
     - Desktop-PC / Mac mit viel RAM
   * - 30B+ Parameter
     - 64GB+
     - Workstation / Server / GPU empfohlen
   * - 70B+ Parameter
     - 128GB+
     - High-End-Server mit mehreren GPUs

**Auf dem Raspberry Pi installieren**

Wenn Sie Ollama direkt auf Ihrem Raspberry Pi ausführen möchten:

* Verwenden Sie ein **64-Bit-Raspberry-Pi-OS**  
* Nachdrücklich empfohlen: **Raspberry Pi 5 (16GB RAM)**  

Führen Sie die folgenden Befehle aus:

.. code-block:: bash

   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull a lightweight model (good for testing)
   ollama pull llama3.2:3b

   # Quick run test (type 'hi' and press Enter)
   ollama run llama3.2:3b

   # Serve the API (default port 11434)
   # Tip: set OLLAMA_HOST=0.0.0.0 to allow access from LAN
   OLLAMA_HOST=0.0.0.0 ollama serve

**Auf Mac / Windows / Linux installieren (Desktop-App)**

1. Laden Sie Ollama von |link_ollama| herunter und installieren Sie es.  

   .. image:: img/llm_ollama_download.png

2. Öffnen Sie die Ollama-App, gehen Sie zum **Model Selector** und verwenden Sie die Suchleiste, um ein Modell zu finden. Geben Sie zum Beispiel ``llama3.2:3b`` ein (ein kleines und leichtgewichtiges Modell für den Einstieg).  

   .. image:: img/llm_ollama_choose.png

3. Sobald der Download abgeschlossen ist, geben Sie im Chatfenster etwas Einfaches wie „Hi“ ein. Ollama beginnt beim ersten Verwenden des Modells automatisch mit dem Herunterladen.

   .. image:: img/llm_olama_llama_download.png

4. Gehen Sie zu **Settings** → aktivieren Sie **Expose Ollama to the network**. Dadurch kann Ihr Raspberry Pi über das lokale Netzwerk darauf zugreifen.  

   .. image:: img/llm_olama_windows_enable.png

.. warning::

   Wenn eine Fehlermeldung wie diese erscheint:

   ``Error: model requires more system memory ...``

   ist das Modell für Ihr Gerät zu groß.  
   Verwenden Sie ein **kleineres Modell** oder wechseln Sie zu einem Computer mit mehr RAM.

2. Ollama testen
----------------------------

Sobald Ollama installiert ist und Ihr Modell bereitsteht, können Sie es mit einer minimalen Chat-Schleife schnell testen.

**IP-Adresse festlegen**

#. Öffnen Sie das Beispielskript:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_ollama.py

#. Passen Sie die Parameter nach Bedarf an:

   * ``llm = Ollama(ip="localhost", model="llama3.2:3b")``: Aktualisieren Sie sowohl ``ip`` als auch ``model`` entsprechend Ihrer eigenen Konfiguration.  

     * ``ip``: Wenn Ollama auf demselben Pi läuft, verwenden Sie ``localhost``. Wenn Ollama auf einem anderen Computer im lokalen Netzwerk läuft, aktivieren Sie in Ollama **Expose to network** und setzen Sie ``ip`` auf die LAN-IP dieses Computers.  
     * ``model``: Muss exakt mit dem Modellnamen übereinstimmen, den Sie in Ollama heruntergeladen bzw. aktiviert haben.  


**Programm ausführen**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 llm_ollama.py

Jetzt können Sie direkt im Terminal mit Fusion HAT+ chatten.

   * Sie können **jedes Modell** verwenden, das auf |link_ollama_hub| verfügbar ist. Kleinere Modelle (z. B. ``moondream:1.8b``, ``phi3:mini``) werden jedoch empfohlen, wenn Sie nur 8–16GB RAM haben.  
   * Stellen Sie sicher, dass das im Code angegebene Modell mit dem Modell übereinstimmt, das Sie bereits in Ollama heruntergeladen haben.  
   * Geben Sie ``exit`` oder ``quit`` ein, um das Programm zu beenden.  
   * Falls keine Verbindung hergestellt werden kann, stellen Sie sicher, dass Ollama läuft und sich beide Geräte im selben lokalen Netzwerk befinden, wenn Sie einen Remote-Host verwenden.

**Code**

.. code-block:: python

   from fusion_hat.llm import Ollama
 
   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   # Change this to your computer IP, if you run it on your pi, then change it to localhost
   llm = Ollama(
      ip="localhost",
      model="llama3.2:3b"
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Response without stream
      # response = llm.prompt(input_text)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


3. Vision Talk mit Ollama
--------------------------

In dieser Demo nimmt die Pi-Kamera **jedes Mal ein neues Bild auf, sobald Sie eine Frage eingeben**.  
Das Programm sendet **Ihren eingegebenen Text zusammen mit dem neuen Foto** über Ollama an ein lokales Vision-Modell  
und gibt anschließend die Antwort des Modells in einfachem Englisch als Stream aus.  
Dies ist eine minimale „See & Tell“-Basis, die Sie später um Farb-, Gesichts- oder QR-Erkennung erweitern können.

**Bevor Sie beginnen**

#. Öffnen Sie die **Ollama**-App (oder starten Sie den Dienst) und stellen Sie sicher, dass ein **visionfähiges Modell** heruntergeladen wurde.

   * Wenn Sie über genügend Speicher verfügen (≥16GB RAM), können Sie ``llava:7b`` ausprobieren.
   * Wenn Sie nur **8GB RAM** haben, sollten Sie ein kleineres Modell wie ``moondream:1.8b`` oder ``granite3.2-vision:2b`` bevorzugen.

   .. image:: img/llm_ollama_image_model.png

**Demo ausführen**

#. Wechseln Sie in den Beispielordner und starten Sie das Skript:

   .. code-block:: bash

      cd ~/ai-lab-kit/llm
      python3 llm_ollama_with_image.py

#. Was beim Ausführen passiert:

   * Das Programm zeigt eine Begrüßungszeile an und wartet auf Ihre Eingabe (``>>>``).
   * **Jedes Mal, wenn Sie etwas eingeben** (z. B. „hello“, „Is there yellow?“, „Any faces?“, „What is on the desk?“), passiert Folgendes:

     * Es wird **ein Foto** mit der Pi-Kamera aufgenommen (gespeichert unter ``/tmp/llm-img.jpg``).  
     * **Ihr Text zusammen mit dem Foto** wird über Ollama an das Vision-Modell gesendet.  
     * Die Antwort des Modells wird **als Stream** im Terminal ausgegeben.

   * Geben Sie ``exit`` oder ``quit`` ein, um das Programm zu beenden.

**Code**

.. code-block:: python

   from fusion_hat.llm import Ollama
   from picamera2 import Picamera2
   import time

   '''
   You need to setup ollama first, see llm_local.py

   You need at leaset 8GB RAM to run llava:7b large multimodal model
   '''

   INSTRUCTIONS = "You are a helpful assistant."
   WELCOME = "Hello, I am a helpful assistant. How can I help you?"

   llm = Ollama(
      ip="localhost",          # e.g., "192.168.100.145" if remote
      model="llava:7b"         # change to "moondream:1.8b" or "granite3.2-vision:2b" for 8GB RAM
   )

   # Set how many messages to keep
   llm.set_max_messages(20)
   # Set instructions
   llm.set_instructions(INSTRUCTIONS)
   # Set welcome message
   llm.set_welcome(WELCOME)

   # Init camera
   camera = Picamera2()
   config = camera.create_still_configuration(
      main={"size": (1280, 720)},
   )
   camera.configure(config)
   camera.start()
   time.sleep(2)

   print(WELCOME)

   while True:
      input_text = input(">>> ")

      # Capture image
      img_path = '/tmp/llm-img.jpg'
      camera.capture_file(img_path)

      # Response without stream
      # response = llm.prompt(input_text, image_path=img_path)
      # print(f"response: {response}")

      # Response with stream
      response = llm.prompt(input_text, stream=True, image_path=img_path)
      for next_word in response:
         if next_word:
               print(next_word, end="", flush=True)
      print("")


Troubleshooting
---------------


* **Ich erhalte eine Fehlermeldung wie: `model requires more system memory ...`.**

  * Das bedeutet, dass das Modell für Ihr Gerät zu groß ist.  
  * Verwenden Sie ein kleineres Modell wie ``moondream:1.8b`` oder ``granite3.2-vision:2b``.  
  * Alternativ können Sie auf einen Computer mit mehr RAM wechseln und Ollama im Netzwerk verfügbar machen.

* **Der Code kann keine Verbindung zu Ollama herstellen (connection refused).** 

  Überprüfen Sie Folgendes:
  
  * Stellen Sie sicher, dass Ollama läuft (``ollama serve`` oder die Desktop-App geöffnet ist).  
  * Wenn Sie einen entfernten Computer verwenden, aktivieren Sie **Expose to network** in den Ollama-Einstellungen.  
  * Prüfen Sie, ob ``ip="..."`` im Code mit der korrekten LAN-IP übereinstimmt.  
  * Stellen Sie sicher, dass sich beide Geräte im selben lokalen Netzwerk befinden.

* **Meine Pi-Kamera nimmt kein Bild auf.**

  * Prüfen Sie, ob ``Picamera2`` installiert ist und mit einem einfachen Testskript funktioniert.  
  * Kontrollieren Sie, ob das Kamerakabel korrekt angeschlossen ist und in ``raspi-config`` aktiviert wurde.  
  * Stellen Sie sicher, dass Ihr Skript Schreibrechte für den Zielpfad besitzt (``/tmp/llm-img.jpg``).

* **Die Ausgabe ist zu langsam.**  

  * Kleinere Modelle antworten schneller, liefern jedoch einfachere Antworten.  
  * Sie können die Kameraauflösung reduzieren (z. B. 640×480 statt 1280×720), um die Bildverarbeitung zu beschleunigen.  
  * Schließen Sie andere Programme auf dem Pi, um CPU- und RAM-Ressourcen freizugeben.