.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_resistor:

Resistor
============

.. image:: img/resistor.png
    :width: 300

Ein Widerstand ist ein elektronisches Bauelement, das den Stromfluss in einem Stromzweig begrenzt.  
Ein Festwiderstand besitzt einen festen, nicht veränderbaren Widerstandswert, während bei einem Potentiometer oder verstellbaren Widerstand der Wert angepasst werden kann.  

Im Schaltplan gibt es zwei gebräuchliche Symbole für Widerstände. Normalerweise ist der Widerstandswert direkt angegeben. Wenn du also eines dieser Symbole in einer Schaltung siehst, steht es für einen Widerstand.  

.. image:: img/resistor_symbol.png
    :width: 400

**Ω** ist die Einheit des elektrischen Widerstands. Größere Einheiten sind KΩ und MΩ.  
Das Verhältnis lautet: 1 MΩ = 1000 KΩ, 1 KΩ = 1000 Ω. Der Widerstandswert ist in der Regel auf dem Bauteil angegeben.  

Um den Wert eines Widerstands zu bestimmen, gibt es zwei Methoden: Entweder man liest die Farbringe ab oder misst den Wert mit einem Multimeter. Empfohlen wird die erste Methode, da sie schneller und einfacher ist.  

.. image:: img/resistance_card.jpg

Wie auf der Karte dargestellt, steht jede Farbe für eine Zahl.  

.. list-table::

   * - Schwarz
     - Braun
     - Rot
     - Orange
     - Gelb
     - Grün
     - Blau
     - Violett
     - Grau
     - Weiß
     - Gold
     - Silber
   * - 0
     - 1
     - 2
     - 3
     - 4
     - 5
     - 6
     - 7
     - 8
     - 9
     - 0,1
     - 0,01

Am häufigsten werden Widerstände mit 4 oder 5 Farbringen eingesetzt.  

Oft ist es anfangs schwierig zu erkennen, von welcher Seite man mit dem Ablesen beginnt.  
Der Trick: Der Abstand zwischen dem 4. und 5. Ring ist meist größer als die Abstände zwischen den anderen Ringen.  

Wenn also an einem Ende des Widerstands ein größerer Abstand zwischen zwei Farbringen erkennbar ist, beginnt man von der gegenüberliegenden Seite zu lesen.  

Sehen wir uns als Beispiel das Ablesen eines 5-Band-Widerstands an:  

.. image:: img/220ohm.jpg
    :width: 500

Dieser Widerstand wird von links nach rechts gelesen.  
Das Schema lautet: 1. Band – 2. Band – 3. Band × 10^Multiplikator (Ω), mit einer Toleranzangabe in %.  

Für diesen Widerstand ergibt sich also: 2 (rot) 2 (rot) 0 (schwarz) × 10^0 (schwarz) Ω = 220 Ω,  
und die zulässige Abweichung beträgt ±1 % (braun).  

.. list-table::Common resistor color band
    :header-rows: 1

    * - Widerstand 
      - Farbcode  
    * - 10Ω   
      - braun schwarz schwarz silber braun
    * - 100Ω   
      - braun schwarz schwarz schwarz braun
    * - 220Ω 
      - rot rot schwarz schwarz braun
    * - 330Ω 
      - orange orange schwarz schwarz braun
    * - 1kΩ 
      - braun schwarz schwarz braun braun
    * - 2kΩ 
      - rot schwarz schwarz braun braun
    * - 5.1kΩ 
      - grün braun schwarz braun braun
    * - 10kΩ 
      - braun schwarz schwarz rot braun 
    * - 100kΩ 
      - braun schwarz schwarz orange braun 
    * - 1MΩ 
      - braun schwarz schwarz grün braun 

Mehr Informationen über Widerstände findest du hier:  
`Resistor - Wikipedia <https://en.wikipedia.org/wiki/Resistor>`_.
