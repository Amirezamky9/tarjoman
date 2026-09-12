import unittest
from tarjoman.core.contracts import DomainType, EmDashPolicy
from tarjoman.domains import DomainRegistry, DomainRouter, DOMAIN_ALIASES


class TestRouter10Domains(unittest.TestCase):
    def setUp(self):
        self.registry = DomainRegistry()
        self.router = DomainRouter(registry=self.registry)

    def test_all_10_profiles_load_from_registry(self):
        """Verify all 10 domain profiles load properly with complete configurations."""
        profiles = self.registry.list_all()
        self.assertEqual(len(profiles), 10)

        domain_ids = {p.id for p in profiles}
        expected_ids = set(DomainType)
        self.assertEqual(domain_ids, expected_ids)

        for profile in profiles:
            self.assertTrue(len(profile.title_fa) > 0)
            self.assertTrue(len(profile.description) > 0)
            self.assertTrue(len(profile.system_prompt) > 0)
            self.assertIsNotNone(profile.typography)

        # Check domain-specific typography & policies
        lit = self.registry.get(DomainType.LITERARY)
        self.assertEqual(lit.typography.em_dash_policy, EmDashPolicy.ERADICATE)
        self.assertTrue(lit.typography.enforce_persian_quotes)
        self.assertTrue(lit.typography.invert_dialogue_tags)
        self.assertIn("توسط", lit.banned_calques)

        sci = self.registry.get(DomainType.SCIENTIFIC)
        self.assertEqual(sci.typography.em_dash_policy, EmDashPolicy.ADAPT)
        self.assertTrue(sci.typography.western_digits)
        self.assertTrue(sci.typography.isolate_english_terms)

        tech = self.registry.get(DomainType.TECHNICAL)
        self.assertEqual(tech.typography.em_dash_policy, EmDashPolicy.PRESERVE)
        self.assertFalse(tech.typography.enforce_persian_quotes)
        self.assertTrue(tech.typography.western_digits)

        med = self.registry.get(DomainType.MEDICAL)
        self.assertTrue(med.typography.western_digits)
        self.assertIn("INN", med.system_prompt)

        phil = self.registry.get(DomainType.PHILOSOPHY)
        self.assertIn("Dasein", phil.system_prompt)

        leg = self.registry.get(DomainType.LEGAL)
        self.assertIn("shall", leg.system_prompt)

        media = self.registry.get(DomainType.MEDIA)
        self.assertIn("هرم وارونه", media.system_prompt)

        fin = self.registry.get(DomainType.FINANCIAL)
        self.assertTrue(fin.typography.western_digits)
        self.assertIn("EBITDA", fin.system_prompt)

        classic = self.registry.get(DomainType.CLASSICAL)
        self.assertIn("کهن", classic.system_prompt)

        trans = self.registry.get(DomainType.TRANSCREATION)
        self.assertIn("Transcreation", trans.system_prompt)

    def test_routing_10_domains(self):
        """Test intelligent text classification for all 10 domains."""
        test_samples = [
            (
                "She whispered softly in the dark shadows, smiling through her tears as the protagonist looked back.",
                DomainType.LITERARY,
            ),
            (
                "The research methodology yielded a statistically significant correlation with p-value < 0.01 in the empirical dataset.",
                DomainType.SCIENTIFIC,
            ),
            (
                "Heidegger's inquiry into Dasein and fundamental ontology revolutionized modern phenomenology and existentialism.",
                DomainType.PHILOSOPHY,
            ),
            (
                "The party shall hereby indemnify the licensee against all liabilities pursuant to clause 4 in case of breach of contract.",
                DomainType.LEGAL,
            ),
            (
                "Deploy the docker container to expose the api endpoint and inspect the compile stack trace.",
                DomainType.TECHNICAL,
            ),
            (
                "The patient underwent biopsy following clinical diagnosis, with a dosage of 500 mg amoxicillin administered.",
                DomainType.MEDICAL,
            ),
            (
                "Breaking news: according to Reuters, the spokesperson announced at a press conference that talks concluded.",
                DomainType.MEDIA,
            ),
            (
                "The corporation reported higher quarterly EBITDA and strong cash flow on its fiscal year balance sheet.",
                DomainType.FINANCIAL,
            ),
            (
                "Thou shalt heed the ancient chronicle of old, for the noble king reigneth over the sacred realm.",
                DomainType.CLASSICAL,
            ),
            (
                "Unleash your potential with our revolutionary new tagline and inspiring brand identity campaign.",
                DomainType.TRANSCREATION,
            ),
        ]

        for text, expected_domain in test_samples:
            profile, confidence = self.router.route(text)
            self.assertEqual(
                profile.id,
                expected_domain,
                f"Failed to route text to {expected_domain.value}: {text}",
            )
            self.assertGreaterEqual(confidence, 0.50)

    def test_persian_alias_overrides(self):
        """Test overriding classification using Persian and English aliases."""
        alias_tests = [
            ("فلسفه", DomainType.PHILOSOPHY),
            ("پزشکی", DomainType.MEDICAL),
            ("دارو", DomainType.MEDICAL),
            ("مالی", DomainType.FINANCIAL),
            ("اقتصاد", DomainType.FINANCIAL),
            ("کهن", DomainType.CLASSICAL),
            ("تبلیغات", DomainType.TRANSCREATION),
            ("شعار", DomainType.TRANSCREATION),
            ("ادبی", DomainType.LITERARY),
            ("علمی", DomainType.SCIENTIFIC),
            ("حقوقی", DomainType.LEGAL),
            ("فنی", DomainType.TECHNICAL),
            ("خبر", DomainType.MEDIA),
            ("scientific", DomainType.SCIENTIFIC),
            ("legal", DomainType.LEGAL),
        ]

        sample_text = "Some generic sentence that could be anything."
        for alias, expected_domain in alias_tests:
            profile, confidence = self.router.route(sample_text, override=alias)
            self.assertEqual(
                profile.id,
                expected_domain,
                f"Override '{alias}' failed to resolve to {expected_domain.value}",
            )
            self.assertEqual(confidence, 1.0)

    def test_invalid_override_raises_value_error(self):
        """Test that unknown domain override raises ValueError."""
        with self.assertRaises(ValueError):
            self.router.route("Hello world", override="nonexistent_domain_xyz")

    def test_registry_get_flexibility(self):
        """Test registry get method supports enum, string, and Persian aliases."""
        p1 = self.registry.get(DomainType.PHILOSOPHY)
        p2 = self.registry.get("philosophy")
        p3 = self.registry.get("فلسفه")
        self.assertEqual(p1.id, DomainType.PHILOSOPHY)
        self.assertEqual(p2.id, DomainType.PHILOSOPHY)
        self.assertEqual(p3.id, DomainType.PHILOSOPHY)


if __name__ == "__main__":
    unittest.main()
