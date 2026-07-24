.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

Gioca con OpenCV (Concetti Base di Computer Vision)
====================================================

Questo mini-corso e’ un’introduzione pratica alla computer vision con **OpenCV** in **Python**.
Imparerai come caricare e visualizzare immagini, lavorare con flussi video, accedere a una telecamera Raspberry Pi, rilevare colori, tracciare oggetti con MeanShift/CAMShift, estrarre bordi con Canny ed eseguire il rilevamento leggero di volti/occhi con Haar cascade.

.. note::

   La maggior parte dei capitoli include sia **spiegazioni dei concetti** che un **blocco di codice completo**.
   Inizia ogni capitolo eseguendo lo script fornito, poi modifica i parametri (soglie, dimensioni del kernel, ROI) per vedere effetti immediati.


.. toctree::
   :maxdepth: 1
   :caption: Contenuti:

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