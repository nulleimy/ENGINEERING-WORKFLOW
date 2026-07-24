---
id: EW-OPS-001
title: Engineering Lifecycle
status: proposed
owner: Eimy Herrer and Johny
version: 0.1.0
last-reviewed: 2026-07-24
---

# Engineering Lifecycle

## Flow

```text
DISCOVER → FRAME → DESIGN → SLICE → BUILD → VERIFY → ACCEPT → RELEASE → OPERATE → LEARN
```

### Discover
Validate the problem, user, constraints and existing alternatives.

### Frame
Create a clear current state, target state, success criteria, ownership, risk and boundary.

### Design
Choose the simplest viable architecture. Record significant, costly or difficult-to-reverse decisions.

### Slice
Produce the smallest independently valuable vertical change with a clear acceptance test.

### Build
Implement only authorized scope. Keep changes deterministic, observable and recoverable.

### Verify
Use the risk-appropriate quality gate and preserve results.

### Accept
The accountable authority confirms outcome, evidence and residual risk.

### Release
Create an identified, attributable and recoverable release.

### Operate
Observe real behavior, reliability, security and cost.

### Learn
Review throughput, failures, rework, incidents, documentation gaps and manual friction. Improve the largest constraint.

## Work-in-progress limit

Default: one active implementation package per person and product area. Exceptions require an explicit reason. Finishing and integrating work takes priority over starting parallel variants.
