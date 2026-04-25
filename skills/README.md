# Skills Index

128 production-ready security skills. All skills are tool-agnostic markdown — they work with Claude Code, Cursor, Copilot, or any assistant that can read files.

## Categories

| Category | Skills | Purpose |
|----------|--------|---------|
| [`secure_development/`](#secure_development) | 103 | Building secure software — AI/agentic infrastructure, cryptography, supply chain, security principles, technology-specific hardening |
| [`security_testing/`](#security_testing) | 17 | Finding vulnerabilities — fuzzing and static analysis |
| [`security_auditing/`](#security_auditing) | 4 | Security review workflows |
| [`developer_tooling/`](#developer_tooling) | 4 | General-purpose development tooling |

---

## `secure_development/`

See [`secure_development/README.md`](secure_development/README.md) for the full index. Summary by subcategory:

| Subcategory | Skills | Focus |
|-------------|--------|-------|
| `agent/` | 3 | Agent identity, agent-to-agent auth, agent-to-MCP-server auth |
| `api-gateway/` | 4 | Authentication enforcement, routing, rate limiting, request validation |
| `api-keys/` | 1 | Avoiding API keys; prefer IdP-issued tokens |
| `authorization-server/` | 4 | OAuth 2.1, dynamic client registration, discovery |
| `crypto/` | 8 | Constant-time analysis, protocol diagramming, zeroization, test vectors, algorithm selection and post-quantum readiness |
| `eval-sandbox/` | 1 | Output validation in isolated sandboxes |
| `external-data-source/` | 6 | Auth, authz, encryption, logging, network ACLs, Redis/ElastiCache for external connections |
| `guardrails/` | 1 | Bidirectional prompt and output filtering |
| `inference-engine/` | 7 | Isolation, JWT enforcement, model scanning/signing, OIDC, token lifecycle |
| `large-language-model/` | 3 | File protection, prompt injection mitigation, third-party model security |
| `mcp-client/` | 5 | OAuth client metadata, discovery, dynamic registration, scopes |
| `mcp-server/` | 18 | Hardening, OAuth 2.1, RBAC, sanitization, token handling, containerization |
| `model-registry/` | 5 | Admin security, logging, model scanning/signing, secure storage |
| `rag-system/` | 1 | Secure storage for RAG/vector/knowledge data |
| `secure-config/` | 5 | Insecure defaults, API sharp edges, agentic CI/CD action auditing, Apache Camel security, build YAML misconfiguration |
| `spiffe-spire/` | 1 | SPIFFE/SPIRE + mTLS for service-to-service auth |
| `supply-chain/` | 5 | Dependency risk auditing, SBOM/provenance, secure pipelines, software signing |
| `security-principles/` | 5 | Defense in depth, least privilege and mediation, secure by design (SD3), simplicity and isolation, transparency and usability |
| `cloud-infrastructure/` | 2 | AWS security baselines (IAM, VPC, CloudTrail, RDS, KMS), general database security |
| `kubernetes/` | 4 | Operator RBAC, OpenShift SCCs, Helm chart security, container hardening |
| `languages/` | 3 | Go secure coding, compiler hardening (flags, sanitizers), C/C++ memory and string safety |
| `messaging/` | 2 | Kafka/AMQ Streams (TLS, SASL, ACLs), MQTT (auth, topic ACLs, payload encryption) |
| `web-security/` | 9 | Web application security, HTTP security headers, React XSS prevention, GraphQL hardening, client-side security, input validation and injection, session management, file uploads, XML and serialization |

---

## `security_testing/`

### `security_testing/fuzzing/` — 12 skills

| Skill | Description |
|-------|-------------|
| [`address-sanitizer.md`](security_testing/fuzzing/address-sanitizer.md) | Detect memory errors (buffer overflows, use-after-free) during C/C++ fuzzing with ASan |
| [`aflpp.md`](security_testing/fuzzing/aflpp.md) | Multi-core coverage-guided fuzzing of C/C++ with AFL++ |
| [`atheris.md`](security_testing/fuzzing/atheris.md) | Coverage-guided fuzzing of pure Python and Python C extensions |
| [`cargo-fuzz.md`](security_testing/fuzzing/cargo-fuzz.md) | Fuzzing Rust projects with cargo-fuzz and a libFuzzer backend |
| [`coverage-analysis.md`](security_testing/fuzzing/coverage-analysis.md) | Measuring code coverage to assess harness effectiveness and identify blockers |
| [`fuzzing-dictionary.md`](security_testing/fuzzing/fuzzing-dictionary.md) | Building domain-specific token dictionaries for parsers, protocols, and formats |
| [`fuzzing-obstacles.md`](security_testing/fuzzing/fuzzing-obstacles.md) | Patching checksums, global state, and other barriers to fuzzer progress |
| [`harness-writing.md`](security_testing/fuzzing/harness-writing.md) | Writing effective fuzz targets across languages |
| [`libafl.md`](security_testing/fuzzing/libafl.md) | Building custom fuzzers with LibAFL's modular fuzzing library |
| [`libfuzzer.md`](security_testing/fuzzing/libfuzzer.md) | Coverage-guided fuzzing of C/C++ code compiled with Clang |
| [`ossfuzz.md`](security_testing/fuzzing/ossfuzz.md) | Enrolling open source projects in OSS-Fuzz for continuous fuzzing |
| [`ruzzy.md`](security_testing/fuzzing/ruzzy.md) | Coverage-guided fuzzing of Ruby code and Ruby C extensions |

### `security_testing/static-analysis/` — 5 skills

| Skill | Description |
|-------|-------------|
| [`codeql.md`](security_testing/static-analysis/codeql.md) | Interprocedural data flow and taint tracking analysis with CodeQL |
| [`sarif-parsing.md`](security_testing/static-analysis/sarif-parsing.md) | Parsing, filtering, and deduplicating SARIF output from any scanner |
| [`semgrep.md`](security_testing/static-analysis/semgrep.md) | Running Semgrep across a codebase with parallel subagents |
| [`semgrep-rule-creator.md`](security_testing/static-analysis/semgrep-rule-creator.md) | Writing custom Semgrep rules for security vulnerabilities and bug patterns |
| [`semgrep-rule-variant-creator.md`](security_testing/static-analysis/semgrep-rule-variant-creator.md) | Porting existing Semgrep rules to new target languages |

---

## `security_auditing/`

### `security_auditing/audit-workflow/` — 4 skills

| Skill | Description |
|-------|-------------|
| [`audit-context-building.md`](security_auditing/audit-workflow/audit-context-building.md) | Line-by-line codebase analysis to build deep architectural context before a security review |
| [`differential-review.md`](security_auditing/audit-workflow/differential-review.md) | Security-focused review of PRs, commits, and diffs with blast radius analysis |
| [`fp-check.md`](security_auditing/audit-workflow/fp-check.md) | Systematic verification of suspected bugs to eliminate false positives |
| [`variant-analysis.md`](security_auditing/audit-workflow/variant-analysis.md) | Finding related vulnerabilities across a codebase after discovering an initial issue |

---

## `developer_tooling/`

### `developer_tooling/testing/` — 1 skill

| Skill | Description |
|-------|-------------|
| [`property-based-testing.md`](developer_tooling/testing/property-based-testing.md) | Property-based testing with Hypothesis (Python), proptest (Rust), and others |

### `developer_tooling/tooling/` — 3 skills

| Skill | Description |
|-------|-------------|
| [`devcontainer-setup.md`](developer_tooling/tooling/devcontainer-setup.md) | Adding Dev Container support with language-specific tooling and persistent volumes |
| [`git-cleanup.md`](developer_tooling/tooling/git-cleanup.md) | Safely analyzing and cleaning up merged, squash-merged, and stale branches |
| [`modern-python.md`](developer_tooling/tooling/modern-python.md) | Configuring Python projects with uv, ruff, and ty |
