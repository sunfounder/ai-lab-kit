.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: 如果您使用的是预装了 "Raspberry Pi OS with AI Fusion Lab Kit" 镜像，则可以跳过本部分。此镜像已包含本章所述的所有软件安装、环境配置和示例代码部署。

.. _install_all_modules:

配置电源与安装软件
================================================================

在本章中，您将安装相关软件、配置音频、设置安全电源管理，并学习如何处理关机。


.. _download_code:

下载示例代码
---------------------------------
下载套件的完整示例代码：

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
