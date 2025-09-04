.. note:: 

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Sichere dir exklusive Rabatte auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Mach mit bei Gewinnspielen und saisonalen Aktionen.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _audio_configuration:

Audio Configuration
=========================

.. _change_audio_output:

Change Audio Output
----------------------------

Wenn dein Lautsprecher keinen Ton wiedergibt, liegt es möglicherweise daran, dass der Raspberry Pi die falsche Audioausgabe gewählt hat. Die richtige Auswahl sollte **Headphones** sein. Du kannst die Audioausgabe folgendermaßen ändern:


Gib den folgenden Befehl ein.

.. raw:: html

   <run></run>

.. code-block:: 

    sudo raspi-config

Wähle **1 System Options**.

.. image:: img/audio1.jpg

Dann **S2 Audio**.

.. image:: img/audio2.jpg

Nachdem du **1 Headphones** ausgewählt hast, drücke ``Enter`` zur Bestätigung und wähle anschließend ``Finish``, um zu beenden.

.. image:: img/audio3.jpg

.. _adjust_volume:

Adjust Volume 
---------------

Wenn dir die Lautstärke der Lautsprecher zu niedrig erscheint, kannst du sie mit folgendem Befehl anpassen:

.. raw:: html

   <run></run>

.. code-block:: 

    alsamixer

.. image:: img/faq1.png

Die Standardansicht wird unten angezeigt.

.. image:: img/faq2.png

Drücke ``F6``, um den Modus **Headphones** auszuwählen.

.. image:: img/faq3.png

Verwende anschließend die Pfeiltasten nach oben und unten, um die Lautstärke einzustellen, und drücke ``ESC``, um zu beenden.

.. image:: img/faq4.png