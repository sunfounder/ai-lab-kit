# AI Fusion Lab Kit Dokumentations-Repository (Deutsch)

> **Kanonische KI-Anleitung.** Dies ist die autoritative CLAUDE.md für das AI Fusion Lab Kit Dokumentationsprojekt (deutsche Sprachvariante). Alle Regeln und Korrekturen sollten zuerst in der englischen Quelle (`docs`-Branch) aktualisiert und dann in diesen Branch übernommen werden.

## Projektidentität

| Feld | Wert |
|---|---|
| **Produkt** | SunFounder AI Fusion Lab Kit — All-in-One KI-/Elektronik-Lernplattform |
| **Repository** | `https://github.com/sunfounder/ai-lab-kit` |
| **Dokumentation** | Sphinx + ReadTheDocs (`sphinx_rtd_theme`) |
| **Veröffentlicht unter** | `https://docs.sunfounder.com/projects/ai-lab-kit/de/latest/` |
| **Unternehmen** | SunFounder (service@sunfounder.com) |
| **Lizenz** | GPL v2 |

Das AI Fusion Lab Kit kombiniert ein modulares Hardware-Kit mit Schritt-für-Schritt-Lernmodulen zu Python-Programmierung, elektronischen Komponenten, Computer Vision (OpenCV, MediaPipe), Objekterkennung (YOLO) und großen Sprachmodellen (Ollama, OpenAI, DeepSeek, xAI, Doubao, Qwen, Gemini). Dieser Branch (`docs-de`) enthält die **deutsche Übersetzung** der Dokumentation.

---

## Branch-Strategie

| Branch | Rolle |
|---|---|
| `main` | Produkt-Quellcode, System-Image, Installer, Beispiele |
| `docs` | **Englische Dokumentationsquelle** — Sphinx RST-Dateien, Bilder, RTD-Konfiguration |
| `docs-de` | **Deutsche Übersetzung** — übersetzte RST-Dateien, `language = 'de'` |

### Grundregel

> **`docs` ist der englische Quell-Branch.** Alle neuen Inhalte und strukturellen Änderungen werden zuerst auf `docs` erstellt und dann in die Sprach-Branches (`docs-de`, `docs-ja`, etc.) übersetzt. Die Sprach-Branches enthalten ausschließlich übersetzte Inhalte.

### Sprach-Branches

| Branch | Sprache | `conf.py` `language` | Veröffentlichte URL |
|---|---|---|---|
| `docs` | Englisch (Quelle) | `'en'` | `/en/latest/` |
| `docs-de` | Deutsch | `'de'` | `/de/latest/` |
| `docs-ja` | Japanisch | `'ja'` | `/ja/latest/` |

Weitere Sprach-Branches (`docs-es`, `docs-fr`, `docs-it`, `docs-zh`) können bei Bedarf von `docs` aus erstellt werden.

---

## Repository-Struktur (docs-de Branch)

```
ai-lab-kit/
├── .readthedocs.yaml              # RTD Build-Konfiguration
├── .gitignore                     # Ignoriert: .vscode, build/, geheime Dateien, Backups
├── .gitmodules                    # Submodul: docs/source/_shared → sf-shared.git (main)
├── LICENSE.txt                    # GPL v2
├── README.md                      # Produktübersicht + Quick-Links (übersetzt)
├── show.txt                       # Legacy GPL-Lizenzanzeige-Skript
├── CLAUDE.md                      # Diese Datei — KI-Assistent-Anleitung
└── docs/
    ├── requirements.txt           # sphinx==7.3.7, sphinx_rtd_theme==3.0.1, sphinx_copybutton
    ├── Makefile / make.bat        # Sphinx-Build (SOURCEDIR=source, BUILDDIR=build)
    └── source/
        ├── conf.py                # Sphinx-Konfig: Erweiterungen, Theme, JS/CSS, rst_epilog
        ├── index.rst              # Root-Toctree — 11 Einträge
        ├── faq.rst                # Häufig gestellte Fragen
        ├── component.rst          # Komponentenreferenz (Toctree in _shared/component/)
        ├── appendix.rst           # Anhang (Toctree in _shared/appendix/)
        ├── quick_start/           # Erste Schritte — OS-Installation, HAT-Montage, Setup
        ├── video_course/          # YouTube-Videokurs-Links
        ├── python/                # ~50 Python-Hardware-Experimente
        ├── llm/                   # KI & Large Language Models
        ├── opencv/                # OpenCV Computer Vision (9 Lektionen)
        ├── mediapipe/             # MediaPipe KI Vision (12 Lektionen)
        ├── yolo/                  # YOLO Objekterkennung (6 Lektionen)
        ├── _shared/               # Git Submodul — produktübergreifende Inhalte
        ├── _static/
        │   ├── lang.js            # Mehrsprachen-Weiterleitungsskript
        │   └── video/             # Eingebettete Videodateien
        ├── _templates/
        │   └── layout.html        # Sphinx HTML-Template (SunFounder Nav-Leiste mit Logo)
        └── img/                   # Alle Dokumentationsbilder (nach Kapitel organisiert)
```

---

## Dokumentationskonventionen

### RST-Datei-Boilerplate

Jede Seite folgt diesem exakten Muster:

```rst
.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _ref_label:

Seitentitel
============
```

Die Marker `start_hello_message` / `end_hello_message` sind in `index.rst` definiert und enthalten den Facebook-Community-Hinweis. Die `.. include::`-Direktive fügt ihn in jede Seite ein.

### Referenz-Labels

Jede `.rst`-Datei definiert ein Referenz-Label für dokumentübergreifende Verlinkungen. Diese Labels sind Code-Identifikatoren, kein lesbarer Text — **niemals übersetzen**.

Wichtige Referenz-Labels:

| Label | Datei | Inhalt |
|---|---|---|
| `get_start` | `quick_start/quick_start.rst` | Kapitel „Erste Schritte" |
| `youtube_list` | `video_course/video_course.rst` | YouTube-Videokurs |
| `play_with_python` | `python/play_with_python.rst` | Python-Kapitel |
| `play_with_llm` | `llm/llm.rst` | KI / LLM-Kapitel |
| `play_with_opencv` | `opencv/opencv.rst` | OpenCV-Kapitel |
| `play_with_mediapipe` | `mediapipe/mediapipe.rst` | MediaPipe-Kapitel |
| `play_with_yolo` | `yolo/yolo.rst` | YOLO-Kapitel |
| `cpn_list` | `component.rst` | Komponentenreferenz |
| `faq` | `faq.rst` | Häufig gestellte Fragen |

Einzelne Lektionen definieren ebenfalls Labels (z. B. `py_led` in `python/1.1_blinking_led_python.rst`). Diese Labels **müssen über alle Sprachvarianten hinweg konsistent bleiben**.

### Link-Ersetzungen (`rst_epilog` in `conf.py`)

Alle externen Links werden als RST-Ersetzungen in `conf.py` unter `rst_epilog` definiert. Externe URLs niemals direkt in `.rst`-Dateien hartkodieren — `|link_xxx|`-Ersetzungen verwenden.

### Bildpfade

Alle Bilder befinden sich unter `docs/source/img/` und werden mit relativen `img/`-Pfaden referenziert. Bilder sind nach Kapitel organisiert (z. B. `img/python/`, `img/opencv/`, `img/mediapipe/`).

### RST-Überschriften-Unterstreichungen

- Titel (oberste Ebene): `=====` Über- und Unterstreichung
- Abschnitt: `------` Unterstreichung
- Unterabschnitt: `~~~~~~` Unterstreichung
- Die Über-/Unterstreichung muss mindestens so lang wie der Titeltext sein
- **CJK-Zeichen zählen als 2 Anzeigespalten** — die Unterstreichung muss der Anzeigebreite entsprechen, nicht der Zeichenanzahl

### Wichtige RST-Regeln

1. **Referenz-Labels niemals übersetzen** — sie sind Code-Identifikatoren.
2. **Code-Blöcke** (Python, Bash, Shell) werden niemals übersetzt.
3. **`conf.py` Link-Ersetzungen** sind die einzige Quelle für externe URLs.
4. **Inline-Markup** (`**...**`) neben CJK-Zeichen benötigt `\ ` (escapiertes Leerzeichen) als Trennzeichen.
5. **Verschachtelte Listen** benötigen Leerzeilen und korrekte Einrückung.
6. **Build-Ausgaben** nach `docs/build/` sind gitignoriert — niemals Build-Artefakte committen.
7. **Das `_shared`-Submodul** enthält produktübergreifende Inhalte — Änderungen müssen über das `sf-shared`-Repository erfolgen.
8. **Lektions-Nummerierung** folgt einem konsistenten Schema: `X.Y_` für Python-Lektionen, `cv_N_` für OpenCV, `mp_N_` für MediaPipe.

---

## Build & Vorschau

### Lokaler Build (Sphinx)

```bash
cd docs
pip install -r requirements.txt
make html          # Ausgabe: docs/build/html/index.html
```

Unter Windows:
```batch
cd docs
make.bat html      # Führt auch: git submodule update --init --remote
```

### ReadTheDocs

Automatischer Build bei Push auf den `docs-de`-Branch. Konfiguration in `.readthedocs.yaml`.

### Veröffentlichte URLs

```
https://docs.sunfounder.com/projects/ai-lab-kit/de/latest/
```

---

## Häufige Wartungsaufgaben

### Eine neue Lektion aus dem Englischen synchronisieren

1. Die neue `.rst`-Datei aus dem `docs`-Branch in den `docs-de`-Branch kopieren
2. Alle benutzerdefinierten Texte ins Deutsche übersetzen
3. Code-Blöcke, Dateipfade und Referenz-Labels unverändert lassen
4. Sicherstellen, dass die RST-Überschriften die korrekte Unterstreichungslänge haben
5. Lokal bauen und auf Warnungen prüfen: `cd docs && make.bat html`
6. Auf `docs-de` committen

### Einen neuen Sprach-Branch erstellen

- Immer von `docs` (Englisch) abzweigen, niemals von einem anderen Sprach-Branch
- `conf.py` aktualisieren: `language = '<code>'` setzen
- Alle `.rst`-Dateien und `README.md` übersetzen
- `CLAUDE.md` übersetzen und die Branch-Kennung aktualisieren
- `make html` ausführen und alle Warnungen vor dem Commit beheben
- Nach dem Push den Inhalt des Remote-Branches auf die korrekte Sprache prüfen

---

## Hinweise für KI-Assistenten

Bei der Arbeit an diesem Repository:

1. **Der `docs-de`-Branch enthält nur Dokumentation.** Produkt-Quellcode und System-Images befinden sich auf `main`.
2. **Der Facebook-Community-Hinweis** am Anfang jeder `.rst`-Datei wird aus `index.rst` über den `start_hello_message`-Include-Block importiert.
3. **`conf.py` Link-Ersetzungen** sind die einzige Quelle für externe URLs. Niemals externe Links in `.rst`-Dateien hartkodieren.
4. **Referenz-Labels** (`.. _label:`) sind Code-Identifikatoren. Niemals übersetzen.
5. **Code-Blöcke** (Python, Bash, Shell) werden niemals übersetzt.
6. **Das `_shared`-Submodul** enthält produktübergreifende Inhalte. Änderungen müssen über das `sf-shared`-Repository erfolgen.
7. **Build-Ausgaben** gehören nach `docs/build/` und sind gitignoriert.
8. **Bilder** befinden sich alle unter `docs/source/img/`.
9. **Das `show`-Skript** im Repo-Root ist ein Legacy-GPL-Lizenzanzeige-Tool (Python-2-Syntax).
10. **Die `make.bat`** unter Windows synchronisiert automatisch das `_shared`-Submodul vor dem Build.
