# Tarjoman Universal Translation Suite (موتور جامع ترجمه «ترجمان»)

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Multi-Agent](https://img.shields.io/badge/Agents-Claude%20Code%20%7C%20Hermes%20%7C%20Cursor-orange.svg)](#multi-agent-ecosystem)
[![Domains](https://img.shields.io/badge/Domains-10%20Specialized%20Profiles-success.svg)](#10-domain-taxonomy--capabilities-matrix)
[![Zero Em-Dash](https://img.shields.io/badge/Typography-Zero%20Em--Dash-purple.svg)](#persian-typography--anti-calque-guarantees)
[![Typst Native](https://img.shields.io/badge/Publishing-Typst%20%2B%20HTML%20Reader-red.svg)](#publishing-output-showcase)
[![CI Tests](https://img.shields.io/badge/Tests-96%20Passing-brightgreen.svg)](#testing-and-verification)

**The Definitive Open-Source Persian Translation Suite & Multi-Agent Skillpack**

*High-fidelity English-to-Persian translation across 10 specialized domains, featuring an autonomous 5-pass human-reflection pipeline, anti-calque purification, strict Persian typography, and publication-ready Typst & HTML exports.*

[Key Features](#key-features) •
[Architecture](#architecture-diagram) •
[10-Domain Taxonomy](#10-domain-taxonomy--capabilities-matrix) •
[Comparison](#comparison-matrix) •
[Quickstart](#quickstart-guides) •
[Publishing Showcase](#publishing-output-showcase) •
[Contributing](#contributing)

</div>

---

## The Value Proposition

Translating English into Persian using raw Large Language Models (LLMs) or classical Machine Translation (MT) services (such as Google Translate or DeepL) routinely produces prose plagued by:

- **Linguistic Calques (گرته‌برداری‌های نحوی)**: Blind translation of passive structures (e.g., using «توسط» for passive voice agent, or «روی چیزی حساب کردن» for *counting on something*).
- **Broken Typography**: Foreign em-dashes (`—`), straight ASCII quotation marks (`"..."`), missing zero-width non-joiners (نیم‌فاصله‌ها), and Arabic character pollutions (`ي` and `ك`).
- **Unnatural Literary Voice**: Mechanical attribution in dialogue (e.g. *«او گفت»* placed awkwardly at the front rather than inverted inside natural Persian speech rhythms).
- **Bidi & Formula Corruption**: Inverting mathematical symbols, scrambling English code fences, and mistranslating international standard terms.
- **Context Amnesia in Long Books**: Inconsistent character names and terminology drift across multi-chapter book projects.

**Tarjoman** solves this comprehensively. Combining specialized linguistic domain profiles, a 5-pass reflective pipeline, strict rule-based anti-calque engines, and multi-agent skillpacks for **Claude Code**, **Hermes**, and **Cursor**, Tarjoman delivers publication-grade Persian texts ready for print or web publication.

---

## Key Features

- 🏛️ **10 Specialized Domain Profiles**: From literary fiction and continental philosophy to clinical medical research, statutory legal contracts, and developer documentation.
- 🔄 **5-Pass Reflection Pipeline**: Human-translator emulation through *Drafting*, *Terminology Alignment*, *Anti-Calque Cleansing*, *Cadence Polishing*, and *MQM Quality Auditing*.
- 🛡️ **Anti-Calque & Purity Engine**: Detects and eliminates structural and lexical loan-translations with rule-backed severity reporting.
- 📐 **Zero Em-Dash & Persian Typography**: Automatic conversion of em-dashes into balanced Persian syntactic equivalents, guillemets (`«...»`), and standard ZWNJ half-spaces.
- 📚 **Book-Scale Translation Memory**: Resumable chapter cache, progress manifests, and dynamic terminology extraction (`terms.tsv`).
- 🖨️ **Publication-Ready Multi-Format Composers**:
  - **Typst PDF**: Flawless Persian bidirectional typesetting (A4 paper or Book layout with Vazirmatn font).
  - **Interactive HTML Reader**: Side-by-side synchronized bilingual reading with glassmorphism UI and search.
  - **Bilingual Markdown**: Segment-aligned tables for revision and human post-editing.
- 🤖 **Universal Multi-Agent Native Skillpacks**: Native integrations for **Claude Code CLI** (`/tarjoman`), **Hermes Autonomous Agent**, and **Cursor / Windsurf** (`.cursorrules`).

---

## Architecture Diagram

```
                              ┌──────────────────────────┐
                              │  Source English Content  │
                              │ (Article / Chapter / Doc)│
                              └────────────┬─────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TARJOMAN 5-PASS REFLECTION PIPELINE                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  Stage 1: Domain Classification & Routing                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ DomainRouter (Heuristic Keyword Density & Statistical Classifier)                │  │
│  │ Selects 1 of 10 Profiles: Literary | Scientific | Philosophy | Legal | Tech ...  │  │
│  └───────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                      ▼                                                 │
│  Stage 2: Contextual Drafting & Dynamic Termbase                                       │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Context-aware segment translation with domain terminology & few-shot grounding   │  │
│  └───────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                      ▼                                                 │
│  Stage 3: Anti-Calque Cleansing & Persian Typography                                   │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ • Regex-driven banned calque replacement (e.g. passive «توسط», «به عنوانِ»)      │  │
│  │ • Zero Em-dash enforcement (— -> parentheses/commas)                             │  │
│  │ • Character normalization (ي/ك -> ی/ک) & Persian quotes («...»)                  │  │
│  └───────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                      ▼                                                 │
│  Stage 4: Cadence & Tone Polishing                                                     │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ • Dialogue inversion (e.g. «گفت فلان» -> گفت‌وگوی روان)                          │  │
│  │ • Etymological precision, bidi code fence isolation, and rhythmic flow           │  │
│  └───────────────────────────────────┬──────────────────────────────────────────────┘  │
│                                      ▼                                                 │
│  Stage 5: Multidimensional Quality Metric (MQM) Audit                                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Automated audit evaluating omission, terminology compliance, and typography      │  │
│  └───────────────────────────────────┬──────────────────────────────────────────────┘  │
└──────────────────────────────────────┼─────────────────────────────────────────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
 ┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
 │  Typst PDF Composer  │   │ Interactive HTML     │   │  Bilingual Markdown  │
 │  • A4 Academic / Book│   │  • Side-by-Side Dual │   │  • Aligned Table     │
 │  • Native Persian RTL│   │  • Synchronized Scroll│  │  • Post-Editing      │
 │  • Vector Typography │   │  • Offline Portable  │   │  • Git-trackable     │
 └──────────────────────┘   └──────────────────────┘   └──────────────────────┘
            │                          │                          │
            └──────────────────────────┼──────────────────────────┘
                                       ▼
            ┌─────────────────────────────────────────────────────┐
            │               MULTI-AGENT INTERFACES                │
            │  Claude Code (/tarjoman) | Hermes | Cursor Rules    │
            └─────────────────────────────────────────────────────┘
```

---

## 10-Domain Taxonomy & Capabilities Matrix

| Domain ID | English Title | نام فارسی دامنه | Key Stylistic & Linguistic Rules | Primary Use Cases |
|:---|:---|:---|:---|:---|
| `literary` | **Literary & Fiction** | ادبی، رمان و داستان | Dialogue attribution inversion, rhythmic cadence, zero em-dash, rich sensory vocabulary. | Fiction, novels, drama, narrative non-fiction. |
| `scientific` | **Scientific & Academic** | علمی، دانشگاهی و مقالات | Strict formula/code isolation, standard Academy terms, LTR citation markers, formal prose. | Journal papers, university theses, academic textbooks. |
| `philosophy` | **Philosophy & Thought** | فلسفه و علوم انسانی | Heideggerian/existential etymological rigor, conceptual precision, avoidance of modern buzzwords. | Continental & analytic philosophy, critical theory, ethics. |
| `legal` | **Legal & Contracts** | حقوقی و اسناد رسمی | Zero ambiguity, statutory terminology (قانون مدنی), preservation of condition clauses, solemn register. | Commercial contracts, treaties, court documents, terms of service. |
| `technical` | **Software & Engineering** | فنی، نرم‌افزار و مهندسی | Unaltered code blocks, untouched CLI flags, Persian-first documentation prose, exact technical glossary. | Developer docs, API references, architecture guides, tutorials. |
| `medical` | **Medical & Clinical** | پزشکی و داروسازی | INN generic drug names, clinical precision, precise dosages, pathology and diagnostic terminology. | Clinical trials, medical textbooks, patient guidelines. |
| `media` | **Media & Journalism** | رسانه‌ای و ژورنالیسم | Inverted pyramid structure, punchy active headlines, concise narrative flow, objective tone. | News dispatches, press releases, editorial journalism. |
| `financial` | **Finance & Economics** | مالی، اقتصاد و بازرگانی | IFRS/GAAP accounting terminology, macro/micro indicators, balance sheet standards, analytical tone. | Annual reports, investment analyses, financial audits. |
| `classical` | **Classical & Historical** | متون کهن و تاریخی | Archaic register, rhythmic eloquence, traditional syntactic constructions, historic titles. | Medieval chronicles, ancient manuscripts, classical epics. |
| `transcreation` | **Creative & Advertising** | بازآفرینی خلاق و تبلیغات | Cultural adaptation over literalism, emotional resonance, memorable taglines, localized idioms. | Brand campaigns, marketing copy, slogans, product landing pages. |

---

## Comparison Matrix

| Feature / Metric | Tarjoman Master Suite | Raw GPT-4 / Claude | Google / DeepL |
|:---|:---:|:---:|:---:|
| **Linguistic Calque Elimination (گرته‌برداری)** | ✅ **Automated & Rule-Backed** | ⚠️ Unreliable / Inconsistent | ❌ Rampant (Literal English calques) |
| **Zero Em-Dash Guarantee** | ✅ **100% Guaranteed** | ❌ Frequently outputs `—` | ❌ Retains English `—` |
| **Persian Quotes («...»)** | ✅ **Enforced via Linter** | ⚠️ Frequently uses `"` or `“”` | ❌ Uses ASCII `"` |
| **Dialogue Attribution Inversion** | ✅ **Built into Literary Engine** | ❌ Places "او گفت" first | ❌ Robotic word-order |
| **10 Domain-Specific Registries** | ✅ **Built-in Registry & Routing** | ❌ Generic general prompting | ❌ Single generic statistical model |
| **Code & Formula Bidi Isolation** | ✅ **Strict RTL/LTR Fencing** | ⚠️ Often breaks equation direction | ❌ Scrambles mixed math/Persian |
| **Book Translation Resumable Memory** | ✅ **Manifest + Dynamic Termbase** | ❌ Context window overflow | ❌ Not supported |
| **Multi-Agent Skillpack (Claude / Hermes / Cursor)** | ✅ **Native Bundles Included** | ❌ Manual setup required | ❌ None |
| **Typeset Typst PDF Output** | ✅ **Native RTL PDF Generator** | ❌ Plain text only | ❌ Plain text only |
| **Interactive Bilingual HTML Reader** | ✅ **Single-File Synchronized Reader** | ❌ None | ❌ None |

---

## Quickstart Guides

### 1. Claude Code CLI (`/tarjoman`)

Tarjoman includes a bundled native Claude Code skillpack in `.claude/skills/tarjoman/`.

```bash
# Launch Claude Code inside your project
claude

# Invoke Tarjoman directly:
/tarjoman "Marcus turned around slowly, wondering if he would ever see home again." --domain literary
```

Features available in Claude Code:
- Automatic domain classification if `--domain` is omitted.
- Access to all 10 domain reference guides in `.claude/skills/tarjoman/references/`.
- Built-in linting against `.claude/skills/tarjoman/scripts/linter.py`.

### 2. Hermes Autonomous Agent

The Hermes agent skillpack lives in `agent-packs/hermes/SKILL.md`. To equip your Hermes instance:

```bash
# Copy or symlink into your Hermes skills directory
cp -r agent-packs/hermes/ ~/.hermes/skills/tarjoman
```

Hermes will autonomously detect English source files, orchestrate the 5-pass reflection process, extract terms into `terms.tsv`, and compile publication outputs.

### 3. Cursor & Windsurf (`.cursorrules`)

Integrate Tarjoman's Persian translation rules directly into your editor:

```bash
# Copy into your project root:
cp agent-packs/cursor/.cursorrules ./.cursorrules
```

Now, every translation or Persian text edit generated in Cursor AI will automatically conform to:
- Zero em-dash policy
- Persian quotation marks (`«` and `»`)
- Banned calque avoidance
- Correct non-joiner (`‌`) usage

### 4. Standalone Python CLI

Install Tarjoman locally:

```bash
pip install -e .
```

#### A. Route and Classify Domain
```bash
# Inspect detected domain, Persian title, and confidence score:
tarjoman route "The randomized clinical trial evaluated patient response."
```

#### B. Translate a Document
```bash
# Translate text with domain selection:
tarjoman translate chapter1.txt -d literary -o chapter1_fa.md

# Translate and output as an aligned bilingual Markdown table:
tarjoman translate paper.txt -d scientific -o paper_bilingual.md --composer bilingual
```

#### C. Compose Publication Outputs
```bash
# 1. Generate Interactive Bilingual HTML Reader:
tarjoman compose html source_en.txt translation_fa.txt -o reader.html --title "هوش مصنوعی"

# 2. Generate and Compile Typst PDF:
tarjoman compose typst translation_fa.txt -s book -o book.typ --compile
```

#### D. Run MQM Quality Audit & Linter
```bash
# Run Stage 5 MQM audit against source and domain rules:
tarjoman audit translation_fa.txt -s source_en.txt -d literary

# Run the Persian typography linter:
tarjoman lint document_fa.md
```

#### E. Manage Book Projects
```bash
# Initialize a new book project with manifest.json and terms.tsv:
tarjoman book init "The Odyssey" -o my_book

# Check project translation progress and dynamic terms:
tarjoman book status my_book
```

---

## Publishing Output Showcase

### 1. Typst PDF Publishing
Tarjoman generates pristine, vector-grade PDFs using [Typst](https://typst.app/), the modern alternative to LaTeX.
- **Academic Papers (`--style paper`)**: A4 format, two-column or single-column layout, Persian Vazirmatn typography, automatic LTR isolation for English math equations and citations.
- **Books & Novels (`--style book`)**: Standard octavo/novel book format, comfortable margins, elegant header running titles, and proper Persian paragraph indentations.

```bash
tarjoman compose typst novel_chapter.txt -s book -o novel.typ --compile
```

### 2. Standalone Interactive HTML Reader
The HTML composer outputs a single, zero-dependency HTML file featuring:
- **Synchronized Scrolling**: Scroll Persian or English side; the opposite column tracks seamlessly.
- **Glassmorphism UI**: Modern, dark-mode-ready, accessible interface powered by the beautiful Vazirmatn font.
- **Interactive Search**: Real-time bilingual search filtering across both languages simultaneously.

```bash
tarjoman compose html original.txt translated.txt -o reader.html
```

### 3. Bilingual Markdown
Generates GitHub-flavored aligned Markdown tables, ideal for translators performing human post-editing (MTPE) or committing to Git repositories with line-by-line diff tracking.

---

## Repository Structure

```text
tarjoman/
├── .github/
│   └── workflows/
│       ├── test.yml            # Multi-Python matrix tests (3.10-3.13) & benchmark CI
│       └── release.yml         # Automated PyPI & GitHub release packaging
├── .claude/
│   └── skills/
│       └── tarjoman/           # Native Claude Code skillpack & 12 reference guides
├── agent-packs/
│   ├── hermes/                 # Autonomous Hermes agent skillpack
│   └── cursor/                 # Editor rules for Cursor and Windsurf (.cursorrules)
├── benchmarks/
│   ├── run_benchmarks.py       # 10-domain automated benchmark suite
│   └── outputs/                # Generated artifacts from benchmark executions
├── tarjoman/
│   ├── core/                   # Pydantic data contracts and schemas
│   ├── domains/                # Domain registry & statistical keyword router
│   │   └── registry/*.json     # 10 JSON domain configuration profiles
│   ├── stages/                 # 5-pass reflection pipeline stages
│   │   ├── draft.py            # Stage 2: Initial contextual drafting
│   │   ├── anti_calque.py      # Stage 3: Anti-calque & typography sanitizer
│   │   ├── cadence.py          # Stage 4: Tone, cadence, & dialogue inversion
│   │   └── audit.py            # Stage 5: Multidimensional Quality Metric (MQM)
│   ├── composers/              # Typst PDF, HTML Reader, and Markdown composers
│   ├── memory/                 # Book project manifest and termbase managers
│   └── cli.py                  # Full Click CLI implementation
├── tests/                      # 96 comprehensive unit and integration tests
├── CONTRIBUTING.md             # Developer guidelines & calque submission instructions
├── LICENSE                     # MIT Open-Source License
├── pyproject.toml              # Build system configuration
└── README.md                   # Project documentation
```

---

## Testing and Verification

Tarjoman adheres to strict verification discipline. All 96 unit tests and the 10-domain benchmark suite are validated on every commit:

```bash
# Run unit tests
python -m unittest discover -s tests -p "test_*.py"

# Run 10-domain verification benchmark
python benchmarks/run_benchmarks.py
```

CI automatically validates all pull requests across Python 3.10, 3.11, 3.12, and 3.13 on `ubuntu-latest`.

---

## Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding or refining domain profiles in `tarjoman/domains/registry/`
- Reporting and registering new linguistic calques in `tarjoman/stages/anti_calque.py`
- Enhancing multi-agent prompts and composers

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<b>Tarjoman Master Suite</b> - <i>Crafted for the Persian language, AI researchers, and translators worldwide.</i>
</div>
