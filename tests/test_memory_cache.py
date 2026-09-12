"""
Tests for Memory, Cache, and Quality Review Fixes in Tarjoman Universal Translation Engine.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tarjoman.core.contracts import (
    DomainProfile,
    DomainType,
    TextSegment,
    TypographicRules,
)
from tarjoman.memory.cache import ResumableCache
from tarjoman.memory.state_manager import StateManager
from tarjoman.stages.stage1_pre_analysis import PreAnalysisStage
from tarjoman.stages.stage3_reflection import RuleBasedReflectionEngine
from tarjoman.stages.stage5_audit import AuditStage


class TestResumableCache(unittest.TestCase):
    """
    Tests for ResumableCache: persistence, resume checks, atomic updates, and exports.
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_path = Path(self.temp_dir.name) / "test_cache.json"
        self.cache = ResumableCache(cache_path=self.cache_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_save_and_retrieve_on_new_instance(self) -> None:
        self.cache.record_segment(
            chapter_id=1,
            segment_id=1,
            source_text="Call me Ishmael.",
            translated_text="مرا اسماعیل صدا بزنید.",
            polished_text="اسماعیلم بنامید.",
        )

        # Create completely fresh instance loading from same file
        new_instance = ResumableCache(cache_path=self.cache_path)
        seg = new_instance.get_segment(1, 1, "Call me Ishmael.")
        self.assertIsNotNone(seg)
        assert seg is not None
        self.assertEqual(seg["chapter_id"], 1)
        self.assertEqual(seg["segment_id"], 1)
        self.assertEqual(seg["source_text"], "Call me Ishmael.")
        self.assertEqual(seg["translated_text"], "مرا اسماعیل صدا بزنید.")
        self.assertEqual(seg["polished_text"], "اسماعیلم بنامید.")

    def test_resume_behavior_is_completed(self) -> None:
        source = "Some years ago—never mind how long precisely."
        self.assertFalse(self.cache.is_completed(1, 2, source))

        self.cache.record_segment(
            chapter_id=1,
            segment_id=2,
            source_text=source,
            translated_text="چند سال پیش—مهم نیست دقیقاً چند سال.",
        )

        self.assertTrue(self.cache.is_completed(1, 2, source))
        # Different source text for same chapter & segment id is NOT completed
        self.assertFalse(self.cache.is_completed(1, 2, "Different text"))

    def test_get_stats_and_export_chapter(self) -> None:
        self.cache.record_segment(1, 2, "Segment two", "بخش دو")
        self.cache.record_segment(1, 1, "Segment one", "بخش یک")
        self.cache.record_segment(2, 1, "Chapter two segment", "فصل دو بخش یک")

        stats = self.cache.get_stats()
        self.assertEqual(stats["total_cached"], 3)
        self.assertEqual(stats["chapters_count"], 2)

        # Chapter 1 export should be sorted by segment_id
        exported = self.cache.export_chapter(chapter_id=1)
        self.assertEqual(len(exported), 2)
        self.assertEqual(exported[0]["segment_id"], 1)
        self.assertEqual(exported[1]["segment_id"], 2)

    def test_clear_cache(self) -> None:
        self.cache.record_segment(1, 1, "Source", "ترجمه")
        self.assertEqual(self.cache.get_stats()["total_cached"], 1)

        self.cache.clear()
        self.assertEqual(self.cache.get_stats()["total_cached"], 0)

        # Reopen on disk to ensure persistent clear
        reopened = ResumableCache(cache_path=self.cache_path)
        self.assertEqual(reopened.get_stats()["total_cached"], 0)


class TestStateManager(unittest.TestCase):
    """
    Tests for StateManager: Dynamic TSV Termbase, Voice Ledger, and Sliding Context.
    """

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tb_path = Path(self.temp_dir.name) / "termbase.tsv"
        self.vl_path = Path(self.temp_dir.name) / "voice_ledger.json"
        self.state_mgr = StateManager(
            termbase_path=self.tb_path,
            voice_ledger_path=self.vl_path,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_termbase_load_save_query(self) -> None:
        self.state_mgr.record_term(
            en_term="attention mechanism",
            fa_term="سازوکار توجه",
            domain="scientific",
            notes="Transformers",
        )
        self.state_mgr.record_term(
            en_term="tokenization",
            fa_term="نشانه‌گذاری",
            domain="technical",
            notes="NLP",
        )

        self.assertEqual(self.state_mgr.resolve_term("attention mechanism"), "سازوکار توجه")
        # Case-insensitive resolution
        self.assertEqual(self.state_mgr.resolve_term("Attention Mechanism"), "سازوکار توجه")
        self.assertTrue(self.state_mgr.has_term("tokenization"))
        self.assertFalse(self.state_mgr.has_term("nonexistent term"))

        # Verify on newly initialized instance from persistent TSV
        new_mgr = StateManager(termbase_path=self.tb_path)
        self.assertEqual(new_mgr.resolve_term("attention mechanism"), "سازوکار توجه")
        self.assertEqual(new_mgr.resolve_term("tokenization"), "نشانه‌گذاری")

    def test_termbase_domain_filtering(self) -> None:
        self.state_mgr.record_term("deep learning", "یادگیری عمیق", domain="scientific")
        self.state_mgr.record_term("neural network", "شبکه عصبی", domain="scientific")
        self.state_mgr.record_term("injunction", "دستور موقت", domain="legal")

        all_terms = self.state_mgr.get_all_terms()
        self.assertEqual(len(all_terms), 3)

        sci_terms = self.state_mgr.get_all_terms(domain="scientific")
        self.assertEqual(len(sci_terms), 2)
        self.assertIn("deep learning", sci_terms)
        self.assertNotIn("injunction", sci_terms)

        legal_terms = self.state_mgr.get_all_terms(domain="legal")
        self.assertEqual(len(legal_terms), 1)

    def test_character_voice_ledger(self) -> None:
        rustam_profile = {
            "register": "epic_formal",
            "pronoun_address": "شما",
            "speech_quirk": "archaic vocabulary and imperative cadence",
        }
        self.state_mgr.record_voice_profile("Rustam", rustam_profile)

        profile = self.state_mgr.get_voice_profile("Rustam")
        self.assertIsNotNone(profile)
        assert profile is not None
        self.assertEqual(profile["register"], "epic_formal")

        # Case-insensitive query
        ci_profile = self.state_mgr.get_voice_profile("rustam")
        self.assertIsNotNone(ci_profile)

        # Missing character
        self.assertIsNone(self.state_mgr.get_voice_profile("Sohrab"))

        # Persistent reload
        reloaded = StateManager(voice_ledger_path=self.vl_path)
        reloaded_prof = reloaded.get_voice_profile("Rustam")
        self.assertIsNotNone(reloaded_prof)

    def test_sliding_context_window(self) -> None:
        p1 = "Paragraph one introduces the opening setting and background."  # 8 words
        p2 = "Paragraph two describes the protagonist encountering a sudden challenge."  # 9 words
        p3 = "Paragraph three resolves the initial encounter with swift determination."  # 9 words

        # 1. When max_words fits all paragraphs
        full_ctx = StateManager.build_sliding_context([p1, p2, p3], max_words=50)
        self.assertEqual(full_ctx, f"{p1}\n\n{p2}\n\n{p3}")

        # 2. When max_words fits only the 2 most recent paragraphs (p2 + p3 = 18 words)
        partial_ctx = StateManager.build_sliding_context([p1, p2, p3], max_words=20)
        self.assertEqual(partial_ctx, f"{p2}\n\n{p3}")

        # 3. When max_words fits only the most recent paragraph (p3 = 9 words)
        single_ctx = StateManager.build_sliding_context([p1, p2, p3], max_words=12)
        self.assertEqual(single_ctx, p3)

        # 4. When even the single most recent paragraph exceeds max_words, takes tail
        tail_ctx = StateManager.build_sliding_context([p3], max_words=4)
        self.assertEqual(tail_ctx, "encounter with swift determination.")

        # 5. Empty or non-positive max_words
        self.assertEqual(StateManager.build_sliding_context([]), "")
        self.assertEqual(StateManager.build_sliding_context([p1], max_words=0), "")


class TestQualityImprovementsAndMomayyez(unittest.TestCase):
    """
    Tests for Task 4 review fixes:
    - Persian momayyez ٫ digit normalization without false-positive number omissions.
    - Protected token cleaning before digit extraction in reflection.
    - Inline math regex avoiding currency like $50 and $100.
    - URL regex avoiding trailing punctuation.
    """

    def setUp(self) -> None:
        self.profile = DomainProfile(
            id=DomainType.SCIENTIFIC,
            title_fa="علمی و دانشگاهی",
            description="ترجمه متون دانشگاهی و فنی",
            system_prompt="سیستم پرامپت علمی",
            typography=TypographicRules(isolate_english_terms=True),
        )

    def test_momayyez_in_audit_no_false_positive(self) -> None:
        """
        Ensure Persian momayyez ٫ (e.g. ۳٫۱۴) matches English 3.14 and does not trigger MQM-NUM-OMISSION.
        """
        seg = TextSegment(
            id=1,
            source_text="The value of pi is approximately 3.14 and Euler is 2.718.",
            translated_text="مقدار پی تقریباً ۳٫۱۴ و اویلر ۲٫۷۱۸ است.",
            polished_text="مقدار پی تقریباً ۳٫۱۴ و اویلر ۲٫۷۱۸ است.",
        )
        audit_stage = AuditStage()
        report = audit_stage.audit([seg], self.profile)

        omission_findings = [f for f in report.findings if f.rule_id == "MQM-NUM-OMISSION"]
        self.assertEqual(len(omission_findings), 0)
        self.assertEqual(report.omission_count, 0)
        self.assertTrue(report.passed)

    def test_momayyez_in_reflection_no_false_positive(self) -> None:
        """
        Ensure RuleBasedReflectionEngine recognizes momayyez ٫ without raising missing number critique.
        """
        engine = RuleBasedReflectionEngine()
        critique, _refined = engine.reflect(
            source="The efficiency is 98.5 percent with factor 1.25.",
            draft="بازدهی ۹۸٫۵ درصد با ضریب ۱٫۲۵ است.",
            profile=self.profile,
        )
        self.assertNotIn("Missing number", critique)

    def test_clean_protected_tokens_before_digit_extraction(self) -> None:
        """
        Ensure ⟦PROTECTED_0⟧ does not leak digit '0' to satisfy or distort missing number detection.
        """
        engine = RuleBasedReflectionEngine()
        # Source has number 42, target has 42 plus a protected token ⟦PROTECTED_0⟧
        critique, _refined = engine.reflect(
            source="The answer is 42.",
            draft="پاسخ ۴۲ است ⟦PROTECTED_0⟧.",
            profile=self.profile,
            metadata={"protected_tokens": {"⟦PROTECTED_0⟧": "https://example.com"}},
        )
        self.assertNotIn("Missing number", critique)

        # If source has number 0, but draft only has ⟦PROTECTED_0⟧ without Persian or English 0:
        critique_missing_zero, _ = engine.reflect(
            source="The base value is 0.",
            draft="مقدار پایه است ⟦PROTECTED_0⟧.",
            profile=self.profile,
            metadata={"protected_tokens": {"⟦PROTECTED_0⟧": "https://example.com"}},
        )
        # Should correctly detect that 0 is missing!
        self.assertIn("Missing number(s) from source: 0", critique_missing_zero)

    def test_inline_math_avoids_currency(self) -> None:
        """
        Check that inline math regex does not match currency amounts like $50 and $100.
        """
        pre_stage = PreAnalysisStage(split_paragraphs=False)

        # Currency example
        currency_text = "The ticket costs $50 and the VIP pass is $100."
        masked_curr, tokens_curr = pre_stage.mask_text(currency_text)
        # Currency must NOT be masked as protected tokens
        self.assertEqual(len(tokens_curr), 0)
        self.assertEqual(masked_curr, currency_text)

        # Valid inline LaTeX math
        math_text = "Let $x + y = z$ be the equation and $\\alpha$ be the angle."
        masked_math, tokens_math = pre_stage.mask_text(math_text)
        self.assertEqual(len(tokens_math), 2)
        restored = pre_stage.restore_tokens(masked_math, tokens_math)
        self.assertEqual(restored, math_text)

    def test_url_avoids_trailing_punctuation(self) -> None:
        """
        Check that URL regex does not capture trailing punctuation (, . ; : ! ?).
        """
        pre_stage = PreAnalysisStage(split_paragraphs=False)

        text_with_urls = (
            "Visit https://example.com/api, review https://example.com/docs. "
            "See https://example.com/faq?q=1; and check https://example.com/contact!"
        )
        masked, tokens = pre_stage.mask_text(text_with_urls)
        self.assertEqual(len(tokens), 4)

        for token, original_url in tokens.items():
            self.assertFalse(original_url.endswith(","))
            self.assertFalse(original_url.endswith("."))
            self.assertFalse(original_url.endswith(";"))
            self.assertFalse(original_url.endswith("!"))

        restored = pre_stage.restore_tokens(masked, tokens)
        self.assertEqual(restored, text_with_urls)


if __name__ == "__main__":
    unittest.main()
