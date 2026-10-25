# Change Log

Newest entries last. Each milestone gets a dated entry that matches the roadmap
status and the GitHub issue comments.

## 2026-10-25

### Pre-workflow prototype (retrospective record)

The prototype was built before this repository adopted the UBC-FRESH dev
workflow. This entry records what happened; it does not claim that the work
followed the workflow at the time.

- `198d63d` built the combined clipped TSA 46/47 checkpoint, bundle, ws4 matrix,
  derived opening-first schedule, and derived benchmark.
- `1e05b29` added the loopback UI geometry, served-model script, docs site, and
  Pages workflow.
- `73d6bec` added GNN-area ground-plot validation: 34 rows / 10 sites, too sparse
  for a GNN-specific accuracy conclusion.
- `f1bae0e` and `ec08555` added the AU analysis, reporting crosswalk, and the
  decision to keep TSA-prefixed model AUs.
- The work went directly to `main`. There was no feature branch, phase issue
  tree, ADR set, changelog, dashboard, or close-out report. P0 retrofits those
  surfaces without changing the model.

### P0.1-P0.5 workflow retrofit

- Added the agent contract, contribution guide, notes index, ADRs, changelog,
  docs index, validator, green dashboard, tests, CI, and issue templates.
- Reconciled issue `#1` as the planned P1 phase and created the P0 parent `#2`
  with child issues `#3` through `#8`.
- Moved the model build and analysis entry points to `pipeline/`; `scripts/`
  now contains workflow tooling only.
- The model, curves, THLB, AAC, and derived benchmark are unchanged.
- Gate scope: the strict lint, type, docstring, and coverage gates apply to
  `scripts/` and `tests/`. The `pipeline/` entry points are excluded because they
  are data-pipeline code validated by execution and `ws4 validate`, not library
  code. This is a deliberate gate-scope decision recorded in ADR 0005.

### P0.6 verification and close-out queue

- `python scripts/dashboard.py`: green on all six gates (lint, format, types,
  tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- CI run `40169934846` passed all three jobs: Quality gates, Pre-commit parity,
  and Green dashboard summary.
- Pull request #9 is open with `Part of #2`. The P0 close-out report is queued in
  `notes/reports/p0-closeout.md`.
- The model, curves, THLB, AAC, and derived benchmark are unchanged.
