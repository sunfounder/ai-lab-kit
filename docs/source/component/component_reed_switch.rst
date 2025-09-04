.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_reed_switch:

Reed Switch Module
======================

.. image:: img/reed_switch.png
    :width: 300
    :align: center

* Verwendet einen normalerweise offenen Reed-Schalter.  
* Komparatorausgang, sauberes Signal, gutes Wellenformverhalten, starke Treibfähigkeit, mehr als 15 mA.  
* Betriebsspannung: 3,3 V – 5 V  
* Ausgangsform: digitaler Schaltausgang (0 und 1).  
* Mit Befestigungsbohrungen für einfache Montage.  
* Kleine Leiterplattengröße: 3,2 cm x 1,4 cm.  
* Verwendet LM393-Komparator mit weitem Spannungsbereich.  

Das Reed-Switch-Modul besteht aus einem Reed-Schalter, Potentiometer, LM393-Komparator, LED usw. Das interne Schaltbild ist unten dargestellt: Befindet sich ein Magnet in der Nähe des Moduls, wird es eingeschaltet und gibt ein Low-Signal aus. Ist kein Magnetfeld vorhanden, bleibt es ausgeschaltet und liefert ein High-Signal. Der Erfassungsabstand zwischen Reed-Schalter und Magnet sollte innerhalb von 1,5 cm liegen – darüber hinaus sinkt die Empfindlichkeit oder es erfolgt keine Auslösung. Die Empfindlichkeit kann über das Potentiometer auf dem Modul angepasst werden.  

.. image:: img/reedswitch_sche.jpg
    :width: 600
    :align: center

Ein Reed-Schalter, auch Magnetschalter oder Reedkontakt genannt,  
besteht aus zwei Metallzungen, die in einem Glasröhrchen mit Inertgas versiegelt sind. Normalerweise liegen die beiden Zungen parallel zueinander, sind jedoch durch einen Spalt getrennt, sodass der Stromkreis offen ist. Befindet sich ein magnetisches Objekt in der Nähe, ziehen sich die Zungen durch die magnetische Kraft gegenseitig an und berühren sich, wodurch der Stromkreis geschlossen wird. Auf diese Weise kann der Reed-Schalter als Magnetsensor eingesetzt werden.  

.. image:: img/HowItWorksReed.jpg

