#!/usr/bin/env python3
"""Validate readiness scores, evidence maturity caps and gap coverage."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DOMAINS = {
    "governance", "product", "architecture", "delivery", "quality", "security",
    "supply-chain", "platform", "release", "operations", "documentation",
    "ai-engineering", "compliance", "incident",
}
CAPS = {
    "UNKNOWN": None,
    "DESIGNED": 5.0,
    "IMPLEMENTED": 7.0,
    "VERIFIED": 8.5,
    "MEASURED": 9.5,
    "INDEPENDENTLY_REVIEWED": 10.0,
}
VALID_STATES = {"UNASSESSED", "GAP_CLOSURE", "CANDIDATE", "WORLD_CLASS_READY", "DEGRADED", "RETIRED"}
VALID_GAP_STATES = {"OPEN", "IN_PROGRESS", "BLOCKED", "CLOSED"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}


def load(path: str) -> dict:
    data = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: root must be object")
    return data


def main() -> int:
    errors: list[str] = []
    scorecard = load("readiness/domain-scorecard.json")
    gaps_doc = load("readiness/gap-register.json")

    threshold = scorecard.get("readiness_threshold")
    if threshold != 9.0:
        errors.append("readiness threshold must be exactly 9.0")
    if scorecard.get("overall_state") not in VALID_STATES:
        errors.append("invalid overall_state")

    domains = scorecard.get("domains", [])
    ids = [item.get("id") for item in domains]
    if set(ids) != EXPECTED_DOMAINS or len(ids) != len(EXPECTED_DOMAINS):
        errors.append("scorecard must define exactly the 14 canonical domains")

    gaps = gaps_doc.get("gaps", [])
    gap_ids = [item.get("id") for item in gaps]
    if len(gap_ids) != len(set(gap_ids)):
        errors.append("gap IDs are not unique")
    known_gaps = set(gap_ids)

    for gap in gaps:
        gap_id = gap.get("id")
        if gap.get("domain") not in EXPECTED_DOMAINS:
            errors.append(f"{gap_id}: unknown domain")
        if gap.get("priority") not in VALID_PRIORITIES:
            errors.append(f"{gap_id}: invalid priority")
        if gap.get("status") not in VALID_GAP_STATES:
            errors.append(f"{gap_id}: invalid status")
        if not gap.get("owner"):
            errors.append(f"{gap_id}: missing owner")
        if not gap.get("closure_evidence"):
            errors.append(f"{gap_id}: missing closure evidence")

    all_ready = True
    for domain in domains:
        domain_id = domain.get("id")
        if domain.get("target") != 9.0:
            errors.append(f"{domain_id}: target must be 9.0")
        maturity = domain.get("evidence_maturity")
        if maturity not in CAPS:
            errors.append(f"{domain_id}: invalid evidence maturity")
            continue
        score = domain.get("score")
        cap = CAPS[maturity]
        if score is None:
            if maturity != "UNKNOWN":
                errors.append(f"{domain_id}: null score requires UNKNOWN maturity")
            all_ready = False
        else:
            if not isinstance(score, (int, float)) or not 0 <= float(score) <= 10:
                errors.append(f"{domain_id}: score outside 0..10")
            elif cap is not None and float(score) > cap:
                errors.append(f"{domain_id}: score {score} exceeds {maturity} cap {cap}")
            if float(score) < threshold:
                all_ready = False
                refs = domain.get("blocking_gaps", [])
                if not refs:
                    errors.append(f"{domain_id}: sub-threshold domain has no blocking gap")
                unknown_refs = sorted(set(refs) - known_gaps)
                if unknown_refs:
                    errors.append(f"{domain_id}: unknown blocking gaps: {', '.join(unknown_refs)}")
                for ref in refs:
                    match = next((gap for gap in gaps if gap.get("id") == ref), None)
                    if match and match.get("domain") != domain_id:
                        errors.append(f"{domain_id}: gap {ref} belongs to {match.get('domain')}")
        if not domain.get("owner") or not domain.get("acceptance_authority"):
            errors.append(f"{domain_id}: missing owner or acceptance authority")
        if not domain.get("evidence"):
            errors.append(f"{domain_id}: missing evidence references")

    declared_ready = scorecard.get("world_class_ready") is True or scorecard.get("overall_state") == "WORLD_CLASS_READY"
    if declared_ready and not all_ready:
        errors.append("WORLD_CLASS_READY declared while one or more domains are below 9.0")
    if declared_ready and any(gap.get("priority") == "P0" and gap.get("status") != "CLOSED" for gap in gaps):
        errors.append("WORLD_CLASS_READY declared with open P0 gaps")
    if all_ready and scorecard.get("overall_state") == "GAP_CLOSURE":
        errors.append("all domains meet threshold but state remains GAP_CLOSURE")

    required = [
        "governance/WORLD_CLASS_READINESS_POLICY.md",
        "readiness/READINESS_SCORE_MODEL.md",
        "roadmap/WORLD_CLASS_9_OF_10_ROADMAP.md",
    ]
    for path in required:
        if not (ROOT / path).is_file():
            errors.append(f"missing readiness artifact: {path}")

    if errors:
        print("READINESS_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1

    scores = [float(item["score"]) for item in domains if item.get("score") is not None]
    print("READINESS_VALIDATION=PASSED")
    print(f"DOMAINS={len(domains)}")
    print(f"THRESHOLD={threshold:.1f}")
    print(f"MINIMUM_SCORE={min(scores):.1f}")
    print(f"DOMAINS_AT_OR_ABOVE_9={sum(score >= threshold for score in scores)}")
    print(f"OPEN_P0_GAPS={sum(gap.get('priority') == 'P0' and gap.get('status') != 'CLOSED' for gap in gaps)}")
    print(f"WORLD_CLASS_READY={str(scorecard.get('world_class_ready')).lower()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
