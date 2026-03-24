.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _setup_pi_fusion_kit:

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi
   :end-before: end_setup_pi

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_screen
   :end-before: end_setup_pi_screen

.. .. include:: /_shared/pi_start/set_up_pi.rst
..    :start-after: start_setup_pi_headless
..    :end-before: end_setup_pi_headless

----------------------------------
If You Have No Screen (Headless)
----------------------------------

Without a monitor, you can configure and log in to your Raspberry Pi remotely.  
This is the most convenient method for most users.

**Required Components**

* Raspberry Pi
* Official Power Supply
* MicroSD Card
* A computer on the same network

**Tips**

* Ensure that your Raspberry Pi and your computer are on the same local network.
* For best stability, use Ethernet if available.


**Connect via SSH**

#. Open a terminal on your computer (Windows: **PowerShell**; macOS/Linux: **Terminal**) and connect to your Raspberry Pi: 

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: In the AI ​​Fusion Lab Kit operating system, the default username is ``pi`` and the password is ``123456``. The default hostname is ``ai-fusion.local``.


2. Alternatively, locate your Pi’s IP address from your router’s DHCP list and connect with:

   .. code-block:: bash

      ssh pi@<IP address>
      # Example:
      ssh pi@192.168.1.42

3. On first login, type ``yes`` to confirm the SSH certificate.

4. Enter the password you configured in Raspberry Pi Imager.  
   (Nothing appears while typing—this is normal.)

5. After login, you now have full command-line access.

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center



.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop
