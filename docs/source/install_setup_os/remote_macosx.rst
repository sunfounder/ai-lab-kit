.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook!  
    Tauchen Sie gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Experten-Support**: Lösen Sie Nachkauf- und Technikprobleme mit Unterstützung unserer Community und unseres Teams.
    - **Lernen & Teilen**: Tauschen Sie Tipps und Tutorials aus, um Ihre Kenntnisse zu erweitern.
    - **Exklusive Vorschauen**: Erhalten Sie frühzeitigen Zugang zu neuen Produktankündigungen und Vorab-Einblicken.
    - **Spezielle Rabatte**: Profitieren Sie von exklusiven Preisnachlässen auf unsere neuesten Produkte.
    - **Festliche Aktionen und Gewinnspiele**: Nehmen Sie an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und umzusetzen? Klicken Sie auf [|link_sf_facebook|] und treten Sie noch heute bei!

For Mac OS X Users
==========================

Für Mac OS X-Nutzer bietet SSH (Secure Shell) eine sichere und komfortable Möglichkeit, auf einen Raspberry Pi aus der Ferne zuzugreifen und ihn zu steuern. Dies ist besonders praktisch, wenn Sie mit dem Raspberry Pi arbeiten möchten, ohne dass ein Monitor angeschlossen ist. Über die Terminal-Anwendung auf dem Mac können Sie eine sichere Verbindung herstellen. Der Vorgang erfolgt über einen SSH-Befehl, der den Benutzernamen und Hostnamen des Raspberry Pi enthält. Bei der ersten Verbindung erscheint eine Sicherheitsabfrage, um die Authentizität des Raspberry Pi zu bestätigen.

#. Melden Sie sich mit folgendem Befehl am Raspberry Pi an: ``ssh <username>@<hostname>.local`` oder ``ssh <username>@<IP-Adresse>``.

    .. code-block::

        ssh pi@raspberrypi.local

    .. image:: img/mac_vnc14.png

#. Beim ersten Login erscheint eine Sicherheitsmeldung. Geben Sie **yes** ein, um fortzufahren.

    .. code-block::

        The authenticity of host 'raspberrypi.local (2400:2410:2101:5800:635b:f0b6:2662:8cba)' can't be established.
        ED25519 key fingerprint is SHA256:oo7x3ZSgAo032wD1tE8eW0fFM/kmewIvRwkBys6XRwg.
        Are you sure you want to continue connecting (yes/no/[fingerprint])?

#. Geben Sie das Passwort für den Raspberry Pi ein. Beachten Sie, dass das Passwort beim Tippen nicht angezeigt wird – dies ist ein übliches Sicherheitsmerkmal.

    .. code-block::

        pi@raspberrypi.local's password: 
        Linux raspberrypi 5.15.61-v8+ #1579 SMP PREEMPT Fri Aug 26 11:16:44 BST 2022 aarch64

        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.

        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Thu Sep 22 12:18:22 2022
        pi@raspberrypi:~ $ 

