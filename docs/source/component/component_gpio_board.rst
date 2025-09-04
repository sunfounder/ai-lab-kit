.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiast Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Tausche Tipps und Tutorials aus, um deine Fähigkeiten zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_gpio_extension_board:

GPIO Extension Board
=====================

Bevor du mit den Befehlen arbeitest, solltest du dich zunächst mit den Pins des Raspberry Pi vertraut machen – dies ist entscheidend für das weitere Verständnis.

Mit einem GPIO Extension Board lassen sich die Pins des Raspberry Pi einfach auf ein Breadboard herausführen. So wird verhindert, dass durch häufiges Ein- und Ausstecken Schäden an den GPIO-Pins entstehen. Hier siehst du unser 40-poliges GPIO Extension Board mit passendem Kabel, geeignet für den Raspberry Pi Model B+, 2 Model B sowie 3 und 4 Model B.

.. image:: img/image32.png
    :align: center

**Pin-Nummern**

Die Pins des Raspberry Pi können auf drei verschiedene Arten benannt werden: WiringPi, BCM und Board.

Beim 40-poligen GPIO Extension Board wird überwiegend die BCM-Namenskonvention verwendet. Einige spezielle Pins, wie die I2C- und SPI-Schnittstellen, behalten jedoch ihre eigenen standardisierten Bezeichnungen.

Die folgende Tabelle zeigt die unterschiedlichen Bezeichnungsarten für WiringPi, Board und den jeweiligen intrinsischen Namen eines Pins auf dem GPIO Extension Board. Zum Beispiel: Der Pin GPIO17 entspricht in der Board-Nummerierung der 11, in der WiringPi-Nummerierung der 0 und trägt intrinsisch den Namen GPIO0.

.. note::

    1) In C wird die WiringPi-Namenskonvention verwendet.
    
    2) In Python werden die Methoden **Board** und **BCM** genutzt, die über die Funktion ``GPIO.setmode()`` festgelegt werden.
    
    3) In Scratch 3 und Processing wird die **BCM-Namenskonvention** angewandt.

.. image:: img/gpio_board.png