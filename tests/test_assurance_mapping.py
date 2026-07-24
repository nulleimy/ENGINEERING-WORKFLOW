from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AssuranceMappingTest(unittest.TestCase):
    def test_assurance_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_assurance_mapping.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("ASSURANCE_VALIDATION=PASSED", result.stdout)
        self.assertIn("FRAMEWORKS=6", result.stdout)
        self.assertIn("ASSURANCE_LEVELS=5", result.stdout)
        self.assertIn("CONTROLS_MAPPED=15", result.stdout)
        self.assertIn("EVIDENCE_TYPES=43", result.stdout)
        self.assertIn("DRAFT_FRAMEWORKS_NORMATIVE=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
