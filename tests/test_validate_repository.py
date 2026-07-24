from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTest(unittest.TestCase):
    def test_repository_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_repository.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("VALIDATION=PASSED", result.stdout)

    def test_project_control_is_present(self) -> None:
        self.assertTrue((ROOT / "project-control.json").is_file())

    def test_constitution_is_preserved(self) -> None:
        constitution = ROOT / "governance/WORLD_CLASS_SOFTWARE_DEVOPS_OPERATING_MODE.md"
        self.assertTrue(constitution.is_file())
        self.assertIn("WORLD-CLASS SOFTWARE / DEVOPS OPERATING MODE", constitution.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
