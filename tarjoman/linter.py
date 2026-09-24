"""
Persian Markdown & Translation Linter for Tarjoman Universal Engine (v2).

Checks Persian text/markdown files for:
1. Guaranteed ZERO em-dashes: '—', '–', and standalone '--' (CLI flags untouched)
2. Straight/curly quotes that must become Persian guillemets «»
3. Expanded banned structural and lexical calques (Najafi/Samii, incl. وي)
4. Missing ZWNJ after verbal prefixes می/نمی
5. Unbalanced Persian quotation marks ('«' vs '»')
6. Non-standard Arabic characters ('ي', 'ك', 'ى', 'ة', 'ـ')

Both this module and the skillpack script
(``.claude/skills/tarjoman/scripts/linter.py``) consume the shared pattern
table in ``tarjoman.stages.anti_calque`` — one source of truth.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Pattern, Tuple

from tarjoman.stages.anti_calque import (
    LINT_ARABIC_CHARS,
    LINT_CALQUE_PATTERNS,
    LINT_DOUBLE_HYPHEN_RE,
    LINT_STRAIGHT_QUOTE_RES,
    LINT_ZWNJ_RES,
)

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class LintIssue:
    line_number: int
    category: str  # "em-dash", "quote-style", "calque", "zwnj", "quote", "arabic"
    message: str
    snippet: str
    suggestion: str = field(default="")


BANNED_CALQUE_PATTERNS: List[Tuple[str, Pattern]] = [
    (name, re.compile(regex, re.UNICODE)) for name, regex in LINT_CALQUE_PATTERNS
]

_STRAIGHT_QUOTE_PATTERNS: List[Pattern] = [
    re.compile(regex, re.UNICODE) for regex in LINT_STRAIGHT_QUOTE_RES
]

_ZWNJ_PATTERNS: List[Pattern] = [
    re.compile(regex, re.UNICODE) for regex in LINT_ZWNJ_RES
]

_DOUBLE_HYPHEN_PATTERN: Pattern = re.compile(LINT_DOUBLE_HYPHEN_RE)


def lint_text(content: str, skip_code_blocks: bool = True) -> List[LintIssue]:
    """Analyze Persian text and return list of detected lint issues.

    Args:
        content: The text/markdown content to analyze.
        skip_code_blocks: If True, ignore lines inside fenced code blocks (```).
    """
    issues: List[LintIssue] = []
    lines = content.splitlines()

    total_opening_quotes = 0
    total_closing_quotes = 0
    in_code_block = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if skip_code_blocks:
                continue

        if skip_code_blocks and in_code_block:
            continue

        # 1. Em-dash, en-dash, and standalone double-hyphen detection.
        for dash_char, name in [("—", "em-dash"), ("–", "en-dash")]:
            if dash_char in line:
                issues.append(
                    LintIssue(
                        line_number=idx,
                        category="em-dash",
                        message=f"Lingering {name} ('{dash_char}') found. Eradicate or adapt into authentic Persian punctuation.",
                        snippet=line.strip(),
                        suggestion="Replace with a Persian comma (،) or parentheses; run AntiCalqueEngine.eliminate_em_dashes().",
                    )
                )
        if _DOUBLE_HYPHEN_PATTERN.search(line):
            issues.append(
                LintIssue(
                    line_number=idx,
                    category="em-dash",
                    message="Lingering standalone double-hyphen ('--') found. It reads as an em-dash in Persian prose.",
                    snippet=line.strip(),
                    suggestion="Replace with a Persian comma (،) or parentheses.",
                )
            )

        # 2. Straight/curly quotes that must become «».
        for qp in _STRAIGHT_QUOTE_PATTERNS:
            match = qp.search(line)
            if match:
                issues.append(
                    LintIssue(
                        line_number=idx,
                        category="quote-style",
                        message=f"Non-Persian quotation marks {match.group(0)[:24]!r} found. Use Persian guillemets «».",
                        snippet=line.strip(),
                        suggestion="Run AntiCalqueEngine.normalize_quotes().",
                    )
                )
                break

        # 3. Banned calques (expanded Najafi/Samii table).
        for calque_name, pattern in BANNED_CALQUE_PATTERNS:
            match = pattern.search(line)
            if match:
                issues.append(
                    LintIssue(
                        line_number=idx,
                        category="calque",
                        message=f"Banned calque detected: '{calque_name}'.",
                        snippet=line.strip(),
                        suggestion="Run AntiCalqueEngine.eliminate_calques().",
                    )
                )

        # 4. Missing ZWNJ after verbal prefixes می/نمی.
        for zp in _ZWNJ_PATTERNS:
            if zp.search(line):
                issues.append(
                    LintIssue(
                        line_number=idx,
                        category="zwnj",
                        message="Missing ZWNJ (نیم‌فاصله) after verbal prefix می/نمی. Write می‌/نمی‌ joined.",
                        snippet=line.strip(),
                        suggestion="Run AntiCalqueEngine.normalize_zwnj().",
                    )
                )
                break

        # 5. Arabic characters (ي, ك, ى, ة, ـ).
        arabic_chars_found = sorted({ch for ch in LINT_ARABIC_CHARS if ch in line})
        if arabic_chars_found:
            chars_str = ", ".join(f"'{c}'" for c in arabic_chars_found)
            issues.append(
                LintIssue(
                    line_number=idx,
                    category="arabic",
                    message=f"Non-standard Arabic characters {chars_str} detected. Normalize to Persian 'ی' and 'ک'.",
                    snippet=line.strip(),
                    suggestion="Run AntiCalqueEngine.standardize_arabic_chars().",
                )
            )

        # Quote counting
        total_opening_quotes += line.count("«")
        total_closing_quotes += line.count("»")

    # 6. Unbalanced Persian quotation marks
    if total_opening_quotes != total_closing_quotes:
        issues.append(
            LintIssue(
                line_number=len(lines) if lines else 1,
                category="quote",
                message=(
                    f"Unbalanced Persian quotation marks: {total_opening_quotes} opening '«' "
                    f"vs {total_closing_quotes} closing '»'."
                ),
                snippet=f"Total '«': {total_opening_quotes}, Total '»': {total_closing_quotes}",
            )
        )

    return issues


def format_report(file_path: str, issues: List[LintIssue]) -> str:
    """Format a diagnostic terminal report for lint issues."""
    lines: List[str] = []
    lines.append(f"{BOLD}Tarjoman Persian Linter Report: {file_path}{RESET}")
    lines.append("=" * 60)

    if not issues:
        lines.append(f"{GREEN}{BOLD}[PASSED]{RESET} No linguistic or typographic issues found. Clean Persian text!")
        return "\n".join(lines)

    lines.append(f"{RED}{BOLD}[FAILED]{RESET} Found {len(issues)} issue(s):\n")

    for i, issue in enumerate(issues, start=1):
        cat_badge = f"{YELLOW}[{issue.category.upper()}]{RESET}"
        lines.append(f" {i}. Line {issue.line_number} {cat_badge}: {issue.message}")
        lines.append(f"    {CYAN}Excerpt:{RESET} {issue.snippet}")
        if issue.suggestion:
            lines.append(f"    {GREEN}Fix:{RESET} {issue.suggestion}")
        lines.append("")

    return "\n".join(lines)
