from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


PLUGIN_ROOT = Path(__file__).parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "audit_text.py"


def load_script():
    spec = importlib.util.spec_from_file_location("audit_text", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


module = load_script()


def args(**overrides):
    values = {
        "max_words": None,
        "max_sections": None,
        "similarity": 0.78,
        "flag_pattern": [],
        "fail_duplicates": False,
        "fail_near_duplicates": False,
        "fail_patterns": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class AuditTextTest(unittest.TestCase):
    def test_word_limit(self):
        result = module.audit("one two three", args(max_words=2))
        self.assertEqual(result.words, 3)
        self.assertEqual(result.failures, ["word count 3 exceeds 2"])

    def test_section_limit_ignores_headings_in_fenced_code(self):
        text = "# Real section\n\n```markdown\n# Example heading\n```"
        result = module.audit(text, args(max_sections=1))
        self.assertEqual(result.sections, 1)
        self.assertFalse(result.failures)

    def test_duplicate_sentence_survives_soft_wrapping(self):
        text = (
            "The worker retries failed writes\nthree times.\n\n"
            "The worker retries failed writes three times."
        )
        result = module.audit(text, args(fail_duplicates=True))
        self.assertEqual(result.sentences, 2)
        self.assertEqual(result.duplicate_sentences, [[1, 2]])
        self.assertTrue(result.failures)

    def test_duplicate_quoted_sentence(self):
        text = 'The worker said "Retry." The worker said "Retry."'
        result = module.audit(text, args(fail_duplicates=True))
        self.assertEqual(result.duplicate_sentences, [[1, 2]])

    def test_exact_duplicates_preserve_meaningful_punctuation(self):
        text = "Let's eat, Grandma. Let's eat Grandma."
        result = module.audit(text, args(fail_duplicates=True))
        self.assertFalse(result.duplicate_sentences)
        self.assertFalse(result.failures)

    def test_exact_duplicates_preserve_meaningful_capitalization(self):
        text = "Polish the draft.\n\npolish the draft."
        result = module.audit(text, args(fail_duplicates=True))
        self.assertFalse(result.duplicate_sentences)

    def test_literal_ship_is_not_flagged(self):
        result = module.audit("We ship release 2.4 after the canary passes.", args())
        self.assertFalse(result.flagged_patterns)

    def test_figurative_ship_is_flagged(self):
        result = module.audit("We need to ship the decision today.", args())
        self.assertTrue(result.flagged_patterns)

    def test_smart_apostrophe_is_normalized_for_patterns(self):
        result = module.audit("It’s worth noting that retries are bounded.", args())
        self.assertTrue(result.flagged_patterns)

    def test_patterns_ignore_fenced_and_inline_code(self):
        text = (
            "Use `it's worth noting` only in this test.\n\n"
            "```text\nThe key takeaway\n```"
        )
        result = module.audit(text, args(fail_patterns=True))
        self.assertFalse(result.flagged_patterns)
        self.assertFalse(result.failures)

    def test_custom_pattern(self):
        result = module.audit(
            "The hinge-point observation is retries must be idempotent.",
            args(flag_pattern=[r"\bhinge-point observation\b"]),
        )
        self.assertEqual(len(result.flagged_patterns), 1)

    def test_near_duplicate_paragraphs(self):
        text = (
            "The old column remains available during rollout, so the migration is safe.\n\n"
            "The migration is safe during rollout because the old column remains available."
        )
        result = module.audit(text, args(fail_near_duplicates=True, similarity=0.7))
        self.assertTrue(result.near_duplicate_paragraphs)
        self.assertTrue(result.failures)

    def test_repeated_openings(self):
        text = "The worker retries. The worker logs. The worker stops."
        result = module.audit(text, args())
        self.assertEqual(
            result.repeated_openings,
            [{"opening": "the worker", "sentences": [1, 2, 3]}],
        )

    def test_cli_reports_json_and_failure_exit(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--max-words", "2", "--json"],
            input="one two three",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(json.loads(completed.stdout)["words"], 3)

    def test_cli_rejects_invalid_regex_without_traceback(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--flag-pattern", "["],
            input="text",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("invalid regular expression", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_cli_rejects_similarity_outside_unit_interval(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--similarity", "1.2"],
            input="text",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("between 0 and 1", completed.stderr)


if __name__ == "__main__":
    unittest.main()
