# Skill Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `scripts/check-skills-format.py` validator that enforces required YAML frontmatter on all skill files, wired into `make lint`, CI, and pre-commit hooks.

**Architecture:** A standalone Python 3 script modelled after `scripts/check-adr-format.py` — no external dependencies, uses only stdlib (`pathlib`, `sys`, `re`). It walks `skills/` recursively, skips `README.md` files, and checks each `.md` file for valid frontmatter with non-empty `name` and `description` fields whose `name` matches the filename stem. Tests use `pytest` with temporary files.

**Tech Stack:** Python 3.13, pytest, stdlib only (pathlib, sys, re)

---

## File Map

| Action | Path | Purpose |
|--------|------|---------|
| Create | `scripts/check-skills-format.py` | Validator script |
| Create | `tests/test_check_skills_format.py` | Pytest unit tests |
| Modify | `Makefile` | Add `check-skills` target, wire into `lint` |
| Modify | `.pre-commit-config.yaml` | Add local hook |

---

## Task 1: Write failing tests

**Files:**
- Create: `tests/test_check_skills_format.py`

- [ ] **Step 1: Create the test file**

```python
"""Tests for scripts/check-skills-format.py."""

import importlib.util
import sys
from pathlib import Path

import pytest


def load_module():
    spec = importlib.util.spec_from_file_location(
        "check_skills_format",
        Path(__file__).parent.parent / "scripts" / "check-skills-format.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def mod():
    return load_module()


def skill(tmp_path: Path, name: str, content: str) -> Path:
    """Write a skill file and return its path."""
    p = tmp_path / f"{name}.md"
    p.write_text(content)
    return p


def test_valid_skill(mod, tmp_path):
    p = skill(tmp_path, "my-skill", "---\nname: my-skill\ndescription: Does something useful.\n---\n\n# Body\n")
    assert mod.check(p) == []


def test_valid_skill_multiline_description(mod, tmp_path):
    content = "---\nname: my-skill\ndescription: >\n  Does something useful\n  across two lines.\n---\n\n# Body\n"
    p = skill(tmp_path, "my-skill", content)
    assert mod.check(p) == []


def test_missing_frontmatter(mod, tmp_path):
    p = skill(tmp_path, "bad-skill", "# No frontmatter here\n")
    errors = mod.check(p)
    assert any("frontmatter" in e.lower() for e in errors)


def test_missing_name_field(mod, tmp_path):
    p = skill(tmp_path, "bad-skill", "---\ndescription: Something.\n---\n")
    errors = mod.check(p)
    assert any("name" in e for e in errors)


def test_missing_description_field(mod, tmp_path):
    p = skill(tmp_path, "bad-skill", "---\nname: bad-skill\n---\n")
    errors = mod.check(p)
    assert any("description" in e for e in errors)


def test_empty_name(mod, tmp_path):
    p = skill(tmp_path, "bad-skill", "---\nname:\ndescription: Something.\n---\n")
    errors = mod.check(p)
    assert any("name" in e for e in errors)


def test_empty_description(mod, tmp_path):
    p = skill(tmp_path, "bad-skill", "---\nname: bad-skill\ndescription:\n---\n")
    errors = mod.check(p)
    assert any("description" in e for e in errors)


def test_name_mismatch(mod, tmp_path):
    p = skill(tmp_path, "actual-name", "---\nname: wrong-name\ndescription: Something.\n---\n")
    errors = mod.check(p)
    assert any("mismatch" in e.lower() or "name" in e for e in errors)


def test_readme_skipped(mod, tmp_path):
    p = tmp_path / "README.md"
    p.write_text("# Index\nNo frontmatter needed.\n")
    # README.md files are not passed to check() — validate collect() excludes them
    assert mod.check(p) == []  # check() on a README returns no errors (name matches stem fails gracefully)


def test_collect_excludes_readmes(mod, tmp_path):
    (tmp_path / "README.md").write_text("# Index\n")
    skill_file = tmp_path / "my-skill.md"
    skill_file.write_text("---\nname: my-skill\ndescription: Useful.\n---\n")
    collected = mod.collect(tmp_path)
    assert skill_file in collected
    assert tmp_path / "README.md" not in collected
```

- [ ] **Step 2: Run tests to confirm they all fail**

```bash
cd /path/to/repo
uv run pytest tests/test_check_skills_format.py -v 2>&1 | head -30
```

Expected: `ModuleNotFoundError` or `FileNotFoundError` — script doesn't exist yet.

---

## Task 2: Implement the validator script

**Files:**
- Create: `scripts/check-skills-format.py`

- [ ] **Step 3: Create the script**

```python
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
                # Collect indented continuation lines
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
    # README.md files are index files, not skills — skip silently
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
            f"{path}: name mismatch — front matter 'name: {name_val}' but filename stem is '{path.stem}'"
        )

    if "description" not in fm or not desc_val:
        errors.append(f"{path}: missing or empty required field 'description'")

    return errors


def collect(root: Path) -> list[Path]:
    """Return all skill .md files under root, excluding README.md files."""
    return sorted(
        p for p in root.rglob("*.md") if p.name != "README.md"
    )


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
```

- [ ] **Step 4: Run the tests**

```bash
uv run pytest tests/test_check_skills_format.py -v
```

Expected: all 10 tests pass.

- [ ] **Step 5: Smoke-test against real skills**

```bash
uv run python scripts/check-skills-format.py
```

Expected: `All 111 skill files pass format checks.` (count may vary).

---

## Task 3: Wire into Makefile

**Files:**
- Modify: `Makefile`

- [ ] **Step 6: Add `check-skills` target and update `lint` and `help`**

In `Makefile`, make these three edits:

1. Add `check-skills` to the `.PHONY` line:
```makefile
.PHONY: help bootstrap lint check check-adrs check-skills fmt
```

2. Add to the `help` target echo block:
```makefile
	@echo "  check-skills         - Validate skill YAML front matter"
```

3. Add the target:
```makefile
check-skills:
	uv run python scripts/check-skills-format.py
```

4. Update `lint` to include it:
```makefile
lint: check check-adrs check-skills
```

- [ ] **Step 7: Verify lint runs all three checks**

```bash
make lint
```

Expected: ruff check, ADR validation, and skill validation all pass with no errors.

---

## Task 4: Add pre-commit hook

**Files:**
- Modify: `.pre-commit-config.yaml`

- [ ] **Step 8: Add the skill validation hook**

Append to the `local` repo hooks in `.pre-commit-config.yaml`:

```yaml
      - id: check-skills
        name: Validate skill front matter
        language: python
        entry: uv run python scripts/check-skills-format.py
        pass_filenames: false
        files: ^skills/.*\.md$
```

Full file after edit:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.9
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: local
    hooks:
      - id: check-adrs
        name: Validate ADR format
        language: python
        entry: uv run python scripts/check-adr-format.py
        pass_filenames: false
        files: ^docs/ADRs/

      - id: check-skills
        name: Validate skill front matter
        language: python
        entry: uv run python scripts/check-skills-format.py
        pass_filenames: false
        files: ^skills/.*\.md$
```

- [ ] **Step 9: Verify pre-commit runs the hook**

```bash
pre-commit run check-skills --all-files
```

Expected: `Validate skill front matter.....Passed`
