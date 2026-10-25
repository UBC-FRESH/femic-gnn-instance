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
### P1.4 prototype-only THLB/AAC release condition

- Added ADR 0006: the derived THLB and AAC are sufficient for a labelled
  prototype only.
- Operational, legal, or investment use requires a reviewed GNN netdown and an
  explicit AAC decision.
- The P2 release gate must state this condition.
- No curve, THLB, AAC, or benchmark change.
### P1.5 decade-10 diagnostic

- The scheduler is deterministic; no seed exists.
- A band-floor run (2,526,000 m3) still left decade 10 at 2,524,255.0 m3.
- The last period has the most scheduled blocks (866), so the miss is a 100-year
  horizon and age-structure end-effect, not a curve or target error.
- Added `notes/reference/decade10-diagnostic.md` and a docs summary.
- No curve, target, THLB, AAC, or benchmark change.
### P1.6 UI/docs release gate and P1 close-out

- Verified the built docs carry the proposed-boundary and derived/non-legal
  labels; the UI remains loopback-only and is not a public deployment.
- P1.2-P1.5 are complete. P1.1 is deferred: the review packet is prepared, not
  sent, and issue #10 remains open.
- P1 is queued for close-out in PR #16; CI run `40171639796` passed. The report
  is `notes/reports/p1-closeout.md`.
- P2 is not activated until the close-out is approved and the boundary review is
  resolved or explicitly carried forward.
- No model, curve, target, THLB, AAC, or benchmark change.
### P1 merge and P2 activation

- P1 merged as `a3af911` (PR #16); parent #1 is closed. P1.1 was closed as
  deferred by the maintainer; no external review is being sought.
- P2 is active on `feature/p2-release`; parent #17 and child #18/#19 are linked.
- Next: write the release notes and known gaps, then tag and verify a prototype
  pre-release.
### P2.1 release notes and known gaps

- Added `notes/releases/v0.1.0-prototype.md` and a public `docs/release.rst`.
- The notes state the proposed-boundary and derived/non-legal labels, the sparse
  ground-plot evidence, the TSA 46 SI dependency, and the decade-10 end-effect.
- P1.1 is recorded as deferred by the maintainer; no external review is claimed.
- No model, curve, target, THLB, AAC, or benchmark change.
### P2.2 queue the prototype release

- P2 release notes and known gaps are in `notes/releases/v0.1.0-prototype.md`
  and `docs/release.rst`.
- `CITATION.cff` is version `0.1.0`; PR #20 is open with CI run `40172281409`
  passing.
- The P2 close-out is queued at `notes/reports/p2-closeout.md`.
- The tag `v0.1.0-prototype` and GitHub pre-release execute after the merge.
- No model, curve, target, THLB, AAC, or benchmark change.
### P2.2 prototype pre-release

- P2 merged as `ea70b26`; PR #20 is closed.
- Tag `v0.1.0-prototype` published as a GitHub **pre-release**:
  https://github.com/UBC-FRESH/femic-gnn-instance/releases/tag/v0.1.0-prototype
- Pages and `llms.txt` return HTTP 200.
- Clean checkout of `ea70b26`: validator 0 errors, 0 warnings; dashboard 6/6 green.
- CI run `40172423658` and Docs run `40172423704` passed on `main`.
- The release is a prototype, not a legal or operational release.
### P3.1 operability and cost/revenue audit

- Opened P3 with parent #22 and child #23-#28.
- Audited FHOPS: strong harvest-system productivity and machine costing; no
  native coastal log price deck, barge network, or operability classifier.
- Audited GNN data: no slope/terrain, roads/landings, barge terminals, grade
  recovery, or prices in the current block model.
- Recorded that the current release is volume-only and is not an operable,
  financially assessed, or "sustainable" harvest level.
- No price, cost, slope, or recovery value was fabricated.
### P3.2 cost and revenue contract

- Added `docs/cost-revenue-contract.rst` with the block/treatment cost table,
  assortment/price table, validation rules, net revenue formula, and sustainable
  gate.
- Added a synthetic fixture under `config/cost_revenue/synthetic/`, explicitly
  marked `SYNTHETIC_FIXTURE_DO_NOT_USE`.
- Recorded the integration boundary: ws4 supplies volume/area; FHOPS supplies
  harvest system cost; this pipeline supplies operability, haul/barge, sorts,
  prices, and net revenue.
- No GNN price, cost, slope, or recovery value is implied by the fixture.
### P3.3/P3.4 progress: price source and FHOPS smoke test

- Identified the BC Coast Log Market Reports (Vancouver Log Market, species and
  grade, three months ending January 2026) as the primary public price source.
- Recorded the copyright/use limit: keep the extracted deck local and
  gitignored; do not republish the raw BC table.
- Confirmed the FHOPS cost core runs via `PYTHONPATH=src`; the CLI still needs
  `optuna`, and the MIP path needs `pyomo`/`highspy`.
- Ran a synthetic single-machine cost smoke test; it is not a GNN result.
- The grade/sort recovery matrix is still missing; net revenue is not credible
  until it exists.
### P3.3/P3.4 local price deck and FHOPS CLI smoke test

- Added a draft local extractor for the BC Coast Log Market Reports; the first
  run wrote 47 old-growth and 29 second-growth species/grade prices to the
  gitignored `runtime/p3/` path.
- The extraction is **not validated**: merged cells can shift values between
  species columns. No price values are committed.
- FHOPS CLI now runs after installing `optuna`, `pyomo`, and `highspy`; the
  synthetic grapple-yarder estimate is 13.80 CAD/m3 for one machine.
- The grade/sort recovery matrix is still missing; net revenue remains
  incomplete.
### P3.3 provisional recovery matrix

- Added `config/cost_revenue/recovery/recovery_matrix.csv` with species/product
  shares and low/base/high cases.
- Every row is marked `data_status=assumption`; it is not a stand-level GNN
  recovery matrix.
- Cited the BC Cruise Compilation Manual, CGNF spruce tables, and CRHS profiles
  as partial public sources; documented what is still missing.
- The sustainable gate must reject this matrix until observed cruise/mill
  recovery replaces it.
### P3.4 one-block terrain and operability sample

- Sampled block 14379: 17.0 ha, 749.6 m3/ha, 782 stems/ha, 0.959 m3 average
  stem; VRI checkpoint clipped to the block.
- Terrain from AWS Terrarium tiles: 58.75% mean slope, 79.05% p90, 548.9 m mean
  elevation.
- FHOPS's ground-based Lahrsen model rejects the block because 58.75% exceeds
  its 48.9% observed range. The block must be cable/heli-costed.
- Added `config/cost_revenue/samples/block_14379.csv` and
  `notes/reference/block-sample-14379.md`.
- No GNN net revenue or sustainable label is claimed.
### P3.4 cable/heli screening on the real block

- Block 14379: 58.75% mean slope, 749.6 m3/ha; FHOPS ground model rejects it.
- Cable/heli screening: helicopter KMAX 87.09 CAD/m3 at 1000 m; Bell 214B
  59.66 CAD/m3; cable Skylead C40 17.61 CAD/m3; Cypress 7280 37.50 CAD/m3.
- These are one-machine/one-model screening costs, excluding move-in, landing,
  haul, barge, overhead, and profit.
- Added the screening table and updated the block note.
- No GNN net revenue or sustainable label is claimed.
### P3.4 12-block operability pilot

- Random pilot of 12 blocks: 41.6% of sampled volume is non-ground under coarse
  slope thresholds (28.3% cable, 13.2% heli candidate).
- Cable screening 17.61-37.50 CAD/m3; helicopter 59.66-87.09 CAD/m3, before
  move-in, landing, haul, barge, overhead, and profit.
- Added `config/cost_revenue/samples/operability_pilot.csv` and
  `notes/reference/operability-pilot.md`.
- Pilot only: coarse DEM, arbitrary thresholds, one machine/model, provisional
  price/recovery. No net revenue or sustainable label.
### P3.4 40-block operability pilot

- Expanded the pilot from 12 to 40 blocks.
- Volume share: **36.9% ground, 34.8% cable, 28.3% heli candidate**.
- **63.1% of sampled volume is non-ground** under the coarse thresholds.
- Added species composition and per-block screening totals.
- Cable screening 17.61-37.50 CAD/m3; helicopter 59.66-87.09 CAD/m3, before
  access, haul, barge, overhead, or profit.
- Pilot caveats remain: coarse DEM, arbitrary thresholds, one model/machine,
  provisional price/recovery, no net revenue.
