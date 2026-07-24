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
Se Non Hai un Monitor (Headless)
----------------------------------

Senza un monitor, puoi configurare e accedere al tuo Raspberry Pi da remoto.
Questo e’ il metodo piu’ conveniente per la maggior parte degli utenti.

**Componenti Necessari**

* Raspberry Pi
* Alimentatore Ufficiale
* Scheda MicroSD
* Un computer sulla stessa rete

**Suggerimenti**

* Assicurati che il tuo Raspberry Pi e il tuo computer siano sulla stessa rete locale.
* Per la massima stabilita’, utilizza Ethernet se disponibile.


**Connettiti via SSH**

#. Apri un terminale sul tuo computer (Windows: **PowerShell**; macOS/Linux: **Terminale**) e connettiti al tuo Raspberry Pi:

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: Nel sistema operativo AI Fusion Lab Kit, il nome utente predefinito e’ ``pi`` e la password e’ ``123456``. Il nome host predefinito e’ ``ai-fusion``.


2. In alternativa, trova l’indirizzo IP del tuo Pi dall’elenco DHCP del router e connettiti con:

   .. code-block:: bash

      ssh pi@<indirizzo IP>
      # Esempio:
      ssh pi@192.168.1.42

3. Al primo accesso, digita ``yes`` per confermare il certificato SSH.

4. Inserisci la password che hai configurato in Raspberry Pi Imager.
   (Non appare nulla durante la digitazione — e’ normale.)

5. Dopo l’accesso, hai ora accesso completo alla riga di comando.

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center



.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop
