# AI Fusion Lab Kit Documentation Repository

> **Canonical AI guidance.** This is the authoritative CLAUDE.md for the AI Fusion Lab Kit documentation project. All language-variant repositories (`ai-lab-kit-rtd-*-sync`) should sync their CLAUDE.md from this file. When adding rules or fixes, update this file first, then propagate to other language repos.

## Project Identity

| Field | Value |
|---|---|
| **Product** | SunFounder AI Fusion Lab Kit — all-in-one AI/electronics learning platform |
| **Repository** | `https://github.com/sunfounder/ai-lab-kit` |
| **Documentation** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Published at** | `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/` |
| **Company** | SunFounder (service@sunfounder.com) |
| **License** | GPL v2 |

The AI Fusion Lab Kit combines a modular hardware kit with step-by-step learning modules covering Python programming, electronic components, computer vision (OpenCV, MediaPipe), object detection (YOLO), and large language models (Ollama, OpenAI, DeepSeek, xAI, Doubao, Qwen, Gemini). This repository's `docs` branch contains **only documentation** — a Sphinx documentation site built via ReadTheDocs.

---

## Branch Strategy

| Branch | Role |
|---|---|
| `main` | Product source code, system image, installer, examples |
| `docs` | **Documentation source** — Sphinx RST files, images, RTD config |

### Cardinal Rule

> **`docs` is the documentation branch.** All documentation changes (content, structure, images, configuration) happen on `docs`. The `main` branch is for product source code and images. These two branches serve different purposes and should not be confused.

### Language Branches

| Branch | Language | `conf.py` `language` | Published URL |
|---|---|---|---|
| `docs` | English (source) | `'en'` | `/en/latest/` |
| `docs-de` | German | `'de'` | `/de/latest/` |
| `docs-ja` | Japanese | `'ja'` | `/ja/latest/` |

Additional language branches (`docs-es`, `docs-fr`, `docs-it`, `docs-zh`) may be created from `docs` as needed.

---

## Repository Layout (docs branch)

```
ai-lab-kit/
├── .readthedocs.yaml              # RTD build config (Sphinx 7.3.7, Python 3.11, Ubuntu 22.04)
├── .gitignore                     # Ignores: .vscode, build/, secret files, backups
├── .gitmodules                    # Submodule: docs/source/_shared → sf-shared.git (main)
├── LICENSE.txt                    # GPL v2
├── README.md                      # Product overview + quick links
├── show.txt                       # Legacy GPL license/warranty display script
├── CLAUDE.md                      # This file — AI assistant guidance
└── docs/
    ├── requirements.txt           # sphinx==7.3.7, sphinx_rtd_theme==3.0.1, sphinx_copybutton
    ├── Makefile / make.bat        # Sphinx build (SOURCEDIR=source, BUILDDIR=build)
    └── source/
        ├── conf.py                # Sphinx config: extensions, theme, JS/CSS, rst_epilog
        ├── index.rst              # Root toctree — 11 entries
        ├── faq.rst                # Frequently asked questions
        ├── component.rst          # Component reference (toctree into _shared/component/)
        ├── appendix.rst           # Appendix (toctree into _shared/appendix/)
        ├── quick_start/           # Getting started — OS install, HAT assembly, setup
        │   ├── quick_start.rst    #   Chapter index
        │   ├── install_the_os.rst
        │   ├── fh_install_the_os.rst
        │   ├── fh_set_up_pi.rst
        │   ├── run_installer.rst
        │   ├── assemble_power_hat.rst
        │   └── need_components.rst
        ├── video_course/          # YouTube video course links
        │   └── video_course.rst
        ├── python/                # ~50 Python hardware experiments
        │   ├── play_with_python.rst   # Chapter index (Output / Input / Camera & Audio / Projects)
        │   ├── 1.1_blinking_led_python.rst ... 1.10_oled_screen.rst       # Output (10 lessons)
        │   ├── 2.1_button_python.rst ... 2.15_10-axis.rst                 # Input (15 lessons)
        │   ├── 3.1_photograph_python.rst ... 3.4_microphone.rst           # Camera & Audio (4 lessons)
        │   └── 4.1_camera_python.rst ... 4.16_pan_tilt_camera.rst         # Projects (16 lessons)
        ├── llm/                   # AI & Large Language Models
        │   ├── llm.rst                # Chapter index
        │   ├── python_tts_espeak_pico2wave.rst  # TTS (eSpeak, pico2wave)
        │   ├── python_tts_piper_openai.rst      # TTS (Piper, OpenAI TTS)
        │   ├── python_ai_assistant.rst          # STT (Vosk)
        │   ├── python_llm_ollama.rst            # Local LLM (Ollama)
        │   ├── python_online_llms.rst           # Online LLMs (OpenAI, xAI, DeepSeek, Doubao, Qwen, Gemini)
        │   ├── python_local_chatbot.rst         # Local chatbot project
        │   └── python_openai_*.rst              # OpenAI-based projects (health, fan, game, lamp, etc.)
        ├── opencv/                # OpenCV computer vision (9 lessons)
        │   ├── opencv.rst             # Chapter index
        │   └── cv_0_setup.rst ... cv_8_face.rst
        ├── mediapipe/             # MediaPipe AI vision (12 lessons)
        │   ├── mediapipe.rst          # Chapter index
        │   └── mp_0_setup.rst ... mp_11_object_track.rst
        ├── yolo/                  # YOLO object detection (6 lessons)
        │   ├── yolo.rst               # Chapter index
        │   └── yolo_*.rst
        ├── _shared/               # Git submodule — cross-product shared content
        │   ├── component/         #   54 component reference pages
        │   ├── appendix/          #   7 appendix pages (I2C, SPI, SSH, VNC, FileZilla)
        │   └── pi_start/          #   Raspberry Pi getting-started guides
        ├── _static/
        │   ├── lang.js            # Multi-language redirect script
        │   └── video/             # Embedded video files
        ├── _templates/
        │   └── layout.html       # Sphinx HTML template (SunFounder nav bar with logo)
        └── img/                  # All documentation images (organized by chapter)
```

---

## Documentation Conventions

### RST File Boilerplate

Every page follows this exact pattern:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

Page Title
===========
```

The `start_hello_message` / `end_hello_message` markers are defined in `index.rst` and contain the Facebook community note. The `.. include::` directive pulls it into every page.

### Reference Labels

Each `.rst` file defines a reference label for cross-document linking. These labels are code identifiers, not human-readable text — **never translate them**.

Key reference labels:

| Label | File | Content |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | Getting started chapter |
| `youtube_list` | `video_course/video_course.rst` | YouTube video course |
| `play_with_python` | `python/play_with_python.rst` | Python chapter |
| `play_with_llm` | `llm/llm.rst` | AI / LLM chapter |
| `play_with_opencv` | `opencv/opencv.rst` | OpenCV chapter |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | MediaPipe chapter |
| `play_with_yolo` | `yolo/yolo.rst` | YOLO chapter |
| `cpn_list` | `component.rst` | Component reference |
| `faq` | `faq.rst` | Frequently asked questions |

Individual lessons also define labels (e.g., `py_led` in `python/1.1_blinking_led_python.rst`). These labels **must remain consistent** across all language variants — they are the cross-document linking mechanism.

### Include Directives

The primary `include` pattern in this project is the hello message import:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
```

Markers in `index.rst` use the format:
```rst
.. start_hello_message

.. note::
    Hello, welcome to the SunFounder ...

.. end_hello_message
```

When content in this block changes, it affects every page that includes it. Ensure consistency when modifying.

### Link Substitutions (`rst_epilog` in `conf.py`)

All external links live as RST substitutions in `conf.py` under `rst_epilog`. There are three groups:

**Component purchase links** (25+ links for LEDs, sensors, motors, etc.):
```rst
.. |link_led_buy| raw:: html
    <a href="https://www.sunfounder.com/products/..." target="_blank">BUY</a>
```

**Language-specific tutorial links** (6 languages):
| Substitution | Purpose |
|---|---|
| `\|link_sf_facebook\|` | SunFounder Facebook community |
| `\|link_en_tutorials\|` | English online tutorials |
| `\|link_german_tutorials\|` | German online tutorials |
| `\|link_jp_tutorials\|` | Japanese online tutorials |
| `\|link_es_tutorials\|` | Spanish online tutorials |
| `\|link_fr_tutorials\|` | French online tutorials |
| `\|link_it_tutorials\|` | Italian online tutorials |

**External reference links** (Raspberry Pi tools, AI platforms, etc.):
| Substitution | Purpose |
|---|---|
| `\|link_rpi_imager\|` | Raspberry Pi Imager download |
| `\|link_rpi_connect\|` | Raspberry Pi Connect |
| `\|link_ollama\|` | Ollama download |
| `\|link_ollama_hub\|` | Ollama model hub |
| `\|link_openai_platform\|` | OpenAI API keys |
| `\|link_deepseek\|` | DeepSeek platform |
| `\|link_grok_ai\|` | xAI Cloud Console |
| `\|link_doubao\|` | Volcengine (Doubao) |
| `\|link_aliyun\|` | Alibaba Bailian (Qwen) |
| `\|link_google_ai\|` | Google AI Studio (Gemini) |
| `\|link_piper_voice\|` | Piper TTS voices |

When adding a new external link, add the `.. |link_xxx|` definition to `conf.py` `rst_epilog`. Never hardcode external URLs in `.rst` files.

### Image Paths

All images live under `docs/source/img/` and are referenced with `img/` relative paths:

```rst
.. image:: img/led_circuit.png
   :width: 80%
   :align: center
```

Images are organized by chapter (e.g., `img/python/`, `img/opencv/`, `img/mediapipe/`).

### File Naming

- **Python lessons**: `X.Y_descriptive_name_python.rst` (e.g., `1.1_blinking_led_python.rst`, `2.14_dht_python.rst`)
- **OpenCV lessons**: `cv_N_descriptive_name.rst` (e.g., `cv_0_setup.rst`, `cv_8_face.rst`)
- **MediaPipe lessons**: `mp_N_descriptive_name.rst` (e.g., `mp_0_setup.rst`, `mp_7_pose.rst`)
- **YOLO lessons**: `yolo_descriptive_name.rst`
- **LLM lessons**: `python_descriptive_name.rst` (e.g., `python_llm_ollama.rst`, `python_openai_health.rst`)
- **Quick start**: `snake_case_descriptive.rst`
- **Chapter indexes**: `descriptive_name.rst` (e.g., `play_with_python.rst`, `llm.rst`, `opencv.rst`)
- **Root pages**: `index.rst`, `faq.rst`, `component.rst`, `appendix.rst`

### RST Section Underlines

- Title (top-level): `=====` overline and underline
- Section: `------` underline
- Sub-section: `~~~~~~` underline
- The overline/underline must be at least as long as the title text
- For CJK titles: CJK characters count as 2 display columns each; the underline must match the display width, not character count

---

## Build & Preview

### Local Build (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Output: docs/build/html/index.html
```

On Windows:
```batch
cd docs
make.bat html      # Also runs: git submodule update --init --remote
```

**Note**: `make.bat` automatically syncs the `_shared` submodule before building. The Makefile does not.

### ReadTheDocs

Builds automatically on push to the `docs` branch. Configuration in `.readthedocs.yaml`:
- OS: Ubuntu 22.04, Python 3.11
- Sphinx config: `docs/source/conf.py`
- Submodules: included (all, recursive)
- Builds all formats (HTML, PDF, ePub)

### Published URLs

```
https://docs.sunfounder.com/projects/ai-lab-kit/en/latest/
```

---

## Sphinx Configuration (conf.py)

### Extensions

| Extension | Purpose |
|---|---|
| `sphinx_copybutton` | Adds copy button to code blocks |
| `sphinx_rtd_theme` | ReadTheDocs theme |
| `sphinx.ext.intersphinx` | Cross-project reference linking |

`sphinx.ext.autosectionlabel` is **disabled** — keep commented out. Causes duplicate label warnings with CJK section titles.

### Theme

- **Theme**: `sphinx_rtd_theme`
- **Options**: flyout attached, version/language selectors disabled
- **GitHub integration**: Enabled, pointing to `sunfounder/ai-lab-kit` on the `docs` branch

### Custom Assets

**JavaScript** (loaded in order):
- `https://ezblock.cc/readDocFile/custom.js` — SunFounder shared custom JS
- `./lang.js` — Multi-language auto-detection and redirect
- ACE code editor: `ace.js`, `ext-language_tools.js`, `theme-chrome.js`, `mode-python.js`, `mode-sh.js`, `monokai.js`
- xterm.js terminal: `xterm.js`, `FitAddon.js`
- `readTheDocIndex.js` — Custom page behavior

**CSS**:
- `https://ezblock.cc/readDocFile/custom.css` — SunFounder shared custom CSS
- `readTheDoc/src/css/index.css` — Custom page styles
- `readTheDoc/src/css/xterm.css` — Terminal styles

**Template**: `_templates/layout.html` — extends default RTD layout, adds SunFounder nav bar with logo linking to `https://sunfounder.com`.

### Multi-Language

The `lang.js` script in `_static/` handles automatic language detection via browser language and redirects to the appropriate URL.

Published URLs follow the pattern `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/`.

The `language` variable in `conf.py` is set to `'en'` by default. When building for other languages:
- Set `language = '<locale>'` in `conf.py`
- Add `.po` translation files under `docs/source/locale/`
- Update the `link_<lang>_tutorials` substitution with the correct description translation

Supported languages: `en`, `de`, `es`, `fr`, `it`, `ja`, `zh`.

---

## Common Maintenance Tasks

### Adding a New Python Lesson

1. Create the `.rst` file in `docs/source/python/` following the naming convention
2. Start with the standard boilerplate (include hello message + ref label + title)
3. Define a `.. _ref_label:` at the top if the page will be cross-referenced
4. Add the file to the appropriate `.. toctree::` in `python/play_with_python.rst` under the correct section (Output / Input / Camera & Audio / Projects)
5. If new components are introduced, add their purchase links to `conf.py` `rst_epilog`
6. Build locally to verify: `cd docs && make.bat html`
7. Commit on `docs`

### Adding a New Chapter

1. Create a directory under `docs/source/` (e.g., `new_chapter/`)
2. Create the chapter index `.rst` with standard boilerplate + `.. _ref_label:` + toctree
3. Add the chapter to the root toctree in `index.rst`
4. Add the `ref_label` to the navigation section in `index.rst`
5. Build locally to verify

### Updating the Root Toctree

The root toctree in `index.rst` has 11 entries in this order:

1. **About This Kit** — `self` (self-referencing)
2. **Getting Started** — `quick_start/quick_start`
3. **Video Course** — `video_course/video_course`
4. **Play with Python** — `python/play_with_python`
5. **AI (LLM)** — `llm/llm`
6. **OpenCV** — `opencv/opencv`
7. **MediaPipe** — `mediapipe/mediapipe`
8. **YOLO** — `yolo/yolo`
9. **Components** — `component`
10. **Appendix** — `appendix`
11. **FAQ** — `faq`

### Adding Content with Include Markers

When content needs to be shared between pages:

1. Add `.. start_<marker>` before and `.. end_<marker>` after the reusable block in the source file
2. In the destination file, use:
   ```rst
   .. include:: /source_file.rst
       :start-after: start_<marker>
       :end-before: end_<marker>
   ```

### Modifying the Submodule

The `docs/source/_shared/` directory is a Git submodule pointing to `https://github.com/sunfounder/sf-shared.git` (branch: `main`). Changes to shared component docs, appendix pages, or Pi setup guides must be made in the `sf-shared` repository, not here.

To update the submodule pointer:
```bash
cd docs/source/_shared
git pull origin main
cd ../../..
git add docs/source/_shared
git commit -m "Update _shared submodule"
```

### Verifying Language Branches

The `docs` branch is the **English source** and must never contain translated content. After any operation that touches the remote repository (push, merge, force-push), verify the integrity of the `docs` branch and all language branches:

**1. Verify `docs` is English:**

```bash
git show remotes/origin/docs:docs/source/conf.py | grep "language ="
# Expected: language = 'en'
```

If the remote `docs` shows a non-English language, restore it from the canonical English source immediately:

```bash
# From the canonical English workspace:
git push origin docs --force
```

**2. Verify each language branch has the correct language code:**

| Branch | Expected `conf.py` | Published URL |
|---|---|---|
| `docs` | `language = 'en'` | `/en/latest/` |
| `docs-de` | `language = 'de'` | `/de/latest/` |
| `docs-ja` | `language = 'ja'` | `/ja/latest/` |

Additional branches (`docs-es`, `docs-fr`, `docs-it`, `docs-zh`) follow the same pattern.

**3. Quick verification script for all branches:**

```bash
for b in docs docs-de docs-ja; do
  lang=$(git show "remotes/origin/$b:docs/source/conf.py" 2>/dev/null | grep "language =")
  echo "$b: $lang"
done
```

**4. When creating a new language branch:**

- Always branch from `docs` (English), never from another language branch
- Update `conf.py`: set `language = '<code>'`, comment out `sphinx.ext.autosectionlabel`
- Translate all `.rst` files and `README.md`
- Translate `CLAUDE.md` and update the branch identifier
- Run `make html` and resolve all warnings before committing
- **CJK languages (Chinese, Japanese)**: CJK characters count as 2 display columns — section underlines/overlines must be 2× the character count. Inline `**markup**` adjacent to CJK characters needs `\ ` (escaped space) as delimiter.
- After pushing, verify the remote branch content matches the intended language

---

## Notes for AI Assistants

When working on this repository:

1. **The `docs` branch is documentation-only.** Product source code and system images live on `main`. Do not add Python scripts, binaries, or disk images to `docs`.
2. **The Facebook community note** at the top of each `.rst` file is imported from `index.rst` via the `start_hello_message` / `end_hello_message` include block. It is part of SunFounder's documentation standard and appears on nearly every user-facing page.
3. **`conf.py` link substitutions** are the single source of external URLs. Never hardcode external links in `.rst` files — use `|link_xxx|` substitutions.
4. **Reference labels** (`.. _label:`) are code identifiers, not human-readable text. Never translate them.
5. **RST section underlines (and overlines) must match title display width.**
   
   - For single-underline headings (title followed by `=` or `-`), the underline must be at least as long as the title text.
   - For overline+underline headings (e.g., `====` above and below the title), **both** the overline and underline must use the same character, be the **exact same length**, and be at least as long as the title. When translating titles, always update both lines together.
   - **CJK display width**: docutils counts CJK characters as **2 display columns** each (ASCII = 1 column). The overline/underline must match the total display width, not the character count.
   
   Translated titles are often longer than the English originals — extend overlines and underlines accordingly. When the title contains CJK characters, the underline/overline will be significantly longer than the character count suggests.

6. **Inline strong markup (`**...**`) breaks when adjacent to CJK characters.** docutils inline markup recognition requires the `**` delimiters to be adjacent to whitespace or ASCII punctuation (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). CJK characters (Chinese, Japanese, Korean) are **not** valid delimiters.

   When `**text**` is immediately preceded or followed by a CJK character, docutils emits `WARNING: Inline strong start-string without end-string.` because it cannot find the closing `**`.

   **Fix**: Insert `\ ` (backslash-escaped space) between the `**` delimiter and the adjacent CJK character:

   ```rst
   # WRONG — closing ** followed by CJK に, warning emitted:
   **PI3V3**にブリッジすると

   # RIGHT — \  acts as a valid delimiter:
   **PI3V3**\ にブリッジすると

   # WRONG — opening ** preceded by CJK は, warning emitted:
   または**コマンドラインツール**

   # RIGHT:
   または\ **コマンドラインツール**
   ```

   This applies equally to other inline markup (`*emphasis*`, ```literal```) when adjacent to CJK text. Always check the build warnings for "Inline ... start-string without end-string" after translating content with inline markup.

7. **Nested lists require blank lines and correct indentation in RST.** When a numbered list item or bullet item contains sub-bullets, a blank line must precede the nested list, and the nested items must be indented to align with the text of the parent item (typically 3+ spaces). Without the blank line, RST renders the bullets as a single run-on line.

   **Wrong** (sub-bullets without blank line):
   ```rst
   3. **Parent item**:
      - First sub-item
      - Second sub-item
   ```

   **Correct**:
   ```rst
   3. **Parent item**:

        - First sub-item
        - Second sub-item
   ```

8. **Code blocks** (Python, bash, shell) are never translated. Command strings and file paths stay as-is.
9. **The `_static` and `_templates` directories** contain custom assets. Changes here affect the global look and behavior of the published site across all pages.
10. **Build output** goes to `docs/build/` and is gitignored — never commit build artifacts.
11. **Images** are all under `docs/source/img/`. When adding new images, place them there (organized by chapter subdirectory) and reference with relative paths.
12. **The `_shared` submodule** contains cross-product content (component references, appendix, Pi setup guides). Changes to these files must go through the `sf-shared` repository, not be edited directly here.
13. **The `show` script** at the repo root is a GPL license display utility — it is Python 2 syntax and should be considered legacy.
14. **Lesson file numbering** follows a consistent scheme: `X.Y_` for Python lessons (where X = section, Y = lesson within section), `cv_N_` for OpenCV, `mp_N_` for MediaPipe. When adding lessons within an existing section, renumber carefully to avoid breaking cross-references.
15. **The `make.bat` Windows build script** automatically runs `git submodule update --init --remote` before building. The `Makefile` does not — when using `make html` on Linux/macOS, ensure the submodule is up to date manually if needed.
