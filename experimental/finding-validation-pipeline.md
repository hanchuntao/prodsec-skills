---
name: finding-validation-pipeline
description: >
  Validate security findings for accuracy, novelty, exploitability, and correct
  severity before escalating to humans. Use after discovering vulnerabilities
  during penetration testing, fuzzing, or security audits to minimize noise and
  ensure every finding that reaches a human is real, novel, and actionable.
---

# Finding Validation Pipeline

## Overview

This skill provides a multi-stage validation pipeline for security findings. The goal is to minimize noise: every finding that reaches a human reviewer should be real, novel, correctly classified, and actionable.

Stages are ordered cheapest-first. Each stage can **short-circuit** the pipeline — if a finding is already a known CVE with a patch, or clearly intended behavior, skip the expensive reproduction and exploitability stages.

## Validation Card

For each finding, produce a validation card:

```markdown
## Validation

| Check                | Result       | Evidence |
|----------------------|--------------|----------|
| Reproduced           | YES/NO/PARTIAL | ... |
| Known CVE            | YES/NO/NEEDS CHECK | ... |
| Upstream aware       | YES/NO/UNKNOWN | ... |
| Intended behavior    | YES/NO/GRAY AREA | ... |
| Exploitable          | YES/NO/PARTIAL | ... |
| Severity correct     | YES/OVER/UNDER | ... |
| **Confidence**       | **HIGH/MEDIUM/LOW** | ... |
| **Action**           | **ESCALATE/INVESTIGATE/CLOSE** | ... |

### Validation Notes
...
```

## Pre-Filter — Informational Findings

Before entering the pipeline, check each finding's severity:

- **Informational AND architecture/design analysis** (not a code bug): Skip Stages 1-6. Mark as ESCALATE (as architecture reference) with HIGH confidence.
- **Informational AND code-level issue** (e.g., dead code, minor quality bug): Run Stages 1-2 only. Skip Stages 3-6.

---

## Stage 1 — CVE and Advisory Search (CHEAPEST — do first)

Search for whether this vulnerability is already known:

1. **NVD/CVE search**: Query NVD, cve.org, and osv.dev for the software and vulnerability class.
2. **Project security advisories**: Check the project's security page for matching advisories.
3. **oss-security mailing list**: Search openwall.com/lists/oss-security for the software and vulnerability class.
4. **Academic literature**: For novel attack classes (timing side channels, padding oracles), search for recent papers describing this exact finding.
5. **Bug bounty platforms**: Search HackerOne or similar for related disclosed reports.

**Classification**:
- **Known CVE with patch**: Duplicate — check if the target runs a patched version
- **Known CVE, unpatched**: Valid — the target runs a vulnerable version
- **Known class, no specific CVE**: May be novel — needs deeper investigation
- **No matches**: Potentially novel — higher priority

**Short-circuit**: If exact CVE match with patch applied to target version → **CLOSE** as duplicate. Skip remaining stages.

---

## Stage 2 — Upstream Context

Determine whether the project is aware of this behavior:

1. **Issue tracker search**: Search the project's issue tracker for the vulnerability class.
2. **Documentation review**: Check if the project's docs mention this behavior as intended, deprecated, or known-risky.
3. **Changelog review**: Search recent changelogs for related fixes or deliberate changes.
4. **Security policy**: Read `SECURITY.md` or equivalent to understand what the project considers in-scope.

**Short-circuit**: If upstream has explicitly documented this as intended behavior or won't-fix → **CLOSE**. Skip remaining stages.

---

## Stage 3 — Intent vs. Bug Classification

Determine whether the behavior is intentional:

1. **Internal consistency**: Does the software protect against this class elsewhere? Inconsistency suggests oversight, not intent.
2. **Peer comparison**: Do 2-3 peer implementations protect against it? If all peers block it, the finding is stronger.
3. **Distribution customization**: Is the finding in upstream code or distro patches/config? Distros may intentionally weaken or strengthen settings.
4. **Opt-in/opt-out mechanism**: If the behavior requires a flag like `--insecure` or `@SECLEVEL=0`, it's more likely intended. If it's the default with no opt-out, it's more concerning.

**Short-circuit**: If clearly intended behavior (e.g., explicit opt-in flag required) → **CLOSE**. Skip remaining stages.

---

## Stage 4 — Reproduction (EXPENSIVE — only if survived Stages 1-3)

Re-run the test that produced the finding, ideally with variations:

- **Timing findings**: Re-run with different trial count, key size, or algorithm parameters. Compute statistical significance (is the difference more than 3 standard deviations?).
- **Configuration findings**: Re-read the config file, confirm the setting exists. Check if it's a system default vs. distribution-specific customization.
- **Parser/crash findings**: Re-run the exact input. Try adjacent inputs. Confirm the crash is deterministic. **Re-run through the system-installed production binary with default flags** — not the ASan build or fuzzer harness. If the system binary rejects the input, note this and attempt a bypass.
- **Protocol findings**: Re-run the connection test. Try from a different client if possible.
- **Injection findings**: Re-run the injection. Verify the injected data actually reached the target.

**Production reproduction artifact**: After reproducing, document:

```markdown
## Production Reproduction

| Field | Value |
|-------|-------|
| **Binary** | <system binary path + version> |
| **Command** | `<exact command run>` |
| **Exit code / Signal** | <exit code or signal number> |
| **Date verified** | <YYYY-MM-DD> |

### Output
<full stdout+stderr captured>
```

**Short-circuit**: If cannot reproduce → **CLOSE**. Skip remaining stages.

---

## Stage 5 — Exploitability Assessment

Determine whether the finding is practically exploitable:

1. **Attack model**: What position does the attacker need? (local, adjacent network, remote, MITM)
2. **Prerequisites**: What must be true? (specific configuration, user interaction, protocol version)
3. **Complexity**: How many queries/attempts are needed? How precise must timing be?
4. **PoC feasibility**: Can a working proof-of-concept be built?

**For timing side channels specifically**:
- Is the timing difference measurable over a real network (not just localhost)?
- How many queries are needed for statistical confidence?
- Does the target rate-limit or log excessive queries?
- Is the vulnerable code path reachable in a typical deployment?

**For configuration findings**:
- Is this the default configuration or does it require manual opt-in?
- What percentage of real-world deployments use this configuration?
- Is there a realistic attack scenario?

---

## Stage 6 — Severity Calibration (FINAL)

Check whether the assigned severity is correct:

1. **Historical comparison**: Search for CVEs in the same software for the same vulnerability class. What CVSS scores did they receive?
2. **CVSS calculation**: Walk through CVSS 3.1 vector components based on the exploitability assessment.
3. **Project severity criteria**: If the project has its own severity definitions, map the finding to those criteria.
4. **Cross-reference with peers**: What severity do similar findings in peer software receive?

**Common calibration errors**:
- **Over-rating config issues**: "Weak cipher available" is not the same as "weak cipher in use by default"
- **Under-rating timing side channels**: A 33% timing difference is large by side-channel standards
- **Ignoring platform context**: A finding on an offensive tool vs. a production server has different severity
- **Conflating theoretical and practical**: "Theoretically possible" is not "practically exploitable"

---

## Confidence Scoring

Combine the stage results into an overall confidence score:

### HIGH Confidence (Escalate to humans)
- Reproduced: YES
- Known CVE: NO or PARTIAL (novel or unpatched)
- Intended behavior: NO
- Exploitable: YES or PARTIAL
- Severity: CORRECT or UNDER

### MEDIUM Confidence (Investigate further)
- Reproduced: YES or PARTIAL
- Any stage returned UNKNOWN or conflicting signals
- May need human judgment on intent or severity

### LOW Confidence (Close or deprioritize)
- Reproduced: NO, or
- Known CVE: YES with patch applied, or
- Intended behavior: YES, or
- Exploitable: NO

## Action Classification

- **ESCALATE**: Finding is real, novel, and exploitable. Route to human reviewer with full validation card.
- **INVESTIGATE**: Finding has mixed signals. Present the ambiguity clearly so a human can make the call with less effort.
- **CLOSE**: Finding is a false positive, duplicate, or intended behavior. Document why and close.

## Validation Summary

Create a summary ranking all findings:

```markdown
# Validation Summary

| Finding | Title | Original Severity | Validated Severity | Confidence | Action |
|---------|-------|-------------------|--------------------|------------|--------|
| 001     | ...   | Medium-High       | Medium-High        | HIGH       | ESCALATE |
| 002     | ...   | High              | Low                | LOW        | CLOSE  |

## Human Review Queue

1. **001 — [Title]** (ESCALATE, HIGH confidence)
   [One-line summary of why.]
   Human effort: ~30 min to [specific check].

2. **006 — [Title]** (INVESTIGATE, MEDIUM confidence)
   [One-line summary of ambiguity.]
   Human effort: ~15 min to [specific check].
```

## Important Notes

- **Don't destroy evidence**: Append validation results to finding files, don't overwrite original content.
- **Be honest about unknowns**: "No results found" is not the same as "not a known vulnerability." Absence of evidence is not evidence of absence.
- **Show your severity reasoning**: Don't just say "severity is correct" — explain why with reference to comparable CVEs or CVSS components.
- **Batch prioritization**: Process High/Critical severity findings first, then Medium, then Low, then Informational.
- **Parallel stages**: Stages 1 (CVE search) and 2 (upstream context) can run in parallel. Stage 4 (reproduction) is expensive — only run it for findings that survive the first three stages.
