.. _mediapipe_install:

MediaPipe Installation Guide (Raspberry Pi)
==========================================

.. warning::
   
   To ensure full functionality of this project, the required MediaPipe and Picamera2 libraries are only fully compatible with **Raspberry Pi OS (Debian 12 / Bookworm , 64-bit)**.

   The new Raspberry Pi OS Trixie (Debian 13) uses Python 3.13 as the system Python, but:

   * MediaPipe is not yet compatible with Python 3.13.
   * Picamera2 (used for camera access) only works with the system Python.

   Please use **Raspberry Pi OS Bookworm 64-bit** for full compatibility.  
   This tutorial will be updated once Trixie becomes supported.


Before You Start
----------------

Before installing MediaPipe, make sure:

* OpenCV has been installed on your Raspberry Pi (see :ref:`opencv_install`).
* You can access the Raspberry Pi desktop through a display.

  * or remotely via **Raspberry Pi Connect** (|link_rpi_connect|)  
  * or remotely through VNC software (see :ref:`remote_desktop`).

* You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).

These preparations ensure MediaPipe can run with full graphical and camera functionality on your Raspberry Pi.



Installation Steps
------------------

#. **Create a virtual environment**

   A virtual environment keeps MediaPipe separated from system libraries
   and prevents version conflicts with other projects.

   .. code-block:: bash

      python3 -m venv ~/mediapipe_env --system-site-packages


#. **Activate the virtual environment**

   This switches Python into the isolated environment you just created.

   .. code-block:: bash

      source ~/mediapipe_env/bin/activate


#. **Upgrade pip**

   Updating pip reduces installation issues and ensures compatibility
   with the latest MediaPipe wheel packages.

   .. code-block:: bash

      pip install --upgrade pip


#. **Install MediaPipe**

   Install MediaPipe directly using pip.  
   On Raspberry Pi OS (Bookworm, ARM64), this will download the correct wheel.

   .. code-block:: bash

      pip install mediapipe


#. **Verify the installation**

   Run a quick test to confirm that MediaPipe is installed properly.

   .. code-block:: bash

      python3 - <<EOF
      import mediapipe as mp
      print("MediaPipe version:", mp.__version__)
      EOF

   Expected output:

   ::

      MediaPipe version: 0.10.18


Common Issues & Solutions
-------------------------

* **Problem:** MediaPipe installation fails

  This usually happens when using an unsupported system. MediaPipe currently works **only on Raspberry Pi OS Bookworm (Debian 12, 64-bit)**.  
  The newer Raspberry Pi OS Trixie (Python 3.13) is not supported.

  **Solution:** Install or switch to Raspberry Pi OS Bookworm.
* **Problem:** Camera cannot be opened in MediaPipe or OpenCV

  This usually happens when the Raspberry Pi camera interface has not been enabled in the system.

  **Solution:** Enable the camera using ``raspi-config`` (Interface Options → Enable Camera):

* **Problem:** OpenCV import errors

  Some pip-installed versions of OpenCV may be incompatible with Raspberry Pi OS libraries.

  **Solution:** Install the stable APT version of OpenCV:

  .. code-block:: bash

     sudo apt install python3-opencv

* **Problem:** MediaPipe cannot be imported after installation 

  This may happen if pip, setuptools, or wheel are outdated.

  **Solution:** Upgrade your Python packaging tools:

  .. code-block:: bash

     pip install --upgrade pip setuptools wheel


Your MediaPipe environment is now ready.  
You can proceed to the next section to run real-time face detection using the Raspberry Pi camera.
