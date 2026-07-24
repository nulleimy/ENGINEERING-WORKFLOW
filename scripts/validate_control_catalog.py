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
        if item.get("requirement") not in {"MUST", "SHOULD", "MAY"}:
            errors.append(f"{control_id}: invalid requirement")

    profiles = load("profiles/catalog.json")
    profile_items = profiles.get("profiles", []) if isinstance(profiles, dict) else []
    known = set(ids)
    profile_ids: list[str] = []
    for profile in profile_items:
        profile_id = profile.get("id")
        profile_ids.append(profile_id)
        if profile.get("maximum_risk") not in RISKS:
            errors.append(f"{profile_id}: invalid maximum_risk")
        unknown = sorted(set(profile.get("required_controls", [])) - known)
        if unknown:
            errors.append(f"{profile_id}: unknown controls: {', '.join(unknown)}")
    if len(profile_ids) != len(set(profile_ids)):
        errors.append("profile IDs are not unique")

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
    print(f"OPEN_SOURCE_COMPONENTS={len(component_items)}")
    print(f"PINNED_ACTIONS={action_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
