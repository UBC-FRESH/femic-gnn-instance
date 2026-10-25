# ADR 0004: Do not tune curves or management assumptions to the derived AAC

Status: accepted
Date: 2026-10-25
Issues: #1, #2, UBC-FRESH/femic#341

## Context

The GNN benchmark is derived from the TSA 46/47 AACs. It is tempting to adjust
curves, density, or management assumptions until the schedule meets the target.
That would conflate benchmark fit with model accuracy and would hide the known
TSA 46 SI/origin issue.

## Decision

Do not tune curves, density, or management assumptions to the derived AAC or a
decade target. Judge model quality against ground observations. A schedule miss
is diagnosed as capacity, ordering, seed, or data, and is recorded rather than
removed by curve changes.

## Consequences

- The decade-10 miss of 781.4 m3 remains visible.
- Managed-SI experiments remain accuracy experiments, not production changes.
- The opening-first schedule can be adjusted only for scheduling reasons, with
  the reason recorded.
- Ground-plot evidence, not the AAC, is the primary accuracy test.

## Alternatives considered

- Tune curves to meet the target: rejected; it is not evidence of accuracy.
- Change the target until it is met: rejected; it hides the result.
- Suppress the miss: rejected; the miss is part of the evidence.
