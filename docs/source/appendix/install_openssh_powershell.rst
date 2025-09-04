.. _openssh_powershell:

Install OpenSSH via Powershell
-----------------------------------

Wenn du versuchst, dich mit ``ssh <username>@<hostname>.local`` (oder ``ssh <username>@<IP address>``) mit deinem Raspberry Pi zu verbinden, aber die folgende Fehlermeldung erscheint:

    .. code-block::

        ssh: The term 'ssh' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the
        spelling of the name, or if a path was included, verify that the path is correct and try again.


bedeutet das, dass dein Computersystem zu alt ist und `OpenSSH <https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui>`_ nicht vorinstalliert wurde. In diesem Fall musst du es manuell gemäß der folgenden Anleitung installieren.

#. Gib ``powershell`` in das Suchfeld deines Windows-Desktops ein, klicke mit der rechten Maustaste auf ``Windows PowerShell`` und wähle im angezeigten Menü ``Run as administrator`` .

    .. image:: img/powershell_ssh.png
        :align: center

#. Verwende den folgenden Befehl, um ``OpenSSH.Client`` zu installieren:

    .. code-block::

        Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

#. Nach der Installation wird die folgende Ausgabe angezeigt:

    .. code-block::

        Path          :
        Online        : True
        RestartNeeded : False

#. Überprüfe die Installation mit folgendem Befehl:

    .. code-block::

        Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'

#. Nun wird dir angezeigt, dass ``OpenSSH.Client`` erfolgreich installiert wurde:

    .. code-block::

        Name  : OpenSSH.Client~~~~0.0.1.0
        State : Installed

        Name  : OpenSSH.Server~~~~0.0.1.0
        State : NotPresent

    .. warning:: 
        Wenn die obige Meldung nicht erscheint, bedeutet das, dass dein Windows-System weiterhin zu alt ist. In diesem Fall empfiehlt es sich, ein Drittanbieter-SSH-Tool zu installieren, wie z. B. :ref:`login_windows`.

#. Starte PowerShell neu und führe es erneut als Administrator aus. Ab diesem Zeitpunkt kannst du dich mit dem Befehl ``ssh`` bei deinem Raspberry Pi anmelden. Dabei wirst du aufgefordert, das zuvor vergebene Passwort einzugeben.

    .. image:: img/powershell_login.png