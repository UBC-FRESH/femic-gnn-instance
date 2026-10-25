# ADR 0001: Use the proposed GNN Statement of Intent boundary as the prototype AOI

Status: accepted
Date: 2026-10-25
Issues: #1, #2, UBC-FRESH/femic#341

## Context

The prototype needs a spatial boundary. No final treaty boundary or legal title
determination is available. BCGW publishes a First Nation Statement of Intent
(SOI) polygon for `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`, and the tracking
issue identifies it as the working boundary.

## Decision

Use the proposed GNN SOI polygon, clipped to the TSA 46/47 union, as the
prototype AOI. Label it as a proposed Statement of Intent boundary on every
public surface. Require GNN review before public or operational use.

## Consequences

- The model has a reproducible, public boundary for the prototype.
- The 21,262.91 ha outside both TSAs is excluded from the forest model.
- The boundary may change after GNN review; model outputs are provisional.
- Public or operational use is blocked on confirmation, not on more modelling.

## Alternatives considered

- A final treaty boundary: not available.
- A hand-drawn or buffered boundary: less transparent and not reproducible.
- No boundary until review: blocks the prototype and the data-prep test.
