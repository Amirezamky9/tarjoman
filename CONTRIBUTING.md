# Contributing to Tarjoman Universal Translation Suite

Thank you for your interest in contributing to **Tarjoman** (موتور جامع ترجمه «ترجمان»)! Tarjoman is an open-source, multi-agent Persian translation engine and publication ecosystem designed to deliver publication-quality Persian prose across 10 specialized domains.

We welcome contributions from translators, linguists, Python developers, AI agent researchers, and typography enthusiasts.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Development Setup](#development-setup)
3. [Contributing Domain Profiles](#contributing-domain-profiles)
4. [Reporting and Adding Calques (Anti-Calque Engine)](#reporting-and-adding-calques-anti-calque-engine)
5. [Persian Typography & Style Guidelines](#persian-typography--style-guidelines)
6. [Testing and Benchmarks](#testing-and-benchmarks)
7. [Submitting a Pull Request](#submitting-a-pull-request)
8. [Release Process](#release-process)

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and respectful community for everyone. Be courteous, constructive, and appreciative of fellow contributors.

---

## Development Setup

### Prerequisites

- **Python 3.10+** (tested on 3.10, 3.11, 3.12, and 3.13)
- **Git**
- Optional: **Typst CLI** (`typst --version`) if you wish to compile PDF publications locally.

### Installation

1. Clone your fork of the repository:
   ```bash
   git clone https://github.com/<your-username>/tarjoman.git
   cd tarjoman
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Linux / macOS:
   source venv/bin/activate
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Windows (bash):
   source venv/Scripts/activate
   ```

3. Install editable package and dependencies:
   ```bash
   pip install --upgrade pip
   pip install -e .
   ```

4. Verify installation:
   ```bash
   tarjoman --version
   python -m unittest discover -s tests -p "test_*.py"
   ```

---

## Contributing Domain Profiles

Tarjoman supports 10 canonical domains, each defined by a JSON profile located in `tarjoman/domains/registry/`:

- `literary.json` — Fiction, novels, short stories, narrative prose
- `scientific.json` — Academic papers, journal articles, scientific books
- `philosophy.json` — Continental & analytic philosophy, intellectual essays
- `legal.json` — Contracts, statutory articles, legal agreements
- `technical.json` — Software engineering, developer guides, code documentation
- `medical.json` — Clinical trials, pathology, pharmacology, healthcare
- `media.json` — Journalism, news reporting, press releases
- `financial.json` — Corporate finance, economics, investment, banking
- `classical.json` — Historical chronicles, ancient texts, classical prose
- `transcreation.json` — Creative marketing, branding slogans, ad copy

### Adding or Enhancing a Domain Profile

Every profile conforms to the `DomainProfile` schema defined in `tarjoman/core/contracts.py`:

```json
{
  "id": "domain_id",
  "name_en": "Domain Name English",
  "name_fa": "نام فارسی دامنه",
  "description": "Concise description of the domain scope and tone",
  "tone": "Formal | Literary | Academic | Archaic | Punchy",
  "formality_level": 1.0,
  "bidi_mode": "persian_first | isolate_formulas",
  "target_cadence": "balanced | rhythmic | concise | solemn",
  "zero_em_dash": true,
  "persian_quotes": true,
  "dialogue_inversion": false,
  "banned_calques": ["..."],
  "terminology": {
    "english_term": "اصطلاح مصوب فارسی"
  },
  "few_shot_pairs": [
    {
      "source": "English sample sentence.",
      "target": "جمله ترجمه‌شده روان و معیار فارسی."
    }
  ],
  "routing_keywords": ["keyword1", "keyword2", "keyword3"],
  "mqm_weights": {
    "terminology": 5.0,
    "accuracy": 5.0,
    "style": 2.0,
    "typography": 1.0
  }
}
```

When modifying or proposing a new profile:
1. Ensure all keywords are lowercase and specific to avoid conflicting routes.
2. Add high-quality `few_shot_pairs` demonstrating domain-specific nuance.
3. Add corresponding unit tests in `tests/test_router_10_domains.py`.

---

## Reporting and Adding Calques (Anti-Calque Engine)

Linguistic calques (گرته‌برداری‌های نحوی و واژگانی) degrade Persian prose quality. Tarjoman's Stage 3 engine automatically detects and replaces common translation loan-shifts.

### Where Calques Live

- **Engine Implementation**: `tarjoman/stages/anti_calque.py`
- **Reference Guide**: `.claude/skills/tarjoman/references/anti-calque.md`

### How to Add a Banned Calque

To register a new calque rule, add an entry to `BANNED_CALQUES` in `tarjoman/stages/anti_calque.py`:

```python
CalqueRule(
    pattern=r"\bتوسط\b",
    banned_persian="توسط (در ساختار مجهول)",
    natural_replacement="معلوم‌سازی فعل یا استفاده از «به‌دستِ / از سوی»",
    english_origin="by (passive voice calque)",
    severity=SeverityLevel.CRITICAL,
    explanation="استفاده از 'توسط' برای فاعل مجهول گرته‌برداری مستقیم از ساختار مجهول انگلیسی است.",
)
```

Ensure you include:
- A regex pattern with word boundaries.
- The literal banned phrase and natural Persian alternatives.
- The English source idiom/structure being imitated.
- Unit tests in `tests/test_anti_calque.py` asserting detection and proper replacement recommendations.

---

## Persian Typography & Style Guidelines

Every pull request modifying translations, templates, or documentation must respect our non-negotiable typography standards:

1. **Zero Em-Dash Policy**:
   - The em-dash (`—` / `—`) is prohibited in Persian output.
   - Use parentheses `(...)`, semicolons `؛`, or commas `،` depending on sentence syntax.
2. **Persian Quotation Marks**:
   - Use guillemets `«...»` instead of ASCII quotes `""` or English curly quotes `“”`.
3. **Persian Characters**:
   - Standard Persian `ی` (`ی`) and `ک` (`ک`), never Arabic `ي` (`ي`) or `ك` (`ك`).
4. **Half-Spaces (ZWNJ)**:
   - Use zero-width non-joiner (`‌`) for prefixes (`می‌رود`), plural suffixes (`کتاب‌ها`), and compound words (`گفت‌وگو`).
5. **Punctuation Attachment**:
   - Punctuation marks (`.` `,` `!` `؟` `؛`) must attach directly to the preceding word with zero space before, followed by a single space after.

### Linting Typography

Run the built-in linter to check any markdown or text file:

```bash
# Using CLI:
tarjoman lint path/to/document.md

# Using standalone script:
python .claude/skills/tarjoman/scripts/linter.py path/to/document.md
```

---

## Testing and Benchmarks

Before submitting any code, verify all suites:

```bash
# 1. Run all unit and integration tests
python -m unittest discover -s tests -p "test_*.py"

# 2. Run the 10-Domain comprehensive benchmark
python benchmarks/run_benchmarks.py
```

All 10 domains must output `PASS` with high confidence scores and valid exports.

---

## Submitting a Pull Request

1. **Branch Naming**:
   - `feat/feature-name` for new features or domain enhancements.
   - `fix/bug-description` for bug fixes.
   - `docs/documentation-update` for documentation changes.
   - `chore/...` for build/CI maintenance.

2. **Commit Convention**:
   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   ```text
   feat(domain): add philosophy specialized terminology
   fix(anti-calque): refine passive voice regex boundary
   docs(readme): add Hermes agent integration guide
   ```

3. **Checklist Before Opening PR**:
   - [ ] All unit tests pass (`python -m unittest discover -s tests -p "test_*.py"`).
   - [ ] Benchmarks pass (`python benchmarks/run_benchmarks.py`).
   - [ ] Linter is clean (`tarjoman lint <files>`).
   - [ ] Documentation updated if CLI options or configuration changed.

---

## Release Process

Releases are automated via GitHub Actions:
- Tagging a release commit with `v*` (e.g., `git tag v1.0.0 && git push origin v1.0.0`) triggers `.github/workflows/release.yml`.
- The workflow builds standard source distributions and wheels (`dist/`) and publishes release artifacts.

---

*Thank you for helping craft the gold standard of Persian translation software!*
