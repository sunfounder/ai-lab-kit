.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _install_the_libraries:

Install the Libraries
==========================

For C User
--------------

BCM2835
~~~~~~~~~~~~~~~
Dies ist eine C-Bibliothek für den Raspberry Pi (RPi). Sie ermöglicht den Zugriff auf GPIOs und andere IO-Funktionen des Broadcom BCM2835-Chips, der im Raspberry Pi eingesetzt wird. Damit erhältst du Zugriff auf die GPIO-Pins des 26-poligen IDE-Anschlusses auf dem RPi-Board und kannst verschiedene externe Geräte steuern und anbinden.

Die Bibliothek stellt Funktionen zum Lesen digitaler Eingaben und Setzen digitaler Ausgaben bereit, unterstützt SPI und I2C sowie den Zugriff auf Systemtimer. Die Erkennung von Pin-Ereignissen wird über Polling unterstützt (Interrupts werden nicht unterstützt).

Kompatibel mit allen Versionen bis einschließlich RPi 4. Funktioniert mit allen Debian-Versionen bis einschließlich Debian Buster 10.


Öffne ein Terminal und lade die ``bcm2835``-Bibliothek in das ``~``-Verzeichnis herunter.

.. raw:: html

   <run></run>

.. code-block:: 

    cd ~
    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.69.tar.gz

Entpacke das Paket.

.. raw:: html

   <run></run>

.. code-block:: 

    tar zxvf bcm2835-1.69.tar.gz

Installiere die BCM2835-Bibliothek mit den folgenden Befehlen:

.. raw:: html

   <run></run>

.. code-block:: 

    cd bcm2835-1.69
    ./configure
    make
    sudo make check
    sudo make install

* Referenz: `bcm2835 <http://www.airspayce.com/mikem/bcm2835/>`_  


For Python User
----------------------

.. _create_virtual:

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Beim Einsatz des Raspberry Pi oder ähnlicher Geräte wird empfohlen, Pakete mit ``pip`` in einer virtuellen Umgebung zu installieren. Diese sorgt für eine klare Trennung von Abhängigkeiten, erhöht die Systemsicherheit, hält das System sauber und erleichtert Migration sowie Austausch von Projekten. Damit wird das Dependency-Management deutlich vereinfacht – ein unverzichtbares Werkzeug in der Python-Entwicklung.

Die Schritte zum Erstellen einer virtuellen Umgebung:

**1. Create a virtual environment**

Stelle zunächst sicher, dass Python auf deinem System installiert ist. Ab Python 3.3 ist das ``venv``-Modul enthalten, sodass keine separate Installation notwendig ist. Bei Python 2 oder einer Version vor Python 3.3 muss ``virtualenv`` installiert werden.

* Für Python 3:

Python 3.3 und neuere Versionen können das ``venv``-Modul direkt nutzen:

.. raw:: html

    <run></run>

.. code-block:: shell

    python3 -m venv myenv

Dies erstellt eine virtuelle Umgebung mit dem Namen ``myenv`` im aktuellen Verzeichnis.

* Für Python 2:

Wenn du noch Python 2 verwendest, installiere zunächst ``virtualenv``:

.. raw:: html

    <run></run>

.. code-block:: shell

    pip install virtualenv

Erstelle anschließend eine virtuelle Umgebung:

.. raw:: html

    <run></run>

.. code-block:: shell

    virtualenv myenv

Dies erstellt ebenfalls eine virtuelle Umgebung mit dem Namen ``myenv`` im aktuellen Verzeichnis.

**2. Activating the Virtual Environment**

Nach dem Erstellen musst du die virtuelle Umgebung aktivieren:

.. note::

    Jedes Mal, wenn du den Raspberry Pi neu startest oder ein neues Terminal öffnest, musst du den folgenden Befehl erneut ausführen, um die virtuelle Umgebung zu aktivieren.

.. raw:: html

    <run></run>

.. code-block:: shell

    source myenv/bin/activate

Nach der Aktivierung erscheint der Name der Umgebung vor der Eingabeaufforderung – ein Hinweis darauf, dass du dich in der virtuellen Umgebung befindest.


**3. Installing Dependencies**

Mit aktivierter virtueller Umgebung kannst du benötigte Abhängigkeiten mit pip installieren. Beispiel:

.. raw:: html

    <run></run>

.. code-block:: shell

    pip install requests

Damit wird die Requests-Bibliothek in der aktuellen virtuellen Umgebung installiert, nicht im globalen System. Dieser Schritt muss nur einmal durchgeführt werden.


**4. Exiting the Virtual Environment**

Wenn du deine Arbeit abgeschlossen hast und die virtuelle Umgebung verlassen möchtest, führe aus:

.. raw:: html

    <run></run>

.. code-block:: shell

    deactivate

Damit kehrst du in die globale Python-Umgebung des Systems zurück.

**5. Deleting the Virtual Environment**

Falls du eine virtuelle Umgebung nicht mehr benötigst, kannst du einfach das entsprechende Verzeichnis löschen:

.. raw:: html

    <run></run>

.. code-block:: shell

    rm -rf myenv


Luma.LED_Matrix
~~~~~~~~~~~~~~~~~~~~~~~

Dies ist eine Python-3-Bibliothek zur Ansteuerung von LED-Matrix-Displays mit dem MAX7219-Treiber (über SPI), WS2812 (NeoPixels, inkl. Pimoroni Unicorn pHat/Hat und Unicorn Hat HD) sowie APA102 (DotStar) auf dem Raspberry Pi und anderen Linux-basierten Single-Board-Computern.

Installiere zunächst die Abhängigkeiten mit:

.. raw:: html

   <run></run>

.. code-block:: 

    sudo usermod -a -G spi,gpio pi
    sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5

.. note:: warning

    Die standardmäßig über apt verfügbaren Versionen von pip und setuptools unter Raspbian sind veraltet und können dazu führen, dass Komponenten nicht korrekt installiert werden. Stelle daher sicher, dass du sie zunächst aktualisierst:

    .. raw:: html

       <run></run>

    .. code-block:: 

        sudo -H pip install --upgrade --ignore-installed pip setuptools

Installiere anschließend die aktuelle Version der luma.led_matrix-Bibliothek direkt von PyPI:

.. raw:: html

   <run></run>

.. code-block:: 

    sudo python3 -m pip install --upgrade luma.led_matrix


* Referenz: `Luma.LED_Matrix <https://luma-led-matrix.readthedocs.io/en/latest/install.html>`_

Spidev and MFRC522
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Bibliothek ``spidev`` erleichtert die Arbeit mit SPI und ist ein zentrales Element dieses Tutorials, da sie benötigt wird, um den Raspberry Pi mit dem RFID RC522 zu verbinden.

Installiere ``spidev`` mit folgendem Befehl über ``pip``:

.. raw:: html

   <run></run>

.. code-block:: 

    sudo pip3 install spidev


Fahre anschließend mit der Installation der MFRC522-Bibliothek fort:

.. raw:: html

   <run></run>

.. code-block:: 

    sudo pip3 install mfrc522

Die MFRC522-Bibliothek besteht aus zwei Dateien: ``MFRC522.py`` und ``SimpleMFRC522.py``.

Dabei implementiert ``MFRC522.py`` das Interface zum RFID RC522 und übernimmt die komplette Kommunikation über das SPI-Interface des Pi.

``SimpleMFRC522.py`` baut auf ``MFRC522.py`` auf und vereinfacht die Nutzung erheblich, indem es dir nur wenige Funktionen bereitstellt, anstatt dich mit allen Details befassen zu müssen.
