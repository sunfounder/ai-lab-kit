.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _assemble_hat:

.. start_assemble_hat

组装并启动 Fusion HAT+（重要）
=======================================================

将 Fusion HAT+ 连接到 Raspberry Pi
----------------------------------------

在这里，我们将教您如何组装 Fusion HAT+。

#. 组装底座。
#. 将电池粘贴到底座上。
#. 使用铜柱固定 Raspberry Pi。
#. 将 FPC 排线连接到 Raspberry Pi。（组装云台时，我们会一起安装排线和摄像头模块。）
#. 将 Fusion HAT+ 插入 Raspberry Pi 的 40 针连接器。
#. **插入电池。**\ （这非常重要。如果不插入电池，Fusion HAT+ 将无法工作。）

有关组装的详细信息，请观看下面的视频。

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/HlAayd1mSxU?si=oZnKyZihyyjQhsHl"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>



充电
-------------------

首次使用前，建议将电池充满电。您可以使用附带的 USB Type-C 充电线或自己的 USB-C 充电器。

.. note::

   电池在到货时电量可能较低，因为亚马逊要求电池在空运前电量低于 30%。在使用前，您\ **必须**\ 将其充满电，以防止过度放电造成损坏。
   将 USB-C 插入 Fusion HAT+，电池将自动开始充电。您无需连接 Raspberry Pi 的电源。

* 我们建议使用 **5V 3A 电源适配器**\ ，例如官方 Raspberry Pi 15W 适配器。
* 您也可以使用 **USB-C PD（Power Delivery）充电器** 或 **QC 2.0 快速充电器**\ 。
* 从 0% 充满通常需要约 **2 小时**\ 。

.. image:: img/power_charge.jpg
   :width: 400
   :align: center

Fusion HAT+ 包含 **两个电池指示灯 LED**\ ，用于显示电池电压水平：

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED 状态
     - 电池电压
   * - 2 个 LED 亮
     - > 7.4V
   * - 1 个 LED 亮
     - < 7.4V
   * - 两个 LED 均灭
     - < 6.5V

充电时，其中一个 LED 会闪烁以指示充电进度：

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED 状态
     - 电池电压
   * - 1 个 LED 亮，1 个 LED 闪烁
     - > 7.4V
   * - 仅 1 个 LED 闪烁
     - < 7.4V


充满电后：

* **如果 Fusion HAT+ 处于开机状态**\ ，两个 LED 将保持常亮。
* **如果 Fusion HAT+ 处于关机状态**\ ，两个 LED 都将熄灭。

.. note::

   在进行长时间的编程或调试时，您可以通过连接 USB-C 线缆让 Fusion HAT+ 保持供电，这样可以在充电的同时运行 Fusion HAT+。即使您在连接充电器的情况下运行 Fusion HAT+，**也不能**\ 取出电池。

开机
----------------------

当电池电量充足时，短按 Fusion HAT+ 上的 **电源按钮**\ 。

* **PWR LED** 将亮起。
* **电池 LED** 也将点亮。
* Raspberry Pi 将自动启动。

.. image:: img/power_button.jpg
    :width: 400

.. end_assemble_hat



.. _assemble_fusion_hat_pan_tilt:

组装云台（用于摄像头）
------------------------------------------------------

为了方便使用摄像头模块，您可以组装一个云台。

.. note::

   组装云台可能会遮挡部分引脚，因此建议仅在使用摄像头时组装，或者组装后将其放置在外部。


.. image:: img/gimbal_assemble.png

有关组装的详细信息，请观看下面的视频。

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/7CkGPKnbjM4"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>
