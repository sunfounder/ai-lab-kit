.. _mediapipe_install:

0. MediaPipe Environment Setup
=====================================

.. warning::
   
   To ensure full functionality of this project, the required MediaPipe and Picamera2 libraries are only fully compatible with **Raspberry Pi OS (Debian 12 / Bookworm)**.

   The newly released Raspberry Pi OS based on Debian 13 (Trixie) ships with Python 3.13, but:

   * MediaPipe is not yet compatible with Python 3.13, and cannot be installed in the system environment.
   * Picamera2 and its libcamera Python bindings are built only for the system Python.

   Therefore, please use **Raspberry Pi OS (Bookworm, Debian 12)** to ensure full compatibility.


-----------------------------
1. Install OpenCV and VNC
-----------------------------

Before proceeding with MediaPipe, we need to install OpenCV and VNC to run MediaPipe on your Raspberry Pi.

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).


----------------------------------------------------------------
2. Create a Virtual Environment
----------------------------------------------------------------


Using a virtual environment is recommended to avoid dependency conflicts between different projects.

.. code-block:: bash

   # Create a virtual environment named 'mediapipe_env'
   python3 -m venv ~/mediapipe_env --system-site-packages

   # Activate the virtual environment
   source ~/mediapipe_env/bin/activate

   # Upgrade pip
   pip install --upgrade pip

.. note::

   All mediapipe related commands and projects should be run in the mediapipe environment.
   
.. note::

   After each reboot of your Raspberry Pi, if you need to use the mediapipe environment again, please re-run:

   .. code-block:: bash

      source ~/mediapipe_env/bin/activate



----------------------------------------------------------------
3. Install MediaPipe
----------------------------------------------------------------

MediaPipe can be installed directly via pip:

.. code-block:: bash

   pip install mediapipe

.. note::

   - For Raspberry Pi OS, `mediapipe` has supported ARM64 since version 0.10.0.
   - If you encounter an "unsupported platform" error, please check if your Python and system architecture are 64-bit.
   - You can confirm the architecture using the following commands:

     .. code-block:: bash

        uname -m
        python3 -V



----------------------------------------------------------------
4. Common Installation Issues and Solutions
----------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Issue
     - Possible Cause
     - Solution
   * - ``mediapipe`` installation fails
     - Python or system architecture incompatibility
     - Ensure it's a 64-bit system; Use ``pip install mediapipe==0.10.5``
   * - Camera cannot be opened
     - Driver not enabled
     - Run ``sudo raspi-config`` → Interface Options → Enable Camera
   * - OpenCV error
     - pip version incompatibility
     - Use ``sudo apt install python3-opencv`` or upgrade pip
   * - Error importing mediapipe
     - pip version is too old
     - Run ``pip install --upgrade pip setuptools wheel``

------------------------------------
5. Verify MediaPipe Installation
------------------------------------

.. code-block:: bash

   python3 - <<EOF
   import mediapipe as mp
   print("MediaPipe version:", mp.__version__)
   EOF

If the terminal outputs a version number, for example:

::

   MediaPipe version: 0.10.18

Then the installation is successful! 🎉



At this point, the MediaPipe runtime environment on your Raspberry Pi is set up.
The next section will introduce how to use MediaPipe for real-time face detection.