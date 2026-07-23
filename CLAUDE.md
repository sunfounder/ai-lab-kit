# Dépôt de documentation du Kit AI Fusion Lab

> **Guide IA canonique.** Ceci est le CLAUDE.md faisant autorité pour le projet de documentation AI Fusion Lab Kit. Tous les dépôts de variantes linguistiques (`ai-lab-kit-rtd-*-sync`) doivent synchroniser leur CLAUDE.md à partir de ce fichier. Lors de l'ajout de règles ou de corrections, mettez d'abord ce fichier à jour, puis propagez les modifications aux autres dépôts linguistiques.

## Identité du projet

| Champ | Valeur |
|---|---|
| **Produit** | SunFounder AI Fusion Lab Kit — plateforme d'apprentissage tout-en-un IA/électronique |
| **Dépôt** | `https://github.com/sunfounder/ai-lab-kit` |
| **Documentation** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Publié sur** | `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/` |
| **Entreprise** | SunFounder (service@sunfounder.com) |
| **Licence** | GPL v2 |

Le Kit AI Fusion Lab combine un kit matériel modulaire avec des modules d'apprentissage étape par étape couvrant la programmation Python, les composants électroniques, la vision par ordinateur (OpenCV, MediaPipe), la détection d'objets (YOLO) et les grands modèles de langage (Ollama, OpenAI, DeepSeek, xAI, Doubao, Qwen, Gemini). La branche `docs` de ce dépôt contient **uniquement la documentation** — un site de documentation Sphinx construit via ReadTheDocs.

---

## Stratégie de branches

| Branche | Rôle |
|---|---|
| `main` | Code source du produit, image système, installateur, exemples |
| `docs` | **Source de la documentation** — Fichiers RST Sphinx, images, configuration RTD |

### Règle fondamentale

> **`docs` est la branche de documentation.** Toutes les modifications de documentation (contenu, structure, images, configuration) se font sur `docs`. La branche `main` est destinée au code source du produit et aux images. Ces deux branches servent des objectifs différents et ne doivent pas être confondues.

### Branches linguistiques

| Branche | Langue | `conf.py` `language` | URL publiée |
|---|---|---|---|
| `docs` | Anglais (source) | `'en'` | `/en/latest/` |
| `docs-de` | Allemand | `'de'` | `/de/latest/` |
| `docs-fr` | Francais | `'fr'` | `/fr/latest/` |
| `docs-ja` | Japonais | `'ja'` | `/ja/latest/` |

Des branches linguistiques supplémentaires (`docs-es`, `docs-it`, `docs-zh`) peuvent être créées à partir de `docs` selon les besoins.

---

## Structure du dépôt (branche docs)

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

## Conventions de documentation

### Structure standard des fichiers RST

Chaque page suit exactement ce modèle :

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

Page Title
===========
```

Les marqueurs `start_hello_message` / `end_hello_message` sont définis dans `index.rst` et contiennent la note de la communauté Facebook. La directive `.. include::` l'insère dans chaque page.

### Étiquettes de référence

Chaque fichier `.rst` définit une étiquette de référence pour les liens inter-documents. Ces étiquettes sont des identifiants de code, pas du texte lisible — **ne jamais les traduire**.

Étiquettes de référence clés :

| Étiquette | Fichier | Contenu |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | Chapitre Premiers pas |
| `youtube_list` | `video_course/video_course.rst` | Cours vidéo YouTube |
| `play_with_python` | `python/play_with_python.rst` | Chapitre Python |
| `play_with_llm` | `llm/llm.rst` | Chapitre IA / LLM |
| `play_with_opencv` | `opencv/opencv.rst` | Chapitre OpenCV |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | Chapitre MediaPipe |
| `play_with_yolo` | `yolo/yolo.rst` | Chapitre YOLO |
| `cpn_list` | `component.rst` | Référence des composants |
| `faq` | `faq.rst` | Foire aux questions |

Les leçons individuelles définissent également des étiquettes (ex. `py_led` dans `python/1.1_blinking_led_python.rst`). Ces étiquettes **doivent rester cohérentes** dans toutes les variantes linguistiques — elles constituent le mécanisme de liaison inter-documents.

### Directives Include

Le principal motif `include` dans ce projet est l'importation du message d'accueil :

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
```

Les marqueurs dans `index.rst` utilisent le format :
```rst
.. start_hello_message

.. note::
    Bonjour, bienvenue chez SunFounder ...

.. end_hello_message
```

Lorsque le contenu de ce bloc change, cela affecte chaque page qui l'inclut. Assurez la cohérence lors des modifications.

### Substitutions de liens (`rst_epilog` dans `conf.py`)

Tous les liens externes sont définis comme substitutions RST dans `conf.py` sous `rst_epilog`. Il y a trois groupes :

**Liens d'achat de composants** (plus de 25 liens pour LED, capteurs, moteurs, etc.) :
```rst
.. |link_led_buy| raw:: html
    <a href="https://www.sunfounder.com/products/..." target="_blank">ACHETER</a>
```

**Liens de tutoriels par langue** (6 langues) :
| Substitution | Usage |
|---|---|
| `\|link_sf_facebook\|` | Communauté Facebook SunFounder |
| `\|link_en_tutorials\|` | Tutoriels en ligne en anglais |
| `\|link_german_tutorials\|` | Tutoriels en ligne en allemand |
| `\|link_jp_tutorials\|` | Tutoriels en ligne en japonais |
| `\|link_es_tutorials\|` | Tutoriels en ligne en espagnol |
| `\|link_fr_tutorials\|` | Tutoriels en ligne en français |
| `\|link_it_tutorials\|` | Tutoriels en ligne en italien |

**Liens de référence externes** (outils Raspberry Pi, plateformes IA, etc.) :
| Substitution | Usage |
|---|---|
| `\|link_rpi_imager\|` | Téléchargement de Raspberry Pi Imager |
| `\|link_rpi_connect\|` | Raspberry Pi Connect |
| `\|link_ollama\|` | Téléchargement d'Ollama |
| `\|link_ollama_hub\|` | Hub de modèles Ollama |
| `\|link_openai_platform\|` | Clés API OpenAI |
| `\|link_deepseek\|` | Plateforme DeepSeek |
| `\|link_grok_ai\|` | Console Cloud xAI |
| `\|link_doubao\|` | Volcengine (Doubao) |
| `\|link_aliyun\|` | Alibaba Bailian (Qwen) |
| `\|link_google_ai\|` | Google AI Studio (Gemini) |
| `\|link_piper_voice\|` | Voix Piper TTS |

Lors de l'ajout d'un nouveau lien externe, ajoutez la définition `.. |link_xxx|` dans `conf.py` `rst_epilog`. Ne jamais coder en dur les URL externes dans les fichiers `.rst`.

### Chemins d'images

Toutes les images se trouvent sous `docs/source/img/` et sont référencées avec des chemins relatifs `img/` :

```rst
.. image:: img/led_circuit.png
   :width: 80%
   :align: center
```

Les images sont organisées par chapitre (ex. `img/python/`, `img/opencv/`, `img/mediapipe/`).

### Nommage des fichiers

- **Leçons Python** : `X.Y_nom_descriptif_python.rst` (ex. `1.1_blinking_led_python.rst`, `2.14_dht_python.rst`)
- **Leçons OpenCV** : `cv_N_nom_descriptif.rst` (ex. `cv_0_setup.rst`, `cv_8_face.rst`)
- **Leçons MediaPipe** : `mp_N_nom_descriptif.rst` (ex. `mp_0_setup.rst`, `mp_7_pose.rst`)
- **Leçons YOLO** : `yolo_nom_descriptif.rst`
- **Leçons LLM** : `python_nom_descriptif.rst` (ex. `python_llm_ollama.rst`, `python_openai_health.rst`)
- **Premiers pas** : `snake_case_descriptif.rst`
- **Index de chapitre** : `nom_descriptif.rst` (ex. `play_with_python.rst`, `llm.rst`, `opencv.rst`)
- **Pages racines** : `index.rst`, `faq.rst`, `component.rst`, `appendix.rst`

### Soulignements de sections RST

- Titre (niveau supérieur) : `=====` surlignement et soulignement
- Section : `------` soulignement
- Sous-section : `~~~~~~` soulignement
- Le surlignement/soulignement doit être au moins aussi long que le texte du titre
- Pour les titres CJK : les caractères CJK comptent pour 2 colonnes d'affichage chacun ; le soulignement doit correspondre à la largeur d'affichage, pas au nombre de caractères

---

## Compilation et prévisualisation

### Compilation locale (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Sortie : docs/build/html/index.html
```

Sous Windows :
```batch
cd docs
make.bat html      # Exécute aussi : git submodule update --init --remote
```

**Remarque** : `make.bat` synchronise automatiquement le sous-module `_shared` avant la compilation. Le Makefile ne le fait pas.

### ReadTheDocs

Compilation automatique lors du push sur la branche `docs`. Configuration dans `.readthedocs.yaml` :
- OS : Ubuntu 22.04, Python 3.11
- Configuration Sphinx : `docs/source/conf.py`
- Sous-modules : inclus (tous, récursif)
- Compile tous les formats (HTML, PDF, ePub)

### URL publiées

```
https://docs.sunfounder.com/projects/ai-lab-kit/fr/latest/
```

---

## Configuration Sphinx (conf.py)

### Extensions

| Extension | Usage |
|---|---|
| `sphinx_copybutton` | Ajoute un bouton de copie aux blocs de code |
| `sphinx_rtd_theme` | Thème ReadTheDocs |
| `sphinx.ext.intersphinx` | Liaison de références inter-projets |

`sphinx.ext.autosectionlabel` est **désactivé** — laisser commenté. Provoque des avertissements de doublons d'étiquettes avec les titres de section CJK.

### Thème

- **Thème** : `sphinx_rtd_theme`
- **Options** : panneau latéral attaché, sélecteurs de version/langue désactivés
- **Intégration GitHub** : Activée, pointant vers `sunfounder/ai-lab-kit` sur la branche `docs`

### Ressources personnalisées

**JavaScript** (chargé dans l'ordre) :
- `https://ezblock.cc/readDocFile/custom.js` — JS personnalisé partagé SunFounder
- `./lang.js` — Détection automatique de la langue et redirection
- Éditeur de code ACE : `ace.js`, `ext-language_tools.js`, `theme-chrome.js`, `mode-python.js`, `mode-sh.js`, `monokai.js`
- Terminal xterm.js : `xterm.js`, `FitAddon.js`
- `readTheDocIndex.js` — Comportement personnalisé des pages

**CSS** :
- `https://ezblock.cc/readDocFile/custom.css` — CSS personnalisé partagé SunFounder
- `readTheDoc/src/css/index.css` — Styles de page personnalisés
- `readTheDoc/src/css/xterm.css` — Styles du terminal

**Template** : `_templates/layout.html` — étend la mise en page RTD par défaut, ajoute la barre de navigation SunFounder avec le logo liant vers `https://sunfounder.com`.

### Multi-langue

Le script `lang.js` dans `_static/` gère la détection automatique de la langue via la langue du navigateur et redirige vers l'URL appropriée.

Les URL publiées suivent le modèle `https://docs.sunfounder.com/projects/ai-lab-kit/<langue>/latest/`.

La variable `language` dans `conf.py` est définie sur `'en'` par défaut. Pour compiler dans d'autres langues :
- Définir `language = '<locale>'` dans `conf.py`
- Ajouter des fichiers de traduction `.po` sous `docs/source/locale/`
- Mettre à jour la substitution `link_<langue>_tutorials` avec la traduction correcte de la description

Langues supportées : `en`, `de`, `es`, `fr`, `it`, `ja`, `zh`.

---

## Tâches de maintenance courantes

### Ajouter une nouvelle leçon Python

1. Créer le fichier `.rst` dans `docs/source/python/` en suivant la convention de nommage
2. Commencer par le modèle standard (include message d'accueil + étiquette ref + titre)
3. Définir un `.. _ref_label:` en haut si la page sera référencée
4. Ajouter le fichier au `.. toctree::` approprié dans `python/play_with_python.rst` sous la bonne section (Output / Input / Camera & Audio / Projects)
5. Si de nouveaux composants sont introduits, ajouter leurs liens d'achat dans `conf.py` `rst_epilog`
6. Compiler localement pour vérifier : `cd docs && make.bat html`
7. Commiter sur `docs`

### Ajouter un nouveau chapitre

1. Créer un répertoire sous `docs/source/` (ex. `nouveau_chapitre/`)
2. Créer l'index de chapitre `.rst` avec le modèle standard + `.. _ref_label:` + toctree
3. Ajouter le chapitre au toctree racine dans `index.rst`
4. Ajouter le `ref_label` à la section de navigation dans `index.rst`
5. Compiler localement pour vérifier

### Mettre à jour le toctree racine

Le toctree racine dans `index.rst` comporte 11 entrées dans cet ordre :

1. **À propos de ce kit** — `self` (auto-référencement)
2. **Premiers pas** — `quick_start/quick_start`
3. **Cours vidéo** — `video_course/video_course`
4. **Jouer avec Python** — `python/play_with_python`
5. **IA (LLM)** — `llm/llm`
6. **OpenCV** — `opencv/opencv`
7. **MediaPipe** — `mediapipe/mediapipe`
8. **YOLO** — `yolo/yolo`
9. **Composants** — `component`
10. **Annexe** — `appendix`
11. **FAQ** — `faq`

### Ajouter du contenu avec des marqueurs Include

Lorsque du contenu doit être partagé entre plusieurs pages :

1. Ajouter `.. start_<marqueur>` avant et `.. end_<marqueur>` après le bloc réutilisable dans le fichier source
2. Dans le fichier de destination, utiliser :
   ```rst
   .. include:: /fichier_source.rst
       :start-after: start_<marqueur>
       :end-before: end_<marqueur>
   ```

### Modifier le sous-module

Le répertoire `docs/source/_shared/` est un sous-module Git pointant vers `https://github.com/sunfounder/sf-shared.git` (branche : `main`). Les modifications des documents de composants partagés, des pages d'annexe ou des guides de démarrage Pi doivent être effectuées dans le dépôt `sf-shared`, pas ici.

Pour mettre à jour le pointeur du sous-module :
```bash
cd docs/source/_shared
git pull origin main
cd ../../..
git add docs/source/_shared
git commit -m "Mise à jour du sous-module _shared"
```

### Vérification des branches linguistiques

La branche `docs` est la **source anglaise** et ne doit jamais contenir de contenu traduit. Après toute opération qui touche le dépôt distant (push, merge, force-push), vérifiez l'intégrité de la branche `docs` et de toutes les branches linguistiques :

**1. Vérifier que `docs` est en anglais :**

```bash
git show remotes/origin/docs:docs/source/conf.py | grep "language ="
# Attendu : language = 'en'
```

Si le `docs` distant affiche une langue autre que l'anglais, restaurez-le immédiatement depuis la source anglaise canonique :

```bash
# Depuis l'espace de travail anglais canonique :
git push origin docs --force
```

**2. Vérifier que chaque branche linguistique a le bon code de langue :**

| Branche | `conf.py` attendu | URL publiée |
|---|---|---|
| `docs` | `language = 'en'` | `/en/latest/` |
| `docs-de` | `language = 'de'` | `/de/latest/` |
| `docs-fr` | `language = 'fr'` | `/fr/latest/` |
| `docs-ja` | `language = 'ja'` | `/ja/latest/` |

Les branches supplémentaires (`docs-es`, `docs-fr`, `docs-it`, `docs-zh`) suivent le même modèle.

**3. Script de vérification rapide pour toutes les branches :**

```bash
for b in docs docs-de docs-fr docs-ja; do
  lang=$(git show "remotes/origin/$b:docs/source/conf.py" 2>/dev/null | grep "language =")
  echo "$b: $lang"
done
```

**4. Lors de la création d'une nouvelle branche linguistique :**

- Toujours créer depuis `docs` (anglais), jamais depuis une autre branche linguistique
- Mettre à jour `conf.py` : définir `language = '<code>'`, commenter `sphinx.ext.autosectionlabel`
- Traduire tous les fichiers `.rst` et `README.md`
- Traduire `CLAUDE.md` et mettre à jour l'identifiant de la branche
- Exécuter `make html` et résoudre tous les avertissements avant de commiter
- **Langues CJK (chinois, japonais)** : les caractères CJK comptent pour 2 colonnes d'affichage — les soulignements/surlignements de section doivent être 2× le nombre de caractères. Le `**markup**` en ligne adjacent aux caractères CJK nécessite `\ ` (espace échappé) comme délimiteur.
- Après le push, vérifier que le contenu de la branche distante correspond à la langue prévue

---

## Notes pour les assistants IA

Lorsque vous travaillez sur ce dépôt :

1. **La branche `docs` est exclusivement dédiée à la documentation.** Le code source du produit et les images système se trouvent sur `main`. N'ajoutez pas de scripts Python, de binaires ou d'images disque à `docs`.
2. **La note de la communauté Facebook** en haut de chaque fichier `.rst` est importée depuis `index.rst` via le bloc include `start_hello_message` / `end_hello_message`. Elle fait partie du standard de documentation SunFounder et apparaît sur presque toutes les pages visibles par l'utilisateur.
3. **Les substitutions de liens `conf.py`** sont la source unique des URL externes. Ne jamais coder en dur des liens externes dans les fichiers `.rst` — utilisez les substitutions `|link_xxx|`.
4. **Les étiquettes de référence** (`.. _label:`) sont des identifiants de code, pas du texte lisible. Ne jamais les traduire.
5. **Les soulignements (et surlignements) de sections RST doivent correspondre à la largeur d'affichage du titre.**
   
   - Pour les titres à soulignement simple (titre suivi de `=` ou `-`), le soulignement doit être au moins aussi long que le texte du titre.
   - Pour les titres à surlignement + soulignement (ex. `====` au-dessus et en dessous du titre), **les deux** — surlignement et soulignement — doivent utiliser le même caractère, avoir la **même longueur exacte** et être au moins aussi longs que le titre. Lors de la traduction des titres, mettez toujours à jour les deux lignes ensemble.
   - **Largeur d'affichage CJK** : docutils compte les caractères CJK comme **2 colonnes d'affichage** chacun (ASCII = 1 colonne). Le surlignement/soulignement doit correspondre à la largeur d'affichage totale, pas au nombre de caractères.
   
   Les titres traduits sont souvent plus longs que les originaux anglais — étendez les surlignements et soulignements en conséquence. Lorsque le titre contient des caractères CJK, le soulignement/surlignement sera significativement plus long que ce que le nombre de caractères suggère.

6. **Le markup en ligne gras (`**...**`) se casse lorsqu'il est adjacent à des caractères CJK.** La reconnaissance du markup en ligne docutils exige que les délimiteurs `**` soient adjacents à des espaces ou à la ponctuation ASCII (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). Les caractères CJK (chinois, japonais, coréen) ne sont **pas** des délimiteurs valides.

   Lorsque `**texte**` est immédiatement précédé ou suivi d'un caractère CJK, docutils émet `WARNING: Inline strong start-string without end-string.` car il ne peut pas trouver le `**` fermant.

   **Correction** : Insérez `\ ` (espace échappé par antislash) entre le délimiteur `**` et le caractère CJK adjacent :

   ```rst
   # FAUX — ** fermant suivi du CJK に, avertissement émis :
   **PI3V3**にブリッジすると

   # CORRECT — \  agit comme un délimiteur valide :
   **PI3V3**\ にブリッジすると

   # FAUX — ** ouvrant précédé du CJK は, avertissement émis :
   または**コマンドラインツール**

   # CORRECT :
   または\ **コマンドラインツール**
   ```

   Cela s'applique également aux autres markups en ligne (`*emphase*`, ```littéral```) lorsqu'ils sont adjacents à du texte CJK. Vérifiez toujours les avertissements de compilation pour "Inline ... start-string without end-string" après avoir traduit du contenu avec du markup en ligne.

7. **Les listes imbriquées nécessitent des lignes vides et une indentation correcte en RST.** Lorsqu'un élément de liste numérotée ou à puces contient des sous-puces, une ligne vide doit précéder la liste imbriquée, et les éléments imbriqués doivent être indentés pour s'aligner avec le texte de l'élément parent (généralement 3+ espaces). Sans la ligne vide, RST rend les puces comme une seule ligne continue.

   **Faux** (sous-puces sans ligne vide) :
   ```rst
   3. **Élément parent** :
      - Premier sous-élément
      - Deuxième sous-élément
   ```

   **Correct** :
   ```rst
   3. **Élément parent** :

        - Premier sous-élément
        - Deuxième sous-élément
   ```

8. **Les blocs de code** (Python, bash, shell) ne sont jamais traduits. Les chaînes de commande et les chemins de fichiers restent tels quels.
9. **Les répertoires `_static` et `_templates`** contiennent des ressources personnalisées. Les modifications ici affectent l'apparence et le comportement globaux du site publié sur toutes les pages.
10. **La sortie de compilation** va dans `docs/build/` et est gitignorée — ne jamais commiter les artefacts de compilation.
11. **Les images** sont toutes sous `docs/source/img/`. Lors de l'ajout de nouvelles images, placez-les là (organisées par sous-répertoire de chapitre) et référencez-les avec des chemins relatifs.
12. **Le sous-module `_shared`** contient du contenu inter-produits (références de composants, annexe, guides de démarrage Pi). Les modifications de ces fichiers doivent passer par le dépôt `sf-shared`, et ne pas être éditées directement ici.
13. **Le script `show`** à la racine du dépôt est un utilitaire d'affichage de licence GPL — il est en syntaxe Python 2 et doit être considéré comme hérité.
14. **La numérotation des fichiers de leçon** suit un schéma cohérent : `X.Y_` pour les leçons Python (où X = section, Y = leçon dans la section), `cv_N_` pour OpenCV, `mp_N_` pour MediaPipe. Lors de l'ajout de leçons dans une section existante, renumérotez soigneusement pour éviter de casser les références croisées.
15. **Le script de compilation Windows `make.bat`** exécute automatiquement `git submodule update --init --remote` avant la compilation. Le `Makefile` ne le fait pas — lorsque vous utilisez `make html` sur Linux/macOS, assurez-vous que le sous-module est à jour manuellement si nécessaire.
