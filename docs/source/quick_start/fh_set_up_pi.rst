.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _setup_pi_fusion_kit:

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi
   :end-before: end_setup_pi

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_screen
   :end-before: end_setup_pi_screen

.. .. include:: /_shared/pi_start/set_up_pi.rst
..    :start-after: start_setup_pi_headless
..    :end-before: end_setup_pi_headless

----------------------------------
Si No Tienes Pantalla (Headless)
----------------------------------

Sin un monitor, puedes configurar e iniciar sesion en tu Raspberry Pi de forma remota.
Este es el metodo mas conveniente para la mayoria de los usuarios.

**Componentes Necesarios**

* Raspberry Pi
* Fuente de alimentacion oficial
* Tarjeta MicroSD
* Un ordenador en la misma red

**Consejos**

* Asegurate de que tu Raspberry Pi y tu ordenador esten en la misma red local.
* Para una mejor estabilidad, usa Ethernet si esta disponible.


**Conectar via SSH**

#. Abre una terminal en tu ordenador (Windows: **PowerShell**; macOS/Linux: **Terminal**) y conectate a tu Raspberry Pi:

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: En el sistema operativo AI Fusion Lab Kit, el nombre de usuario predeterminado es ``pi`` y la contraseña es ``123456``. El nombre de host predeterminado es ``ai-fusion``.


2. Alternativamente, localiza la direccion IP de tu Pi desde la lista DHCP de tu router y conectate con:

   .. code-block:: bash

      ssh pi@<IP address>
      # Example:
      ssh pi@192.168.1.42

3. En el primer inicio de sesion, escribe ``yes`` para confirmar el certificado SSH.

4. Ingresa la contraseña que configuraste en Raspberry Pi Imager.
   (No aparece nada mientras escribes, esto es normal.)

5. Despues de iniciar sesion, ahora tienes acceso completo a la linea de comandos.

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center



.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop
