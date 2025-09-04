.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiast Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Fähigkeiten zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_joystick:

Joystick-Modul
=======================

.. image:: img/joystick_pic.png
    :align: center
    :width: 600

Die Grundidee eines Joysticks besteht darin, die Bewegung eines Steuerknüppels in elektronische Signale umzuwandeln, die von einem Computer verarbeitet werden können.  

Um dem Computer den gesamten Bewegungsbereich zu übermitteln, muss ein Joystick die Position des Sticks auf zwei Achsen erfassen – der X-Achse (links nach rechts) und der Y-Achse (auf und ab). Genau wie in der Geometrie lässt sich so die Position des Sticks durch die X-Y-Koordinaten exakt bestimmen.  

Zur Ermittlung der Position überwacht das Joystick-Steuersystem einfach die Stellung jeder Achse. Klassische analoge Joysticks nutzen dafür zwei Potentiometer, also veränderbare Widerstände.  

Zusätzlich verfügt der Joystick über einen digitalen Eingang, der aktiviert wird, wenn der Stick nach unten gedrückt wird.  

.. image:: img/joystick318.png
    :align: center
    :width: 600

