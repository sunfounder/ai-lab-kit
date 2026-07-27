# Repositorio de documentación de AI Fusion Lab Kit

> **Guía canónica de IA.** Este es el CLAUDE.md traducido al español para el proyecto de documentación de AI Fusion Lab Kit, correspondiente a la rama `docs-es`. El CLAUDE.md original en inglés (rama `docs`) es la fuente autorizada. Las reglas y correcciones se actualizan primero en ese archivo y luego se propagan a los demás repositorios de idiomas.

## Identidad del proyecto

| Campo | Valor |
|---|---|
| **Producto** | SunFounder AI Fusion Lab Kit — plataforma de aprendizaje integral de IA/electrónica |
| **Repositorio** | `https://github.com/sunfounder/ai-lab-kit` |
| **Documentación** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Publicado en** | `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/` |
| **Empresa** | SunFounder (service@sunfounder.com) |
| **Licencia** | GPL v2 |

AI Fusion Lab Kit combina un kit de hardware modular con módulos de aprendizaje paso a paso que cubren programación en Python, componentes electrónicos, visión por computadora (OpenCV, MediaPipe), detección de objetos (YOLO) y modelos de lenguaje grandes (Ollama, OpenAI, DeepSeek, xAI, Doubao, Qwen, Gemini). La rama `docs` de este repositorio contiene **solo documentación** — un sitio de documentación Sphinx construido a través de ReadTheDocs.

---

## Estrategia de ramas

| Rama | Función |
|---|---|
| `main` | Código fuente del producto, imagen del sistema, instalador, ejemplos |
| `docs` | **Fuente de documentación** — archivos Sphinx RST, imágenes, configuración de RTD |

### Regla fundamental

> **`docs` es la rama de documentación.** Todos los cambios de documentación (contenido, estructura, imágenes, configuración) se realizan en `docs`. La rama `main` es para el código fuente del producto y las imágenes. Estas dos ramas tienen propósitos diferentes y no deben confundirse.

### Ramas de idiomas

| Rama | Idioma | `conf.py` `language` | URL publicada |
|---|---|---|---|
| `docs` | English (source) | `'en'` | `/en/latest/` |
| `docs-de` | German | `'de'` | `/de/latest/` |
| `docs-es` | Español | `'es'` | `/es/latest/` |
| `docs-ja` | Japanese | `'ja'` | `/ja/latest/` |

Se pueden crear ramas de idiomas adicionales (`docs-fr`, `docs-it`, `docs-zh`) a partir de `docs` según sea necesario.

---

## Estructura del repositorio (rama docs)

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

## Convenciones de documentación

### Plantilla de archivo RST

Cada página sigue este patrón exacto:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

Page Title
==========
```

Los marcadores `start_hello_message` / `end_hello_message` están definidos en `index.rst` y contienen la nota de la comunidad de Facebook. La directiva `.. include::` la incorpora en cada página.

### Etiquetas de referencia

Cada archivo `.rst` define una etiqueta de referencia para el enlace entre documentos. Estas etiquetas son identificadores de código, no texto legible — **nunca las traduzcas**.

Etiquetas de referencia clave:

| Etiqueta | Archivo | Contenido |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | Capítulo de primeros pasos |
| `youtube_list` | `video_course/video_course.rst` | Curso en video de YouTube |
| `play_with_python` | `python/play_with_python.rst` | Capítulo de Python |
| `play_with_llm` | `llm/llm.rst` | Capítulo de IA / LLM |
| `play_with_opencv` | `opencv/opencv.rst` | Capítulo de OpenCV |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | Capítulo de MediaPipe |
| `play_with_yolo` | `yolo/yolo.rst` | Capítulo de YOLO |
| `cpn_list` | `component.rst` | Referencia de componentes |
| `faq` | `faq.rst` | Preguntas frecuentes |

Las lecciones individuales también definen etiquetas (por ejemplo, `py_led` en `python/1.1_blinking_led_python.rst`). Estas etiquetas **deben mantenerse consistentes** en todas las variantes de idioma — son el mecanismo de enlace entre documentos.

### Directivas Include

El patrón principal de `include` en este proyecto es la importación del mensaje de bienvenida:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
```

Los marcadores en `index.rst` usan el siguiente formato:
```rst
.. start_hello_message

.. note::
    Hello, welcome to the SunFounder ...

.. end_hello_message
```

Cuando el contenido de este bloque cambie, afecta a todas las páginas que lo incluyen. Asegúrate de mantener la coherencia al modificarlo.

### Sustituciones de enlaces (`rst_epilog` en `conf.py`)

Todos los enlaces externos viven como sustituciones RST en `conf.py` bajo `rst_epilog`. Hay tres grupos:

**Enlaces de compra de componentes** (más de 25 enlaces para LEDs, sensores, motores, etc.):
```rst
.. |link_led_buy| raw:: html
    <a href="https://www.sunfounder.com/products/..." target="_blank">BUY</a>
```

**Enlaces de tutoriales por idioma** (6 idiomas):
| Sustitución | Propósito |
|---|---|
| `\|link_sf_facebook\|` | Comunidad de Facebook de SunFounder |
| `\|link_en_tutorials\|` | Tutoriales en línea en inglés |
| `\|link_german_tutorials\|` | Tutoriales en línea en alemán |
| `\|link_jp_tutorials\|` | Tutoriales en línea en japonés |
| `\|link_es_tutorials\|` | Tutoriales en línea en español |
| `\|link_fr_tutorials\|` | Tutoriales en línea en francés |
| `\|link_it_tutorials\|` | Tutoriales en línea en italiano |

**Enlaces de referencia externos** (herramientas Raspberry Pi, plataformas de IA, etc.):
| Sustitución | Propósito |
|---|---|
| `\|link_rpi_imager\|` | Descarga de Raspberry Pi Imager |
| `\|link_rpi_connect\|` | Raspberry Pi Connect |
| `\|link_ollama\|` | Descarga de Ollama |
| `\|link_ollama_hub\|` | Centro de modelos Ollama |
| `\|link_openai_platform\|` | Claves API de OpenAI |
| `\|link_deepseek\|` | Plataforma DeepSeek |
| `\|link_grok_ai\|` | Consola en la nube xAI |
| `\|link_doubao\|` | Volcengine (Doubao) |
| `\|link_aliyun\|` | Alibaba Bailian (Qwen) |
| `\|link_google_ai\|` | Google AI Studio (Gemini) |
| `\|link_piper_voice\|` | Voces de Piper TTS |

Al añadir un nuevo enlace externo, agrega la definición `.. |link_xxx|` en `rst_epilog` de `conf.py`. Nunca uses URLs externas directamente en los archivos `.rst`.

### Rutas de imágenes

Todas las imágenes se encuentran en `docs/source/img/` y se referencian con rutas relativas `img/`:

```rst
.. image:: img/led_circuit.png
   :width: 80%
   :align: center
```

Las imágenes están organizadas por capítulo (por ejemplo, `img/python/`, `img/opencv/`, `img/mediapipe/`).

### Nomenclatura de archivos

- **Lecciones de Python**: `X.Y_nombre_descriptivo_python.rst` (ej., `1.1_blinking_led_python.rst`, `2.14_dht_python.rst`)
- **Lecciones de OpenCV**: `cv_N_nombre_descriptivo.rst` (ej., `cv_0_setup.rst`, `cv_8_face.rst`)
- **Lecciones de MediaPipe**: `mp_N_nombre_descriptivo.rst` (ej., `mp_0_setup.rst`, `mp_7_pose.rst`)
- **Lecciones de YOLO**: `yolo_nombre_descriptivo.rst`
- **Lecciones de LLM**: `python_nombre_descriptivo.rst` (ej., `python_llm_ollama.rst`, `python_openai_health.rst`)
- **Inicio rápido**: `snake_case_descriptivo.rst`
- **Índices de capítulos**: `nombre_descriptivo.rst` (ej., `play_with_python.rst`, `llm.rst`, `opencv.rst`)
- **Páginas raíz**: `index.rst`, `faq.rst`, `component.rst`, `appendix.rst`

### Subrayados de secciones RST

- Título (nivel superior): `=====` con sobrelineado y subrayado
- Sección: `------` subrayado
- Subsección: `~~~~~~` subrayado
- El sobrelineado/subrayado debe tener al menos la misma longitud que el texto del título
- Para títulos CJK: los caracteres CJK cuentan como 2 columnas de visualización cada uno; el subrayado debe coincidir con el ancho de visualización, no con el recuento de caracteres

---

## Construcción y vista previa

### Construcción local (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Output: docs/build/html/index.html
```

En Windows:
```batch
cd docs
make.bat html      # Also runs: git submodule update --init --remote
```

**Nota**: `make.bat` sincroniza automáticamente el submódulo `_shared` antes de construir. El Makefile no lo hace.

### ReadTheDocs

Se construye automáticamente al hacer push a la rama `docs`. Configuración en `.readthedocs.yaml`:
- SO: Ubuntu 22.04, Python 3.11
- Configuración de Sphinx: `docs/source/conf.py`
- Submódulos: incluidos (todos, recursivos)
- Construye todos los formatos (HTML, PDF, ePub)

### URLs publicadas

```
https://docs.sunfounder.com/projects/ai-lab-kit/en/latest/
```

---

## Configuración de Sphinx (conf.py)

### Extensiones

| Extensión | Propósito |
|---|---|
| `sphinx_copybutton` | Añade botón de copia a los bloques de código |
| `sphinx_rtd_theme` | Tema de ReadTheDocs |
| `sphinx.ext.intersphinx` | Enlace de referencias entre proyectos |

`sphinx.ext.autosectionlabel` está **deshabilitado** — mantenlo comentado. Provoca advertencias de etiquetas duplicadas con títulos de sección CJK.

### Tema

- **Tema**: `sphinx_rtd_theme`
- **Opciones**: panel adjunto, selectores de idioma/versión deshabilitados
- **Integración con GitHub**: Habilitada, apuntando a `sunfounder/ai-lab-kit` en la rama `docs`

### Recursos personalizados

**JavaScript** (cargados en orden):
- `https://ezblock.cc/readDocFile/custom.js` — JS personalizado compartido de SunFounder
- `./lang.js` — Detección automática de idioma y redirección multilingüe
- Editor de código ACE: `ace.js`, `ext-language_tools.js`, `theme-chrome.js`, `mode-python.js`, `mode-sh.js`, `monokai.js`
- Terminal xterm.js: `xterm.js`, `FitAddon.js`
- `readTheDocIndex.js` — Comportamiento personalizado de la página

**CSS**:
- `https://ezblock.cc/readDocFile/custom.css` — CSS personalizado compartido de SunFounder
- `readTheDoc/src/css/index.css` — Estilos de página personalizados
- `readTheDoc/src/css/xterm.css` — Estilos de terminal

**Plantilla**: `_templates/layout.html` — extiende el diseño predeterminado de RTD, añade la barra de navegación de SunFounder con logotipo enlazando a `https://sunfounder.com`.

### Multilingüe

El script `lang.js` en `_static/` maneja la detección automática de idioma a través del idioma del navegador y redirige a la URL apropiada.

Las URLs publicadas siguen el patrón `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/`.

La variable `language` en `conf.py` está establecida en `'en'` por defecto. Al construir para otros idiomas:
- Establece `language = '<locale>'` en `conf.py`
- Añade archivos de traducción `.po` en `docs/source/locale/`
- Actualiza la sustitución `link_<lang>_tutorials` con la traducción correcta de la descripción

Idiomas soportados: `en`, `de`, `es`, `fr`, `it`, `ja`, `zh`.

---

## Tareas comunes de mantenimiento

### Añadir una nueva lección de Python

1. Crea el archivo `.rst` en `docs/source/python/` siguiendo la convención de nomenclatura
2. Comienza con la plantilla estándar (incluir mensaje de bienvenida + etiqueta ref + título)
3. Define un `.. _ref_label:` en la parte superior si la página tendrá referencias cruzadas
4. Añade el archivo al `.. toctree::` apropiado en `python/play_with_python.rst` bajo la sección correcta (Output / Input / Camera & Audio / Projects)
5. Si se introducen nuevos componentes, añade sus enlaces de compra a `rst_epilog` en `conf.py`
6. Construye localmente para verificar: `cd docs && make.bat html`
7. Haz commit en `docs`

### Añadir un nuevo capítulo

1. Crea un directorio en `docs/source/` (ej., `new_chapter/`)
2. Crea el archivo `.rst` del índice del capítulo con la plantilla estándar + `.. _ref_label:` + toctree
3. Añade el capítulo al toctree raíz en `index.rst`
4. Añade el `ref_label` a la sección de navegación en `index.rst`
5. Construye localmente para verificar

### Actualizar el toctree raíz

El toctree raíz en `index.rst` tiene 11 entradas en este orden:

1. **About This Kit** — `self` (autorreferenciado)
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

### Añadir contenido con marcadores Include

Cuando el contenido necesita compartirse entre páginas:

1. Añade `.. start_<marcador>` antes y `.. end_<marcador>` después del bloque reutilizable en el archivo fuente
2. En el archivo de destino, usa:
   ```rst
   .. include:: /source_file.rst
       :start-after: start_<marcador>
       :end-before: end_<marcador>
   ```

### Modificar el submódulo

El directorio `docs/source/_shared/` es un submódulo Git que apunta a `https://github.com/sunfounder/sf-shared.git` (rama: `main`). Los cambios en la documentación compartida de componentes, páginas de apéndice o guías de configuración de Pi deben realizarse en el repositorio `sf-shared`, no aquí.

Para actualizar el puntero del submódulo:
```bash
cd docs/source/_shared
git pull origin main
cd ../../..
git add docs/source/_shared
git commit -m "Update _shared submodule"
```

### Verificar las ramas de idiomas

La rama `docs` es la **fuente en inglés** y nunca debe contener contenido traducido. Después de cualquier operación que toque el repositorio remoto (push, merge, force-push), verifica la integridad de la rama `docs` y de todas las ramas de idiomas:

**1. Verificar que `docs` esté en inglés:**

```bash
git show remotes/origin/docs:docs/source/conf.py | grep "language ="
# Esperado: language = 'en'
```

Si la rama remota `docs` muestra un idioma que no sea inglés, restáurala desde la fuente canónica en inglés inmediatamente:

```bash
# Desde el espacio de trabajo canónico en inglés:
git push origin docs --force
```

**2. Verificar que cada rama de idioma tenga el código de idioma correcto:**

| Rama | `conf.py` esperado | URL publicada |
|---|---|---|
| `docs` | `language = 'en'` | `/en/latest/` |
| `docs-de` | `language = 'de'` | `/de/latest/` |
| `docs-es` | `language = 'es'` | `/es/latest/` |
| `docs-ja` | `language = 'ja'` | `/ja/latest/` |

Las ramas adicionales (`docs-fr`, `docs-it`, `docs-zh`) siguen el mismo patrón.

**3. Script de verificación rápida para todas las ramas:**

```bash
for b in docs docs-de docs-ja docs-es; do
  lang=$(git show "remotes/origin/$b:docs/source/conf.py" 2>/dev/null | grep "language =")
  echo "$b: $lang"
done
```

**4. Al crear una nueva rama de idioma:**

- Siempre crea la rama desde `docs` (inglés), nunca desde otra rama de idioma
- Actualiza `conf.py`: establece `language = '<código>'`, comenta `sphinx.ext.autosectionlabel`
- Traduce todos los archivos `.rst` y `README.md`
- Traduce `CLAUDE.md` y actualiza el identificador de la rama
- Ejecuta `make html` y resuelve todas las advertencias antes de hacer commit
- **Idiomas CJK (chino, japonés)**: los caracteres CJK cuentan como 2 columnas de visualización — los sobrelineados/subrayados de sección deben ser 2× el recuento de caracteres. El marcado `**` en línea adyacente a caracteres CJK necesita `\ ` (espacio escapado) como delimitador.
- Después de hacer push, verifica que el contenido de la rama remota coincida con el idioma previsto

---

## Notas para asistentes de IA

Al trabajar en este repositorio:

1. **La rama `docs` es solo de documentación.** El código fuente del producto y las imágenes del sistema están en `main`. No añadas scripts de Python, binarios o imágenes de disco a `docs`.
2. **La nota de la comunidad de Facebook** en la parte superior de cada archivo `.rst` se importa desde `index.rst` mediante el bloque include `start_hello_message` / `end_hello_message`. Es parte del estándar de documentación de SunFounder y aparece en casi todas las páginas dirigidas al usuario.
3. **Las sustituciones de enlaces en `conf.py`** son la fuente única de URLs externas. Nunca uses URLs externas directamente en archivos `.rst` — usa las sustituciones `|link_xxx|`.
4. **Las etiquetas de referencia** (`.. _label:`) son identificadores de código, no texto legible. Nunca las traduzcas.
5. **Los subrayados (y sobrelineados) de secciones RST deben coincidir con el ancho de visualización del título.**

   - Para encabezados con un solo subrayado (título seguido de `=` o `-`), el subrayado debe tener al menos la misma longitud que el texto del título.
   - Para encabezados con sobrelineado+subrayado (ej., `====` encima y debajo del título), **ambos**, el sobrelineado y el subrayado, deben usar el mismo carácter, tener la **misma longitud exacta** y ser al menos tan largos como el título. Al traducir títulos, actualiza siempre ambas líneas juntas.
   - **Ancho de visualización CJK**: docutils cuenta los caracteres CJK como **2 columnas de visualización** cada uno (ASCII = 1 columna). El sobrelineado/subrayado debe coincidir con el ancho de visualización total, no con el recuento de caracteres.

   Los títulos traducidos suelen ser más largos que los originales en inglés — extiende los sobrelineados y subrayados en consecuencia. Cuando el título contiene caracteres CJK, el subrayado/overline será significativamente más largo de lo que sugiere el recuento de caracteres.

6. **El marcado strong en línea (`**...**`) se rompe cuando está adyacente a caracteres CJK.** El reconocimiento de marcado en línea de docutils requiere que los delimitadores `**` estén adyacentes a espacios en blanco o puntuación ASCII (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). Los caracteres CJK (chino, japonés, coreano) **no** son delimitadores válidos.

   Cuando `**texto**` está inmediatamente precedido o seguido por un caracter CJK, docutils emite `WARNING: Inline strong start-string without end-string.` porque no puede encontrar el `**` de cierre.

   **Solución**: Inserta `\ ` (espacio escapado con barra invertida) entre el delimitador `**` y el caracter CJK adyacente:

   ```rst
   # INCORRECTO — cierre ** seguido de CJK に, se emite advertencia:
   **PI3V3**にブリッジすると

   # CORRECTO — \  actúa como delimitador válido:
   **PI3V3**\ にブリッジすると

   # INCORRECTO — apertura ** precedida de CJK は, se emite advertencia:
   または**コマンドラインツール**

   # CORRECTO:
   または\ **コマンドラインツール**
   ```

   Esto aplica igualmente a otro marcado en línea (`*emphasis*`, `` `literal` ``) cuando está adyacente a texto CJK. Siempre revisa las advertencias de compilación en busca de "Inline ... start-string without end-string" después de traducir contenido con marcado en línea.

7. **Las listas anidadas requieren líneas en blanco y sangría correcta en RST.** Cuando un elemento de lista numerada o con viñetas contiene subviñetas, debe preceder una línea en blanco a la lista anidada, y los elementos anidados deben estar sangrados para alinearse con el texto del elemento padre (típicamente 3+ espacios). Sin la línea en blanco, RST renderiza las viñetas como una sola línea continua.

   **Incorrecto** (subviñetas sin línea en blanco):
   ```rst
   3. **Elemento padre**:
      - Primer subelemento
      - Segundo subelemento
   ```

   **Correcto**:
   ```rst
   3. **Elemento padre**:

        - Primer subelemento
        - Segundo subelemento
   ```

8. **Los bloques de código** (Python, bash, shell) nunca se traducen. Las cadenas de comando y las rutas de archivo se mantienen intactas.
9. **Los directorios `_static` y `_templates`** contienen recursos personalizados. Los cambios aquí afectan la apariencia y el comportamiento global del sitio publicado en todas las páginas.
10. **La salida de compilación** va a `docs/build/` y está en gitignore — nunca hagas commit de los artefactos de compilación.
11. **Las imágenes** están todas en `docs/source/img/`. Al añadir nuevas imágenes, colócalas allí (organizadas por subdirectorio de capítulo) y haz referencia con rutas relativas.
12. **El submódulo `_shared`** contiene contenido transversal entre productos (referencias de componentes, apéndice, guías de configuración de Pi). Los cambios en estos archivos deben realizarse a través del repositorio `sf-shared`, no editarse directamente aquí.
13. **El script `show`** en la raíz del repositorio es una utilidad de visualización de licencia GPL — usa sintaxis Python 2 y debe considerarse heredado.
14. **La numeración de archivos de lecciones** sigue un esquema consistente: `X.Y_` para lecciones de Python (donde X = sección, Y = lección dentro de la sección), `cv_N_` para OpenCV, `mp_N_` para MediaPipe. Al añadir lecciones dentro de una sección existente, renumerar con cuidado para evitar romper referencias cruzadas.
15. **El script de compilación `make.bat` para Windows** ejecuta automáticamente `git submodule update --init --remote` antes de compilar. El `Makefile` no lo hace — al usar `make html` en Linux/macOS, asegúrate de que el submódulo esté actualizado manualmente si es necesario.
