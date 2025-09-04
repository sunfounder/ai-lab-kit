.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_ultrasonic_sensor:

Ultraschall-Modul
================================

.. image:: img/ultrasonic_pic.png
    :width: 400
    :align: center

Das Ultraschall-Entfernungsmodul ermöglicht berührungslose Messungen im Bereich von 2 cm bis 400 cm, mit einer Messgenauigkeit von bis zu 3 mm.  
Innerhalb von 5 m bleibt das Signal stabil, nach 5 m wird es allmählich schwächer und verschwindet spätestens bei 7 m.

Das Modul besteht aus einem Ultraschall-Sender, einem Empfänger und einer Steuerschaltung. Die Grundprinzipien sind:

#. Mit einem IO-Flipflop wird ein High-Pegel-Signal von mindestens 10 µs verarbeitet.

#. Das Modul sendet automatisch acht 40-kHz-Impulse aus und überprüft, ob ein Rücksignal empfangen wird.

#. Wird ein Signal zurückgegeben, so entspricht die Dauer des High-Pegels am Ausgang der Zeitspanne zwischen Aussendung und Empfang der Ultraschallwelle.  
   Testdistanz = (High-Pegel-Zeit × Schallgeschwindigkeit (340 m/s)) / 2.



Das Zeitdiagramm ist unten dargestellt:

.. image:: img/ultrasonic228.png

Zum Start der Entfernungsmessung genügt es, einen kurzen Impuls von 10 µs an den Trigger-Eingang anzulegen.  
Daraufhin sendet das Modul eine Serie von 8 Ultraschallzyklen bei 40 kHz aus und setzt das Echo-Signal.  
Die Entfernung wird anhand der Zeitspanne zwischen dem Sendeimpuls und dem Empfang des Echos berechnet.

Formel: us / 58 = Zentimeter oder us / 148 = Zoll; alternativ:  
Reichweite = High-Pegel-Zeit × Schallgeschwindigkeit (340 m/s) / 2.  

Es wird empfohlen, Messzyklen von mehr als 60 ms einzuhalten, um Signalüberlagerungen zwischen Trigger- und Echo-Signal zu vermeiden.

