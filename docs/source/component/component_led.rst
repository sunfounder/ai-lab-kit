.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials und erweitere so deine Kenntnisse.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_led:

LED
==========

.. image:: img/LED.png
    :width: 400

Die lichtemittierende Diode (LED) ist ein Halbleiterbauelement, das elektrische Energie über PN-Übergänge in Lichtenergie umwandelt. Je nach Wellenlänge wird sie in Laserdioden, Infrarot-Leuchtdioden und sichtbare Leuchtdioden unterteilt, wobei letztere allgemein als LEDs bekannt sind.  

Da Dioden eine gerichtete Leitfähigkeit besitzen, fließt der Strom nur in einer Richtung, wie es das Pfeilsymbol in der Schaltung anzeigt. Der Pluspol muss mit der Anode und der Minuspol mit der Kathode verbunden werden, damit die LED aufleuchtet.  

.. image:: img/led_symbol.png


Eine LED besitzt zwei Pins: Der längere ist die Anode, der kürzere die Kathode. Achte darauf, sie nicht vertauscht anzuschließen. LEDs haben einen festen Spannungsabfall in Durchlassrichtung und dürfen nicht direkt an die Versorgungsspannung angeschlossen werden, da diese höher als der Spannungsabfall sein kann und die LED beschädigt würde.  
Der Spannungsabfall einer roten, gelben oder grünen LED beträgt etwa 1,8 V, während er bei einer weißen LED ca. 2,6 V beträgt. Die meisten LEDs vertragen einen maximalen Strom von 20 mA, daher muss ein Vorwiderstand in Reihe geschaltet werden.  

Die Formel für den Widerstandswert lautet:

    R = (Vsupply – VD)/I

**R** steht für den Widerstandswert des Vorwiderstands, **Vsupply** für die Versorgungsspannung, **VD** für den Spannungsabfall und **I** für den Betriebsstrom der LED.  

Eine ausführliche Einführung findest du hier: `LED - Wikipedia <https://en.wikipedia.org/wiki/Light-emitting_diode>`_.

