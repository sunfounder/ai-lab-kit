.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_diode:

Diode
=================

Eine Diode ist ein elektronisches Bauelement mit zwei Anschlüssen, das den Stromfluss nur in einer Richtung zulässt – diese Eigenschaft wird als Gleichrichterfunktion bezeichnet. Man kann sich eine Diode daher wie ein elektronisches Rückschlagventil vorstellen.  

Durch ihre Einweg-Leitfähigkeit wird die Diode in nahezu allen komplexeren elektronischen Schaltungen eingesetzt. Sie zählt zu den ersten Halbleiterbauelementen und verfügt über ein sehr breites Anwendungsspektrum.  

Je nach Einsatzzweck unterscheidet man verschiedene Typen: Detektordioden, Gleichrichterdioden, Begrenzerdioden, Zenerdioden usw.  
In diesem Kit sind Gleichrichterdioden und Zenerdioden enthalten.  

**Rectifier Diode**

.. image:: img/in4007_diode.png
.. image:: img/symbol_rectifier_diode.png
    :width: 200

Eine Gleichrichterdiode ist eine Halbleiterdiode, die verwendet wird, um Wechselstrom (AC) in Gleichstrom (DC) umzuwandeln, z. B. in einer Brückengleichrichterschaltung.  
In der Digitaltechnik wird sie häufig durch Schottky-Dioden ersetzt, die aufgrund ihrer geringen Schaltverluste geschätzt werden. Gleichrichterdioden können Ströme von Milliampere bis zu mehreren Kiloampere sowie Spannungen bis in den Kilovoltbereich leiten.  

Sie werden in der Regel aus Silizium gefertigt, wodurch sie hohe Stromstärken bewältigen können. Es existieren auch Varianten auf Basis von Germanium oder Galliumarsenid, die allerdings weniger verbreitet sind. Germaniumdioden besitzen eine niedrigere Sperrspannung und eine geringere zulässige Sperrschichttemperatur, bieten jedoch den Vorteil einer niedrigeren Schwellenspannung im Vorwärtsbetrieb im Vergleich zu Siliziumdioden.  

* `1N400x general-purpose diode  - Wikipedia <https://en.wikipedia.org/wiki/1N400x_general-purpose_diode>`_


**Zener Diode**

Eine Zener-Diode ist eine spezielle Diode, die so ausgelegt ist, dass sie bei Erreichen einer definierten Sperrspannung – der sogenannten Zenerspannung – zuverlässig in Sperrrichtung leitend wird.  

Sie weist bis zum kritischen Durchbruchspunkt einen sehr hohen Widerstand auf. Sobald dieser Punkt erreicht wird, sinkt der Widerstand stark ab, der Strom steigt an, während die Spannung in diesem Bereich nahezu konstant bleibt. Dadurch eignet sich die Zener-Diode hervorragend zur Spannungsstabilisierung.  

.. image:: img/zener_diode.png
.. image:: img/symbol-zener-diode.jpg


* `Zener diode - Wikipedia <https://en.wikipedia.org/wiki/Zener_diode>`_
