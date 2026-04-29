.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

FAQ
=====================


Nachfolgend finden Sie einige der häufigsten Fragen, die bei der Verwendung des
AI Fusion Lab Kits auftreten können. Wenn Ihr Problem hier nicht aufgeführt ist,
lesen Sie bitte die Hinweise zur Fehlerbehebung in den einzelnen Kapiteln oder
kontaktieren Sie den Support.

Allgemeine Fragen
-----------------

**Wo kann ich das System-Image herunterladen?**

    Das empfohlene Raspberry Pi System-Image sowie die Einrichtungsanleitung
    finden Sie im Abschnitt :ref:`get_start`. Die Dokumentation enthält außerdem
    eine Schritt-für-Schritt-Anleitung zur Installation für Einsteiger.

**Benötige ich eine Internetverbindung, um das Kit zu verwenden?**

    Grundlegende Python- und Hardware-Beispiele benötigen keine Internetverbindung.
    Cloudbasierte LLMs und einige KI-Funktionen erfordern jedoch eine aktive
    Internetverbindung.

**Welche Raspberry-Pi-Modelle werden unterstützt?**

    Das Kit unterstützt offiziell den Raspberry Pi 4B und den Raspberry Pi 5.
    Andere Modelle können möglicherweise funktionieren, sind jedoch aufgrund von
    Leistungs- oder Kompatibilitätseinschränkungen nicht garantiert.

**Muss ich den FusionHAT separat mit Strom versorgen?**

    Ja. *Der FusionHAT benötigt eine eigene Stromversorgung*. Der
    Stromanschluss des Raspberry Pi versorgt den FusionHAT nicht mit Strom.
    Wenn der FusionHAT nicht mit Strom versorgt wird, funktionieren einige
    Funktionen — wie z. B. der Lautsprecher oder andere integrierte Module —
    möglicherweise nicht korrekt.

Software / Installation
-----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    Dieses Problem wird normalerweise durch einen Konflikt zwischen der
    systeminstallierten ``RPi.GPIO``-Bibliothek und der vom Fusion HAT
    verwendeten GPIO-Bibliothek verursacht.  
    Um das Problem zu lösen, entfernen Sie bitte manuell die
    ``RPi.GPIO``-Systempaketdateien und führen das Programm anschließend erneut aus.

    1. Entfernen Sie die Systemdateien von ``RPi.GPIO``:

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Starten Sie den Raspberry Pi neu:

       .. code-block:: bash

          sudo reboot

    3. Führen Sie das Beispiel erneut aus (verwenden Sie ``sudo`` nur, wenn es erforderlich ist):

Nach dem Entfernen der konflikterzeugenden ``RPi.GPIO``-Dateien sollte das
tasterbasierte Interrupt-Beispiel wieder normal funktionieren.


**OSError: Fusion HAT nicht verbunden. Überprüfen Sie, ob das Fusion Hat mit Strom versorgt wird.**

Wenn dieser Fehler beim Ausführen einiger Beispiele auftritt (z. B. beim Aufruf von PWM-Pins), können folgende Ursachen vorliegen:

1. Das Fusion HAT ist nicht richtig verbunden;
2. Falsche Stromversorgungsmethode;
3. Der Treiber des Fusion HAT fehlt nach einem Update des Raspberry Pi Systems.

Führen Sie die folgenden Schritte aus, um das Problem zu überprüfen und zu beheben:

1. Führen Sie den folgenden Befehl aus, um den Status des Fusion HAT zu überprüfen:

   .. code-block:: bash

      i2cdetect -y 1

   Unter normalen Bedingungen sollte eine Ausgabe ähnlich der folgenden erscheinen (mit ``UU`` an Adresse ``0x1e``):

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

2. Wenn Sie nicht ``UU``, sondern ``17`` sehen, fehlt der Fusion HAT Treiber. Bitte installieren Sie den Treiber neu, indem Sie die folgenden Befehle ausführen:

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. Wenn Sie weder ``UU`` noch ``17`` sehen, ist das Fusion HAT nicht mit dem Raspberry Pi verbunden oder es liegt ein Stromversorgungsproblem vor. Bitte stellen Sie sicher, dass Ihr Raspberry Pi richtig mit dem Fusion HAT verbunden ist und dass der Raspberry Pi über das Fusion HAT mit Strom versorgt wird (nicht unabhängig mit Strom versorgt wird).

4. Wenn die oben genannten Schritte das Problem nicht beheben, führen Sie bitte die folgenden Befehle aus und senden Sie uns die Ausgabe:

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat
      cat ~/.ai-fusion


**Das Installationsskript ist fehlgeschlagen. Was soll ich tun?**

    Stellen Sie sicher, dass Ihr Raspberry Pi OS auf dem neuesten Stand ist
    und während der Installation eine stabile Netzwerkverbindung besteht.
    Versuchen Sie, das Setup-Skript erneut auszuführen. Wenn das Problem weiterhin
    besteht, starten Sie das System neu und überprüfen Sie Ihre Python-Version.

**Python-Beispiele lassen sich nicht ausführen. Woran könnte das liegen?**

    Dies hängt normalerweise mit fehlenden Python-Bibliotheken oder einer
    fehlerhaften Umgebungseinrichtung zusammen. Vergewissern Sie sich,
    dass die Abhängigkeiten gemäß der Anleitung im Abschnitt
    :ref:`get_start` installiert wurden.

**Die Kamera wird nicht erkannt.**

    Stellen Sie sicher, dass das Flachbandkabel korrekt angeschlossen ist und
    nicht verkehrt herum eingesteckt wurde. Überprüfen Sie außerdem, ob die
    Kamera-Schnittstelle in den Raspberry-Pi-Einstellungen aktiviert ist.

KI-Funktionen
-------------

**LLM-Antworten sind langsam oder werden nicht zurückgegeben.**

    Dies deutet häufig auf eine schlechte Internetverbindung oder
    API-Limitierungen des gewählten Modellanbieters hin. Versuchen Sie,
    das Netzwerk zu wechseln oder ein anderes Modell zu testen.

**Speech-to-Text (STT) ist ungenau.**

    Überprüfen Sie Ihre Mikrofonverbindung und reduzieren Sie Hintergrundgeräusche.
    Einige Modelle benötigen möglicherweise zusätzliche Sprachpakete oder
    Konfigurationsanpassungen.

**In der Vosk-STT-Komponente erscheint „Error querying device -1“.**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    Bitte führen Sie ``sudo /opt/setup_fusion_hat_audio.sh`` aus, um das Audio
    erneut einzurichten.

**Zugriffsverweigerung bei Verwendung von TTS/STT**

    Wenn Sie TTS- (Text-to-Speech) oder STT-Befehle (Speech-to-Text) ausführen, erhalten Sie einen Berechtigungsfehler wie:

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
        PermissionError: [Errno 13] Permission denied: '/opt/piper_models'

    Dieses Problem tritt in der AI Fusion Lab Kit OS Version 0.0.1 auf. Das System versucht, ein Verzeichnis (/opt/piper_models) zu erstellen, das Root-Rechte erfordert, aber der aktuelle Benutzer hat nicht ausreichende Berechtigungen. Aktualisieren Sie das AI Fusion Lab Kit OS von Version 0.0.1 auf 0.1.0, indem Sie den folgenden Befehl ausführen:

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash

Computer Vision / MediaPipe
---------------------------

**OpenCV-Beispiele zeigen Fehler beim Zugriff auf die Kamera.**

    Nur ein Prozess kann gleichzeitig auf die Kamera zugreifen. Stellen Sie sicher,
    dass keine anderen Kamera-Anwendungen im Hintergrund laufen.

**MediaPipe-Beispiele laufen langsam.**

    Echtzeit-Computer-Vision erfordert erhebliche Rechenleistung.
    Reduzieren Sie gegebenenfalls die Eingabeauflösung oder schließen Sie
    andere Prozesse, um Systemressourcen freizugeben.

**MediaPipe-Projekte funktionieren nicht auf der neuesten Raspberry-Pi-OS-Version.**

    MediaPipe unterstützt derzeit die neueste Raspberry-Pi-OS-Version
    (Trixie) aufgrund von Abhängigkeits- und Architekturänderungen nicht.
    Bitte verwenden Sie die Legacy-Version (Bookworm), die alle
    MediaPipe-basierten Beispiele unterstützt.

Hardware-Probleme
-----------------

**Eine Komponente reagiert nicht.**

    Überprüfen Sie Ihre Verdrahtung und stellen Sie sicher, dass die
    Komponenten korrekt ausgerichtet sind. Siehe Abschnitt :ref:`cpn_list`
    für Pinbeschreibungen und Beispielschaltpläne.

**Das Gerät funktioniert plötzlich nicht mehr.**

    Dies kann durch eine instabile Stromversorgung verursacht werden.
    Stellen Sie sicher, dass Ihr Netzteil den empfohlenen Spezifikationen
    für das verwendete Raspberry-Pi-Modell entspricht.

Kontakt und Support
-------------------

**Wie kann ich weitere Hilfe erhalten?**

    Sie können die Dokumentation für detaillierte Hinweise zur
    Fehlerbehebung konsultieren. Wenn Sie Fragen haben, kontaktieren Sie
    uns gerne unter **service@sunfounder.com** — wir helfen Ihnen gerne weiter.