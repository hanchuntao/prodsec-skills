# Security Skills

Security skills for AI coding assistants and agentic systems. Skills encode security recommendations, guidelines, and best practices as structured markdown files that AI assistants (Claude Code, Cursor, Copilot, and others) consume directly while writing, testing, and auditing code.

The goal is to shift security left: apply security guidance during development, not after review.

## Get started

```bash
make bootstrap
```

Installs ruff, ty, pre-commit, and wires up git hooks so linting and ADR validation run automatically before each commit. Requires [`uv`](https://docs.astral.sh/uv/) on your PATH.

## Using a skill

Reference any skill by path in your assistant prompt:

```
Using `skills/secure_development/mcp-server/input-output-sanitization.md`: review this MCP server for injection risks.
```

```
Using `skills/security_testing/fuzzing/cargo-fuzz.md`: write a fuzzing harness for this parser.
```

```
Using `skills/security_auditing/audit-workflow/differential-review.md`: review the security impact of this diff.
```

Skills are tool-agnostic — the same file works in any assistant that can read files.

## Skill catalog

128 skills across four categories. See [`skills/README.md`](skills/README.md) for the full index.

| Category | Skills | Purpose |
|----------|--------|---------|
| [`skills/secure_development/`](skills/secure_development/README.md) | 103 | Building secure software — AI/agentic infrastructure, cryptography, supply chain, security principles, technology-specific hardening |
| [`skills/security_testing/`](skills/README.md#security_testing) | 17 | Finding vulnerabilities — fuzzing and static analysis |
| [`skills/security_auditing/`](skills/README.md#security_auditing) | 4 | Security review workflows |
| [`skills/developer_tooling/`](skills/README.md#developer_tooling) | 4 | General-purpose development tooling |

## Repository layout

```
skills/                  # Production-ready curated skills
  secure_development/
  security_testing/
  security_auditing/
  developer_tooling/
experimental/            # Work in progress; contributions welcome
docs/                    # Design notes and project docs
  glossary.md            # Security terminology
  ADRs/                  # Architecture decision records
AGENTS.md                # Context for AI agents working in this repo
CONTRIBUTING.md          # Contribution guidelines
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full details. The short version:

1. New or experimental skills go in `experimental/` first.
2. Skills must use the standard front matter format:
   ```markdown
   ---
   name: skill-name
   description: Precise one-line trigger condition for the skill.
   ---
   ```
3. Skills must be tool-agnostic — no assistant-specific syntax or config.
4. When adapting skills from upstream sources, record the source commit and license in the relevant category `README.md`. Trail of Bits skills are CC BY-SA 4.0; adaptations carry the same license.

### Updating indexes when adding a skill

Every new skill file requires updates to **four index files** — do this in the same commit as the skill itself:

| File | What to update |
|------|----------------|
| `skills/<category>/README.md` | Add the skill to its subcategory table; increment the subcategory skill count |
| `skills/README.md` | Increment the category count and the total count in the header; update the subcategory row if the subcategory is listed |
| `README.md` (this file) | Increment the category count and the "N skills across four categories" total |
| `AGENTS.md` | Increment the `skills/<category>/` count in the Repository layout table |

For architecture decisions and conventions, see [`AGENTS.md`](AGENTS.md).

## License

This project is licensed under the Apache License 2.0 — see [`LICENSE`](LICENSE) for details.

**Some skills are adapted from third-party sources under their own licenses:**

| Source | License | Skills | Details |
|--------|---------|--------|---------|
| [Trail of Bits Skills Marketplace](https://github.com/trailofbits/skills) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) | 32 skills (fuzzing, static analysis, audit workflows, developer tooling, and select crypto/config/supply-chain skills) | ShareAlike — adaptations must use the same license |
| [CoSAI Project CodeGuard](https://github.com/cosai-oasis/project-codeguard) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | 8 skills (web security, C/C++ safety, algorithm selection, build YAML) | Attribution required |

Each affected skill file has `license` and `origin` fields in its YAML front matter. See [`NOTICE`](NOTICE) for the complete list and [`skills/secure_development/README.md`](skills/secure_development/README.md) for full provenance.
