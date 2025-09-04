.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_relay:

Relay
==========================================

.. image:: img/relay_pic.png
    :width: 200
    :align: center

Ein Relais ist ein Bauelement, das Verbindungen zwischen zwei oder mehr Punkten bzw. Geräten herstellt, sobald ein Eingangssignal anliegt. Anders gesagt: Ein Relais sorgt für eine galvanische Trennung zwischen Steuerung und Last, da Verbraucher sowohl mit Gleichstrom (DC) als auch mit Wechselstrom (AC) betrieben werden können. Mikrocontroller hingegen arbeiten mit DC-Signalen, sodass ein Relais notwendig ist, um diese Lücke zu überbrücken. Relais sind besonders nützlich, wenn mit einem kleinen Steuersignal große Ströme oder Spannungen geschaltet werden müssen.

Jedes Relais besteht aus fünf Hauptkomponenten:

.. image:: img/relay142.jpeg

**Elektromagnet** – Ein Eisenkern, umwickelt mit einer Spule. Fließt Strom durch die Spule, wird der Kern magnetisch und wirkt somit als Elektromagnet.

**Anker (Armature)** – Der bewegliche Magnetstreifen wird als Anker bezeichnet. Wird die Spule erregt, erzeugt sie ein Magnetfeld, das den Anker bewegt und die normalerweise offenen (N/O) oder normalerweise geschlossenen (N/C) Kontakte betätigt. Der Anker kann sowohl mit Gleich- als auch mit Wechselstrom bewegt werden.

**Feder** – Fließt kein Strom durch die Spule des Elektromagneten, zieht die Feder den Anker zurück, sodass der Stromkreis unterbrochen bleibt.

**Kontaktpaar** – Relais besitzen zwei Arten von Kontakten:

- Normally Open (N/O) – geschlossen, wenn das Relais aktiviert ist, geöffnet, wenn es inaktiv ist.  
- Normally Closed (N/C) – geöffnet, wenn das Relais aktiviert ist, geschlossen, wenn es inaktiv ist.  

**Gehäuse** – Relais sind meist von einem Kunststoffrahmen umschlossen, der Schutz bietet.

Das Funktionsprinzip eines Relais ist einfach:  
Wird das Relais mit Strom versorgt, fließt ein Strom durch die Steuerspule und der Elektromagnet wird erregt. Dadurch zieht er den Anker an, wodurch die beweglichen Kontakte nach unten auf die N/O-Kontakte gedrückt werden und der Lastkreis geschlossen wird.  
Wird die Versorgung getrennt, fällt die Magnetkraft ab, die Feder zieht den Anker zurück und verbindet die beweglichen Kontakte mit den N/C-Kontakten. Auf diese Weise kann durch das Ein- und Ausschalten des Relais der Zustand eines Lastkreises präzise gesteuert werden.
