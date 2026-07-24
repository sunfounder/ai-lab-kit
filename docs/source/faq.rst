.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

FAQ
=====================


Di seguito sono riportate alcune delle domande piu’ comuni che gli utenti potrebbero incontrare durante l’utilizzo di
AI Fusion Lab Kit. Se il tuo problema non e’ elencato qui, consulta le
note di risoluzione dei problemi in ogni capitolo o contatta il supporto.

Domande Generali
-----------------

**Dove posso scaricare l’immagine del sistema operativo?**

    Puoi trovare l’immagine del sistema Raspberry Pi consigliata e le istruzioni
    di configurazione nella sezione :ref:`get_start`. La documentazione fornisce
    anche una guida all’installazione passo-passo per i principianti.

**Ho bisogno di una connessione Internet per utilizzare il kit?**

    Gli esempi Python di base e hardware non richiedono accesso a Internet.
    Tuttavia, i LLM basati su cloud e alcune funzionalita’ AI richiedono una
    connessione Internet attiva.

**Quali modelli di Raspberry Pi sono supportati?**

    Il kit supporta ufficialmente Raspberry Pi 4B e Raspberry Pi 5.
    Altri modelli potrebbero funzionare ma non sono garantiti a causa di limitazioni
    di prestazioni o compatibilita’.

**Devo alimentare il FusionHAT separatamente?**

    Si’. *Il FusionHAT richiede una propria alimentazione*. L’ingresso di
    alimentazione del Raspberry Pi non fornisce energia al FusionHAT. Se il
    FusionHAT non e’ alimentato, alcune funzioni — come l’altoparlante o altri
    moduli integrati — potrebbero non funzionare correttamente.

Software / Installazione
-----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    Questo problema e’ solitamente causato da un conflitto tra la libreria ``RPi.GPIO`` installata nel sistema e la libreria GPIO utilizzata da Fusion HAT.
    Per risolverlo, rimuovi manualmente i file del pacchetto ``RPi.GPIO`` di sistema e poi esegui di nuovo il programma.

    1. Rimuovi i file ``RPi.GPIO`` di sistema:

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Riavvia il Raspberry Pi:

       .. code-block:: bash

          sudo reboot

    3. Esegui di nuovo l’esempio (non usare sudo se non necessario):

Dopo aver rimosso i file ``RPi.GPIO`` in conflitto, l’esempio del pulsante basato su interrupt dovrebbe funzionare normalmente.



**OSError: Fusion HAT not connected, check if Fusion Hat is powered on**

Se incontri questo errore durante l’esecuzione di alcuni esempi (ad es., quando chiami i pin PWM), le cause possibili sono:

1. Fusion HAT non e’ collegato correttamente;
2. Metodo di alimentazione errato;
3. Il driver Fusion HAT e’ mancante dopo un aggiornamento del sistema Raspberry Pi.

Segui i passaggi seguenti per verificare e risolvere il problema:

1. Esegui il seguente comando per controllare lo stato del Fusion HAT:

   .. code-block:: bash

      i2cdetect -y 1

   In condizioni normali, dovresti vedere un output simile al seguente (con ``UU`` all’indirizzo ``0x1e``):

   .. code-block:: bash

      pi@ai-fusion:~ $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:                         -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- --
      20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- -- --

2. Se non vedi ``UU`` ma vedi ``17``, il driver Fusion HAT e’ mancante. Reinstalla il driver eseguendo i seguenti comandi:

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. Se non vedi ne’ ``UU`` ne’ ``17``, significa che Fusion HAT non e’ collegato al Raspberry Pi o c’e’ un problema di alimentazione. Assicurati che il tuo Raspberry Pi sia correttamente collegato al Fusion HAT e che il Raspberry Pi sia alimentato dal Fusion HAT (non alimentato in modo indipendente).

4. Se i passaggi precedenti non risolvono il problema, esegui i seguenti comandi e inviaci l’output:

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat
      cat ~/.ai-fusion

**Lo script di installazione ha fallito. Cosa devo fare?**

    Assicurati che il tuo Raspberry Pi OS sia aggiornato e che tu abbia una
    connessione di rete stabile durante l’installazione. Prova a eseguire di
    nuovo lo script di configurazione. Se il problema persiste, riavvia il
    sistema e ricontrolla la versione di Python.

**Gli esempi Python non vengono eseguiti. Quale potrebbe essere la causa?**

    Questo e’ solitamente correlato a librerie Python mancanti o a una
    configurazione dell’ambiente errata. Verifica che le dipendenze siano state
    installate tramite la guida di configurazione in :ref:`get_start`.

**La telecamera non viene rilevata.**

    Assicurati che il cavo a nastro sia saldamente collegato e non inserito
    al contrario. Conferma anche che l’interfaccia della telecamera sia
    abilitata nelle impostazioni di configurazione del Raspberry Pi.

Funzionalita’ AI
-----------

**Le risposte LLM sono lente o non arrivano.**

    Questo spesso indica una scarsa connettivita’ Internet o limiti di
    frequenza API dal fornitore del modello selezionato. Prova a cambiare
    rete o a testare con un modello diverso.

**Il riconoscimento vocale (STT) e’ impreciso.**

    Controlla la connessione del microfono e riduci il rumore di fondo.
    Alcuni modelli potrebbero richiedere pacchetti linguistici aggiuntivi
    o regolazioni della configurazione.

**Mostra ‘Error querying device -1’ nel modulo Vosk STT.**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f’Error querying device {device}’)
        sounddevice.PortAudioError: Error querying device -1

    Esegui ``sudo /opt/setup_fusion_hat_audio.sh`` per riconfigurare l’audio


**Permesso negato durante l’uso di TTS/STT**

    Quando esegui comandi TTS (Text-to-Speech) o STT (Speech-to-Text), incontri un errore di autorizzazione come:

    .. code-block:: bash

        Traceback (most recent call last):
            File "/home/pi/ai-lab-kit/llm/tts_piper.py", line 3, in <module>
                tts = Piper()
                    ^^^^^^^
            File "/usr/local/lib/python3.11/dist-packages/fusion_hat/tts.py", line 125, in _piper_init_with_speaker
                _original_piper_init(self, *args, **kwargs)
            File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/tts/piper.py", line 30, in __init__
                os.makedirs(PIPER_MODEL_DIR, 0o777)
            File "<frozen os>", line 225, in makedirs
        PermissionError: [Errno 13] Permission denied: ‘/opt/piper_models’


    Questo problema si verifica nella versione 0.0.1 del sistema operativo AI Fusion Lab Kit. Il sistema tenta di creare una directory (/opt/piper_models) che richiede privilegi di root, ma l’utente corrente non dispone di autorizzazioni sufficienti. Aggiorna il sistema operativo AI Fusion Lab Kit dalla versione 0.0.1 alla 0.1.0 eseguendo il seguente comando:

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash


Visione Artificiale / MediaPipe
---------------------------

**Gli esempi OpenCV mostrano errori durante l’accesso alla telecamera.**

    Un solo processo puo’ accedere alla telecamera alla volta. Assicurati che
    nessun’altra applicazione per telecamera sia in esecuzione in background.

**Gli esempi MediaPipe funzionano lentamente.**

    La visione artificiale in tempo reale richiede una potenza di elaborazione
    significativa. Considera di ridurre la risoluzione di input o chiudere
    altri processi per liberare risorse di sistema.

**I progetti MediaPipe non funzionano sull’ultimo Raspberry Pi OS.**

    MediaPipe attualmente non supporta le versioni piu’ recenti del sistema
    Raspberry Pi (Trixie) a causa di modifiche alle dipendenze e
    all’architettura. Utilizza la versione precedente (Bookworm) che supporta
    tutti gli esempi basati su MediaPipe.

Problemi Hardware
---------------

**Un componente non risponde.**

    Ricontrolla i collegamenti dei cavi e assicurati del corretto orientamento.
    Fai riferimento alla sezione :ref:`cpn_list` per le descrizioni dei pin e
    gli schemi di esempio.

**Il dispositivo smette improvvisamente di funzionare.**

    Questo potrebbe essere causato da instabilita’ dell’alimentazione.
    Assicurati che la tua alimentazione soddisfi le specifiche raccomandate
    per il modello di Raspberry Pi in uso.

Contatti e Supporto
-------------------

**Come posso ottenere ulteriore aiuto?**

    Puoi consultare la documentazione per passaggi dettagliati di risoluzione
    dei problemi. Se hai domande, contattaci all’indirizzo
    **service@sunfounder.com** — siamo qui per aiutarti.
