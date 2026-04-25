# Secure Development skills

103 tool-agnostic secure development skills organized by category, covering **AI/agentic infrastructure security**, **code-level secure configuration**, **security design principles**, and **technology-specific hardening**.

## Usage

Reference any skill by path in your assistant prompt:

```
Using `skills/secure_development/mcp-server/input-output-sanitization.md`: review this MCP server for injection risks.
```

Skills follow the same format as the rest of `skills/` — YAML front matter (`name`, `description`) plus markdown body. They work with any assistant (Cursor, Claude Code, Copilot, etc.).

Teams copying this collection can delete category folders that are not relevant to their project.

## Categories

### AI and agentic infrastructure security

| Category | Skills | Focus |
|----------|--------|-------|
| [`agent/`](agent/) | 3 | Agent identity, agent-to-agent auth, agent-to-MCP-server auth (SPIFFE/mTLS) |
| [`api-gateway/`](api-gateway/) | 4 | Authentication enforcement, routing, rate limiting, request validation for AI endpoints |
| [`api-keys/`](api-keys/) | 1 | Avoiding API keys in production; prefer IdP-issued tokens |
| [`authorization-server/`](authorization-server/) | 4 | OAuth 2.1 implementation, dynamic client registration, discovery for MCP |
| [`eval-sandbox/`](eval-sandbox/) | 1 | Output validation in isolated sandboxes before use |
| [`external-data-source/`](external-data-source/) | 6 | Auth, authz, encryption, logging, network ACLs, Redis/ElastiCache for external data connections |
| [`guardrails/`](guardrails/) | 1 | Bidirectional filtering of prompts and model outputs |
| [`inference-engine/`](inference-engine/) | 7 | Isolation, JWT enforcement, model scanning/signing, OIDC, token lifecycle |
| [`large-language-model/`](large-language-model/) | 3 | File protection, prompt injection mitigation, third-party model security |
| [`mcp-client/`](mcp-client/) | 5 | OAuth client metadata, discovery, dynamic registration, scopes, protected resources |
| [`mcp-server/`](mcp-server/) | 18 | Hardening (local/remote), OAuth 2.1 resource server, RBAC, input/output sanitization, token handling, containerization, tool injection prevention |
| [`model-registry/`](model-registry/) | 5 | Admin security, logging, model scanning/signing, secure storage |
| [`rag-system/`](rag-system/) | 1 | Secure storage for RAG/vector/knowledge data |
| [`spiffe-spire/`](spiffe-spire/) | 1 | SPIFFE/SPIRE + mTLS for service-to-service authentication |

### Code-level secure configuration and cryptography

| Category | Skills | Focus |
|----------|--------|-------|
| [`crypto/`](crypto/) | 8 | Constant-time analysis, protocol diagramming, zeroization audit, test vectors (Wycheproof), algorithm selection and post-quantum readiness |
| [`secure-config/`](secure-config/) | 5 | Insecure defaults, API sharp edges, agentic CI/CD action auditing, Apache Camel security, build YAML misconfiguration (GitLab CI, Tekton, Containerfile) |
| [`supply-chain/`](supply-chain/) | 5 | Dependency risk auditing, SBOM/provenance, secure pipelines, software signing, vulnerability management |

### Security design principles

| Category | Skills | Focus |
|----------|--------|-------|
| [`security-principles/`](security-principles/) | 5 | Defense in depth, least privilege and mediation, secure by design (SD3), simplicity and isolation, transparency and usability |

### Technology-specific security

| Category | Skills | Focus |
|----------|--------|-------|
| [`cloud-infrastructure/`](cloud-infrastructure/) | 2 | AWS security baselines (IAM, VPC, CloudTrail, RDS, KMS), general database security |
| [`kubernetes/`](kubernetes/) | 4 | Operator RBAC, OpenShift SCCs, Helm chart security, container hardening |
| [`languages/`](languages/) | 3 | Go secure coding, compiler hardening (flags, sanitizers), C/C++ memory and string safety |
| [`messaging/`](messaging/) | 2 | Kafka/AMQ Streams (TLS, SASL, ACLs), MQTT (auth, topic ACLs, payload encryption) |
| [`web-security/`](web-security/) | 9 | Web application security, HTTP security headers, React XSS prevention, GraphQL hardening, client-side security (XSS/CSRF/CSP), input validation and injection, session management, file upload security, XML and serialization hardening |

## Relationship to `skills/product-security.md`

[`skills/product-security.md`](../product-security.md) provides a **posture and compliance** review (CVEs, SBOMs, licenses, images, supply chain). When that review identifies a dimension needing deeper investigation, the skills here provide specialized analysis:

| Product Security dimension | Relevant skills |
|---------------------------|--------------------------|
| Known vulnerabilities | `../security_testing/static-analysis/`, `../security_auditing/audit-workflow/variant-analysis.md` |
| Supply chain integrity | `supply-chain/`, `secure-config/agentic-actions-auditor.md` |
| Cryptographic compliance | `crypto/` |
| Container / image security | `secure-config/insecure-defaults.md`, `mcp-server/containerization.md` |
| Code-level review | `../security_auditing/audit-workflow/` |
| Testing gaps | `../security_testing/fuzzing/`, `../developer_tooling/testing/` |
| AI/agentic security | `agent/`, `mcp-server/`, `mcp-client/`, `inference-engine/`, `guardrails/`, `large-language-model/` |

## Provenance

### AI/agentic infrastructure security skills (63 skills)

- **Source**: Internal security skills repository
- **Upstream commit**: `5d104a5863943aa0ac19b13ca5de7f191d7b7214` (2026-03-03)
- **Format**: Already tool-agnostic markdown; copied with directory names converted to kebab-case

### Code-level secure configuration and cryptography skills (15 skills)

- **Source**: Partly Trail of Bits Skills Marketplace ([trailofbits/skills](https://github.com/trailofbits/skills)), partly original
- **Trail of Bits upstream commit**: `88947f59f1032c1f4d84d6fab244acff6f014728` (2026-04-07)
- **Conversion**: Claude Code plugin format → flat tool-agnostic markdown; `plugin.json`, `hooks/`, and `allowed-tools` dropped; reference docs inlined or pointed to upstream
- **License**: Trail of Bits skills are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). This adaptation maintains the same license.

**Note:** Security auditing, security testing, and developer tooling skills originally in this collection have been moved to their own top-level categories: `security_auditing/`, `security_testing/`, and `developer_tooling/`.

### Traditional application security skills (8 skills)

- **Source**: CoSAI [Project CodeGuard](https://github.com/cosai-oasis/project-codeguard) (v1.3.1)
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Conversion**: CodeGuard consolidated rules adapted to individual skill format (YAML frontmatter, tool-agnostic markdown). OWASP backing sources used for enrichment. `build-yaml-misconfiguration` is a new skill authored for GitLab CI and Tekton, not a direct CodeGuard import.
- **Skills**: `web-security/client-side-security`, `web-security/file-handling-uploads`, `web-security/input-validation-injection`, `web-security/session-management-cookies`, `web-security/xml-serialization-security`, `languages/safe-c-functions`, `crypto/algorithm-selection`, `secure-config/build-yaml-misconfiguration`
- **Gap analysis**: See `docs/codeguard-gap-analysis.md` for import decisions, skipped items, and items deferred for future skills.

## Contributing

When updating these skills, follow the format conventions in `skills/` (see [`CONTRIBUTING.md`](../../CONTRIBUTING.md)).
