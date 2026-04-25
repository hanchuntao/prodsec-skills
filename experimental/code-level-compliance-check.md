---
name: code-level-compliance-check
description: >
  Validate codebase against code-level compliance signals for regulatory
  frameworks (FedRAMP, FIPS 140-3, OWASP Top 10, SOC 2 Type II). Scoped to
  source code analysis only — not a compliance certification.
---

# Code-Level Compliance Check

## Overview

This skill provides checklists for scanning code-level compliance signals across four regulatory frameworks. It checks **source code, configuration files, deployment manifests, and dependency manifests only** — it does not verify organizational, infrastructure, or procedural controls.

**This is a development aid, not a compliance certification.**

## Supported Frameworks

- **FedRAMP** — Federal Risk and Authorization Management Program code-level controls
- **FIPS** — FIPS 140-3 approved cryptography and key management patterns
- **OWASP** — OWASP Top 10 (2021) compliance with evidence
- **SOC 2** — SOC 2 Type II code-level security controls

Multiple frameworks can be checked in a single pass.

## Scope Constraint

Limit analysis to code-level signals only:
- Source code files
- Configuration files (Dockerfiles, docker-compose, Kubernetes manifests, Terraform, CI configs)
- Dependency manifests (package.json, requirements.txt, go.mod, Cargo.toml)
- Hardcoded values

Do NOT attempt to verify:
- Organizational policies and procedures
- Infrastructure and network controls outside the codebase
- Personnel security (background checks, training)
- Physical security controls
- Vendor and third-party risk management
- Incident response procedures and testing
- Continuous monitoring infrastructure
- CMVP certification status of cryptographic modules (FIPS)
- Audit log forwarding and SIEM integration

---

## FedRAMP Code-Level Signals

### Access Control (AC)

- Role-based access control (RBAC) implementation patterns in code
- Least privilege enforcement (no overly broad permission grants in code)
- Session timeout configuration in application code
- Multi-factor authentication enforcement in authentication flows

### Audit and Accountability (AU)

- Audit logging calls present for security-relevant events (login, logout, privilege changes, data access)
- Log entries include who, what, when, where (user ID, action, timestamp, source IP)
- Sensitive data excluded from log statements (no passwords, tokens, PII in log calls)

### Configuration Management (CM)

- No hardcoded environment-specific values (IPs, hostnames) in source code
- Configuration loaded from environment variables or secret managers (not hardcoded)
- Dependency pinning (exact versions in manifests, not ranges for production deps)

### Identification and Authentication (IA)

- Password complexity enforcement (min length, complexity rules in validation code)
- Account lockout after failed attempts (present in authentication logic)
- Secure credential storage patterns (hashing libraries used, not plaintext storage)

### System and Communications Protection (SC)

- TLS/HTTPS enforcement in HTTP client configuration
- No HTTP (non-TLS) connections to external services in code
- Encryption at rest patterns (use of encryption libraries for stored sensitive data)

---

## FIPS 140-3 Code-Level Signals

### Approved Cryptographic Algorithms

Flag any use of non-FIPS-approved algorithms:

| Category | NOT Approved | Approved |
|----------|-------------|----------|
| Hash functions | MD5, SHA-1 | SHA-2 (SHA-256, SHA-384, SHA-512), SHA-3 |
| Symmetric encryption | DES, 3DES, RC4, RC2, Blowfish | AES (128, 192, 256-bit) |
| Asymmetric encryption | RSA < 2048 bits | RSA >= 2048, ECDSA with NIST curves (P-256, P-384, P-521) |
| Key agreement | DH < 2048 bits | DH >= 2048, ECDH with NIST curves |
| MAC | HMAC-SHA1 (flag for review) | HMAC-SHA-256 and above |

### Key Management Patterns

- Key derivation using PBKDF2, HKDF, or NIST-approved KDFs (flag use of custom KDFs)
- Key lengths meeting FIPS minimums (flag short keys)
- Secure key storage patterns (keys not hardcoded in source)

### Random Number Generation

- Use of cryptographically secure RNG (flag use of `Math.random()`, `random.random()`, or non-CSPRNG for security purposes)
- Flag use of predictable seeds for security-sensitive randomness

### Cipher Mode of Operation

- Flag ECB mode usage (not approved for most uses)
- Flag unauthenticated CBC for encryption-then-MAC concerns (prefer GCM or CCM)

### FIPS Severity Rating

- **Critical**: Non-FIPS algorithm actively used in security-sensitive path
- **High**: Non-FIPS algorithm used but context unclear, or key length below minimum
- **Medium**: Potentially non-FIPS pattern requiring manual review
- **Low**: Approved algorithm but suboptimal configuration

---

## OWASP Top 10 (2021) Code-Level Signals

### A01 — Broken Access Control

- Missing authorization checks on sensitive endpoints
- Insecure direct object references (user-controlled IDs without ownership check)
- CORS misconfiguration (wildcard origins in code)

### A02 — Cryptographic Failures

- Sensitive data transmitted in HTTP (non-TLS)
- Weak or deprecated cryptographic algorithms (see FIPS section for specifics)
- Secrets hardcoded in source

### A03 — Injection

- SQL queries built by string concatenation (not parameterized)
- Command injection (`os.system`, `exec` with user input)
- LDAP, XPath, SSTI injection patterns
- NoSQL injection (unvalidated object queries)

### A04 — Insecure Design

- Missing input validation on public API endpoints
- Business logic that can be bypassed by parameter manipulation
- Rate limiting absent on authentication/sensitive endpoints

### A05 — Security Misconfiguration

- Debug endpoints or stack traces exposed in production configuration
- Default credentials in config files
- Unnecessary features or services enabled in deployment manifests

### A06 — Vulnerable and Outdated Components

- Dependency manifests present for review (flag if lock files are absent)
- Known vulnerable version ranges (flag if visible from manifest context)

### A07 — Identification and Authentication Failures

- Weak session management (short session IDs, missing expiry)
- Brute force protection absent on login endpoints
- Insecure password reset flows

### A08 — Software and Data Integrity Failures

- Deserialization of untrusted data without validation
- Dependency integrity checks absent (no subresource integrity, no lock files)
- CI/CD pipeline accepting unverified artifacts

### A09 — Security Logging and Monitoring Failures

- Absence of logging for authentication events, access control failures
- Sensitive data included in log statements

### A10 — Server-Side Request Forgery (SSRF)

- User-controlled URLs passed to HTTP client libraries without allowlist validation
- DNS rebinding exposure patterns

---

## SOC 2 Type II Code-Level Signals

Focus on the Security trust service criteria (CC).

### CC6 — Logical and Physical Access Controls

- Authentication required for all non-public endpoints (flag missing auth middleware)
- Role-based access control implementation (RBAC patterns present)
- Privileged access controls (admin functions gated by elevated role checks)
- Session management (timeouts, invalidation on logout)

### CC7 — System Operations

- Error handling that does not expose stack traces or internal details to users
- Logging of security-relevant events (authentication, authorization failures, data access)
- Sensitive data excluded from logs (no passwords, tokens, or PII in log calls)

### CC8 — Change Management

- No commented-out code containing credentials or sensitive logic
- Environment-specific configuration externalized (not hardcoded for prod/staging)
- Feature flags or configuration toggles present for controlled rollout

### CC9 — Risk Mitigation

- Input validation on all external data sources (HTTP params, file uploads, webhooks)
- Output encoding to prevent injection in rendered content
- Dependency versions pinned (supply chain risk reduction)

### Data Protection Patterns

- Encryption used for sensitive data fields at rest (ORM-level or application-level)
- Secure transmission enforced (TLS configuration, HSTS headers in web config)
- PII minimization (collect only what is needed)

---

## Severity Rating

Rate each finding: **Critical / High / Medium / Low**.

## Verdict Rules

- **BLOCKED**: Any Critical findings OR 3+ High findings
- **PASS_WITH_NOTES**: 1-2 High findings OR 3+ Medium findings
- **PASS**: Only Medium/Low findings

## Report Structure

Organize findings by framework and control category. For each finding, include:
- Framework and control reference (e.g., "FIPS — Approved Algorithms")
- File and line (if applicable)
- Severity (Critical/High/Medium/Low)
- Description of the gap
- Recommended remediation

End the report with:
- Prioritized action items (address Critical before any compliance claim)
- Risk score (1-10 scale)
- Limitations section documenting what was NOT checked

## Limitations

This report covers **code-level compliance signals only**:

**What is checked:**
- Code-level security patterns (encryption, auth, input validation)
- Configuration file analysis (Dockerfiles, deployment manifests)
- Dependency and library usage patterns
- Hardcoded credentials and secret management patterns

**What is NOT checked:**
- Organizational policies and procedures
- Infrastructure and network controls
- Personnel security
- Physical security controls
- Vendor and third-party risk management
- Incident response procedures
- Continuous monitoring infrastructure
- CMVP certification status of cryptographic modules
- Audit log forwarding and SIEM integration

**This report is a development aid, not a compliance certification.**
