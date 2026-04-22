.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _install_os_sd_fusion_kit:

オペレーティングシステムのインストール
=======================================

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_imager
   :end-before: end_imager

専用イメージファイルのダウンロード
------------------------------------

AI Fusion Lab Kitのオペレーティングシステムイメージファイルをダウンロードします：  
`Raspberry Pi OS mit AI Fusion Lab Kit <https://sunfounder.github.io/download/ai-fusion-lab-kit/index.html>`_

.. image:: img/fusion_kit_imager_download.png
   :width: 90%

このイメージはRaspberry Pi OSをベースにしており、AI Fusion Lab Kitがシステムにあらかじめインストールされています。AI Fusion Lab Kitに必要なすべてのソフトウェア、サンプルコード、関連する設定が含まれています。このイメージを使用することで、マニュアルに記載されているいくつかの設定手順を省略できます。

もし手動で設定を行う標準のRaspberry Pi OSを使用したい場合は、以下をインストールしてください：  
`Raspberry Pi OS (Legacy, 64-bit) (Bookworm, Debian 12)`

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_install_os
   :end-before: end_install_os

3. 「オペレーティングシステム」セクションに移動し、**カスタムイメージを使用** を選択します。

   .. image:: img/fusion_kit_imager1.png
      :width: 90%

   ダウンロードしたイメージファイル ``ai.fusion.lab.kit-bookworm.64.full.20xx.xx.xx-latest.zip`` を選択します。

   .. image:: img/fusion_kit_imager2.png
      :width: 90%

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_storage
   :end-before: end_storage

.. .. include:: /_shared/pi_start/install_os_trixie.rst
..    :start-after: start_cutomization_os
..    :end-before: end_cutomization_os

.. include:: /_shared/pi_start/install_os_trixie.rst
   :start-after: start_write_os
   :end-before: end_write_os