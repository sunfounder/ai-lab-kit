.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _login_windows:

PuTTY
=========================

Wenn du Windows verwendest, kannst du verschiedene SSH-Anwendungen nutzen. Hier empfehlen wir `PuTTY <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.

**Step 1**

Lade PuTTY herunter.

**Step 2**

Öffne PuTTY und klicke in der linken Baumstruktur auf **Session**. Gib die IP-Adresse des RPi in das Textfeld unter **Host Name (or IP address)** ein und trage unter **Port** die Zahl **22** ein (Standardwert ist 22).

.. image:: img/image25.png
    :align: center

**Step 3**

Klicke auf **Open**. Beim ersten Login auf den Raspberry Pi über die IP-Adresse erscheint eine Sicherheitsabfrage – klicke einfach auf **Yes**.

**Step 4**

Wenn im PuTTY-Fenster die Eingabeaufforderung „ **login as:** “ erscheint, gib „ **pi** “ (den Benutzernamen des RPi) ein und als  **password** „raspberry“ (Standardpasswort, sofern du es nicht geändert hast).

.. note::

    Bei der Passworteingabe werden keine Zeichen angezeigt – das ist normal. Wichtig ist nur, dass du das korrekte Passwort eingibst.
    
    Falls neben PuTTY „inactive“ erscheint, bedeutet das, dass die Verbindung getrennt wurde und neu aufgebaut werden muss.
    
.. image:: img/image26.png
    :align: center

**Step 5**

Nun ist der Raspberry Pi verbunden, und du kannst mit den nächsten Schritten fortfahren.