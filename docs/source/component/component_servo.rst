.. note::

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse nach dem Kauf auftretende Probleme und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Tutorials, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitig Zugang zu neuen Produktankündigungen und exklusiven Vorschauen.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu erschaffen? Klicke [|link_sf_facebook|] und tritt noch heute bei!

.. _cpn_servo:

Servo
===========

.. image:: img/servo.png
    :align: center

Ein Servo besteht im Wesentlichen aus folgenden Komponenten: Gehäuse, Welle, Getriebesystem, Potentiometer, Gleichstrommotor und einer eingebetteten Steuerplatine.  

Die Funktionsweise ist wie folgt: Der Mikrocontroller sendet PWM-Signale an das Servo. Diese werden von der Steuerplatine im Inneren über den Signaleingang empfangen, die daraufhin den Motor ansteuert. Der Motor treibt das Getriebe an, das wiederum die Welle nach einer Untersetzung bewegt. Welle und Potentiometer sind gekoppelt: Dreht sich die Welle, verändert sich die Stellung des Potentiometers, welches ein Spannungssignal an die Steuerplatine zurückgibt. Die Platine ermittelt damit Richtung und Geschwindigkeit der Drehung, sodass das Servo präzise an der vorgegebenen Position stoppt und diese zuverlässig hält.

.. image:: img/servo_internal.png
    :align: center

Der Drehwinkel wird durch die Dauer des Impulses bestimmt, der am Steuerdraht anliegt – dieses Verfahren wird als Pulsweitenmodulation (PWM) bezeichnet. Das Servo erwartet alle 20 ms einen Impuls. Die Impulsbreite bestimmt die Drehstellung des Motors. Ein Impuls von 1,5 ms positioniert die Welle beispielsweise in die Neutralstellung von 90°.  
Liegt die Impulsdauer unter 1,5 ms, dreht die Welle um einen bestimmten Winkel gegen den Uhrzeigersinn aus der Neutralstellung heraus. Bei Impulsdauern über 1,5 ms erfolgt die Bewegung im Uhrzeigersinn. Die minimale und maximale Impulsbreite, die eine gültige Position ansteuern, sind je nach Servomodell unterschiedlich. In der Regel liegt die minimale Impulsbreite bei etwa 0,5 ms und die maximale bei 2,5 ms.

.. image:: img/servo_duty.png
    :width: 600
    :align: center
