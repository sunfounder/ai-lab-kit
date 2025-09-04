.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_7_segment:

7-segment Display
======================

.. image:: img/7-seg.jpg

Ein 7-Segment-Display ist ein bauteilförmiges Modul in Form einer „8“, das aus 7 LEDs besteht. Jede LED wird als Segment bezeichnet – sobald sie aktiviert wird, bildet sie einen Teil einer darzustellenden Ziffer.

Es gibt zwei Arten von Anschlussvarianten: Common Cathode (CC) und Common Anode (CA). Wie der Name schon andeutet, sind bei einem CC-Display alle Kathoden der 7 LEDs verbunden, während bei einem CA-Display alle Anoden der 7 Segmente zusammengeschaltet sind.

In diesem Kit verwenden wir ein Common-Cathode-7-Segment-Display. Hier das entsprechende Schaltzeichen:

.. image:: img/segment_cathode.png
    :width: 800

Jede LED im Display ist einem bestimmten Segment zugeordnet, dessen Anschlussbein aus dem rechteckigen Kunststoffgehäuse herausgeführt ist. Diese Pins sind von „a“ bis „g“ beschriftet und stehen jeweils für eine LED. Die restlichen Pins sind zusammengeschaltet und bilden einen gemeinsamen Anschluss. Durch das gezielte Vorwärtsbeschalten der entsprechenden Pins in einer bestimmten Reihenfolge leuchten einige Segmente auf, während andere dunkel bleiben. Auf diese Weise wird das jeweilige Zeichen auf dem Display sichtbar.

**Display Codes** 

Um dir zu zeigen, wie 7-Segment-Anzeigen (Common Cathode) Zahlen darstellen, haben wir die folgende Tabelle erstellt. Dargestellt sind die Zahlen 0–F auf dem 7-Segment-Display. (DP) GFEDCBA gibt an, welche LEDs auf 0 oder 1 gesetzt werden. Beispiel: 00111111 bedeutet, dass DP und G auf 0 gesetzt sind, während alle anderen auf 1 stehen. Dadurch wird die Zahl 0 angezeigt. Der HEX-Code entspricht dabei der hexadezimalen Darstellung.

.. image:: img/segment_code.png

