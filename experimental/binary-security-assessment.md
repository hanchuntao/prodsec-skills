---
name: binary-security-assessment
description: >
  Methodology for multi-phase security assessment of binaries, libraries, and
  services. Covers 11 phases from reconnaissance through differential testing,
  with phase selection guidance, severity classification, and finding report
  templates. Use when planning or executing a security assessment of compiled
  software.
---

# Binary Security Assessment Methodology

## Overview

This skill defines an 11-phase methodology for security assessment of binaries, libraries, and network services. Not all phases apply to every target — use the phase selection guide to choose the right approach.

## Phase Overview

| Phase | Name | When to Run | Typical Duration |
|-------|------|-------------|-----------------|
| 0 | Reconnaissance | Always | 10-18 min |
| 1 | Cryptographic analysis | Target handles crypto (TLS, key management) | 30-60 min |
| 2 | Parser fuzzing | Target parses structured input | 30-60 min |
| 3 | Protocol testing | Target implements a network protocol | 30-60 min |
| 4 | Certificate validation | Target validates certificates or hostnames | 15-30 min |
| 5 | Configuration audit | Target has system-level config files | 15-30 min |
| 6 | Input sanitization | Target accepts user input (CLI, URLs, headers) | 15-30 min |
| 7 | Sanitizer testing | Source available, hidden memory bugs suspected | 1-2 hours |
| 8 | Source code review | Source available, logic bugs suspected | 2-4 hours |
| 9 | Coverage-guided fuzzing | Source available, complex input handling | 24-72 hours |
| 10 | Differential testing | Multiple implementations of same standard exist | 1-2 hours |

**Phases 0-6** are fast (minutes to an hour). Run them first.
**Phases 7-8** are medium effort (hours). Run when source is available.
**Phase 9** is long-running (hours to days). Start early, triage crashes as they arrive.

---

## Technique-vs-Target-Type Matrix

| Target Type | Best Technique | Why | Fuzzing Yield |
|-------------|---------------|-----|---------------|
| **Parsers** (ASN.1, DER, XML, RPM, images) | Phase 9 (fuzzing) | Complex memory management, variable-length fields | **High** — most CVEs found this way |
| **Math/crypto** (PQC, RSA, ECC, hashing) | Phase 8 (source review) | Minimal memory management, logic bugs don't crash | **Low** |
| **Protocol state machines** (TLS, SSH, HTTP) | Phase 9 + Phase 8 | State transitions + protocol parsing | **Medium** — need stateful harnesses |
| **Integration boundaries** (key serialization, cert encoding) | Phase 9 (fuzzing) | Parser code wrapping crypto | **Highest** — 2x edge coverage vs. standalone |
| **Configuration/policy** | Phase 5 + Phase 8 | Logic bugs, not memory corruption | **Low** for fuzzing |

**Key principle**: If mostly math with minimal malloc/memcpy, prioritize source review. If it parses structured binary input, prioritize fuzzing. If it does both, fuzz the parser paths and review the crypto paths.

---

## Phase 1 — Cryptographic Analysis

Test for cryptographic weaknesses:

- **RSA timing side channels**: Measure decryption timing (200+ trials) for valid vs. malformed ciphertexts. Flag >10% median timing differences. Compare against RSA-OAEP as constant-time control.
- **ECDSA nonce analysis**: Sign same message 20+ times, verify all signatures unique (nonce reuse = private key recovery). Note whether signing is deterministic (RFC 6979).
- **RNG quality**: Generate 50 keys rapidly, hash each, check for duplicates (duplicate = critical RNG failure).
- **DH parameter validation**: Attempt weak sizes (512, 768, 1024 bits), check for appropriate warnings.
- **Key derivation**: Test for legacy KDF (MD5, no PBKDF2), password handling edge cases (empty, long, special characters, format strings), password truncation.

## Phase 2 — Parser Fuzzing

Test every input parser with:

1. Empty input (0 bytes)
2. Null bytes (256 bytes of 0x00)
3. Huge length fields (e.g., ASN.1 length = 0xFFFFFFFF)
4. Negative/invalid lengths
5. Truncated valid input (50% and 90%)
6. Deeply nested structures (10,000+ levels)
7. Oversized fields (1MB+)
8. Invalid enum/OID values
9. Format-specific attacks (invalid base64, wrong tags)

Run each with `timeout 5`. Flag: crashes, hangs (>5s), unexpected success, excessive memory use.

## Phase 3 — Protocol Testing

- **TLS version and cipher audit**: Test SSLv3 through TLS 1.3. Test NULL, anonymous, export, RC4, DES, CBC, and AEAD ciphers. Test at both DEFAULT and lowest security level.
- **Handshake robustness**: Malformed ClientHello, zero-length cipher list, huge SNI, invalid version, non-TLS data to TLS port.
- **Renegotiation and sessions**: Client-initiated renegotiation, session resumption, corrupted session tickets, unsafe legacy renegotiation.

## Phase 4 — Certificate and Identity Validation

Test chain validation, wrong CA rejection, name constraints, SAN mismatches, null byte CN bypass, self-signed rejection, SHA-1 cert handling, expired cert rejection, and corrupted signature rejection.

## Phase 5 — Configuration Audit

Review system config files for security settings (minimum protocol versions, cipher strings, security levels, enabled providers). Check for unsafe options, hardcoded paths/credentials, information disclosure in version output, and file permissions on key material.

## Phase 6 — Input Sanitization and Injection

Test command injection via subject fields, format string injection in password fields, path traversal in module loading, oversized inputs, concurrent operations, and error message information leakage.

## Phase 7 — Sanitizer Testing

Recompile with sanitizers (ASan, UBSan, MSan) and re-run all inputs from Phases 2-6:

| Sanitizer | Report Type | Severity |
|-----------|-------------|----------|
| ASan | heap-buffer-overflow | Critical — likely exploitable |
| ASan | stack-buffer-overflow | High — potentially exploitable |
| ASan | use-after-free | Critical — exploitable |
| ASan | double-free | High — exploitable |
| UBSan | signed integer overflow | Medium — may corrupt state |
| UBSan | null pointer dereference | Medium — DoS at minimum |
| MSan | use-of-uninitialized-value | High — information leak |

Also create targeted inputs for boundary values, after-free patterns, integer overflow, and uninitialized data.

## Phase 8 — Source Code Review

Focus on code that handles untrusted input:

**Memory safety**: `memcpy`/`memmove` with unchecked lengths, `strlen` on non-null-terminated strings, `sprintf` instead of `snprintf`, stack buffers with unchecked input lengths, `realloc` without NULL check.

**Integer issues**: overflow in size calculations, signed/unsigned comparison, width truncation near boundaries.

**Logic bugs**: off-by-one, TOCTOU, missing null checks, switch fallthrough, error paths that skip cleanup.

**Crypto-specific**: non-constant-time comparison (`memcmp` vs. `CRYPTO_memcmp`), padding oracle patterns, nonce/IV reuse, weak PRNG seeding.

**Historical pattern matching**: Fetch recent CVE fixes, understand the bug pattern, search for the same pattern elsewhere in the codebase.

## Phase 9 — Coverage-Guided Fuzzing

See the existing fuzzing skills in this repository for detailed AFL++, libFuzzer, cargo-fuzz, LibAFL, and other fuzzer-specific guidance. Key methodology points:

- **Harness selection**: Prioritize integration harnesses over standalone algorithm harnesses (2x edge coverage)
- **Seed validation gate**: Verify seeds exercise target code beyond error-handling baseline before launching
- **CVE pre-validation**: Build a known-vulnerable version to confirm toolchain detects known bugs
- **10-minute coverage checkpoint**: Stop campaigns where bitmap coverage is stagnant and corpus is not growing
- **System binary gate**: Reproduce every crash with the production binary using default flags before writing a finding

## Phase 10 — Differential Testing

Run the same inputs through multiple implementations and compare behavior. Disagreement on malformed input handling indicates a bug in at least one implementation.

| Divergence Type | Significance |
|----------------|-------------|
| Exit-code divergence + one crashes | Bug in crashing implementation (high confidence) |
| Exit-code divergence + both complete | One is more permissive — check which should reject |
| Output divergence + same exit code | Silent behavior difference — may be benign or a parsing discrepancy |

---

## System Binary Gate

**For every crash/memory-safety finding**: Reproduce with the system-installed production binary using default flags before writing the finding.

- If the system binary crashes: **confirmed production vulnerability**
- If it rejects the input: determine why, attempt bypass
- If the bug requires special flags: document clearly, lower severity
- If it only triggers under ASan: note this, rate as code quality issue unless a production trigger is found

## Severity Classification

| Severity | Criteria |
|----------|----------|
| Critical | Remote code execution, private key disclosure, authentication bypass |
| High | MITM without authentication, crypto break, verification bypass |
| Medium-High | Exploitable side channel, weak defaults enabling attacks |
| Medium | Deprecated protocols/ciphers accepted, missing safety warnings |
| Low-Medium | Weak algorithms accepted at non-default settings |
| Low | Information disclosure, legacy features available but not default |

## Finding Report Template

```markdown
# Finding: [Title]

| Field | Value |
|-------|-------|
| **Target** | [package and version] |
| **Severity** | [severity] |
| **CVSS** | [score] ([vector]) |
| **CWE** | [CWE-ID] |
| **Date** | [YYYY-MM-DD] |

## Executive Summary
[2-3 sentences]

## Finding Detail
[Root cause analysis with code references]

## Evidence
[Exact commands and output]

## Production Reproduction
[System binary + default flags reproduction]

## Impact Assessment
[Exploitability factors, attack model, prerequisites]

## Workaround
[Mitigation without code fix]

## Exploitation in the Wild
[Search results from exploit databases]

## Affected Products
[Platform product mapping]

## Proposed Fix
[Code patch, verified if possible]

## Recommendations
[Prioritized action items]
```

## Important Notes

- Use `timeout` on all commands to prevent hangs
- Timing measurements over SSH have ~4ms overhead — only flag signals >10% above noise
- Sanitizer builds go in separate directories — never overwrite system binaries
- Source review should focus on code handling untrusted input, not boilerplate
- Document what was tested and found secure — positive findings tell the consumer what they don't need to worry about
