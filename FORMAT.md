# Input Contract

This exercise uses a **reduced representation** of a Terraform JSON plan. The files in `examples/` were created for the interview and are not complete Terraform exports. You are not expected to implement the entire Terraform format within the time limit.

The structure is based on [HashiCorp — JSON Output Format](https://developer.hashicorp.com/terraform/internals/json-format), specifically Plan Representation and Change Representation. A full export is produced with `terraform show -json`; you do not need to run that command for this exercise.

The requirements below define the contract for this exercise. In particular, do not assume that fields required here are mandatory in every real Terraform plan.

## Required fields

The root must be a JSON object:

| Field | Exercise requirement |
|---|---|
| `format_version` | The string `"1.0"`. This is the only version supported in the exercise |
| `resource_changes` | An array of change objects. It may be empty |

Each entry in `resource_changes` must contain:

| Field | Exercise requirement |
|---|---|
| `address` | A nonempty string containing at least one non-whitespace character; report the full value |
| `mode` | The string `"managed"`. Other modes are outside the supported subset |
| `type` | A nonempty string containing at least one non-whitespace character; match protected types exactly and case-sensitively |
| `change` | An object |
| `change.actions` | One of the arrays listed below |

You do not need to parse address syntax or check that an address matches `type`. In valid examples, addresses are unique and consistent with their types; validating these two properties is outside the exercise.

## Supported actions

| `change.actions` | Meaning |
|---|---|
| `["no-op"]` | No change |
| `["create"]` | Create |
| `["update"]` | Update an existing resource |
| `["delete"]` | Delete |
| `["delete", "create"]` | Replace: delete first, then create |
| `["create", "delete"]` | Replace: create first, then delete |

Other action arrays, including an empty array, are unsupported. The policy in the README applies to the entire `resource_changes` array.

## Validation scope

- An unreadable file, invalid JSON, a missing required field, an incorrect type, or an unsupported value results in `ERROR`. Do not substitute defaults for missing required fields.
- A valid document with `resource_changes: []` passes the policy. A missing array violates the input contract.
- Additional fields are allowed at every level and must be ignored. The contents of `before`, `after`, tags, and descriptions do not affect the decision. You do not need to validate the structure of these additional fields.
- Any `type` value that meets the table's requirements is valid. Only the two exact types named in the README are protected; supported actions on other types pass the policy.
- Unknown future attribute values, planning status, drift, IAM, networking, dependencies, and actual infrastructure state are outside the evaluation scope. This report cannot serve as a complete check of a real plan before applying it.

Evaluation inputs are limited to small UTF-8 JSON files without duplicate keys or nonstandard numeric values. Streaming, input size limits, and support for binary plan files are not required.
