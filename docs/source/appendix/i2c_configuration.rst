.. _i2c_config:

I2C Configuration
-----------------------

**Step 1**: Aktiviere den I2C-Port deines Raspberry Pi (wenn er bereits aktiviert ist, kannst du diesen Schritt überspringen; falls du dir nicht sicher bist, fahre bitte fort).

.. raw:: html

   <run></run>
 
.. code-block:: 

    sudo raspi-config

**3 Interfacing options**

.. image:: img/image282.png
    :align: center

**I4 I2C**

.. image:: img/I4i2c.jpeg
    :align: center

**<Yes>, dann <Ok> -> <Finish>**

.. image:: img/image284.png
    :align: center

**Step 2:** Überprüfe, ob die I2C-Module geladen und aktiv sind.

.. raw:: html

   <run></run>
 
.. code-block:: 

    lsmod | grep i2c

Die folgende Ausgabe sollte erscheinen (die Zahlen können abweichen). Falls keine Ausgabe erfolgt, starte den Raspberry Pi mit ``sudo reboot`` neu.

.. code-block:: 

    i2c_dev                     6276    0
    i2c_bcm2708                 4121    0

**Step 3:** Installiere i2c-tools.

.. raw:: html

   <run></run>
 
.. code-block:: 

    sudo apt-get install i2c-tools

**Step 4:** Überprüfe die Adresse des I2C-Geräts.


.. raw:: html

    <run></run>
  
.. code-block:: 

    i2cdetect -y 1      # For Raspberry Pi 2 and higher version



.. raw:: html

   <run></run>
 
.. code-block:: 

    i2cdetect -y 0      # For Raspberry Pi 1


.. code-block:: 

    pi@raspberrypi ~ $ i2cdetect -y 1
        0  1  2  3   4  5  6  7  8  9   a  b  c  d  e  f
    00:           -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- -- --

Wenn ein I2C-Gerät angeschlossen ist, wird dessen Adresse angezeigt.

**Step 5:**

**Für C-Sprach-Nutzer:** Installiere libi2c-dev.

.. raw:: html

   <run></run>
 
.. code-block:: 

    sudo apt-get install libi2c-dev 

**Für Python-Nutzer:**

1. Aktivieren der virtuellen Umgebung.

.. note::
    
    * Bevor du die Umgebung aktivieren kannst, musst du sicherstellen, dass du eine virtuelle Umgebung erstellt hast. Siehe dazu: :ref:`create_virtual`.

    * Jedes Mal, wenn du den Raspberry Pi neu startest oder ein neues Terminal öffnest, musst du den folgenden Befehl erneut ausführen, um die virtuelle Umgebung zu aktivieren.

.. raw:: html

    <run></run>

.. code-block:: shell

    source myenv/bin/activate

Nach der Aktivierung siehst du den Namen der virtuellen Umgebung vor der Befehlszeile. Das zeigt an, dass du nun innerhalb der virtuellen Umgebung arbeitest.


2. Installiere smbus für I2C.

.. raw:: html

    <run></run>
 
.. code-block:: 

    sudo pip3 install smbus2


3. Beenden der virtuellen Umgebung.

Wenn du deine Arbeit abgeschlossen hast und die virtuelle Umgebung verlassen möchtest, führe einfach aus:

.. raw:: html

    <run></run>

.. code-block:: shell

    deactivate

Damit kehrst du in die globale Python-Umgebung des Systems zurück.