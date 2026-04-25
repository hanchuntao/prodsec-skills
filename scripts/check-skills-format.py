#!/usr/bin/env python3
"""Validate YAML front matter for all skill files under skills/.

Checks every .md file (excluding README.md) for:
  - YAML front matter present (--- delimiters)
  - Required field: name (non-empty)
  - Required field: description (non-empty)
  - name value matches the file stem (e.g. my-skill.md → name: my-skill)
"""

import sys
from pathlib import Path

SKILLS_DIR = Path("skills")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return scalar front matter fields, or None if absent/malformed.

    Handles plain scalars and YAML block scalars (> and |).
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    lines = text[4:end].splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, raw = line.partition(":")
            value = raw.strip()
            if value in (">", "|", ">-", "|-"):
                parts: list[str] = []
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    parts.append(lines[i].strip())
                    i += 1
                fields[key.strip()] = " ".join(parts)
                continue
            fields[key.strip()] = value.strip('"').strip("'")
        i += 1
    return fields


def check(path: Path) -> list[str]:
    """Return a list of error strings for the given skill file."""
    if path.name == "README.md":
        return []

    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm is None:
        return [f"{path}: missing or malformed YAML front matter"]

    name_val = fm.get("name", "")
    desc_val = fm.get("description", "")

    if "name" not in fm or not name_val:
        errors.append(f"{path}: missing or empty required field 'name'")
    elif name_val != path.stem:
        errors.append(
            f"{path}: name mismatch — front matter 'name: {name_val}'"
            f" but filename stem is '{path.stem}'"
        )

    if "description" not in fm or not desc_val:
        errors.append(f"{path}: missing or empty required field 'description'")

    return errors


def collect(root: Path) -> list[Path]:
    """Return all skill .md files under root, excluding README.md files."""
    return sorted(p for p in root.rglob("*.md") if p.name != "README.md")


def main() -> None:
    paths = collect(SKILLS_DIR)
    if not paths:
        print(f"No skill files found under {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    all_errors: list[str] = []
    for path in paths:
        all_errors.extend(check(path))

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} error(s) in skill format checks.", file=sys.stderr)
        sys.exit(1)

    print(f"All {len(paths)} skill files pass format checks.")


if __name__ == "__main__":
    main()
