from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_constitutions.py"
SPEC = importlib.util.spec_from_file_location("validate_constitutions", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ConstitutionalValidationTest(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_product_constitution_tampering_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "governance").mkdir(parents=True)
            for rel in (
                "governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md",
                "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md",
                "governance/CONSTITUTIONAL_AUTHORITY.json",
                "project-control.json",
            ):
                source = ROOT / rel
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            product = root / "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md"
            product.write_text(product.read_text(encoding="utf-8") + "\nunauthorized change\n", encoding="utf-8")
            errors = MODULE.validate(root)
            self.assertTrue(any("hash mismatch" in item for item in errors), errors)

    def test_weakened_protected_operations_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "governance").mkdir(parents=True)
            for rel in (
                "governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md",
                "governance/PRODUCT_DECISION_EXECUTION_CONSTITUTION.md",
                "governance/CONSTITUTIONAL_AUTHORITY.json",
                "project-control.json",
            ):
                source = ROOT / rel
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            index_path = root / "governance/CONSTITUTIONAL_AUTHORITY.json"
            data = json.loads(index_path.read_text(encoding="utf-8"))
            data["protected_operations_require_explicit_operator_authorization"].remove("release")
            index_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            errors = MODULE.validate(root)
            self.assertTrue(any("protected-operation" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
