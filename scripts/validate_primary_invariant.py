#!/usr/bin/env python3
"""Validate the machine-enforced primary engineering invariant."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_PROPERTIES = {"simple", "purposeful", "automated", "secure", "measurable", "reversible", "evidence-verifiable"}
EXPECTED_REV = {"REV-0", "REV-1", "REV-2", "REV-3", "REV-4"}
EXPECTED_NODES = {"product-problem", "decision", "work-package", "change-set", "verification", "review", "acceptance", "release", "deployment", "telemetry", "incident", "learning"}
NON_EXCEPTABLE = {"truthful-status", "evidence-integrity", "secret-protection", "explicit-protected-operation-authorization"}


def load(root: Path, rel: str, errors: list[str]) -> dict:
    path = root / rel
    if not path.is_file():
        errors.append(f"missing {rel}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    invariant = load(root, "governance/PRIMARY_ENGINEERING_INVARIANT.json", errors)
    product = root / "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md"
    if not product.is_file():
        errors.append("missing product constitution")
    else:
        text = product.read_text(encoding="utf-8")
        if "## ČLÁNEK 0 — PRIMÁRNÍ VÝVOJOVÝ INVARIANT" not in text:
            errors.append("Article 0 primary invariant is missing")
        if invariant.get("constitution_sha256") != digest(product):
            errors.append("primary invariant is not bound to current product constitution")

    properties = {item.get("id") for item in invariant.get("required_properties", []) if isinstance(item, dict)}
    if properties != EXPECTED_PROPERTIES:
        errors.append("required change properties changed or are incomplete")
    if any(item.get("requirement") != "MUST" for item in invariant.get("required_properties", []) if isinstance(item, dict)):
        errors.append("all change properties must be MUST")
    if set(invariant.get("non_exceptable_boundaries", [])) != NON_EXCEPTABLE:
        errors.append("non-exceptable boundaries changed or are incomplete")
    for key, rel in invariant.get("supporting_controls", {}).items():
        if not (root / rel).is_file():
            errors.append(f"missing supporting control {key}: {rel}")

    complexity = load(root, "config/complexity-budget.json", errors)
    dimensions = complexity.get("dimensions", [])
    if len({item.get("id") for item in dimensions if isinstance(item, dict)}) != 7:
        errors.append("complexity dimensions must be exactly seven unique controls")
    if any(not isinstance(item.get("default_limit"), (int, float)) or item.get("default_limit") < 0 for item in dimensions if isinstance(item, dict)):
        errors.append("complexity limits must be non-negative numbers")

    reversibility = load(root, "config/reversibility-classes.json", errors)
    classes = {item.get("id") for item in reversibility.get("classes", []) if isinstance(item, dict)}
    if classes != EXPECTED_REV:
        errors.append("reversibility classes must be REV-0 through REV-4")
    by_id = {item.get("id"): item for item in reversibility.get("classes", []) if isinstance(item, dict)}
    for class_id in ("REV-3", "REV-4"):
        if by_id.get(class_id, {}).get("minimum_lane") != "R3":
            errors.append(f"{class_id} must require R3")

    manual = load(root, "evidence/manual-work-register.json", errors)
    states = set(manual.get("allowed_states", []))
    if not {"MANUAL", "AUTOMATION_CANDIDATE", "AUTOMATED", "VERIFIED"}.issubset(states):
        errors.append("manual work lifecycle states are incomplete")
    threshold = manual.get("automation_candidate_threshold", {})
    if threshold.get("occurrences_per_30_days", 0) < 1 or threshold.get("minutes_per_occurrence", 0) < 1:
        errors.append("manual work thresholds must be positive")

    graph = load(root, "evidence/lifecycle-evidence-graph.json", errors)
    if set(graph.get("required_node_types", [])) != EXPECTED_NODES:
        errors.append("lifecycle node types changed or are incomplete")
    rules = graph.get("rules", {})
    if not all(rules.get(key) is True for key in ("no-orphan-release", "no-orphan-deployment", "no-orphan-incident", "canonical-record-required")):
        errors.append("lifecycle orphan/canonical rules must fail closed")
    node_ids = [node.get("id") for node in graph.get("nodes", []) if isinstance(node, dict)]
    if len(node_ids) != len(set(node_ids)):
        errors.append("lifecycle graph contains duplicate node ids")
    known = set(node_ids)
    for edge in graph.get("edges", []):
        if edge.get("from") not in known or edge.get("to") not in known:
            errors.append("lifecycle graph edge references unknown node")

    authority = load(root, "governance/CONSTITUTIONAL_AUTHORITY.json", errors)
    reference = authority.get("primary_engineering_invariant", {})
    invariant_path = root / reference.get("path", "")
    if not invariant_path.is_file() or reference.get("sha256") != digest(invariant_path):
        errors.append("constitutional authority invariant hash mismatch")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = validate(args.root)
    if errors:
        print("PRIMARY_INVARIANT_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    print("PRIMARY_INVARIANT_VALIDATION=PASSED")
    print("REQUIRED_PROPERTIES=7")
    print("COMPLEXITY_DIMENSIONS=7")
    print("REVERSIBILITY_CLASSES=5")
    print("LIFECYCLE_NODE_TYPES=12")
    return 0


if __name__ == "__main__":
    sys.exit(main())
