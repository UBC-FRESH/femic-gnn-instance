# P10 Close-Out: Documentation and Provenance Refresh

Phase: P10 / `UBC-FRESH/femic-gnn-instance#49`
Task: P10.1 / `UBC-FRESH/femic-gnn-instance#50`
Branch: `feature/p10-docs-refresh`
PR: `UBC-FRESH/femic-gnn-instance#51`
Status: complete; merged as the P10 docs commit

## Outcome

The public documentation now matches P9 and separates three clearly different
things:

- the **volume-only release**;
- the **P3 diagnostic** cost/operability screen;
- the **P9 descriptive/pilot indicators**.

## Changes

- Added `docs/indicators.rst` with source, coverage, field, validation,
  provenance, and rebuild sections.
- Updated `README.md`, `docs/index.rst`, `docs/release.rst`,
  `docs/benchmark.rst`, and `docs/economic-screening.rst`.
- Documented the optional P9 path and prerequisites in
  `docs/model-build.rst` and `pipeline/README.md`.
- Updated `docs/llms.txt` and the docs toctree.
- Tracked `notes/gnn-partner-data-request.md`.
- Recorded P10 in `ROADMAP.md` and `CHANGE_LOG.md`.

## Verification

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator,
  docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- Sphinx `-W`: clean.
- CI: Green dashboard summary, Pre-commit parity, and Quality gates passed on
  PR #51.

## Limits

- The partner data request still has placeholder follow-up date and contact
  fields; no dates, names, or responses were invented.
- The P9 fields remain descriptive; no operability threshold, CHM, biomass, or
  sustainable claim is promoted.
- No model, curve, THLB, AAC, scenario, data, or release-label change.

## Decision

Close P10 and P10.1. The public documentation is current for the P9 state. Any
future indicator or model change needs its own evidence-backed phase.

## Follow-up

- Fill the partner request follow-up/contact fields when the maintainer has
  them.
- Do not reopen P9/P10 for public terrain claims without new evidence.
