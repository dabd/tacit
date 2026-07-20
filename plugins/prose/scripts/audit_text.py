#!/usr/bin/env python3
"""Report measurable text properties without claiming semantic correctness."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Pattern


WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(.*?)\1", re.DOTALL)
SENTENCE_BOUNDARY_RE = re.compile(
    r"(?:(?<=[.!?])|(?<=[.!?][\"'”’)]))\s+(?=[A-Z0-9`\"'“‘(])"
)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "because", "been", "but", "by",
    "can", "for", "from", "has", "have", "if", "in", "is", "it", "of", "on",
    "or", "our", "so", "that", "the", "their", "then", "this", "to", "was",
    "we", "were", "will", "with", "you", "your",
}

# These patterns are smoke checks. The prose skill's general tests decide
# whether wording is appropriate in context.
DEFAULT_PATTERNS = [
    r"\bit(?:'s| is) worth noting\b",
    r"\bthe key takeaway\b",
    r"\bat the end of the day\b",
    r"\bload-bearing (?:insight|idea|point|argument|reason)\b",
    r"\bunlock(?:s|ed|ing)? (?:value|potential|a path|opportunities)\b",
    r"\bland(?:s|ed|ing)? (?:the point|the message|the argument)\b",
    r"\bship(?:s|ped|ping)? (?:a decision|the decision|the narrative|the message)\b",
]


@dataclass
class Audit:
    words: int
    sentences: int
    paragraphs: int
    sections: int
    duplicate_sentences: list[list[int]]
    near_duplicate_paragraphs: list[dict]
    repeated_openings: list[dict]
    flagged_patterns: list[dict]
    failures: list[str]


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def normalize_unicode(text: str) -> str:
    return text.translate(
        str.maketrans(
            {
                "\u2018": "'",
                "\u2019": "'",
                "\u201c": '"',
                "\u201d": '"',
                "\u2011": "-",
                "\u2013": "-",
                "\u2014": "-",
            }
        )
    )


def without_fenced_code(text: str) -> str:
    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in text.splitlines():
        match = FENCE_RE.match(line)
        marker = match.group(1) if match else None
        if fence_character is None and marker:
            fence_character = marker[0]
            fence_length = len(marker)
            output.append("")
            continue
        if fence_character is not None:
            stripped = line.lstrip()
            if stripped.startswith(fence_character * fence_length):
                fence_character = None
                fence_length = 0
            output.append("")
            continue
        output.append(line)

    return "\n".join(output)


def without_inline_code(text: str) -> str:
    return INLINE_CODE_RE.sub(" ", text)


def visible_paragraphs(text: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", without_fenced_code(text))
    paragraphs: list[str] = []
    for block in blocks:
        lines: list[str] = []
        for line in block.splitlines():
            stripped = line.strip()
            if not stripped or HEADING_RE.fullmatch(stripped):
                continue
            if re.fullmatch(r"(?:[-*_]\s*){3,}", stripped):
                continue
            stripped = re.sub(r"^>\s?", "", stripped)
            stripped = re.sub(r"^(?:[-+*]|\d+[.)])\s+", "", stripped)
            lines.append(stripped)
        paragraph = " ".join(lines).strip()
        if paragraph:
            paragraphs.append(paragraph)
    return paragraphs


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_BOUNDARY_RE.split(text) if part.strip()]


def all_sentences(paragraphs: Iterable[str]) -> list[str]:
    return [sentence for paragraph in paragraphs for sentence in split_sentences(paragraph)]


def normalize_exact(text: str) -> str:
    return " ".join(normalize_unicode(text).split())


def token_set(text: str) -> set[str]:
    return {
        token.lower()
        for token in words(normalize_unicode(text))
        if token.lower() not in STOPWORDS and len(token) > 2
    }


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def duplicate_sentence_groups(sentences: list[str]) -> list[list[int]]:
    indexes: dict[str, list[int]] = {}
    for index, sentence in enumerate(sentences, start=1):
        key = normalize_exact(sentence)
        if key:
            indexes.setdefault(key, []).append(index)
    return [group for group in indexes.values() if len(group) > 1]


def near_duplicate_paragraphs(paragraphs: list[str], threshold: float) -> list[dict]:
    result: list[dict] = []
    sets = [token_set(paragraph) for paragraph in paragraphs]
    for left_index in range(len(paragraphs)):
        for right_index in range(left_index + 1, len(paragraphs)):
            score = jaccard(sets[left_index], sets[right_index])
            if score >= threshold and min(len(sets[left_index]), len(sets[right_index])) >= 4:
                result.append(
                    {
                        "paragraphs": [left_index + 1, right_index + 1],
                        "similarity": round(score, 3),
                    }
                )
    return result


def repeated_openings(sentences: list[str], size: int = 2) -> list[dict]:
    openings: dict[str, list[int]] = {}
    for index, sentence in enumerate(sentences, start=1):
        tokens = [token.lower() for token in words(sentence)]
        if len(tokens) >= size:
            opening = " ".join(tokens[:size])
            openings.setdefault(opening, []).append(index)
    return [
        {"opening": opening, "sentences": indexes}
        for opening, indexes in openings.items()
        if len(indexes) >= 3
    ]


def compile_patterns(patterns: Iterable[str]) -> list[Pattern[str]]:
    compiled: list[Pattern[str]] = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern, flags=re.IGNORECASE))
        except re.error as error:
            raise ValueError(f"invalid regular expression {pattern!r}: {error}") from error
    return compiled


def flagged_patterns(text: str, patterns: Iterable[Pattern[str]]) -> list[dict]:
    searchable = normalize_unicode(without_inline_code(without_fenced_code(text)))
    found: list[dict] = []
    for pattern in patterns:
        matches = [match.group(0) for match in pattern.finditer(searchable)]
        if matches:
            found.append({"pattern": pattern.pattern, "matches": matches})
    return found


def audit(text: str, args: argparse.Namespace) -> Audit:
    fence_free = without_fenced_code(text)
    paragraphs = visible_paragraphs(text)
    sentences = all_sentences(paragraphs)
    patterns = compile_patterns([*DEFAULT_PATTERNS, *(args.flag_pattern or [])])

    result = Audit(
        words=len(words(fence_free)),
        sentences=len(sentences),
        paragraphs=len(paragraphs),
        sections=len(HEADING_RE.findall(fence_free)),
        duplicate_sentences=duplicate_sentence_groups(sentences),
        near_duplicate_paragraphs=near_duplicate_paragraphs(paragraphs, args.similarity),
        repeated_openings=repeated_openings(sentences),
        flagged_patterns=flagged_patterns(text, patterns),
        failures=[],
    )

    if args.max_words is not None and result.words > args.max_words:
        result.failures.append(f"word count {result.words} exceeds {args.max_words}")
    if args.max_sections is not None and result.sections > args.max_sections:
        result.failures.append(f"section count {result.sections} exceeds {args.max_sections}")
    if args.fail_duplicates and result.duplicate_sentences:
        result.failures.append("exact duplicate sentences found")
    if args.fail_near_duplicates and result.near_duplicate_paragraphs:
        result.failures.append("lexically similar paragraphs found")
    if args.fail_patterns and result.flagged_patterns:
        result.failures.append("flagged phrasing found")

    return result


def unit_interval(value: str) -> float:
    parsed = float(value)
    if not 0.0 <= parsed <= 1.0:
        raise argparse.ArgumentTypeError("similarity must be between 0 and 1")
    return parsed


def nonnegative_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be zero or greater")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="Text file. Reads stdin when omitted.")
    parser.add_argument("--max-words", type=nonnegative_integer)
    parser.add_argument("--max-sections", type=nonnegative_integer)
    parser.add_argument(
        "--similarity",
        type=unit_interval,
        default=0.78,
        help="Jaccard threshold for lexical paragraph similarity.",
    )
    parser.add_argument("--flag-pattern", action="append", help="Additional regular expression to flag.")
    parser.add_argument("--fail-duplicates", action="store_true")
    parser.add_argument("--fail-near-duplicates", action="store_true")
    parser.add_argument("--fail-patterns", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        source = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
        result = audit(source, args)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))

    payload = asdict(result)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"words: {result.words}")
        print(f"sentences: {result.sentences}")
        print(f"paragraphs: {result.paragraphs}")
        print(f"sections: {result.sections}")
        if result.duplicate_sentences:
            print(f"duplicate sentences: {result.duplicate_sentences}")
        if result.near_duplicate_paragraphs:
            print(f"lexically similar paragraphs: {result.near_duplicate_paragraphs}")
        if result.repeated_openings:
            print(f"repeated openings: {result.repeated_openings}")
        if result.flagged_patterns:
            print(f"flagged patterns: {result.flagged_patterns}")
        for failure in result.failures:
            print(f"FAIL: {failure}", file=sys.stderr)

    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
