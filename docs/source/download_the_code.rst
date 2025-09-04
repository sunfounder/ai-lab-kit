.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community auf Facebook! Tauche gemeinsam mit anderen Enthusiasten tiefer in Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse After-Sales-Fragen und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Tausche Tipps und Anleitungen aus, um deine Fähigkeiten auszubauen.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und Sneak Peeks.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu bauen? Klicke auf [|link_sf_facebook|] und tritt noch heute bei!

Download the Code & Library
=====================================

.. _download_the_code:

Download the code
-----------------------------

.. note:: Bevor Sie den Code herunterladen, beachten Sie bitte, dass der Beispielcode **ONLY** unter Raspberry Pi OS getestet wurde. Wir stellen zwei Methoden für den Download bereit:

**Method 1: Use git clone (Recommended)**

Melden Sie sich auf dem Raspberry Pi an und wechseln Sie anschließend in das Verzeichnis ``~``.

.. raw:: html

   <run></run>

.. code-block::

   cd ~/


.. note::

   cd wechselt vom aktuellen Pfad in das gewünschte Verzeichnis. Hier bedeutet das, zum Pfad ``~/`` zu wechseln.

Klonen Sie das Repository von GitHub.

.. raw:: html

   <run></run>

.. code-block::

   git clone https://github.com/sunfounder/ai-explorer-lab-kit.git

**Method 2: Download the code**

Laden Sie den Quellcode von GitHub herunter: https://github.com/sunfounder/ai-explorer-lab-kit

.. image:: img/download_code.png



.. _download_the_lib:

Download & Install the Library
----------------------------------

Für dieses Kit werden alle GPIO-Funktionen über den Fusion HAT bereitgestellt. Verwenden Sie daher die zugehörige ``fusion-hat``-Bibliothek, um darauf zuzugreifen und sie zu steuern.

Führen Sie im Terminal die folgenden Befehle aus, um das Modul ``fusion-hat`` zu installieren.

   .. raw:: html

      <run></run>

   .. code-block::

      cd ~/
      git clone https://github.com/sunfounder/fusion-hat.git
      cd fusion-hat
      sudo python3 setup.py install

.. note:: Ausführliche Informationen zu fusion-hat finden Sie unter |link_fusion_hat|.

.. _install_i2s:

Install ``i2samp.sh`` for the Speaker
------------------------------------------------------

``i2samp.sh`` ist ein ausgefeiltes Bash-Skript zur Einrichtung und Konfiguration eines I2S-(Inter-IC Sound)-Verstärkers auf dem Raspberry Pi und ähnlichen Geräten. Es steht unter der MIT-Lizenz, prüft vor der Installation bzw. Konfiguration die Kompatibilität und unterstützt eine Vielzahl von Hardware- und Betriebssystemkombinationen.

Damit Ihr Lautsprecher korrekt funktioniert, müssen Sie dieses Skript unbedingt installieren.

Gehen Sie wie folgt vor:

.. code-block::

    cd ~/fusion-hat
    sudo bash i2samp.sh

Geben Sie ``y`` ein und drücken Sie ``Enter``, um das Skript fortzusetzen.

    .. image:: img/install_i2s1.png

Geben Sie ``y`` ein und drücken Sie ``Enter``, um ``/dev/zero`` im Hintergrund auszuführen.

    .. image:: img/install_i2s2.png

Geben Sie ``y`` ein und drücken Sie ``Enter``, um den Raspberry Pi neu zu starten.

    .. image:: img/install_i2s2.png

.. warning::

    Falls nach dem Neustart kein Ton zu hören ist, müssen Sie das Skript ``i2samp.sh`` möglicherweise mehrfach ausführen.