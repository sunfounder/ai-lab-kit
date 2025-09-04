.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiast Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Tausche Tipps und Tutorials aus, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_i2c_lcd:

I2C LCD1602
==============

.. image:: img/i2c_lcd1602.png
    :width: 800

* **GND**: Masse
* **VCC**: Spannungsversorgung, 5V
* **SDA**: Serielle Datenleitung. Mit Pull-up-Widerstand an VCC anschließen.
* **SCL**: Serieller Takt. Mit Pull-up-Widerstand an VCC anschließen.

Wie allgemein bekannt ist, bereichern LCDs und andere Displays zwar die Mensch-Maschine-Interaktion erheblich, sie haben jedoch einen gemeinsamen Nachteil: Werden sie mit einem Controller verbunden, blockieren sie zahlreiche IO-Pins. Da viele Controller nur über begrenzte Schnittstellen verfügen, schränkt dies deren weitere Funktionen erheblich ein.  

Um dieses Problem zu lösen, wurde das **LCD1602** mit einem **I2C-Modul** entwickelt. Dieses Modul basiert auf dem integrierten **PCF8574 I2C-Chip**, der serielle I2C-Daten in parallele Daten für das LCD umwandelt.        

* `PCF8574 Datasheet <https://www.ti.com/lit/ds/symlink/pcf8574.pdf?ts=1627006546204&ref_url=https%253A%252F%252Fwww.google.com%252F>`_

**I2C-Adresse**

Die Standardadresse ist in der Regel 0x27, in einigen Fällen kann sie jedoch 0x3F betragen.  

Am Beispiel der Standardadresse 0x27 lässt sich die Geräteadresse durch Kurzschließen der A0/A1/A2-Pads ändern. Im Auslieferungszustand sind A0/A1/A2 = 1, wird ein Pad überbrückt, wird der jeweilige Wert zu 0.

.. image:: img/i2c_address.jpg
    :width: 600

**Hintergrundbeleuchtung/Kontrast**

Die Hintergrundbeleuchtung kann über eine Jumperkappe aktiviert werden; zum Deaktivieren einfach die Jumperkappe entfernen.  
Das blaue Potentiometer auf der Rückseite dient zur Einstellung des Kontrasts (dem Helligkeitsverhältnis zwischen reinem Weiß und tiefem Schwarz).

.. image:: img/back_lcd1602.jpg

* **Shorting Cap**: Aktiviert die Hintergrundbeleuchtung; ohne Kappe ist sie deaktiviert.  
* **Potentiometer**: Regelt den Kontrast (Lesbarkeit des Textes). Im Uhrzeigersinn erhöhen, gegen den Uhrzeigersinn verringern.


