"""Run the plan validator and report the required CI check's outcome."""

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan")
    args = parser.parse_args(argv)

    result = subprocess.run(
        [sys.executable, str(ROOT / "guardrail.py"), args.plan],
        capture_output=True,
        text=True,
    )
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)

    if any(line.startswith("[BLOCK]") for line in result.stdout.splitlines()):
        print("CI check: failed")
        return 1

    print("CI check: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
