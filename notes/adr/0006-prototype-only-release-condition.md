# ADR 0006: Prototype-only release condition for the derived THLB and AAC

Status: accepted
Date: 2026-10-25
Issues: #1, #13, UBC-FRESH/femic#341

## Context

The GNN prototype has a derived calibrated THLB of 52,984.42 ha and a derived
annual AAC of 252,636.75 m3/yr. Neither is a reviewed GNN netdown or a legal
allowable cut. P1.4 asks whether those derived values are sufficient for a
labelled prototype or whether a reviewed netdown is required before release.

## Decision

Use the derived values for the labelled prototype only. Public docs and the UI
may show them with the proposed-boundary and non-legal labels. Do not use them
for operational, legal, or investment decisions. Require a reviewed GNN netdown
and an explicit AAC decision before any operational release.

The P2 release gate must state this condition. A prototype release may proceed
only if the boundary review is recorded or explicitly deferred.

## Consequences

- The prototype remains useful for method and data review.
- The derived AAC is not presented as a legal cut.
- A reviewed netdown can replace the derived values later without changing the
  label rule.
- No curve or target change is needed to satisfy this decision.

## Alternatives considered

- Treat the derived values as sufficient for release: rejected; there is no
  reviewed netdown.
- Withhold all public access until a netdown exists: rejected for the prototype;
  the docs already carry the limitation and the public value is method review.
- Drop the AAC benchmark: rejected; it is useful as a clearly labelled derived
  comparison.
