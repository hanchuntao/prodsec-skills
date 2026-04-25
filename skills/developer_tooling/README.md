# Developer Tooling skills

4 general-purpose development skills — devcontainers, git cleanup, modern Python tooling, and property-based testing.

## Usage

Reference any skill by path in your assistant prompt:

```
Using `skills/developer_tooling/tooling/devcontainer-setup.md`: add Dev Container support to this project.
```

```
Using `skills/developer_tooling/testing/property-based-testing.md`: write property-based tests for this parser.
```

Skills follow the same format as the rest of `skills/` — YAML front matter (`name`, `description`) plus markdown body. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Testing — 1 skill

| Skill | Focus |
|-------|-------|
| [`property-based-testing.md`](testing/property-based-testing.md) | Property-based testing with Hypothesis (Python), proptest (Rust), and others |

### Tooling — 3 skills

| Skill | Focus |
|-------|-------|
| [`devcontainer-setup.md`](tooling/devcontainer-setup.md) | Adding Dev Container support with language-specific tooling and persistent volumes |
| [`git-cleanup.md`](tooling/git-cleanup.md) | Safely analyzing and cleaning up merged, squash-merged, and stale branches |
| [`modern-python.md`](tooling/modern-python.md) | Configuring Python projects with uv, ruff, and ty |

## Provenance

- **Source**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
