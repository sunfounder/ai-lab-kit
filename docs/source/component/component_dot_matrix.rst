.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_dot_matrix:

LED Matrix Module
==============================

.. image:: img/max7219_module.jpg
    :width: 400
    :align: center

Dies ist ein 8x8-Punktmatrix-Modul mit gemeinsamer Kathode, das über den MAX7219 angesteuert wird.  
Das Modul arbeitet mit einer Betriebsspannung von 5V, die Abmessungen betragen 50mm x 32mm x 15mm.  
Links befindet sich der Eingangsport, rechts der Ausgangsport – mehrere Module können in Reihe geschaltet werden.

* **VCC**: Positive Versorgungsspannung. Mit +5V verbinden.  
* **GND**: Masse (beide GND-Pins müssen verbunden werden).  
* **DIN**: Serieller Dateneingang. Daten werden an der steigenden Flanke von CLK ins interne 16-Bit-Schieberegister geladen.  
* **CS**: Chip-Select-Eingang. Solange CS auf Low liegt, werden serielle Daten ins Schieberegister geladen. Mit der steigenden Flanke von CS werden die letzten 16 Bits übernommen.  
* **CLK**: Serieller Takteingang. Maximalrate 10 MHz. Bei der steigenden Flanke von CLK werden Daten ins Register eingelesen, bei der fallenden Flanke über DOUT ausgegeben. Beim MAX7221 ist der CLK-Eingang nur aktiv, solange CS auf Low liegt.  

**MAX7219**

Der MAX7219 ist ein kompakter Displaytreiber mit serieller Ein-/Ausgabe und gemeinsamer Kathode. Er ermöglicht die Ansteuerung von 7-Segment-LED-Anzeigen mit bis zu 8 Stellen, Balkenanzeigen oder bis zu 64 einzelnen LEDs.  
Im Chip integriert sind ein BCD-Code-B-Decoder, Multiplex-Scan-Logik, Segment- und Digit-Treiber sowie ein 8x8-Statik-RAM zur Speicherung der einzelnen Digits.  

Zur Strombegrenzung aller LEDs ist nur ein externer Widerstand erforderlich. Der MAX7221 ist zudem kompatibel mit SPI™, QSPI™ und MICROWIRE™ und verfügt über flankenbegrenzte Segmenttreiber zur Reduzierung elektromagnetischer Störungen (EMI).  

Ein praktisches 4-Draht-Interface erlaubt die Verbindung mit gängigen Mikroprozessoren. Einzelne Digits können gezielt adressiert und aktualisiert werden, ohne die gesamte Anzeige neu zu beschreiben. Darüber hinaus bieten MAX7219/MAX7221 die Wahl zwischen Code-B-Dekodierung oder keiner Dekodierung für jedes einzelne Digit.  

.. image:: img/max7219_sche.png

* `MAX7219 Datasheet <https://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf>`_

