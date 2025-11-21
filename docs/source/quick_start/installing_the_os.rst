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

2. Installing the OS
============================================================

To get your Raspberry Pi ready, you first need to install the Raspberry Pi OS onto a Micro SD card.  
This section will guide you through the process step by step.

**Required Components**

* A Personal Computer (Windows, macOS, or Linux)
* A Micro SD card (≥16GB, reliable brand such as Sandisk or Samsung)
* A Micro SD card Reader

----

**1. Install Raspberry Pi Imager**

#. Open the official Raspberry Pi download page: |link_rpi_imager|.  

   Download the correct version for your operating system (Windows, macOS, or Ubuntu).  

   .. image:: img/os_install_imager.png
       :align: center

#. After installation, launch Raspberry Pi Imager by clicking the desktop icon or searching for ``Raspberry Pi Imager`` in your system’s menu.  

   .. image:: img/os_open_imager.png
       :align: center

**2. Install OS to Micro SD Card**

#. Insert your Micro SD card into your computer using a card reader. Make sure the card is empty or that you have backed up any important data.

#. In Imager, first click **Choose Device** and select your Raspberry Pi model. (e.g., Raspberry Pi 5, Raspberry Pi 4, 3 or Zero 2W).  

   .. image:: img/os_choose_device.png
       :align: center

#. Next, click **Choose OS** and select the recommended **Raspberry Pi OS (64-bit)** option.

   .. image:: img/os_choose_os.png
       :align: center

#. Click **Choose Storage** and select your Micro SD card. To avoid mistakes, unplug other USB drives so only the SD card is listed.

   .. note::

      Be very careful when selecting the storage device. Choosing the wrong disk could erase important data.

   .. image:: img/os_choose_sd.png
       :align: center

#. Click **Next**, then choose **EDIT SETTINGS** to configure your Raspberry Pi before writing.  

   .. note::

      If you plan to use a monitor, keyboard, and mouse directly with your Raspberry Pi, you can skip advanced settings and just click **Yes** to start writing. 
      However, if you want to use headless setup (remote connection via Wi-Fi), you must complete the following settings.

   .. image:: img/os_enter_setting.png
       :align: center

----

**3. OS Customization Settings**

* **Set Hostname**:  

  * Choose a unique name for your Pi.  
  * You can later access it in the network as ``<hostname>.local``.  

  .. image:: img/os_set_hostname.png
      :align: center

* **Set Username & Password**: 

  * Create a secure login for your Pi.  
  * Unlike older OS versions, Raspberry Pi no longer provides a default account.

  .. image:: img/os_set_username.png
      :align: center

* **Configure Wi-Fi**:

  * Enter your Wi-Fi **SSID** (network name) and **Password**.  
  * Set the correct **Wireless LAN country** using the |link_iso_code| (e.g., US, UK, CN); otherwise Wi-Fi will not work.

  .. image:: img/os_set_wifi.png
      :align: center

* **Enable SSH (Optional but Recommended)**: 

  This allows remote access from your PC. You can log in using the username/password, or set up public-key authentication.  

  .. image:: img/os_enable_ssh.png
      :align: center

* **Other Options**:  
  
  You may enable "Play sound when finished" or "Eject media when finished" for convenience.  

  .. image:: img/os_options.png
      :align: center

----

**4. Write the OS Image**

#. After customizing, click **Save**, then **Yes** to apply settings.  

   .. image:: img/os_click_yes.png
       :align: center

#. If your card has existing data, confirm by clicking **Yes** to overwrite.  

   .. image:: img/os_continue.png
       :align: center

#. Wait until the writing and verification process is complete. This may take several minutes. Once finished, you will see **Write Successful**.  

   .. image:: img/os_finish.png
       :align: center


#. Finally, remove the SD card from the reader and insert it into the slot on the underside of your Raspberry Pi. Your Raspberry Pi is now ready to boot with the new OS installed!

   .. image:: img/os_sd_to_pi.jpg
      :width: 500
      :align: center

