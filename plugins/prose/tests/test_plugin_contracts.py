from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


PLUGIN_ROOT = Path(__file__).parents[1]
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]


def text(path: str) -> str:
    return (PLUGIN_ROOT / path).read_text(encoding="utf-8")


class PluginContractsTest(unittest.TestCase):
    def test_explicit_modes_allow_natural_language_activation(self):
        for skill in ("compress", "laconic"):
            content = text(f"skills/{skill}/SKILL.md")
            self.assertNotIn("disable-model-invocation: true", content)

    def test_prose_excludes_substantive_review(self):
        content = text("skills/prose/SKILL.md")
        for term in ("architecture", "correctness", "security", "prose"):
            self.assertIn(term, content.split("---", 2)[1].lower())

    def test_foundations_is_packaged_and_cited_by_every_skill(self):
        foundations = text("FOUNDATIONS.md")
        for heading in (
            "## Preserve meaning",
            "## Prefer concrete agency",
            "## Eliminate duplicated claims",
            "## Compression philosophy",
            "## Tacit-specific contributions",
        ):
            self.assertIn(heading, foundations)
        for skill in ("prose", "compress", "laconic"):
            skill_text = text(f"skills/{skill}/SKILL.md")
            self.assertIn("FOUNDATIONS.md", skill_text)
            self.assertNotIn("../../FOUNDATIONS.md", skill_text)
            self.assertEqual(text(f"skills/{skill}/FOUNDATIONS.md"), foundations)

    def test_reviewers_receive_limits_and_document_purpose(self):
        content = text("skills/compress/SKILL.md")
        for phrase in ("hard limits", "document purpose", "semantic inventory"):
            self.assertIn(phrase, content)

    def test_loaded_prompts_do_not_use_known_conspicuous_phrases(self):
        prohibited = (
            "job of the text",
            "throat-clearing",
            "advertise a model",
            "stylistic flourishes",
            "observable finish line",
            "load-bearing reasoning",
            "carry its own weight",
        )
        paths = list((PLUGIN_ROOT / "skills").rglob("*.md")) + list(
            (PLUGIN_ROOT / "agents").rglob("*.md")
        )
        for path in paths:
            content = path.read_text(encoding="utf-8").lower()
            for phrase in prohibited:
                self.assertNotIn(phrase, content, f"{phrase!r} in {path}")

    def test_human_facing_markdown_uses_ascii_hyphens(self):
        for path in REPOSITORY_ROOT.rglob("*.md"):
            content = path.read_text(encoding="utf-8")
            self.assertNotRegex(content, re.compile("[\u2011\u2013\u2014]"), str(path))

    def test_json_files_parse_and_version_is_semantic(self):
        for path in REPOSITORY_ROOT.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
        manifest = json.loads(text(".claude-plugin/plugin.json"))
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
