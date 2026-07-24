# Repository della Documentazione di AI Fusion Lab Kit

> **Traduzione italiana.** Questo CLAUDE.md è la versione italiana per il progetto di documentazione di AI Fusion Lab Kit. Il file originale in inglese (canonico) si trova nel branch `docs` del repository principale. Quando vengono aggiunte regole o correzioni, aggiornare prima il file inglese, poi propagare agli altri repository linguistici.

## Identita' del Progetto

| Campo | Valore |
|---|---|
| **Prodotto** | SunFounder AI Fusion Lab Kit — piattaforma di apprendimento AI/elettronica tutto-in-uno |
| **Repository** | `https://github.com/sunfounder/ai-lab-kit` |
| **Documentazione** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Pubblicata su** | `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/` |
| **Azienda** | SunFounder (service@sunfounder.com) |
| **Licenza** | GPL v2 |

AI Fusion Lab Kit combina un kit hardware modulare con moduli di apprendimento passo-passo che coprono programmazione Python, componenti elettronici, visione artificiale (OpenCV, MediaPipe), rilevamento oggetti (YOLO) e modelli linguistici di grandi dimensioni (Ollama, OpenAI, DeepSeek, xAI, Doubao, Qwen, Gemini). Il branch `docs` di questo repository contiene **solo documentazione** — un sito di documentazione Sphinx costruito tramite ReadTheDocs.

---

## Strategia dei Branch

| Branch | Ruolo |
|---|---|
| `main` | Codice sorgente del prodotto, immagine di sistema, installer, esempi |
| `docs` | **Sorgente della documentazione** — file RST Sphinx, immagini, configurazione RTD |

### Regola Cardinale

> **`docs` e' il branch della documentazione.** Tutte le modifiche alla documentazione (contenuto, struttura, immagini, configurazione) avvengono su `docs`. Il branch `main` e' per il codice sorgente del prodotto e le immagini del sistema. Questi due branch servono scopi diversi e non devono essere confusi.

### Branch Linguistici

| Branch | Lingua | `conf.py` `language` | URL Pubblicato |
|---|---|---|---|
| `docs` | Inglese (sorgente) | `'en'` | `/en/latest/` |
| `docs-de` | Tedesco | `'de'` | `/de/latest/` |
| `docs-ja` | Giapponese | `'ja'` | `/ja/latest/` |
| `docs-it` | Italiano | `'it'` | `/it/latest/` |

Ulteriori branch linguistici (`docs-es`, `docs-fr`, `docs-zh`) possono essere creati da `docs` secondo necessita'.

---

## Struttura del Repository (branch docs)

```
ai-lab-kit/
├── .readthedocs.yaml              # Configurazione build RTD (Sphinx 7.3.7, Python 3.11, Ubuntu 22.04)
├── .gitignore                     # Ignora: .vscode, build/, file segreti, backup
├── .gitmodules                    # Sottomodulo: docs/source/_shared → sf-shared.git (main)
├── LICENSE.txt                    # GPL v2
├── README.md                      # Panoramica del prodotto + collegamenti rapidi
├── show.txt                       # Script legacy per visualizzazione licenza GPL
├── CLAUDE.md                      # Questo file — guida per assistenti AI
└── docs/
    ├── requirements.txt           # sphinx==7.3.7, sphinx_rtd_theme==3.0.1, sphinx_copybutton
    ├── Makefile / make.bat        # Build Sphinx (SOURCEDIR=source, BUILDDIR=build)
    └── source/
        ├── conf.py                # Configurazione Sphinx: estensioni, tema, JS/CSS, rst_epilog
        ├── index.rst              # Toctree principale — 11 voci
        ├── faq.rst                # Domande frequenti
        ├── component.rst          # Riferimento componenti (toctree in _shared/component/)
        ├── appendix.rst           # Appendice (toctree in _shared/appendix/)
        ├── quick_start/           # Per iniziare — installazione OS, assemblaggio HAT, configurazione
        │   ├── quick_start.rst    #   Indice del capitolo
        │   ├── install_the_os.rst
        │   ├── fh_install_the_os.rst
        │   ├── fh_set_up_pi.rst
        │   ├── run_installer.rst
        │   ├── assemble_power_hat.rst
        │   └── need_components.rst
        ├── video_course/          # Collegamenti ai corsi video YouTube
        │   └── video_course.rst
        ├── python/                # ~50 esperimenti hardware Python
        │   ├── play_with_python.rst   # Indice del capitolo (Output / Input / Camera & Audio / Progetti)
        │   ├── 1.1_blinking_led_python.rst ... 1.10_oled_screen.rst       # Output (10 lezioni)
        │   ├── 2.1_button_python.rst ... 2.15_10-axis.rst                 # Input (15 lezioni)
        │   ├── 3.1_photograph_python.rst ... 3.4_microphone.rst           # Camera & Audio (4 lezioni)
        │   └── 4.1_camera_python.rst ... 4.16_pan_tilt_camera.rst         # Progetti (16 lezioni)
        ├── llm/                   # AI e Modelli Linguistici di Grandi Dimensioni
        │   ├── llm.rst                # Indice del capitolo
        │   ├── python_tts_espeak_pico2wave.rst  # TTS (eSpeak, pico2wave)
        │   ├── python_tts_piper_openai.rst      # TTS (Piper, OpenAI TTS)
        │   ├── python_ai_assistant.rst          # STT (Vosk)
        │   ├── python_llm_ollama.rst            # LLM locale (Ollama)
        │   ├── python_online_llms.rst           # LLM online (OpenAI, xAI, DeepSeek, Doubao, Qwen, Gemini)
        │   ├── python_local_chatbot.rst         # Progetto chatbot locale
        │   └── python_openai_*.rst              # Progetti basati su OpenAI (salute, ventola, gioco, lampada, ecc.)
        ├── opencv/                # Visione artificiale OpenCV (9 lezioni)
        │   ├── opencv.rst             # Indice del capitolo
        │   └── cv_0_setup.rst ... cv_8_face.rst
        ├── mediapipe/             # Visione AI MediaPipe (12 lezioni)
        │   ├── mediapipe.rst          # Indice del capitolo
        │   └── mp_0_setup.rst ... mp_11_object_track.rst
        ├── yolo/                  # Rilevamento oggetti YOLO (6 lezioni)
        │   ├── yolo.rst               # Indice del capitolo
        │   └── yolo_*.rst
        ├── _shared/               # Sottomodulo Git — contenuti condivisi tra prodotti
        │   ├── component/         #   54 pagine di riferimento componenti
        │   ├── appendix/          #   7 pagine appendice (I2C, SPI, SSH, VNC, FileZilla)
        │   └── pi_start/          #   Guide per iniziare con Raspberry Pi
        ├── _static/
        │   ├── lang.js            # Script di reindirizzamento multilingua
        │   └── video/             # File video incorporati
        ├── _templates/
        │   └── layout.html       # Template HTML Sphinx (barra di navigazione SunFounder con logo)
        └── img/                  # Tutte le immagini della documentazione (organizzate per capitolo)
```

---

## Convenzioni della Documentazione

### Boilerplate dei File RST

Ogni pagina segue questo schema esatto:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

Titolo Pagina
=============
```

I marcatori `start_hello_message` / `end_hello_message` sono definiti in `index.rst` e contengono la nota della community Facebook. La direttiva `.. include::` la inserisce in ogni pagina.

### Etichette di Riferimento

Ogni file `.rst` definisce un'etichetta di riferimento per il collegamento tra documenti. Queste etichette sono identificatori di codice, non testo leggibile — **non tradurle mai**.

Etichette di riferimento principali:

| Etichetta | File | Contenuto |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | Capitolo "Per iniziare" |
| `youtube_list` | `video_course/video_course.rst` | Corso video YouTube |
| `play_with_python` | `python/play_with_python.rst` | Capitolo Python |
| `play_with_llm` | `llm/llm.rst` | Capitolo AI / LLM |
| `play_with_opencv` | `opencv/opencv.rst` | Capitolo OpenCV |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | Capitolo MediaPipe |
| `play_with_yolo` | `yolo/yolo.rst` | Capitolo YOLO |
| `cpn_list` | `component.rst` | Riferimento componenti |
| `faq` | `faq.rst` | Domande frequenti |

Anche le singole lezioni definiscono etichette (ad es., `py_led` in `python/1.1_blinking_led_python.rst`). Queste etichette **devono rimanere coerenti** in tutte le varianti linguistiche — sono il meccanismo di collegamento tra documenti.

### Direttive Include

Il pattern `include` principale in questo progetto e' l'importazione del messaggio di benvenuto:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message
```

I marcatori in `index.rst` usano il formato:
```rst
.. start_hello_message

.. note::
    Ciao, benvenuto nel SunFounder ...

.. end_hello_message
```

Quando il contenuto in questo blocco cambia, influenza ogni pagina che lo include. Garantisci la coerenza durante la modifica.

### Sostituzioni dei Collegamenti (`rst_epilog` in `conf.py`)

Tutti i collegamenti esterni vivono come sostituzioni RST in `conf.py` sotto `rst_epilog`. Ci sono tre gruppi:

**Collegamenti acquisto componenti** (25+ collegamenti per LED, sensori, motori, ecc.):
```rst
.. |link_led_buy| raw:: html
    <a href="https://www.sunfounder.com/products/..." target="_blank">ACQUISTA</a>
```

**Collegamenti tutorial specifici per lingua** (6 lingue):
| Sostituzione | Scopo |
|---|---|
| `\|link_sf_facebook\|` | Community Facebook SunFounder |
| `\|link_en_tutorials\|` | Tutorial online in inglese |
| `\|link_german_tutorials\|` | Tutorial online in tedesco |
| `\|link_jp_tutorials\|` | Tutorial online in giapponese |
| `\|link_es_tutorials\|` | Tutorial online in spagnolo |
| `\|link_fr_tutorials\|` | Tutorial online in francese |
| `\|link_it_tutorials\|` | Tutorial online in italiano |

**Collegamenti di riferimento esterni** (strumenti Raspberry Pi, piattaforme AI, ecc.):
| Sostituzione | Scopo |
|---|---|
| `\|link_rpi_imager\|` | Download Raspberry Pi Imager |
| `\|link_rpi_connect\|` | Raspberry Pi Connect |
| `\|link_ollama\|` | Download Ollama |
| `\|link_ollama_hub\|` | Hub modelli Ollama |
| `\|link_openai_platform\|` | Chiavi API OpenAI |
| `\|link_deepseek\|` | Piattaforma DeepSeek |
| `\|link_grok_ai\|` | Console Cloud xAI |
| `\|link_doubao\|` | Volcengine (Doubao) |
| `\|link_aliyun\|` | Alibaba Bailian (Qwen) |
| `\|link_google_ai\|` | Google AI Studio (Gemini) |
| `\|link_piper_voice\|` | Voci Piper TTS |

Quando aggiungi un nuovo collegamento esterno, aggiungi la definizione `.. |link_xxx|` in `conf.py` `rst_epilog`. Non codificare mai URL esterni nei file `.rst`.

### Percorsi delle Immagini

Tutte le immagini risiedono in `docs/source/img/` e vengono referenziate con percorsi relativi `img/`:

```rst
.. image:: img/led_circuit.png
   :width: 80%
   :align: center
```

Le immagini sono organizzate per capitolo (ad es., `img/python/`, `img/opencv/`, `img/mediapipe/`).

### Convenzioni sui Nomi dei File

- **Lezioni Python**: `X.Y_nome_descrittivo_python.rst` (ad es., `1.1_blinking_led_python.rst`, `2.14_dht_python.rst`)
- **Lezioni OpenCV**: `cv_N_nome_descrittivo.rst` (ad es., `cv_0_setup.rst`, `cv_8_face.rst`)
- **Lezioni MediaPipe**: `mp_N_nome_descrittivo.rst` (ad es., `mp_0_setup.rst`, `mp_7_pose.rst`)
- **Lezioni YOLO**: `yolo_nome_descrittivo.rst`
- **Lezioni LLM**: `python_nome_descrittivo.rst` (ad es., `python_llm_ollama.rst`, `python_openai_health.rst`)
- **Guida rapida**: `snake_case_descrittivo.rst`
- **Indici dei capitoli**: `nome_descrittivo.rst` (ad es., `play_with_python.rst`, `llm.rst`, `opencv.rst`)
- **Pagine principali**: `index.rst`, `faq.rst`, `component.rst`, `appendix.rst`

### Sottolineature delle Sezioni RST

- Titolo (livello superiore): `=====` sopra e sotto il testo
- Sezione: `------` sottolineatura
- Sotto-sezione: `~~~~~~` sottolineatura
- La riga superiore/inferiore deve essere almeno lunga quanto il testo del titolo
- Per titoli CJK: i caratteri CJK contano come 2 colonne di visualizzazione ciascuno; la sottolineatura deve corrispondere alla larghezza di visualizzazione, non al conteggio dei caratteri

---

## Build e Anteprima

### Build Locale (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Output: docs/build/html/index.html
```

Su Windows:
```batch
cd docs
make.bat html      # Esegue anche: git submodule update --init --remote
```

**Nota**: `make.bat` sincronizza automaticamente il sottomodulo `_shared` prima di compilare. Il Makefile no.

### ReadTheDocs

Viene compilato automaticamente al push sul branch `docs`. Configurazione in `.readthedocs.yaml`:
- OS: Ubuntu 22.04, Python 3.11
- Config Sphinx: `docs/source/conf.py`
- Sottomoduli: inclusi (tutti, ricorsivi)
- Compila tutti i formati (HTML, PDF, ePub)

### URL Pubblicati

```
https://docs.sunfounder.com/projects/ai-lab-kit/en/latest/
```

---

## Configurazione Sphinx (conf.py)

### Estensioni

| Estensione | Scopo |
|---|---|
| `sphinx_copybutton` | Aggiunge pulsante copia ai blocchi di codice |
| `sphinx_rtd_theme` | Tema ReadTheDocs |
| `sphinx.ext.intersphinx` | Collegamento tra progetti |

`sphinx.ext.autosectionlabel` e' **disabilitato** — mantenerlo commentato. Causa avvisi di etichette duplicate con titoli in CJK.

### Tema

- **Tema**: `sphinx_rtd_theme`
- **Opzioni**: flyout allegato, selettori versione/lingua disabilitati
- **Integrazione GitHub**: Abilitata, che punta a `sunfounder/ai-lab-kit` sul branch `docs`

### Asset Personalizzati

**JavaScript** (caricati in ordine):
- `https://ezblock.cc/readDocFile/custom.js` — JS personalizzato condiviso SunFounder
- `./lang.js` — Rilevamento automatico della lingua e reindirizzamento
- Editor ACE: `ace.js`, `ext-language_tools.js`, `theme-chrome.js`, `mode-python.js`, `mode-sh.js`, `monokai.js`
- Terminale xterm.js: `xterm.js`, `FitAddon.js`
- `readTheDocIndex.js` — Comportamento personalizzato della pagina

**CSS**:
- `https://ezblock.cc/readDocFile/custom.css` — CSS personalizzato condiviso SunFounder
- `readTheDoc/src/css/index.css` — Stili pagina personalizzati
- `readTheDoc/src/css/xterm.css` — Stili terminale

**Template**: `_templates/layout.html` — estende il layout RTD predefinito, aggiunge barra di navigazione SunFounder con logo che collega a `https://sunfounder.com`.

### Multi-Lingua

Lo script `lang.js` in `_static/` gestisce il rilevamento automatico della lingua tramite la lingua del browser e reindirizza all'URL appropriato.

Gli URL pubblicati seguono lo schema `https://docs.sunfounder.com/projects/ai-lab-kit/<lang>/latest/`.

La variabile `language` in `conf.py` e' impostata su `'en'` per impostazione predefinita. Quando si compila per altre lingue:
- Imposta `language = '<locale>'` in `conf.py`
- Aggiungi file di traduzione `.po` sotto `docs/source/locale/`
- Aggiorna la sostituzione `link_<lang>_tutorials` con la traduzione corretta della descrizione

Lingue supportate: `en`, `de`, `es`, `fr`, `it`, `ja`, `zh`.

---

## Attivita' di Manutenzione Comuni

### Aggiungere una Nuova Lezione Python

1. Crea il file `.rst` in `docs/source/python/` seguendo la convenzione di denominazione
2. Inizia con il boilerplate standard (include messaggio di benvenuto + etichetta ref + titolo)
3. Definisci un `.. _ref_label:` all'inizio se la pagina verra' referenziata
4. Aggiungi il file al `.. toctree::` appropriato in `python/play_with_python.rst` sotto la sezione corretta (Output / Input / Camera & Audio / Progetti)
5. Se vengono introdotti nuovi componenti, aggiungi i loro link di acquisto in `conf.py` `rst_epilog`
6. Compila localmente per verificare: `cd docs && make.bat html`
7. Fai il commit su `docs`

### Aggiungere un Nuovo Capitolo

1. Crea una directory sotto `docs/source/` (ad es., `new_chapter/`)
2. Crea l'indice del capitolo `.rst` con boilerplate standard + `.. _ref_label:` + toctree
3. Aggiungi il capitolo al toctree principale in `index.rst`
4. Aggiungi `ref_label` alla sezione di navigazione in `index.rst`
5. Compila localmente per verificare

### Aggiornare il Toctree Principale

Il toctree principale in `index.rst` ha 11 voci in questo ordine:

1. **Informazioni sul Kit** — `self` (autoriferimento)
2. **Per Iniziare** — `quick_start/quick_start`
3. **Corso Video** — `video_course/video_course`
4. **Gioca con Python** — `python/play_with_python`
5. **AI (LLM)** — `llm/llm`
6. **OpenCV** — `opencv/opencv`
7. **MediaPipe** — `mediapipe/mediapipe`
8. **YOLO** — `yolo/yolo`
9. **Componenti** — `component`
10. **Appendice** — `appendix`
11. **FAQ** — `faq`

### Aggiungere Contenuti con Marcatori Include

Quando il contenuto deve essere condiviso tra pagine:

1. Aggiungi `.. start_<marcatore>` prima e `.. end_<marcatore>` dopo il blocco riutilizzabile nel file sorgente
2. Nel file di destinazione, usa:
   ```rst
   .. include:: /file_sorgente.rst
       :start-after: start_<marcatore>
       :end-before: end_<marcatore>
   ```

### Modificare il Sottomodulo

La directory `docs/source/_shared/` e' un sottomodulo Git che punta a `https://github.com/sunfounder/sf-shared.git` (branch: `main`). Le modifiche ai documenti dei componenti condivisi, alle pagine dell'appendice o alle guide di configurazione del Pi devono essere apportate nel repository `sf-shared`, non qui.

Per aggiornare il puntatore del sottomodulo:
```bash
cd docs/source/_shared
git pull origin main
cd ../../..
git add docs/source/_shared
git commit -m "Update _shared submodule"
```

### Verificare i Branch Linguistici

Il branch `docs` e' la **sorgente inglese** e non deve mai contenere contenuti tradotti. Dopo qualsiasi operazione che tocca il repository remoto (push, merge, force-push), verifica l'integrita' del branch `docs` e di tutti i branch linguistici:

**1. Verifica che `docs` sia in inglese:**

```bash
git show remotes/origin/docs:docs/source/conf.py | grep "language ="
# Previsto: language = 'en'
```

Se il `docs` remoto mostra una lingua diversa dall'inglese, ripristinalo dalla fonte inglese canonica immediatamente:

```bash
# Dall'area di lavoro inglese canonica:
git push origin docs --force
```

**2. Verifica che ogni branch linguistico abbia il codice lingua corretto:**

| Branch | `conf.py` previsto | URL Pubblicato |
|---|---|---|
| `docs` | `language = 'en'` | `/en/latest/` |
| `docs-de` | `language = 'de'` | `/de/latest/` |
| `docs-ja` | `language = 'ja'` | `/ja/latest/` |
| `docs-it` | `language = 'it'` | `/it/latest/` |

Branch aggiuntivi (`docs-es`, `docs-fr`, `docs-zh`) seguono lo stesso schema.

**3. Script di verifica rapida per tutti i branch:**

```bash
for b in docs docs-de docs-ja docs-it; do
  lang=$(git show "remotes/origin/$b:docs/source/conf.py" 2>/dev/null | grep "language =")
  echo "$b: $lang"
done
```

**4. Quando si crea un nuovo branch linguistico:**

- Crea sempre un branch da `docs` (inglese), mai da un altro branch linguistico
- Aggiorna `conf.py`: imposta `language = '<codice>'`, commenta `sphinx.ext.autosectionlabel`
- Traduci tutti i file `.rst` e `README.md`
- Traduci `CLAUDE.md` e aggiorna l'identificatore del branch
- Esegui `make html` e risolvi tutti gli avvisi prima del commit
- **Lingue CJK (Cinese, Giapponese)**: i caratteri CJK contano come 2 colonne di visualizzazione — le righe di sottolineatura/sopralineatura delle sezioni devono essere 2× il conteggio caratteri. Il `**markup**` inline adiacente a caratteri CJK necessita di `\ ` (spazio con escape) come delimitatore.
- Dopo il push, verifica che il contenuto del branch remoto corrisponda alla lingua prevista

---

## Note per gli Assistenti AI

Quando lavori su questo repository:

1. **Il branch `docs` e' solo documentazione.** Il codice sorgente del prodotto e le immagini di sistema risiedono su `main`. Non aggiungere script Python, binari o immagini disco a `docs`.
2. **La nota della community Facebook** all'inizio di ogni file `.rst` viene importata da `index.rst` tramite il blocco include `start_hello_message` / `end_hello_message`. Fa parte dello standard di documentazione SunFounder e appare su quasi tutte le pagine visibili all'utente.
3. **Le sostituzioni di collegamento in `conf.py`** sono l'unica fonte di URL esterni. Non codificare mai collegamenti esterni nei file `.rst` — usa le sostituzioni `|link_xxx|`.
4. **Le etichette di riferimento** (`.. _label:`) sono identificatori di codice, non testo leggibile. Non tradurle mai.
5. **Le righe di sottolineatura (e sopralineatura) delle sezioni RST devono corrispondere alla larghezza di visualizzazione del titolo.**
   
   - Per intestazioni con singola sottolineatura (titolo seguito da `=` o `-`), la sottolineatura deve essere almeno lunga quanto il testo del titolo.
   - Per intestazioni con sopralineatura+sottolineatura (ad es., `====` sopra e sotto il titolo), **entrambe** la sopralineatura e la sottolineatura devono usare lo stesso carattere, essere della **stessa identica lunghezza**, ed essere almeno lunghe quanto il titolo. Quando traduci i titoli, aggiorna sempre entrambe le righe insieme.
   - **Larghezza di visualizzazione CJK**: docutils conta i caratteri CJK come **2 colonne di visualizzazione** ciascuno (ASCII = 1 colonna). La sopralineatura/sottolineatura deve corrispondere alla larghezza di visualizzazione totale, non al conteggio dei caratteri.
   
   I titoli tradotti sono spesso piu' lunghi degli originali inglesi — estendi sopralineature e sottolineature di conseguenza. Quando il titolo contiene caratteri CJK, la sottolineatura/sopralineatura sara' significativamente piu' lunga di quanto suggerito dal conteggio dei caratteri.

6. **Il markup strong inline (`**...**`) si rompe quando e' adiacente a caratteri CJK.** Il riconoscimento del markup inline di docutils richiede che i delimitatori `**` siano adiacenti a spazi bianchi o punteggiatura ASCII (`- : / . , ; ! ? ' " ( ) [ ] { } < >`). I caratteri CJK (Cinese, Giapponese, Coreano) **non** sono delimitatori validi.

   Quando `**testo**` e' immediatamente preceduto o seguito da un carattere CJK, docutils emette `WARNING: Inline strong start-string without end-string.` perche' non riesce a trovare il `**` di chiusura.

   **Soluzione**: Inserisci `\ ` (spazio con escape backslash) tra il delimitatore `**` e il carattere CJK adiacente:

   ```rst
   # SBAGLIATO — ** di chiusura seguito da CJK に, avviso emesso:
   **PI3V3**にブリッジすると

   # GIUSTO — \  agisce come delimitatore valido:
   **PI3V3**\ にブリッジすると

   # SBAGLIATO — ** di apertura preceduto da CJK は, avviso emesso:
   または**コマンドラインツール**

   # GIUSTO:
   または\ **コマンドラインツール**
   ```

   Questo si applica ugualmente ad altri markup inline (`*enfasi*`, ```letterale```) quando adiacenti a testo CJK. Controlla sempre gli avvisi di compilazione per "Inline ... start-string without end-string" dopo aver tradotto contenuti con markup inline.

7. **Gli elenchi annidati richiedono righe vuote e indentazione corretta in RST.** Quando un elemento di un elenco numerato o puntato contiene sotto-elenchi, una riga vuota deve precedere l'elenco annidato, e gli elementi annidati devono essere indentati per allinearsi al testo dell'elemento genitore (tipicamente 3+ spazi). Senza la riga vuota, RST visualizza i punti elenco come un'unica riga continua.

   **Sbagliato** (sotto-elenco senza riga vuota):
   ```rst
   3. **Elemento genitore**:
      - Primo sotto-elemento
      - Secondo sotto-elemento
   ```

   **Giusto**:
   ```rst
   3. **Elemento genitore**:

        - Primo sotto-elemento
        - Secondo sotto-elemento
   ```

8. **I blocchi di codice** (Python, bash, shell) non vengono mai tradotti. Le stringhe di comando e i percorsi dei file rimangono invariati.
9. **Le directory `_static` e `_templates`** contengono asset personalizzati. Le modifiche qui influenzano l'aspetto globale e il comportamento del sito pubblicato su tutte le pagine.
10. **L'output della build** va in `docs/build/` ed e' in gitignore — non fare mai commit degli artefatti di compilazione.
11. **Le immagini** sono tutte sotto `docs/source/img/`. Quando aggiungi nuove immagini, posizionale li' (organizzate per sottodirectory di capitolo) e referenziale con percorsi relativi.
12. **Il sottomodulo `_shared`** contiene contenuti tra prodotti (riferimenti componenti, appendice, guide di configurazione Pi). Le modifiche a questi file devono passare attraverso il repository `sf-shared`, non essere modificate direttamente qui.
13. **Lo script `show`** nella radice del repository e' un'utilita' di visualizzazione della licenza GPL — e' in sintassi Python 2 e dovrebbe essere considerato legacy.
14. **La numerazione dei file delle lezioni** segue uno schema coerente: `X.Y_` per lezioni Python (dove X = sezione, Y = lezione all'interno della sezione), `cv_N_` per OpenCV, `mp_N_` per MediaPipe. Quando aggiungi lezioni all'interno di una sezione esistente, rinumerale con attenzione per evitare di rompere i riferimenti incrociati.
15. **Lo script di build Windows `make.bat`** esegue automaticamente `git submodule update --init --remote` prima di compilare. Il `Makefile` no — quando usi `make html` su Linux/macOS, assicurati che il sottomodulo sia aggiornato manualmente se necessario.
