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
        self.assertIn("CONTROLS=14", result.stdout)
        self.assertIn("PROFILES=5", result.stdout)
        self.assertIn("OPEN_SOURCE_COMPONENTS=12", result.stdout)


if __name__ == "__main__":
    unittest.main()
