from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


PLUGIN_ROOT = Path(__file__).parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "run_evals.py"


def load_script():
    spec = importlib.util.spec_from_file_location("run_evals", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


module = load_script()


class RunEvalsTest(unittest.TestCase):
    def test_grade_output_checks_deterministic_requirements(self):
        case = {
            "id": "sample",
            "input": "Original text.",
            "requirements": {
                "must_preserve_exact": ["INC-204"],
                "must_not_contain": ["load-bearing"],
                "max_words": 5,
                "max_sections": 0,
                "output_only": True,
            },
        }
        grade = module.grade_output(case, "Keep INC-204 safe.")
        self.assertEqual(grade.status, "pass")
        self.assertFalse(grade.failures)

    def test_grade_output_marks_semantic_checks_for_review(self):
        case = {
            "id": "semantic",
            "input": "The timeout may follow pool exhaustion.",
            "requirements": {
                "must_preserve": ["may", "pool exhaustion"],
                "manual_checks": ["uncertainty is not strengthened"],
            },
        }
        grade = module.grade_output(case, "Pool exhaustion may cause the timeout.")
        self.assertEqual(grade.status, "manual")
        self.assertEqual(grade.manual_checks, ["uncertainty is not strengthened"])

    def test_grade_output_detects_unsolicited_explanation(self):
        case = {
            "id": "output-only",
            "input": "Retry failed writes.",
            "requirements": {"output_only": True},
        }
        grade = module.grade_output(case, "Here is the revised text:\n\nRetry failed writes.")
        self.assertEqual(grade.status, "fail")
        self.assertIn("output includes an explanation marker", grade.failures)

    def test_extract_invoked_skills_from_stream_events(self):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "prose:compress"},
                        }
                    ]
                },
            }
        ]
        self.assertEqual(module.extract_invoked_skills(events), ["prose:compress"])

    def test_slash_activation_requires_runtime_command_resolution(self):
        case = {
            "expected_skill": "compress",
            "invocation": "slash",
            "prompt": "/prose:compress Reduce this.",
        }
        self.assertEqual(module.activation_status(case, [], []), "fail")
        self.assertEqual(
            module.activation_status(case, [], ["prose:compress"]),
            "pass",
        )
        case["prompt"] = "Reduce this."
        self.assertEqual(module.activation_status(case, [], ["prose:compress"]), "fail")

    def test_natural_activation_requires_skill_invocation(self):
        case = {
            "expected_skill": "compress",
            "invocation": "natural",
            "prompt": "Reduce this as far as possible.",
        }
        self.assertEqual(module.activation_status(case, [], ["prose:compress"]), "fail")
        self.assertEqual(
            module.activation_status(case, ["prose:compress"], ["prose:compress"]),
            "pass",
        )

    def test_behavior_grade_fails_without_runtime_skill_evidence(self):
        case = {
            "id": "missing-skill",
            "skill": "compress",
            "prompt": "/prose:compress Reduce this.",
            "input": "Keep this fact.",
            "requirements": {"must_preserve": ["fact"]},
        }
        run = {"output": "Keep this fact.", "invoked_skills": [], "available_commands": []}
        grade = module.grade_behavior_run(case, run)
        self.assertEqual(grade.status, "fail")
        self.assertIn("missing runtime evidence for prose:compress", grade.failures)

    def test_extract_available_commands_from_init_event(self):
        events = [
            {
                "type": "system",
                "subtype": "init",
                "slash_commands": ["prose:compress", "prose:laconic"],
            }
        ]
        self.assertEqual(
            module.extract_available_commands(events),
            ["prose:compress", "prose:laconic"],
        )

    def test_validate_corpus_accepts_repository_cases(self):
        summary = module.validate_corpus(PLUGIN_ROOT)
        self.assertGreaterEqual(summary["activation_cases"], 10)
        self.assertGreaterEqual(summary["behavior_cases"], 12)
        self.assertFalse(summary["errors"])

    def test_cli_validate_only(self):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--plugin-root", str(PLUGIN_ROOT), "--validate-only"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertFalse(payload["errors"])

    def test_write_result_keeps_raw_events_and_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            path = module.write_result(
                Path(directory),
                {
                    "id": "case-1",
                    "model": "sonnet",
                    "surface_version": "2.1.215",
                    "output": "Result",
                    "events": [{"type": "result", "result": "Result"}],
                },
            )
            saved = json.loads(path.read_text())
            self.assertEqual(saved["model"], "sonnet")
            self.assertEqual(saved["events"][0]["type"], "result")

    def test_run_directory_identifies_plugin_state(self):
        metadata = {"plugin_version": "0.2.0", "plugin_hash": "a" * 64}
        started_at = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            path, run_id = module.create_run_directory(
                Path(directory), metadata, started_at=started_at
            )
            self.assertTrue(path.is_dir())
            self.assertIn("v0.2.0", run_id)
            self.assertIn("aaaaaaaaaaaa", run_id)

    def test_plugin_metadata_records_manifest_version_and_content_hash(self):
        metadata = module.plugin_metadata(PLUGIN_ROOT)
        self.assertEqual(metadata["plugin_version"], "0.2.0")
        self.assertRegex(metadata["plugin_hash"], r"^[0-9a-f]{64}$")

    @patch.object(module.subprocess, "run")
    def test_run_claude_disables_installed_plugin_settings(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, '{"type":"result","result":"OK"}\n', "")
        module.run_claude("claude", "Prompt", "sonnet", PLUGIN_ROOT, None)
        command = run.call_args.args[0]
        index = command.index("--setting-sources")
        self.assertEqual(command[index + 1], "")

    @patch.object(module.subprocess, "run")
    def test_run_claude_uses_safe_mode_for_baseline(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, '{"type":"result","result":"OK"}\n', "")
        module.run_claude("claude", "Prompt", "sonnet", None, None)
        self.assertIn("--safe-mode", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
