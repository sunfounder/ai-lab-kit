.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. 使用YOLOE检测任意物体
===================================

YOLOE（You Only Look Once with Embeddings）是YOLO家族的最新成员，引入了语言-视觉联合学习能力。简单来说，YOLOE不仅能检测训练过的物体，还能通过文本描述或提示检测任意新物体，无需重新训练。

YOLOE的主要特点：

* **开放词汇检测**：通过文本描述检测任意物体，不限于预定义类别
* **无提示模式**：无需任何提示即可自动检测图像中的显著物体
* **高效部署**：继承了YOLO的高效架构，在Raspberry Pi上流畅运行
* **多任务支持**：支持目标检测和实例分割等多种任务

这使得YOLOE特别适合快速原型开发以及需要灵活检测各种物体的应用。

安装依赖
---------------------------------------------------

首先，安装YOLOE所需的CLIP库：

.. code-block:: bash

   pip3 install git+https://github.com/ultralytics/CLIP.git --break-system-packages

无提示模式
-----------------------------

无提示模式是使用YOLOE最直观的方式。在此模式下，模型自动检测图像中所有显著的物体，无需任何文本提示。其行为类似于传统YOLO，但具有更好的开放词汇能力。

.. image:: img/yolo_prompt_free1.png

图示：我将摄像头对准了杂乱的桌面，YOLOE的无提示模式自动识别并分割了视野中所有显著的物体——显示器、键盘、水杯、笔记本、鼠标……每个物体都用不同颜色的分割掩膜标注，无需任何文本提示。一切都一目了然。

**工作原理**：模型通过视觉特征分析自动识别图像中的前景物体并进行分割。这种方法适用于快速浏览图像内容，或不确定需要检测哪些物体的情况。

以下代码演示了如何在Raspberry Pi上以无提示模式运行YOLOE：

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_free.py

.. code-block:: python

   from ultralytics import YOLO
   from picamera2 import Picamera2
   import cv2

   # prompt-free mode
   model = YOLO("yoloe-11s-seg-pf.pt")  # pf = prompt-free

   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("Prompt-free mode: detecting everything automatically...")
   print("Press 'q' to exit")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, imgsz=320)
      annotated = results[0].plot()
      cv2.imshow("YOLOE Prompt-Free", annotated)

      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**无提示模式的特点**：

* **无需配置**：直接运行即可检测图像中的显著物体
* **自动分割**：同时输出检测框和分割掩膜
* **无类别标签**：仅显示检测到的物体位置，不含类别名称
* **适用场景**：快速浏览、通用目标检测、发现未知物体

文本提示模式
----------------------------------

文本提示模式是YOLOE真正展现其强大能力的地方。通过自然语言描述，您可以告诉模型要检测什么物体，模型会实时识别并定位这些物体。

.. image:: img/yolo_prompt_word.png

图示：我拿了一张半黄半白的纸放在摄像头前，并用文本提示告诉模型寻找"yellow paper"。YOLOE准确理解了这个描述，只将纸张的黄色部分进行了分割并用边界框标记，完全忽略了白色部分。这展示了YOLOE通过自然语言进行精细物体识别的能力。

**工作原理**：模型将文本提示编码为特征向量，然后与图像特征进行匹配，识别出与文本描述最对应的区域。这种方法允许您动态指定检测目标，无需重新训练模型。

以下代码演示了如何使用文本提示检测特定物体：

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_text.py

.. code-block:: python

   from ultralytics import YOLOE
   from picamera2 import Picamera2
   import cv2

   # load YOLOE model
   model = YOLOE("yoloe-26n-seg.pt")  # nano version

   # set the classes to detect (text prompt)
   names = ["yellow paper", "red cup", "person wearing glasses"]
   model.set_classes(names, model.get_text_pe(names))

   # initialize the camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLOE running with text prompts, press 'q' to exit...")
   print(f"Detecting: {', '.join(names)}")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, conf=0.3)  # set confidence threshold to 0.3
      annotated = results[0].plot()
      cv2.imshow("YOLOE on Raspberry Pi", annotated)

      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**文本提示模式的特点**：

* **动态检测**：随时修改检测目标，无需重新训练
* **自然语言**：用日常用语描述物体，如"蓝色汽车"、"木椅子"
* **多目标检测**：一次指定多个检测目标
* **精细控制**：描述颜色、材质、形状等属性
* **置信度阈值**：通过 ``conf``\ 参数控制检测灵敏度

高级用法
-------------------------------------

**动态切换检测目标**

您可以在运行时修改文本提示，无需重启程序：

.. code-block:: python

   # Initialize model
   model = YOLOE("yoloe-26n-seg.pt")

   # Initial detection targets
   current_names = ["red apple"]
   model.set_classes(current_names, model.get_text_pe(current_names))

   while True:
      frame = picam2.capture_array()

      # Check if detection target needs to be switched
      key = cv2.waitKey(1) & 0xFF
      if key == ord('1'):
         current_names = ["banana"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: banana")
      elif key == ord('2'):
         current_names = ["orange"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: orange")

      results = model.predict(frame, conf=0.3)
      annotated = results[0].plot()
      cv2.imshow("YOLOE", annotated)

      if key == ord('q'):
         break

**使用更复杂的文本描述**

YOLOE支持复杂的自然语言描述，以实现更精确的物体定位：

.. code-block:: python

   # More precise description examples
   names = [
       "person wearing a red hat",
       "car with open door",
       "small dog on the left side",
       "yellow paper on the desk"
   ]
   model.set_classes(names, model.get_text_pe(names))

**调整检测参数**

Raspberry Pi上的性能优化：

.. code-block:: python

   # Performance optimization configuration
   results = model.predict(
       frame,
       imgsz=224,        # Lower resolution for faster speed
       conf=0.4,         # Higher confidence threshold reduces false positives
       iou=0.5,          # Adjust IOU threshold
       verbose=False     # Disable verbose output
   )

性能优化技巧
-------------------------------------------------

在Raspberry Pi上运行YOLOE时，以下优化可以帮助获得更好的性能：

1. **选择合适的模型**：

   - ``yoloe-26n-seg.pt``：Nano版本，速度最快
   - ``yoloe-11s-seg-pf.pt``：S版本，精度更高但较慢

2. **降低输入分辨率**：

   - ``imgsz=224``：最快速度
   - ``imgsz=320``：平衡选择（推荐）
   - ``imgsz=416``：更高精度

3. **调整置信度阈值**：

   - 提高 ``conf``\ 参数（例如到0.5）可减少检测数量，提高速度

4. **减少检测类别**：

   - 在文本提示模式下，限制 ``names``\ 列表的长度可以提高推理速度

常见问题
-------------------------

**问：YOLOE和传统YOLO有什么区别？**

答：传统YOLO只能检测训练时定义的固定类别，而YOLOE可以通过文本提示检测任意物体，无需重新训练。

**问：无提示模式能检测所有物体吗？**

答：无提示模式检测图像中视觉上显著的物体，但不提供类别标签，适合快速浏览场景。

**问：文本提示支持中文吗？**

答：建议使用英文提示以获得最佳效果，因为模型主要基于英文数据训练。

**问：在Raspberry Pi上运行YOLOE的速度如何？**

答：在Raspberry Pi 5上，使用nano模型和320分辨率，可以实现3-5 FPS的实时性能。

**问：可以同时使用多个文本提示吗？**

答：可以，只需将多个描述添加到 ``names``\ 列表中，模型将同时检测所有这些物体。