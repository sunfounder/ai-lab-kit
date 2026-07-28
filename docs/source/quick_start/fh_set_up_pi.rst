.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _setup_pi_fusion_kit:

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi
   :end-before: end_setup_pi

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_screen
   :end-before: end_setup_pi_screen

.. .. include:: /_shared/pi_start/set_up_pi.rst
..    :start-after: start_setup_pi_headless
..    :end-before: end_setup_pi_headless

----------------------------------
无屏幕模式（Headless）
----------------------------------

如果没有显示器，您可以通过远程方式配置和登录 Raspberry Pi。
这是对大多数用户来说最便捷的方法。

**所需组件**

* Raspberry Pi
* 官方电源适配器
* MicroSD 卡
* 同一网络下的电脑

**提示**

* 请确保 Raspberry Pi 和您的电脑处于同一局域网中。
* 为了获得最佳稳定性，建议使用有线网络连接。


**通过 SSH 连接**

#. 在电脑上打开终端（Windows：**PowerShell**\ ；macOS/Linux：**终端**\ ），连接到您的 Raspberry Pi：

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: 在 AI Fusion Lab Kit 操作系统中，默认用户名为 ``pi``\ ，密码为 ``123456``\ 。默认主机名为 ``ai-fusion``\ 。

2. 或者，从路由器的 DHCP 列表中查找 Pi 的 IP 地址，然后使用以下命令连接：

   .. code-block:: bash

      ssh pi@<IP address>
      # 示例：
      ssh pi@192.168.1.42

3. 首次登录时，输入 ``yes`` 确认 SSH 证书。

4. 输入您在 Raspberry Pi Imager 中配置的密码。
   （输入时不会显示任何内容——这是正常现象。）

5. 登录后，您现在拥有完整的命令行访问权限。

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center



.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop
