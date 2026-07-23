.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

Jouer avec OpenCV (Les bases de la vision par ordinateur)
==========================================================

Ce mini-cours est une introduction pratique à la vision par ordinateur avec **OpenCV** en **Python**.
Vous apprendrez à charger et afficher des images, travailler avec des flux vidéo, accéder à une caméra Raspberry Pi, détecter des couleurs, suivre des objets avec MeanShift/CAMShift, extraire des contours avec Canny, et exécuter une détection légère de visages/yeux avec les cascades Haar.

.. note::

   La plupart des chapitres incluent à la fois des **explications conceptuelles** et un **bloc de code complet**.
   Commencez chaque chapitre en exécutant le script fourni, puis modifiez les paramètres (seuils, tailles de noyau, ROI) pour observer les effets immédiats.


.. toctree::
   :maxdepth: 1
   :caption: Sommaire :

   cv_0_setup.rst
   cv_1_imshow.rst
   cv_2_video.rst
   cv_3_camera.rst
   cv_4_color.rst
   cv_5_meanshift.rst
   cv_6_camshift.rst
   cv_7_canny.rst
   cv_8_face.rst
   cv_9_color_track.rst