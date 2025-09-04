.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_rgb_led:

RGB LED
=================

.. image:: img/rgb_led.png
    :width: 100
    
RGB-LEDs können Licht in unterschiedlichen Farben abstrahlen. Eine RGB-LED vereint drei LEDs – Rot, Grün und Blau – in einem transparenten oder halbtransparenten Kunststoffgehäuse. Durch Variation der Eingangsspannungen an den drei Pins und deren Überlagerung können verschiedene Farben erzeugt werden. Statistisch lassen sich so bis zu 16.777.216 Farbtöne darstellen. 

.. image:: img/rgb_light.png
    :width: 600

RGB-LEDs lassen sich in zwei Typen unterteilen: **gemeinsame Anode** und **gemeinsame Kathode**. In diesem Kit wird die Variante mit gemeinsamer Kathode verwendet. **Common Cathode (CC)** bedeutet, dass die Kathoden aller drei LEDs miteinander verbunden sind. Nach dem Anschluss an GND und dem Anlegen von Signalen an die drei übrigen Pins leuchtet die LED in der jeweiligen Farbe. 

Das zugehörige Schaltsymbol ist unten dargestellt:

.. image:: img/rgb_symbol.png
    :width: 300

Eine RGB-LED besitzt insgesamt 4 Pins: Der längste Pin ist GND, die übrigen drei sind Rot, Grün und Blau. An der Kunststoffhülle befindet sich eine Kerbe; der nächstgelegene Pin ist der erste und entspricht dem roten Kanal, gefolgt von GND, Grün und Blau. 

.. image:: img/rgb_pin.jpg
    :width: 200

