# ADR 0005: Separate workflow tooling from the model pipeline

Status: accepted
Date: 2026-10-25
Issues: #1, #2

## Context

The workflow seed applies strict lint, type, docstring, and coverage gates to
`scripts/`. The GNN repository also contains data-pipeline entry points that
read large spatial inputs, call FEMIC and ws4, and are validated by execution.
Applying the seed's gates to both would either require a large type-and-test
retrofit unrelated to the model or weaken the gates for the workflow tooling.

## Decision

Keep `scripts/` for workflow tooling only: `check_workflow.py` and
`dashboard.py`. Move the model build and analysis entry points to `pipeline/`.
The strict gates apply to `scripts/`, `tests/`, and `docs/conf.py`. The
`pipeline/` entry points are excluded from those gates and are validated by
execution, `ws4 validate`, and the documented model evidence.

## Consequences

- The dashboard is meaningful and fast.
- The pipeline remains a runnable, documented artifact without pretending to be
  a typed library.
- A future pipeline test lane can be added without changing the workflow gates.
- The exclusion is explicit and recorded here and in the changelog.

## Alternatives considered

- Apply all gates to the pipeline: rejected as a disproportionate retrofit.
- Remove the gates: rejected; the workflow tooling still needs them.
- Keep both in `scripts/`: rejected because the gate scope would be ambiguous.
