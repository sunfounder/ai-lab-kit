# AI Fusion Lab Kit 文档仓库

> **权威 AI 指南。** 这是 AI Fusion Lab Kit 文档项目的权威 CLAUDE.md。所有语言变体仓库（`ai-lab-kit-rtd-*-sync`）应从此文件同步其 CLAUDE.md。在添加规则或修复时，请先更新此文件，然后传播到其他语言仓库。

## 项目标识

| 字段 | 值 |
|---|---|
| **产品** | SunFounder AI Fusion Lab Kit —— 一体化 AI/电子学习平台 |
| **仓库** | `https://github.com/sunfounder/ai-lab-kit` |
| **文档** | Sphinx + ReadTheDocs（`sphinx_rtd_theme`） |
| **发布地址** | `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/` |
| **公司** | SunFounder（service@sunfounder.com） |
| **许可证** | GPL v2 |

AI Fusion Lab Kit 将模块化硬件套件与循序渐进的学习模块相结合，涵盖 Python 编程、电子元器件、计算机视觉（OpenCV、MediaPipe）、目标检测（YOLO）和大语言模型（Ollama、OpenAI、DeepSeek、xAI、Doubao、Qwen、Gemini）。本仓库的 `docs` 分支仅包含**文档** —— 一个通过 ReadTheDocs 构建的 Sphinx 文档站点。

---

## 分支策略

| 分支 | 角色 |
|---|---|
| `main` | 产品源代码、系统镜像、安装程序、示例 |
| `docs` | **文档源文件** —— Sphinx RST 文件、图片、RTD 配置 |

### 基本原则

> **`docs` 是文档分支。** 所有文档变更（内容、结构、图片、配置）都在 `docs` 上进行。`main` 分支用于产品源代码和镜像。这两个分支服务于不同的目的，不应混淆。

### 语言分支

| 分支 | 语言 | `conf.py` `language` | 发布 URL |
|---|---|---|---|
| `docs` | 英语（源文件） | `'en'` | `/en/latest/` |
| `docs-de` | 德语 | `'de'` | `/de/latest/` |
| `docs-ja` | 日语 | `'ja'` | `/ja/latest/` |
| `docs-cn` | 中文 | `'zh'` | `/zh/latest/` |

其他语言分支（`docs-es`、`docs-fr`、`docs-it`、`docs-zh`）可根据需要从 `docs` 创建。

---

## 仓库结构（docs 分支）

```
ai-lab-kit/
├── .readthedocs.yaml              # RTD 构建配置（Sphinx 7.3.7、Python 3.11、Ubuntu 22.04）
├── .gitignore                     # 忽略：.vscode、build/、密钥文件、备份
├── .gitmodules                    # 子模块：docs/source/_shared → sf-shared.git（main）
├── LICENSE.txt                    # GPL v2
├── README.md                      # 产品概述 + 快速链接
├── show.txt                       # 旧版 GPL 许可证/担保显示脚本
├── CLAUDE.md                      # 本文件 —— AI 助手指南
└── docs/
    ├── requirements.txt           # sphinx==7.3.7、sphinx_rtd_theme==3.0.1、sphinx_copybutton
    ├── Makefile / make.bat        # Sphinx 构建（SOURCEDIR=source、BUILDDIR=build）
    └── source/
        ├── conf.py                # Sphinx 配置：扩展、主题、JS/CSS、rst_epilog
        ├── index.rst              # 根 toctree —— 11 个条目
        ├── faq.rst                # 常见问题
        ├── component.rst          # 元器件参考（toctree 指向 _shared/component/）
        ├── appendix.rst           # 附录（toctree 指向 _shared/appendix/）
        ├── quick_start/           # 快速入门 —— OS 安装、HAT 组装、设置
        │   ├── quick_start.rst    #   章节索引
        │   ├── install_the_os.rst
        │   ├── fh_install_the_os.rst
        │   ├── fh_set_up_pi.rst
        │   ├── run_installer.rst
        │   ├── assemble_power_hat.rst
        │   └── need_components.rst
        ├── video_course/          # YouTube 视频课程链接
        │   └── video_course.rst
        ├── python/                # 约 50 个 Python 硬件实验
        │   ├── play_with_python.rst   # 章节索引（输出 / 输入 / 摄像头与音频 / 项目）
        │   ├── 1.1_blinking_led_python.rst ... 1.10_oled_screen.rst       # 输出（10 课）
        │   ├── 2.1_button_python.rst ... 2.15_10-axis.rst                 # 输入（15 课）
        │   ├── 3.1_photograph_python.rst ... 3.4_microphone.rst           # 摄像头与音频（4 课）
        │   └── 4.1_camera_python.rst ... 4.16_pan_tilt_camera.rst         # 项目（16 课）
        ├── llm/                   # AI 与大语言模型
        │   ├── llm.rst                # 章节索引
        │   ├── python_tts_espeak_pico2wave.rst  # TTS（eSpeak、pico2wave）
        │   ├── python_tts_piper_openai.rst      # TTS（Piper、OpenAI TTS）
        │   ├── python_ai_assistant.rst          # STT（Vosk）
        │   ├── python_llm_ollama.rst            # 本地 LLM（Ollama）
        │   ├── python_online_llms.rst           # 在线 LLM（OpenAI、xAI、DeepSeek、Doubao、Qwen、Gemini）
        │   ├── python_local_chatbot.rst         # 本地聊天机器人项目
        │   └── python_openai_*.rst              # 基于 OpenAI 的项目（健康、风扇、游戏、灯等）
        ├── opencv/                # OpenCV 计算机视觉（9 课）
        │   ├── opencv.rst             # 章节索引
        │   └── cv_0_setup.rst ... cv_8_face.rst
        ├── mediapipe/             # MediaPipe AI 视觉（12 课）
        │   ├── mediapipe.rst          # 章节索引
        │   └── mp_0_setup.rst ... mp_11_object_track.rst
        ├── yolo/                  # YOLO 目标检测（6 课）
        │   ├── yolo.rst               # 章节索引
        │   └── yolo_*.rst
        ├── _shared/               # Git 子模块 —— 跨产品共享内容
        │   ├── component/         #   54 个元器件参考页面
        │   ├── appendix/          #   7 个附录页面（I2C、SPI、SSH、VNC、FileZilla）
        │   └── pi_start/          #   Raspberry Pi 入门指南
        ├── _static/
        │   ├── lang.js            # 多语言重定向脚本
        │   └── video/             # 嵌入式视频文件
        ├── _templates/
        │   └── layout.html        # Sphinx HTML 模板（带 logo 的 SunFounder 导航栏）
        └── img/                   # 所有文档图片（按章节组织）
```

---

## 文档约定

### RST 文件样板

每个页面都遵循以下精确模式：

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

页面标题
===========
```

`start_hello_message` / `end_hello_message` 标记定义在 `index.rst` 中，包含 Facebook 社区公告。`.. include::` 指令将其引入每个页面。

### 引用标签

每个 `.rst` 文件定义一个用于跨文档链接的引用标签。这些标签是代码标识符，而非人类可读的文本——**切勿翻译它们**。

关键引用标签：

| 标签 | 文件 | 内容 |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | 快速入门章节 |
| `youtube_list` | `video_course/video_course.rst` | YouTube 视频课程 |
| `play_with_python` | `python/play_with_python.rst` | Python 章节 |
| `play_with_llm` | `llm/llm.rst` | AI / LLM 章节 |
| `play_with_opencv` | `opencv/opencv.rst` | OpenCV 章节 |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | MediaPipe 章节 |
| `play_with_yolo` | `yolo/yolo.rst` | YOLO 章节 |
| `cpn_list` | `component.rst` | 元器件参考 |
| `faq` | `faq.rst` | 常见问题 |

各个课程也定义了标签（例如 `python/1.1_blinking_led_python.rst` 中的 `py_led`）。这些标签**必须在所有语言变体中保持一致**——它们是跨文档链接机制。

### Include 指令

本项目主要的 `include` 模式是欢迎消息导入：

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
```

`index.rst` 中的标记使用以下格式：
```rst
.. start_hello_message

.. note::
    Hello, welcome to the SunFounder ...

.. end_hello_message
```

当此块中的内容发生变化时，将影响所有包含它的页面。修改时请确保一致性。

### 链接替换（`conf.py` 中的 `rst_epilog`）

所有外部链接都以 RST 替换的方式存在于 `conf.py` 的 `rst_epilog` 中。共有三组：

**元器件购买链接**（25+ 个 LED、传感器、电机等链接）：
```rst
.. |link_led_buy| raw:: html
    <a href="https://www.sunfounder.com/products/..." target="_blank">购买</a>
```

**语言特定教程链接**（6 种语言）：
| 替换 | 用途 |
|---|---|
| `\|link_sf_facebook\|` | SunFounder Facebook 社区 |
| `\|link_en_tutorials\|` | 英语在线教程 |
| `\|link_german_tutorials\|` | 德语在线教程 |
| `\|link_jp_tutorials\|` | 日语在线教程 |
| `\|link_es_tutorials\|` | 西班牙语在线教程 |
| `\|link_fr_tutorials\|` | 法语在线教程 |
| `\|link_it_tutorials\|` | 意大利语在线教程 |

**外部参考链接**（Raspberry Pi 工具、AI 平台等）：
| 替换 | 用途 |
|---|---|
| `\|link_rpi_imager\|` | Raspberry Pi Imager 下载 |
| `\|link_rpi_connect\|` | Raspberry Pi Connect |
| `\|link_ollama\|` | Ollama 下载 |
| `\|link_ollama_hub\|` | Ollama 模型中心 |
| `\|link_openai_platform\|` | OpenAI API 密钥 |
| `\|link_deepseek\|` | DeepSeek 平台 |
| `\|link_grok_ai\|` | xAI Cloud Console |
| `\|link_doubao\|` | 火山引擎（豆包） |
| `\|link_aliyun\|` | 阿里云百炼（Qwen） |
| `\|link_google_ai\|` | Google AI Studio（Gemini） |
| `\|link_piper_voice\|` | Piper TTS 语音 |

在添加新的外部链接时，请将 `.. |link_xxx|` 定义添加到 `conf.py` 的 `rst_epilog` 中。切勿在 `.rst` 文件中硬编码外部 URL。

### 图片路径

所有图片位于 `docs/source/img/` 下，使用 `img/` 相对路径引用：

```rst
.. image:: img/led_circuit.png
   :width: 80%
   :align: center
```

图片按章节组织（例如 `img/python/`、`img/opencv/`、`img/mediapipe/`）。

### 文件命名

- **Python 课程**：`X.Y_descriptive_name_python.rst`（例如 `1.1_blinking_led_python.rst`、`2.14_dht_python.rst`）
- **OpenCV 课程**：`cv_N_descriptive_name.rst`（例如 `cv_0_setup.rst`、`cv_8_face.rst`）
- **MediaPipe 课程**：`mp_N_descriptive_name.rst`（例如 `mp_0_setup.rst`、`mp_7_pose.rst`）
- **YOLO 课程**：`yolo_descriptive_name.rst`
- **LLM 课程**：`python_descriptive_name.rst`（例如 `python_llm_ollama.rst`、`python_openai_health.rst`）
- **快速入门**：`snake_case_descriptive.rst`
- **章节索引**：`descriptive_name.rst`（例如 `play_with_python.rst`、`llm.rst`、`opencv.rst`）
- **根页面**：`index.rst`、`faq.rst`、`component.rst`、`appendix.rst`

### RST 章节下划线

- 标题（顶层）：`=====` 上划线和下划线
- 章节：`------` 下划线
- 子章节：`~~~~~~` 下划线
- 上划线/下划线必须至少与标题文本等长
- 对于 CJK 标题：每个 CJK 字符计为 2 个显示列；下划线必须匹配显示宽度，而非字符数

---

## 构建与预览

### 本地构建（Sphinx）

```bash
cd docs
pip install -r requirements.txt
make html          # 输出：docs/build/html/index.html
```

在 Windows 上：
```batch
cd docs
make.bat html      # 同时运行：git submodule update --init --remote
```

**注意**：`make.bat` 在构建前会自动同步 `_shared` 子模块。Makefile 不会。

### ReadTheDocs

推送到 `docs` 分支时自动构建。配置在 `.readthedocs.yaml` 中：
- 操作系统：Ubuntu 22.04、Python 3.11
- Sphinx 配置：`docs/source/conf.py`
- 子模块：包含（全部、递归）
- 构建所有格式（HTML、PDF、ePub）

### 发布 URL

```
https://docs.sunfounder.com/projects/ai-lab-kit/en/latest/
```

---

## Sphinx 配置（conf.py）

### 扩展

| 扩展 | 用途 |
|---|---|
| `sphinx_copybutton` | 为代码块添加复制按钮 |
| `sphinx_rtd_theme` | ReadTheDocs 主题 |
| `sphinx.ext.intersphinx` | 跨项目引用链接 |

`sphinx.ext.autosectionlabel` **已禁用** —— 保持注释状态。在包含 CJK 章节标题时会导致重复标签警告。

### 主题

- **主题**：`sphinx_rtd_theme`
- **选项**：flyout 附加，版本/语言选择器禁用
- **GitHub 集成**：已启用，指向 `sunfounder/ai-lab-kit` 的 `docs` 分支

### 自定义资源

**JavaScript**（按顺序加载）：
- `https://ezblock.cc/readDocFile/custom.js` —— SunFounder 共享自定义 JS
- `./lang.js` —— 多语言自动检测和重定向
- ACE 代码编辑器：`ace.js`、`ext-language_tools.js`、`theme-chrome.js`、`mode-python.js`、`mode-sh.js`、`monokai.js`
- xterm.js 终端：`xterm.js`、`FitAddon.js`
- `readTheDocIndex.js` —— 自定义页面行为

**CSS**：
- `https://ezblock.cc/readDocFile/custom.css` —— SunFounder 共享自定义 CSS
- `readTheDoc/src/css/index.css` —— 自定义页面样式
- `readTheDoc/src/css/xterm.css` —— 终端样式

**模板**：`_templates/layout.html` —— 扩展默认 RTD 布局，添加链接到 `https://sunfounder.com` 的 SunFounder 导航栏及 logo。

### 多语言

`_static/` 中的 `lang.js` 脚本通过浏览器语言自动检测并重定向到相应的 URL。

发布 URL 遵循模式 `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/`。

`conf.py` 中的 `language` 变量默认设置为 `'en'`。在为其他语言构建时：
- 在 `conf.py` 中设置 `language = '<locale>'`
- 在 `docs/source/locale/` 下添加 `.po` 翻译文件
- 使用正确的描述翻译更新 `link_<lang>_tutorials` 替换

支持的语言：`en`、`de`、`es`、`fr`、`it`、`ja`、`zh`。

---

## 常见维护任务

### 添加新的 Python 课程

1. 按照命名约定在 `docs/source/python/` 中创建 `.rst` 文件
2. 以标准样板开头（包含欢迎消息 + 引用标签 + 标题）
3. 如果页面将被交叉引用，在顶部定义 `.. _ref_label:`
4. 将文件添加到 `python/play_with_python.rst` 中的相应 `.. toctree::`，放在正确的部分（输出 / 输入 / 摄像头与音频 / 项目）
5. 如果引入了新元器件，将其购买链接添加到 `conf.py` 的 `rst_epilog`
6. 本地构建验证：`cd docs && make.bat html`
7. 在 `docs` 上提交

### 添加新章节

1. 在 `docs/source/` 下创建目录（例如 `new_chapter/`）
2. 创建章节索引 `.rst`，包含标准样板 + `.. _ref_label:` + toctree
3. 将章节添加到 `index.rst` 的根 toctree
4. 将 `ref_label` 添加到 `index.rst` 的导航部分
5. 本地构建验证

### 更新根 Toctree

`index.rst` 中的根 toctree 按顺序包含 11 个条目：

1. **关于本套件** —— `self`（自引用）
2. **快速入门** —— `quick_start/quick_start`
3. **视频课程** —— `video_course/video_course`
4. **玩转 Python** —— `python/play_with_python`
5. **AI（LLM）** —— `llm/llm`
6. **OpenCV** —— `opencv/opencv`
7. **MediaPipe** —— `mediapipe/mediapipe`
8. **YOLO** —— `yolo/yolo`
9. **元器件** —— `component`
10. **附录** —— `appendix`
11. **常见问题** —— `faq`

### 使用 Include 标记添加内容

当需要在页面之间共享内容时：

1. 在源文件中，在可重用块之前添加 `.. start_<marker>`，之后添加 `.. end_<marker>`
2. 在目标文件中，使用：
   ```rst
   .. include:: /source_file.rst
       :start-after: start_<marker>
       :end-before: end_<marker>
   ```

### 修改子模块

`docs/source/_shared/` 目录是一个 Git 子模块，指向 `https://github.com/sunfounder/sf-shared.git`（分支：`main`）。共享元器件文档、附录页面或 Pi 设置指南的更改必须在 `sf-shared` 仓库中进行，而非此处。

要更新子模块指针：
```bash
cd docs/source/_shared
git pull origin main
cd ../../..
git add docs/source/_shared
git commit -m "更新 _shared 子模块"
```

### 验证语言分支

`docs` 分支是**英语源文件**，绝不能包含翻译内容。在执行任何涉及远程仓库的操作（推送、合并、强制推送）后，请验证 `docs` 分支和所有语言分支的完整性：

**1. 验证 `docs` 为英语：**

```bash
git show remotes/origin/docs:docs/source/conf.py | grep "language ="
# 预期：language = 'en'
```

如果远程 `docs` 显示非英语语言，请立即从规范英语源恢复：

```bash
# 从规范英语工作区：
git push origin docs --force
```

**2. 验证每个语言分支具有正确的语言代码：**

| 分支 | 预期 `conf.py` | 发布 URL |
|---|---|---|
| `docs` | `language = 'en'` | `/en/latest/` |
| `docs-de` | `language = 'de'` | `/de/latest/` |
| `docs-ja` | `language = 'ja'` | `/ja/latest/` |
| `docs-cn` | `language = 'zh'` | `/zh/latest/` |

其他分支（`docs-es`、`docs-fr`、`docs-it`、`docs-zh`）遵循相同模式。

**3. 所有分支的快速验证脚本：**

```bash
for b in docs docs-de docs-ja docs-cn; do
  lang=$(git show "remotes/origin/$b:docs/source/conf.py" 2>/dev/null | grep "language =")
  echo "$b: $lang"
done
```

**4. 创建新的语言分支时：**

- 始终从 `docs`（英语）分支，切勿从其他语言分支
- 更新 `conf.py`：设置 `language = '<code>'`，注释掉 `sphinx.ext.autosectionlabel`
- 翻译所有 `.rst` 文件和 `README.md`
- 翻译 `CLAUDE.md` 并更新分支标识符
- 运行 `make html` 并在提交前解决所有警告
- **CJK 语言（中文、日语）**：每个 CJK 字符计为 2 个显示列——章节上划线/下划线必须为字符数的 2 倍。与 CJK 字符相邻的内联 `**markup**` 需要使用 `\ `（转义空格）作为分隔符。
- 推送后，验证远程分支内容是否与目标语言一致

---

## AI 助手注意事项

在处理此仓库时：

1. **`docs` 分支仅包含文档。** 产品源代码和系统镜像位于 `main`。不要向 `docs` 添加 Python 脚本、二进制文件或磁盘镜像。
2. **Facebook 社区公告** 位于每个 `.rst` 文件的顶部，通过 `index.rst` 的 `start_hello_message` / `end_hello_message` 包含块导入。它是 SunFounder 文档标准的一部分，出现在几乎所有面向用户的页面上。
3. **`conf.py` 链接替换** 是外部 URL 的唯一来源。切勿在 `.rst` 文件中硬编码外部链接——使用 `|link_xxx|` 替换。
4. **引用标签**（`.. _label:`）是代码标识符，而非人类可读的文本。切勿翻译它们。
5. **RST 章节下划线（和上划线）必须匹配标题的显示宽度。**

   - 对于单下划线标题（标题后跟 `=` 或 `-`），下划线必须至少与标题文本等长。
   - 对于上划线+下划线标题（例如标题上方和下方的 `====`），**两个**线必须使用相同字符，**长度完全相等**，且至少与标题等长。翻译标题时，请同时更新两个线。
   - **CJK 显示宽度**：docutils 将每个 CJK 字符计为 **2 个显示列**（ASCII = 1 列）。上划线/下划线必须匹配总显示宽度，而非字符数。

   翻译后的标题通常比英文原文更长——请相应延长上划线和下划线。当标题包含 CJK 字符时，下划线/上划线将比字符数显示的长度长得多。

6. **内联加粗标记（`**...**`）在与 CJK 字符相邻时会中断。** docutils 内联标记识别要求 `**` 分隔符与空白或 ASCII 标点相邻（`- : / . , ; ! ? ' " ( ) [ ] { } < >`）。CJK 字符（中文、日文、韩文）**不是**有效的分隔符。

   当 `**text**` 前面或后面紧邻 CJK 字符时，docutils 会发出 `WARNING: Inline strong start-string without end-string.` 因为它找不到闭合的 `**`。

   **修复**：在 `**` 分隔符与相邻 CJK 字符之间插入 `\ `（反斜杠转义空格）：

   ```rst
   # 错误 —— 闭合 ** 后跟 CJK 字符，发出警告：
   **PI3V3**にブリッジすると

   # 正确 —— \ 作为有效分隔符：
   **PI3V3**\ にブリッジすると

   # 错误 —— 开 ** 前有 CJK 字符，发出警告：
   または**コマンドラインツール**

   # 正确：
   または\ **コマンドラインツール**
   ```

   当其他内联标记（`*emphasis*`、`` `literal` ``）与 CJK 文本相邻时同样适用。在翻译包含内联标记的内容后，请始终检查构建警告中是否有 "Inline ... start-string without end-string"。

7. **RST 中的嵌套列表需要空行和正确的缩进。** 当编号列表项或项目符号项包含子项目时，必须在嵌套列表前添加空行，并且嵌套项必须缩进以与父项文本对齐（通常为 3 个以上空格）。如果没有空行，RST 会将项目符号渲染为连续的一行。

   **错误**（子项目没有空行）：
   ```rst
   3. **父项**：
      - 第一个子项
      - 第二个子项
   ```

   **正确**：
   ```rst
   3. **父项**：

        - 第一个子项
        - 第二个子项
   ```

8. **代码块**（Python、bash、shell）绝不翻译。命令字符串和文件路径保持不变。
9. **`_static` 和 `_templates` 目录** 包含自定义资源。此处的更改会影响已发布站点的全局外观和行为。
10. **构建输出** 位于 `docs/build/` 且已被 gitignore——切勿提交构建产物。
11. **图片** 全部位于 `docs/source/img/` 下。添加新图片时，请将其放置在此处（按章节子目录组织）并使用相对路径引用。
12. **`_shared` 子模块** 包含跨产品内容（元器件参考、附录、Pi 设置指南）。对这些文件的更改必须通过 `sf-shared` 仓库进行，而非在此处直接编辑。
13. **仓库根目录的 `show` 脚本** 是一个 GPL 许可证显示工具——它使用 Python 2 语法，应视为遗留文件。
14. **课程文件编号** 遵循一致的方案：Python 课程为 `X.Y_`（其中 X = 部分，Y = 部分内的课程），OpenCV 为 `cv_N_`，MediaPipe 为 `mp_N_`。在现有部分内添加课程时，请仔细重新编号以避免破坏交叉引用。
15. **`make.bat` Windows 构建脚本** 在构建前会自动运行 `git submodule update --init --remote`。`Makefile` 不会——在 Linux/macOS 上使用 `make html` 时，如有需要请手动确保子模块是最新的。
