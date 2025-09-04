.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_motor:

DC Motor
===================

.. image:: img/image114.jpeg
    :align: center

Dies ist ein 3V-DC-Motor. Wenn an seinen beiden Anschlüssen ein hohes und ein niedriges Signal anliegt, beginnt er sich zu drehen.

* **Größe**: 25 × 20 × 15 mm  
* **Betriebsspannung**: 1–6 V  
* **Leerlaufstrom** (3 V): 100 mA  
* **Leerlaufdrehzahl** (3 V): 10000 U/min  
* **Blockierstrom** (3 V): 800 mA  
* **Wellendurchmesser**: 2 mm  

Ein Gleichstrommotor (DC-Motor) ist ein kontinuierlicher Aktor, der elektrische Energie in mechanische Energie umwandelt. Durch die kontinuierliche Drehbewegung treiben DC-Motoren Pumpen, Lüfter, Kompressoren, Laufräder und andere Geräte an.  

Ein DC-Motor besteht aus zwei Hauptteilen: dem unbeweglichen Teil, dem **Stator**, und dem inneren, sich drehenden Teil, dem **Rotor** (oder auch **Anker** genannt), der die Bewegung erzeugt.  
Der entscheidende Punkt bei der Erzeugung von Bewegung ist die Platzierung des Ankers im Magnetfeld des Permanentmagneten (dessen Feld sich vom Nordpol zum Südpol erstreckt). Die Wechselwirkung zwischen dem Magnetfeld und den bewegten Ladungsträgern (der stromführende Draht erzeugt das Magnetfeld) erzeugt das Drehmoment, das den Anker in Rotation versetzt.  

.. image:: img/motor_sche.png
    :align: center

Der Strom fließt vom Pluspol der Batterie durch den Stromkreis, über die Kupferbürsten zum Kommutator und von dort zum Anker.  
Aufgrund der beiden Unterbrechungen im Kommutator kehrt sich dieser Stromfluss jedoch bei jeder vollen Umdrehung um.  
Diese kontinuierliche Umpolung wandelt die Gleichstromversorgung der Batterie faktisch in eine Wechselwirkung um, sodass der Anker stets im richtigen Moment das Drehmoment in die richtige Richtung erhält, um die Drehung aufrechtzuerhalten.  

