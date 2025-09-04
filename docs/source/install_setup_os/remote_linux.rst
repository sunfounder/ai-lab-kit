.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook!  
    Tauchen Sie gemeinsam mit anderen Technikfans tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Nachkauf- und Technikprobleme mit Unterstützung unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Fähigkeiten zu erweitern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Einblicken.
    - **Spezielle Rabatte**: Profitieren Sie von exklusiven Vergünstigungen auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu entwickeln? Klicken Sie auf [|link_sf_facebook|] und treten Sie noch heute bei!

For Linux/Unix Users
==========================

#. Öffnen Sie das **Terminal** auf Ihrem Linux/Unix-System.

#. Stellen Sie sicher, dass Ihr Raspberry Pi mit demselben Netzwerk verbunden ist. Überprüfen Sie dies mit dem Befehl `ping <hostname>.local`. Zum Beispiel:

    .. code-block::

        ping raspberrypi.local

    Wenn der Raspberry Pi verbunden ist, sollte dessen IP-Adresse angezeigt werden.

    * Erscheint im Terminal eine Meldung wie ``Ping request could not find host pi.local. Please check the name and try again.``, überprüfen Sie den eingegebenen Hostnamen.
    * Falls keine IP-Adresse angezeigt wird, kontrollieren Sie die Netzwerk- oder WLAN-Einstellungen Ihres Raspberry Pi.

#. Starten Sie eine SSH-Verbindung mit dem Befehl ``ssh <username>@<hostname>.local`` oder ``ssh <username>@<IP-Adresse>``. Zum Beispiel:

    .. code-block::

        ssh pi@raspberrypi.local

#. Beim ersten Login erscheint eine Sicherheitsmeldung. Geben Sie ``yes`` ein, um fortzufahren.

    .. code-block::

        The authenticity of host 'raspberrypi.local (2400:2410:2101:5800:635b:f0b6:2662:8cba)' can't be established.
        ED25519 key fingerprint is SHA256:oo7x3ZSgAo032wD1tE8eW0fFM/kmewIvRwkBys6XRwg.
        Are you sure you want to continue connecting (yes/no/[fingerprint])?

#. Geben Sie anschließend das zuvor festgelegte Passwort ein. Aus Sicherheitsgründen wird es beim Tippen nicht angezeigt.

    .. note::
        Es ist normal, dass das Passwort im Terminal nicht sichtbar ist. Achten Sie lediglich darauf, es korrekt einzugeben.

#. Nach erfolgreicher Anmeldung ist Ihr Raspberry Pi verbunden, und Sie können mit dem nächsten Schritt fortfahren.
