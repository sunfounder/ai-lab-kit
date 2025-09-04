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

.. _remote_desktop:

Remote Desktop Access for Raspberry Pi
==================================================

Für Anwender, die eine grafische Benutzeroberfläche (GUI) der Kommandozeile vorziehen, unterstützt der Raspberry Pi den Fernzugriff über Remote Desktop.  
In dieser Anleitung erfahren Sie, wie Sie VNC (Virtual Network Computing) einrichten und verwenden, um Ihren Raspberry Pi aus der Ferne zu steuern.

Wir empfehlen hierfür die Nutzung von `VNC® Viewer <https://www.realvnc.com/en/connect/download/viewer/>`_.

**VNC-Dienst auf dem Raspberry Pi aktivieren**

Der VNC-Dienst ist in Raspberry Pi OS bereits vorinstalliert, aber standardmäßig deaktiviert.  
Gehen Sie wie folgt vor, um ihn zu aktivieren:

#. Geben Sie im Terminal des Raspberry Pi den folgenden Befehl ein:

    .. raw:: html

        <run></run>

    .. code-block:: 

        sudo raspi-config

#. Navigieren Sie mit der Pfeiltaste nach unten zu **Interfacing Options** und drücken Sie **Enter**.

    .. image:: img/config_interface.png
        :align: center

#. Wählen Sie **VNC** aus den Optionen.

    .. image:: img/vnc.png
        :align: center

#. Verwenden Sie die Pfeiltasten, um **<Yes>** -> **<OK>** -> **<Finish>** auszuwählen und die Aktivierung des VNC-Dienstes abzuschließen.

    .. image:: img/vnc_yes.png
        :align: center

**Anmeldung über VNC Viewer**

#. Laden Sie den `VNC Viewer <https://www.realvnc.com/en/connect/download/viewer/>`_ auf Ihren Computer herunter und installieren Sie ihn.

#. Starten Sie anschließend den VNC Viewer. Geben Sie den Hostnamen oder die IP-Adresse Ihres Raspberry Pi ein und drücken Sie Enter.

    .. image:: img/vnc_viewer1.png
        :align: center

#. Geben Sie bei Aufforderung den Benutzernamen und das Passwort Ihres Raspberry Pi ein und klicken Sie auf **OK**.

    .. image:: img/vnc_viewer2.png
        :align: center

#. Nun haben Sie Zugriff auf die Desktop-Oberfläche Ihres Raspberry Pi.

    .. image:: img/bullseye_desktop.png
        :align: center
