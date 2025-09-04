.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiast Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Tausche Tipps und Tutorials aus, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_humiture_sensor:

Humiture-Sensormodul
=============================

.. image:: img/dht11_pic.png
    :width: 400
    :align: center

Der digitale Temperatur- und Luftfeuchtigkeitssensor DHT11 ist ein Kombisensor, der ein kalibriertes digitales Ausgangssignal für Temperatur und Luftfeuchtigkeit liefert.  
Durch den Einsatz spezieller digitaler Erfassungsmodule sowie moderner Temperatur- und Feuchtigkeitssensortechnologien bietet das Produkt eine hohe Zuverlässigkeit und ausgezeichnete Langzeitstabilität.


Der Sensor verfügt lediglich über drei nutzbare Pins: VCC, GND und DATA.  
Der Kommunikationsprozess beginnt damit, dass die DATA-Leitung ein Startsignal an den DHT11 sendet. Der Sensor empfängt dieses Signal und gibt eine Antwort zurück. Anschließend empfängt der Host das Antwortsignal und liest daraufhin insgesamt **40 Bit** an Klima-Daten aus (8 Bit Luftfeuchtigkeit – Ganzzahl, 8 Bit Luftfeuchtigkeit – Dezimal, 8 Bit Temperatur – Ganzzahl, 8 Bit Temperatur – Dezimal, 8 Bit Prüfsumme).

.. image:: img/Dht11.png


* `DHT11 Datasheet <https://components101.com/sites/default/files/component_datasheet/DHT11-Temperature-Sensor.pdf>`_

