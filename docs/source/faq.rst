.. _faq:

FAQ
===


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
