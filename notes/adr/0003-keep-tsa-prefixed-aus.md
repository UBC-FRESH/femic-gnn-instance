# ADR 0003: Keep TSA-prefixed AUs and use a reporting-only crosswalk

Status: accepted
Date: 2026-10-25
Issues: #1, #2

## Context

TSA 46 and TSA 47 use overlapping nominal strata and SI classes, but their
curves differ materially. For example, CWH_CW H untreated volume at age 100 is
85.5 m3/ha in TSA 46 and 584.6 m3/ha in TSA 47. TSA 46 also has a known
checkpoint SI understatement in managed stands.

## Decision

Keep TSA-prefixed AU ids in the model. Add a reporting-only crosswalk that maps
`CWH_FDC` to `CWH_FD` and `MH_H` to `MH_HM`. Do not merge model AUs or choose
one curve for a nominal match without evidence that the curves should be equal.

## Consequences

- Curve and SI provenance remain visible.
- The model has 39 AUs, with 37 carrying clipped area.
- Reports can aggregate by reporting group without hiding the TSA split.
- A future harmonization needs a separate accuracy case and ADR.

## Alternatives considered

- Merge by stratum and SI: rejected because it hides large curve differences.
- Keep only the largest TSA's curve: rejected for the same reason.
- Drop the small AUs: rejected because area and THLB shares are not the only
  consideration; provenance matters.
