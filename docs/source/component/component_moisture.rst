.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_soil_moisture:

Soil Moisture Module
================================

.. image:: img/soil_mositure.png

* GND: Masse  
* VCC: Stromversorgung, 3,3 V ~ 5 V  
* AOUT: Gibt den Bodenfeuchtigkeitswert aus – je feuchter der Boden, desto kleiner der Messwert.  

Dieser kapazitive Bodenfeuchtigkeitssensor unterscheidet sich von den meisten resistiven Sensoren auf dem Markt, da er das Prinzip der kapazitiven Induktion zur Messung der Bodenfeuchtigkeit nutzt. Dadurch wird das Problem der Korrosionsanfälligkeit resistiver Sensoren vermieden und die Lebensdauer erheblich verlängert.  


Der Sensor besteht aus korrosionsbeständigen Materialien und überzeugt durch eine lange Lebensdauer. Er wird einfach in die Erde rund um die Pflanzen gesteckt, um die Bodenfeuchtigkeit in Echtzeit zu überwachen. Das Modul verfügt über einen integrierten Spannungsregler, der einen Betrieb im Spannungsbereich von 3,3 bis 5,5 V ermöglicht. Damit eignet es sich ideal für Mikrocontroller mit 3,3 V- und 5 V-Stromversorgung.  

Das folgende Diagramm zeigt den Schaltplan des kapazitiven Bodenfeuchtigkeitssensors.  

.. image:: img/solid_schematic.png

Ein fester Frequenzoszillator, aufgebaut mit einem 555-Timer-IC, erzeugt ein Rechtecksignal, das dem Sensor als kapazitives Element zugeführt wird. Für dieses Rechtecksignal weist der Kondensator eine bestimmte Reaktanz auf und bildet zusammen mit einem rein ohmschen Widerstand (10k Widerstand an Pin 3) einen Spannungsteiler.  

Je höher die Bodenfeuchtigkeit, desto größer die Kapazität des Sensors. Dadurch sinkt die Reaktanz für das Rechtecksignal, was die Spannung auf der Signalleitung reduziert. Somit nimmt der Messwert am analogen Eingang des Mikrocontrollers ab.  


**Specification**

* Betriebsspannung: 3,3 ~ 5,5 VDC  
* Ausgangsspannung: 0 ~ 3,0 VDC  
* Betriebsstrom: 5 mA  
* Schnittstelle: PH2.0-3P  
* Abmessungen: 3,86 × 0,905 Zoll (L × B)  
* Gewicht: 15 g  

