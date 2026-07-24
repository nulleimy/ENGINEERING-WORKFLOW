---
id: EW-GOV-001
title: Engineering Constitution
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Engineering Constitution

This constitution defines the non-negotiable invariants of the engineering system. Procedures and tools may change; these invariants may only change through explicit joint approval and a versioned governance decision.

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
16. **Continuous improvement targets constraints.** Metrics are used to remove bottlenecks and rework, never to rank people or reward activity volume.

## Authority order

1. law, safety and binding contractual obligations;
2. this constitution and approved project constitution;
3. accepted security and compliance controls;
4. current authorized work package;
5. project documentation;
6. tool defaults and personal preference.

## Amendment

A constitutional amendment requires:

- an ADR describing the deficiency and alternatives;
- impact and migration analysis;
- approval by Eimy and Johny;
- a major or minor version change according to compatibility impact;
- a recorded adoption plan for affected projects.
