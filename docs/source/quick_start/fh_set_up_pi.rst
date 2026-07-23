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

------------------------------------------------------
Si vous n'avez pas d'ecran (sans interface graphique)
------------------------------------------------------

Sans moniteur, vous pouvez configurer et vous connecter a votre Raspberry Pi a distance.
C'est la methode la plus pratique pour la plupart des utilisateurs.

**Composants requis**

* Raspberry Pi
* Alimentation officielle
* Carte MicroSD
* Un ordinateur sur le meme reseau

**Conseils**

* Assurez-vous que votre Raspberry Pi et votre ordinateur sont sur le meme reseau local.
* Pour une meilleure stabilite, utilisez Ethernet si possible.


**Connexion via SSH**

#. Ouvrez un terminal sur votre ordinateur (Windows : **PowerShell** ; macOS/Linux : **Terminal**) et connectez-vous a votre Raspberry Pi :

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: Dans le systeme d'exploitation AI Fusion Lab Kit, le nom d'utilisateur par defaut est ``pi`` et le mot de passe est ``123456``. Le nom d'hote par defaut est ``ai-fusion``.


2. Sinon, trouvez l'adresse IP de votre Pi dans la liste DHCP de votre routeur et connectez-vous avec :

   .. code-block:: bash

      ssh pi@<adresse IP>
      # Exemple :
      ssh pi@192.168.1.42

3. Lors de la premiere connexion, tapez ``yes`` pour confirmer le certificat SSH.

4. Saisissez le mot de passe que vous avez configure dans Raspberry Pi Imager.
   (Rien n'apparait lors de la saisie -- c'est normal.)

5. Apres la connexion, vous avez un acces complet en ligne de commande.

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center



.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop
