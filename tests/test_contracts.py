import unittest
from tarjoman.core.contracts import (
    DomainType,
    EmDashPolicy,
    TypographicRules,
    DomainProfile,
    TextSegment,
    StageResult,
    AuditFinding,
    AuditReport,
    BookManifest,
)


class TestContracts(unittest.TestCase):
    def test_all_10_domains_exist(self):
        expected = {
            "literary",
            "scientific",
            "philosophy",
            "legal",
            "technical",
            "medical",
            "media",
            "financial",
            "classical",
            "transcreation",
        }
        actual = {d.value for d in DomainType}
        self.assertEqual(expected, actual)

    def test_book_manifest_structure(self):
        manifest = BookManifest(
            title="Sample Book",
            source_language="en",
            target_language="fa",
            total_chapters=5,
        )
        self.assertEqual(manifest.total_chapters, 5)
        self.assertEqual(manifest.terms_count, 0)
        self.assertEqual(manifest.current_chapter, 0)
        self.assertEqual(manifest.total_segments, 0)
        self.assertEqual(manifest.translated_segments, 0)

    def test_text_segment_reflection_critique_optional(self):
        seg = TextSegment(id=1, source_text="Hello world")
        self.assertIsNone(seg.reflection_critique)
        self.assertIsNone(seg.translated_text)
        self.assertIsNone(seg.polished_text)

        seg_with_critique = TextSegment(
            id=2,
            source_text="Test",
            reflection_critique="Critique text",
        )
        self.assertEqual(seg_with_critique.reflection_critique, "Critique text")

    def test_typographic_rules_defaults(self):
        rules = TypographicRules()
        self.assertEqual(rules.em_dash_policy, EmDashPolicy.ADAPT)
        self.assertTrue(rules.enforce_persian_quotes)
        self.assertTrue(rules.strict_zwnj)


if __name__ == "__main__":
    unittest.main()
