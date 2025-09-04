.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook!  
    Entdecken Sie gemeinsam mit anderen Technikbegeisterten die Welt von Raspberry Pi, Arduino und ESP32 noch intensiver.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Anleitungen aus, um Ihre Kenntnisse zu erweitern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und ersten Einblicken.
    - **Spezielle Rabatte**: Profitieren Sie von exklusiven Preisnachlässen auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicken Sie auf [|link_sf_facebook|] und treten Sie noch heute bei!

.. _install_os:

Installing the OS
=======================

**Benötigte Komponenten**

* Raspberry Pi 5B
* Ein Personal Computer
* Eine Micro-SD-Karte

**Installationsschritte**

#. Besuchen Sie die Raspberry Pi Software-Downloadseite unter `Raspberry Pi Imager <https://www.raspberrypi.org/software/>`_.  
   Wählen Sie die Imager-Version, die mit Ihrem Betriebssystem kompatibel ist. Laden Sie die Datei herunter und öffnen Sie sie, um die Installation zu starten.

    .. image:: img/os_install_imager.png

#. Während der Installation kann je nach Betriebssystem eine Sicherheitsabfrage erscheinen.  
   Unter Windows wird beispielsweise eine Warnmeldung angezeigt. Wählen Sie in diesem Fall **Weitere Informationen** und anschließend **Trotzdem ausführen**.  
   Folgen Sie den Anweisungen auf dem Bildschirm, um die Installation des Raspberry Pi Imagers abzuschließen.

    .. image:: img/os_info.png

#. Stecken Sie Ihre SD-Karte in den SD-Kartensteckplatz Ihres Computers oder Laptops.

#. Starten Sie die Raspberry Pi Imager-Anwendung, indem Sie auf das Symbol klicken oder ``rpi-imager`` im Terminal eingeben.

    .. image:: img/os_open_imager.png

#. Klicken Sie auf **CHOOSE DEVICE** und wählen Sie Ihr spezifisches Raspberry-Pi-Modell (z. B. Raspberry Pi Zero 2 W) aus der Liste.

    .. image:: img/os_choose_device.png

#. Klicken Sie anschließend auf **Choose OS** und wählen Sie ein Betriebssystem für die Installation.

    .. image:: img/os_choose_os.png

#. Klicken Sie auf **Choose Storage** und wählen Sie das passende Speichermedium für die Installation.

    .. note::

        Achten Sie darauf, das richtige Speichermedium auszuwählen. Um Verwechslungen zu vermeiden, entfernen Sie zusätzliche Speichermedien, falls mehrere angeschlossen sind.

    .. image:: img/os_choose_sd.png

#. Klicken Sie auf **NEXT** und dann auf **EDIT SETTINGS**, um Ihre OS-Einstellungen anzupassen.  
   Falls Sie einen Monitor am Raspberry Pi angeschlossen haben, können Sie die nächsten Schritte überspringen und auf „Yes“ klicken, um die Installation sofort zu starten. Weitere Einstellungen können Sie später direkt am Monitor vornehmen.

    .. image:: img/os_enter_setting.png

#. Legen Sie einen **Hostname** für Ihren Raspberry Pi fest.

    .. note::

        Der Hostname ist der Netzwerkname Ihres Raspberry Pi. Sie können Ihren Pi über ``<hostname>.local`` oder ``<hostname>.lan`` erreichen.

    .. image:: img/os_set_hostname.png

#. Erstellen Sie einen **Benutzernamen** und ein **Passwort** für das Administratorkonto des Raspberry Pi.

    .. note::

        Ein eigener Benutzername und ein sicheres Passwort sind entscheidend, um Ihren Raspberry Pi zu schützen, da er kein voreingestelltes Passwort besitzt.

    .. image:: img/os_set_username.png

#. Konfigurieren Sie das drahtlose LAN, indem Sie die **SSID** und das **Passwort** Ihres Netzwerks angeben.

    .. note::

        Stellen Sie das Feld ``Wireless LAN country`` auf den zweistelligen `ISO/IEC alpha2 code <https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements>`_ Ihres Landes ein.

    .. image:: img/os_set_wifi.png

#. Klicken Sie auf **SERVICES** und aktivieren Sie **SSH**, um sicheren, passwortgeschützten Fernzugriff zu ermöglichen. Speichern Sie anschließend Ihre Einstellungen.

    .. image:: img/os_enable_ssh.png

#. Bestätigen Sie Ihre gewählten Einstellungen mit **Yes**.

    .. image:: img/os_click_yes.png

#. Falls sich bereits Daten auf der SD-Karte befinden, sichern Sie diese unbedingt, um Datenverlust zu vermeiden.  
   Klicken Sie auf **Yes**, wenn keine Sicherung erforderlich ist.

    .. image:: img/os_continue.png

#. Die Installation des Betriebssystems auf der SD-Karte wird gestartet. Nach Abschluss erscheint ein Bestätigungsdialog.

    .. image:: img/os_finish.png
        :align: center
