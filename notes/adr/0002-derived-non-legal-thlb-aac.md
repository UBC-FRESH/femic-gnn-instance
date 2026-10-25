# ADR 0002: Label the GNN THLB and AAC as derived and non-legal

Status: accepted
Date: 2026-10-25
Issues: #1, #2, UBC-FRESH/femic#341

## Context

The GNN area has no standalone legal THLB or AAC. The prototype nevertheless
needs a managed area and a benchmark for an opening-first schedule. The TSA 46
and TSA 47 base models have calibrated THLB and published AAC values.

## Decision

Derive the GNN THLB by clipping the calibrated TSA 46/47 checkpoints and summing
the clipped calibrated area. Derive the annual AAC as the THLB-weighted share of
the published TSA 46 and TSA 47 AACs. Label both as derived and non-legal.

## Consequences

- The prototype has a transparent benchmark: 52,984.42 ha THLB and
  252,636.75 m3/yr.
- The benchmark is not evidence of a legal allowable cut.
- A reviewed GNN netdown can replace the derived values later without changing
  the label rule.
- The opening-first target must not be used to tune curves.

## Alternatives considered

- Gross-area share of the TSAs: ignores productivity and THLB differences.
- A zero or unavailable AAC: blocks the benchmark.
- Treating the derived value as legal: rejected; it would misstate the evidence.
