.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

Mit OpenCV spielen (Grundlagen der Computer Vision)
===================================================================

Dieser Minikurs bietet einen praxisnahen Einstieg in die Computer Vision mit **OpenCV** in **Python**.  
Sie lernen, wie Sie Bilder laden und anzeigen, mit Videostreams arbeiten, auf eine Raspberry-Pi-Kamera zugreifen, Farben erkennen, Objekte mit MeanShift/CAMShift verfolgen, Kanten mit Canny extrahieren und eine leichtgewichtige Gesichts-/Augenerkennung mit Haar-Cascades ausführen.

.. note::

   Die meisten Kapitel enthalten sowohl **konzeptionelle Erklärungen** als auch einen **vollständigen Codeblock**.  
   Starten Sie jedes Kapitel, indem Sie das bereitgestellte Skript ausführen, und passen Sie dann Parameter (Schwellenwerte, Kernelgrößen, ROI) an, um die Auswirkungen sofort zu sehen.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

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