#!/usr/bin/env python3
"""Validate the portable control, profile and open-source catalogs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_ID = re.compile(r"^EW-[A-Z]+-[0-9]{3}$")
FULL_SHA = re.compile(r"^[a-f0-9]{40}$")
ACTION = re.compile(r"^\s*-\s+uses:\s*([^\s#]+)", re.MULTILINE)
RISKS = {"R0", "R1", "R2", "R3"}
ASSURANCE_LEVELS = {
    "A1-professional-foundation",
    "A2-controlled-engineering",
    "A3-high-assurance-product",
    "A4-production-assurance",
    "A5-critical-trust",
}
ANTI_DOWNGRADE_CONTROL = "EW-GOV-002"
SELECTION_POLICY = "highest-applicable-assurance; downgrade-by-convenience-prohibited"


def load(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    catalog = load("controls/catalog.json")
    controls = catalog.get("controls", []) if isinstance(catalog, dict) else []
    ids = [item.get("id") for item in controls if isinstance(item, dict)]
    if not controls:
        errors.append("control catalog is empty")
    if len(ids) != len(set(ids)):
        errors.append("control IDs are not unique")
    for item in controls:
        control_id = item.get("id")
        if not isinstance(control_id, str) or not CONTROL_ID.match(control_id):
            errors.append(f"invalid control ID: {control_id!r}")
        if item.get("minimum_risk") not in RISKS:
            errors.append(f"{control_id}: invalid minimum_risk")
        if item.get("requirement") != "MUST":
            errors.append(f"{control_id}: control catalog accepts only MUST requirements")

    anti_downgrade = next((item for item in controls if item.get("id") == ANTI_DOWNGRADE_CONTROL), None)
    if anti_downgrade is None:
        errors.append(f"missing mandatory control: {ANTI_DOWNGRADE_CONTROL}")
    elif anti_downgrade.get("exception_allowed") is not False:
        errors.append(f"{ANTI_DOWNGRADE_CONTROL}: anti-downgrade control must be non-exceptable")

    profiles = load("profiles/catalog.json")
    profile_items = profiles.get("profiles", []) if isinstance(profiles, dict) else []
    if not isinstance(profiles, dict) or profiles.get("selection_policy") != SELECTION_POLICY:
        errors.append("profiles catalog does not enforce highest-applicable assurance selection")
    known = set(ids)
    profile_ids: list[str] = []
    assurance_levels: list[str] = []
    for profile in profile_items:
        profile_id = profile.get("id")
        profile_ids.append(profile_id)
        assurance_level = profile.get("assurance_level")
        assurance_levels.append(assurance_level)
        if assurance_level not in ASSURANCE_LEVELS:
            errors.append(f"{profile_id}: invalid assurance_level")
        if profile.get("maximum_risk") not in RISKS:
            errors.append(f"{profile_id}: invalid maximum_risk")
        required = set(profile.get("required_controls", []))
        unknown = sorted(required - known)
        if unknown:
            errors.append(f"{profile_id}: unknown controls: {', '.join(unknown)}")
        if ANTI_DOWNGRADE_CONTROL not in required:
            errors.append(f"{profile_id}: missing mandatory anti-downgrade control")
        if "profile-downgrade-to-avoid-controls" not in set(profile.get("prohibited", [])):
            errors.append(f"{profile_id}: profile downgrade prohibition is missing")
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("profile IDs are not unique")
    if len(assurance_levels) != len(set(assurance_levels)):
        errors.append("assurance levels are not unique across profiles")

    assurance_policy = ROOT / "governance/WORLD_CLASS_ASSURANCE_POLICY.md"
    if not assurance_policy.is_file():
        errors.append("missing world-class assurance policy")

    components = load("config/open-source-components.json")
    component_items = components.get("components", []) if isinstance(components, dict) else []
    component_ids = [item.get("id") for item in component_items]
    if len(component_ids) != len(set(component_ids)):
        errors.append("open-source component IDs are not unique")
    for item in component_items:
        if not str(item.get("source", "")).startswith("https://"):
            errors.append(f"{item.get('id')}: source must use https")
        if not item.get("license"):
            errors.append(f"{item.get('id')}: missing license")

    action_count = 0
    for workflow in (ROOT / ".github/workflows").glob("*.y*ml"):
        text = workflow.read_text(encoding="utf-8")
        for target in ACTION.findall(text):
            if target.startswith("./"):
                continue
            action_count += 1
            if "@" not in target or not FULL_SHA.match(target.rsplit("@", 1)[1]):
                errors.append(f"{workflow.relative_to(ROOT)}: mutable action reference: {target}")

    if errors:
        print("CONTROL_VALIDATION=FAILED")
        for message in errors:
            print(f"ERROR: {message}")
        return 1

    print("CONTROL_VALIDATION=PASSED")
    print(f"CONTROLS={len(controls)}")
    print(f"PROFILES={len(profile_items)}")
    print(f"ASSURANCE_LEVELS={len(assurance_levels)}")
    print(f"OPEN_SOURCE_COMPONENTS={len(component_items)}")
    print(f"PINNED_ACTIONS={action_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
