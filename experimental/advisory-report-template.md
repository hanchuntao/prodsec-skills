---
name: advisory-report-template
description: >
  Transform a validated security finding into an advisory-ready report with 14
  mandatory fields. Use as the last step before human escalation — ensures the
  recipient can act without requesting additional information.
---

# Advisory Report Template

## Overview

This skill transforms a security finding that has passed validation and adversarial review into a document that a product security team can act on without requesting additional information. It defines 14 mandatory fields that encode the information security teams need to triage, reproduce, assess, and remediate a vulnerability.

**This is a translator, not an analyst.** It does not discover new information about the vulnerability. It reorganizes and verifies what the finding already established. If a field cannot be filled from the finding, flag it as TODO rather than speculating.

## Prerequisites

Before generating an advisory:

1. Finding file exists and is readable
2. Adversarial review exists with a PASS verdict (CONDITIONAL PASS and FAIL block generation)
3. If a revision log exists, all must-fix items are resolved

## The 14 Mandatory Fields

### Field 1: Executive Summary

**Contains**: 2-3 sentences understandable by a VP of Engineering. No jargon, no code, no CVE numbers. Answer: what is broken, what can an attacker do, and how bad is it.

**Guidance**: Strip technical detail. Replace "heap-buffer-overflow in findPreambleTag due to unchecked preamble tag length exceeding the allocated buffer" with "A maliciously crafted RPM spec file can crash rpmbuild and potentially execute arbitrary code during package builds." Do NOT include version numbers, NVRs, or architecture details — those have their own fields.

**Quality check**: Read it aloud. If it requires knowledge of the codebase to understand, rewrite it.

### Field 2: Affected Versions

**Contains**: A table of exact package versions (NVRs where applicable) where the vulnerable code is present. Not "package 4.x" — actual build IDs.

| Package | Version | NVR | Status |
|---------|---------|-----|--------|
| ... | ... | ... | Vulnerable (confirmed) / Vulnerable (code present, untested) / Not affected / TODO |

**Guidance**: For versions that cannot be confirmed from available sources, mark as TODO with the specific query the human should run.

### Field 3: Affected Products

**Contains**: A table mapping the vulnerability to product lines. Not "probably in the product" — explicit per-product status.

| Product | Version | Status |
|---------|---------|--------|
| ... | ... | Affected / Likely affected (uses <version>) / Not affected / TODO |

**Guidance**: Enumerate from package presence in build tags where accessible. For products that cannot be verified, provide the table with TODO markers and the specific checks the human should perform.

### Field 4: Architecture Validation

**Contains**: A table showing which CPU architectures were tested and the result on each.

| Architecture | Tested | Result |
|-------------|--------|--------|
| x86_64 | YES/NO | Crash confirmed / Not tested |
| aarch64 | YES/NO | Crash confirmed / Not tested |
| s390x | NO | TODO — requires test system |
| ppc64le | NO | TODO — requires test system |

**Guidance**: For crash/memory-safety findings, note whether the bug is architecture-dependent (pointer size, alignment, endianness). Flag untested architectures required by the target platform.

### Field 5: Reproduction Steps

**Contains**: Numbered, copy-paste-ready steps using the system-installed binary with default flags. The recipient must be able to reproduce in under 5 minutes without special tooling.

**Requirements**:
- Must use the **system binary**, not an ASan build or fuzzer harness
- Must use **default flags** — no force flags, no insecure mode, no custom environment variables unless they are the default
- Must include **expected output**: exact exit code, signal, error message, or behavioral indicator
- Must include **system tested**: OS, package version, architecture

### Field 6: Embedded PoC

**Contains**: The actual trigger file content, not a generation command. The recipient must be able to reproduce WITHOUT running a generator script.

**Requirements**:
- For text files, include inline
- For binary files, include as base64
- Include SHA-256 hash and file size
- A generator command may be included as a convenience, but the actual file content is mandatory

**Why**: The recipient may be in a restricted environment or may not trust running a script from a security report.

### Field 7: Root Cause

**Contains**: The exact file path, function name, and line numbers where the vulnerability exists. Annotated code showing the flaw.

**Requirements**:
- File path, function name, line range
- Commit hash (if available)
- Annotated code snippet showing the flaw
- **Verify line numbers against actual source code.** If line numbers are wrong (shifted due to patches, different version), correct them and note the version checked
- Mark as: `Verified against <package-version> on <date>` or `Unverified — requires source code access`

### Field 8: Impact Assessment (CVSS)

**Contains**: A CVSS 3.1 score with per-component justification. Not just "High (7.5)" — a full breakdown explaining WHY each component has its value.

| Component | Value | Justification |
|-----------|-------|---------------|
| AV (Attack Vector) | L/A/N | Why? Local file processing = L. Network service = N. |
| AC (Attack Complexity) | L/H | Why? Crafted input with no special conditions = L. Requires race/MITM = H. |
| PR (Privileges Required) | N/L/H | Why? Unauthenticated input = N. Requires user account = L. |
| UI (User Interaction) | N/R | Why? Automated processing = N. Requires user to open file = R. |
| S (Scope) | U/C | Why? Stays within the process = U. Escapes to other components = C. |
| C (Confidentiality) | N/L/H | Why? No data leak = N. Heap contents leaked = L. |
| I (Integrity) | N/L/H | Why? No data modification = N. Arbitrary write = H. |
| A (Availability) | N/L/H | Why? Process crash = H. Temporary degradation = L. |

Cross-reference against 2-3 comparable CVEs in the same software for calibration.

### Field 9: Workaround

**Contains**: Actionable steps to mitigate the vulnerability WITHOUT a code fix. Must work with the current released version.

**Options to consider**:
- Input validation (reject inputs exceeding a threshold)
- Resource limits (RLIMIT_STACK, RLIMIT_AS, ulimit)
- Container isolation (run the vulnerable binary in a restricted container)
- Configuration changes (disable a feature, change a default)
- Network-level controls (firewall rules, rate limiting)

If no viable workaround exists, say so explicitly: "No workaround available — a code fix is required."

Do NOT suggest "upgrade to the latest version" as a workaround — that is a fix, not a workaround.

### Field 10: Proposed Fix

**Contains**: A code patch that addresses the root cause. Must be syntactically valid and ideally compile-tested.

**Requirements**:
- Verify the fix applies to the actual source code (confirm surrounding code matches)
- Mark as:
  - `Verified: YES — compiles against <commit/version>`
  - `Verified: SYNTAX ONLY — not compile-tested`
  - `Verified: NO — fix does not apply cleanly, see notes`
- If no fix can be proposed: mark as TODO. Do NOT auto-generate a fix that cannot be verified — an incorrect fix damages credibility more than a missing one

### Field 11: Exploitation in the Wild

**Contains**: Evidence of whether this vulnerability or its class is being actively exploited. Document the search methodology so the recipient knows the absence is informed.

**Searches to perform**:
- Exploit databases (Exploit-DB)
- GitHub security advisories
- CISA Known Exploited Vulnerabilities (KEV) catalog
- oss-security mailing list

Document each search and its result. If no exploitation evidence is found, state "No evidence found" with the searches performed.

### Field 12: Blast Radius

**Contains**: An enumeration of what else is affected beyond the immediate target.

**For libraries**: Identify binaries that link against the vulnerable library (dependency queries, ldd).

**For binaries**: Identify tools, services, or automation that invoke the vulnerable binary.

**For build tools**: Assess whether the vulnerability affects the build pipeline itself (supply chain risk).

Document the dependency chain. A vulnerability in a widely-linked library has a much larger blast radius than one in a standalone CLI tool.

### Field 13: Build System Impact

**Contains**: For build infrastructure targets, an assessment of whether the vulnerability can be exploited through the build system.

- If the target is NOT build infrastructure: write "N/A" and mark as FILLED
- If the target IS build infrastructure: assess supply chain risk — can a malicious source artifact trigger the vulnerability during build? What isolation exists? What privileges does the build process run with?

### Field 14: References

**Contains**: Every external source consulted during the assessment and report generation.

Organize into categories:
- CVE searches: URLs queried and results
- Upstream issues: issue tracker links, mailing list threads
- Related advisories: vendor advisories addressing similar issues
- Source code references: commit hashes for vulnerable code and fix commits
- Standards: CWE entries, CVSS calculator links

**Every URL must be real. Do NOT fabricate reference URLs.**

---

## Quality Status Taxonomy

For each field in the advisory, assign a status:

| Status | Meaning |
|--------|---------|
| **FILLED** | Complete and verified against primary sources |
| **FILLED (auto-generated)** | Generated during report creation, not extracted from the finding — flag for human review |
| **PARTIAL** | Some content but gaps remain (e.g., 3 of 7 versions confirmed) |
| **TODO** | Could not be filled — specific information needed is documented |

## Completeness Scorecard

End the advisory with:

```markdown
## Completeness Scorecard

| # | Field | Status | Notes |
|---|-------|--------|-------|
| 1 | Executive Summary | FILLED | |
| 2 | Affected Versions | PARTIAL | 3 of 7 NVRs confirmed |
| 3 | Affected Products | TODO | Requires build system access |
| ... | ... | ... | ... |

**Complete**: X/14
**TODOs remaining**: [list with what is needed for each]
```

## Key Principles

- **The advisory stands alone.** The recipient should not need to read the original finding to understand the vulnerability.
- **Every line number must be verified.** A wrong line number forces the recipient to re-analyze the entire root cause.
- **PoC must be embedded, not generated.** "Run this script" is not acceptable in a restricted environment.
- **CVSS justification is per-component.** A bare score tells the recipient nothing.
- **Do NOT fabricate references.** If a search returned no results, say so.
- **Do NOT inflate severity.** Stacking theoretical impacts that are not all demonstrated is dishonest.
- **Do NOT downplay severity.** If the bug is a remotely exploitable heap overflow in build infrastructure, say so.
- **Mark auto-generated content.** Anything the reporter fills itself (rather than extracting from the finding) must be flagged for human review.
- **One finding, one advisory.** Do not batch multiple findings into a single advisory.
