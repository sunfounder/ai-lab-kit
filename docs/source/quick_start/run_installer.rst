.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. note:: Si estas usando la imagen preinstalada "Raspberry Pi OS with AI Fusion Lab Kit", puedes omitir esta seccion. Esta imagen ya incluye todas las instalaciones de software, configuraciones de entorno e implementaciones de codigo de ejemplo descritas en este capitulo.

.. _install_all_modules:

Configurar Alimentacion e Instalar Software
================================================================

En este capitulo, instalaras el software relacionado, configuraras el audio, estableceras la gestion segura de alimentacion y aprenderas como manejar los apagados.


.. _download_code:

Descargar Codigo de Ejemplo
---------------------------------
Descarga el conjunto completo de codigo de ejemplo para el kit:

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
