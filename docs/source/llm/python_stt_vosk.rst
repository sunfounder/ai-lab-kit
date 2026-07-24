.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _py_stt_whisper:
.. _test_vosk:

3. STT con Vosk (Offline)
==============================================

Vosk e' un motore leggero di riconoscimento vocale (STT) che supporta molte lingue e funziona completamente **offline** su Raspberry Pi.
Hai bisogno di accesso a Internet solo una volta per scaricare un modello linguistico. Dopo, tutto funziona senza connessione di rete.

.. raw:: html

      <video width="500" loop muted controls>
          <source src="../_static/video/Stt_With_Vosk.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

In questa lezione:

* Controlleremo il microfono su Raspberry Pi.
* Installeremo e testeremo Vosk con un modello linguistico scelto.


.. start_mic


Esegui il programma
--------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/llm
   sudo python3 stt_vosk_stream.py

La prima volta che esegui questo codice con una nuova lingua, Vosk:

* **Scarichera' automaticamente il modello linguistico** (per impostazione predefinita, la versione piccola).
* **Stampera' l'elenco delle lingue supportate**.
* Iniziera' ad **ascoltare** l'input audio attraverso il microfono.

Vedrai qualcosa di simile nel terminale:

.. code-block:: text

         vosk-model-small-en-us-0.15.zip: 100%|███████████████████| 39.3M/39.3M [00:05<00:00, 7.85MB/s]
         ['ar', 'ar-tn', 'ca', 'cn', 'cs', 'de', 'en-gb', 'en-in', 'en-us', 'eo', 'es', 'fa', 'fr', 'gu', 'hi', 'it', 'ja', 'ko', 'kz', 'nl', 'pl', 'pt', 'ru', 'sv', 'te', 'tg', 'tr', 'ua', 'uz', 'vn']
         Say something

Questo significa:

   * Il file del modello (``vosk-model-small-en-us-0.15``) e' stato scaricato.
   * L'elenco delle lingue supportate e' stato stampato.
   * Il sistema ora sta ascoltando -- dì qualcosa nel microfono del Fusion HAT+ e il testo riconosciuto apparira' nel terminale.

**Suggerimenti:**

* Tieni il microfono a circa **15-30 cm** di distanza per una migliore precisione.
* Scegli un **modello che corrisponda alla tua lingua e accento**.
* Usa un ambiente silenzioso per migliorare il riconoscimento.

Codice
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


**Spiegazione del codice:**

* ``stt.listen(stream=True)`` -- Avvia il riconoscimento vocale in streaming e produce risultati intermedi mentre parli.
* ``result["partial"]`` -- Mostra il **testo riconosciuto in tempo reale** (aggiornato continuamente).
* ``result["final"]`` -- Mostra la **frase riconosciuta finale** quando smetti di parlare.
* Il ciclo viene eseguito continuamente, permettendo la **trascrizione in tempo reale a mani libere**.

Suggerimento: Questa modalita' di streaming e' perfetta per **assistenti vocali**, **controllo comandi** o **trascrizione live**.

Risoluzione dei Problemi
-------------------------

* **Nessun file o directory (durante l'esecuzione di `arecord`)**

  Potresti aver usato il numero di scheda/dispositivo sbagliato.
  Esegui:

  .. code-block:: bash

     arecord -l

  e sostituisci ``1,0`` con i numeri mostrati per il tuo microfono USB.


* **Vosk non riconosce il parlato**

  * Assicurati che il **codice lingua** corrisponda al tuo modello (ad esempio ``en-us`` per inglese, ``zh-cn`` per cinese).
  * Tieni il microfono a 15-30 cm di distanza ed evita il rumore di fondo.
  * Parla chiaramente e lentamente.

* **Latenza elevata / riconoscimento lento**

  * Il download automatico predefinito e' un **modello piccolo** (piu' veloce, ma meno accurato).
  * Se e' ancora lento, chiudi altri programmi per liberare CPU.

.. end_mic
