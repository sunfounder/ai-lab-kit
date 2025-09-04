.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_pir:

PIR-Bewegungssensormodul
============================

.. image:: img/pir_pic.png
    :width: 300
    :align: center

Der PIR-Sensor erkennt Infrarot-Wärmestrahlung, die von Organismen ausgesendet wird, und kann so deren Anwesenheit feststellen.  

Der PIR-Sensor ist in zwei Segmente unterteilt, die an einen Differenzverstärker angeschlossen sind. Befindet sich ein stationäres Objekt vor dem Sensor, empfangen beide Segmente die gleiche Menge Strahlung, und der Ausgang bleibt null. Bewegt sich jedoch ein Objekt, empfängt ein Segment mehr Strahlung als das andere, was den Ausgangswert zwischen hoch und niedrig schwanken lässt. Diese Veränderung der Ausgangsspannung zeigt die Bewegungserkennung an.  

.. image:: img/PIR_working_principle.jpg
    :width: 800

Nach dem Anschließen des Sensormoduls erfolgt eine Initialisierung von etwa einer Minute. Während dieser Zeit gibt das Modul in Abständen 0–3 Signale aus. Danach wechselt es in den Standby-Modus. Achte darauf, dass keine Lichtquellen oder andere Störquellen auf die Oberfläche des Moduls einwirken, um Fehlfunktionen durch Störsignale zu vermeiden. Auch zu viel Luftzug sollte vermieden werden, da dieser den Sensor ebenfalls beeinflussen kann.  

.. image:: img/pir_back.png
    :width: 600
    :align: center

**Entfernungseinstellung**

Durch Drehen des Potentiometers für die Entfernungseinstellung im Uhrzeigersinn wird die Reichweite der Erkennung vergrößert, bis maximal etwa 0–7 Meter. Drehst du es gegen den Uhrzeigersinn, verringert sich die Reichweite auf ein Minimum von etwa 0–3 Meter.  

**Verzögerungseinstellung**

Drehe das Potentiometer für die Verzögerung im Uhrzeigersinn, um die Erkennungsverzögerung zu erhöhen. Der Maximalwert kann bis zu 300 Sekunden erreichen. Drehst du es gegen den Uhrzeigersinn, kann die Verzögerung auf ein Minimum von 5 Sekunden reduziert werden.  

**Zwei Auslösemodi**

Die Auswahl erfolgt über eine Steckbrücke (Jumper).  

* **H**: Wiederholbarer Auslösemodus. Nach Erkennung einer Person gibt das Modul ein High-Signal aus. Betritt während der Verzögerungszeit jemand erneut den Erfassungsbereich, bleibt der Ausgang weiterhin auf High.  

* **L**: Nicht wiederholbarer Auslösemodus. Erkennt der Sensor eine Person, gibt er ein High-Signal aus. Nach Ablauf der Verzögerung wechselt der Ausgang automatisch von High auf Low.  

