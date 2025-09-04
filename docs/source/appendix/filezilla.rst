.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _filezilla:

Filezilla Software
==========================

.. image:: img/filezilla_icon.png

Das File Transfer Protocol (FTP) ist ein standardisiertes Kommunikationsprotokoll, das zum Übertragen von Dateien von einem Server zu einem Client in einem Computernetzwerk verwendet wird.

Filezilla ist eine Open-Source-Software, die nicht nur FTP, sondern auch FTP über TLS (FTPS) und SFTP unterstützt. Mit Filezilla können wir lokale Dateien (wie Bilder, Audiodateien usw.) auf den Raspberry Pi hochladen oder Dateien vom Raspberry Pi auf den lokalen Rechner herunterladen.

**Step 1**: Download Filezilla.

Lade den Client von der `Filezilla’s official website <https://filezilla-project.org/>`_ herunter. Filezilla bietet außerdem eine sehr gute Dokumentation, siehe: `Documentation - Filezilla <https://wiki.filezilla-project.org/Documentation>`_.

**Step 2**: Connect to Raspberry Pi

Nach der schnellen Installation öffne das Programm und `connect it to an FTP server <https://wiki.filezilla-project.org/Using#Connecting_to_an_FTP_server>`_. Es gibt drei Möglichkeiten, eine Verbindung herzustellen – hier nutzen wir die **Quick Connect**-Leiste. Gib **Hostname/IP**, **Benutzername**, **Passwort** und **Port (22)** ein und klicke anschließend auf **Quick Connect** oder drücke **Enter**, um die Verbindung zum Server herzustellen.

.. image:: img/filezilla_connect.png

.. note::

    Quick Connect ist eine gute Möglichkeit, deine Zugangsdaten zu testen. Wenn du einen dauerhaften Eintrag anlegen möchtest, kannst du nach einer erfolgreichen Quick-Connect-Verbindung **File** -> **Copy Current Connection to Site Manager** auswählen, einen Namen vergeben und auf **OK** klicken. Beim nächsten Mal kannst du dann über **File** -> **Site Manager** die gespeicherte Verbindung auswählen.

    .. image:: img/ftp_site.png

**Step 3**: Upload/download files.

Du kannst lokale Dateien auf den Raspberry Pi hochladen, indem du sie einfach per Drag & Drop hineinziehst, oder Dateien vom Raspberry Pi auf deinen lokalen Rechner herunterladen.

.. image:: img/upload_ftp.png
