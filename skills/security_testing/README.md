# Security Testing skills

17 skills for finding vulnerabilities through automated testing — coverage-guided fuzzing and static analysis.

## Usage

Reference any skill by path in your assistant prompt:

```
Using `skills/security_testing/fuzzing/cargo-fuzz.md`: write a fuzzing harness for this parser.
```

```
Using `skills/security_testing/static-analysis/semgrep.md`: scan this codebase for vulnerabilities.
```

Skills follow the same format as the rest of `skills/` — YAML front matter (`name`, `description`) plus markdown body. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

## Categories

### Fuzzing — 12 skills

| Skill | Focus |
|-------|-------|
| [`address-sanitizer.md`](fuzzing/address-sanitizer.md) | Detect memory errors (buffer overflows, use-after-free) during C/C++ fuzzing with ASan |
| [`aflpp.md`](fuzzing/aflpp.md) | Multi-core coverage-guided fuzzing of C/C++ with AFL++ |
| [`atheris.md`](fuzzing/atheris.md) | Coverage-guided fuzzing of pure Python and Python C extensions |
| [`cargo-fuzz.md`](fuzzing/cargo-fuzz.md) | Fuzzing Rust projects with cargo-fuzz and a libFuzzer backend |
| [`coverage-analysis.md`](fuzzing/coverage-analysis.md) | Measuring code coverage to assess harness effectiveness and identify blockers |
| [`fuzzing-dictionary.md`](fuzzing/fuzzing-dictionary.md) | Building domain-specific token dictionaries for parsers, protocols, and formats |
| [`fuzzing-obstacles.md`](fuzzing/fuzzing-obstacles.md) | Patching checksums, global state, and other barriers to fuzzer progress |
| [`harness-writing.md`](fuzzing/harness-writing.md) | Writing effective fuzz targets across languages |
| [`libafl.md`](fuzzing/libafl.md) | Building custom fuzzers with LibAFL's modular fuzzing library |
| [`libfuzzer.md`](fuzzing/libfuzzer.md) | Coverage-guided fuzzing of C/C++ code compiled with Clang |
| [`ossfuzz.md`](fuzzing/ossfuzz.md) | Enrolling open source projects in OSS-Fuzz for continuous fuzzing |
| [`ruzzy.md`](fuzzing/ruzzy.md) | Coverage-guided fuzzing of Ruby code and Ruby C extensions |

### Static analysis — 5 skills

| Skill | Focus |
|-------|-------|
| [`codeql.md`](static-analysis/codeql.md) | Interprocedural data flow and taint tracking analysis with CodeQL |
| [`sarif-parsing.md`](static-analysis/sarif-parsing.md) | Parsing, filtering, and deduplicating SARIF output from any scanner |
| [`semgrep.md`](static-analysis/semgrep.md) | Running Semgrep across a codebase with parallel subagents |
| [`semgrep-rule-creator.md`](static-analysis/semgrep-rule-creator.md) | Writing custom Semgrep rules for security vulnerabilities and bug patterns |
| [`semgrep-rule-variant-creator.md`](static-analysis/semgrep-rule-variant-creator.md) | Porting existing Semgrep rules to new target languages |

## Provenance

- **Fuzzing skills**: Adapted from Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)). Upstream commit: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07). License: CC BY-SA 4.0.
- **Static analysis skills**: Adapted from Trail of Bits Skills Marketplace. Same upstream commit and license. Curated versions inline reference docs and drop tool-specific artifacts (plugin.json, hooks, scripts).
