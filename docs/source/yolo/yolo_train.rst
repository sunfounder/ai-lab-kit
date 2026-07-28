.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. 训练自定义YOLO模型
=====================================

训练自己的YOLO模型，本质上就是让深度学习算法从您提供的图像数据中学习如何识别特定物体。这个过程可以类比为教一个孩子认识新事物：您给他们展示大量不同角度和环境下的示例图片，告诉他们"这是目标物体"。经过足够的示例学习后，他们就能在新的图片中准确识别出该物体。

对于YOLO来说，训练过程是这样的：

1. **数据准备**：收集包含目标物体的图像，并标注每个物体的位置和类别
2. **模型学习**：算法通过分析这些标注数据，自动学习物体的特征模式
3. **权重生成**：训练完成后，生成包含所学知识的模型文件（.pt文件）
4. **推理应用**：将该模型部署到Raspberry Pi上，用于检测新图像

得益于迁移学习，我们不需要从头开始训练。Ultralytics平台提供了预训练的基础模型（如YOLOv8n），它们已经在数百万张图像上完成了训练。我们只需要用少量自己的图像对这些模型进行"微调"，就能创建出有效的自定义模型。



----------------------------------------------------------

拍照采集
------------------------------

由于我们的YOLO项目基于Raspberry Pi，我们将使用Raspberry Pi摄像头来拍摄照片。为了获得更好的效果，我们还使用了手机拍摄一些照片以增加数据多样性。

**拍照技巧**

* **清晰度**：尽可能清晰地拍摄物体，避免模糊
* **多样性**：从不同角度（正面、侧面、俯视等）和不同光照条件（强光、弱光、逆光等）拍摄照片
* **背景变化**：尽量在不同的背景下拍摄，帮助模型学习物体的本质特征而非背景
* **避免重叠**：可以同时拍摄多个物体，但避免物体之间严重重叠
* **数量建议**：每类目标至少拍摄50-100张照片，图像越多效果越好

**应该用什么物体？**

您可以选择任何感兴趣的物体进行训练，例如：一个玩偶、一个杯子、一把椅子，甚至您的宠物。本教程以雪人玩具为例，请将其替换为您自己的目标物体。

.. image:: img/ultralytics_a1_capture_photo.png

**使用Raspberry Pi摄像头拍照**

以下是使用Raspberry Pi摄像头拍照的代码：

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_capture_images.py

.. code-block:: python

   #!/usr/bin/env python3
   """
   Simple camera capture script for Raspberry Pi
   Press SPACE to capture, ESC to exit
   Images saved to ./captured_images/
   """

   from picamera2 import Picamera2
   import cv2
   import os
   import time

   # Create save directory
   save_dir = "captured_images"
   os.makedirs(save_dir, exist_ok=True)

   # Initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   # Wait for camera to warm up
   time.sleep(1)

   print("=== Camera Capture Tool ===")
   print(f"Images will be saved to: {save_dir}")
   print("Controls:")
   print("  SPACE - Capture image")
   print("  ESC   - Exit")
   print("==========================")

   count = 0

   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Display frame with instructions
         display = frame.copy()
         cv2.putText(display, f"Captured: {count} images", (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
         cv2.putText(display, "Press SPACE to capture, ESC to exit", (10, 60),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         cv2.imshow("Camera Capture", display)

         # Wait for key press
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key
               # Save image
               filename = f"{save_dir}/img_{count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               count += 1

               # Optional: flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow("Camera Capture", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key
               print(f"\nExiting. Total captured: {count} images")
               break

   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("Camera stopped")

**将图像传输到电脑**

拍照后，使用 :ref:`filezilla`\ 将图像从Raspberry Pi下载到您的电脑：

1. 在Raspberry Pi上查看IP地址：\ ``hostname -I``
2. 在FileZilla中连接到Raspberry Pi（用户名：pi，密码：您的密码）
3. 导航到\ ``~/ai-lab-kit/yolo/captured_images/``\ 目录
4. 将所有图像下载到您的电脑


----------------------------------------------------------


训练模型
-------------------------------------------------

我们将使用在线\ `Ultralytics平台 <https://platform.ultralytics.com/>`_。该平台提供便捷的模型训练服务，无需配置复杂的训练环境。

**注册与登录**

1. 点击右上角的 **Get started**\ 进入注册页面，完成注册流程。

.. image:: img/ultralytics_1_signup.png

**创建数据集**

2. 注册后，您将进入主页。点击 **New Dataset**\ 创建新的数据集。

.. image:: img/ultralytics_3_new_dataset.png

3. 弹出一个窗口。在这里，您可以上传刚才用Raspberry Pi拍摄的照片，并输入 **Dataset name**\ （数据集名称）。然后点击 **Create & upload**\ （创建并上传）。

.. image:: img/ultralytics_4_create_dataset.png

4. 现在您进入了数据集界面，可以看到所有上传的图像。

.. image:: img/ultralytics_5_dataset.png

**标注图像**

5. 打开每张照片进行标注。使用右侧的 **+Add Class**\ 按钮添加类别。根据您要识别的对象添加适当的类别名称（例如：训练识别杯子则添加"cup"，训练识别宠物则添加"pet"）。

   **标注技巧**：
   - 使用鼠标在物体周围绘制边界框，尽量贴近物体边缘
   - 确保每个物体都被正确标注
   - 如果图像中没有目标物体，则无需标注

.. image:: img/ultralytics_6_train2.png

6. 重复以上步骤，直到所有照片都标注完成。检查每张图像上的标注是否准确。

.. image:: img/ultralytics_7_train3.png

**创建训练模型**

7. 点击 **Models**，然后点击 **New Model**。

.. image:: img/ultralytics_8_new_model.png

8. 在弹出的窗口中，选择 **YOLOv8n**\ 或 **YOLO11n**\ 作为 **Base Model**\ （基础模型）。这些是适合Raspberry Pi的Nano版本，体积小、速度快。

.. image:: img/ultralytics_9_new_model1.png

9. 配置训练参数：

   - **Image size**\ （图像大小）：选择 **320**\ （这是Raspberry Pi可以高效处理的图像大小）
   - **Epochs**\ （训练轮数）：保持默认（通常50-100轮）
   - **GPU Type**\ （GPU类型）：无特殊要求，但不同的GPU类型会影响训练速度和成本

   **注意**：Ultralytics新用户可获得5美元免费额度；训练一个小模型通常只需花费几美分，按需使用即可。

.. image:: img/ultralytics_9_new_model2.png

10. 点击 **Start Training**\ （开始训练）。等待一段时间（通常10-30分钟，取决于数据量和GPU），模型将完成训练。

    训练期间，您可以查看实时指标：

    - **box_loss**：边界框损失，越小越好
    - **cls_loss**：分类损失，越小越好
    - **mAP**：平均精度均值，越高越好（0-1范围）

**下载与部署**

11. 训练完成后，点击 **Download PyTorch Model**\ 下载训练好的模型（将是一个.pt文件）。

.. image:: img/ultralytics_10_download_model.png

12. 下载后，使用FileZilla将其传输到Raspberry Pi（建议放在\ ``~/ai-lab-kit/yolo/``\ 目录下）。

**运行自定义模型**

将模型放到Raspberry Pi后，您需要修改示例代码中的模型路径。以下是一个完整的运行示例：

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   nano yolo_custom.py

将模型文件名替换为您自己下载的文件：

.. code-block:: python
   :emphasize-lines: 6

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("your_model.pt")  # Replace with your model filename

   # initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLO start, Press 'q' to exit...")

   try:
      while True:
         # capture frame
         frame = picam2.capture_array()

         # run YOLO and set imgsz=320
         results = model(frame, imgsz=320)

         # draw results
         annotated = results[0].plot()

         # show results
         cv2.imshow("YOLO on Raspberry Pi", annotated)

         # press 'q' to exit
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("exit")

**验证结果**

13. 运行示例代码，观察YOLO模型在Raspberry Pi上的表现：

    .. code-block:: bash

       python3 yolo_custom.py

    如果一切正常，您应该能在摄像头画面中看到训练的目标物体被边界框框出，并显示类别名称和置信度分数。

.. image:: img/ultralytics_a2_yolo_find.png


恭喜！您已成功训练了自己的YOLO模型，并将其部署到了Raspberry Pi上。

----------------------------------------------------------

训练技巧与建议
-------------------------------------------------

**提升模型性能**

* **增加数据量**：每类目标至少50-100张图片
* **数据增强**：拍摄时主动变化角度、距离和光照
* **负样本**：包含一些没有目标物体的图像，有助于减少误检
* **平衡数据集**：如果识别多个类别，确保每个类别的图像数量相近



常见问题
-------------------------


**问：模型检测效果不理想怎么办？**

- 检查标注的准确性
- 增加训练图像数量
- 尝试更大的模型（如YOLOv8s）或更多训练轮数
- 从不同场景拍摄更多图像

**问：训练需要多长时间？**

- 大约50张图像配合YOLOv8n，通常需要10-20分钟
- 平台会根据所选的GPU自动调整

**问：可以在本地训练吗？**

可以，但需要配置Python环境和GPU驱动。对于初学者，建议使用Ultralytics平台快速验证想法。