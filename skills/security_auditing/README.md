# Security Auditing skills

4 skills for security review workflows — structured approaches to code auditing, differential review, false-positive verification, and variant analysis.

## Usage

Reference any skill by path in your assistant prompt:

```
Using `skills/security_auditing/audit-workflow/differential-review.md`: review the security impact of this diff.
```

```
Using `skills/security_auditing/audit-workflow/variant-analysis.md`: find related vulnerabilities after this initial finding.
```

Skills follow the same format as the rest of `skills/` — YAML front matter (`name`, `description`) plus markdown body. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Audit workflow — 4 skills

| Skill | Focus |
|-------|-------|
| [`audit-context-building.md`](audit-workflow/audit-context-building.md) | Line-by-line codebase analysis to build deep architectural context before a security review |
| [`differential-review.md`](audit-workflow/differential-review.md) | Security-focused review of PRs, commits, and diffs with blast radius analysis |
| [`fp-check.md`](audit-workflow/fp-check.md) | Systematic verification of suspected bugs to eliminate false positives |
| [`variant-analysis.md`](audit-workflow/variant-analysis.md) | Finding related vulnerabilities across a codebase after discovering an initial issue |

## Provenance

- **Source**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
