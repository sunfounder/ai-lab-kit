.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_4_digit:

4-Digit 7-Segment Display
==================================

Das 4-stellige 7-Segment-Display besteht aus vier einzelnen 7-Segment-Anzeigen, die zusammenarbeiten.

.. image:: img/4-digit-sche.png

Jede Stelle des 4-stelligen 7-Segment-Displays arbeitet unabhängig. Mithilfe des Prinzips der visuellen Persistenz wird jede Ziffer nacheinander sehr schnell angezeigt, sodass durch die Nachbildwirkung ein kontinuierlicher Zeichenstring sichtbar wird.

Beispiel: Wenn „1234“ dargestellt wird, zeigt zunächst das erste 7-Segment die „1“, während die anderen dunkel bleiben. Nach kurzer Zeit zeigt das zweite Segment die „2“, während die übrigen nichts anzeigen. Dieser Vorgang setzt sich für alle vier Segmente fort. Da der Zyklus sehr kurz ist (typischerweise etwa 5 ms) und das menschliche Auge ein optisches Nachbild hat, nehmen wir alle vier Ziffern gleichzeitig wahr.

.. image:: img/image78.png


**Display Codes**

Um dir den Aufbau eines 7-Segment-Displays (Common Anode) zu verdeutlichen, haben wir die folgende Tabelle erstellt. Sie zeigt die Darstellung der Zahlen 0–F auf dem 7-Segment-Display. (DP) GFEDCBA steht dabei für die jeweiligen LEDs, die auf 0 oder 1 gesetzt werden. Beispiel: 11000000 bedeutet, dass DP und G auf 1 gesetzt sind, während alle anderen auf 0 stehen. Damit wird die Zahl 0 dargestellt. Der HEX-Code entspricht der jeweiligen hexadezimalen Darstellung.

.. image:: img/common_anode.png

