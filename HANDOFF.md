# Prototype Handoff

Simulated teammate handoff supplied as part of the exercise.

> I used an AI assistant to put together the plan check. It checks the JSON
> structure before evaluating the resource changes and produces a report for
> review. It covers deletion and replacement of the protected resource types.
>
> The CI entry point prints the validator report and turns the result into a job
> status. Inputs that cannot be evaluated should not get a green check.
>
> The tests cover the protected resource types and the CI integration. They pass
> locally. I think this is ready to make a required check, with a human still
> approving the infrastructure change afterward.
>
> Please review it and make any changes you think are needed before we adopt it.
