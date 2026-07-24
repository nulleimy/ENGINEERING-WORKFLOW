#!/usr/bin/env python3
"""Validate assurance frameworks, mappings, targets and evidence references."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = {"A1", "A2", "A3", "A4", "A5"}
RELATIONSHIPS = {"direct", "supporting", "contextual"}
FRAMEWORK_STATUSES = {"final", "approved", "stable", "current", "draft"}
SLSA_LEVEL = re.compile(r"^L[0-3]$")


def load(path: str) -> dict:
    data = json.loads((ROOT / path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: root must be an object")
    return data


def duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def main() -> int:
    errors: list[str] = []

    controls_doc = load("controls/catalog.json")
    control_ids = [item.get("id") for item in controls_doc.get("controls", [])]
    known_controls = set(control_ids)

    framework_doc = load("assurance/framework-catalog.json")
    frameworks = framework_doc.get("frameworks", [])
    framework_ids = [item.get("id") for item in frameworks]
    known_frameworks = set(framework_ids)
    if duplicate := duplicates(framework_ids):
        errors.append(f"duplicate framework IDs: {', '.join(sorted(duplicate))}")
    for framework in frameworks:
        framework_id = framework.get("id")
        status = framework.get("status")
        if status not in FRAMEWORK_STATUSES:
            errors.append(f"{framework_id}: invalid framework status {status!r}")
        if not str(framework.get("source", "")).startswith("https://"):
            errors.append(f"{framework_id}: source must use https")
        if status == "draft" and framework.get("normative_use") is not False:
            errors.append(f"{framework_id}: draft framework cannot be normative")

    target_doc = load("assurance/assurance-level-targets.json")
    levels = target_doc.get("levels", [])
    level_ids = [item.get("id") for item in levels]
    if set(level_ids) != LEVELS:
        errors.append(f"assurance targets must define exactly {sorted(LEVELS)}")
    for level in levels:
        targets = level.get("targets", {})
        for key, value in targets.items():
            if key.startswith("slsa_") and key.endswith(("minimum", "target")):
                if not isinstance(value, str) or not SLSA_LEVEL.match(value):
                    errors.append(f"{level.get('id')}: invalid {key} value {value!r}")

    evidence_doc = load("evidence/evidence-catalog.json")
    evidence = evidence_doc.get("evidence_types", [])
    evidence_ids = [item.get("id") for item in evidence]
    known_evidence = set(evidence_ids)
    if duplicate := duplicates(evidence_ids):
        errors.append(f"duplicate evidence IDs: {', '.join(sorted(duplicate))}")
    for item in evidence:
        evidence_id = item.get("id")
        if item.get("minimum_assurance") not in LEVELS:
            errors.append(f"{evidence_id}: invalid minimum assurance")
        if not item.get("retention"):
            errors.append(f"{evidence_id}: missing retention")

    mapping_doc = load("assurance/control-framework-mapping.json")
    mappings = mapping_doc.get("mappings", [])
    mapped_controls = [item.get("control_id") for item in mappings]
    if duplicate := duplicates(mapped_controls):
        errors.append(f"duplicate mapped control IDs: {', '.join(sorted(duplicate))}")
    missing = sorted(known_controls - set(mapped_controls))
    unknown = sorted(set(mapped_controls) - known_controls)
    if missing:
        errors.append(f"controls without assurance mapping: {', '.join(missing)}")
    if unknown:
        errors.append(f"mapping references unknown controls: {', '.join(unknown)}")

    for mapping in mappings:
        control_id = mapping.get("control_id")
        framework_refs = mapping.get("frameworks", [])
        if not framework_refs:
            errors.append(f"{control_id}: no framework mappings")
        for reference in framework_refs:
            framework_id = reference.get("framework_id")
            if framework_id not in known_frameworks:
                errors.append(f"{control_id}: unknown framework {framework_id!r}")
            if reference.get("relationship") not in RELATIONSHIPS:
                errors.append(f"{control_id}/{framework_id}: invalid relationship")
            if not reference.get("references"):
                errors.append(f"{control_id}/{framework_id}: missing references")
        for evidence_id in mapping.get("evidence", []):
            if evidence_id not in known_evidence:
                errors.append(f"{control_id}: unknown evidence {evidence_id}")

    if not (ROOT / "assurance/ASSURANCE_MAPPING_STANDARD.md").is_file():
        errors.append("missing assurance mapping standard")

    if errors:
        print("ASSURANCE_VALIDATION=FAILED")
        for message in errors:
            print(f"ERROR: {message}")
        return 1

    print("ASSURANCE_VALIDATION=PASSED")
    print(f"FRAMEWORKS={len(frameworks)}")
    print(f"ASSURANCE_LEVELS={len(levels)}")
    print(f"CONTROLS_MAPPED={len(mappings)}")
    print(f"EVIDENCE_TYPES={len(evidence)}")
    print("DRAFT_FRAMEWORKS_NORMATIVE=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
