#!/usr/bin/env python3
"""Run or validate Tacit's activation and behavior evaluation corpus."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PLUGIN_ROOT = SCRIPT_DIR.parent


def load_audit_module():
    path = SCRIPT_DIR / "audit_text.py"
    spec = importlib.util.spec_from_file_location("tacit_audit_text", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


audit_text = load_audit_module()

REQUIRED_TAGS = {
    "attribution",
    "claim-duplication",
    "clean-noop",
    "future-tic",
    "hard-section-limit",
    "hard-word-limit",
    "impossible-limit",
    "laconic",
    "link-symbol",
    "literal-domain",
    "output-only",
    "uncertainty",
}
EXPLANATION_MARKERS = (
    "here is the revised",
    "here's the revised",
    "revised text:",
    "changes made:",
    "explanation:",
)


@dataclass
class Grade:
    status: str
    failures: list[str]
    manual_checks: list[str]


def grade_status(failures: list[str], manual_checks: list[str]) -> str:
    if failures:
        return "fail"
    if manual_checks:
        return "manual"
    return "pass"


def normalized(text: str) -> str:
    return " ".join(text.casefold().split())


def audit_args(max_words: int | None, max_sections: int | None) -> argparse.Namespace:
    return argparse.Namespace(
        max_words=max_words,
        max_sections=max_sections,
        similarity=0.78,
        flag_pattern=[],
        fail_duplicates=False,
        fail_near_duplicates=False,
        fail_patterns=False,
    )


def grade_output(case: dict[str, Any], output: str) -> Grade:
    requirements = case.get("requirements", {})
    failures: list[str] = []
    compact_output = normalized(output)

    for phrase in requirements.get("must_preserve", []):
        if normalized(phrase) not in compact_output:
            failures.append(f"missing required text: {phrase}")
    for phrase in requirements.get("must_preserve_exact", []):
        if phrase not in output:
            failures.append(f"missing exact text: {phrase}")
    for phrase in requirements.get("must_not_contain", []):
        if normalized(phrase) in compact_output:
            failures.append(f"contains prohibited text: {phrase}")

    max_words = requirements.get("max_words")
    max_sections = requirements.get("max_sections")
    measured = audit_text.audit(output, audit_args(max_words, max_sections))
    failures.extend(measured.failures)

    if requirements.get("prefer_unchanged") and output.strip() != case.get("input", "").strip():
        failures.append("clean input changed")
    if "max_word_ratio" in requirements and case.get("input"):
        source_words = max(1, len(audit_text.words(case["input"])))
        if measured.words / source_words > requirements["max_word_ratio"]:
            failures.append(f"word ratio exceeds {requirements['max_word_ratio']}")
    if requirements.get("requires_conflict_notice") and not output.startswith("Constraint conflict:"):
        failures.append("missing constraint conflict notice")
    if requirements.get("output_only"):
        opening = normalized(output[:120])
        if any(marker in opening for marker in EXPLANATION_MARKERS):
            failures.append("output includes an explanation marker")

    manual_checks = list(requirements.get("manual_checks", []))
    status = grade_status(failures, manual_checks)
    return Grade(status=status, failures=failures, manual_checks=manual_checks)


def load_activation_cases(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def load_behavior_cases(path: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"{path}:{line_number}: {error}") from error
    return cases


def duplicate_ids(cases: Iterable[dict[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for case in cases:
        case_id = case.get("id", "")
        if case_id in seen:
            duplicates.add(case_id)
        seen.add(case_id)
    return duplicates


def validate_corpus(plugin_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        activation = load_activation_cases(plugin_root / "evals" / "prompts.csv")
        behavior = load_behavior_cases(plugin_root / "evals" / "cases.jsonl")
    except (OSError, ValueError) as error:
        return {"activation_cases": 0, "behavior_cases": 0, "tags": [], "errors": [str(error)]}

    for duplicate in sorted(duplicate_ids([*activation, *behavior])):
        errors.append(f"duplicate case id: {duplicate}")
    for case in activation:
        if case.get("expected_skill") not in {"none", "prose", "compress", "laconic"}:
            errors.append(f"{case.get('id')}: invalid expected_skill")
        if case.get("invocation") not in {"natural", "slash"}:
            errors.append(f"{case.get('id')}: invalid invocation")
        if not case.get("prompt"):
            errors.append(f"{case.get('id')}: missing prompt")
    tags = {tag for case in behavior for tag in case.get("tags", [])}
    missing_tags = REQUIRED_TAGS - tags
    if missing_tags:
        errors.append(f"missing required behavior tags: {', '.join(sorted(missing_tags))}")
    for case in behavior:
        if case.get("skill") not in {"prose", "compress", "laconic"}:
            errors.append(f"{case.get('id')}: invalid skill")
        if not case.get("prompt") or "input" not in case or "requirements" not in case:
            errors.append(f"{case.get('id')}: behavior case is incomplete")

    return {
        "activation_cases": len(activation),
        "behavior_cases": len(behavior),
        "tags": sorted(tags),
        "errors": errors,
    }


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def extract_invoked_skills(events: Iterable[dict[str, Any]]) -> list[str]:
    skills: list[str] = []
    for event in events:
        for item in walk(event):
            if item.get("name") == "Skill" and isinstance(item.get("input"), dict):
                skill = item["input"].get("skill")
                if isinstance(skill, str) and skill not in skills:
                    skills.append(skill)
    return skills


def extract_available_commands(events: Iterable[dict[str, Any]]) -> list[str]:
    commands: list[str] = []
    for event in events:
        if event.get("type") != "system" or event.get("subtype") != "init":
            continue
        for command in event.get("slash_commands", []):
            if isinstance(command, str) and command not in commands:
                commands.append(command)
    return commands


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "result"


def plugin_metadata(plugin_root: Path) -> dict[str, str]:
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{manifest_path}: missing plugin version")

    digest = hashlib.sha256()
    files = sorted(
        path
        for path in plugin_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    )
    for path in files:
        relative = path.relative_to(plugin_root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return {"plugin_version": version, "plugin_hash": digest.hexdigest()}


def create_run_directory(
    output_dir: Path,
    metadata: dict[str, str],
    started_at: datetime | None = None,
) -> tuple[Path, str]:
    started = started_at or datetime.now(timezone.utc)
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    timestamp = started.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    version = safe_name(metadata["plugin_version"])
    run_id = f"{timestamp}--v{version}--{metadata['plugin_hash'][:12]}"
    path = output_dir / run_id
    path.mkdir(parents=True, exist_ok=False)
    return path, run_id


def write_result(output_dir: Path, result: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = "--".join(
        safe_name(str(result.get(field, "")))
        for field in ("id", "model", "arm")
        if result.get(field)
    )
    path = output_dir / f"{name}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def parse_stream(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def result_text(events: Iterable[dict[str, Any]]) -> str:
    for event in reversed(list(events)):
        if event.get("type") == "result" and isinstance(event.get("result"), str):
            return event["result"]
    return ""


def run_claude(
    claude_bin: str,
    prompt: str,
    model: str,
    plugin_root: Path | None,
    max_budget_usd: float | None,
) -> dict[str, Any]:
    command = [
        claude_bin,
        "-p",
        "--model",
        model,
        "--output-format",
        "stream-json",
        "--verbose",
        "--no-session-persistence",
        "--setting-sources",
        "",
    ]
    if plugin_root is None:
        command.append("--safe-mode")
    else:
        command.extend(["--plugin-dir", str(plugin_root)])
    if max_budget_usd is not None:
        command.extend(["--max-budget-usd", str(max_budget_usd)])
    command.append(prompt)
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    events = parse_stream(completed.stdout)
    return {
        "command": command[:-1] + ["<prompt>"],
        "returncode": completed.returncode,
        "stderr": completed.stderr,
        "events": events,
        "output": result_text(events),
        "invoked_skills": extract_invoked_skills(events),
        "available_commands": extract_available_commands(events),
    }


def surface_version(claude_bin: str) -> str:
    completed = subprocess.run([claude_bin, "--version"], text=True, capture_output=True, check=False)
    return completed.stdout.strip() or completed.stderr.strip() or "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-root", type=Path, default=DEFAULT_PLUGIN_ROOT)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--model", action="append", default=[])
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--output-dir", type=Path, default=Path("eval-results"))
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--include-baseline", action="store_true")
    parser.add_argument("--max-budget-usd", type=float)
    return parser


def activation_status(
    case: dict[str, str], invoked: list[str], available_commands: list[str]
) -> str:
    expected = case["expected_skill"]
    plugin_skills = {skill for skill in invoked if skill.startswith("prose:")}
    if expected == "none":
        return "pass" if not plugin_skills else "fail"

    qualified = f"prose:{expected}"
    unexpected = plugin_skills - {qualified}
    if unexpected:
        return "fail"
    if qualified in plugin_skills:
        return "pass"
    slash_prompt = case["prompt"].lstrip().startswith(f"/{qualified}")
    if case["invocation"] == "slash" and slash_prompt and qualified in available_commands:
        return "pass"
    return "fail"


def grade_behavior_run(case: dict[str, Any], run: dict[str, Any]) -> Grade:
    grade = grade_output(case, run["output"])
    qualified = f"prose:{case['skill']}"
    invoked = set(run["invoked_skills"])
    available = set(run["available_commands"])
    is_slash = case["prompt"].lstrip().startswith(f"/{qualified}")
    has_evidence = qualified in invoked or (is_slash and qualified in available)
    unexpected = {skill for skill in invoked if skill.startswith("prose:")} - {qualified}

    failures = list(grade.failures)
    if not has_evidence:
        failures.append(f"missing runtime evidence for {qualified}")
    if unexpected:
        failures.append(f"unexpected prose skills invoked: {', '.join(sorted(unexpected))}")
    status = grade_status(failures, grade.manual_checks)
    return Grade(status=status, failures=failures, manual_checks=grade.manual_checks)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    validation = validate_corpus(args.plugin_root)
    if args.validate_only or validation["errors"]:
        print(json.dumps(validation, indent=2, ensure_ascii=False))
        return 1 if validation["errors"] else 0

    activation = load_activation_cases(args.plugin_root / "evals" / "prompts.csv")
    behavior = load_behavior_cases(args.plugin_root / "evals" / "cases.jsonl")
    selected = set(args.case)
    all_ids = {case["id"] for case in [*activation, *behavior]}
    unknown_ids = selected - all_ids
    if unknown_ids:
        print(f"unknown case id: {', '.join(sorted(unknown_ids))}", file=sys.stderr)
        return 2
    models = list(dict.fromkeys(args.model or ["sonnet"]))
    version = surface_version(args.claude_bin)
    try:
        metadata = plugin_metadata(args.plugin_root)
        run_dir, run_id = create_run_directory(args.output_dir, metadata)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"cannot prepare evaluation run: {error}", file=sys.stderr)
        return 2
    totals = {"pass": 0, "manual": 0, "fail": 0, "error": 0}
    result_metadata = {**metadata, "run_id": run_id}

    for model in models:
        for case in activation:
            if selected and case["id"] not in selected:
                continue
            run = run_claude(args.claude_bin, case["prompt"], model, args.plugin_root, args.max_budget_usd)
            status = (
                "error"
                if run["returncode"]
                else activation_status(case, run["invoked_skills"], run["available_commands"])
            )
            totals[status] += 1
            write_result(
                run_dir,
                {
                    **result_metadata,
                    "id": case["id"],
                    "kind": "activation",
                    "arm": "plugin",
                    "model": model,
                    "surface_version": version,
                    "expected_skill": case["expected_skill"],
                    "status": status,
                    **run,
                },
            )
        for case in behavior:
            if selected and case["id"] not in selected:
                continue
            prompt = f"{case['prompt']}\n\n{case['input']}"
            run = run_claude(args.claude_bin, prompt, model, args.plugin_root, args.max_budget_usd)
            grade = grade_behavior_run(case, run) if not run["returncode"] else Grade("fail", [], [])
            status = "error" if run["returncode"] else grade.status
            totals[status] += 1
            write_result(
                run_dir,
                {
                    **result_metadata,
                    "id": case["id"],
                    "kind": "behavior",
                    "arm": "plugin",
                    "model": model,
                    "surface_version": version,
                    "grade": asdict(grade),
                    "status": status,
                    **run,
                },
            )
            if args.include_baseline:
                baseline = run_claude(args.claude_bin, prompt, model, None, args.max_budget_usd)
                baseline_grade = (
                    grade_output(case, baseline["output"])
                    if not baseline["returncode"]
                    else Grade("fail", [], [])
                )
                write_result(
                    run_dir,
                    {
                        **result_metadata,
                        "id": case["id"],
                        "kind": "behavior",
                        "arm": "baseline",
                        "model": model,
                        "surface_version": version,
                        "grade": asdict(baseline_grade),
                        "status": "error" if baseline["returncode"] else baseline_grade.status,
                        **baseline,
                    },
                )

    summary = {
        "surface_version": version,
        "models": models,
        **result_metadata,
        "run_directory": str(run_dir),
        "totals": totals,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if totals["fail"] or totals["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
