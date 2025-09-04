.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_thermistor:

Thermistor
===============

.. image:: img/thermistor.png
    :width: 150
    :align: center

Ein Thermistor ist ein spezieller Widerstand, dessen Widerstandswert stark temperaturabhängig ist – wesentlich stärker als bei Standardwiderständen. Der Begriff setzt sich aus *thermal* und *resistor* zusammen. Thermistoren finden breite Anwendung als Einschaltstrombegrenzer, Temperatursensoren (meist NTC-Typen), selbstzurücksetzende Überstromschutzvorrichtungen sowie selbstregulierende Heizelemente (typischerweise PTC-Typen).

* `Thermistor - Wikipedia <https://en.wikipedia.org/wiki/Thermistor>`_

Hier ist das Schaltzeichen eines Thermistors dargestellt.

.. image:: img/thermistor_symbol.png
    :width: 300
    :align: center

Thermistoren lassen sich in zwei entgegengesetzte Grundtypen unterteilen:

* Bei NTC-Thermistoren (Negative Temperature Coefficient) sinkt der Widerstand mit steigender Temperatur. Ursache ist meist die Zunahme der Leitungselektronen, die durch thermische Anregung aus dem Valenzband freigesetzt werden. NTCs werden häufig als Temperatursensoren oder in Serie mit Schaltungen als Einschaltstrombegrenzer eingesetzt.
* Bei PTC-Thermistoren (Positive Temperature Coefficient) steigt der Widerstand mit zunehmender Temperatur, in der Regel aufgrund verstärkter thermischer Gitteranregungen, insbesondere durch Verunreinigungen oder Gitterfehler. PTCs werden üblicherweise in Serie in Schaltungen eingesetzt, um als rückstellbare Sicherungen gegen Überstrom zu schützen.

In diesem Kit verwenden wir einen NTC-Thermistor. Jeder Thermistor besitzt einen Nennwiderstand; hier beträgt dieser 10 kΩ, gemessen bei 25 °C.

Die Beziehung zwischen Widerstand und Temperatur lautet:

    RT = RN * expB(1/TK – 1/TN)   

* **RT** ist der Widerstand des NTC-Thermistors bei der Temperatur TK.  
* **RN** ist der Widerstand des NTC-Thermistors bei der Referenztemperatur TN. Hier beträgt RN 10 kΩ.  
* **TK** ist die Temperatur in Kelvin (K). Dabei gilt TK = 273,15 + °C.  
* **TN** ist die Referenztemperatur in Kelvin; hier: 273,15 + 25.  
* **B (Beta)** ist die Materialkonstante des NTC-Thermistors, auch Wärmesensitivitätsindex genannt, mit einem typischen Wert von 3950.  
* **exp** steht für die Exponentialfunktion, deren Basis die eulersche Zahl *e* ist (ca. 2,7).  

Durch Umstellen der Formel ergibt sich:  
TK = 1 / (ln(RT/RN)/B + 1/TN).  
Zieht man hiervon 273,15 ab, erhält man die Temperatur in °C.

Diese Beziehung ist eine empirische Näherung und liefert nur innerhalb des spezifizierten Temperatur- und Widerstandsbereichs genaue Ergebnisse.
