"""
Tests for the 5-Pass Human-Emulation Reflection Pipeline.

Covers:
- Stage 1: Element masking and token restoration (LaTeX math, code blocks, URLs, emails, paragraphs)
- Stage 2: Semantic draft generation with Echo and Callable backends
- Stage 3: Reflection critique generation across 4 MQM axes and refinement
- Stage 4 & 5: Polishing and Quality Audit (numbers, quotes, calques, token integrity)
- Full 5-pass pipeline execution and 100% formula/number survival
"""
from __future__ import annotations

import unittest

from tarjoman.core.contracts import (
    DomainProfile,
    DomainType,
    EmDashPolicy,
    TextSegment,
    TypographicRules,
)
from tarjoman.core.pipeline import TranslationPipeline
from tarjoman.stages.stage1_pre_analysis import PreAnalysisStage
from tarjoman.stages.stage2_draft import (
    CallableTranslationBackend,
    EchoDraftBackend,
    SemanticDraftStage,
)
from tarjoman.stages.stage3_reflection import (
    ReflectionStage,
    RuleBasedReflectionEngine,
)
from tarjoman.stages.stage4_polish import StylisticPolishStage
from tarjoman.stages.stage5_audit import AuditStage


class TestPreAnalysisStage(unittest.TestCase):
    """Tests for Stage 1: Pre-Analysis and Token Masking."""

    def setUp(self) -> None:
        self.stage = PreAnalysisStage(split_paragraphs=True)
        self.profile = DomainProfile(
            id=DomainType.SCIENTIFIC,
            title_fa="علمی",
            description="علمی و دانشگاهی",
            system_prompt="ترجمه متون علمی",
        )

    def test_latex_math_masking_and_restoration(self) -> None:
        text = "Formula $E=mc^2$ and display $$\\int_{0}^{\\infty} e^{-x} dx = 1$$ in physics."
        masked, token_map = self.stage.mask_text(text)

        self.assertNotIn("$E=mc^2$", masked)
        self.assertNotIn("$$\\int_{0}^{\\infty} e^{-x} dx = 1$$", masked)
        self.assertEqual(len(token_map), 2)

        restored = PreAnalysisStage.restore_tokens(masked, token_map)
        self.assertEqual(restored, text)

    def test_code_blocks_masking_and_restoration(self) -> None:
        text = "Check inline `npm install` and block:\n```python\ndef add(a, b):\n    return a + b\n```\nDone."
        masked, token_map = self.stage.mask_text(text)

        self.assertNotIn("`npm install`", masked)
        self.assertNotIn("def add(a, b):", masked)
        self.assertEqual(len(token_map), 2)

        restored = PreAnalysisStage.restore_tokens(masked, token_map)
        self.assertEqual(restored, text)

    def test_url_and_email_masking_and_restoration(self) -> None:
        text = "Visit https://anthropic.com/research or contact test.user@domain.org for info."
        masked, token_map = self.stage.mask_text(text)

        self.assertNotIn("https://anthropic.com/research", masked)
        self.assertNotIn("test.user@domain.org", masked)
        self.assertEqual(len(token_map), 2)

        restored = PreAnalysisStage.restore_tokens(masked, token_map)
        self.assertEqual(restored, text)

    def test_multi_paragraph_splitting(self) -> None:
        raw = "Paragraph 1 with $x=1$.\n\nParagraph 2 with `print(2)`.\n\nParagraph 3."
        seg = TextSegment(id=1, source_text=raw)
        result = self.stage.process([seg], self.profile)

        self.assertEqual(len(result.segments), 3)
        self.assertEqual(result.segments[0].id, 1)
        self.assertEqual(result.segments[1].id, 2)
        self.assertEqual(result.segments[2].id, 3)

        # Tokens correctly partitioned per paragraph
        self.assertEqual(len(result.segments[0].metadata["protected_tokens"]), 1)
        self.assertEqual(len(result.segments[1].metadata["protected_tokens"]), 1)
        self.assertEqual(len(result.segments[2].metadata["protected_tokens"]), 0)


class TestSemanticDraftStage(unittest.TestCase):
    """Tests for Stage 2: Semantic Drafting."""

    def setUp(self) -> None:
        self.profile = DomainProfile(
            id=DomainType.SCIENTIFIC,
            title_fa="علمی",
            description="علمی",
            system_prompt="دستور ترجمه علمی",
        )

    def test_echo_draft_backend(self) -> None:
        stage = SemanticDraftStage(EchoDraftBackend(prefix="[DRAFT] "))
        seg = TextSegment(id=1, source_text="Sample text")
        result = stage.process([seg], self.profile)

        self.assertEqual(result.segments[0].translated_text, "[DRAFT] Sample text")

    def test_callable_translation_backend(self) -> None:
        def custom_translate(prompt: str, system_prompt: str) -> str:
            return f"FA({prompt})"

        stage = SemanticDraftStage(CallableTranslationBackend(custom_translate))
        seg = TextSegment(id=1, source_text="Machine learning")
        result = stage.process([seg], self.profile)

        self.assertEqual(result.segments[0].translated_text, "FA(Machine learning)")

    def test_protected_segment_bypass(self) -> None:
        stage = SemanticDraftStage(EchoDraftBackend(prefix="[DRAFT] "))
        seg = TextSegment(id=1, source_text="Do not translate", is_protected=True)
        result = stage.process([seg], self.profile)

        self.assertEqual(result.segments[0].translated_text, "Do not translate")


class TestReflectionStage(unittest.TestCase):
    """Tests for Stage 3: Reflection and Critique."""

    def setUp(self) -> None:
        self.profile = DomainProfile(
            id=DomainType.LITERARY,
            title_fa="ادبی",
            description="ادبیات داستانی",
            system_prompt="ترجمه ادبی",
            banned_calques=["روی میز بودن"],
            terminology_map={"quantum entanglement": "درهم‌تنیدگی کوانتومی"},
            typography=TypographicRules(
                invert_dialogue_tags=True,
                em_dash_policy=EmDashPolicy.ERADICATE,
            ),
        )
        self.stage = ReflectionStage()

    def test_reflection_critique_recording(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="The 42 particles in quantum entanglement. «Wait» he said.",
            translated_text="«صبر کن» او گفت. این موضوع روی میز بودن است. quantum entanglement",
            metadata={"protected_tokens": {}},
        )
        result = self.stage.process([seg], self.profile)
        critique = result.segments[0].reflection_critique
        refined = result.segments[0].translated_text

        # Verify critique noted issues along MQM axes
        self.assertIn("MQM Reflection Critique", critique)
        self.assertIn("Accuracy", critique)  # missing number 42
        self.assertIn("Fluency", critique)   # banned calque
        self.assertIn("Style", critique)     # un-inverted dialogue tag
        self.assertIn("Terminology", critique)  # quantum entanglement

        # Verify refinements were applied
        self.assertIn("درهم‌تنیدگی کوانتومی", refined)
        self.assertIn("او گفت: «صبر کن.»", refined)

    def test_clean_reflection_pass(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="Simple text with 10 units.",
            translated_text="متن ساده با 10 واحد.",
            metadata={"protected_tokens": {}},
        )
        result = self.stage.process([seg], self.profile)
        critique = result.segments[0].reflection_critique
        self.assertIn("No defects detected", critique)


class TestAuditStage(unittest.TestCase):
    """Tests for Stage 5: Quality Audit."""

    def setUp(self) -> None:
        self.profile = DomainProfile(
            id=DomainType.SCIENTIFIC,
            title_fa="علمی",
            description="علمی",
            system_prompt="علمی",
            banned_calques=["روی میز بودن"],
        )
        self.stage = AuditStage()

    def test_clean_audit_passes(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="We achieved 99 percent accuracy with ⟦PROTECTED_0⟧.",
            polished_text="ما به ۹۹ درصد دقت با ⟦PROTECTED_0⟧ دست یافتیم.",
            metadata={"protected_tokens": {"⟦PROTECTED_0⟧": "$p < 0.05$"}},
        )
        report = self.stage.audit([seg], self.profile)

        self.assertTrue(report.passed)
        self.assertEqual(report.quality_score, 100.0)
        self.assertEqual(len(report.findings), 0)

    def test_audit_flags_missing_number(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="Testing 500 samples in 3 groups.",
            polished_text="آزمایش در ۳ گروه انجام شد.",  # 500 missing
            metadata={"protected_tokens": {}},
        )
        report = self.stage.audit([seg], self.profile)

        self.assertFalse(report.passed)
        self.assertGreaterEqual(report.omission_count, 1)
        self.assertTrue(any(f.rule_id == "MQM-NUM-OMISSION" for f in report.findings))

    def test_audit_flags_unbalanced_quotes(self) -> None:
        seg = TextSegment(
            id=1,
            source_text='He said "Yes".',
            polished_text="او گفت «بله.",  # Unbalanced quote
            metadata={"protected_tokens": {}},
        )
        report = self.stage.audit([seg], self.profile)

        self.assertTrue(any(f.rule_id == "MQM-PUNCT-QUOTES" for f in report.findings))

    def test_audit_flags_banned_calque(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="This option is on the table.",
            polished_text="این گزینه روی میز بودن است.",
            metadata={"protected_tokens": {}},
        )
        report = self.stage.audit([seg], self.profile)

        self.assertTrue(any(f.rule_id == "MQM-CALQUE-BANNED" for f in report.findings))
        self.assertEqual(report.banned_calque_count, 1)

    def test_audit_flags_corrupted_protected_token(self) -> None:
        seg = TextSegment(
            id=1,
            source_text="Calculated using ⟦PROTECTED_0⟧.",
            polished_text="محاسبه با فرمول نامشخص انجام شد.",  # token lost
            metadata={"protected_tokens": {"⟦PROTECTED_0⟧": "$E=mc^2$"}},
        )
        report = self.stage.audit([seg], self.profile)

        self.assertFalse(report.passed)
        self.assertTrue(any(f.rule_id == "MQM-PROTECTED-TOKEN-LOST" for f in report.findings))


class TestFull5PassPipeline(unittest.TestCase):
    """End-to-end tests for the complete 5-pass translation pipeline."""

    def setUp(self) -> None:
        self.scientific_profile = DomainProfile(
            id=DomainType.SCIENTIFIC,
            title_fa="علمی",
            description="علمی و پژوهشی",
            system_prompt="متن علمی را با دقت اصطلاحات ترجمه کن.",
            banned_calques=["روی میز بودن"],
            terminology_map={"relativity": "نسبیت"},
        )
        self.literary_profile = DomainProfile(
            id=DomainType.LITERARY,
            title_fa="ادبی",
            description="ادبیات داستانی",
            system_prompt="ترجمه با نثر روان فارسی و سجاوندی دقیق.",
            typography=TypographicRules(
                invert_dialogue_tags=True,
                em_dash_policy=EmDashPolicy.ADAPT,
                strict_zwnj=True,
            ),
        )

    def test_full_pipeline_with_echo_backend(self) -> None:
        pipeline = TranslationPipeline(backend=EchoDraftBackend())
        raw_text = "In physics, $E=mc^2$ explains energy with 42 joules."

        segments, report = pipeline.run(raw_text, self.scientific_profile)

        self.assertEqual(len(segments), 1)
        self.assertTrue(report.passed)
        self.assertEqual(report.quality_score, 100.0)

        # 100% survival of formula and number
        self.assertIn("$E=mc^2$", segments[0].polished_text)
        self.assertIn("42", segments[0].polished_text)

    def test_full_pipeline_with_custom_persian_backend(self) -> None:
        def mock_translate(prompt: str, sys_prompt: str) -> str:
            # Replaces words while leaving protected tokens and numbers intact
            t = prompt.replace("According to relativity,", "طبق نسبیت،")
            t = t.replace("formula", "فرمول")
            t = t.replace("has 100 units.", "دارای ۱۰۰ واحد است.")
            return t

        pipeline = TranslationPipeline(backend=CallableTranslationBackend(mock_translate))
        raw_text = "According to relativity, formula $E=mc^2$ has 100 units."

        segments, report = pipeline.run(raw_text, self.scientific_profile)

        self.assertTrue(report.passed)
        final_text = segments[0].polished_text

        # Math survived 100%
        self.assertIn("$E=mc^2$", final_text)
        # Digits survived 100%
        self.assertTrue("100" in final_text or "۱۰۰" in final_text)
        # Persian terminology applied
        self.assertIn("نسبیت", final_text)

    def test_formulas_code_urls_and_numbers_survive_100_percent(self) -> None:
        raw_text = (
            "Review code `git status` and test URL https://example.com/api?v=2.\n\n"
            "Display equation:\n"
            "$$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$$\n\n"
            "Result confirmed with 99.9% precision at support@tarjoman.ai."
        )

        pipeline = TranslationPipeline(backend=EchoDraftBackend())
        translated = pipeline.translate_text(raw_text, self.scientific_profile)

        # All protected elements survived completely intact
        self.assertIn("`git status`", translated)
        self.assertIn("https://example.com/api?v=2", translated)
        self.assertIn("$$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$$", translated)
        self.assertIn("support@tarjoman.ai", translated)
        self.assertIn("99.9", translated)

    def test_literary_pipeline_dialogue_and_dashes(self) -> None:
        raw_text = '«منتظرم باش» هری گفت. هوا تاریک بود -- خیلی تاریک.'
        pipeline = TranslationPipeline(backend=EchoDraftBackend())
        segments, report = pipeline.run(raw_text, self.literary_profile)

        polished = segments[0].polished_text
        # Dialogue tag inverted
        self.assertIn("هری گفت: «منتظرم باش.»", polished)
        # Dashes adapted
        self.assertIn(" - ", polished)


if __name__ == "__main__":
    unittest.main()
