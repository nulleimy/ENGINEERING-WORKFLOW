from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_primary_invariant.py"
SPEC = importlib.util.spec_from_file_location("validate_primary_invariant", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
FILES = (
    "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md",
    "governance/PRIMARY_ENGINEERING_INVARIANT.json",
    "governance/CONSTITUTIONAL_AUTHORITY.json",
    "config/complexity-budget.json",
    "config/reversibility-classes.json",
    "evidence/manual-work-register.json",
    "evidence/lifecycle-evidence-graph.json",
)


def copy_fixture(root: Path) -> None:
    for rel in FILES:
        source = ROOT / rel
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


class PrimaryInvariantTest(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_missing_property_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_fixture(root)
            invariant = root / "governance/PRIMARY_ENGINEERING_INVARIANT.json"
            data = json.loads(invariant.read_text(encoding="utf-8"))
            data["required_properties"].pop()
            invariant.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            authority = root / "governance/CONSTITUTIONAL_AUTHORITY.json"
            authority_data = json.loads(authority.read_text(encoding="utf-8"))
            authority_data["primary_engineering_invariant"]["sha256"] = hashlib.sha256(invariant.read_bytes()).hexdigest()
            authority.write_text(json.dumps(authority_data, indent=2) + "\n", encoding="utf-8")
            self.assertTrue(any("required change properties" in item for item in MODULE.validate(root)))

    def test_rev4_weakened_lane_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_fixture(root)
            path = root / "config/reversibility-classes.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            next(item for item in data["classes"] if item["id"] == "REV-4")["minimum_lane"] = "R1"
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            self.assertTrue(any("REV-4 must require R3" in item for item in MODULE.validate(root)))

    def test_orphan_edge_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            copy_fixture(root)
            path = root / "evidence/lifecycle-evidence-graph.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["edges"] = [{"from": "missing", "to": "also-missing"}]
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            self.assertTrue(any("unknown node" in item for item in MODULE.validate(root)))


if __name__ == "__main__":
    unittest.main()
