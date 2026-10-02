"""Tests supplied with the initial plan guardrail prototype."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_tool(script, plan_path):
    return subprocess.run(
        [sys.executable, str(ROOT / script), str(plan_path)],
        capture_output=True,
        text=True,
    )


class PrototypeTests(unittest.TestCase):
    def check_deletion(self, resource_type):
        address = f"{resource_type}.primary"
        plan = {
            "format_version": "1.0",
            "resource_changes": [
                {
                    "address": address,
                    "mode": "managed",
                    "type": resource_type,
                    "change": {"actions": ["delete"]},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            result = run_tool("guardrail.py", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(address, result.stdout)

    def test_database_deletion_is_blocked(self):
        self.check_deletion("aws_db_instance")

    def test_bucket_deletion_is_blocked(self):
        self.check_deletion("aws_s3_bucket")

    def test_blocked_example_reports_resource(self):
        result = run_tool("guardrail.py", ROOT / "examples" / "blocked.json")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("aws_s3_bucket.archive", result.stdout)

    def test_ci_rejects_blocked_example(self):
        result = run_tool("ci/check_plan.py", ROOT / "examples" / "blocked.json")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
