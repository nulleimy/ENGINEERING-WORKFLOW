---
id: EW-GOV-001
title: Engineering Constitution
status: proposed
owner: Eimy Herrer and Johny
version: 0.7.0-rc.1
last-reviewed: 2026-07-26
---

# Engineering Constitution

This constitution defines the concise non-negotiable invariants of the engineering system. It is subordinate to the exact canonical technical operating mode and the Product, Decision and Execution Constitution. Procedures and tools may change; constitutional meaning changes only through explicit approval and a versioned governance decision.

## Constitutional relationship

- `WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md` governs technical truth, technical work modes, protected operations and technical Definition of Done.
- `PRODUCT_DECISION_EXECUTION_CONSTITUTION.md` governs product value, decision classes, realization discipline and readiness beyond code completion.
- `CONSTITUTIONAL_AUTHORITY.json` binds both documents to exact hashes and defines fail-closed conflict handling.
- This document provides the concise project-level invariant summary and may not weaken either higher constitution.

## Invariants

1. **Truth over appearance.** `IMPLEMENTED`, `VERIFIED`, `RELEASED`, `OPERATING` and `COMPLETE` must describe evidence-backed states.
2. **Clear ownership.** Every product, change, release, risk acceptance and operational service has a named accountable owner or authority.
3. **One canonical current state.** Critical facts must have one declared canonical location and may not depend only on chat, memory or one device.
4. **Portable control records.** Project, work, decision, baseline, verification, release and incident records must remain exportable in open formats.
5. **Small reversible slices.** Work is decomposed into the smallest independently valuable, testable and recoverable change.
6. **Risk-proportional control.** Low-risk work is fast; critical work is independently reviewed, rehearsed and evidence-rich.
7. **Automation over repeated manual judgment.** Deterministic checks are automated and made part of the golden path.
8. **Secure by default.** External inputs, dependencies, identities, agents and generated outputs are untrusted until validated.
9. **Separation of creation and acceptance.** R2/R3 work is not accepted solely by its author.
10. **Reproducible and attributable outputs.** Important artifacts identify inputs, method, environment, producer and integrity.
11. **Recovery is a product capability.** Critical systems have tested restore, rollback or safe-forward procedures.
12. **Documentation is part of the product.** It is current, owned, testable where possible and updated with the change.
13. **Tools are adapters.** Git, GitHub, Drive, CI platforms, cloud providers and AI models can be replaced without redefining the operating model.
14. **No hidden production state.** Manual emergency changes must be captured, reviewed and reconciled into the canonical state.
15. **No unauthorized reuse.** Code, data, models, designs and documents retain explicit provenance, license and ownership.
16. **Continuous improvement targets constraints.** Metrics remove bottlenecks and rework; they do not rank people or reward activity volume.
17. **No protected operation without explicit authority.** A decision record does not itself authorize merge, release, license change, destructive action or production change.

## Authority order

1. law, safety, binding contractual and platform obligations;
2. `WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md`;
3. `PRODUCT_DECISION_EXECUTION_CONSTITUTION.md`;
4. explicit authorized operator mandate;
5. this constitution and accepted project governance records;
6. current authorized Work Package and accepted decision records;
7. working documentation, tool defaults and personal preference.

An unresolved conflict is `BLOCKED`. At equal authority the safer and more evidence-demanding applicable requirement wins.

## Amendment

A constitutional amendment requires:

- an ADR describing the deficiency and alternatives;
- impact, compatibility and migration analysis;
- explicit approval by Eimy and Johny or their formally assigned successor authorities;
- a major or minor version change according to compatibility impact;
- updated integrity hashes and authority index when constitutional content changes;
- a recorded adoption plan for affected projects.
