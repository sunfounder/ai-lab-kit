.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

Installation du systeme d'exploitation
======================================



.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager


Telecharger le fichier image exclusif
------------------------------------------------------

Telechargez le fichier image du systeme d'exploitation AI Fusion Lab Kit : `Raspberry Pi OS with AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_.

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

Cette image est basee sur Raspberry Pi OS et est livree avec le AI Fusion Lab Kit pre-integre dans le systeme. Elle comprend tous les logiciels necessaires, les exemples de code et les configurations associees requises pour le AI Fusion Lab Kit. En utilisant cette image, vous pouvez ignorer certaines etapes de configuration decrites dans la documentation.

Si vous preferez utiliser un systeme Raspberry Pi OS natif pour une configuration manuelle, veuillez installer :
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. Allez dans la section OS et choisissez **Use custom**

   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   Et selectionnez le fichier image telecharge ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip``.

   .. image:: img/fusion_kit_imager2.png
      :width: 90%

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_storage
   :end-before: end_storage

.. .. include:: /_shared/pi_start/install_os_trixie.rst
..    :start-after: start_cutomization_os
..    :end-before: end_cutomization_os

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_write_os
   :end-before: end_write_os
