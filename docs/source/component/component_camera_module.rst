.. note::

    Hallo und willkommen in der SunFounder Raspberry Pi & Arduino & ESP32 Enthusiasten-Community auf Facebook! Tauche gemeinsam mit anderen Technikbegeisterten tiefer in die Welt von Raspberry Pi, Arduino und ESP32 ein.

    **Why Join?**

    - **Expert Support**: Löse Probleme nach dem Kauf und technische Herausforderungen mit Unterstützung unserer Community und unseres Teams.
    - **Learn & Share**: Teile Tipps und Anleitungen, um deine Kenntnisse zu erweitern.
    - **Exclusive Previews**: Erhalte frühzeitigen Zugang zu neuen Produktankündigungen und exklusiven Einblicken.
    - **Special Discounts**: Profitiere von exklusiven Rabatten auf unsere neuesten Produkte.
    - **Festive Promotions and Giveaways**: Nimm an Verlosungen und saisonalen Aktionen teil.

    👉 Bereit, mit uns zu entdecken und Neues zu erschaffen? Klicke auf [|link_sf_facebook|] und werde noch heute Mitglied!

.. _cpn_camera_module:

Camera Module
====================================


**Description**

.. image:: img/camera_module_pic.png
   :width: 200
   :align: center

Dies ist ein 5-Megapixel-Raspberry-Pi-Kameramodul mit einem OV5647-Sensor. Es ist sofort einsatzbereit („Plug and Play“): Verbinde einfach das beiliegende Flachbandkabel mit dem CSI-Port (Camera Serial Interface) deines Raspberry Pi – und schon kann es losgehen.  

Das Board ist sehr kompakt – etwa 25 mm x 23 mm x 9 mm groß – und wiegt lediglich 3 g. Damit eignet es sich ideal für mobile Anwendungen oder Projekte, bei denen Größe und Gewicht entscheidend sind. Das Kameramodul besitzt eine native Auflösung von 5 Megapixeln und eine fest eingebaute Linse. Es kann Standbilder mit 2592 × 1944 Pixeln aufnehmen und unterstützt zudem Videoformate wie 1080p30, 720p60 und 640×480p90.  

.. note:: 

   Das Modul kann ausschließlich Bilder und Videos aufnehmen, jedoch keine Audiodaten.



**Specification**

* **Static Images Resolution**: 2592×1944 
* **Supported Video Resolution**: 1080p/30 fps, 720p/60 fps und 640×480p 60/90 Videoaufnahme 
* **Aperture (F)**: 1.8 
* **Visual Angle**: 65 Grad 
* **Dimension**: 24 mm × 23.5 mm × 8 mm 
* **Weight**: 3 g 
* **Interface**: CSI-Anschluss 
* **Supported OS**: Raspberry Pi OS (neueste Version empfohlen) 



Assemble the Camera Module
-------------------------------------


Am Kameramodul oder Raspberry Pi findest du einen flachen Kunststoffstecker. Ziehe vorsichtig den schwarzen Fixierriegel heraus, bis er teilweise gelöst ist. Führe dann das FFC-Kabel wie gezeigt in den Stecker ein und schiebe den Riegel wieder zurück.  

Wenn das FFC-Kabel korrekt eingesetzt ist, sitzt es gerade und lässt sich bei leichtem Ziehen nicht herauslösen. Ist das nicht der Fall, wiederhole den Vorgang.  


.. image:: img/connect_ffc.png
.. image:: img/1.10_camera.png
   :width: 700

.. warning::

   Installiere die Kamera niemals bei eingeschalteter Stromversorgung – dies kann das Modul dauerhaft beschädigen.

.. _enable_camera:

Enable the Camera Interface
---------------------------------------

Führe den folgenden Befehl aus, um die Kameraschnittstelle deines Raspberry Pi zu aktivieren. Wenn du sie bereits aktiviert hast, kannst du diesen Schritt überspringen. Falls du unsicher bist, führe ihn bitte durch.  

.. raw:: html

   <run></run>

.. code-block:: 

   sudo raspi-config

**3 Interfacing options**

.. image:: img/image282.png
   :align: center

**P1 Camera**

.. image:: img/camera_config1.png
   :align: center

**<Yes>, dann <Ok> -> <Finish>**

.. image:: img/camera_config2.png
   :align: center

Nach Abschluss der Konfiguration empfiehlt es sich, den Raspberry Pi neu zu starten.

.. raw:: html

   <run></run>

.. code-block:: 

   sudo reboot

