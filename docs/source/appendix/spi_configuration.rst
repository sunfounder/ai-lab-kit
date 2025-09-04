.. _spi_configuration:

SPI Configuration
-----------------------

**Step 1**: Aktiviere den SPI-Port deines Raspberry Pi (wenn er bereits aktiviert ist, kannst du diesen Schritt überspringen; falls du dir nicht sicher bist, fahre bitte fort).

.. raw:: html

   <run></run>

.. code-block:: 

    sudo raspi-config

**3 Interfacing options**

.. image:: img/image282.png
   :align: center

**I3 SPI**

.. image:: img/i3spi.png
   :align: center

**<YES>, anschließend <OK> und <Finish> auswählen.**

.. image:: img/image286.png
   :align: center 

**Step 2:** Überprüfe, ob die SPI-Module geladen und aktiv sind.

.. raw:: html

   <run></run>

.. code-block:: 

    ls /dev/sp*

Die folgende Ausgabe sollte erscheinen (die Zahlen können variieren):


.. code-block:: 

    /dev/spidev0.0  /dev/spidev0.1

**Step 3:** Installiere das Python-Modul SPI-Py.

.. raw:: html

   <run></run>

.. code-block:: 

    git clone https://github.com/lthiery/SPI-Py.git
    cd SPI-Py
    sudo python3 setup.py install

.. note::
    Dieser Schritt ist nur für Python-Nutzer relevant. Wenn du in C programmierst, kannst du ihn überspringen.
