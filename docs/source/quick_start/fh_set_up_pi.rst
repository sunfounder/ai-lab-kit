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

--------------------------------------------------
画面がない場合（ヘッドレス）
--------------------------------------------------

モニターがなくても、Raspberry Piをリモートで設定し、リモートログインできます。
これはほとんどのユーザーにとって最も便利な方法です。

**必要なコンポーネント**

* Raspberry Pi
* 公式電源アダプター
* MicroSDカード
* 同じネットワーク上のコンピューター

**注意事項**

* Raspberry Piとコンピューターが同じローカルネットワーク上にあることを確認してください。
* 安定性を最大限にするため、可能であれば有線イーサネット接続を使用してください。

**SSHによる接続**

#. コンピューターでターミナルを開き（Windows: **PowerShell**、macOS/Linux: **ターミナル**）、Raspberry Piに接続します：

   .. code-block:: bash

      ssh pi@ai-fusion.local

   .. note:: AI Fusion Lab Kitのオペレーティングシステムでは、デフォルトのユーザー名は ``pi``、デフォルトのパスワードは ``123456`` です。デフォルトのホスト名は ``ai-fusion`` です。

2. または、ルーターのDHCPリストからPiのIPアドレスを確認し、次のように接続することもできます：

   .. code-block:: bash

      ssh pi@<IPアドレス>
      # 例：
      ssh pi@192.168.1.42

3. 初回ログイン時に ``yes`` と入力してSSH証明書を確認します。

4. Raspberry Pi Imagerで設定したパスワードを入力します。
   （入力中は何も表示されませんが、これで正常です。）

5. ログイン後、コマンドラインへの完全なアクセスが可能になります。

   .. .. image:: /_shared/pi_start/img/ssh_login.png
   ..    :align: center

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_troubleshooting
   :end-before: end_setup_pi_troubleshooting

.. include:: /_shared/pi_start/set_up_pi.rst
   :start-after: start_setup_pi_remote_desktop
   :end-before: end_setup_pi_remote_desktop