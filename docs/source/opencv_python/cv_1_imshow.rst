1. Show Image
==============================================

In this chapter, we’ll explore a simple example to help you quickly experience the basic usage of OpenCV: **reading and displaying an image**.

In the example project folder, we have already prepared a sample photo named ``my_photo.jpg``.  
You can also use the :ref:`py_photograph` example to take a photo and save it to the current folder.


1. Project Overview
-------------------

In this section, we will accomplish the following tasks:

- Use ``cv2.imread`` to read a local image
- Use ``cv2.imshow`` to display the image
- Use ``cv2.waitKey`` to control window behavior
- Use ``cv2.destroyAllWindows`` to close the window

After successfully running this code, an image window will pop up on your screen.

.. image:: img/opencv_imshow.png
   :alt: Preview of the result
   :align: center


2. Run the Code
------------------------

.. 1. Make sure you have installed OpenCV on your Raspberry Pi (see the previous chapter).  
.. 2. Make sure you have installed ``realVNC`` and can connect to your Raspberry Pi through it.  
.. 3. Make sure you have downloaded the ``ai-lab-kit`` project (see :ref:`download_code`).  
.. 4. In RealVNC, navigate to the project directory ``ai-lab-kit/opencv_python``, where you will find several existing scripts.  
.. 5. In this project, open the ``cv_imgshow.py`` file to see the effect.



Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).

Open the terminal in VNC and enter the following command:


.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_imgshow.py

3. Complete Code
----------------

.. code-block:: python

   # Python code to read image
   import cv2

   # To read image from disk, we use
   # cv2.imread function, in below method,
   img = cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)

   # Creating GUI window to display an image on screen
   # first Parameter is window title (should be in string format)
   # Second Parameter is image array
   cv2.imshow("Picture", img)

   # To hold the window on screen, we use cv2.waitKey method
   # Once it detects the close input, it will release the control
   # To the next line
   # First Parameter is for holding screen for specified milliseconds
   # It should be positive integer. If 0 is passed as parameter, then it will
   # hold the screen until user closes it.
   cv2.waitKey(0)

   # It is for removing/deleting created GUI window from screen
   # and memory
   cv2.destroyAllWindows()



4. Execution Result
-------------------

When you run the code, an image window will pop up displaying `my_photo.jpg`.

.. note::

   - If you see an “image cannot be loaded” error, make sure `my_photo.jpg` exists in the current working directory.  
   - You can also try reading the image using an absolute path, for example:

     ::

        img = cv2.imread("/home/<USER_NAME>/ai-lab-kit/opencv_python/my_photo.jpg", cv2.IMREAD_COLOR)


5. Code Explanation
-------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``  

  Reads the image named `my_photo.jpg` and loads it in color mode.

- ``cv2.imshow("Picture", img)``  

  Creates a window titled “Picture” and displays the image.

- ``cv2.waitKey(0)``  

  When the parameter is `0`, the program will wait indefinitely until you close the window or press any key.

- ``cv2.destroyAllWindows()``  

  Closes all OpenCV windows and releases resources.



6. Further Practice
-------------------

- Try changing the window title in ``imshow`` to “My First OpenCV Window”.  
- Replace the image with a different one and observe the result.  
- Modify the ``waitKey`` parameter to `3000` so the program automatically closes the window after 3 seconds.
