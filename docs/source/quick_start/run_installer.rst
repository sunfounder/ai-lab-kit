.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: If you are using the pre-installed "Raspberry Pi OS with AI Fusion Lab Kit" image, you can skip this section. This image already includes all the software installations, environment configurations, and example code deployments described in this chapter.

.. _install_all_modules:

Configure Power & Install Software
================================================================

In this chapter, you’ll install the related software, configure audio, set up safe power management and learn how to handle shutdowns.
 

.. _download_code:

Download Sample Code
---------------------------------
Download the complete set of example code for the kit:

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
