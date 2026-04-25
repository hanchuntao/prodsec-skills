# prodsec-skills Constitution

## Purpose

This constitution establishes the guiding principles and end-to-end security processes for the prodsec-skills project. It is intentionally short and high-level; repository operations live in AGENTS.md, and significant decisions in ADRs.

## Guiding principles

1. **Security everywhere.** Skills apply across the entire lifecycle — during development, in CI/CD checks, at review, and in production operations. Every skill should reduce the distance between intent and a secure outcome, wherever it is invoked.
2. **Automation-first, humans where it matters.** Changes that satisfy policy checks should flow through rule-based automation without human intervention. Agentic AI is the default whenever interaction is needed — triaging, debugging, implementing, analyzing. Human review is reserved for decisions that genuinely require human judgment.
3. **Tool-agnostic.** Skills target all AI assistants equally. No skill may contain syntax, configuration, or directives specific to a single tool or vendor.
4. **Upstream-first.** Respect open-source community norms. Follow each upstream project's AI contribution policy, and prefer upstreaming fixes over carrying private patches.
5. **Transparency and provenance.** Every skill must trace back to an accountable author and, when adapted from external sources, must record the origin commit and license.
6. **Risk-proportionate.** The higher the risk, the more urgently and visibly the accountable person must be alerted. Guidance should be calibrated to actual impact, not applied uniformly regardless of context.

## Secure development lifecycle

Skills are the connective tissue of an end-to-end secure development lifecycle. Each phase has a clear security mandate:

1. **Design.** Threat-model before code exists. Skills encode the threat patterns, trust boundaries, and architectural constraints that agents surface during design discussions.
2. **Develop.** Apply security guidance as code is written. Agents invoke skills in real time to steer implementation toward secure defaults — cryptography choices, input validation, dependency selection.
3. **Test.** Validate security properties automatically. Skills drive fuzzing harnesses, static-analysis rulesets, and property-based tests that run without manual intervention.
4. **Check.** Evaluate policy at merge and release boundaries. When a skill identifies a risk, alert the accountable person with severity and context proportionate to the impact so they can make an informed decision.
5. **Operate.** Feed production signals back into skills. Incident findings, CVE patterns, and post-mortem lessons refine existing skills or spawn new ones, closing the loop.

## Security checks and accountability

- **Policy-as-code.** Security requirements expressed in skills should be mechanically evaluable wherever possible — in CI, in pre-commit hooks, in deployment pipelines.
- **Alert hierarchy.** Skills declare their severity: *informational* (log for awareness), *warning* (notify the responsible engineer), or *critical* (escalate immediately to the accountable decision-maker). The appropriate level follows the risk-proportionate principle.
- **Continuous validation.** Checks are not one-time. As skills evolve, previously passing code may need re-evaluation. Automation should support retroactive scanning when skills are updated.

## Feedback and continuous improvement

- **Incidents inform skills.** Every significant vulnerability or security incident should be assessed for whether a new or updated skill would have prevented or detected it earlier.
- **Metrics drive priority.** Track which skills fire most often, which alerts escalate most frequently, and where false positives erode trust. Use this data to prioritize skill refinement.
- **Skills are living documents.** No skill is final. The landscape of threats, tooling, and best practices changes — skills must be revisited and updated as the context evolves.

## Conflict resolution

When two or more skills offer contradictory recommendations:

1. **Specificity wins.** A skill scoped to a narrower context (e.g., a particular protocol or threat model) takes precedence over a more general skill.
2. **Fail secure.** When specificity is equal, the stricter (more security-conservative) recommendation prevails.
3. **Escalate.** If the conflict cannot be resolved by the rules above, the project maintainers decide — documented as an ADR if the resolution sets precedent.