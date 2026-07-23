.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Si vous utilisez l'image préinstallée "Raspberry Pi OS with AI Fusion Lab Kit", vous pouvez sauter cette section. Cette image inclut déjà toutes les installations logicielles, les configurations d'environnement et les déploiements de code d'exemple décrits dans ce chapitre.


.. _mediapipe_install:

0. Installer MediaPipe
==========================================================================

À propos de la Version du Système d'Exploitation
-------------------------------

.. warning::

   **OS recommandé** : Raspberry Pi OS Bookworm (Debian 12, 64 bits)

   Raspberry Pi OS Trixie (Debian 13) n'est pas recommandé car :

   * MediaPipe ne supporte pas encore Python 3.13.
   * Picamera2 fonctionne uniquement avec le Python système.

Ce tutoriel sera mis à jour dès que Trixie sera supporté.

Si vous souhaitez demander le support officiel de MediaPipe pour Python 3.13, vous pouvez soumettre un retour ici :

* GitHub Issue : https://github.com/google-ai-edge/mediapipe/issues/5708
* Page de support : https://ai.google.dev/edge/mediapipe/support



Avant de Commencer
----------------

.. important::


   Avant de commencer, assurez-vous :

   * Que le support motorisé est assemblé
   * Que vous pouvez accéder au bureau du Raspberry Pi
   * Que le package de code est installé
   * Que Fusion HAT+ est installé et configuré
   * Qu'OpenCV est installé

   Pour les instructions détaillées, voir :ref:`opencv_install`.

Ces préparations garantissent que MediaPipe peut fonctionner avec toutes les fonctionnalités graphiques et de la caméra sur votre Raspberry Pi.


Étapes d'Installation
----------------------------------

#. Installer MediaPipe

   Installez MediaPipe avec pip. Sur Raspberry Pi OS Bookworm (Debian 12, 64 bits),
   pip téléchargera la wheel correcte automatiquement.

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. Vérifier l'installation

   Exécutez la commande suivante pour confirmer que MediaPipe est installé correctement.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Sortie attendue :

   .. code-block:: text

      MediaPipe version: 0.10.18


Problèmes Courants et Solutions
-------------------------

#. L'installation de MediaPipe échoue

   Cela se produit généralement lors de l'utilisation d'une version non supportée du système d'exploitation.

   Solution :

   * MediaPipe fonctionne actuellement uniquement sur Raspberry Pi OS Bookworm (Debian 12, 64 bits).
   * Raspberry Pi OS Trixie (Debian 13, Python 3.13) n'est pas supporté.

#. La caméra ne peut pas être ouverte dans MediaPipe ou OpenCV

   Cela se produit généralement lorsque l'interface de la caméra Raspberry Pi n'est pas activée.

   Solution :

   * Activez la caméra dans ``raspi-config`` :
     Interface Options → Camera → Enable

#. Erreurs d'importation OpenCV

   Certaines versions d'OpenCV installées via pip peuvent être incompatibles avec les bibliothèques de Raspberry Pi OS.

   Solution :

   .. code-block:: bash

      sudo apt install python3-opencv

#. MediaPipe ne peut pas être importé après l'installation

   Cela peut se produire si pip, setuptools ou wheel sont obsolètes.

   Solution :

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


Votre MediaPipe est maintenant prêt.
Vous pouvez passer à la section suivante pour exécuter la détection faciale en temps réel avec la caméra Raspberry Pi.