.. note:: 

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_transistor:

Transistor
============

.. image:: img/npn_pnp.png
    :width: 300

Ein Transistor ist ein Halbleiterbauelement, das Strom durch Strom steuert. Er verstärkt schwache Signale zu Signalen mit größerer Amplitude und dient zudem als berührungsloser Schalter.  

Ein Transistor besteht aus einer Dreischichtstruktur aus P- und N-Typ-Halbleitern, die intern drei Zonen bilden. Die dünnere mittlere Schicht ist die Basisregion; die beiden anderen sind N- oder P-Typ. Die kleinere Zone mit hoher Konzentration an Majoritätsladungsträgern ist die Emitter-Region, die andere die Kollektor-Region. Durch diese Struktur kann der Transistor als Verstärker eingesetzt werden.  
Aus diesen drei Regionen ergeben sich drei Anschlüsse: Basis (b), Emitter (e) und Kollektor (c). Sie bilden zwei P-N-Übergänge, nämlich den Emitter- und den Kollektor-Übergang. Die Pfeilrichtung im Transistorsymbol zeigt die Richtung des Emitter-Übergangs an.  

* `P–N junction - Wikipedia <https://en.wikipedia.org/wiki/P-n_junction>`_

Je nach Halbleitertyp unterscheidet man zwei Gruppen: NPN- und PNP-Transistoren. Wie die Abkürzungen erkennen lassen, besteht ein NPN-Transistor aus zwei N-Typ- und einem P-Typ-Halbleiter, während es beim PNP-Typ umgekehrt ist. Siehe Abbildung unten.  

.. note::
    Der S8550 ist ein PNP-Transistor und der S8050 ein NPN-Transistor. Sie sehen sich sehr ähnlich, daher sollte man die Beschriftung sorgfältig prüfen.


.. image:: img/transistor_symbol.png
    :width: 600

Wird ein High-Pegel-Signal an einen NPN-Transistor angelegt, wird er durchgeschaltet. Ein PNP-Transistor hingegen benötigt ein Low-Pegel-Signal, um zu leiten. Beide Typen werden häufig für berührungslose Schalter verwendet, wie in diesem Experiment.  

Hält man die beschriftete Seite nach vorne und die Pins nach unten, so gilt: Von links nach rechts sind die Anschlüsse Emitter (e), Basis (b) und Kollektor (c).  

.. image:: img/ebc.png
    :width: 150


* `S8050 Transistor Datasheet <https://datasheet4u.com/datasheet-pdf/WeitronTechnology/S8050/pdf.php?id=576670>`_
* `S8550 Transistor Datasheet <https://www.mouser.com/datasheet/2/149/SS8550-118608.pdf>`_

