.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

Juega con OpenCV (Conceptos Básicos de Visión Artificial)
=========================================================

Este minicurso es una introducción práctica a la visión artificial con **OpenCV** en **Python**.
Aprenderás a cargar y mostrar imágenes, trabajar con flujos de video, acceder a la cámara Raspberry Pi, detectar colores, rastrear objetos con MeanShift/CAMShift, extraer bordes con Canny y ejecutar detección ligera de rostros/ojos con clasificadores Haar.

.. note::

   La mayoría de los capítulos incluyen tanto **explicaciones conceptuales** como un **bloque de código completo**.
   Comienza cada capítulo ejecutando el script proporcionado, luego ajusta los parámetros (umbrales, tamaños de kernel, ROI) para ver los efectos inmediatos.


.. toctree::
   :maxdepth: 1
   :caption: Contenido:

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
