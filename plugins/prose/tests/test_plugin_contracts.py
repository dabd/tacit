from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


PLUGIN_ROOT = Path(__file__).parents[1]
REPOSITORY_ROOT = PLUGIN_ROOT.parents[1]
SKILLS = ("prose", "compress", "laconic")


def plugin_text(relative_path: str) -> str:
    return (PLUGIN_ROOT / relative_path).read_text(encoding="utf-8")


def section(content: str, title: str) -> str:
    match = re.search(
        rf"(?ms)^#{{2}} {re.escape(title)}\s*$\n(.*?)(?=^#{{2}} |\Z)", content
    )
    if match is None:
        raise AssertionError(f"Missing section: {title}")
    return match.group(1)


def example_pair(content: str, title: str) -> tuple[str, str]:
    match = re.search(
        r"(?ms)^\*\*Before:\*\*\s*(.*?)^\*\*After:\*\*\s*(.*)\Z",
        section(content, title),
    )
    if match is None:
        raise AssertionError(f"Missing Before/After pair: {title}")
    return tuple(" ".join(block.split()) for block in match.groups())


class PluginContractsTest(unittest.TestCase):
    def test_package_and_activation_contract(self):
        skill_directories = {
            path.name for path in (PLUGIN_ROOT / "skills").iterdir() if path.is_dir()
        }
        command_files = {
            path.name for path in (PLUGIN_ROOT / "commands").iterdir() if path.is_file()
        }
        self.assertEqual(skill_directories, set(SKILLS))
        self.assertEqual(command_files, {"polish.md"})
        for removed_directory in ("agents", "evals", "scripts"):
            self.assertFalse((PLUGIN_ROOT / removed_directory).exists())

        portable_keys = {
            "name",
            "description",
            "license",
            "metadata",
            "allowed-tools",
        }
        boundaries = {
            "prose": ("draft", "ordinary coding"),
            "compress": ("extreme", "ordinary editing"),
            "laconic": ("including when combined with compression", "compression alone"),
        }
        for skill, terms in boundaries.items():
            with self.subTest(skill=skill):
                content = plugin_text(f"skills/{skill}/SKILL.md")
                frontmatter = content.split("---", 2)[1]
                keys = set(re.findall(r"(?m)^([a-z][a-z-]*):", frontmatter))
                self.assertLessEqual(keys, portable_keys)
                description = re.search(
                    r"(?ms)^description:\s*(.*?)(?=^[a-z][a-z-]*:\s|\Z)",
                    frontmatter,
                )
                self.assertIsNotNone(description)
                normalized = " ".join(description.group(1).split()).lower()
                self.assertIn("use when", normalized)
                self.assertIn("do not use", normalized)
                for term in terms:
                    self.assertIn(term, normalized)
                self.assertNotRegex(content, r"/prose(?::[a-z-]+)?")
                self.assertNotRegex(content, r"\$prose:[a-z-]+")
                self.assertNotIn("$ARGUMENTS", content)

        prose = plugin_text("skills/prose/SKILL.md").lower()
        self.assertIn("unless the user also asks for prose editing", prose)
        polish = plugin_text("commands/polish.md")
        self.assertIn("$ARGUMENTS", polish)
        self.assertRegex(
            polish, r"(?i)(?:apply|use|invoke)\s+the\s+`?prose`?\s+skill"
        )

    def test_one_foundations_document_supplies_every_linked_contract(self):
        foundations = list(PLUGIN_ROOT.rglob("FOUNDATIONS.md"))
        self.assertEqual(foundations, [PLUGIN_ROOT / "FOUNDATIONS.md"])
        headings = re.findall(r"(?m)^#{1,6} ([^#\n]+?)\s*$", plugin_text("FOUNDATIONS.md"))
        anchors = {
            re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", heading.lower()).strip())
            for heading in headings
        }

        for skill in SKILLS:
            with self.subTest(skill=skill):
                skill_path = PLUGIN_ROOT / "skills" / skill / "SKILL.md"
                targets = re.findall(
                    r"\[[^]]+\]\(([^)]+)\)", skill_path.read_text(encoding="utf-8")
                )
                self.assertTrue(targets)
                for target in targets:
                    match = re.fullmatch(
                        r"\.\./\.\./FOUNDATIONS\.md#([a-z0-9-]+)", target
                    )
                    self.assertIsNotNone(match)
                    self.assertIn(match.group(1), anchors)

    def test_semantic_responsibilities_and_composition_are_distinct(self):
        prose = plugin_text("skills/prose/SKILL.md")
        compress = plugin_text("skills/compress/SKILL.md")
        laconic = plugin_text("skills/laconic/SKILL.md")
        foundations = plugin_text("FOUNDATIONS.md")

        self.assertIn("recognisable voice", prose.lower())
        self.assertIn(
            "Preserve the document's headings, section order, and other "
            "macrostructure unless the user explicitly asks to reorganise it.",
            prose,
        )
        self.assertIn(
            "Inventory all semantic content before classifying it as required "
            "or optional.",
            compress,
        )
        self.assertIn(
            "Compress may remove optional content after building the semantic "
            "inventory. It does not choose the register.",
            compress,
        )
        self.assertIn("Do not remove unique information.", laconic)
        self.assertNotIn("voice", section(laconic, "Register").lower())
        self.assertNotIn(
            "voice", section(foundations, "Shared preservation contract").lower()
        )

        ordering = (
            "When both modifiers are requested, apply Compress first and Laconic second."
        )
        for content in (foundations, compress, laconic):
            self.assertIn(ordering, content)

    def test_examples_preserve_proposals_modality_and_rationale(self):
        examples = plugin_text("examples/before-after.md")
        _, compressed = example_pair(examples, "Extreme compression reconstructs")
        self.assertEqual(
            compressed,
            "We propose single-flight token refresh: concurrent refreshes can "
            "overwrite the token and log the user out.",
        )

        combined_before, combined_after = example_pair(
            examples, "Compress plus Laconic"
        )
        self.assertEqual(
            combined_before.count("The old column remains available during rollout."),
            2,
        )
        self.assertIn(
            "We should remove the old column after every reader migrates.",
            combined_before,
        )
        self.assertEqual(
            combined_after,
            "The old column remains available during rollout for compatibility. "
            "We should remove it after every reader migrates.",
        )

    def test_surfaces_expose_the_same_plugin_and_distinct_invocations(self):
        manifests = {
            "claude": json.loads(plugin_text(".claude-plugin/plugin.json")),
            "codex": json.loads(plugin_text(".codex-plugin/plugin.json")),
        }
        for manifest in manifests.values():
            self.assertEqual((manifest["name"], manifest["version"]), ("prose", "0.3.0"))
        self.assertEqual(manifests["codex"]["skills"], "./skills/")
        shared_fields = (
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
        )
        self.assertEqual(
            {field: manifests["claude"][field] for field in shared_fields},
            {field: manifests["codex"][field] for field in shared_fields},
        )

        marketplace_paths = (
            REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json",
            REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json",
        )
        for path in marketplace_paths:
            with self.subTest(marketplace=path):
                marketplace = json.loads(path.read_text(encoding="utf-8"))
                entries = [
                    entry for entry in marketplace["plugins"] if entry["name"] == "prose"
                ]
                self.assertEqual(len(entries), 1)
                source = entries[0]["source"]
                self.assertEqual(
                    source["path"] if isinstance(source, dict) else source,
                    "./plugins/prose",
                )

        readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
        claude = section(readme, "Claude Code")
        codex = section(readme, "Codex")
        self.assertEqual(
            set(re.findall(r"/prose:([a-z-]+)", claude)),
            {"polish", "compress", "laconic"},
        )
        self.assertEqual(
            set(re.findall(r"\$prose:([a-z-]+)", codex)),
            {"prose", "compress", "laconic"},
        )


if __name__ == "__main__":
    unittest.main()
