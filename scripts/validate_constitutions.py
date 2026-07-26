#!/usr/bin/env python3
"""Validate exact constitutional authority, Article 0 and protected operations."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_AUTHORITY_ORDER = [
    "applicable-law-security-platform-rules",
    "governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md",
    "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md",
    "explicit-authorized-operator-mandate",
    "project-governance-and-approved-records",
    "working-documentation-and-tool-configuration",
    "undocumented-assumptions",
]
EXPECTED_ROLES = {"canonical-technical-constitution", "product-decision-execution-constitution"}
EXPECTED_PROTECTED_OPERATIONS = {
    "file-deletion", "git-history-rewrite", "force-push", "production-infrastructure-change",
    "production-data-migration", "secret-rotation", "license-change", "branch-merge", "release", "public-api-change",
}
TECHNICAL_MARKERS = {"## 3. SOURCE OF TRUTH", "## 4. PRACOVNÍ REŽIMY", "## 7. BEZPEČNOST", "## 16. DEFINITION OF DONE", "## 18. OCHRANA PROJEKTU"}
PRODUCT_MARKERS = {
    "## ČLÁNEK 0 — PRIMÁRNÍ VÝVOJOVÝ INVARIANT",
    "## 0. Účel a vztah k technické ústavě",
    "## 6. Rozhodovací třídy",
    "## 11. Definition of Ready",
    "## 13. Release Ready a Operational Ready",
    "## 18. Self-test a conformance",
    "## 20. Jediný zdroj pravdy a změna ústavy",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    index_path = root / "governance/CONSTITUTIONAL_AUTHORITY.json"
    if not index_path.is_file():
        return ["missing governance/CONSTITUTIONAL_AUTHORITY.json"]
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid constitutional authority JSON: {exc}"]

    if data.get("schema_version") != "1.0.0":
        errors.append("unsupported constitutional authority schema version")
    if data.get("authority_order") != EXPECTED_AUTHORITY_ORDER:
        errors.append("constitutional authority order changed or is incomplete")
    if data.get("conflict_resolution", {}).get("unresolved") != "BLOCKED":
        errors.append("unresolved constitutional conflicts must fail closed as BLOCKED")
    if set(data.get("protected_operations_require_explicit_operator_authorization", [])) != EXPECTED_PROTECTED_OPERATIONS:
        errors.append("protected-operation authorization boundary changed or is incomplete")

    documents = data.get("documents", [])
    if len(documents) != 2:
        errors.append("exactly two constitutional authority documents are required")
        return errors
    if {item.get("role") for item in documents} != EXPECTED_ROLES:
        errors.append("constitutional document roles changed or are incomplete")

    texts: dict[str, str] = {}
    for item in documents:
        rel = item.get("path")
        path = (root / rel).resolve() if isinstance(rel, str) else root
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"constitutional path escapes repository: {rel}")
            continue
        if not path.is_file():
            errors.append(f"missing constitution: {rel}")
            continue
        actual = sha256(path)
        if actual != item.get("sha256"):
            errors.append(f"hash mismatch for {rel}: {actual} != {item.get('sha256')}")
        if item.get("exact_content_required") is not True:
            errors.append(f"exact content is not required for {rel}")
        texts[item.get("role", "unknown")] = path.read_text(encoding="utf-8")

    technical = texts.get("canonical-technical-constitution", "")
    product = texts.get("product-decision-execution-constitution", "")
    for marker in sorted(TECHNICAL_MARKERS):
        if marker not in technical:
            errors.append(f"technical constitution marker missing: {marker}")
    for marker in sorted(PRODUCT_MARKERS):
        if marker not in product:
            errors.append(f"product constitution marker missing: {marker}")
    technical_doc = next((item for item in documents if item.get("role") == "canonical-technical-constitution"), {})
    if technical_doc.get("sha256") and technical_doc["sha256"] not in product:
        errors.append("product constitution is not bound to the technical constitution hash")

    invariant = data.get("primary_engineering_invariant", {})
    rel = invariant.get("path")
    invariant_path = root / rel if isinstance(rel, str) else root / "missing"
    if not invariant_path.is_file():
        errors.append("missing primary engineering invariant")
    elif sha256(invariant_path) != invariant.get("sha256"):
        errors.append("primary engineering invariant hash mismatch")
    if invariant.get("exact_content_required") is not True:
        errors.append("primary engineering invariant exact content is not required")

    project_control_path = root / "project-control.json"
    if not project_control_path.is_file():
        errors.append("missing project-control.json")
    else:
        try:
            control = json.loads(project_control_path.read_text(encoding="utf-8")).get("control", {})
        except Exception as exc:
            errors.append(f"invalid project-control.json: {exc}")
            control = {}
        references = {
            "technical_operating_mode": "governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md",
            "product_decision_execution_constitution": "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md",
            "constitutional_authority": "governance/CONSTITUTIONAL_AUTHORITY.json",
            "constitutional_compatibility_report": "governance/CONSTITUTIONAL_COMPATIBILITY_REPORT.md",
            "primary_engineering_invariant": "governance/PRIMARY_ENGINEERING_INVARIANT.json",
        }
        for key, expected in references.items():
            if control.get(key) != expected:
                errors.append(f"project-control.json {key} must reference {expected}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    errors = validate(args.root)
    if errors:
        print("CONSTITUTION_VALIDATION=FAILED")
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    index = json.loads((args.root / "governance/CONSTITUTIONAL_AUTHORITY.json").read_text(encoding="utf-8"))
    print("CONSTITUTION_VALIDATION=PASSED")
    for item in index["documents"]:
        print(f"{item['role'].upper().replace('-', '_')}_SHA256={item['sha256']}")
    print(f"PRIMARY_ENGINEERING_INVARIANT_SHA256={index['primary_engineering_invariant']['sha256']}")
    print(f"AUTHORITY_LEVELS={len(index['authority_order'])}")
    print(f"PROTECTED_OPERATIONS={len(index['protected_operations_require_explicit_operator_authorization'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
