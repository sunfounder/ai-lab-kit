.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _py_online_llm:

5. 连接在线大语言模型
=========================

在本课中，我们将学习如何将你的 Fusion HAT+（或树莓派）连接到不同的\ **在线大语言模型（LLM）**。
每个提供商都需要 API 密钥，并提供不同的模型供你选择。

我们将介绍如何：

* 安全地创建和保存你的 API 密钥。
* 选择适合你需求的模型。
* 运行我们的示例代码与模型聊天。

让我们逐个提供商逐步进行。

----

OpenAI
----------

OpenAI 提供强大的模型，如 **GPT-4o** 和 **GPT-4.1**，可用于文本和视觉任务。

以下是设置方法：

.. start_setup_openai

**获取并保存你的 API 密钥**

#. 前往 |link_openai_platform| 并登录。在 **API keys** 页面，点击 **Create new secret key**。

   .. image:: img/llm_openai_create.png

#. 填写详细信息（所有者、名称、项目及权限，如有需要），然后点击 **Create secret key**。

   .. image:: img/llm_openai_create_confirm.png

#. 密钥创建后，立即复制——你将无法再次看到它。如果丢失，你需要生成一个新的。

   .. image:: img/llm_openai_copy.png

#. 在你的项目文件夹中（例如：\ ``/``），创建一个名为 ``secret.py``\ 的文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 将你的密钥粘贴到文件中，如下所示：

   .. code-block:: python

       # secret.py
       # Store secrets here. Never commit this file to Git.
       OPENAI_API_KEY = "sk-xxx"

**启用计费并查看模型**

#. 在使用密钥之前，请前往 OpenAI 账户的 **Billing** 页面，添加付款信息并充值少量额度。

   .. image:: img/llm_openai_billing.png

#. 然后进入 **Limits** 页面，查看你的账户可使用哪些模型，并复制准确的模型 ID 以在代码中使用。

   .. image:: img/llm_openai_models.png


.. end_setup_openai

**使用示例代码测试**

#. 打开我们的示例代码：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``gpt-4o``）：

   .. code-block:: python

      from fusion_hat.llm import OpenAI
      from secret import OPENAI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = OpenAI(
         api_key=OPENAI_API_KEY,
         model="gpt-4o",
      )

  保存并退出（\ ``Ctrl+X``\，然后 ``Y``\，再 ``Enter``）。

#. 最后，运行测试：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

----

Gemini
------------------

Gemini 是 Google 的 AI 模型系列。它速度快，非常适合通用任务。

**获取并保存你的 API 密钥**

#. 登录 |link_google_ai|，然后进入 API Keys 页面。

   .. image:: img/llm_gemini_get.png

#. 点击右上角的 **Create API key** 按钮。

   .. image:: img/llm_gemini_create.png

#. 你可以为现有项目或新项目创建密钥。

   .. image:: img/llm_gemini_choose.png

#. 复制生成的 API 密钥。

   .. image:: img/llm_gemini_copy.png

#. 在你的项目文件夹中：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 粘贴密钥：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.
       GEMINI_API_KEY = "AIxxx"

**查看可用模型**

前往官方 |link_gemini_model| 页面，你将看到模型列表、它们确切的 API ID 以及各自优化的用例。

   .. image:: img/llm_gemini_model.png

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``gemini-2.5-flash``）：

   .. code-block:: python

      from fusion_hat.llm import Gemini
      from secret import GEMINI_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Gemini(
         api_key=GEMINI_API_KEY,
         model="gemini-2.5-flash",
      )

#. 保存并运行：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

----

Qwen
------------------

Qwen 是阿里云提供的一系列大语言和多模态模型。
这些模型支持文本生成、推理和多模态理解（如图像分析）。

**获取 API 密钥**

要调用 Qwen 模型，你需要一个 **API 密钥**。
大多数国际用户应使用 **DashScope International（Model Studio）**\ 控制台。
中国大陆用户可以使用 **百炼（Bailian）**\ 控制台。

* **国际用户**

  #. 前往阿里云官方 |link_qwen_inter| 页面。
  #. 登录或创建一个 **Alibaba Cloud** 账户。
  #. 导航到 **Model Studio**\ （选择新加坡或北京区域）。

      * 如果页面顶部出现 "Activate Now" 提示，点击它以激活 Model Studio 并获得免费配额（仅限新加坡）。
      * 激活是免费的——只有在免费配额用完后才会收费。
      * 如果没有出现激活提示，说明服务已经激活。

  #. 进入 **Key Management** 页面。在 **API Key** 标签页，点击 **Create API Key**。
  #. 创建后，复制你的 API 密钥并妥善保管。

    .. image:: img/llm_qwen_api_key.png
        :width: 800

  .. note::
     香港、澳门和台湾的用户也应选择 **International（Model Studio）**\ 选项。

* **中国大陆用户**

  如果你在中国大陆，可以使用 **阿里云百炼（Bailian）**\ 控制台：

  #. 登录 |link_aliyun|\ （百炼控制台）并完成账户验证。
  #. 选择 **Create API Key**。如果提示模型服务未激活，点击 **Activate**，同意条款并领取免费配额。激活后，**Create API Key** 按钮将可用。

     .. image:: img/llm_qwen_aliyun_create.png

  #. 再次点击 **Create API Key**，检查你的账户，然后点击 **Confirm**。

     .. image:: img/llm_qwen_aliyun_confirm.png

  #. 创建后，复制你的 API 密钥。

     .. image:: img/llm_qwen_aliyun_copy.png

**保存你的 API 密钥**

#. 在你的项目文件夹中：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 像这样粘贴你的密钥：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        QWEN_API_KEY = "sk-xxx"

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``qwen-plus``）：

   .. code-block:: python

      from fusion_hat.llm import Qwen
      from secret import QWEN_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Qwen(
         api_key=QWEN_API_KEY,
         model="qwen-plus",
      )

#. 运行：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

Grok（xAI）
------------------
Grok 是 xAI 的对话式 AI，由 Elon Musk 的团队创建。你可以通过 xAI API 连接到它。

**获取并保存你的 API 密钥**

#. 在此处注册账户：|link_grok_ai|。首先向你的账户充值——否则 API 将无法使用。

#. 进入 API Keys 页面，点击 **Create API key**。

   .. image:: img/llm_grok_create.png

#. 为密钥输入一个名称，然后点击 **Create API key**。

   .. image:: img/llm_grok_name.png

#. 复制生成的密钥并妥善保管。

   .. image:: img/llm_grok_copy.png

#. 在你的项目文件夹中：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 像这样粘贴你的密钥：

   .. code-block:: python

        # secret.py
        # Store secrets here. Never commit this file to Git.

        GROK_API_KEY = "xai-xxx"

**查看可用模型**

前往 xAI 控制台的 Models 页面。你可以在这里看到你的团队可用的所有模型及其准确的 API ID——在代码中使用这些 ID。

   .. image:: img/llm_grok_model.png

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``grok-4-latest``）：

   .. code-block:: python

      from fusion_hat.llm import Grok
      from secret import GROK_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Grok(
         api_key=GROK_API_KEY,
         model="grok-4-latest",
      )

#. 运行：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

----

DeepSeek
------------------

DeepSeek 是一个中国 LLM 提供商，提供价格实惠且能力出色的模型。

**获取并保存你的 API 密钥**

#. 登录 |link_deepseek|。

#. 在右上角菜单中，选择 **API Keys → Create API Key**。

   .. image:: img/llm_deepseek_create.png

#. 输入名称，点击 **Create**，然后复制密钥。

   .. image:: img/llm_deepseek_copy.png

#. 在你的项目文件夹中：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 添加你的密钥：

   .. code-block:: python

       # secret.py
       DEEPSEEK_API_KEY = "sk-xxx"

**启用计费**

你需要先为账户充值。从少量金额开始（如 10 元人民币）。

   .. image:: img/llm_deepseek_chognzhi.png

**可用模型**

在撰写本文时（2025-09-12），DeepSeek 提供：

* ``deepseek-chat``
* ``deepseek-reasoner``

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``deepseek-chat``）：

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

#. 运行：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

----

Doubao
------------------
Doubao 是字节跳动的 AI 模型平台（火山引擎 Ark）。

**获取并保存你的 API 密钥**

#. 登录 |link_doubao|。

#. 在左侧菜单中，向下滚动到 **API Key Management → Create API Key**。

   .. image:: img/llm_doubao_create.png

#. 选择名称并点击 **Create**。

   .. image:: img/llm_doubao_name.png

#. 点击 **Show API Key** 图标并复制。

   .. image:: img/llm_doubao_copy.png

#. 在你的项目文件夹中：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano secret.py

#. 添加你的密钥：

   .. code-block:: python

       # secret.py
       DOUBAO_API_KEY = "xxx"

**选择模型**

#. 前往模型市场并选择一个模型。

   .. image:: img/llm_doubao_model_select.png

#. 例如，选择 **Doubao-seed-1.6**，然后点击 **API 接入**。

   .. image:: img/llm_doubao_model.png

#. 选择你的 API 密钥，然后点击 **Use API**。

   .. image:: img/llm_doubao_use_api.png

#. 点击 **Enable Model**。

   .. image:: img/llm_doubao_kaitong.png

#. 悬停在模型 ID 上以复制它。

   .. image:: img/llm_doubao_copy_id.png

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

       cd ~/ai-lab-kit/llm
       sudo nano llm_test.py

#. 将内容替换为以下代码，并将 ``model="xxx"``\ 更新为你想要的模型（例如，\ ``doubao-seed-1-6-250615``）：

   .. code-block:: python

      from fusion_hat.llm import Doubao
      from secret import DOUBAO_API_KEY

      INSTRUCTIONS = "You are a helpful assistant."
      WELCOME = "Hello, I am a helpful assistant. How can I help you?"

      llm = Doubao(
         api_key=DOUBAO_API_KEY,
         model="doubao-seed-1-6-250615",
      )

#. 运行：

   .. code-block:: bash

       sudo python3 llm_test.py

现在你可以直接在终端中与 Fusion HAT+ 聊天。

通用说明
--------------

本项目通过统一接口支持连接多个 LLM 平台。
我们内置了以下平台的支持：

* **OpenAI**\ （ChatGPT / GPT-4o、GPT-4、GPT-3.5）
* **Gemini**\ （Google AI Studio / Vertex AI）
* **Grok**\ （xAI）
* **DeepSeek**
* **Qwen（通义千问）**
* **Doubao（豆包）**

此外，你可以连接到\ **任何其他与 OpenAI API 格式兼容的 LLM 服务**。
对于这些平台，你需要手动获取 **API 密钥**\ 和正确的 **base_url**。

**获取并保存你的 API 密钥**

#. 从你要使用的平台获取 **API 密钥**。（详情请参见各平台的官方控制台。）

#. 在你的项目文件夹中，创建一个新文件：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      nano secret.py

#. 将你的密钥添加到 ``secret.py``\ 中：

   .. code-block:: python

      # secret.py
      API_KEY = "your_api_key_here"

.. warning::

   保持你的 API 密钥私密。不要将 ``secret.py``\ 上传到公共仓库。

**使用示例代码测试**

#. 打开测试文件：

   .. code-block:: bash

      cd ~/ai-lab-kit/llm/
      sudo nano llm_others.py

#. 将 Python 文件的内容替换为以下示例，并填写你平台正确的 ``base_url``\ 和 ``model``：

   .. note::

      关于 ``base_url``：
      我们支持 **OpenAI API 格式**，以及任何与其\ **兼容**\ 的 API。
      每个提供商都有自己 ``base_url``。请查看他们的文档。

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

#. 运行程序：

   .. code-block:: bash

      sudo python3 llm_others.py
