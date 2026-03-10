.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _tts_espeak_pico2wave:

1. Espeak と Pico2Wave による TTS
=================================================

このレッスンでは、Raspberry Pi に標準搭載されている 2 つの text-to-speech（TTS）エンジン、 **Espeak** と **Pico2Wave** を使って、Fusion HAT+ に音声を出力させます。  

この 2 つのエンジンはどちらもシンプルでオフライン動作に対応していますが、音声の特徴はかなり異なります：

* **Espeak**: 非常に軽量で高速ですが、声は機械的です。速度、ピッチ、音量などを調整できます。  
* **Pico2Wave**: Espeak よりも滑らかで自然な音声を生成しますが、設定できる項目は少なめです。  

このレッスンでは、 **音声品質** と **機能の違い** を実際に聞き比べることができます。  

----

1. Espeak のテスト
--------------------

Espeak は Raspberry Pi OS に含まれている軽量な TTS エンジンです。  
音声はやや機械的ですが、音量、ピッチ、速度などを細かく調整できるのが特長です。  

**プログラムを実行する**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_espeak.py

  * Fusion HAT+ から “Hello! I'm Espeak TTS.” と聞こえるはずです。
  * コード内の調整パラメータを変更して、 ``amp`` 、 ``speed`` 、 ``gap`` 、 ``pitch`` が音声にどう影響するか試してみてください。

**コード**

.. code-block:: python
  
  from fusion_hat.tts import Espeak

  # Create Espeak TTS instance
  tts = Espeak()
  # Set amplitude 0-200, default 100
  tts.set_amp(200)
  # Set speed 80-260, default 150
  tts.set_speed(150)
  # Set gap 0-200, default 1
  tts.set_gap(1)
  # Set pitch 0-99, default 80
  tts.set_pitch(80)

  tts.say("Hello! I’m Espeak TTS.")

**コードの説明：**

* ``tts.set_amp()`` — 音量を設定します（0～200）。  
* ``tts.set_speed()`` — 読み上げ速度を調整します（80～260）。  
* ``tts.set_gap()`` — 単語間の間隔を設定します（0～200）。  
* ``tts.set_pitch()`` — ピッチを設定します（0～99）。  
* ``tts.say()`` — テキストを音声に変換して再生します。

💡 **ヒント：** ピッチと速度を上げると明るく元気なロボット音声になり、下げると落ち着いた真面目な印象になります。

----


2. Pico2Wave のテスト
------------------------

Pico2Wave は、Espeak と比べて **より自然で人間らしい音声** を生成します。  
使い方はとても簡単ですが、柔軟性は低く、 **変更できるのは言語だけ** で、ピッチ、速度、音量は調整できません。  
そのため、細かな設定を行わずに、聞き取りやすく滑らかな音声を使いたい場合に適しています。

**プログラムを実行する**

  .. code-block:: bash
  
      cd ~/ai-lab-kit/llm
      sudo python3 tts_pico2wave.py

* Fusion HAT+ から “Hello! I'm Pico2Wave TTS.” と聞こえるはずです。  
* 言語を変更して（たとえばスペイン語なら ``es-ES``）、音声の違いを聞いてみてください。  

**コード**

.. code-block:: python

  from fusion_hat.tts import Pico2Wave

  # Create Pico2Wave TTS instance
  tts = Pico2Wave()

  # Set the language
  tts.set_lang('en-US')  # en-US, en-GB, de-DE, es-ES, fr-FR, it-IT
  
  # Quick hello (sanity check)
  tts.say("Hello! I'm Pico2Wave TTS.")

**コードの説明：**

* ``tts.set_lang()`` — 音声合成の出力言語を設定します。

  - ``en-US`` （デフォルト）
  - ``en-GB``
  - ``de-DE``
  - ``es-ES``
  - ``fr-FR``
  - ``it-IT``

* ``tts.say()`` — テキストを音声に変換し、すぐに再生します。  


----

トラブルシューティング
-------------------------

* **Espeak または Pico2Wave を実行しても音が出ない**

  * スピーカーまたはヘッドホンが正しく接続されていて、音量がミュートになっていないか確認してください。  
  * ターミナルで次の簡単なテストを実行してください：

    .. code-block:: bash

       espeak "Hello world"
       pico2wave -w test.wav "Hello world" && aplay test.wav

  何も聞こえない場合は、問題は Python コードではなく音声出力側にあります。

* **Espeak の声が速すぎる、または機械的すぎる**

  * コード内のパラメータを調整してみてください：

    .. code-block:: python

       tts.set_speed(120)   # slower
       tts.set_pitch(60)    # different pitch

* **コード実行時に Permission denied が出る**

  * ``sudo`` を付けて実行してみてください：

    .. code-block:: bash

       sudo python3 test_tts_espeak.py

比較：Espeak と Pico2Wave
-------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Feature
     - Espeak
     - Pico2Wave
   * - Voice quality
     - 機械的、合成音声らしい
     - より自然で人間らしい
   * - Languages
     - 標準では英語
     - 少なめだが主要言語に対応
   * - Adjustable
     - あり（速度、ピッチなど）
     - なし（言語のみ）
   * - Performance
     - 非常に高速で軽量
     - やや遅めで少し重い

