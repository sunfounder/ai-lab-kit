2. Play Video
=======================================

In this chapter, you’ll learn how to read and play video streams in OpenCV, and how to control playback speed by calculating the frame processing time.



1. Project Overview
-------------------

In this section, we will achieve the following goals:

- Use ``cv2.VideoCapture`` to open a video file
- Read and display video frame by frame
- Automatically restart the video after it ends
- Control the playback frame rate using processing time calculations
- Press the `q` key to exit playback

.. image:: img/opencv_video.png
   :alt: Video playback interface illustration
   :align: center


2. Run the Code
------------------------



Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).

Open the terminal in VNC and enter the following command:



.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_video.py



3. Complete Code
----------------

.. code-block:: python

   import cv2

   # Read video
   cap = cv2.VideoCapture('sample2.mp4')

   while True:
       start_time = cv2.getTickCount()
       ret, frame = cap.read()
       
       # If video ends, restart from beginning
       if not ret:
           cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
           continue

       # Resize frame for better display
       frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
       
       # Show results
       cv2.imshow('Video', frame)

       # Calculate delay to maintain desired FPS
       expected_delay = max(1, int(1000 / cap.get(cv2.CAP_PROP_FPS)))
       process_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
       delay = int(expected_delay - process_time)
       
       # Ensure delay is non-negative
       delay = max(0, delay)
       
       # Wait for the next frame
       k = cv2.waitKey(delay) & 0xff
       if k == ord('q'):
           break

   # Release video capture object
   cap.release()

   # Destroy all opened windows
   cv2.destroyAllWindows()

4. Execution Result
-------------------

After successfully running the code, a window will pop up playing `sample2.mp4`.

- The video will automatically restart when it reaches the end.  
- Playback speed will be close to the original FPS.  
- Press `q` to exit the program.

.. note::

   - Make sure the video file path is correct.  
   - If the video cannot be played, check the video codec format or try using common formats such as `.mp4` or `.avi`.  
   - If the playback speed seems off, print ``cap.get(cv2.CAP_PROP_FPS)`` to confirm the FPS.


5. Code Explanation
-------------------

- ``cap = cv2.VideoCapture('sample2.mp4')``  

  Opens the video file `sample2.mp4`. If the path is incorrect, the video cannot be read.

- ``ret, frame = cap.read()``  

  Reads the video frame by frame. ``ret`` indicates whether the read was successful, and ``frame`` stores the current frame.

- ``if not ret: cap.set(cv2.CAP_PROP_POS_FRAMES, 0)``  

  When the video reaches the end, the frame pointer is reset to the beginning to enable looped playback.

- ``frame = cv2.resize(frame, (640, 480))``  

  Resizes the video frame to 640×480 for consistent display.

- ``expected_delay = 1000 / FPS`` + processing time calculation  

  Calculates the expected delay for each frame and adjusts it dynamically based on actual processing time to maintain smooth playback.

- ``cv2.waitKey(delay)``  

  Controls how long each frame stays on the screen. Press `q` to quit the playback.

- ``cap.release()`` and ``cv2.destroyAllWindows()``  

  Release the video capture object and close all OpenCV windows.




6. Further Practice
-------------------

- Try changing the window size to see how it affects image clarity.  
- Replace the video file with different ones to test compatibility.  
- Print the processing time per frame to better understand the relationship between FPS and playback delay.
