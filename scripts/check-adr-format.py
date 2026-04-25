#!/usr/bin/env python3
"""Validate ADR format for all ADRs in docs/ADRs/ (excluding the template).

Checks:
  - Filename matches NNNN-description.md
  - ADR numbers are unique
  - YAML front matter present with required fields: title, status
  - status is a valid value
  - Date: YYYY-MM-DD line present in body
  - Required sections present: ## Status, ## Context, ## Decision, ## Consequences
  - Undecided ADRs have an ## Options section
  - Front matter status matches ## Status section body
"""

import re
import sys
from pathlib import Path

ADRS_DIR = Path("docs/ADRs")
VALID_STATUSES = {"Proposed", "Undecided", "Accepted", "Deprecated", "Superseded"}
REQUIRED_SECTIONS = {"## Status", "## Context", "## Decision", "## Consequences"}
FILENAME_RE = re.compile(r"^\d{4}-.+\.md$")
DATE_RE = re.compile(r"^Date: \d{4}-\d{2}-\d{2}$", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return scalar front matter fields, or None if front matter is absent/malformed."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, raw = line.partition(":")
            fields[key.strip()] = raw.split("#")[0].strip().strip('"')
    return fields


def body_status(text: str) -> str | None:
    """Return the first non-empty line after '## Status' in the body."""
    found = False
    for line in text.splitlines():
        if line == "## Status":
            found = True
            continue
        if found:
            if line.startswith("#"):
                break
            if line.strip():
                return line.strip().split()[0]
    return None


def check(path: Path, seen_numbers: set[str]) -> list[str]:
    errors: list[str] = []
    name = path.name

    if not FILENAME_RE.match(name):
        return [f"{name}: filename must match NNNN-description.md"]

    num = name[:4]
    if num in seen_numbers:
        errors.append(f"{name}: ADR number {num} is already used")
    seen_numbers.add(num)

    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm is None:
        errors.append(f"{name}: missing or malformed YAML front matter")
        return errors

    for field in ("title", "status"):
        if field not in fm:
            errors.append(f"{name}: missing required front matter field '{field}'")

    fm_status = fm.get("status", "")
    if fm_status and fm_status not in VALID_STATUSES:
        errors.append(
            f"{name}: invalid status '{fm_status}' (valid: {', '.join(sorted(VALID_STATUSES))})"
        )

    if not DATE_RE.search(text):
        errors.append(f"{name}: missing or malformed 'Date: YYYY-MM-DD' line")

    lines = set(text.splitlines())
    for section in REQUIRED_SECTIONS:
        if section not in lines:
            errors.append(f"{name}: missing required section '{section}'")

    if fm_status == "Undecided" and "## Options" not in lines:
        errors.append(f"{name}: Undecided ADR must have '## Options' section")

    bs = body_status(text)
    if bs and fm_status and bs != fm_status:
        errors.append(
            f"{name}: status mismatch — front matter '{fm_status}' vs body '{bs}'"
        )

    return errors


def main() -> None:
    paths = sorted(p for p in ADRS_DIR.glob("*.md") if p.name != "0000-adr-template.md")
    if not paths:
        print(f"No ADR files found in {ADRS_DIR}", file=sys.stderr)
        sys.exit(1)

    seen_numbers: set[str] = set()
    all_errors: list[str] = []
    for path in paths:
        all_errors.extend(check(path, seen_numbers))

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) in ADR format checks.", file=sys.stderr)
        sys.exit(1)

    print(f"All {len(paths)} ADRs pass format checks.")


if __name__ == "__main__":
    main()
