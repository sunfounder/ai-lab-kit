.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!


.. _install_all_modules:

5. Configure Power & Install Software (Important)
================================================================

In this chapter, you’ll set up safe power management, install the related software, configure audio, and learn how to handle shutdowns and the App service.


Configure Shutdown Behavior
----------------------------

The Fusion HAT relies on the Raspberry Pi shutdown signal to manage the full system power.  
Therefore, you need to configure shutdown behavior properly.

**For Raspberry Pi 5 and 4B**

These models support complete power-off after shutdown. The Fusion HAT monitors the 3.3V line to detect the Pi’s power state.

1. Place the jumper on **RPI State → Pi3V3**.

   .. image:: img/run_state.png

2. Edit the EEPROM configuration manually:

   .. code-block::

      sudo raspi-config

3. Navigate to: **Advanced Options → Shutdown Behaviour → B1 Full power off...**.

   .. image:: img/run_power_off.png

4. After saving, you will be prompted to reboot for changes to take effect.


**For Raspberry Pi Zero 2W, 3B, 3B+**

These models do **not** support full power-off using 3.3V. Instead, GPIO26 must be configured as a shutdown state indicator.

1. Place the jumper on **RPI_STATE → IO26**.

   .. image:: img/run_state.png

2. Edit the ``/boot/firmware/config.txt`` file:

   .. code-block::

      sudo nano /boot/firmware/config.txt

3. Add the following line at the end to set GPIO26 as low on shutdown and high on power-up:

   .. code-block::

      dtoverlay=gpio-poweroff,gpio_pin=26,active_low=1

4. Reboot to apply changes:

   .. code-block::

      sudo reboot



Download Code
---------------------------------

.. code-block:: 


   cd ~/
   git clone https://github.com/sunfounder/ai-explorer-lab-kit.git



.. _download_the_lib:

Download & Install the Library
----------------------------------

For this kit, all GPIO functionalities are managed through the Fusion HAT. Therefore, you need to use the accompanying ``fusion-hat`` library to access and control them.

Run the command in terminal to install ``fusion-hat`` module.

   .. raw:: html

      <run></run>

   .. code-block::

      cd ~/
      git clone https://github.com/sunfounder/fusion-hat.git
      cd fusion-hat
      sudo python3 setup.py install

.. note:: For the detail of fusion-hat, please refer to the |link_fusion_hat|.

.. _install_i2s:

Install ``i2samp.sh`` for the Speaker
------------------------------------------------------

The ``i2samp.sh`` is a sophisticated Bash script specifically designed for setting up and configuring an I2S (Inter-IC Sound) amplifier on Raspberry Pi and similar devices. Licensed under the MIT license, it ensures compatibility with a range of hardware and operating systems, conducting thorough checks before proceeding with any installation or configuration.

If you want your speaker to work properly, you definitely need to install this script. 

The steps are as follows:

.. code-block::

    cd ~/fusion-hat
    sudo bash i2samp.sh

输入多个Y来确认。
If there is no sound after restarting, you may need to run the ``i2samp.sh`` script several times.


Safe Shutdown
--------------

After the above configuration, you can safely shut down your PiCar-X using the power button.

**Soft Shutdown**

* Press and hold the power button for **2 seconds**.  
* The two power LEDs will flash rapidly.  
* Release the button → Fusion HAT triggers Raspberry Pi shutdown.  
* Once the Pi finishes shutting down, Fusion HAT cuts power automatically.  
* This protects your SD card and files.

**Hard Shutdown**

* If the system freezes or crashes, press and hold the power button for **5+ seconds**.  
* Fusion HAT will force power-off.  
* ⚠️ Warning: This may corrupt the SD card or system files. Use only when necessary.
