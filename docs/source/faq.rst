.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

よくある質問（FAQ）
=====================


以下は、AI Fusion Lab Kit を使用する際によく寄せられる質問です。  
ここに記載されていない問題については、各章のトラブルシューティングを参照するか、サポートまでお問い合わせください。


一般的な質問
-----------------

**システムイメージはどこでダウンロードできますか？**

    推奨される Raspberry Pi システムイメージおよびセットアップ手順は  
    :ref:`get_start` セクションで確認できます。  
    ドキュメントには、初心者向けのステップバイステップのインストールガイドも掲載されています。

**キットを使用するためにインターネット接続は必要ですか？**

    基本的な Python およびハードウェアのサンプルは、インターネット接続がなくても実行できます。  
    ただし、クラウドベースの LLM や一部の AI 機能を使用する場合は、インターネット接続が必要です。

**どの Raspberry Pi モデルがサポートされていますか？**

    本キットは **Raspberry Pi 4B** および **Raspberry Pi 5** を公式にサポートしています。  
    その他のモデルでも動作する場合がありますが、性能や互換性の制限により保証はされません。

**FusionHAT に別途電源は必要ですか？**

    はい。 *FusionHAT は専用の電源供給が必要です* 。  
    Raspberry Pi の電源入力から FusionHAT に電力は供給されません。  
    FusionHAT に電源が供給されていない場合、スピーカーなどのオンボードモジュールを含む一部の機能が正常に動作しない可能性があります。




ソフトウェア / インストール
----------------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    この問題は、システムにインストールされている ``RPi.GPIO`` ライブラリと  
    Fusion HAT が使用する GPIO ライブラリとの競合によって発生することが多いです。  
    以下の手順でシステムの ``RPi.GPIO`` パッケージを削除してから、再度プログラムを実行してください。

    1. システムの ``RPi.GPIO`` ファイルを削除します：

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Raspberry Pi を再起動します：

       .. code-block:: bash

          sudo reboot

    3. 再度サンプルを実行します（必要な場合を除き sudo は使用しないでください）：

 ``RPi.GPIO`` の競合ファイルを削除すると、割り込みベースのボタン例は正常に動作するようになります。


**インストールスクリプトが失敗しました。どうすればよいですか？**

    Raspberry Pi OS が最新の状態であること、およびインストール中に安定したネットワーク接続があることを確認してください。  
    セットアップスクリプトをもう一度実行してみてください。  
    問題が解決しない場合は、システムを再起動し、Python のバージョンを再確認してください。

**Python のサンプルが実行できません。原因は何ですか？**

    多くの場合、Python ライブラリが不足しているか、環境設定が正しくないことが原因です。  
    :ref:`get_start` のセットアップガイドに従って依存関係がインストールされているか確認してください。

**カメラが認識されません。**

    リボンケーブルが正しく接続されているか、逆向きに挿入されていないか確認してください。  
    また、Raspberry Pi の設定でカメラインターフェースが有効になっていることを確認してください。



AI 機能
-----------

**LLM の応答が遅い、または返ってこない。**

    インターネット接続が不安定であるか、使用しているモデルプロバイダーの API 制限に達している可能性があります。  
    ネットワークを変更するか、別のモデルで試してみてください。

**Speech-to-Text (STT) の精度が低い。**

    マイクの接続を確認し、周囲のノイズを減らしてください。  
    一部のモデルでは、追加の言語パックや設定の調整が必要な場合があります。

**Vosk STT モジュールで 'Error querying device -1' が表示される。**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    音声設定を再構成するために、次のコマンドを実行してください： ``sudo /opt/setup_fusion_hat_audio.sh``

**TTS/STT使用時のアクセス拒否エラーについて**

    TTS（Text-to-Speech）またはSTT（Speech-to-Text）コマンドを実行すると、以下のような権限エラーが発生する場合があります：

    .. code-block:: bash

        Traceback (most recent call last):
            File "/home/pi/ai-lab-kit/llm/tts_piper.py", line 3, in <module>
                tts = Piper()
                    ^^^^^^^
            File "/usr/local/lib/python3.11/dist-packages/fusion_hat/tts.py", line 125, in _piper_init_with_speaker
                _original_piper_init(self, *args, **kwargs)
            File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/tts/piper.py", line 30, in __init__
                os.makedirs(PIPER_MODEL_DIR, 0o777)
            File "<frozen os>", line 225, in makedirs
        PermissionError: [Errno 13] Permission denied: '/opt/piper_models'

    この問題は、AI Fusion Lab Kit OS バージョン 0.0.1 で発生します。システムはルート権限を必要とするディレクトリ（/opt/piper_models）を作成しようとしますが、現在のユーザーに十分な権限がありません。以下のコマンドを実行して、AI Fusion Lab Kit OSをバージョン 0.0.1 から 0.1.0 にアップグレードしてください：

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash


コンピュータビジョン / MediaPipe
----------------------------------

**OpenCV のサンプルでカメラアクセス時にエラーが表示される。**

    カメラは同時に 1 つのプロセスのみが使用できます。  
    バックグラウンドで他のカメラアプリケーションが動作していないか確認してください。

**MediaPipe のサンプルの動作が遅い。**

    リアルタイムのコンピュータビジョン処理には高い処理能力が必要です。  
    入力解像度を下げるか、他のプロセスを終了してシステムリソースを確保してください。

**最新の Raspberry Pi OS で MediaPipe プロジェクトが動作しない。**

    MediaPipe は依存関係およびアーキテクチャの変更により、  
    最新の Raspberry Pi OS（Trixie）を現在サポートしていません。  
    MediaPipe を使用する例では、**Legacy バージョン（Bookworm）** を使用してください。


ハードウェアの問題
--------------------

**コンポーネントが反応しません。**

    配線が正しいか、接続方向が正しいかを確認してください。  
    ピンの説明や接続図については :ref:`cpn_list` を参照してください。

**デバイスが突然動作しなくなりました。**

    電源の不安定が原因の可能性があります。  
    使用している Raspberry Pi モデルに推奨されている電源仕様を満たしているか確認してください。

サポートについて
-------------------

**追加のサポートを受けるには？**

    まずはドキュメントのトラブルシューティング手順をご確認ください。  
    ご質問がある場合は、 **service@sunfounder.com** までお気軽にお問い合わせください。サポートチームが対応いたします。
