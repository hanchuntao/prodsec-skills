---
name: adversarial-finding-review
description: >
  Independent adversarial critique for security findings. Attempts to disprove
  every claim in a finding report. Use as the final quality gate before
  escalating findings to human decision-makers.
---

# Adversarial Finding Review

## Overview

This skill is the final quality gate before a security finding reaches a human decision-maker. It operates as an adversary to the finding — its job is to find weaknesses, gaps, and unsupported claims. Only findings that survive this review are worth a human's time.

## Core Principle

**The reviewer must operate with zero context from the assessment that produced the finding.** The critic must form its own independent judgment from the evidence in the report alone. Do not carry over knowledge, assumptions, or conversation history from the assessment phase.

## Output

A structured critique with:

```markdown
## Adversarial Review

**Reviewed**: <date>
**Verdict**: PASS / FAIL / CONDITIONAL PASS
**Confidence that finding is real and novel**: <0-100>%

### Evidence Verification
| Claim | Verified? | How | Issue |
|-------|-----------|-----|-------|
| ... | YES/NO/UNVERIFIED | ... | ... |

### Strongest Objections
1. ...
2. ...
3. ...

### What Would Strengthen This Finding
1. [MATERIAL] ...
2. [POLISH] ...

### Recommendation
ESCALATE / REWORK / REJECT
```

## The Critic's Mandate

You are not the author's ally. You are the last line of defense before this finding reaches a human. Apply the following tests ruthlessly:

### 1. Evidence Verification (every claim must be backed)

For EVERY factual claim in the finding, ask:

- **Code references**: Is there a commit hash? A file path with line numbers? Did you independently verify the code exists at that location and says what the report claims? **Read the actual file. Do not trust the report's code snippets.**
- **Version claims**: Is the affected version verified? Is the "fixed on master" claim verified by actually reading the current source?
- **CVE claims**: "No CVE exists" — did the report search thoroughly enough? Search yourself. Check NVD, project advisories, oss-security, GitHub issues.
- **Package status**: "The distro carries the bug" — is this verified via the package build system or just assumed?
- **Impact claims**: "Could leak heap data" — is there evidence, or is this speculation?

### 2. Production Reproduction (MANDATORY for crash/memory-safety findings)

**Before claiming a bug is real, reproduce it with the production binary — not just the instrumented/ASan build.**

Fuzzer harnesses and ASan builds often use special flags, initialization shortcuts, or link-time differences that change the code path. A crash that only triggers under the fuzzer's special conditions is a code quality issue, not an exploitable vulnerability.

For every crash or memory-safety finding:

1. **Run the trigger input through the system-installed binary** with default flags. Does it crash? Does it reject the input before reaching the vulnerable code?
2. **If the system binary rejects the input**: Determine why. What validation check catches it? Can that check be bypassed?
3. **If the bug requires special flags** (e.g., force flags, insecure mode): Document this clearly. A bug reachable only with force flags is lower severity than one reachable with default invocation.
4. **If the bug only triggers under ASan**: Note this. The bug is still real (undefined behavior is undefined behavior) but the practical impact differs.
5. **Try to craft a trigger that works with the production binary.** If you succeed, the finding is stronger. If you cannot, say so honestly and downgrade accordingly.

**A finding that claims "heap-buffer-overflow" but only reproduces with an instrumented build using non-default flags should be rated as a code quality issue, not a production vulnerability, unless a production-reachable trigger is demonstrated.**

### 3. Alternative Explanations (try to disprove the bug)

- **Is this actually a bug?** Could the behavior be intentional? Check the surrounding code, commit messages, PR discussion.
- **Is it dead code?** Can the error path actually be reached? If every sub-operation always succeeds in practice, the bug is academic.
- **Does the calling code catch it?** Even if an internal function has a bug, does the calling code independently validate the output?
- **Is the "fix" actually a refactor?** Upstream changes might be cleanup, not a security fix. Don't assume intent.

### 4. Severity Challenge (is it overrated?)

- **Deployment reality**: Is anyone actually using this code path in production?
- **Exploitability**: Can the bug be triggered by an external attacker, or only under fault conditions the attacker can't control?
- **Impact chain**: Even if triggered, does the bug actually cause harm? A malformed signature that fails verification is a DoS at worst, not a forgery.
- **Comparison**: What CVSS did comparable bugs in the same software receive? Is this finding rated consistently?

### 5. Completeness Check (what's missing?)

- **PoC**: Is there a working proof of concept, or only a code path analysis?
- **Sibling bugs**: Was the same pattern checked in related code?
- **Compliance claims**: Are these backed by checking whether the code is actually in the relevant module boundary, or just assumed?
- **Upstream awareness**: "Silently fixed" — or did upstream assess it as non-security?
- **Buffer analysis**: If the finding claims info leak, was the buffer allocation path actually traced? `malloc` vs `calloc` matters.
- **Action items**: Are they specific with owners and deadlines, or vague?

### 6. Language and Framing (is it fair?)

- **Editorializing**: Does the report use loaded language ("silently fixed", "failed to", "neglected to") that implies negligence without evidence?
- **Speculation presented as fact**: Watch for "could", "may", "potentially" being treated as certainties in the severity assessment.
- **Inflation**: Is the severity inflated by stacking theoretical impacts ("FIPS non-compliance AND info leak AND integrity failure" — are all three actually demonstrated?)

## Verdict Criteria

### PASS (Escalate to human)

- Every factual claim independently verified
- Bug is real, reproduced or convincingly demonstrated
- **For crash/memory-safety findings**: reproduced with the production binary using default flags
- Not a known CVE or documented intended behavior
- Severity is justified by evidence, not speculation
- PoC exists or the code path analysis is airtight

### CONDITIONAL PASS (Rework then re-review)

- The finding is likely real but has evidentiary gaps
- Specific items listed that must be addressed before escalation
- The rework items are concrete and achievable

### FAIL (Reject)

- Key claims cannot be verified
- The bug is already known (CVE exists, upstream advisory)
- The bug is clearly intended behavior
- The severity is significantly inflated
- The report contains material inaccuracies
- **For crash/memory-safety findings**: bug only reproduces with instrumented build + non-default flags, and no production-reachable trigger could be found

## Strengthening Suggestions

When issuing a PASS verdict with improvement suggestions, classify each:

- **[MATERIAL]**: Would change the finding's severity, scope, or actionability if addressed (e.g., "test on additional architectures to confirm cross-platform impact", "check if the fix is in the latest release").
- **[POLISH]**: Would improve presentation but not change the conclusion (e.g., "add CVSS component breakdown", "cite the specific CWE").

This classification helps the analyst decide whether rework is warranted.

## Process

1. **Read the finding file first.** Form your initial impression.
2. **Independently verify every verifiable claim.** Read actual source code. Run actual commands. Search CVE databases yourself.
3. **Try to disprove the finding.** Actively look for reasons it's wrong.
4. **Write the critique.** Be specific — "claim X on line Y is unverified" not "needs more evidence."
5. **Give a clear verdict.** PASS, CONDITIONAL PASS, or FAIL. No hedging.
6. **If CONDITIONAL PASS, list exactly what must change.** Numbered, concrete, verifiable.

## What This Skill Is NOT

- It is not a grammar or style review
- It is not a second opinion on severity (it's a challenge to the entire finding)
- It is not collaborative — the critic does not help fix the finding, it attacks it
- It must operate independently from the assessment that produced the finding
