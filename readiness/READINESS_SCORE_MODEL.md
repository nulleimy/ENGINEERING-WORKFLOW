---
id: EW-READINESS-001
title: World-Class Readiness Score Model
status: proposed
owner: Eimy Herrer and Johny
version: 0.4.0-rc.1
last-reviewed: 2026-07-24
---

# World-Class Readiness Score Model

## Intent

The scorecard converts broad claims such as “professional”, “secure” or “world class” into a repeatable assessment tied to evidence, outcomes and ownership.

## Domain score

Each domain is scored from `0.0` to `10.0` using five dimensions of equal maximum value:

| Dimension | Maximum | Question |
|---|---:|---|
| Definition | 2.0 | Are outcomes, boundaries and owners explicit? |
| Implementation | 2.0 | Do required mechanisms actually exist? |
| Automation | 2.0 | Are repeated deterministic controls enforced automatically? |
| Evidence | 2.0 | Is current, attributable and integrity-verifiable evidence available? |
| Operational outcome | 2.0 | Has the capability worked under realistic use, recovery or independent review? |

A dimension cannot receive full credit from intention or documentation alone.

## Evidence maturity

The domain score is capped by evidence maturity:

```text
UNKNOWN                 → no defensible numeric score
DESIGNED                → maximum 5.0
IMPLEMENTED             → maximum 7.0
VERIFIED                → maximum 8.5
MEASURED                 → maximum 9.5
INDEPENDENTLY_REVIEWED  → maximum 10.0
```

## Minimum 9.0 rule

A domain reaches 9.0 only when:

- the capability is implemented;
- relevant controls are automated or an explicit reason explains why automation is unsafe;
- verification evidence is current;
- a realistic pilot, production measurement, recovery exercise or independent assessment exists;
- open critical findings are zero;
- residual risks are explicitly accepted;
- the score has a named acceptance authority.

## No-average masking

An overall arithmetic average may be reported for trend analysis, but it is not a readiness decision. `WORLD_CLASS_READY` requires every applicable domain score to meet the threshold independently.

## Score freshness

Every domain declares an assessment date and evidence expiry. An expired score becomes `UNKNOWN` until reassessed.

## Honest baseline

Initial scores describe the current evidence state, not the desired reputation. Missing operational history is recorded as a gap rather than estimated optimistically.
