.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

Preguntas Frecuentes
====================


A continuacion se presentan algunas de las preguntas mas comunes que los usuarios pueden encontrar al usar el
AI Fusion Lab Kit. Si tu problema no aparece aqui, consulta las
notas de solucion de problemas en cada capitulo o contacta al soporte.

Preguntas Generales
-------------------

**¿Donde puedo descargar la imagen del sistema?**

    Puedes encontrar la imagen recomendada del sistema para Raspberry Pi y las instrucciones de configuracion
    en la seccion :ref:`get_start`. La documentacion tambien
    proporciona una guia de instalacion paso a paso para principiantes.

**¿Necesito conexion a internet para usar el kit?**

    Los ejemplos basicos de Python y hardware no requieren acceso a internet.
    Sin embargo, los LLM basados en la nube y algunas funciones de IA requieren una conexion
    a internet activa.

**¿Que modelos de Raspberry Pi son compatibles?**

    El kit es compatible oficialmente con Raspberry Pi 4B y Raspberry Pi 5.
    Otros modelos pueden funcionar, pero no estan garantizados debido a limitaciones
    de rendimiento o compatibilidad.

**¿Necesito alimentar el FusionHAT por separado?**

    Si. *El FusionHAT requiere su propia fuente de alimentacion*. La entrada de alimentacion
    de la Raspberry Pi no suministra energia al FusionHAT. Si el FusionHAT no esta
    alimentado, algunas funciones — como el altavoz u otros modulos integrados —
    pueden no funcionar correctamente.

Software / Instalacion
----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    Este problema generalmente es causado por un conflicto entre la libreria ``RPi.GPIO`` instalada en el sistema y la libreria GPIO utilizada por Fusion HAT.
    Para solucionarlo, elimina manualmente los archivos del paquete ``RPi.GPIO`` del sistema y luego ejecuta el programa nuevamente.

    1. Elimina los archivos del sistema ``RPi.GPIO``:

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Reinicia la Raspberry Pi:

       .. code-block:: bash

          sudo reboot

    3. Ejecuta el ejemplo nuevamente (no uses sudo a menos que sea necesario):

Despues de eliminar los archivos conflictivos de ``RPi.GPIO``, el ejemplo del boton basado en interrupciones deberia funcionar normalmente.



**OSError: Fusion HAT not connected, check if Fusion Hat is powered on**

Si encuentras este error al ejecutar algunos ejemplos (por ejemplo, al usar pines PWM), las posibles causas son:

1. El Fusion HAT no esta conectado correctamente;
2. Metodo de alimentacion incorrecto;
3. El controlador del Fusion HAT falta despues de una actualizacion del sistema Raspberry Pi.

Sigue los pasos a continuacion para verificar y resolver el problema:

1. Ejecuta el siguiente comando para verificar el estado del Fusion HAT:

   .. code-block:: bash

      i2cdetect -y 1

   En condiciones normales, deberias ver una salida similar a la siguiente (con ``UU`` en la direccion ``0x1e``):

   .. code-block:: bash

      pi@ai-fusion:~ $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:                         -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- --
      20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- -- --

2. Si no ves ``UU`` pero ves ``17``, el controlador del Fusion HAT falta. Reinstala el controlador ejecutando los siguientes comandos:

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. Si no ves ni ``UU`` ni ``17``, significa que el Fusion HAT no esta conectado a la Raspberry Pi o hay un problema de alimentacion. Asegurate de que tu Raspberry Pi este correctamente conectada al Fusion HAT y que la Raspberry Pi reciba alimentacion a traves del Fusion HAT (no alimentada de forma independiente).

4. Si los pasos anteriores no resuelven el problema, ejecuta los siguientes comandos y envianos la salida:

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat
      cat ~/.ai-fusion

**El script de instalacion fallo. ¿Que debo hacer?**

    Asegurate de que tu sistema operativo Raspberry Pi este actualizado y de que tengas una conexion
    de red estable durante la instalacion. Intenta ejecutar el script de configuracion nuevamente.
    Si el problema persiste, reinicia el sistema y verifica tu version de Python.

**Los ejemplos de Python no se ejecutan. ¿Cual podria ser la causa?**

    Esto generalmente esta relacionado con la falta de librerias de Python o una configuracion
    incorrecta del entorno. Verifica que las dependencias se hayan instalado
    siguiendo la guia de configuracion en :ref:`get_start`.

**La camara no es detectada.**

    Asegurate de que el cable de cinta este firmemente conectado y no insertado al reves.
    Tambien confirma que la interfaz de la camara este habilitada en la configuracion
    de la Raspberry Pi.

Funciones de IA
---------------

**Las respuestas del LLM son lentas o no regresan.**

    Esto a menudo indica una mala conectividad a internet o limites de tasa de API
    del proveedor de modelo seleccionado. Intenta cambiar de red o probar con un
    modelo diferente.

**El reconocimiento de voz (STT) es impreciso.**

    Verifica la conexion de tu microfono y reduce el ruido de fondo. Algunos modelos
    pueden requerir paquetes de idioma adicionales o ajustes de configuracion.

**Muestra 'Error querying device -1' en el modulo Vosk STT.**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    Ejecuta ``sudo /opt/setup_fusion_hat_audio.sh`` para reconfigurar el audio


**Permiso denegado al usar TTS/STT**

    Al ejecutar comandos de TTS (Texto a Voz) o STT (Voz a Texto), te encuentras con un error de permiso como:

    .. code-block:: bash

        Traceback (most recent call last):
            File "/home/pi/ai-lab-kit/llm/tts_piper.py", line 3, in <module>
                tts = Piper()
                    ^^^^^^^
            File "/usr/local/lib/python3.11/dist-packages/fusion_hat/tts.py", line 125, in _piper_init_with_speaker
                _original_piper_init(self, *args, **kwargs)
            File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/tts/piper.py", line 30, in __init__
                os.makedirs(PIPER_MODEL_DIR, 0o777)
            File "<frozen os>", line 225, in makedirs
        PermissionError: [Errno 13] Permission denied: '/opt/piper_models'


    Este problema ocurre en la version 0.0.1 del sistema operativo AI Fusion Lab Kit. El sistema intenta crear un directorio (/opt/piper_models) que requiere privilegios de root, pero el usuario actual no tiene permisos suficientes. Actualiza el sistema operativo AI Fusion Lab Kit de la version 0.0.1 a la 0.1.0 ejecutando el siguiente comando:

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash


Vision por Computadora / MediaPipe
-----------------------------------

**Los ejemplos de OpenCV muestran errores al acceder a la camara.**

    Solo un proceso puede acceder a la camara a la vez. Asegurate de que ninguna otra
    aplicacion de camara se este ejecutando en segundo plano.

**Los ejemplos de MediaPipe se ejecutan lentamente.**

    La vision por computadora en tiempo real requiere una potencia de procesamiento significativa. Considera
    reducir la resolucion de entrada o cerrar otros procesos para liberar recursos
    del sistema.

**Los proyectos de MediaPipe no funcionan en la ultima version de Raspberry Pi OS.**

    MediaPipe actualmente no es compatible con las versiones mas recientes del sistema Raspberry Pi (version Trixie)
    debido a cambios en las dependencias y la arquitectura. Utiliza la version anterior
    (version Bookworm) que es compatible con todos los ejemplos basados en MediaPipe.

Problemas de Hardware
---------------------

**Un componente no responde.**

    Revisa tus conexiones de cableado y asegurate de que la orientacion sea correcta.
    Consulta la seccion :ref:`cpn_list` para ver las descripciones de los pines y diagramas de ejemplo.

**El dispositivo deja de funcionar repentinamente.**

    Esto puede deberse a inestabilidad en la alimentacion. Asegurate de que tu fuente de alimentacion
    cumpla con las especificaciones recomendadas para el modelo de Raspberry Pi en uso.

Contacto y Soporte
------------------

**¿Como puedo obtener ayuda adicional?**

    Puedes consultar la documentacion para obtener pasos detallados de solucion de problemas.
    Si tienes alguna pregunta, comunicate con nosotros a **service@sunfounder.com** — estamos aqui para ayudarte.
