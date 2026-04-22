.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: プリインストールされた「Raspberry Pi OS mit AI Fusion Lab Kit」イメージを使用する場合は、このセクションをスキップできます。このイメージには、本章で説明するすべてのソフトウェアインストール、環境設定、およびサンプルコードのデプロイが既に含まれています。

0. YOLO環境のセットアップ
==============================

この章では、Raspberry PiにYOLOをインストールし、正しく動作することを確認する方法を説明します。

#. カメラモジュールを便利に使用するために、:ref:`assemble_fusion_hat_pan_tilt` の組み立てを推奨します。

   .. note:: 
     
      パンチルトユニットを組み立てると、いくつかのピンが隠れてしまう可能性があります。そのため、カメラを使用する際に組み立てるか、組み立て後に外側に配置することをお勧めします。
   
   .. image:: ../quick_start/img/gimbal_assemble.png

#. Raspberry Piデスクトップにアクセスします：

   * :ref:`remote_desktop`：**VNC** を使用して完全なデスクトップ環境を利用します。
   * |link_rpi_connect|：**Raspberry Pi Connect** を使用して、任意のブラウザから安全にPiにアクセスします。

3. 必要な依存関係をインストールします：

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade -y
      sudo apt install python3-pip python3-opencv python3-numpy python3-picamera2 -y

4. Ultralytics（公式YOLOライブラリ）をインストールします：

   .. code-block:: bash

      # CPUバージョンのPyTorchをインストール（CPUソースを指定）
      pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --break-system-packages

      # Ultralyticsをインストール（ただしtorchの依存関係はスキップ）
      pip3 install ultralytics --no-deps --break-system-packages

      # Ultralyticsのその他の依存関係を手動でインストール
      pip3 install pyyaml requests psutil polars tqdm matplotlib seaborn --break-system-packages