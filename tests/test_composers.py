"""
Tests for Tarjoman Publishing Composers.

Covers:
- BaseComposer: paragraph splitting and edge cases
- BilingualMarkdownComposer: table formatting, pipe escaping, mismatched paragraph counts
- HtmlReaderComposer: standalone HTML5, Vazirmatn CDN, dual view modes, theme toggle, copy buttons, XSS escaping
- TypstPdfComposer: RTL and Vazirmatn configuration, book (A5) vs paper (A4) styles, LaTeX math conversions
- TypstPdfComposer.compile_pdf: end-to-end PDF generation and graceful error handling
- Typst assets: verification of book.typ and paper.typ templates
"""
from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from tarjoman.composers.base import BaseComposer
from tarjoman.composers.bilingual_md import BilingualMarkdownComposer
from tarjoman.composers.html_reader import HtmlReaderComposer
from tarjoman.composers.typst_pdf import TypstPdfComposer


class ConcreteComposer(BaseComposer):
    def compose(self, *args, **kwargs) -> str:
        return "concrete"


class TestBaseComposer(unittest.TestCase):
    """Unit tests for BaseComposer."""

    def test_split_paragraphs_basic(self) -> None:
        text = "Paragraph 1\n\nParagraph 2\n\n\nParagraph 3"
        paras = BaseComposer.split_paragraphs(text)
        self.assertEqual(len(paras), 3)
        self.assertEqual(paras[0], "Paragraph 1")
        self.assertEqual(paras[1], "Paragraph 2")
        self.assertEqual(paras[2], "Paragraph 3")

    def test_split_paragraphs_empty_or_whitespace(self) -> None:
        self.assertEqual(BaseComposer.split_paragraphs(""), [])
        self.assertEqual(BaseComposer.split_paragraphs("   \n\n   "), [])


class TestBilingualMarkdownComposer(unittest.TestCase):
    """Unit tests for BilingualMarkdownComposer."""

    def setUp(self) -> None:
        self.composer = BilingualMarkdownComposer()

    def test_basic_table_generation(self) -> None:
        src = "Paragraph one.\n\nParagraph two."
        tgt = "بند اول.\n\nبند دوم."
        md = self.composer.compose(src, tgt)

        self.assertIn("# بررسی تطبیقی دو زبانه (Bilingual Side-by-Side Review)", md)
        self.assertIn("| متن اصلی انگلیسی | ترجمه فارسی صیقل‌خورده |", md)
        self.assertIn("| :--- | :--- |", md)
        self.assertIn("| Paragraph one. | بند اول. |", md)
        self.assertIn("| Paragraph two. | بند دوم. |", md)

    def test_pipe_escaping_in_both_columns(self) -> None:
        src = "Use A | B operator in regex."
        tgt = "از عملگر الف | ب در عبارات باقاعده استفاده کنید."
        md = self.composer.compose(src, tgt)

        # Pipe must be escaped with backslash
        self.assertIn(r"A \| B", md)
        self.assertIn(r"الف \| ب", md)

    def test_newline_escaping_within_cells(self) -> None:
        src = "Line 1\nLine 2 inside single paragraph."
        tgt = "خط اول\nخط دوم درون یک بند."
        md = self.composer.compose(src, tgt)

        # Raw newlines inside cell replaced with <br>
        self.assertIn("Line 1<br>Line 2 inside single paragraph.", md)
        self.assertIn("خط اول<br>خط دوم درون یک بند.", md)

    def test_mismatched_paragraph_counts_more_source(self) -> None:
        src = "P1\n\nP2\n\nP3"
        tgt = "ب۱"
        md = self.composer.compose(src, tgt)

        lines = md.strip().split("\n")
        # Title(1) + blank(1) + header(1) + divider(1) + 3 rows = 7 lines
        rows = [l for l in lines if l.startswith("| ") and ":---" not in l and "متن اصلی" not in l]
        self.assertEqual(len(rows), 3)
        self.assertIn("| P1 | ب۱ |", rows[0])
        self.assertIn("| P2 |  |", rows[1])
        self.assertIn("| P3 |  |", rows[2])

    def test_mismatched_paragraph_counts_more_target(self) -> None:
        src = "P1"
        tgt = "ب۱\n\nب۲\n\nب۳"
        md = self.composer.compose(src, tgt)

        rows = [l for l in md.strip().split("\n") if l.startswith("| ") and ":---" not in l and "متن اصلی" not in l]
        self.assertEqual(len(rows), 3)
        self.assertIn("| P1 | ب۱ |", rows[0])
        self.assertIn("|  | ب۲ |", rows[1])
        self.assertIn("|  | ب۳ |", rows[2])

    def test_list_input_and_custom_title(self) -> None:
        src_list = ["First item", "Second item"]
        tgt_list = ["مورد اول", "مورد دوم"]
        md = self.composer.compose(src_list, tgt_list, title="گزارش مقایسه‌ای")

        self.assertIn("# گزارش مقایسه‌ای", md)
        self.assertIn("| First item | مورد اول |", md)


class TestHtmlReaderComposer(unittest.TestCase):
    """Unit tests for HtmlReaderComposer."""

    def setUp(self) -> None:
        self.composer = HtmlReaderComposer()

    def test_standalone_html_structure(self) -> None:
        html = self.composer.compose("Hello world.", "سلام دنیا.", title="کتاب آزمایشی")

        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn('<html lang="fa" dir="rtl"', html)
        self.assertIn("<title>کتاب آزمایشی</title>", html)
        self.assertIn("</html>", html)

    def test_vazirmatn_cdn_presence(self) -> None:
        html = self.composer.compose("Hello", "سلام", title="Test")
        self.assertIn("vazirmatn", html.lower())
        self.assertIn("fonts.googleapis.com", html)
        self.assertIn("jsdelivr.net", html)

    def test_dual_view_modes_and_controls(self) -> None:
        html = self.composer.compose("Hello", "سلام")

        # Initial class is mode-bilingual
        self.assertIn("mode-bilingual", html)
        # Switch function toggleViewMode handles mode-persian
        self.assertIn("mode-persian", html)
        self.assertIn("toggleViewMode", html)
        self.assertIn("مطالعه فارسی", html)

    def test_theme_toggle_controls(self) -> None:
        html = self.composer.compose("Hello", "سلام")

        self.assertIn("themeToggleBtn", html)
        self.assertIn("toggleTheme", html)
        self.assertIn('data-theme="light"', html)
        self.assertIn('data-theme="dark"', html)

    def test_copy_buttons_and_metadata(self) -> None:
        html = self.composer.compose("Para 1\n\nPara 2", "بند ۱\n\nبند ۲")

        self.assertIn("copySegment", html)
        self.assertIn("copyFullTranslation", html)
        self.assertIn("تعداد بندها: 2", html)
        self.assertIn("زمان تقریبی مطالعه:", html)

    def test_xss_protection(self) -> None:
        dangerous_src = "<script>alert('xss')</script>"
        dangerous_tgt = "<img src=x onerror=alert('xss')>"
        html = self.composer.compose(dangerous_src, dangerous_tgt, title="<tag>Title</tag>")

        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;alert", html)
        self.assertNotIn("<img src=x", html)
        self.assertIn("&lt;img src=x", html)
        self.assertNotIn("<tag>Title</tag>", html)
        self.assertIn("&lt;tag&gt;Title&lt;/tag&gt;", html)


class TestTypstPdfComposer(unittest.TestCase):
    """Unit tests for TypstPdfComposer."""

    def setUp(self) -> None:
        self.composer = TypstPdfComposer()

    def test_rtl_and_vazirmatn_configuration(self) -> None:
        typ = self.composer.compose("متن نمونه", style="book")

        self.assertIn('dir: rtl', typ)
        self.assertIn('lang: "fa"', typ)
        self.assertIn('font: "Vazirmatn"', typ)
        self.assertIn('leading: 0.85em', typ)
        self.assertIn('first-line-indent: 1.5em', typ)

    def test_book_style_a5(self) -> None:
        typ = self.composer.compose("متن کتاب", title="عنوان کتاب", style="book")

        self.assertIn('paper: "a5"', typ)
        self.assertIn('margin: (x: 1.8cm, top: 2.2cm, bottom: 2.2cm)', typ)
        self.assertIn('numbering: "1"', typ)
        self.assertIn('= عنوان کتاب', typ)
        self.assertIn('متن کتاب', typ)

    def test_paper_style_a4(self) -> None:
        typ = self.composer.compose("متن مقاله", title="عنوان مقاله", author="نویسنده", style="paper")

        self.assertIn('paper: "a4"', typ)
        self.assertIn('margin: (x: 2.5cm, y: 2.5cm)', typ)
        self.assertIn('= عنوان مقاله', typ)
        self.assertIn('نویسنده', typ)

    def test_latex_math_conversion_inline_and_display(self) -> None:
        # $E=mc^2$ converted to Typst-safe math representation $E = m c^2$
        res1 = self.composer.convert_latex_math("فرمول فیزیک $E=mc^2$ است.")
        self.assertIn("m c^2", res1)

        # Greek letter \sigma inside math
        res2 = self.composer.convert_latex_math(r"نماد انحراف معیار $\sigma$ است.")
        self.assertIn("$sigma$", res2)

        # Bare \sigma symbol
        res3 = self.composer.convert_latex_math(r"\sigma")
        self.assertEqual(res3, "sigma")

        # Fractions: \frac{a}{b} -> (a) / (b)
        res4 = self.composer.convert_latex_math(r"$\frac{n(n+1)}{2}$")
        self.assertTrue("(n(n + 1)) / (2)" in res4 or "(n(n+1)) / (2)" in res4)

        # Roots: \sqrt{x} -> sqrt(x)
        res5 = self.composer.convert_latex_math(r"$\sqrt{x^2 + y^2}$")
        self.assertIn("sqrt(x^2 + y^2)", res5)

        # Operators: \times, \leq, \infty
        res6 = self.composer.convert_latex_math(r"$a \times b \leq \infty$")
        self.assertIn("times", res6)
        self.assertIn("<=", res6)
        self.assertIn("infinity", res6)

    def test_compose_with_embedded_math_and_bare_symbols(self) -> None:
        text = "فرمول مشهور انرژی $E=mc^2$ است و انحراف با \\sigma سنجیده می‌شود."
        typ = self.composer.compose(text, style="book")

        self.assertIn("m c^2", typ)
        self.assertIn("$sigma$", typ)

    def test_compile_pdf_real_execution(self) -> None:
        raw_text = "این یک آزمایش برای ساخت فایل با فرمول $E=mc^2$ و انحراف $\\sigma$ است."
        content = self.composer.compose(raw_text, title="آزمایش کامپایل پی‌دی‌اف")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            pdf_path = f.name

        try:
            success = self.composer.compile_pdf(content, pdf_path)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(pdf_path))
            self.assertGreater(os.path.getsize(pdf_path), 1000)
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    def test_compile_pdf_failure_handling(self) -> None:
        # Invalid typst syntax
        bad_content = "#set invalid_directive_that_does_not_exist((("
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            pdf_path = f.name

        try:
            with patch("shutil.which", return_value=None):
                success = self.composer.compile_pdf(bad_content, pdf_path)
                self.assertFalse(success)
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)


class TestTypstAssets(unittest.TestCase):
    """Unit tests for Typst publication asset templates."""

    def test_book_template_asset_exists_and_valid(self) -> None:
        book_path = os.path.join(os.path.dirname(__file__), "..", "assets", "typst", "book.typ")
        self.assertTrue(os.path.exists(book_path))

        with open(book_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('paper: "a5"', content)
        self.assertIn('font: "Vazirmatn"', content)
        self.assertIn('dir: rtl', content)

    def test_paper_template_asset_exists_and_valid(self) -> None:
        paper_path = os.path.join(os.path.dirname(__file__), "..", "assets", "typst", "paper.typ")
        self.assertTrue(os.path.exists(paper_path))

        with open(paper_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('paper: "a4"', content)
        self.assertIn('font: "Vazirmatn"', content)
        self.assertIn('dir: rtl', content)


if __name__ == "__main__":
    unittest.main()
