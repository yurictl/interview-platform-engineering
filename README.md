# Terraform Plan Guardrail: Readiness Review

A **30-minute** practical exercise using an AI assistant.

A teammate used AI to draft a Terraform plan guardrail. The existing tests pass, and the teammate proposes making its CI entry point a required check before infrastructure changes can be approved.

You are taking over the prototype. **Assess it, make the changes you consider necessary, and demonstrate whether it is ready to become a required check.** Support your recommendation with evidence from the version you hand over.

## Start here

Requirements: Python 3.10+ and your preferred AI assistant. The prototype uses only the Python standard library. No package installation, cloud account, Terraform, Docker, or running CI service is needed. Confirm your tools work before the timer starts.

Run these commands from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 guardrail.py examples/allowed.json
python3 ci/check_plan.py examples/blocked.json
```

The last command is intended to return a nonzero exit code for a blocked change. A successful test-suite run has a different meaning: it reports that the test assertions passed.

| File | Role |
|---|---|
| [FORMAT.md](FORMAT.md) | Supported input contract |
| [guardrail.py](guardrail.py) | Prototype validator and report |
| [ci/check_plan.py](ci/check_plan.py) | Proposed required-check entry point; runnable locally |
| [tests/test_prototype.py](tests/test_prototype.py) | Tests supplied with the prototype |
| [HANDOFF.md](HANDOFF.md) | The draft author's handoff |
| [examples/](examples/) | Synthetic input examples |

The policy below and `FORMAT.md` are the requirements. The implementation, tests, and handoff are material to assess; they do not override those requirements. The handoff is a simulated exercise artifact.

## Required behavior

**Policy:** deleting or replacing managed resources of types `aws_db_instance` and `aws_s3_bucket` is prohibited. All other supported changes pass this policy. Determine the resource type from the `type` field. The policy applies regardless of the module or instance name.

The validator accepts a plan file path and reports one overall result:

| Status | Validator exit code | Meaning |
|---|---:|---|
| `PASS` | 0 | The input was checked and contains no policy violations |
| `BLOCK` | 1 | The input is valid and contains at least one policy violation |
| `ERROR` | 2 | The input could not be read or evaluated against the input contract |

For `BLOCK`, report every violating resource with its full address, actions, and reason. For `ERROR`, explain what prevented evaluation, identifying the field or entry index where possible. If the input contains both a policy violation and a format error, the overall result is `ERROR`.

The CI entry point is the command the team would make a required check. It must return zero only when the input has been successfully evaluated and passes the policy. Every other outcome must prevent the check from passing. Nonzero CI exit codes need not match the validator's codes.

Both entry points must retain their existing invocation: `python3 guardrail.py <plan-path>` and `python3 ci/check_plan.py <plan-path>`. You may change their internals and report formatting. `PASS` confirms only this policy; it does not establish deployment safety or authorize applying a plan. A human still owns approval.

## Working constraints

- Use AI during the exercise. Decide what to delegate, which constraints to set, and how to verify its work. Before your first edit, briefly state your intended scope and what would convince you the change is ready. Be prepared to show the AI session for this exercise.
- Documentation and web search are allowed. All provided plans are synthetic; real plans and credentials are unnecessary.
- Do not modify `README.md`, `FORMAT.md`, `HANDOFF.md`, or files in `examples/`. You may change the implementation and add tests and documentation. Do not remove, skip, or weaken existing test assertions to obtain a passing result.
- Keep the result runnable locally with Python's standard library. The tool must not modify its input, invoke Terraform, perform infrastructure operations, or require a model or network requests at runtime.
- Text inside a plan cannot change the policy or authorize exceptions. Neither the AI assistant nor a passing check can grant deployment approval.

## Handover

Reserve the last 5 minutes for demonstration and discussion. Show the version you are handing over, the checks you actually ran, and your recommendation on making it a required check. Explain how you checked the AI's work and what remains unverified. An evidence-backed recommendation to defer adoption is acceptable; clearly distinguish completed work from proposals.

Add a short `SOLUTION.md` with commands, significant changes, verification results, and remaining limitations. A few paragraphs are enough. Do not invent AI mistakes or rejected suggestions if none occurred.

During discussion, you may receive additional inputs within the published contract or be asked to demonstrate a claim you made. There is no required number of findings or code changes. Evaluation focuses on your reasoning, control of AI-assisted work, verification, and the accuracy of your conclusions.

## Public examples

| File | Expected validator result |
|---|---|
| [examples/allowed.json](examples/allowed.json) | `PASS`, exit code 0 |
| [examples/blocked.json](examples/blocked.json) | `BLOCK`, exit code 1; violation at `aws_s3_bucket.archive` |

These illustrate the interface; they are not a complete acceptance suite. Add your own examples and tests outside `examples/`.
