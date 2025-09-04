.. note:: 
 
    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook!  
    Tauchen Sie gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Nachkauf- und technische Probleme mit Unterstützung unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Kenntnisse zu erweitern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Vorab-Einblicken.
    - **Spezielle Rabatte**: Profitieren Sie von exklusiven Preisnachlässen auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und umzusetzen? Klicken Sie auf [|link_sf_facebook|] und treten Sie noch heute bei!

For Windows Users
=======================

Für Windows 10 oder höher können Sie sich per Remote-Login mit Ihrem Raspberry Pi verbinden. Gehen Sie dazu wie folgt vor:

#. Suchen Sie im Windows-Suchfeld nach ``powershell``. Klicken Sie mit der rechten Maustaste auf ``Windows PowerShell`` und wählen Sie **Als Administrator ausführen**.

    .. image:: img/powershell_ssh.png
        :align: center

#. Ermitteln Sie die IP-Adresse Ihres Raspberry Pi, indem Sie in PowerShell den Befehl ``ping -4 <hostname>.local`` eingeben.

    .. code-block::

        ping -4 raspberrypi.local

    .. image:: img/sp221221_145225.png
        :width: 550
        :align: center

    Sobald der Raspberry Pi mit dem Netzwerk verbunden ist, wird die IP-Adresse angezeigt.

    * Falls im Terminal die Meldung erscheint: ``Ping request could not find host pi.local. Please check the name and try again.``, überprüfen Sie den eingegebenen Hostnamen.
    * Sollte die IP-Adresse weiterhin nicht ermittelt werden können, prüfen Sie die Netzwerk- oder WLAN-Einstellungen des Raspberry Pi.

#. Sobald die IP-Adresse bestätigt ist, melden Sie sich am Raspberry Pi an mit: ``ssh <username>@<hostname>.local`` oder ``ssh <username>@<IP-Adresse>``.

    .. code-block::

        ssh pi@raspberrypi.local

    .. warning::

        Falls eine Fehlermeldung erscheint wie ``The term 'ssh' is not recognized as the name of a cmdlet...``, sind auf Ihrem System möglicherweise keine SSH-Tools vorinstalliert. In diesem Fall müssen Sie OpenSSH manuell gemäß :ref:`openssh_powershell` installieren oder ein Drittanbieter-Tool wie in :ref:`login_windows` beschrieben verwenden.

#. Beim ersten Login erscheint eine Sicherheitsmeldung. Geben Sie ``yes`` ein, um fortzufahren.

    .. code-block::

        The authenticity of host 'raspberrypi.local (2400:2410:2101:5800:635b:f0b6:2662:8cba)' can't be established.
        ED25519 key fingerprint is SHA256:oo7x3ZSgAo032wD1tE8eW0fFM/kmewIvRwkBys6XRwg.
        Are you sure you want to continue connecting (yes/no/[fingerprint])?

#. Geben Sie das zuvor festgelegte Passwort ein. Beachten Sie, dass die Passworteingabe aus Sicherheitsgründen nicht sichtbar ist.

    .. note::
        Dass beim Eingeben des Passworts keine Zeichen angezeigt werden, ist völlig normal. Achten Sie lediglich darauf, das korrekte Passwort einzugeben.

#. Nach erfolgreicher Anmeldung ist Ihr Raspberry Pi bereit für Remote-Operationen.

    .. image:: img/sp221221_140628.png
        :width: 550
        :align: center
