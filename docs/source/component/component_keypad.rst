.. note:: 

    Hallo, willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Warum beitreten?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Tausche Tipps und Tutorials aus, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Gewinnspielen und saisonalen Aktionen teil.

    👉 Bereit, mit uns Neues zu entdecken und zu entwickeln? Klicke [|link_sf_facebook|] und trete noch heute bei!

.. _cpn_keypad:

Keypad
========================

Ein Keypad ist ein rechteckiges Tastenfeld mit 12 oder 16 OFF-(ON)-Tasten.  
Die Kontakte sind über eine Stiftleiste zugänglich, die sich für den Anschluss eines Flachbandkabels oder zum Einsetzen in eine Leiterplatte eignet.  
Bei manchen Keypads ist jede Taste mit einem separaten Kontakt in der Stiftleiste verbunden, während alle Tasten eine gemeinsame Masse teilen.  

.. image:: img/keypad314.png

Häufiger jedoch sind die Tasten in einer Matrix verschaltet, was bedeutet, dass jede Taste ein einzigartiges Leiterpaar in der Matrix überbrückt.  
Diese Konfiguration eignet sich ideal für das Abfragen durch einen Mikrocontroller, der so programmiert werden kann, dass er nacheinander Impulse an jede der vier horizontalen Leitungen sendet.  
Während jedes Impulses überprüft der Mikrocontroller die verbleibenden vier vertikalen Leitungen, um festzustellen, welche – falls überhaupt – ein Signal führt.  
Um unvorhersehbares Verhalten der Eingänge bei fehlendem Signal zu vermeiden, sollten Pull-up- oder Pull-down-Widerstände an die Eingangsleitungen angeschlossen werden.  
