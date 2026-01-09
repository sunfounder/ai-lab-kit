.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

Play with OpenCV (Computer Vision Basics)
==================================================

This mini-course is a hands-on introduction to computer vision with **OpenCV** in **Python**.  
You’ll learn how to load and display images, work with video streams, access a Raspberry Pi camera, detect colors, track objects with MeanShift/CAMShift, extract edges with Canny, and run lightweight face/eye detection with Haar cascades.

.. note::

   Most chapters include both **concept explanations** and a **complete code block**.  
   Start each chapter by running the provided script, then tweak parameters (thresholds, kernel sizes, ROI) to see immediate effects.


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