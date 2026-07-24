.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Se si utilizza l'immagine preinstallata "Raspberry Pi OS with AI Fusion Lab Kit", questa sezione puo essere saltata. Tale immagine include gia tutte le installazioni software, le configurazioni ambientali e i deployment del codice di esempio descritti in questo capitolo.


.. _mediapipe_install:

0. Setup di MediaPipe
====================================================================

Informazioni sulla Versione del Sistema Operativo
-------------------------------------------------

.. warning::

   **Sistema Operativo Raccomandato**: Raspberry Pi OS Bookworm (Debian 12, 64-bit)

   Raspberry Pi OS Trixie (Debian 13) non e raccomandato perche:

   * MediaPipe non supporta ancora Python 3.13.
   * Picamera2 funziona solo con il Python di sistema.

Questo tutorial verra aggiornato quando Trixie sara supportato.

Se desideri richiedere il supporto ufficiale di MediaPipe per Python 3.13, puoi inviare un feedback qui:

* GitHub Issue: https://github.com/google-ai-edge/mediapipe/issues/5708
* Support Page: https://ai.google.dev/edge/mediapipe/support



Prima di Iniziare
----------------

.. important::


   Prima di iniziare, assicurati di:

   * Aver assemblato il pan-tilt
   * Poter accedere al desktop del Raspberry Pi
   * Aver installato il pacchetto del codice
   * Aver installato e configurato Fusion HAT+
   * Aver installato OpenCV

   Per istruzioni dettagliate, consulta :ref:`opencv_install`.

Queste preparazioni garantiscono che MediaPipe possa funzionare con tutte le funzionalita grafiche e della fotocamera sul tuo Raspberry Pi.


Passaggi di Installazione
----------------------------------

#. Installare MediaPipe

   Installa MediaPipe usando pip. Su Raspberry Pi OS Bookworm (Debian 12, 64-bit),
   pip scarichera automaticamente la wheel corretta.

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. Verificare l'installazione

   Esegui il seguente comando per confermare che MediaPipe sia installato correttamente.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Output previsto:

   .. code-block:: text

      MediaPipe version: 0.10.18


Problemi Comuni e Soluzioni
-------------------------

#. L'installazione di MediaPipe fallisce

   Questo accade solitamente quando si utilizza una versione del sistema operativo non supportata.

   Soluzione:

   * MediaPipe attualmente funziona solo su Raspberry Pi OS Bookworm (Debian 12, 64-bit).
   * Raspberry Pi OS Trixie (Debian 13, Python 3.13) non e supportato.

#. La fotocamera non puo essere aperta in MediaPipe o OpenCV

   Questo accade solitamente quando l'interfaccia della fotocamera del Raspberry Pi non e abilitata.

   Soluzione:

   * Abilita la fotocamera in ``raspi-config``:
     Interface Options → Camera → Enable

#. Errori di importazione di OpenCV

   Alcune versioni di OpenCV installate con pip potrebbero essere incompatibili con le librerie di Raspberry Pi OS.

   Soluzione:

   .. code-block:: bash

      sudo apt install python3-opencv

#. MediaPipe non puo essere importato dopo l'installazione

   Questo puo accadere se pip, setuptools o wheel sono obsoleti.

   Soluzione:

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


Il tuo MediaPipe e ora pronto.
Puoi procedere alla sezione successiva per eseguire il rilevamento facciale in tempo reale utilizzando la fotocamera del Raspberry Pi.
