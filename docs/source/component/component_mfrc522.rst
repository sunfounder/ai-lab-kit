.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials und erweitere so deine Kenntnisse.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_mfrc522:

MFRC522 Module
=====================

**RFID**

Radio Frequency Identification (RFID) bezeichnet Technologien, die eine drahtlose Kommunikation zwischen einem Objekt (oder Tag) und einem Abfragegerät (Reader) nutzen, um Objekte automatisch zu identifizieren und nachzuverfolgen. Die Übertragungsreichweite eines Tags ist in der Regel auf wenige Meter vom Reader begrenzt. Eine direkte Sichtverbindung zwischen Reader und Tag ist dabei nicht zwingend erforderlich.

Die meisten Tags enthalten mindestens einen integrierten Schaltkreis (IC) sowie eine Antenne. Der Mikrochip speichert Informationen und steuert die Hochfrequenz-(RF)-Kommunikation mit dem Reader. Passive Tags besitzen keine eigene Energiequelle und sind auf ein externes elektromagnetisches Signal angewiesen, das vom Reader bereitgestellt wird. Aktive Tags hingegen verfügen über eine eigene Energiequelle, etwa eine Batterie, wodurch sie erweiterte Verarbeitungs- und Übertragungsfunktionen sowie eine größere Reichweite bieten.

.. image:: img/image230.png


**MFRC522**

Der MFRC522 ist ein integrierter Lese-/Schreibchip für RFID-Karten. Er arbeitet im 13,56-MHz-Bereich und wurde von NXP entwickelt. Mit seinem niedrigen Stromverbrauch, geringen Kosten und seiner kompakten Bauweise ist er eine ausgezeichnete Wahl für intelligente Messgeräte und tragbare Handheld-Geräte.

Der MFRC522 setzt auf moderne Modulations- und Demodulationsverfahren, die in allen gängigen passiven 13,56-MHz-Kontaktlos-Kommunikationsmethoden und -protokollen vollständig implementiert sind. Darüber hinaus unterstützt er den schnellen **CRYPTO1**-Verschlüsselungsalgorithmus zur Authentifizierung von MIFARE-Produkten. Der MFRC522 ist mit den MIFARE-Serien für Hochgeschwindigkeits-Kontaktlos-Kommunikation kompatibel und erreicht dabei eine bidirektionale Datenübertragungsrate von bis zu 424 kbit/s. 

Als neues Mitglied der hochintegrierten 13,56-MHz-Reader-Serie ähnelt der MFRC522 den bestehenden MFRC500- und MFRC530-Chips, weist jedoch auch deutliche Unterschiede auf. Die Kommunikation mit dem Hostsystem erfolgt über eine serielle Schnittstelle, wodurch weniger Verdrahtung nötig ist. Es stehen **SPI**, **I2C** sowie **UART** (ähnlich RS232) als Betriebsmodi zur Verfügung. Dies reduziert den Verkabelungsaufwand, spart Platz auf der Leiterplatte und senkt die Kosten.
