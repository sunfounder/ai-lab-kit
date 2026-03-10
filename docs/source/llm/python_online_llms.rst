.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. オンラインLLMへの接続
================================

このレッスンでは、Fusion HAT+（または Raspberry Pi）を、さまざまな **オンライン大規模言語モデル（LLM）** に接続する方法を学びます。  
各プロバイダーは API キーが必要で、選択できるモデルもそれぞれ異なります。  

ここでは次の内容を扱います：

* API キーを安全に作成し、保存する方法
* 目的に合ったモデルの選び方
* サンプルコードを実行してモデルとチャットする方法

各プロバイダーごとに、手順を順番に確認していきましょう。

----

OpenAI
----------

OpenAI は **GPT-4o** や **GPT-4.1** などの強力なモデルを提供しており、テキスト処理だけでなくビジョンタスクにも利用できます。  

設定手順は以下の通りです：

.. start_setup_openai

**APIキーの取得と保存**

#. |link_openai_platform| にアクセスしてログインします。 **API keys** ページで **Create new secret key** をクリックします。

   .. image:: img/llm_openai_create.png

#. 必要事項（Owner、Name、Project、必要に応じて権限）を入力し、 **Create secret key** をクリックします。

   .. image:: img/llm_openai_create_confirm.png

#. キーが作成されたら、すぐにコピーしてください。後から再表示できません。紛失した場合は新しく作成し直す必要があります。

   .. image:: img/llm_openai_copy.png

#. プロジェクトフォルダ（例： ``/`` ）内に ``secret.py`` というファイルを作成します：

   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. ファイルにキーを次のように貼り付けます：

   .. code-block:: python
   
       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**請求設定の有効化と利用可能モデルの確認**

#. キーを使用する前に、OpenAI アカウントの **Billing** ページで支払い情報を追加し、少額のクレジットをチャージしてください。  

   .. image:: img/llm_openai_billing.png

#. 続いて **Limits** ページで、アカウントで利用可能なモデルを確認し、コードで使用する正確なモデルIDをコピーします。  

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**サンプルコードで動作確認**

#. サンプルコードを開きます：

   .. code-block:: bash
   
       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``gpt-4o`` ）に変更します：

   .. code-block:: python
   
      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )
  
   保存して終了します（ ``Ctrl+X`` → ``Y`` → ``Enter`` ）。  

#. 最後にテストを実行します：

   .. code-block:: bash
   
       sudo python3 llm_test.py
   
これでターミナルから Fusion HAT+ と直接チャットできます。

----

Gemini
------------------

Gemini は Google の AI モデルファミリーです。高速で、汎用的な用途に適しています。  

**APIキーの取得と保存**

#. |link_google_ai| にログインし、API Keys ページへ移動します。

   .. image:: img/llm_gemini_get.png

#. 右上の **Create API key** ボタンをクリックします。

   .. image:: img/llm_gemini_create.png

#. 既存プロジェクト用、または新規プロジェクト用としてキーを作成できます。

   .. image:: img/llm_gemini_choose.png

#. 生成された API キーをコピーします。

   .. image:: img/llm_gemini_copy.png

#. プロジェクトフォルダで：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. キーを貼り付けます：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**利用可能モデルの確認**

公式の |link_gemini_model| ページを開くと、モデル一覧、正確な API ID、最適化された用途などを確認できます。

   .. image:: img/llm_gemini_model.png

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``gemini-2.5-flash`` ）に変更します：

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. 保存して実行します：

   .. code-block:: bash

       sudo python3 llm_test.py

これでターミナルから Fusion HAT+ と直接チャットできます。

----

Qwen
------------------

Qwen は Alibaba Cloud が提供する大規模言語／マルチモーダルモデルのファミリーです。  
テキスト生成、推論、画像解析などのマルチモーダル理解に対応しています。

**APIキーの取得**

Qwen モデルを呼び出すには **API Key** が必要です。  
海外ユーザーの多くは **DashScope International（Model Studio）** コンソールを利用してください。  
中国本土のユーザーは代わりに **Bailian（百炼）** コンソールを利用できます。

* **海外ユーザー向け**

  #. Alibaba Cloud の公式 |link_qwen_inter| ページへアクセスします。  
  #. **Alibaba Cloud** アカウントでサインイン、または新規作成します。  
  #. **Model Studio** に移動します（Singapore または Beijing リージョンを選択）。  
     
      * ページ上部に「Activate Now」の表示がある場合はクリックして有効化し、無料枠を受け取ります（Singapore のみ）。  
      * 有効化は無料で、無料枠を使い切った後にのみ課金されます。  
      * 有効化の案内が表示されない場合、すでにサービスは有効です。 
  
  #. **Key Management** ページへ移動します。 **API Key** タブで **Create API Key** をクリックします。  
  #. 作成後、API Key をコピーして安全に保管します。  
   
    .. image:: img/llm_qwen_api_key.png
        :width: 800
  
  .. note::
     香港・マカオ・台湾のユーザーも **International（Model Studio）** を選択してください。
  
* **中国本土ユーザー向け**

  中国本土の場合は **Alibaba Cloud Bailian（百炼）** コンソールを利用できます：
  
  #. |link_aliyun| （百炼コンソール）にログインし、アカウント認証を完了します。  
  #. **Create API Key** を選択します。モデルサービス未開通の案内が出た場合は **Activate** をクリックし、規約に同意して無料枠を受け取ります。有効化後に **Create API Key** ボタンが利用可能になります。  
   
     .. image:: img/llm_qwen_aliyun_create.png
  
  #. 再度 **Create API Key** をクリックし、アカウントを確認して **Confirm** をクリックします。  
   
     .. image:: img/llm_qwen_aliyun_confirm.png
  
  #. 作成後、API Key をコピーします。  
   
     .. image:: img/llm_qwen_aliyun_copy.png

**APIキーの保存**

#. プロジェクトフォルダで：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 次のようにキーを貼り付けます：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
        
        QWEN_API_KEY = "sk-xxx"

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``qwen-plus`` ）に変更します：

   .. code-block:: python
   
      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model="qwen-plus",
      )

#. 次のコマンドで実行します：

   .. code-block:: bash
   
       sudo python3 llm_test.py

これでターミナルから Fusion HAT+ と直接チャットできます。

Grok (xAI)
------------------
Grok は xAI が提供する会話型AIで、Elon Musk のチームによって開発されています。xAI API を通じて接続できます。

**APIキーの取得と保存**

#. |link_grok_ai| でアカウント登録を行います。事前にクレジットを追加してください。クレジットがない場合、API は動作しません。

#. API Keys ページへ移動し、 **Create API key** をクリックします。  

   .. image:: img/llm_grok_create.png

#. キーの名前を入力し、 **Create API key** をクリックします。 

   .. image:: img/llm_grok_name.png

#. 生成されたキーをコピーして安全に保管します。 

   .. image:: img/llm_grok_copy.png

#. プロジェクトフォルダで：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 次のようにキーを貼り付けます：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
        
        GROK_API_KEY = "xai-xxx"

**利用可能モデルの確認**

xAI コンソールの Models ページで、チームで利用可能なモデル一覧と正確な API ID を確認できます。これらの ID をコードで使用します。

   .. image:: img/llm_grok_model.png

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``grok-4-latest``）に変更します：

   .. code-block:: python
   
      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. 次のコマンドで実行します：

   .. code-block:: bash
   
       sudo python3 llm_test.py

これでターミナルから Fusion HAT+ と直接チャットできます。

----

DeepSeek
------------------

DeepSeek は中国の LLM プロバイダーで、手頃な価格で実用的なモデルを提供しています。  

**APIキーの取得と保存**

#. |link_deepseek| にログインします。 

#. 右上メニューから **API Keys → Create API Key** を選択します。 

   .. image:: img/llm_deepseek_create.png

#. 名前を入力して **Create** をクリックし、キーをコピーします。

   .. image:: img/llm_deepseek_copy.png

#. プロジェクトフォルダで：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. キーを追加します：

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**課金の有効化**

まずアカウントへのチャージが必要です。少額（例：10元程度）から始めるのがおすすめです。 

   .. image:: img/llm_deepseek_chognzhi.png

**利用可能モデル**

執筆時点（2025-09-12）で、DeepSeek が提供しているモデルは次の通りです：  

* ``deepseek-chat``  
* ``deepseek-reasoner``  

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``deepseek-chat`` ）に変更します：

   .. code-block:: python
   
      from fusion_hat.llm import Deepseek
      from secret import DEEPSEEK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Deepseek(
         api_key=DEEPSEEK_API_KEY,
         model="deepseek-chat",
         max_messages=20,
      )

#. 実行します：

   .. code-block:: bash
   
       sudo python3 llm_test.py

これでターミナルから Fusion HAT+ と直接チャットできます。

----

Doubao
------------------
Doubao は ByteDance の AI モデルプラットフォーム（Volcengine Ark）です。  

**APIキーの取得と保存**

#. |link_doubao| にログインします。

#. 左メニューを下にスクロールし、 **API Key Management → Create API Key** を選択します。 

   .. image:: img/llm_doubao_create.png

#. 名前を設定して **Create** をクリックします。  

   .. image:: img/llm_doubao_name.png

#. **Show API Key** アイコンをクリックしてコピーします。 

   .. image:: img/llm_doubao_copy.png

#. プロジェクトフォルダで：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. キーを追加します：

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**モデルの選択**

#. モデルマーケットプレイスに移動してモデルを選択します。  

   .. image:: img/llm_doubao_model_select.png

#. 例として **Doubao-seed-1.6** を選択し、 **API 接入** をクリックします。 

   .. image:: img/llm_doubao_model.png

#. API Key を選択し、 **Use API** をクリックします。 

   .. image:: img/llm_doubao_use_api.png

#. **Enable Model** をクリックします。 

   .. image:: img/llm_doubao_kaitong.png

#. モデルIDにカーソルを合わせてコピーします。 

   .. image:: img/llm_doubao_copy_id.png

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 下のコードに置き換え、 ``model="xxx"`` を使用したいモデル（例： ``doubao-seed-1-6-250615`` ）に変更します：

   .. code-block:: python
   
      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. 次のコマンドで実行します：

   .. code-block:: bash
   
       sudo python3 llm_test.py

これでターミナルから Fusion HAT+ と直接チャットできます。

General
--------------

このプロジェクトは、統一されたインターフェースを通じて複数の LLM プラットフォームへ接続できるように設計されています。  
標準で次のプラットフォームに対応しています：

* **OpenAI** （ChatGPT / GPT-4o、GPT-4、GPT-3.5）  
* **Gemini** （Google AI Studio / Vertex AI）  
* **Grok**  （xAI）  
* **DeepSeek**  
* **Qwen（通义千问）**  
* **Doubao（豆包）**  

さらに、 **OpenAI API 互換フォーマット** に対応した **他の任意の LLM サービス** にも接続できます。  
その場合は、該当プラットフォームの **API Key** と正しい **base_url** を手動で用意してください。

**APIキーの取得と保存**

#. 利用したいプラットフォームから **API Key** を取得します（詳細は各社の公式コンソールを参照してください）。  

#. プロジェクトフォルダで新しいファイルを作成します：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. ``secret.py`` にキーを追加します：

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   API Key は必ず非公開にしてください。 ``secret.py`` を公開リポジトリへアップロードしないでください。

**サンプルコードで動作確認**

#. テストファイルを開きます：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. 以下の例に置き換え、プラットフォームに合わせて正しい ``base_url`` と ``model`` を入力します：

   .. note::

      ``base_url`` について：  
      本プロジェクトは **OpenAI API 形式** 、およびそれと **互換** のある API をサポートします。  
      ``base_url`` はプロバイダーごとに異なるため、各社ドキュメントを確認してください。  

   .. code-block:: python

      from fusion_hat.llm import LLM
      from secret import API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = LLM(
         base_url = f"",
         api_key=API_KEY,
         model="",
      )

#. プログラムを実行します：

   .. code-block:: bash

      sudo python3 llm_others.py



