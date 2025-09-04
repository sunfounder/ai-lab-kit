.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _remote_desktop:

Remote Desktop 
=====================

Es gibt zwei Möglichkeiten, den Desktop des Raspberry Pi aus der Ferne zu steuern:

**VNC** und **XRDP** – du kannst beide nutzen.

VNC 
--------------

Mit VNC kannst du die Remote-Desktop-Funktion verwenden.

**Enable VNC service**

Der VNC-Dienst ist bereits im System installiert, jedoch standardmäßig deaktiviert. Du musst ihn in der Konfiguration aktivieren.

**Step 1**

Gib folgenden Befehl ein:

.. raw:: html

    <run></run>

.. code-block:: 

    sudo raspi-config

.. image:: img/image287.png
   :align: center

**Step 2**

Wähle mit den Pfeiltasten **3 Interfacing Options** und bestätige mit **Enter**.

.. image:: img/image282.png
   :align: center

**Step 3**

**P3 VNC**

.. image:: img/image288.png
   :align: center

**Step 4**

Wähle **Yes -> OK -> Finish**, um die Konfiguration zu beenden.

.. image:: img/image289.png
   :align: center

**Login to VNC**

**Step 1**

Lade den `VNC Viewer <https://www.realvnc.com/en/connect/download/viewer/>`_ auf deinen Computer herunter und installiere ihn. Öffne das Programm nach der Installation.

**Step 2**

Wähle „ **New connection** “.

.. image:: img/image290.png
   :align: center

**Step 3**

Gib die IP-Adresse des Raspberry Pi und einen beliebigen **Name** ein.

.. image:: img/image291.png
   :align: center

**Step 4**

Doppelklicke auf die eben erstellte **connection**:

.. image:: img/image292.png
   :align: center

**Step 5**

Gib den Benutzernamen (**pi**) und das Passwort (**raspberry** als Standard) ein.

.. image:: img/image293.png
   :align: center

**Step 6**

Nun siehst du den Desktop des Raspberry Pi:

.. image:: img/image294.png
   :align: center

Damit ist der VNC-Teil abgeschlossen.


XRDP
-----------------------

Eine weitere Möglichkeit für den Remote-Desktop ist XRDP. Es bietet über das RDP-Protokoll (Microsoft Remote Desktop Protocol) eine grafische Anmeldung auf entfernten Rechnern.

**Install XRDP**

**Step 1**

Melde dich per SSH beim Raspberry Pi an.

**Step 2**

Führe die folgenden Befehle zur Installation von XRDP aus:

.. raw:: html

    <run></run>

.. code-block:: 

   sudo apt-get update
   sudo apt-get install xrdp

**Step 3**

Die Installation startet. Bestätige mit „Y“ und drücke Enter.

.. image:: img/image295.png
   :align: center

**Step 4**

Nach Abschluss der Installation kannst du dich mit den Windows-Remote-Desktop-Tools beim Raspberry Pi anmelden.

**Login to XRDP**

**Step 1**

Unter Windows kannst du die integrierte Remote-Desktop-Funktion nutzen. Mac-Nutzer können „Microsoft Remote Desktop“ aus dem App Store herunterladen – der Ablauf ist nahezu identisch. Im folgenden Beispiel wird die Windows-Variante gezeigt.

**Step 2**

Tippe „ **mstsc** “ im Ausführen-Dialog (WIN+R) ein, öffne die Remote-Desktop-Verbindung und gib die IP-Adresse des Raspberry Pi ein. Klicke anschließend auf „Connect“.

.. image:: img/image296.png
   :align: center

**Step 3**

Es erscheint die xrdp-Anmeldemaske. Gib deinen Benutzernamen und dein Passwort ein und klicke auf „OK“. Beim ersten Login lautet der Benutzername „pi“ und das Passwort „raspberry“.

.. image:: img/image297.png
   :align: center

**Step 4**

Nun bist du erfolgreich per Remote-Desktop mit dem Raspberry Pi verbunden.

.. image:: img/image20.png
   :align: center

**Copyright Notice**

Alle Inhalte, einschließlich, aber nicht beschränkt auf Texte, Bilder und Code in diesem Handbuch, sind Eigentum der Firma SunFounder. Sie dürfen ausschließlich für persönliche Studien, Recherchen, zum Lernen oder andere nichtkommerzielle und gemeinnützige Zwecke gemäß den geltenden Vorschriften und Urheberrechtsgesetzen genutzt werden, ohne die Rechte des Autors oder anderer Rechtsinhaber zu verletzen. Jede Nutzung für kommerzielle Zwecke ohne Genehmigung behält sich die Firma vor, rechtlich zu verfolgen.
