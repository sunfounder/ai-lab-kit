.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: Si vous utilisez l'image pre-installee "Raspberry Pi OS with AI Fusion Lab Kit", vous pouvez ignorer cette section. Cette image comprend deja toutes les installations logicielles, les configurations d'environnement et les deploiements de code d'exemple decrits dans ce chapitre.

.. _install_all_modules:

Configurer l'alimentation et installer les logiciels
================================================================

Dans ce chapitre, vous allez installer les logiciels associes, configurer l'audio, mettre en place une gestion sure de l'alimentation et apprendre a gerer les arrets.



.. _download_code:

Telecharger le code d'exemple
---------------------------------
Telechargez l'ensemble complet du code d'exemple pour le kit :

   .. raw:: html

      <run></run>

   .. code-block::

      cd ~/
      git clone https://github.com/sunfounder/ai-lab-kit.git --depth 1


.. _install_fusion_hat:

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_install_fusion_hat
   :end-before: end_install_fusion_hat

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_configure_safe_shutdown
   :end-before: end_configure_safe_shutdown
