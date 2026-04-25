---
name: pre-assessment-recon
description: >
  Structured pre-assessment reconnaissance on a target binary, library, package,
  or service. Use before launching a security assessment to profile the target,
  assess attack surface, discover existing fuzz infrastructure, and make a
  go/no-go decision. Produces a structured recon report.
---

# Pre-Assessment Reconnaissance

## Overview

This skill performs structured reconnaissance on a target before launching a full security assessment. It answers the questions that, when skipped, cause wasted effort: What harnesses exist? Where are the seeds? Is OSS-Fuzz already covering this? What technique should be applied? Is this target worth assessing?

**Time budget**: 10-18 minutes. This is a pre-flight, not the assessment itself.

## Inputs

- **Target**: A binary name, library, package name, or host:port for a network service
- **Scope** (optional): Narrow the focus (e.g., `pqc`, `tls`, `parsers`). Default: full recon.

## Output

A single structured recon report with 8 sections covering target profile, security history, platform context, attack surface, existing fuzz infrastructure, technique recommendation, seed/dictionary plan, and a go/no-go recommendation.

---

## Section 1 — Target Profile

Gather baseline facts about the target.

### For a binary/library/package

- **Binary properties**: architecture, linking (static/dynamic), stripped, PIE, NX, RELRO
- **Source code**: upstream repo, lines of code, language breakdown
- **Version info**: latest upstream release, release cadence
- **Deployment model**: runs as root? network-facing? processes untrusted input?

### For a network service

- Service version detection and fingerprinting
- Open ports and services
- Banner grab and protocol identification

### Version Delta Warning

Compare the version on the test system against the version the target platform ships. If they differ, flag prominently:

> **VERSION MISMATCH**: Test system has `<package> <test-version>`. Target platform ships `<platform-version>`. Findings apply to `<test-version>`. Verify applicability before filing.

---

## Section 2 — Security History

Understand the target's vulnerability track record.

### CVE Search

- Query NVD, cve.org, and osv.dev for the target
- Summarize: total CVE count (last 3 years), severity distribution, top bug classes
- Note any actively exploited vulnerabilities

### OSS-Fuzz Status

- Is the target enrolled in OSS-Fuzz?
- If yes: which harnesses, estimated bug count, corpus availability

### Known Exploits

- Check exploit databases (searchsploit, Exploit-DB) for existing exploits
- Search for prior security research: public audits, blog posts, conference talks

### Upstream Issue Tracker

Search for security-adjacent patterns in the issue tracker:
- Open issues describing crashes or memory safety bugs
- PRs fixing buffer handling or adding bounds checks
- Comments flagging interfaces as problematic
- Fuzzing integration attempts

---

## Section 3 — Platform Context

Determine how this target matters to the target platform.

- **Package status**: versions shipped across platform releases
- **Version delta**: how far behind upstream, whether platform carries additional patches
- **Criticality**: is it in the base/minimal image? A build dependency? In a compliance boundary (e.g., FIPS)?
- **Content classification**: core vs. optional vs. third-party

---

## Section 4 — Attack Surface Analysis

Map the target's inputs to identify where untrusted data meets memory management.

### 4a. Input Inventory

Identify every source of untrusted input:
- CLI arguments and subcommands
- File format parsers (identify supported formats from binary strings and help output)
- Network listeners (if applicable)
- Environment variable inputs

### 4b. Parser Identification

For source-available targets, locate parser code:
- Memory-managing parser code (malloc/realloc/memcpy near parse/decode functions)
- Parser entry points and their input formats

### 4c. Trust Boundaries

- Does the binary run as root or drop privileges?
- Does it process input before authentication?
- Does it fork/exec other programs?
- SUID/SGID bits or capabilities?

### 4d. Risk Ranking

Rank files/functions by risk:
1. Processes untrusted input directly
2. Contains memory management (malloc/realloc/memcpy)
3. Has high cyclomatic complexity
4. Has a history of CVE fixes

### 4e. Binary Structure Analysis

Use reverse engineering tools (radare2, Ghidra) on the compiled binary to:
- Identify the largest/most complex functions
- Map call graphs from parser entry points
- Find cross-references to dangerous functions (memcpy, strcpy, etc.)
- Determine which functions are reachable from the harness entry point

### 4f. Dynamic Trace Analysis

Trace runtime behavior on a real input using ltrace/strace to understand:
- Library call profile (what C library functions are called, with counts)
- Memory operation patterns (malloc sizes, memcpy lengths)
- Syscall profile (file access, mmap, network)
- Harness dependencies (files, env vars the binary requires)

---

## Section 5 — Existing Fuzz Infrastructure

Discover what the project already provides for fuzzing.

### Harnesses

- Standard fuzz directories (`fuzz/`, `fuzzing/`)
- For each harness: input format, code exercised, standalone vs. integration

### Corpora and Seeds

- Project's own fuzz corpora
- Test data that could serve as seeds (certificates, test vectors, fixtures)
- NIST/Wycheproof/ACVP test vectors

### Dictionaries

- Project-provided dictionaries
- Applicable community dictionaries (AFL++ dictionaries)
- Auto-generated from binary strings

### Build System Compatibility

- Does the build system support AFL++ instrumentation?
- Sanitizer support (ASan/UBSan/MSan)?
- Fuzzing CI configuration?

---

## Section 6 — Technique Recommendation

Based on findings, recommend which assessment phases to run.

### Technique-vs-Target-Type Decision Matrix

| Target Type | Primary Technique | Secondary Technique |
|-------------|------------------|-------------------|
| **Parsers** (ASN.1, XML, HTTP, images, RPM) | Coverage-guided fuzzing | Parser fuzzing, sanitizer testing |
| **Math/crypto** (PQC, RSA, ECC) | Source code review | Crypto analysis, integration harness fuzzing only |
| **Protocol state machines** (TLS, SSH) | Fuzzing + protocol testing | Source code review |
| **Integration boundaries** (serialization, encoding) | Coverage-guided fuzzing | Source code review |
| **Config/policy** | Configuration audit | Source code review |

**Key principle**: If a target is mostly math with minimal malloc/memcpy, prioritize source review. If it parses structured binary input, prioritize fuzzing. If it does both (e.g., a crypto library that parses DER-encoded keys), fuzz the parser paths and review the crypto paths.

### Resource Estimation

- Memory requirements per fuzzer instance (with ASan)
- Number of parallel campaigns needed
- Expected execution speed
- Recommended campaign duration

---

## Section 7 — Seed and Dictionary Plan

Consolidate every seed and dictionary source into an actionable gathering plan:

- Seed sources with locations, counts, formats, and conversion requirements
- Dictionary sources with token counts and format compatibility
- Exact commands to collect, convert, and merge seeds and dictionaries
- Readiness assessment (sufficient seeds? dictionary tokens?)

---

## Section 8 — Go/No-Go Recommendation

### GO — target is worth a full assessment

- Has meaningful attack surface (untrusted input + memory management)
- Not already saturated by existing fuzzing with public corpus
- Ships in products on the target platform (criticality justifies effort)
- Resources are available
- Harnesses and seeds exist or can be written quickly

### DEFER — prerequisites needed

- Source not yet available
- Harnesses need to be written first (estimate effort)
- A dependency must be assessed first
- Resources currently occupied

### SKIP — not worth assessing now

- Existing fuzzing already covers it thoroughly
- Not shipped in any relevant products
- Recent thorough audit exists
- Attack surface is minimal (pure math, no parsing, no memory management)

---

## Report Format

```markdown
# Recon Report: <target>

| Field | Value |
|-------|-------|
| **Date** | <YYYY-MM-DD> |
| **Target** | <target name and version> |
| **Time spent** | <minutes> |
| **Recommendation** | **GO / DEFER / SKIP** |

## 1. Target Profile
## 2. Security History
## 3. Platform Context
## 4. Attack Surface Analysis
## 5. Existing Fuzz Infrastructure
## 6. Technique Recommendation
## 7. Seed and Dictionary Plan
## 8. Go/No-Go Recommendation
```

## Important Notes

- This is reconnaissance only. No fuzzing, no exploit attempts, no timing measurements.
- If a section cannot be completed (e.g., source unavailable), note the gap and move on.
- Keep the report factual. Do not speculate about vulnerabilities — that is the assessment's job.
- The report should be self-contained: a human reading it should be able to make a go/no-go decision without running any commands.
