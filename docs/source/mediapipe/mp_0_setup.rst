.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message



.. note:: Si estás usando la imagen preinstalada "Raspberry Pi OS with AI Fusion Lab Kit", puedes omitir esta sección. Esta imagen ya incluye todas las instalaciones de software, configuraciones de entorno e implementaciones de código de ejemplo descritas en este capítulo.


.. _mediapipe_install:

0. Configurar MediaPipe
====================================================================

Acerca de la Versión del SO
-------------------------------

.. warning::

   **SO recomendado**: Raspberry Pi OS Bookworm (Debian 12, 64 bits)

   Raspberry Pi OS Trixie (Debian 13) no se recomienda porque:

   * MediaPipe aún no es compatible con Python 3.13.
   * Picamera2 solo funciona con el Python del sistema.

Este tutorial se actualizará cuando Trixie sea compatible.

Si deseas solicitar compatibilidad oficial de MediaPipe para Python 3.13, puedes enviar comentarios aquí:

* GitHub Issue: https://github.com/google-ai-edge/mediapipe/issues/5708
* Página de Soporte: https://ai.google.dev/edge/mediapipe/support



Antes de Comenzar
----------------

.. important::


   Antes de comenzar, asegúrate de:

   * Tener el soporte para cámara ensamblado
   * Poder acceder al escritorio de Raspberry Pi
   * Tener el paquete de código instalado
   * Tener Fusion HAT+ instalado y configurado
   * Tener OpenCV instalado

   Para obtener instrucciones detalladas, consulta :ref:`opencv_install`.

Estas preparaciones aseguran que MediaPipe pueda ejecutarse con todas las funcionalidades gráficas y de cámara en tu Raspberry Pi.


Pasos de Instalación
----------------------------------

#. Instalar MediaPipe

   Instala MediaPipe usando pip. En Raspberry Pi OS Bookworm (Debian 12, 64 bits),
   pip descargará la rueda correcta automáticamente.

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. Verificar la instalación

   Ejecuta el siguiente comando para confirmar que MediaPipe esté instalado correctamente.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Salida esperada:

   .. code-block:: text

      MediaPipe version: 0.10.18


Problemas Comunes y Soluciones
-------------------------

#. La instalación de MediaPipe falla

   Esto suele ocurrir cuando se usa una versión de SO no compatible.

   Solución:

   * MediaPipe actualmente funciona solo en Raspberry Pi OS Bookworm (Debian 12, 64 bits).
   * Raspberry Pi OS Trixie (Debian 13, Python 3.13) no es compatible.

#. La cámara no se puede abrir en MediaPipe u OpenCV

   Esto suele ocurrir cuando la interfaz de la cámara Raspberry Pi no está habilitada.

   Solución:

   * Habilita la cámara en ``raspi-config``:
     Interface Options → Camera → Enable

#. Errores de importación de OpenCV

   Algunas versiones de OpenCV instaladas con pip pueden ser incompatibles con las bibliotecas de Raspberry Pi OS.

   Solución:

   .. code-block:: bash

      sudo apt install python3-opencv

#. MediaPipe no se puede importar después de la instalación

   Esto puede ocurrir si pip, setuptools o wheel están desactualizados.

   Solución:

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


Tu MediaPipe está listo.
Puedes continuar con la siguiente sección para ejecutar la detección de rostros en tiempo real usando la cámara Raspberry Pi.
