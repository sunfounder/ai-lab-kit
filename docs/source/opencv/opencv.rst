.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_opencv:

OpenCVで遊ぼう（コンピュータビジョンの基礎）
==================================================

このミニコースでは、 **Python** の **OpenCV** を使って、コンピュータビジョンを実践的に学びます。  
画像の読み込みと表示、動画ストリームの処理、Raspberry Pi カメラへのアクセス、色検出、MeanShift/CAMShift による物体追跡、Canny によるエッジ抽出、そして Haar カスケードを用いた軽量な顔・目検出まで、一通り体験できます。

.. note::

   ほとんどの章には、**概念の説明** と **完全なコードブロック** の両方が含まれています。  
   まずは各章で用意されたスクリプトを実行し、その後にパラメータ（しきい値、カーネルサイズ、ROI など）を調整して、結果がどのように変化するかを確認してみてください。


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