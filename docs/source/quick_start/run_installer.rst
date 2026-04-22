.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note::

   プリインストールされた「Raspberry Pi OS mit AI Fusion Lab Kit」イメージを使用する場合は、このセクションをスキップできます。このイメージには、本章で説明するすべてのソフトウェアインストール、環境設定、およびサンプルコードのデプロイが既に含まれています。

.. _install_all_modules:

電源設定とソフトウェアのインストール
================================================================

この章では、関連するソフトウェアのインストール、オーディオ設定、安全な電源管理の構成、そして安全なシャットダウン方法について学びます。


.. _download_code:

サンプルコードのダウンロード
---------------------------------

このキットで使用するすべてのサンプルコードをダウンロードします：

   .. raw:: html

      <run></run>

   .. code-block::

      cd ~/
      git clone https://github.com/sunfounder/ai-lab-kit.git --depth 1


.. _install_fusion_hat:

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_install_fusion_hat
   :end-before: end_install_fusion_hat

.. include:: /_shared/pi_start/run_installer_fusion_hat.rst
   :start-after: start_configure_safe_shutdown
   :end-before: end_configure_safe_shutdown