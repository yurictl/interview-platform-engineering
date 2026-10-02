"""Check the supported Terraform plan subset and print a policy report."""

import argparse
import json
import sys
from pathlib import Path


PROTECTED_TYPES = {"aws_db_instance", "aws_s3_bucket"}
SUPPORTED_ACTIONS = (
    ["no-op"],
    ["create"],
    ["update"],
    ["delete"],
    ["delete", "create"],
    ["create", "delete"],
)


class InputError(ValueError):
    pass


def validate_input(plan):
    if not isinstance(plan, dict):
        raise InputError("The root must be an object")
    if plan.get("format_version") != "1.0":
        raise InputError("format_version must be the string '1.0'")
    changes = plan.get("resource_changes")
    if not isinstance(changes, list):
        raise InputError("resource_changes must be an array")

    for index, resource in enumerate(changes):
        location = f"resource_changes[{index}]"
        if not isinstance(resource, dict):
            raise InputError(f"{location} must be an object")
        for field in ("address", "type"):
            value = resource.get(field)
            if not isinstance(value, str) or not value.strip():
                raise InputError(f"{location}.{field} must be a nonblank string")
        if resource.get("mode") != "managed":
            raise InputError(f"{location}.mode must be 'managed'")
        change = resource.get("change")
        if not isinstance(change, dict):
            raise InputError(f"{location}.change must be an object")
        if change.get("actions") not in SUPPORTED_ACTIONS:
            raise InputError(f"{location}.change.actions is missing or unsupported")
    return changes


def find_violations(changes):
    findings = []
    for resource in changes:
        actions = resource["change"]["actions"]
        if resource["type"] in PROTECTED_TYPES and actions == ["delete"]:
            findings.append(
                {
                    "address": resource["address"],
                    "actions": actions,
                    "reason": "Protected resources must not be deleted or replaced",
                }
            )
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args(argv)

    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        changes = validate_input(plan)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2

    findings = find_violations(changes)
    for finding in findings:
        print(
            f"[BLOCK] {finding['address']} actions={finding['actions']}: "
            f"{finding['reason']}"
        )
    if findings:
        return 1

    print("[PASS] No violations of the protected-resource policy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
