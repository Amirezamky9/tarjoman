#!/usr/bin/env python3
"""
Tarjoman Universal Translation Engine: 10-Domain Verification Benchmark Suite.

Executes comprehensive end-to-end verification across all 10 domain archetypes:
1. Literary & Fiction
2. Scientific & Academic
3. Philosophy & Humanities
4. Legal & Statutory
5. Technical & Engineering
6. Medical & Clinical
7. Media & Journalism
8. Financial & Economics
9. Classical & Historical
10. Transcreation & Creative Branding

For each domain:
- Validates intelligent domain classification with DomainRouter
- Executes 5-pass human-emulation reflection pipeline
- Audits against MQM quality standards (Score >= 90.0, 0 critical findings)
- Composes Bilingual Markdown, interactive HTML reader, and compiles Typst PDF
- Outputs a formatted terminal benchmark matrix
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure tarjoman is importable
BENCHMARKS_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = BENCHMARKS_DIR.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tarjoman.composers.bilingual_md import BilingualMarkdownComposer
from tarjoman.composers.html_reader import HtmlReaderComposer
from tarjoman.composers.typst_pdf import TypstPdfComposer
from tarjoman.core.contracts import DomainType
from tarjoman.core.pipeline import TranslationPipeline
from tarjoman.domains.router import DomainRegistry, DomainRouter

# ANSI Color Codes
BOLD = "\033[1m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def run_all_benchmarks() -> bool:
    """Run full 10-domain verification benchmark suite."""
    samples_dir = BENCHMARKS_DIR / "samples"
    outputs_dir = BENCHMARKS_DIR / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    registry = DomainRegistry()
    router = DomainRouter(registry=registry)
    pipeline = TranslationPipeline()

    bilingual_composer = BilingualMarkdownComposer()
    html_composer = HtmlReaderComposer()
    typst_composer = TypstPdfComposer()

    print(f"\n{BOLD}{CYAN}================================================================================{RESET}")
    print(f"{BOLD}{CYAN}      TARJOMAN UNIVERSAL ENGINE: 10-DOMAIN COMPREHENSIVE BENCHMARK      {RESET}")
    print(f"{BOLD}{CYAN}================================================================================{RESET}")
    print(f"Executing 5-pass reflection, MQM audit, and 3-format publishing across 10 domains...\n")

    results_table: List[Dict[str, str]] = []
    all_passed = True
    start_total_time = time.time()

    for domain in DomainType:
        sample_path = samples_dir / f"{domain.value}.txt"
        if not sample_path.exists():
            raise FileNotFoundError(f"Missing benchmark sample file: {sample_path}")

        raw_text = sample_path.read_text(encoding="utf-8")
        domain_start = time.time()

        # 1. Routing Verification
        detected_profile, confidence = router.route(raw_text)
        assert detected_profile.id == domain, (
            f"Classification mismatch for {domain.value}: detected {detected_profile.id.value}"
        )

        # 2. 5-Pass Translation Pipeline & MQM Audit
        segments, audit_report = pipeline.run(raw_text, detected_profile)
        assert audit_report.passed, f"MQM Audit failed for domain '{domain.value}'"
        assert audit_report.quality_score >= 90.0, (
            f"Quality score {audit_report.quality_score} below 90.0 for '{domain.value}'"
        )
        critical_findings = [f for f in audit_report.findings if f.severity == "critical"]
        assert len(critical_findings) == 0, (
            f"Critical findings detected for domain '{domain.value}': {critical_findings}"
        )

        target_text = "\n\n".join(seg.polished_text or "" for seg in segments)

        # 3. Composers Generation
        domain_out_dir = outputs_dir / domain.value
        domain_out_dir.mkdir(parents=True, exist_ok=True)

        # 3a. Bilingual Markdown
        bi_md = bilingual_composer.compose(
            raw_text,
            target_text,
            title=f"بررسی تطبیقی دو زبانه: {detected_profile.title_fa}",
        )
        bi_path = domain_out_dir / f"{domain.value}_bilingual.md"
        bi_path.write_text(bi_md, encoding="utf-8")

        # 3b. Interactive HTML Reader
        html_content = html_composer.compose(
            raw_text,
            target_text,
            title=f"خوانش تطبیقی ترجمان: {detected_profile.title_fa}",
        )
        html_path = domain_out_dir / f"{domain.value}_reader.html"
        html_path.write_text(html_content, encoding="utf-8")

        # 3c. Typst Source and PDF Compilation
        typst_source = typst_composer.compose(
            target_text,
            title=f"ترجمه: {detected_profile.title_fa}",
            style="paper" if domain in (DomainType.SCIENTIFIC, DomainType.LEGAL, DomainType.TECHNICAL) else "book",
        )
        typ_path = domain_out_dir / f"{domain.value}_publication.typ"
        typ_path.write_text(typst_source, encoding="utf-8")

        pdf_path = domain_out_dir / f"{domain.value}_publication.pdf"
        pdf_compiled = typst_composer.compile_pdf(typst_source, str(pdf_path))

        elapsed = time.time() - domain_start

        results_table.append(
            {
                "domain": domain.value,
                "title_fa": detected_profile.title_fa,
                "confidence": f"{confidence * 100:.0f}%",
                "score": f"{audit_report.quality_score:.1f}",
                "audit": "PASS" if audit_report.passed else "FAIL",
                "bi_md": "YES",
                "html": "YES",
                "pdf": "YES" if pdf_compiled else "TYP-ONLY",
                "time": f"{elapsed:.2f}s",
            }
        )

    total_time = time.time() - start_total_time

    # Print Formatted Results Table
    header = (
        f"{'Domain':<15} | {'Persian Title':<26} | {'Conf':<6} | {'Score':<6} | "
        f"{'Audit':<6} | {'Bi-MD':<6} | {'HTML':<6} | {'PDF':<8} | {'Time':<6}"
    )
    separator = "-" * len(header)

    print(header)
    print(separator)
    for row in results_table:
        pdf_badge = f"{GREEN}{row['pdf']:<8}{RESET}" if row["pdf"] == "YES" else f"{YELLOW}{row['pdf']:<8}{RESET}"
        audit_badge = f"{GREEN}{row['audit']:<6}{RESET}" if row["audit"] == "PASS" else f"{RED}{row['audit']:<6}{RESET}"
        print(
            f"{row['domain']:<15} | {row['title_fa']:<26} | {row['confidence']:<6} | "
            f"{row['score']:<6} | {audit_badge} | {row['bi_md']:<6} | {row['html']:<6} | "
            f"{pdf_badge} | {row['time']:<6}"
        )
    print(separator)

    print(f"\n{BOLD}{GREEN}[SUCCESS]{RESET} All 10 Domain Verification Benchmarks PASSED (10/10) in {total_time:.2f}s!")
    print(f"Publishing artifacts generated in: {outputs_dir.resolve()}\n")

    return True


if __name__ == "__main__":
    success = run_all_benchmarks()
    sys.exit(0 if success else 1)
