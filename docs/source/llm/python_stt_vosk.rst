.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_stt_whisper:

3. STT mit Vosk (Offline)
==============================================

Vosk ist eine leichtgewichtige Speech-to-Text-Engine (STT), die viele Sprachen unterstützt und vollständig **offline** auf dem Raspberry Pi ausgeführt werden kann.  
Sie benötigen nur einmal Internetzugang, um ein Sprachmodell herunterzuladen. Danach funktioniert alles ohne Netzwerkverbindung.  

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

In dieser Lektion werden wir:  

* das Mikrofon auf dem Raspberry Pi prüfen,  
* Vosk mit einem ausgewählten Sprachmodell installieren und testen.  

.. start_mic

.. _test_vosk:

Programm ausführen
--------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

Wenn Sie diesen Code zum ersten Mal mit einer neuen Sprache ausführen, wird Vosk:

* das Sprachmodell **automatisch herunterladen** (standardmäßig die kleine Version),
* die Liste der unterstützten Sprachen **ausgeben**,
* beginnen, über das Mikrofon auf Audioeingaben zu **hören**.

Im Terminal sehen Sie dann etwa Folgendes:

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

Das bedeutet:

   * Die Modelldatei (``vosk-model-small-en-us-0.15``) wurde heruntergeladen.  
   * Die Liste der unterstützten Sprachen wurde ausgegeben.  
   * Das System hört jetzt zu — sprechen Sie etwas in das Mikrofon des Fusion HAT+, und der erkannte Text erscheint im Terminal.

**Tipps:**

* Halten Sie das Mikrofon für eine bessere Erkennungsgenauigkeit in einem Abstand von **15–30 cm**.  
* Wählen Sie ein **Modell, das zu Ihrer Sprache und Ihrem Akzent passt**.  
* Verwenden Sie möglichst eine ruhige Umgebung, um die Erkennung zu verbessern.

Code
---------------

.. code-block:: python

   from fusion_hat.stt import Vosk as STT

   stt = STT(language="en-us")

   while True:
      print("Say something")
      for result in stt.listen(stream=True):
         if result["done"]:
               print(f"final:   {result['final']}")
         else:
               print(f"partial: {result['partial']}", end="\r", flush=True)


**Code-Erklärung:**

* ``stt.listen(stream=True)`` — Startet die **Streaming-Spracherkennung** und liefert während des Sprechens fortlaufend Zwischenergebnisse.  
* ``result["partial"]`` — Zeigt den **in Echtzeit erkannten Text** an (wird kontinuierlich aktualisiert).  
* ``result["final"]`` — Zeigt den **endgültig erkannten Satz** an, sobald Sie aufhören zu sprechen.  
* Die Schleife läuft dauerhaft weiter und ermöglicht so eine **freihändige Echtzeit-Transkription**.

**Tipp:** Dieser Streaming-Modus eignet sich ideal für **Sprachassistenten**, **Sprachbefehle** oder **Live-Transkription**.

Troubleshooting
-----------------

* **No such file or directory (beim Ausführen von `arecord`)**

  Möglicherweise wurde die falsche Karten-/Gerätenummer verwendet.  
  Führen Sie aus:

  .. code-block:: bash

     arecord -l

  und ersetzen Sie ``1,0`` durch die Nummern, die für Ihr USB-Mikrofon angezeigt werden.


* **Vosk erkennt keine Sprache**

  * Stellen Sie sicher, dass der **Sprachcode** zum Modell passt (z. B. ``en-us`` für Englisch, ``zh-cn`` für Chinesisch).  
  * Halten Sie das Mikrofon etwa **15–30 cm** entfernt und vermeiden Sie Hintergrundgeräusche.  
  * Sprechen Sie deutlich und nicht zu schnell.

* **Hohe Latenz / langsame Erkennung**

  * Das automatisch heruntergeladene Modell ist standardmäßig ein **kleines Modell** (schneller, aber weniger genau).  
  * Wenn die Erkennung trotzdem langsam ist, schließen Sie andere Programme, um CPU-Ressourcen freizugeben.

.. end_mic