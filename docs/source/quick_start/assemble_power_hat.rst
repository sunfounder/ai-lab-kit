.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _assemble_hat:


.. start_assemble_hat

Fusion HAT+ の組み立てと電源投入（重要）
=======================================================

Fusion HAT+ を Raspberry Pi に接続する
----------------------------------------

ここでは、Fusion HAT+ の組み立て方法を説明します。

#. ベースを組み立てます。
#. バッテリーをベースに貼り付けます。
#. スタンドオフを使用して Raspberry Pi を固定します。
#. FPC ケーブルを Raspberry Pi に接続します。（パン・チルトを組み立てる際に、カメラモジュールと一緒に取り付けます。）
#. Fusion HAT+ を Raspberry Pi の 40 ピンコネクタに差し込みます。
#. **バッテリーを挿入します。** （これは非常に重要です。バッテリーを挿入しないと、Fusion HAT+ は動作しません。）


組み立ての詳細については、以下の動画をご覧ください。

.. raw:: html

  <iframe width="100%" 
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/HlAayd1mSxU?si=oZnKyZihyyjQhsHl" 
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
    </iframe>



充電
-------------------

初めて使用する前に、バッテリーを完全に充電することを推奨します。付属の USB Type-C 充電ケーブル、またはお手持ちの USB-C 充電器を使用できます。

.. note::

  Amazon の航空輸送規定により、出荷時のバッテリー残量は 30% 未満になっている場合があります。過放電や損傷を防ぐため、使用前に **必ず** 完全に充電してください。  
  USB-C ケーブルを Fusion HAT+ に接続すると、自動的にバッテリーの充電が開始されます。Raspberry Pi に別途電源を接続する必要はありません。

* **5V 3A の電源アダプター** （例：Raspberry Pi 公式 15W アダプター）の使用を推奨します。  
* **USB-C PD（Power Delivery）充電器** や **QC 2.0 急速充電器** も使用できます。  
* 0% から満充電までは通常 **約 2 時間** かかります。

.. image:: img/power_charge.jpg
   :width: 400
   :align: center

Fusion HAT+ には **2 つのバッテリーインジケーター LED** があり、バッテリー電圧レベルを表示します。

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED 状態
     - バッテリー電圧
   * - LED 2 個点灯
     - > 7.4V
   * - LED 1 個点灯
     - < 7.4V
   * - 両方の LED 消灯
     - < 6.5V

充電中は、LED の 1 つが点滅して充電の進行状況を示します。

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - LED 状態
     - バッテリー電圧
   * - LED 1 個点灯、もう 1 個点滅
     - > 7.4V
   * - LED 1 個のみ点滅
     - < 7.4V


満充電になると：

* **Fusion HAT+ が ON の場合**、2 つの LED は点灯したままになります。  
* **Fusion HAT+ が OFF の場合**、2 つの LED は消灯します。

.. note::

   長時間のプログラミングやデバッグを行う場合は、USB-C ケーブルを接続したまま使用することで、  
   バッテリーを充電しながら Fusion HAT+ を動作させることができます。  
   充電器を接続した状態で Fusion HAT+ を動作させる場合でも、バッテリーを **取り外すことはできません**。

電源を入れる
----------------------

バッテリーが十分に充電されている状態で、Fusion HAT+ の **電源ボタン** を短く押します。

* **PWR LED** が点灯します。  
* **バッテリー LED** も点灯します。  
* Raspberry Pi は自動的に起動します。

.. image:: img/power_button.jpg
    :width: 400


.. end_assemble_hat

.. _assemble_fusion_hat_pan_tilt:

パン・チルトの組み立て（カメラ用）
------------------------------------------------------

カメラモジュールをより使いやすくするために、パン・チルト機構を組み立てることができます。

.. note:: 
  
  パン・チルトを組み立てると一部のピンが隠れる場合があります。そのため、カメラを使用する場合のみ組み立てるか、組み立て後に外側へ配置することを推奨します。


.. image:: img/gimbal_assemble.png

組み立ての詳細については、以下の動画をご覧ください。

.. raw:: html

  <iframe width="100%" 
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/mDCNKVzNLkg?si=2gYJ1feopWgglekR" 
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
    </iframe>