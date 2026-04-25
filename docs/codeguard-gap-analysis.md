# CodeGuard vs. prodsec-skills: Gap Analysis

**Date:** 2026-04-09
**Purpose:** Identify skills/coverage in [project-codeguard](https://github.com/cosai-oasis/project-codeguard) that are absent or less complete in prodsec-skills.

---

## Import Decisions (2026-04-09)

### Imported from CodeGuard

1. Client-side web security (XSS, CSRF, CSP, clickjacking)
2. File handling & uploads
3. C/C++ memory safety coding standard
4. Input validation / injection (general -- beyond MCP)
5. Database security
6. Build YAML misconfiguration (GitLab CI, Tekton, Containerfile hardening) -- custom, not a direct CodeGuard import
7. Crypto algorithm selection & post-quantum
8. XML & serialization / deserialization
9. Session management & cookies

### Skipped (covered elsewhere or low priority)

1. Kubernetes / container orchestration -- existing skills cover OpenShift/K8s
2. Framework-specific hardening (Django, Rails, .NET, etc.)
3. Mobile app security
4. Privacy & data protection -- covered in relevant individual skills
5. MCP security architectural patterns from CodeGuard -- prodsec-skills already deeper here
6. Supply chain governance & incident response
7. Logging detection & alerting patterns
8. IaC security

### Deferred for future skills

1. Authentication & MFA (user-facing)
2. Authorization & access control (general)
3. API & web services (REST, GraphQL, SOAP, SSRF)
4. Digital certificate validation

---

## Executive Summary

**CodeGuard** contains 23 consolidated security rules + 83 OWASP deep-dive reference files, focused on **secure coding practices across traditional application development** (web, mobile, API, database, IaC, CI/CD).

**prodsec-skills** contains 114 production + 13 experimental skills, focused on **agentic/AI infrastructure security** (MCP, inference engines, model registries, OAuth 2.1 for agents) and **security testing/auditing methodology** (fuzzing, static analysis, code audit workflows).

The two repos are highly complementary with surprisingly little overlap. CodeGuard's strength is breadth across traditional application security domains; prodsec-skills' strength is depth in AI/agentic security and offensive/testing methodology.

### By the Numbers

| Metric | CodeGuard | prodsec-skills |
|--------|-----------|----------------|
| Total skill/rule files | 23 rules + 83 OWASP sources | 114 production + 13 experimental |
| Traditional AppSec coverage | Comprehensive (OWASP Top 10+) | Minimal |
| AI/Agentic security coverage | 1 rule (MCP) | 63+ skills |
| Security testing methodology | None | 17 skills (fuzzing, SAST) |
| Security audit workflows | None | 4 skills |
| Framework-specific guides | 8 frameworks | None |
| Language coverage | 20+ languages | Language-agnostic |

---

## Part 1: Complete Gaps (In CodeGuard, NOT in prodsec-skills)

These are entire topic areas that CodeGuard covers and prodsec-skills has **no equivalent skill for** -- not even in `experimental/`.

### 1.1 Client-Side Web Security (XSS, CSRF, CSP, Clickjacking)

**CodeGuard file:** `codeguard-0-client-side-web-security.md` (~730 words)
**OWASP backing:** 11 additional deep-dive files (XSS prevention, DOM XSS, DOM clobbering, CSP, CSRF, clickjacking, XS-Leaks, third-party JS, AJAX, HTML5 security)

**What's missing from prodsec-skills:**
- XSS prevention by output context (HTML, attribute, JS, URL, CSS)
- DOM-based XSS dangerous sinks (`innerHTML`, `eval`, `document.write`)
- Trusted Types API enforcement
- Content Security Policy (nonce/hash-based, report-only rollout)
- CSRF defense (SameSite cookies, token patterns, Origin validation)
- Clickjacking defense (`frame-ancestors`, X-Frame-Options)
- Cross-site leaks / XS-Leaks (Fetch Metadata, COOP/COEP/CORP)
- Third-party JavaScript governance (SRI, sandboxed iframes)
- HTTP security headers (HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)

**Priority: HIGH** -- Any team building web UIs needs this guidance.

---

### 1.2 Authentication and Multi-Factor Authentication

**CodeGuard file:** `codeguard-0-authentication-mfa.md` (~877 words)
**OWASP backing:** 8 files (authentication, MFA, password storage, credential stuffing, forgot password, security questions, OAuth2, SAML)

**What's missing from prodsec-skills:**
- Password policy (passphrases, Unicode support, breach corpus checks via k-anonymity)
- Password hashing algorithm parameters (Argon2id: m=19-46 MiB, t=2, p=1; scrypt; bcrypt; PBKDF2)
- Optional peppering with KMS/HSM
- Auth flow hardening (TLS, rate limits, progressive backoff, timing-consistent responses)
- MFA hierarchy (passkeys/WebAuthn preferred > TOTP > SMS discouraged)
- MFA recovery with backup codes
- Federation protocols (OAuth 2.0/OIDC with PKCE, SAML with signature wrapping prevention)
- JWT management (algorithm pinning, denylist/allowlist revocation, DPoP/mTLS sender-constraining)
- Password recovery/reset flows (CSPRNG tokens, anti-enumeration)
- Admin account isolation

**Note:** prodsec-skills covers OAuth 2.1 and OIDC extensively, but only for **agentic system authentication** (MCP clients, inference engines). It does not cover **user-facing authentication** (login forms, password management, MFA).

**Priority: HIGH** -- Fundamental to any application with user accounts.

---

### 1.3 Authorization and Access Control (General)

**CodeGuard file:** `codeguard-0-authorization-access-control.md` (~472 words)
**OWASP backing:** 5 files (authorization, authorization testing automation, IDOR prevention, mass assignment, transaction authorization)

**What's missing from prodsec-skills:**
- Deny-by-default authorization principles
- ABAC/ReBAC vs. RBAC comparison (prodsec-skills has RBAC for MCP only)
- IDOR prevention (user-scoped queries vs. direct object references)
- Mass assignment prevention (DTOs, explicit allow-lists)
- Transaction authorization / step-up auth for sensitive actions
- Authorization testing automation with CI-integrated authorization matrices

**Note:** prodsec-skills has `mcp-server/rbac.md` but it is narrowly scoped to MCP tool invocation. General application authorization patterns are absent.

**Priority: HIGH**

---

### 1.4 C/C++ Memory Safety

**CodeGuard file:** `codeguard-0-safe-c-functions.md` (~1,768 words -- the largest rule)
**OWASP backing:** 3 files (safe C functions, C toolchain hardening, memory/string usage guidelines)

**What's missing from prodsec-skills:**
- Banned function list (gets, strcpy, strcat, sprintf, scanf, strtok, memcpy, memset)
- Safe replacement function signatures (snprintf, fgets, strcpy_s, strcat_s, strtok_r)
- 15+ concrete refactoring code examples
- Compiler hardening flags (-fstack-protector-all, -fsanitize=address, -D_FORTIFY_SOURCE=2)
- Linker hardening (RELRO, noexecstack, NX, ASLR, PIE)
- Code review checklists for C/C++ memory safety
- Common pitfalls with corrections (wrong size parameter, ignoring return values, sizeof on pointers)

**Note:** prodsec-skills has excellent fuzzing skills (AFL++, libFuzzer, cargo-fuzz) and AddressSanitizer guidance, but no **preventive** secure C coding standard.

**Priority: MEDIUM-HIGH** -- Essential for teams writing C/C++.

---

### 1.5 Infrastructure as Code (IaC) Security

**CodeGuard file:** `codeguard-0-iac-security.md` (~849 words)

**What's missing from prodsec-skills:**
- Network security for IaC (no 0.0.0.0/0 to admin ports, VPC flow logs, egress filtering)
- Cloud-specific encryption requirements (S3, Azure Blob, GCS, RDS, EBS)
- IAM hardening (no wildcard permissions, workload identity, IMDSv2)
- Terraform-specific guidance (`sensitive = true`, state file encryption)
- Container/VM image minimization (distroless, pinned base images)
- Multi-cloud coverage (AWS, Azure, GCP specific service names)

**Priority: MEDIUM-HIGH** -- Critical for teams managing cloud infrastructure.

---

### 1.6 Cloud Orchestration / Kubernetes Security

**CodeGuard file:** `codeguard-0-cloud-orchestration-kubernetes.md` (~217 words)
**OWASP backing:** `codeguard-0-kubernetes-security.md`

**What's missing from prodsec-skills:**
- Kubernetes RBAC scoping and namespace separation
- Admission policies (OPA/Gatekeeper/Kyverno)
- Default-deny network policies
- Secrets management with KMS providers
- Node hardening and auto-updates
- Image signature verification in admission
- Break-glass roles with MFA/time-bound approvals
- CIS benchmark verification

**Note:** prodsec-skills covers containerization for MCP servers (`mcp-server/containerization.md`) but not Kubernetes cluster-level security.

**Priority: MEDIUM-HIGH**

---

### 1.7 Database Security

**CodeGuard file:** `codeguard-0-data-storage.md` (~506 words)
**OWASP backing:** `codeguard-0-database-security.md`

**What's missing from prodsec-skills:**
- Backend database isolation (DMZ, firewall rules, no direct thick-client connections)
- Per-platform hardening: SQL Server (xp_cmdshell, CLR), MySQL (FILE privilege, secure_installation), PostgreSQL, MongoDB, Redis
- Dedicated per-app database accounts with least privilege
- Transaction log segregation and encrypted backups
- Credential storage outside web root

**Priority: MEDIUM**

---

### 1.8 Framework-Specific Security Hardening

**CodeGuard file:** `codeguard-0-framework-and-languages.md` (~772 words)
**OWASP backing:** 11 framework-specific deep-dive files

**What's missing from prodsec-skills:**
- **Django:** DEBUG off, SecurityMiddleware, HSTS, CSRF, secret key management
- **Django REST Framework:** authentication/permission classes, object-level authz, throttling
- **Laravel:** APP_DEBUG, cookie encryption, mass assignment with `$request->only()`
- **Symfony:** Twig escaping, CSRF tokens, Doctrine parameterization
- **Ruby on Rails:** 16 dangerous functions to avoid, Devise, protect_from_forgery
- **.NET/ASP.NET Core:** Authorize attributes, DPAPI, anti-forgery
- **Java/JAAS:** PreparedStatement, parameterized logging, LoginModule lifecycle
- **Node.js:** helmet, hpp, rate limiting, event loop monitoring
- **PHP Configuration:** php.ini hardening (expose_php, open_basedir, session cookie flags)

**Priority: MEDIUM** -- Valuable for teams working with specific frameworks.

---

### 1.9 Mobile Application Security

**CodeGuard file:** `codeguard-0-mobile-apps.md` (~691 words)
**OWASP backing:** `codeguard-0-mobile-application-security.md`

**What's missing from prodsec-skills:**
- iOS-specific: Keychain, Secure Enclave, App Attest API, DeviceCheck, Siri/Shortcuts permissions
- Android-specific: Keystore with TEE/StrongBox, ProGuard, Play Integrity API, backup mode
- Certificate pinning for mobile
- Anti-tampering (debug/hook/injection detection, emulator/root/jailbreak detection)
- Biometric authentication patterns
- Code obfuscation and integrity verification

**Priority: MEDIUM** -- Only relevant for teams building mobile apps.

---

### 1.10 Session Management and Cookies

**CodeGuard file:** `codeguard-0-session-management-and-cookies.md` (~542 words)
**OWASP backing:** 3 files (session management, cookie theft mitigation, open redirects)

**What's missing from prodsec-skills:**
- Session ID generation (CSPRNG, 64+ bits entropy)
- Cookie security (Secure/HttpOnly/SameSite, __Host- prefix)
- Session lifecycle (rotation on auth/privilege change)
- Idle/absolute timeouts (2-5 min high-value, 4-8 hrs absolute)
- Cookie theft detection via fingerprinting
- Client-side storage restrictions (no localStorage for tokens)

**Priority: MEDIUM**

---

### 1.11 File Handling and Uploads

**CodeGuard file:** `codeguard-0-file-handling-and-uploads.md` (~495 words)
**OWASP backing:** `codeguard-0-file-upload.md`

**What's missing from prodsec-skills:**
- Extension validation (allow-list, double extension prevention)
- Content-type and magic number validation
- Filename security (UUID generation, character restrictions)
- Image rewriting and CDR (Content Disarm and Reconstruct)
- Storage isolation (outside webroot, application handlers)
- Upload/download size and rate limits

**Priority: MEDIUM**

---

### 1.12 XML and Serialization Security

**CodeGuard file:** `codeguard-0-xml-and-serialization.md` (~448 words)
**OWASP backing:** 3 files (XXE prevention, XML security, deserialization)

**What's missing from prodsec-skills:**
- XXE prevention per platform (Java DocumentBuilderFactory, .NET XmlReaderSettings, Python defusedxml)
- Entity expansion / Billion Laughs attacks
- XSLT/Transformer hardening
- Deserialization safety per language (PHP unserialize, Python pickle, Java ObjectInputStream, .NET BinaryFormatter)
- Safe alternatives per language (json_decode, yaml.safe_load, DataContractSerializer)

**Priority: MEDIUM**

---

### 1.13 Digital Certificate Validation

**CodeGuard file:** `codeguard-1-digital-certificates.md` (~836 words, "always-apply" tier)

**What's missing from prodsec-skills:**
- Automated detection of certificates in code (PEM markers, library function calls)
- Four mandatory checks: expiration, key strength (RSA < 2048, EC < P-256), signature algorithm (MD5/SHA-1), self-signed detection
- Severity classification with templated report messages
- Designed as a plug-and-play AI code review rule

**Priority: MEDIUM**

---

### 1.14 Privacy and Data Protection

**CodeGuard file:** `codeguard-0-privacy-data-protection.md` (~149 words)
**OWASP backing:** `codeguard-0-user-privacy-protection.md`

**What's missing from prodsec-skills:**
- IP address leakage minimization
- User transparency about privacy limitations
- Account enumeration prevention
- Privacy-focused audit trails

**Note:** This is CodeGuard's weakest rule (very brief). Low incremental value.

**Priority: LOW**

---

### 1.15 API and Web Services Security (General)

**CodeGuard file:** `codeguard-0-api-web-services.md` (~595 words)
**OWASP backing:** 5 files (REST security, REST assessment, GraphQL, web service security, SSRF prevention)

**What's missing from prodsec-skills:**
- GraphQL-specific security (depth/complexity limits, disable introspection, batching rate limits)
- SSRF prevention (two threat models: fixed partners vs. arbitrary URLs)
- SOAP/WS XML hardening
- Microservices identity patterns (sidecar PDPs, service identity via mTLS)
- Content-Type enforcement and unknown field rejection

**Note:** prodsec-skills has API gateway skills but focused on AI inference endpoints, not general web API security.

**Priority: MEDIUM-HIGH**

---

### 1.16 DevOps / CI-CD / Container Hardening (General)

**CodeGuard file:** `codeguard-0-devops-ci-cd-containers.md` (~481 words)
**OWASP backing:** 4 files (CI/CD security, Docker security, Node.js Docker, virtual patching)

**What's missing from prodsec-skills:**
- Docker hardening specifics (non-root USER, cap-drop all, no docker.sock mount, read-only rootfs, pin by digest)
- CI/CD pipeline security (protected branches, signed commits, ephemeral runners, security gates)
- Virtual patching lifecycle (WAF/ModSecurity, log-only then enforce, retire after code fix)
- C/C++ compiler/linker hardening flags in CI (PIE, CFI, RELRO, checksec verification)
- Node.js container best practices (npm ci --omit=dev, dumb-init)

**Note:** prodsec-skills has supply chain and pipeline skills but focused on SBOM/provenance/signing, not container runtime hardening.

**Priority: MEDIUM**

---

### 1.17 OWASP Reference Library (83 Deep-Dive Files)

CodeGuard includes 83 detailed OWASP-derived reference files in `sources/owasp/` that provide deep technical guidance on individual topics. These serve as detailed backing material for the consolidated rules. prodsec-skills has no equivalent reference library.

Key categories not covered at all by prodsec-skills:
- **Architecture/Design:** Attack surface analysis, threat modeling, network segmentation, zero-trust architecture, microservices security
- **Legacy:** Legacy application management
- **Browser:** Browser extension vulnerabilities, CSS security
- **Error handling:** Standardized error handling patterns

**Priority: LOW-MEDIUM** -- These are reference material, not operational skills, but provide valuable depth.

---

## Part 2: Where CodeGuard Is More Complete Than prodsec-skills

These are topics where **both repos have coverage**, but CodeGuard's version is **more complete or better**.

### 2.1 Input Validation and Injection Prevention

**Verdict: CodeGuard is significantly more complete**

| Aspect | CodeGuard | prodsec-skills |
|--------|-----------|----------------|
| Injection types | SQL, SOQL, LDAP, OS command, prototype pollution | Generic (MCP-specific) |
| Code examples | Java PreparedStatement, ProcessBuilder | None |
| Language coverage | 14 languages | Language-agnostic |
| Test plan | Static checks, fuzzing, negative tests | None |
| Salesforce/Apex | SOQL/SOSL bind variables, WITH USER_MODE | Not covered |

**prodsec-skills unique value:** Addresses LLM-generated parameters as untrusted input and tool output poisoning -- concerns CodeGuard doesn't cover.

**Recommendation:** Adopt CodeGuard's general injection prevention content. Keep prodsec-skills' MCP-specific trust model guidance as a complement.

---

### 2.2 Crypto Algorithm Selection and Post-Quantum Readiness

**Verdict: CodeGuard fills a gap prodsec-skills doesn't address**

prodsec-skills has excellent crypto **testing and verification** (constant-time analysis, Wycheproof, zeroize-audit, ProVerif formal verification) but has **no guidance on which algorithms to use**. CodeGuard provides:

- Banned algorithms (MD5, RC4, DES, 3DES)
- Deprecated algorithms (SHA-1, AES-CBC, AES-ECB)
- Recommended modern algorithms (AES-GCM, ChaCha20-Poly1305, X25519)
- Post-quantum readiness (ML-KEM-768 hybrid, ML-DSA for HSM)
- OpenSSL deprecated API migration guide
- Protocol version enforcement (TLS 1.3, IKEv2)

**Recommendation:** Add an algorithm selection / crypto policy skill to prodsec-skills. The existing crypto testing skills assume the algorithm choice is already made correctly.

---

### 2.3 Logging (Detection and Alerting)

**Verdict: Complementary, but CodeGuard is stronger on detection use cases**

prodsec-skills' logging skills provide better concrete implementation guidance (JSON log format examples, MCP-specific audit fields). But CodeGuard covers areas prodsec-skills misses entirely:

- Detection patterns (auth anomalies, credential stuffing, impossible travel, privilege changes, SSRF indicators, data exfiltration)
- Alert tuning, runbooks, on-call coverage
- Privacy/compliance (data classification, retention/deletion, user-linked log deletion)
- Validation methodology (redaction unit tests, periodic PII audits, tabletop exercises)
- Log storage isolation and integrity

**Recommendation:** Enrich prodsec-skills logging skills with detection/alerting patterns and privacy controls.

---

### 2.4 Supply Chain Security (Governance and Incident Response)

**Verdict: Complementary, but CodeGuard covers governance prodsec-skills misses**

prodsec-skills is stronger on operational tooling (SBOM generation with syft, risk auditing methodology, response timelines). CodeGuard covers governance areas prodsec-skills doesn't:

- Package hygiene (npm ci vs install, lockfile consistency, install script auditing)
- Typosquatting and protestware defense
- Hermetic builds (no network in compile/packaging)
- `.npmrc` scoped registry configuration
- Publisher account 2FA
- Incident response playbook (rapid rollback, isolate compromised packages, throttle rollouts)
- "Minimize dependency footprint" as a principle

**Recommendation:** Add governance/hygiene and incident response content to prodsec-skills supply chain skills.

---

## Part 3: Summary and Prioritized Recommendations

### Priority Matrix

| Priority | Gap | Effort to Address | Impact |
|----------|-----|-------------------|--------|
| **HIGH** | Client-side web security (XSS, CSRF, CSP) | Medium -- adapt CodeGuard + OWASP sources | Broad applicability |
| **HIGH** | Authentication and MFA (user-facing) | Medium -- new skill needed | Fundamental to most apps |
| **HIGH** | Authorization and access control (general) | Low-Medium -- expand beyond MCP RBAC | Fundamental to most apps |
| **HIGH** | API/web services security (GraphQL, SSRF, SOAP) | Medium -- new skill needed | Broad applicability |
| **MEDIUM-HIGH** | C/C++ memory safety coding standard | Low -- adapt CodeGuard directly | Critical for C/C++ teams |
| **MEDIUM-HIGH** | IaC security (Terraform, CloudFormation, cloud) | Medium -- new skill needed | Cloud-native teams |
| **MEDIUM-HIGH** | Kubernetes cluster security | Low-Medium -- expand containerization skill | Cloud-native teams |
| **MEDIUM** | Database security (platform-specific hardening) | Low-Medium -- new skill needed | Teams with direct DB access |
| **MEDIUM** | Framework-specific guides (Django, Rails, etc.) | Medium -- 8+ sub-skills needed | Language-specific teams |
| **MEDIUM** | Session management and cookies | Low -- new skill needed | Web application teams |
| **MEDIUM** | File handling and uploads | Low -- new skill needed | Web application teams |
| **MEDIUM** | XML and serialization / deserialization | Low -- new skill needed | Enterprise/Java/.NET teams |
| **MEDIUM** | Digital certificate validation | Low -- adapt CodeGuard directly | Broad applicability |
| **MEDIUM** | DevOps / CI-CD / container hardening | Low-Medium -- expand existing skills | All teams |
| **MEDIUM** | Crypto algorithm selection / PQC policy | Low -- new skill needed | Complements existing crypto skills |
| **LOW-MEDIUM** | Input validation / injection (general) | Low -- new skill, keep MCP-specific | Broad applicability |
| **LOW-MEDIUM** | Mobile application security | Medium -- new skill | Mobile teams only |
| **LOW-MEDIUM** | Logging detection/alerting patterns | Low -- enrich existing skills | SOC/monitoring teams |
| **LOW** | Privacy and data protection | Low -- brief, low value | Incremental |

### What prodsec-skills Has That CodeGuard Does NOT

For completeness, prodsec-skills has extensive coverage in areas CodeGuard lacks entirely:

- **Fuzzing methodology** (12 skills: AFL++, libFuzzer, cargo-fuzz, Atheris, LibAFL, ruzzy, OSS-Fuzz, harness writing, coverage analysis, dictionaries, obstacle removal)
- **Static analysis tooling** (5 skills: CodeQL, Semgrep, SARIF parsing, custom rule creation)
- **Security audit workflows** (4 skills: context building, differential review, false positive checking, variant analysis)
- **AI/Agentic infrastructure** (63 skills: agent identity, MCP server/client security, inference engine security, model registry, RAG, guardrails, eval sandbox)
- **Cryptographic verification** (constant-time analysis/testing, Wycheproof, formal verification with ProVerif)
- **SDLC process** (skills for orientation, DAST, SAST triage)
- **Developer tooling** (property-based testing, devcontainers, git cleanup, modern Python)
- **Experimental assessment methodologies** (13 skills: adversarial finding review, binary assessment, threat modeling gate, finding validation pipeline)

---

## Appendix: File-Level Mapping

### CodeGuard Rules with No prodsec-skills Equivalent

| CodeGuard Rule | Topic | prodsec-skills Status |
|---|---|---|
| `codeguard-0-authentication-mfa.md` | User auth, MFA, password hashing | **ABSENT** |
| `codeguard-0-authorization-access-control.md` | General authz, IDOR, mass assignment | **ABSENT** (MCP RBAC only) |
| `codeguard-0-client-side-web-security.md` | XSS, CSRF, CSP, clickjacking | **ABSENT** |
| `codeguard-0-cloud-orchestration-kubernetes.md` | Kubernetes hardening | **ABSENT** |
| `codeguard-0-data-storage.md` | Database security | **ABSENT** |
| `codeguard-0-file-handling-and-uploads.md` | File upload security | **ABSENT** |
| `codeguard-0-framework-and-languages.md` | Framework hardening (8 frameworks) | **ABSENT** |
| `codeguard-0-iac-security.md` | IaC / cloud security | **ABSENT** |
| `codeguard-0-mobile-apps.md` | iOS/Android security | **ABSENT** |
| `codeguard-0-privacy-data-protection.md` | Privacy, data protection | **ABSENT** |
| `codeguard-0-safe-c-functions.md` | C/C++ memory safety | **ABSENT** |
| `codeguard-0-session-management-and-cookies.md` | Sessions, cookies | **ABSENT** |
| `codeguard-0-xml-and-serialization.md` | XXE, deserialization | **ABSENT** |
| `codeguard-0-api-web-services.md` | REST, GraphQL, SOAP, SSRF | **ABSENT** (API gateway is AI-focused) |
| `codeguard-0-devops-ci-cd-containers.md` | Docker, CI/CD, virtual patching | **PARTIAL** (supply chain only) |
| `codeguard-1-digital-certificates.md` | X.509 validation in code | **ABSENT** |
| `codeguard-0-additional-cryptography.md` | Crypto selection, TLS, HSTS | **ABSENT** (testing only) |

### CodeGuard Rules with prodsec-skills Overlap

| CodeGuard Rule | prodsec-skills Equivalent | Verdict |
|---|---|---|
| `codeguard-1-hardcoded-credentials.md` | `experimental/secrets-detection-patterns.md` | prodsec BETTER |
| `codeguard-1-crypto-algorithms.md` | `crypto/*` (7 skills) | COMPLEMENTARY |
| `codeguard-0-mcp-security.md` | `mcp-server/*` + `mcp-client/*` (23 skills) | COMPLEMENTARY (prodsec deeper) |
| `codeguard-0-supply-chain-security.md` | `supply-chain/*` (5 skills) | COMPLEMENTARY |
| `codeguard-0-input-validation-injection.md` | `mcp-server/input-output-sanitization.md` | CodeGuard BETTER (general) |
| `codeguard-0-logging.md` | `mcp-server/logging-and-observability.md` + `external-data-source/logging.md` | COMPLEMENTARY |
