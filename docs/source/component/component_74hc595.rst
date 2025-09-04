.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_74hc595:

74HC595
===========

.. image:: img/74HC595.png

Der 74HC595 besteht aus einem 8-Bit-Schieberegister und einem Speicherregister mit dreistufigen parallelen Ausgängen. Er wandelt serielle Eingaben in parallele Ausgaben um und spart so IO-Pins eines Mikrocontrollers.  
Wenn MR (Pin 10) auf High und OE (Pin 13) auf Low liegt, werden die Daten an der steigenden Flanke von SHcp eingelesen und über dieselbe Flanke ins Speicherregister übertragen. Sind beide Takte verbunden, läuft das Schieberegister stets einen Puls vor dem Speicherregister.  
Das Speicherregister verfügt über einen seriellen Eingangspin (Ds), einen seriellen Ausgangspin (Q) sowie einen asynchronen Reset-Eingang (Low-aktiv). Es stellt einen parallelen 8-Bit-Bus mit drei Zuständen bereit. Wenn OE aktiviert ist (Low), werden die Daten aus dem Speicherregister auf den Bus ausgegeben.

* `74HC595 Datasheet <https://www.ti.com/lit/ds/symlink/cd74hc595.pdf?ts=1617341564801>`_

.. image:: img/74hc595_pin.png
    :width: 600

Pins des 74HC595 und ihre Funktionen:

* **Q0-Q7**: 8-Bit parallele Datenausgänge, können direkt 8 LEDs oder 8 Pins einer 7-Segment-Anzeige steuern.  
* **Q7’**: Serieller Ausgangspin, wird mit DS eines weiteren 74HC595 verbunden, um mehrere Bausteine in Reihe zu schalten.  
* **MR**: Reset-Pin, Low-aktiv.  
* **SHcp**: Takteingang des Schieberegisters. An der steigenden Flanke werden die Daten im Schieberegister jeweils um eine Position verschoben (z. B. von Q1 nach Q2 usw.). An der fallenden Flanke bleiben die Daten unverändert.  
* **STcp**: Takteingang des Speicherregisters. An der steigenden Flanke werden die Daten aus dem Schieberegister ins Speicherregister übernommen.  
* **CE**: Output-Enable-Pin, Low-aktiv.  
* **DS**: Serieller Dateneingangspin.  
* **VCC**: Betriebsspannung.  
* **GND**: Masse.  


