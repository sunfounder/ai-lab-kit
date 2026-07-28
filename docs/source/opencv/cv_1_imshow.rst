.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. 显示图像
==============================================

在本章中，我们将探索一个简单示例，帮助您快速体验OpenCV的基本用法：\ **读取和显示图像**。

在示例项目文件夹中，我们已经准备了一张名为\ ``my_photo.jpg``\ 的示例照片。
您也可以使用 :ref:`py_photograph`\ 示例拍摄照片并保存到当前文件夹。


1. 项目概览
-------------------

在本节中，我们将完成以下任务：

- 使用 ``cv2.imread`` 读取本地图像
- 使用 ``cv2.imshow`` 显示图像
- 使用 ``cv2.waitKey`` 控制窗口行为
- 使用 ``cv2.destroyAllWindows`` 关闭窗口

成功运行此代码后，屏幕上将弹出一个图像窗口。

.. image:: img/opencv_imshow.png
   :alt: 结果预览
   :align: center


2. 运行代码
------------------------

.. important::

   开始之前，请确保：

   * 云台已组装
   * 您可以访问Raspberry Pi桌面
   * 代码包已安装
   * Fusion HAT+已安装并配置
   * OpenCV已安装

   详细说明请参见 :ref:`opencv_install`。


#. 打开终端并输入以下命令：

   .. code-block:: bash

      cd ~/ai-lab-kit/opencv_python
      python3 cv_1_imgshow.py

#. 运行脚本后，OpenCV会打开一个标题为\ ``Picture``\ 的窗口，并显示从\ ``my_photo.jpg``\ 加载的图像。

   窗口将保持打开状态，直到用户退出程序。

   要退出程序，您可以：

   * 按键盘上的 **q** 键
   * 点击关闭按钮关闭窗口

   窗口关闭后，所有OpenCV资源将被释放，程序退出。

3. 完整代码
-------------------

.. code-block:: python

   # Python code to read and display an image using OpenCV
   import cv2
   from pathlib import Path

   # Get the directory of the current Python file
   BASE_DIR = Path(__file__).resolve().parent

   # Read image from disk
   # cv2.imread loads the image as a NumPy array
   img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

   # Create a GUI window to display the image
   # First parameter: window title
   # Second parameter: image array
   cv2.imshow("Picture", img)

   # Keep the window open until the user closes it or presses 'q'
   # cv2.waitKey only listens for keyboard events, not the close button
   # Therefore, we use a loop to detect both window close and key press
   while True:
      # Check if the window has been closed
      if cv2.getWindowProperty("Picture", cv2.WND_PROP_VISIBLE) < 1:
         break

      # Wait for 1 ms and check for key press
      # Press 'q' to exit the program
      if cv2.waitKey(1) & 0xFF == ord("q"):
         break

   # Destroy all OpenCV windows and release memory
   cv2.destroyAllWindows()

4. 代码解释
----------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``

  读取名为\ ``my_photo.jpg``\ 的图像，并以彩色模式加载。

- ``cv2.imshow("Picture", img)``

  创建一个标题为"Picture"的窗口并显示图像。

- ``cv2.waitKey(0)``

  当参数为\ ``0``\ 时，程序将无限等待，直到您关闭窗口或按下任意键。

- ``cv2.getWindowProperty()``

  获取指定窗口的属性值（例如，窗口是否仍然可见）。


- ``cv2.destroyAllWindows()``

  关闭所有OpenCV窗口并释放资源。

5. 扩展练习
-----------------------

- 尝试将\ ``imshow``\ 中的窗口标题改为"My First OpenCV Window"。
- 将图像替换为其他图片并观察结果。
- 将\ ``waitKey``\ 参数修改为\ ``3000``，使程序在3秒后自动关闭窗口。