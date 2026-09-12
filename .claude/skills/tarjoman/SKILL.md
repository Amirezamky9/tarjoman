---
name: tarjoman
description: Universal multi-domain Persian translation master skill covering 10 domains with 5-pass reflection pipeline, anti-calque enforcement, and Typst/HTML/Bilingual composers.
---

# Tarjoman Universal Translation Engine (موتور جامع ترجمه «ترجمان»)

Welcome to **Tarjoman** — the production-grade, multi-domain English-to-Persian translation and localization intelligence system. Tarjoman transcends raw machine translation by enforcing classical Persian linguistic purity, dynamic equivalence, five-pass human-emulation reflection, and multi-format publication composition.

---

## 1. Core Architectural Principles & Identity

1. **Human-Emulation over Literal Word-for-Word**:
   Tarjoman rejects robotic calques and mechanical word substitution. Following the translation philosophy of Eugene Nida and Mohammad-Ali Jamalzadeh, every sentence is reconstructed in idiomatic, native Persian syntax while preserving exact conceptual fidelity.

2. **Absolute Zero Em-Dash (Hermes Protocol)**:
   The English em-dash (`—`) and en-dash (`–`) as parenthetical or dramatic pauses are alien to Persian typography. In literary, classical, and narrative registers, em-dashes are eradicated and replaced with natural Persian syntax (semicolons, conjunctions, appositives, or rhythmic sentence splitting). In technical, academic, and legal registers, parenthetical dashes are converted into proper Persian commas (`،`), colons (`:`), or parentheses.

3. **Anti-Calque Linguistic Purity**:
   Enforces the linguistic doctrines of Abolhassan Najafi (*Ghalat Nanevisim* - غلط ننویسیم) and Ahmad Samii Guilani (*Negaresh va Virayesh* - نگارش و ویرایش). Mechanical borrowings such as passive-by agent phrases (`توسط ... انجام شد`), `روی کسی حساب کردن`, `نقش بازی کردن`, and `در پایان روز` are systematically transformed into authentic Persian active constructions.

4. **Multi-Domain Intelligence (10 Specialized Domains)**:
   Auto-routes texts to one of 10 domain profiles, each equipped with dedicated vocabulary maps, typographic rules, and strict register settings.

5. **Five-Pass Reflection Pipeline**:
   Implements a rigorous five-stage workflow: Pre-analysis Masking -> Semantic Draft -> Multi-dimension Reflection -> Typographic & Anti-Calque Polish -> MQM Quality Audit.

---

## 2. The 10 Domain Taxonomy & Routing Rules

When input text is received without an explicit domain override, Tarjoman analyzes vocabulary, lexical density, and syntactic structures to route into one of the 10 domains:

| # | Domain ID | Persian Title | Core Heuristics & Key Markers | Typography & Quotation Rules |
|---|---|---|---|---|
| 1 | `literary` | ادبی، رمان و داستان | Dialogue, narrative past, emotional prose, sensory adjectives | Zero em-dash, inverted dialogue tags (`گفت: «...»`), Persian quotes «...», Eastern digits |
| 2 | `scientific` | علمی و مقالات دانشگاهی | LaTeX math `$E=mc^2$`, citations `[1]`, `p < 0.05`, passive methodology | Directional LTR isolates, Western digits, preserved LaTeX math, adapted dashes |
| 3 | `philosophy` | فلسفه و علوم انسانی | *Dasein*, ontological, epistemology, German/Greek roots, Being/Nothingness | Etymological precision, hyphenated compound nouns, conceptual footnotes |
| 4 | `legal` | حقوقی و قراردادها | Statutory clauses, "shall", "indemnify", "jurisdiction", covenants | Unambiguous modal obligations («ملزم است»), verbatim party definitions, Western digits for clauses |
| 5 | `technical` | فنی و مهندسی نرم‌افزار | Markdown code fences, CLI flags, API endpoints, SDK parameters | Preserved code blocks, concise imperative verbs, Western digits, isolated terms |
| 6 | `medical` | پزشکی و داروسازی | Clinical trials, dosages (`50 mg/kg`), randomized control, INN drug names | Zero tolerance for ambiguity, strict INN generic names, Western digits for dosages |
| 7 | `media` | رسانه و روزنامه‌نگاری | Inverted pyramid, AP/Reuters datelines, active leads, hard news | Punchy active headlines, concise leads, standard journalistic Persian |
| 8 | `financial` | مالی و اقتصادی | Balance sheets, EBITDA, IFRS/GAAP, market bull/bear, fiscal quarters | Standard accounting terminology, Western digits for currency/rates, percentage formatting |
| 9 | `classical` | متون کهن و تاریخی | Archaisms, solemn chronicles, biblical/epic registers, elevated diction | Rhythmic cadence, archaic vocabulary (*اندر*, *همی* where appropriate), zero em-dash |
| 10 | `transcreation` | تبلیغات و پیام‌های بازاریابی | Slogans, emotional hooks, punchlines, brand identity, CTAs | Cultural adaptation, idiomatic resonance, punchy rhyming or rhythmic cadence |

Detailed guides for each domain are available in `references/<domain>.md`.

---

## 3. Locked Typographic & Linguistic Defaults

All Tarjoman outputs adhere strictly to the following standards:

1. **Persian Quotation Marks**:
   - Always enclose direct speech and titles in Persian angle quotes: `«...»`.
   - Never leave English straight quotes (`"..."`) or curly quotes (`“...”`) in the Persian output.

2. **Zero-Width Non-Joiner (ZWNJ / نیم‌فاصله)**:
   - Compulsory for verb prefixes: `می‌رود`, `نمی‌دانم` (U+200C).
   - Compulsory for plural suffix `ها`: `کتاب‌ها`, `روش‌ها`.
   - Compulsory for comparative suffixes: `بهترین‌شان`, `سریع‌تر`.
   - Compulsory for Persian ezafe on silent heh: `خانه‌ی من` or `خانهٔ من`.
   - Compulsory for compound nouns: `تصمیم‌گیری`, `گفت‌وگو`, `بین‌المللی`.

3. **Standard Persian Character Set**:
   - Always use standard Persian `ک` (U+06A9) instead of Arabic `ك` (U+0643).
   - Always use standard dotless Persian `ی` (U+06CC) instead of Arabic `ي` (U+064A) or `ى` (U+0649).
   - Normalize full stops, Persian commas (`،`), semicolons (`؛`), and question marks (`؟`).

4. **Digit Localization Policy**:
   - **Eastern Persian Digits (`۰۱۲۳۴۵۶۷۸۹`)**: Used in `literary`, `classical`, `media`, and general text.
   - **Western Latin Digits (`0123456789`)**: Retained in `scientific`, `technical`, `financial`, and `medical` domains to ensure numerical alignment in equations, code, accounting tables, and drug dosages.

---

## 4. Five-Pass Human-Emulation Reflection Workflow

Tarjoman executes every translation task through five discrete stages:

```
[Input Text]
     │
     ▼
[Stage 1: Pre-Analysis & Masking] ──> Extracts & masks formulas ($...$), code fences, URLs, citations
     │
     ▼
[Stage 2: Semantic Drafting]      ──> Dynamic equivalence drafting aligned with domain register
     │
     ▼
[Stage 3: Multi-Pass Reflection]  ──> Evaluates Accuracy, Fluency, Terminology, and Tone
     │
     ▼
[Stage 4: Typographic & Polish]   ──> Anti-calque engine, ZWNJ normalization, dialogue tag inversion
     │
     ▼
[Stage 5: Quality Audit (MQM)]    ──> Verifies quote parity, missing numbers, restores protected tokens
     │
     ▼
[Composed Output: Typst / HTML / Bilingual MD]
```

### Stage 1: Pre-Analysis & Element Masking
Identifies and replaces volatile elements with unique reversible placeholders (`__PROT_TOKEN_0__`):
- Inline and block LaTeX math (`$...$`, `$$...$$`)
- Markdown code blocks and inline code (`` `code` ``)
- URLs, email addresses, and API endpoints
- Bibliographic citations (e.g., `[12]`, `Smith et al. (2021)`)

### Stage 2: Dynamic Equivalence Drafting
Produces the initial Persian draft reflecting the target domain's syntax, style prompt, and domain terminology map.

### Stage 3: Reflection & Self-Critique
The model reflects upon its draft across 4 evaluation axes:
- **Accuracy**: Were nuances, qualifications, or negations omitted or distorted?
- **Fluency**: Does the text sound like natural Persian written by an educated native speaker?
- **Terminology**: Are specialized terms translated consistently with standard domain glossaries?
- **Style & Register**: Does the text adhere to the domain's emotional and formal register?

### Stage 4: Typographic & Anti-Calque Polishing
Applies automated transformations:
- Converts passive-by constructions (`توسط X انجام شد` -> `X انجام داد`)
- Rewrites calqued idioms (`روی کسی حساب کردن` -> `به کسی اعتماد/تکیه کردن`)
- Inverts dialogue attribution tags in literary prose (`"Hello," she said` -> `سلام کرد و گفت: «...»`)
- Eradicates lingering em-dashes into fluid Persian syntax
- Standardizes ZWNJ across compound words and verbal prefixes

### Stage 5: Multidimensional Quality Metric (MQM) Audit
Performs automated verification:
- **Number Consistency**: Ensures all numerals present in the source are preserved.
- **Quote Balance**: Verifies opening `«` matches closing `»`.
- **Token Integrity**: Restores all protected placeholders without corruption.
- Computes overall Quality Score (0 - 100). If score < 80, flags for human review or auto-refines.

---

## 5. Publishing Composers Integration

Tarjoman includes three native publishing composers:

1. **Typst PDF Composer (`TypstPdfComposer`)**:
   Generates publication-ready PDF documents with native RTL typography, Vazirmatn font bindings, balanced margins, running headers, and table of contents:
   - Book template (A5 format, chapter numbering, inner/outer margins)
   - Academic paper template (A4 format, bilingual abstract, two-column support)

2. **Interactive HTML Reader (`HtmlReaderComposer`)**:
   Produces a standalone, self-contained HTML5 reader:
   - Embedded Vazirmatn font CDN
   - Real-time Toggle: Bilingual Parallel Mode vs. Persian-Only Reader Mode
   - Dark / Light theme switcher with local storage persistence
   - One-click copy for paragraphs and chapters

3. **Bilingual Markdown Composer (`BilingualMarkdownComposer`)**:
   Aligns English source paragraphs and polished Persian target paragraphs into clean GitHub-flavored Markdown tables.

---

## 6. Command-Line Interface (CLI) Quickstart

The Tarjoman engine is accessible via the CLI:

```bash
# 1. Route text to determine domain
tarjoman route "The quantum state vector undergoes unitary transformation."

# 2. Translate text with automatic domain routing
tarjoman translate --input document.txt --output translated.md

# 3. Translate with explicit domain override
tarjoman translate --input chapter1.txt --domain literary --composer bilingual

# 4. Generate publication-ready Typst PDF
tarjoman compose typst --input translated.md --style book --output book.pdf

# 5. Generate interactive HTML reader
tarjoman compose html --source document.txt --target translated.md --output reader.html

# 6. Audit an existing Persian translation for calques and typographic issues
tarjoman audit --input translated.md
```

---

## 7. Quality Linter Script

Use the built-in quality linter to verify any Persian text or translation output:

```bash
python .claude/skills/tarjoman/scripts/linter.py path/to/translated.md
```

The linter detects:
- Em-dashes (`—`, `–`)
- Banned calques and passive-by constructions
- Unbalanced Persian quotation marks (`«` vs `»`)
- Arabic letters (`ي`, `ك`) needing normalization to Persian `ی` and `ک`
