.. note::

    Hello, welcome to the SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasts Community on Facebook! Dive deeper into Raspberry Pi, Arduino, and ESP32 with fellow enthusiasts.

    **Why Join?**

    - **Expert Support**: Solve post-sale issues and technical challenges with help from our community and team.
    - **Learn & Share**: Exchange tips and tutorials to enhance your skills.
    - **Exclusive Previews**: Get early access to new product announcements and sneak peeks.
    - **Special Discounts**: Enjoy exclusive discounts on our newest products.
    - **Festive Promotions and Giveaways**: Take part in giveaways and holiday promotions.

    👉 Ready to explore and create with us? Click [|link_sf_facebook|] and join today!


.. _install_os_sd:

2. Installing the Operating System
===================================

Before using your Raspberry Pi, you need to install **Raspberry Pi OS** onto a microSD card.  
This guide explains how to do that using **Raspberry Pi Imager** in a simple, beginner-friendly way.

**Required Components**

* A computer (Windows, macOS, or Linux)
* A microSD card (16GB or larger; recommended brands: SanDisk, Samsung)
* A microSD card reader

-------------------

**1. Install Raspberry Pi Imager**


#. Visit the official Raspberry Pi Imager download page: |link_rpi_imager|. Download the correct installer for your operating system.

   .. image:: img/imager_download.png
      :width: 70%

#. Follow the installation prompts (language, install path, confirmation). After installation, launch **Raspberry Pi Imager** from your desktop or applications menu.

   .. image:: img/imager_install.png
      :width: 90%

-------------------

**2. Install the OS to the microSD Card**

#. Insert your microSD card into your computer using a card reader. Back up any important data before proceeding.

#. When Raspberry Pi Imager opens, you will see the **Device** page. Select your Raspberry Pi model from the list (e.g., Raspberry Pi 5, 4, 3, or Zero 2W).

   .. image:: img/imager_device.png
      :width: 90%

#. Go to the **OS** section and choose the recommended **Raspberry Pi OS (64-bit)** option.

   .. image:: img/imager_os.png
      :width: 90%

#. In the **Storage** section, select your microSD card. For safety, unplug other USB drives so only the SD card appears in the list.

   .. note::

      Be very careful when selecting the storage device.  
      Choosing the wrong drive may erase important data.

   .. image:: img/imager_storage.png
      :width: 90%

#. Click **Next** to continue to the customization step.

   .. note::

      * If you will connect a monitor, keyboard, and mouse directly to your Raspberry Pi, you may click **SKIP CUSTOMISATION**.  
      * If you plan to set up the Raspberry Pi *headless* (Wi-Fi remote access), you must complete the customization settings.

   .. image:: img/imager_custom_skip.png
      :width: 90%

-------------------

**3. OS Customization Settings**

#. **Set Hostname**

   * Give your Raspberry Pi a unique hostname.  
   * You can connect to it later using ``hostname.local``.

   .. image:: img/imager_custom_hostname.png
      :width: 90%

#. **Set Localisation**

   * Choose your country, language, and time zone.  
   * Make sure the **capital city** is correct—incorrect settings may cause Wi-Fi issues.
   
   .. image:: img/imager_custom_local.png
      :width: 90%

#. **Set Username & Password**

   Create the default user account for your Raspberry Pi.
   
   .. image:: img/imager_custom_user.png
      :width: 90%

#. **Configure Wi-Fi**

   * Enter your Wi-Fi **SSID** (network name) and **password**.  
   * Your Raspberry Pi will automatically connect on first boot.
   
   .. image:: img/imager_custom_wifi.png
      :width: 90%

#. **Enable SSH (Optional but Recommended)**

   * Enabling SSH allows you to remotely log in from your computer.  
   * You may log in using your username/password or configure SSH keys.
   
   .. image:: img/imager_custom_ssh.png
      :width: 90%

#. **Enable Raspberry Pi Connect (Optional)**


   Raspberry Pi Connect allows you to access your Raspberry Pi desktop from a web browser.
   
   * Turn on **Raspberry Pi Connect**, then click **OPEN RASPBERRY PI CONNECT**.
   
     .. image:: img/imager_custom_connect.png
        :width: 90%

   
   * Sign in with your Raspberry Pi ID and generate your authentication key.
   
     .. image:: img/imager_custom_authkey.png
        :width: 90%
   
   * The token will be automatically filled in.
   
     .. image:: img/imager_custom_connect_token.png
        :width: 90%

-------------------

**4. Write the OS Image**


#. Review all settings and click **WRITE**.

   .. image:: img/imager_writing.png
      :width: 90%

#. If the card already contains data, Raspberry Pi Imager will show a warning that all data on the device will be erased. Double-check that you selected the correct drive, then click **I UNDERSTAND, ERASE AND WRITE** to continue.

   .. image:: img/imager_erase.png
      :width: 90%

#. Wait for the writing and verification to finish. When it is done, Raspberry Pi Imager will show **Write complete!** and a summary of your choices. The storage device will be ejected automatically so you can remove it safely.


   .. image:: img/imager_finish.png
        :width: 90%

#. Remove the microSD card and insert it into the slot on the underside of your Raspberry Pi. Your Raspberry Pi is now ready to boot with the new OS!

   .. image:: img/os_sd_to_pi.jpg
        :width: 70%


