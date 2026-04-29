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

--------------------------------------------------

Wenn Sie keinen Bildschirm haben (Headless)
----------------------------------------------------

Ohne Monitor können Sie Ihren Raspberry Pi fernkonfigurieren und sich remote anmelden.  
Dies ist für die meisten Benutzer die bequemste Methode.

**Benötigte Komponenten**

* Raspberry Pi
* Offizielles Netzteil
* MicroSD-Karte
* Ein Computer im selben Netzwerk

**Hinweise**

* Stellen Sie sicher, dass sich Ihr Raspberry Pi und Ihr Computer im selben lokalen Netzwerk befinden.
* Verwenden Sie aus Gründen der besten Stabilität nach Möglichkeit eine Ethernet-Verbindung.

**Verbindung per SSH herstellen**

#. Öffnen Sie ein Terminal auf Ihrem Computer (Windows: **PowerShell**; macOS/Linux: **Terminal**) und verbinden Sie sich mit Ihrem Raspberry Pi:

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: Im Betriebssystem des AI Fusion Lab Kits lautet der Standardbenutzername ``pi`` und das Standardkennwort ``123456``. Der Standard-Hostname lautet ``ai-fusion``.

2. Alternativ können Sie die IP-Adresse Ihres Pi aus der DHCP-Liste Ihres Routers ermitteln und sich wie folgt verbinden:

   .. code-block:: bash

      ssh pi@<IP-Adresse>
      # Beispiel:
      ssh pi@192.168.1.42

3. Bei der ersten Anmeldung geben Sie ``yes`` ein, um das SSH-Zertifikat zu bestätigen.

4. Geben Sie das Kennwort ein, das Sie im Raspberry Pi Imager konfiguriert haben.  
   (Während der Eingabe wird nichts angezeigt – das ist normal.)

5. Nach der Anmeldung haben Sie vollen Zugriff auf die Befehlszeile.

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop