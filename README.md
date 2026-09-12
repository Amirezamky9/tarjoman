# Tarjoman Universal Translation Engine (موتور جامع ترجمه «ترجمان»)

Tarjoman is a production-grade, multi-domain English-to-Persian translation and publication suite. It delivers publication-quality Persian prose across 10 specialized domains, enforcing strict typography, anti-calque linguistic purity, reflective multi-agent translation loops, and professional bilingual exports (Typst PDF and Interactive HTML Reader).

## 10 Specialized Domains

1. **Literary (`literary`)**: Fiction, novels, and narrative prose with rhythmic cadence and dialogue inversion.
2. **Scientific (`scientific`)**: Academic papers, journal articles, and textbooks with strict bidi/formula isolation.
3. **Philosophy (`philosophy`)**: Continental/analytic philosophy, existentialism, and deep conceptual etymology.
4. **Legal (`legal`)**: Contracts, statutory codes, and official agreements with zero ambiguity.
5. **Technical (`technical`)**: Software engineering, developer documentation, CLI flags, and code fences.
6. **Medical (`medical`)**: Clinical trials, pathology, pharmacology, INN drug nomenclature, and dosages.
7. **Media (`media`)**: Journalism, news dispatch, inverted pyramid structure, and active punchy headlines.
8. **Financial (`financial`)**: Corporate finance, macroeconomics, IFRS/GAAP standards, and balance sheets.
9. **Classical (`classical`)**: Ancient chronicles, historical manuscripts, scriptures, and solemn archaic prose.
10. **Transcreation (`transcreation`)**: Creative marketing, branding, taglines, and culturally resonant copywriting.

## Installation

```bash
pip install -e .
```

## Quickstart

```python
from tarjoman.domains import DomainRegistry, DomainRouter

registry = DomainRegistry()
router = DomainRouter(registry=registry)

profile, confidence = router.route("The clinical trial demonstrated statistically significant efficacy.")
print(profile.id, confidence)
```

## License

MIT License
