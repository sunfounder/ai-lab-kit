.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _assemble_hat:

.. start_assemble_hat

Fusion HAT+ montieren und einschalten (Wichtig)
=======================================================

Fusion HAT+ mit dem Raspberry Pi verbinden
---------------------------------------------------------

Hier zeigen wir Ihnen, wie Sie das Fusion HAT+ montieren.

#. Montieren Sie die Basis.
#. Befestigen Sie den Akku auf der Basis.
#. Befestigen Sie den Raspberry Pi mit Abstandshaltern.
#. Verbinden Sie das FPC-Kabel mit dem Raspberry Pi. (Wir montieren es zusammen mit dem Kameramodul, wenn wir die Pan-Tilt-Halterung zusammenbauen.)
#. Stecken Sie das Fusion HAT+ auf den 40-Pin-Anschluss des Raspberry Pi.
#. **Setzen Sie den Akku ein.** (Dies ist sehr wichtig. Wenn der Akku nicht eingesetzt ist, funktioniert das Fusion HAT+ nicht.)

Weitere Details zur Montage finden Sie im folgenden Video.

.. raw:: html

  <iframe width="100%" 
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/HlAayd1mSxU?si=oZnKyZihyyjQhsHl" 
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
    </iframe>



Aufladen
-------------------

Vor der ersten Verwendung wird empfohlen, den Akku vollständig aufzuladen. Sie können dazu das mitgelieferte USB-Type-C-Ladekabel oder ein eigenes USB-C-Ladegerät verwenden.

.. note::

  Der Akku kann mit geringer Ladung geliefert werden, da Amazon verlangt, dass er vor dem Lufttransport unter 30 % geladen ist. Sie **MÜSSEN** ihn vor der Verwendung vollständig aufladen, um Tiefentladung und mögliche Schäden zu vermeiden.
  Schließen Sie das USB-C-Kabel an das Fusion HAT+ an; der Akku wird automatisch geladen. Sie müssen dabei **keine** Stromversorgung direkt mit dem Raspberry Pi verbinden.

* Wir empfehlen ein **5V-3A-Netzteil**, zum Beispiel das offizielle Raspberry Pi 15W-Netzteil.
* Sie können auch ein **USB-C-PD (Power Delivery)**-Ladegerät oder ein **QC-2.0-Schnellladegerät** verwenden.
* Das vollständige Aufladen von 0 % bis 100 % dauert in der Regel etwa **2 Stunden**.

.. image:: img/power_charge.jpg
   :width: 400
   :align: center

Das Fusion HAT+ verfügt über **zwei Batterie-Status-LEDs**, die den Spannungszustand des Akkus anzeigen:

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED-Status
     - Batteriespannung
   * - 2 LEDs AN
     - > 7.4V
   * - 1 LED AN
     - < 7.4V
   * - Beide LEDs AUS
     - < 6.5V

Während des Ladevorgangs blinkt eine der LEDs, um den Ladefortschritt anzuzeigen:

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED-Status
     - Batteriespannung
   * - 1 LED AN, 1 LED blinkt
     - > 7.4V
   * - Nur 1 LED blinkt
     - < 7.4V


Nach dem vollständigen Aufladen:

* **Wenn das Fusion HAT+ eingeschaltet ist**, bleiben beide LEDs dauerhaft an.
* **Wenn das Fusion HAT+ ausgeschaltet ist**, gehen beide LEDs aus.

.. note::

   Für längere Programmier- oder Debug-Sitzungen können Sie das Fusion HAT+ dauerhaft über das USB-C-Kabel mit Strom versorgen.
   Dabei wird der Akku gleichzeitig geladen und das Fusion HAT+ betrieben.
   Auch wenn das Fusion HAT+ während des Ladevorgangs verwendet wird, darf der Akku **nicht** entfernt werden.

Einschalten
----------------------

Wenn der Akku ausreichend geladen ist, drücken Sie kurz den **Power-Button** auf dem Fusion HAT+.

* Die **PWR-LED** leuchtet auf.
* Die **Batterie-LEDs** leuchten ebenfalls.
* Der Raspberry Pi startet automatisch.

.. image:: img/power_button.jpg
    :width: 400

.. end_assemble_hat

.. _assemble_fusion_hat_pan_tilt:

Pan-Tilt montieren (für die Kamera)
------------------------------------------------------

Um das Kameramodul einfacher zu verwenden, können Sie eine Pan-Tilt-Halterung montieren.

.. note::

  Das Montieren der Pan-Tilt-Halterung kann einige Pins verdecken. Es wird daher empfohlen, sie nur zu montieren, wenn die Kamera verwendet wird, oder sie nach dem Zusammenbau außen zu platzieren.

.. image:: img/gimbal_assemble.png

Weitere Details zur Montage finden Sie im folgenden Video.

.. raw:: html

  <iframe width="100%" 
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/7CkGPKnbjM4" 
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
    </iframe>