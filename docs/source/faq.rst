.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

常见问题
=====================

以下列出了用户在使用 AI Fusion Lab Kit 时可能遇到的一些常见问题。如果您的问题未在此列出，请参考各章节中的故障排除说明或联系技术支持。

常规问题
-----------------

**在哪里可以下载系统镜像？**

    您可以在 :ref:`get_start` 部分找到推荐的 Raspberry Pi 系统镜像和设置
    说明。本文档还为初学者提供了逐步安装指导。

**使用此套件需要联网吗？**

    基础的 Python 和硬件示例不需要网络连接。
    然而，基于云的 LLM 和一些 AI 功能确实需要有效的网络连接。

**支持哪些 Raspberry Pi 型号？**

    该套件官方支持 Raspberry Pi 4B 和 Raspberry Pi 5。
    其他型号可能也能使用，但由于性能或兼容性限制，不保证完全可用。

**是否需要单独为 FusionHAT 供电？**

    是的。**FusionHAT 需要自己的电源**\ 。Raspberry Pi 的电源输入不会为 FusionHAT 供电。
    如果 FusionHAT 未上电，某些功能（如扬声器或其他板载模块）可能无法正常工作。

软件 / 安装
-----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    此问题通常由系统安装的 ``RPi.GPIO`` 库与 Fusion HAT 使用的 GPIO 库之间的冲突引起。
    要解决此问题，请手动删除系统中的 ``RPi.GPIO`` 包文件，然后重新运行程序。

    1. 删除系统 ``RPi.GPIO`` 文件：

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. 重新启动 Raspberry Pi：

       .. code-block:: bash

          sudo reboot

    3. 再次运行示例（除非必要，否则不要使用 sudo）：

删除冲突的 ``RPi.GPIO`` 文件后，基于中断的按钮示例应能正常工作。



**OSError: Fusion HAT not connected, check if Fusion Hat is powered on**

如果在运行某些示例（例如调用 PWM 引脚时）遇到此错误，可能的原因包括：

1. Fusion HAT 未正确连接；
2. 供电方式不正确；
3. Raspberry Pi 系统更新后缺少 Fusion HAT 驱动程序。

请按照以下步骤检查和解决问题：

1. 运行以下命令检查 Fusion HAT 的状态：

   .. code-block:: bash

      i2cdetect -y 1

   正常情况下，您应该看到类似以下的输出（地址 ``0x1e`` 处显示 ``UU``\ ）：

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

2. 如果未显示 ``UU`` 而是显示 ``17``，则说明 Fusion HAT 驱动程序缺失。请运行以下命令重新安装驱动程序：

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. 如果既未显示 ``UU`` 也未显示 ``17``，则说明 Fusion HAT 未连接到 Raspberry Pi 或存在电源问题。请确保您的 Raspberry Pi 已正确连接到 Fusion HAT，并且 Raspberry Pi 由 Fusion HAT 供电（而非独立供电）。

4. 如果上述步骤未能解决问题，请运行以下命令并将输出发送给我们：

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat
      cat ~/.ai-fusion

**安装脚本执行失败，该怎么办？**

    请确保您的 Raspberry Pi OS 是最新版本，且在安装过程中保持稳定的网络连接。尝试重新运行安装脚本。如果问题仍然存在，请重启系统并重新检查 Python 版本。

**Python 示例无法运行，可能的原因是什么？**

    这通常与缺少 Python 库或环境配置不正确有关。请确认已按照 :ref:`get_start` 中的设置指南完成依赖项的安装。

**无法检测到摄像头。**

    请确保排线连接牢固且方向正确。同时确认在 Raspberry Pi 配置设置中已启用摄像头接口。

AI 功能
-----------

**LLM 响应缓慢或无响应。**

    这通常表明网络连接质量较差或所选模型提供商的 API 速率受限。请尝试切换网络或使用不同的模型进行测试。

**语音转文本（STT）不准确。**

    请检查麦克风连接并减少背景噪音。某些模型可能需要额外的语言包或配置调整。

**Vosk STT 模块显示 'Error querying device -1'。**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    请执行 ``sudo /opt/setup_fusion_hat_audio.sh`` 重新设置音频。

**使用 TTS/STT 时权限被拒绝**

    运行 TTS（文本转语音）或 STT（语音转文本）命令时，遇到类似如下的权限错误：

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

    此问题出现在 AI Fusion Lab Kit OS 版本 0.0.1 中。系统尝试创建需要 root 权限的目录 (/opt/piper_models)，但当前用户权限不足。请运行以下命令将 AI Fusion Lab Kit OS 从 0.0.1 升级到 0.1.0：

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash

计算机视觉 / MediaPipe
---------------------------

**OpenCV 示例在访问摄像头时显示错误。**

    每次只能有一个进程访问摄像头。请确保没有其他摄像头应用程序在后台运行。

**MediaPipe 示例运行缓慢。**

    实时计算机视觉需要大量的处理能力。请考虑降低输入分辨率或关闭其他进程以释放系统资源。

**MediaPipe 项目在最新的 Raspberry Pi OS 上无法运行。**

    MediaPipe 目前不支持最新的（Trixie 版本）Raspberry Pi 系统版本，这是由于依赖关系和架构变化所致。请使用支持所有基于 MediaPipe 的示例的旧版本（Bookworm 版本）。

硬件问题
---------------

**某个组件无响应。**

    请重新检查接线连接，确保方向正确。请参考 :ref:`cpn_list` 部分查看引脚说明和示例图示。

**设备突然停止工作。**

    这可能是由电源不稳定引起的。请确保您的电源符合所用 Raspberry Pi 型号的推荐规格。

联系与支持
-------------------

**如何获得更多帮助？**

    您可以查阅文档了解详细的故障排除步骤。如果您有任何疑问，请发送邮件至 **service@sunfounder.com**，我们很乐意为您提供帮助。
