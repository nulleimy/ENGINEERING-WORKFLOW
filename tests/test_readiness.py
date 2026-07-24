from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadinessValidationTest(unittest.TestCase):
    def test_readiness_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_readiness.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("READINESS_VALIDATION=PASSED", result.stdout)
        self.assertIn("DOMAINS=14", result.stdout)
        self.assertIn("THRESHOLD=9.0", result.stdout)
        self.assertIn("DOMAINS_AT_OR_ABOVE_9=0", result.stdout)
        self.assertIn("WORLD_CLASS_READY=false", result.stdout)


if __name__ == "__main__":
    unittest.main()
