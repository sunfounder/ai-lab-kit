.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

OpenCV计算机视觉基础入门
==================================================

本迷你课程是使用\ **OpenCV**\ 和\ **Python**\ 进行计算机视觉的动手入门教程。
您将学习如何加载与显示图像、处理视频流、访问Raspberry Pi摄像头、检测颜色、使用MeanShift/CAMShift追踪物体、利用Canny提取边缘，以及通过Haar级联进行轻量级的人脸与眼睛检测。

.. note::

   大多数章节同时包含\ **概念讲解**\ 和\ **完整代码块**。
   请从运行提供的脚本开始每章的学习，然后调整参数（阈值、内核大小、ROI）以观察即时效果。


.. toctree::
   :maxdepth: 1
   :caption: 目录:

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