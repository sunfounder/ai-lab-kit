.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. note:: 
   
   プリインストールされた「Raspberry Pi OS mit AI Fusion Lab Kit」イメージを使用する場合は、このセクションをスキップできます。このイメージには、本章で説明するすべてのソフトウェアインストール、環境設定、およびサンプルコードのデプロイが既に含まれています。

.. _mediapipe_install:

0. MediaPipe のセットアップ
====================================================================

OS バージョンについて
-------------------------------

.. warning::

   **推奨 OS**: Raspberry Pi OS Bookworm（Debian 12、64-bit）

   Raspberry Pi OS Trixie（Debian 13）は次の理由により推奨されません：

   * MediaPipe はまだ Python 3.13 をサポートしていません。
   * Picamera2 はシステムの Python でのみ動作します。

Trixie がサポートされた際には、このチュートリアルを更新する予定です。

MediaPipe の Python 3.13 対応をリクエストしたい場合は、以下のページからフィードバックを送ることができます：

* GitHub Issue: https://github.com/google-ai-edge/mediapipe/issues/5708
* Support Page: https://ai.google.dev/edge/mediapipe/support



開始前の準備
----------------

.. important::


   作業を始める前に、次の項目を確認してください：

   * パンチルト機構が組み立てられている
   * Raspberry Pi のデスクトップ環境にアクセスできる
   * コードパッケージがインストールされている
   * Fusion HAT+ がインストールおよび設定済みである
   * OpenCV がインストールされている

   詳しい手順については :ref:`opencv_install` を参照してください。

これらの準備を行うことで、Raspberry Pi 上で MediaPipe をカメラおよびグラフィカル機能とともに正常に実行できます。


インストール手順
----------------------------------

#. MediaPipe をインストールする

   pip を使用して MediaPipe をインストールします。  
   Raspberry Pi OS Bookworm（Debian 12、64-bit）では、pip が適切な wheel パッケージを自動的にダウンロードします。

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. インストールの確認

   次のコマンドを実行して、MediaPipe が正しくインストールされていることを確認します。

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   期待される出力：

   .. code-block:: text

      MediaPipe version: 0.10.18


よくある問題と解決方法
-------------------------

#. MediaPipe のインストールに失敗する

   これは通常、サポートされていない OS バージョンを使用している場合に発生します。

   解決方法：

   * MediaPipe は現在、Raspberry Pi OS Bookworm（Debian 12、64-bit）のみで動作します。
   * Raspberry Pi OS Trixie（Debian 13、Python 3.13）はサポートされていません。

#. MediaPipe または OpenCV でカメラが開けない

   これは Raspberry Pi のカメラインターフェースが有効になっていない場合に発生することが多いです。

   解決方法：

   * ``raspi-config`` でカメラを有効にします：
     Interface Options → Camera → Enable

#. OpenCV の import エラー

   pip でインストールした OpenCV の一部のバージョンは、Raspberry Pi OS のライブラリと互換性がない場合があります。

   解決方法：

   .. code-block:: bash

      sudo apt install python3-opencv

#. インストール後に MediaPipe を import できない

   pip、setuptools、または wheel が古い場合に発生することがあります。

   解決方法：

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


これで MediaPipe の準備は完了です。  
次のセクションでは、Raspberry Pi カメラを使用したリアルタイムの顔検出を実行します。
