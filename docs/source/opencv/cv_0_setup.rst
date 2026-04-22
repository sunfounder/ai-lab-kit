.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: 
   
   プリインストールされた「Raspberry Pi OS mit AI Fusion Lab Kit」イメージを使用する場合は、このセクションをスキップできます。このイメージには、本章で説明するすべてのソフトウェアインストール、環境設定、およびサンプルコードのデプロイが既に含まれています。

.. _opencv_install:

0. OpenCV のセットアップ
=========================================================================

この章では、Raspberry Pi に OpenCV をインストールし、正しく動作することを確認する方法を説明します。

#. カメラモジュールを使いやすくするため、:ref:`assemble_fusion_hat_pan_tilt` の組み立てを推奨します。

   .. note:: 
     
      パンチルトを組み立てると一部のピンが隠れる場合があるため、カメラを使用する場合のみ組み立てるか、組み立て後に外側へ配置することを推奨します。
   
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Raspberry Pi のデスクトップにアクセスします：

   * :ref:`remote_desktop` : **VNC** を使ってフルデスクトップ環境にアクセスします。
   * |link_rpi_connect| : **Raspberry Pi Connect** を使って、ブラウザから安全に Raspberry Pi へアクセスします。


#. :ref:`install_all_modules` のセットアップを完了してください（提供されているコードパッケージをダウンロードし、Fusion HAT+ のインストールと設定を完了します）。


#. 次に、最新のパッケージを取得できるよう、Raspberry Pi のソフトウェアソースを更新します：

   .. code-block:: shell

      sudo apt update

#. 以下のコマンドで、Python 3 用の OpenCV をインストールします：

   .. code-block:: bash

      sudo apt install python3-opencv

#. 次のコマンドを実行して、OpenCV が正常にインストールされたことを確認します：

   .. code-block:: bash

      python3 -c "import cv2; print(cv2.__version__)"

   OpenCV のバージョン番号が表示されれば、インストールは成功です。

   .. image:: img/install_opencv_check_version.png
      :align: center