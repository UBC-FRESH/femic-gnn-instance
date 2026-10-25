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
### P1 activation

- P0 merged as `f9a11c5`; parent #2 and child #3-#8 are closed.
- P1 is active on `feature/p1-validation-hardening`; parent #1 and child
  #10-#15 are linked.
- The first task is P1.1: prepare the boundary and public-output review packet.
  GNN confirmation is external and blocking.
### P1.1 boundary and public-output review packet

- Added `notes/reference/gnn-review-packet.md` with boundary provenance, the
  public-output inventory, review questions, and the no-confirmation rule.
- Added `docs/review.html` to the public docs and linked it from the docs index
  and `docs/llms.txt`.
- P1.1 remains open: the packet is prepared, not sent, and no GNN confirmation
  has been received.
### P1.2 public-plot inventory and PSP check

- Inventory found 51 public sites inside the GNN AOI: 24 PSP (17 PSP_R, 7 PSP_G)
  and 27 non-PSP (22 VRI/CMI/NFI, 4 CMI/YSM, plus the south CMI/NFI set).
- The filtered PSP check produced 55 observations from 12 sites. Median age is
  101 years; PSP_R is experimental and PSP_G is natural growth, so this is not a
  managed-young TIPSY benchmark.
- The non-PSP matched sample remains 34 rows / 10 sites. The combined evidence is
  still too sparse for a GNN-specific managed-curve accuracy conclusion.
- Added `config/tsr/gnn_ground_plot_inventory.csv`,
  `config/tsr/gnn_psp_validation_tsa46.csv`, and the summary table.
- No curve, THLB, AAC, or benchmark change.
### P1.3 inherited TSA 46 SI/origin issue

- Opened base-model issue `UBC-FRESH/femic#343` for the TSA 46 checkpoint SI
  understatement in managed stands.
- Recorded the GNN exposure: TSA 46 is 34.7% of the derived THLB; CWH_CW H is
  13.9%, CWH_CW M 7.1%, and CWH_HW H 5.3%.
- Kept TSA-prefixed AUs; no managed-SI switch and no AAC tuning. The base issue
  remains an open dependency.
