.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_mpu6050:

MPU6050 Modul
===================

.. image:: img/mpu6050_pic.png
    :width: 200
    :align: center

Das MPU-6050 ist ein 6-Achsen-Bewegungssensor (bestehend aus einem 3-Achsen-Gyroskop und einem 3-Achsen-Beschleunigungsmesser).

Seine drei Koordinatenachsen sind wie folgt definiert:

Lege das MPU6050 flach auf den Tisch, sodass die Seite mit der Beschriftung nach oben zeigt und sich der Punkt auf dieser Fläche in der oberen linken Ecke befindet. Die senkrechte Richtung nach oben entspricht dann der Z-Achse des Chips. Die Richtung von links nach rechts stellt die X-Achse dar. Dementsprechend ist die Richtung von hinten nach vorne die Y-Achse.  

.. image:: img/mpu223.png


**3-Achsen-Beschleunigungsmesser**

Der Beschleunigungsmesser arbeitet nach dem piezoelektrischen Effekt – der Fähigkeit bestimmter Materialien, bei mechanischer Belastung eine elektrische Ladung zu erzeugen.  

Stelle dir ein quaderförmiges Gehäuse vor, in dem sich eine kleine Kugel befindet (wie in der Abbildung oben). Die Wände dieses Gehäuses bestehen aus piezoelektrischen Kristallen. Neigst du den Quader, bewegt sich die Kugel aufgrund der Schwerkraft in Richtung der Neigung. Die Wand, auf die die Kugel trifft, erzeugt dabei winzige piezoelektrische Ströme. Insgesamt gibt es drei Paare gegenüberliegender Wände in einem Quader, die jeweils einer Achse im 3D-Raum entsprechen: X-, Y- und Z-Achse. Anhand der Ströme, die in den piezoelektrischen Wänden erzeugt werden, lässt sich die Richtung und Größe der Neigung bestimmen.  

.. image:: img/mpu224.png


Mit dem MPU6050 lässt sich die Beschleunigung auf jeder Koordinatenachse erfassen (im stationären Ruhezustand beträgt die Z-Achse 1 g, während X- und Y-Achse 0 anzeigen). Bei Neigung oder unter Bedingungen wie Schwerelosigkeit oder Überlastung ändern sich die entsprechenden Messwerte.  

Es stehen vier programmierbare Messbereiche zur Verfügung: ±2g, ±4g, ±8g und ±16g (Standard: ±2g), wobei jeder Bereich eine bestimmte Genauigkeit bietet. Die Werte reichen von -32768 bis 32767.  

Die Messwerte des Beschleunigungsmessers werden durch Umrechnung vom Rohwert in den entsprechenden Messbereich in Beschleunigungswerte übertragen.  

Beschleunigung = (Rohdaten der Achse / 65536 \* Vollbereich des Beschleunigungsmessers) g  

Beispiel X-Achse: Wenn der Rohwert des Beschleunigungssensors 16384 beträgt und der Bereich ±2g gewählt ist:  

**Beschleunigung entlang der X-Achse = (16384 / 65536 \* 4) g** **=1g**  

**3-Achsen-Gyroskop**

Gyroskope arbeiten nach dem Prinzip der Corioliskraft. Man stelle sich eine gabelähnliche Struktur vor, die sich ständig vor- und zurückbewegt. Sie wird mithilfe piezoelektrischer Kristalle fixiert. Versucht man nun, diese Anordnung zu kippen, wirkt auf die Kristalle eine Kraft in Richtung der Neigung. Diese Kraft entsteht durch die Trägheit der bewegten Gabel. Die Kristalle erzeugen dadurch einen Strom im Einklang mit dem piezoelektrischen Effekt, der anschließend verstärkt wird.  

.. image:: img/mpu225.png

Das Gyroskop verfügt ebenfalls über vier Messbereiche: ±250, ±500, ±1000 und ±2000 °/s. Das Berechnungsverfahren entspricht im Wesentlichen dem des Beschleunigungsmessers.  

Die Formel zur Umrechnung des Rohwerts in die Winkelgeschwindigkeit lautet:  

Winkelgeschwindigkeit = (Rohdaten der Gyroskop-Achse / 65536 \* Vollbereich des Gyroskops) °/s  

Beispiel X-Achse: Wenn der Rohwert des Gyroskops 16384 beträgt und der Bereich ±250 °/s gewählt ist:  

**Winkelgeschwindigkeit entlang der X-Achse = (16384 / 65536 \* 500) °/s** **=125°/s**
