.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mediapipe_install:

0. Setup MediaPipe
====================================================================

About the OS Version
-------------------------------

.. warning::

   **Recommended OS**: Raspberry Pi OS Bookworm (Debian 12, 64-bit)

   Raspberry Pi OS Trixie (Debian 13) is not recommended because:

   * MediaPipe does not yet support Python 3.13.
   * Picamera2 only works with the system Python.

This tutorial will be updated once Trixie becomes supported.

If you would like to request official MediaPipe support for Python 3.13, you can submit feedback here:

* GitHub Issue: https://github.com/google-ai-edge/mediapipe/issues/5708
* Support Page: https://ai.google.dev/edge/mediapipe/support



Before You Start
----------------

.. important::


   Before you start, make sure:

   * The pan-tilt is assembled
   * You can access the Raspberry Pi desktop
   * The code package is installed
   * Fusion HAT+ is installed and configured
   * OpenCV is installed

   For detailed instructions, see :ref:`opencv_install`.

These preparations ensure MediaPipe can run with full graphical and camera functionality on your Raspberry Pi.


Installation Steps
----------------------------------

#. Install MediaPipe

   Install MediaPipe using pip. On Raspberry Pi OS Bookworm (Debian 12, 64-bit),
   pip will download the correct wheel automatically.

   .. code-block:: bash

      sudo pip install mediapipe --break-system-packages

#. Verify the installation

   Run the following command to confirm that MediaPipe is installed correctly.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Expected output:

   .. code-block:: text

      MediaPipe version: 0.10.18


Common Issues & Solutions
-------------------------

#. MediaPipe installation fails

   This usually happens when using an unsupported OS version.

   Solution:

   * MediaPipe currently works only on Raspberry Pi OS Bookworm (Debian 12, 64-bit).
   * Raspberry Pi OS Trixie (Debian 13, Python 3.13) is not supported.

#. Camera cannot be opened in MediaPipe or OpenCV

   This usually happens when the Raspberry Pi camera interface is not enabled.

   Solution:

   * Enable the camera in ``raspi-config``:
     Interface Options → Camera → Enable

#. OpenCV import errors

   Some pip-installed versions of OpenCV may be incompatible with Raspberry Pi OS libraries.

   Solution:

   .. code-block:: bash

      sudo apt install python3-opencv

#. MediaPipe cannot be imported after installation

   This may happen if pip, setuptools, or wheel are outdated.

   Solution:

   .. code-block:: bash

      sudo pip install --upgrade pip setuptools wheel


Your MediaPipe is now ready.  
You can proceed to the next section to run real-time face detection using the Raspberry Pi camera.
