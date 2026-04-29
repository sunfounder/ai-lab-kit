.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

FAQ
=====================


Below are some of the most common questions users may encounter while using the
AI Fusion Lab Kit. If your issue is not listed here, please refer to the
troubleshooting notes in each chapter or contact support.

General Questions
-----------------

**Where can I download the system image?**

    You can find the recommended Raspberry Pi system image and setup
    instructions in the :ref:`get_start` section. The documentation also
    provides step-by-step installation guidance for beginners.

**Do I need an internet connection to use the kit?**

    Basic Python and hardware examples do not require internet access.
    However, cloud-based LLMs and some AI features do require an active
    internet connection.

**Which Raspberry Pi models are supported?**

    The kit officially supports Raspberry Pi 4B and Raspberry Pi 5.
    Other models may work but are not guaranteed due to performance
    or compatibility limitations.

**Do I need to power the FusionHAT separately?**

    Yes. *The FusionHAT requires its own power supply*. The Raspberry Pi power
    input does not supply power to the FusionHAT. If the FusionHAT is not
    powered, certain functions — such as the speaker or other onboard modules —
    may not work properly.

Software / Installation
-----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    This issue is usually caused by a conflict between the system-installed ``RPi.GPIO`` library and the GPIO library used by Fusion HAT.  
    To solve it, please manually remove the system ``RPi.GPIO`` package files and then run the program again.

    1. Remove the system ``RPi.GPIO`` files:

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Reboot the Raspberry Pi:

       .. code-block:: bash

          sudo reboot

    3. Run the example again (do not use sudo unless required):

After removing the conflicting ``RPi.GPIO`` files, the interrupt-based button example should work normally.



**OSError: Fusion HAT not connected, check if Fusion Hat is powered on**

If you encounter this error when running some examples (e.g., when calling PWM pins), the possible causes are:

1. The Fusion HAT is not properly connected;
2. Incorrect power supply method;
3. The Fusion HAT driver is missing after a Raspberry Pi system update.

Follow the steps below to check and resolve the issue:

1. Run the following command to check the status of the Fusion HAT:

   .. code-block:: bash

      i2cdetect -y 1

   Under normal conditions, you should see output similar to the following (with ``UU`` at address ``0x1e``):

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

2. If you do not see ``UU`` but see ``17`` instead, the Fusion HAT driver is missing. Please reinstall the driver by running the following commands:

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. If you see neither ``UU`` nor ``17``, it means the Fusion HAT is not connected to the Raspberry Pi or there is a power issue. Please ensure that your Raspberry Pi is properly connected to the Fusion HAT and that the Raspberry Pi is powered by the Fusion HAT (not powered independently).

4. If the above steps do not resolve the issue, please run the following commands and send us the output:

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat

**The installation script failed. What should I do?**

    Ensure that your Raspberry Pi OS is up-to-date and that you have a stable
    network connection during installation. Try running the setup script again.
    If the issue persists, reboot the system and recheck your Python version.

**Python examples cannot run. What might be the cause?**

    This is usually related to missing Python libraries or incorrect
    environment setup. Verify that the dependencies were installed
    through the setup guide in :ref:`get_start`.

**The camera is not detected.**

    Make sure the ribbon cable is firmly connected and not inserted backwards.
    Also confirm that the camera interface is enabled in the Raspberry Pi
    configuration settings.

AI Features
-----------

**LLM responses are slow or not returning.**

    This often indicates poor internet connectivity or API-rate limits from
    the selected model provider. Try switching networks or testing with a
    different model.

**Speech-to-Text (STT) is inaccurate.**

    Check your microphone connection and reduce background noise. Some models
    may require additional language packs or configuration adjustments.

**Show 'Error querying device -1' in the Vosk STT module.**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    Please execute ``sudo /opt/setup_fusion_hat_audio.sh`` to re-setup audio


**Permission denied when usibg TTS/STT**

    When running TTS (Text-to-Speech) or STT (Speech-to-Text) commands, you encounter a permission error like:

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


    This issue occurs in AI Fusion Lab Kit OS version 0.0.1. The system attempts to create a directory (/opt/piper_models) that requires root privileges, but the current user lacks sufficient permissions. Update the AI Fusion Lab Kit OS from version 0.0.1 to 0.1.0 by running the following command:

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash


Computer Vision / MediaPipe
---------------------------

**OpenCV examples show errors when accessing the camera.**

    Only one process can access the camera at a time. Ensure that no other
    camera applications are running in the background.

**MediaPipe examples run slowly.**

    Real-time computer vision requires significant processing power. Consider
    reducing the input resolution or closing other processes to free system
    resources.

**MediaPipe projects do not work on the latest Raspberry Pi OS.**

    MediaPipe currently does not support the newest (Trixie version) Raspberry Pi system
    releases due to dependency and architecture changes. Please use the legecy version
    (Bookworm version) that supports all MediaPipe-based examples.

Hardware Issues
---------------

**A component does not respond.**

    Recheck your wiring connections and ensure proper orientation.
    Refer to the :ref:`cpn_list` section for pin descriptions and sample diagrams.

**The device suddenly stops working.**

    This may be caused by power instability. Please ensure your power supply
    meets the recommended specifications for the Raspberry Pi model in use.

Contact and Support
-------------------

**How can I get additional help?**

    You may consult the documentation for detailed troubleshooting steps.
    If you have any questions, just reach out to us at **service@sunfounder.com** —we’re here to help.
