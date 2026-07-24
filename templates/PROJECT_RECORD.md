---
id: EW-TPL-001
title: Template — Project Record
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Template — Project Record

```yaml
project:
  id: <unique-id>
  name: <name>
  status: concept | discovery | defined | building | validating | operating | maintenance | retired | archived
  product_owner: <person-or-role>
  technical_owner: <person-or-role>

purpose:
  problem: <problem>
  target_users: []
  value_proposition: <value>
  exclusions: []

control:
  canonical_location: <URI-or-path>
  engineering_standard_version: <version>
  current_baseline: <baseline-id>
  current_release: <release-id-or-null>

risk:
  classification: R0 | R1 | R2 | R3
  known_risks: []
```
