.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_touch_switch:

Touch-Schalter-Modul
==================================

.. image:: img/touch168.png
    :width: 300
    :align: center

Das Touch-Schalter-Modul arbeitet, indem es Änderungen in der Kapazität erkennt, die durch den Einfluss eines externen Objekts verursacht werden. Die Touchfläche ist mit isolierendem Material bedeckt, sodass der Benutzer keinen direkten Kontakt mit der elektrischen Schaltung hat.

Ein kapazitiver Touch-Schalter besteht aus mehreren Schichten — einer oberen Isolationsschicht, gefolgt von der Touchfläche, einer weiteren Isolationsschicht und schließlich der Massefläche.

.. image:: img/touch169.jpeg

In der Praxis kann ein kapazitiver Sensor auf einer doppelseitigen Leiterplatte realisiert werden, wobei eine Seite als Touch-Sensor und die gegenüberliegende als Massefläche des Kondensators dient. Wird Spannung an diese Flächen angelegt, laden sich beide auf. Im Gleichgewichtszustand liegt an beiden Platten die gleiche Spannung wie an der Spannungsquelle an.

Die Touch-Detektorschaltung verfügt über einen Oszillator, dessen Frequenz von der Kapazität des Touchpads abhängt. Nähert sich ein Finger der Touchfläche, erhöht sich die Kapazität und verändert dadurch die Frequenz des internen Oszillators. Die Schaltung überwacht diese Frequenz in zeitlichen Abständen, und sobald die Abweichung einen festgelegten Schwellenwert überschreitet, löst die Schaltung ein Tastendruck-Ereignis aus.

