from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ControlCatalogTest(unittest.TestCase):
    def test_control_catalog_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_control_catalog.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("CONTROL_VALIDATION=PASSED", result.stdout)
        self.assertIn("CONTROLS=15", result.stdout)
        self.assertIn("PROFILES=5", result.stdout)
        self.assertIn("ASSURANCE_LEVELS=5", result.stdout)
        self.assertIn("OPEN_SOURCE_COMPONENTS=12", result.stdout)

    def test_world_class_assurance_policy_exists(self) -> None:
        policy = ROOT / "governance/WORLD_CLASS_ASSURANCE_POLICY.md"
        self.assertTrue(policy.is_file())
        text = policy.read_text(encoding="utf-8")
        self.assertIn("highest applicable assurance profile", text.lower())
        self.assertIn("downgrade", text.lower())


if __name__ == "__main__":
    unittest.main()
