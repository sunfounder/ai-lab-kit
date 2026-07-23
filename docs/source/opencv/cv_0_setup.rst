.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Si vous utilisez l'image préinstallée "Raspberry Pi OS with AI Fusion Lab Kit", vous pouvez sauter cette section. Cette image inclut déjà toutes les installations logicielles, les configurations d'environnement et les déploiements de code d'exemple décrits dans ce chapitre.


.. _opencv_install:

0. Installer OpenCV
======================================================================

Ce chapitre vous explique comment installer OpenCV sur le Raspberry Pi et vérifier qu'il fonctionne correctement.

#. Pour utiliser le module caméra facilement, :ref:`assemble_fusion_hat_pan_tilt` est recommandé.

   .. note::

      L'assemblage du support motorisé peut obstruer certaines broches, il est donc recommandé de l'assembler uniquement lors de l'utilisation de la caméra, ou de le placer à l'extérieur après assemblage.

   .. image:: ../quick_start/img/gimbal_assemble.png

#. Accédez au bureau du Raspberry Pi :

   * :ref:`remote_desktop` : Utilisez **VNC** pour une expérience de bureau complète.
   * |link_rpi_connect| : Utilisez **Raspberry Pi Connect** pour accéder à votre Pi en toute sécurité depuis n'importe quel navigateur.


#. Suivez la procédure dans :ref:`install_all_modules` (téléchargez le package de code fourni et terminez l'installation et la configuration de Fusion HAT+).


#. Maintenant, mettez à jour les sources logicielles du Raspberry Pi pour obtenir les derniers packages :

   .. code-block:: shell

      sudo apt update

#. Utilisez la commande suivante pour installer la version Python 3 d'OpenCV :

   .. code-block:: bash

      sudo apt install python3-opencv

#. Exécutez la commande ci-dessous pour vérifier qu'OpenCV a été installé avec succès :

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   Si le numéro de version d'OpenCV s'affiche, l'installation a réussi.

   .. image:: img/install_opencv_check_version.png
      :align: center