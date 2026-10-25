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
### P3.4 stratified operability and transport assumptions

- Species-stratified pilot: 18.7% ground, 36.2% cable, 45.1% heli candidate by
  volume; 81.3% non-ground. Fir/spruce were not represented at this depth.
- The random 40-block pilot remains 63.1% non-ground. The defensible conclusion
  is a large non-ground share, not one universal percentage.
- Added provisional truck/barge/terminal assumptions with low/base/high ranges;
  every value is `data_status=assumption`.
- Base transport allowance is about 31 CAD/m3 (12 truck + 15 barge + 4 terminal),
  not a quote.
- No net revenue or sustainable label is claimed.
### P3.4 CLEWs/FFCM barge and truck cost evidence

- Found legacy FFCM transport costs in `UBC-FRESH/clews-c2070-fresh`.
- Log barge: 3,000 m3, 25 km/h, 120 CAD/h operating, 18.345 CAD/km fuel,
  4.57 CAD/m3 transload.
- Truck: 46.1 m3, 90 km/h, 120 CAD/h operating, 1.257 CAD/km fuel.
- Derived at 100 km truck + 100 km barge + transload: **10.961 CAD/m3**.
- The source labels these "rough prototype only" and says cost year/assumptions
  are unclear. They are legacy diagnostic, not current quotes.
- Replaced the earlier 31 CAD/m3 placeholder with the legacy diagnostic basis.
### P3.5 screening net revenue ranges

- Ran a range-based net revenue screen for cable/heli blocks using the local
  reviewed price deck, provisional recovery matrix, legacy CLEWs transport, and
  one-machine cable/heli screening costs.
- Random 40-block sample: 25 priced blocks, 229,015 m3; net range +5.21M to
  +50.30M CAD; 0% unprofitable even in the optimistic case.
- Species-stratified sample: 25 priced blocks, 232,482 m3; net range -1.70M to
  +36.32M CAD; 13.1% of priced volume unprofitable even in the best case.
- The range is dominated by price/recovery assumptions. Ground blocks remain
  unpriced. This is **screening only**, not a net revenue or sustainable claim.
- Detailed per-block outputs stay local because the BC price table is not
  redistributable.
### P3.3 local price deck validation

- Manually checked the second-growth cedar/fir/Hembal/spruce rows against the
  BC Coast Log Market Report for 2026-01-31.
- Recorded the local deck SHA-256 and the license/redistribution limit.
- Second-growth cypress is missing; old-growth cypress is only a proxy.
- The deck remains a screening input, not a calibrated netback.
### P3.4 full harvest-system screening costs

- Used the FHOPS harvest-system registry for `ground_fb_skid`,
  `cable_running_sr54`, and `helicopter`.
- Screening system costs: ground 15.37 CAD/m3, cable 17.77 CAD/m3, helicopter
  78.13 CAD/m3, before transport/overhead/profit.
- Added the legacy 100 km transport allowance: ground 26.33, cable 28.73,
  helicopter 89.09 CAD/m3.
- Bottleneck approximation, not a solved FHOPS shift schedule; cablesystem uses
  mechanised felling and may not be safe on the 39% block.
- Added `pipeline/full_system_cost.py`, the sample table, and the note.
### P3.5 positive net revenue share of sampled THLB

- Priced cable/heli THLB in the current screen: 242.5 ha, 0.46% of the derived
  GNN THLB.
- Positive in the best case: 88.5% of priced THLB; worst case: 63.5%.
- Ground THLB in the sample (86.0 ha) remains unpriced.
- This is not a full-THLB fraction; the sample is not representative and uses
  one-machine costs.
### P3.5 full-THLB screening

- Covered all 52,984.43 ha of derived THLB at the VRI checkpoint-polygon level.
- Positive net unit revenue: **95.5% base**; 88.0% low case; 96.8% high case.
- By class: ground 96.6%, cable 97.4%, heli candidate 90.8% positive.
- Sensitivities: 87.8% at 2x harvest cost; 92.3% at 30 CAD/m3 transport.
- Screening only: class-average system costs, coarse DEM, provisional
  prices/recovery, legacy transport. No sustainable label.
### P3.4 FHOPS hauling barge gap

- Tested FHOPS main at `52462d2a` (P11 hauling). The layer is truck-only: no transport mode,
  vessel, port, or barge cycle.
- A barge-named `TruckType` validates as a truck; `haul plan` is infeasible under the truck model.
- Opened upstream issue `UBC-FRESH/fhops#187` with a Sunshine Coast -> Howe Sound fixture and
  acceptance criteria.
- GNN barge transport remains a diagnostic assumption, not a solved FHOPS haul plan.
### P3 close-out queued

- Added `docs/economic-screening.rst` with the full-THLB diagnostic screen.
- P3 is `pr-open`; all tasks are checked with stated limits.
- The release stays volume-only. The screen is not a sustainable or financially
  calibrated result.
- FHOPS barge support remains upstream issue #187.
- P3 PR #29 CI run `40219295693` passed. The close-out report is queued at
  `notes/reports/p3-closeout.md`.
- P3 merged as `fff6435` (PR #29); parent #22 and children #25-#28 are closed. The phase is complete as a diagnostic screen.
### P4 activation and FHOPS marine transport

- Activated P4 on `feature/p4-fhops-marine` (parent #30, task #31).
- `UBC-FRESH/fhops#187` is resolved in `f788d7a6`; FHOPS now models barges, ports, water arcs,
  terminal handling, and barge trips explicitly.
- Added the representative FHOPS Sunshine Coast -> Howe Sound fixture under
  `config/cost_revenue/transport/fhops_marine/` and the adapter
  `pipeline/fhops_marine_transport.py`.
- The adapter solves Phase I at 100/75/50% barge utilisation and adds contract fixed dispatch
  costs: **5.642 / 6.100 / 7.097 CAD/m3** before caveats. The fixture is synthetic, not a quote.
- Added `--transport fhops-marine` to both net revenue screens; legacy remains selectable and
  reproduces the published result exactly.
- Full-THLB sensitivity with FHOPS marine transport: **90.2% low / 95.8% base / 97.0% high**,
  versus legacy 88.0 / 95.5 / 96.8. The published screen remains legacy.
- Added `notes/reference/fhops-marine-transport.md`, updated the barge-gap and transport notes, and
  added the FHOPS sensitivity to `docs/economic-screening.rst`.
- `python scripts/dashboard.py`: GREEN on all six gates. `check_workflow.py`: 0 errors, 0 warnings.
  Sphinx build clean.
- No release, sustainable label, or model change is authorized by P4.
- P4.1 is `pr-open` in PR #32. The P4 close-out report is queued at
  `notes/reports/p4-closeout.md`; no merge, release, or sustainable label is authorized.
- P4 merged as `6a8d94f` (PR #32); task #31 and parent #30 are closed. The phase is complete as a diagnostic transport integration.
### P5.1 marine geography correction

- Confirmed the GNN AOI is northern Vancouver Island (centroid about 51.185 N, -127.408 W),
  not the Sunshine Coast.
- The FHOPS marine fixture is Sunshine Coast -> Howe Sound with an 80 km water leg. It is an
  API/cost-path test, not a GNN transport estimate.
- Added `notes/reference/gnn-marine-geography.md` with candidate public infrastructure, source
  links, uncertainty, the straight-line mismatch check, and the missing terminal/route/quote data.
- Corrected the fixture labels in the transport config, adapter, notes, README, and economic-screening
  docs. Removed the FHOPS full-THLB comparison table from the public screening page.
- Changed the test data status to `upstream_fhops_fixture_api_test`; no published screen, model, or
  sustainable label changed.
- Candidate public infrastructure includes Port Hardy, Port McNeill, Beaver Cove, Coal Harbour,
  Alert Bay, and Port Alice. None is confirmed as a GNN log-barge terminal.
- Current carrier and terminal quotes remain missing and are not public.
- P5.1 is `pr-open` in PR #35. The P5 close-out report is queued at
  `notes/reports/p5-closeout.md`; no published transport switch or model change is authorized.
- P5 merged as `fab4e0a` (PR #35); task #34 and parent #33 are closed. The phase is complete as a geography/data correction; the published transport base remains legacy.
### P6.1 Quatsino Sound to Ladysmith public-route proxy

- Added a diagnostic GNN proxy using the public Quatsino Sound -> Ladysmith Harbour route
  (Seaspan Log Barging 101, 2023) and historical TFL 6 Quatsino Dryland Log Sort / Seaspan
  barging evidence.
- The route is approximately 589 km and 1,910 minutes one way at 10 knots. Barge capacity,
  rates, road legs, terminal handling, and fleet size are explicit assumptions.
- Cases: **8.125 / 9.203 / 11.360 CAD/m3** at 100/75/50% utilisation. The P4 API fixture was
  5.642/6.100/7.097; the proxy is higher because the water leg is much longer.
- FHOPS Phase I cannot solve the 3,955-minute voyage with one barge under its daily fleet
  constraint. Added an analytical proxy from the FHOPS marine lane contract and opened
  `UBC-FRESH/fhops#196`.
- The proxy is labelled `public_route_assumption_rates`; it is not a quote, not the published
  base, and does not authorize a sustainable label.
- Dashboard GREEN, validator 0/0, docs clean.
- P6.1 is `pr-open` in PR #38. The P6 close-out report is queued at
  `notes/reports/p6-closeout.md`; no published transport switch or model change is authorized.
- P6 merged as `c9fcb8c` (PR #38); task #37 and parent #36 are closed. The public-route proxy is complete as a diagnostic; the published transport base remains legacy.

### P7.1 solved Quatsino-Ladysmith marine transport

- Switched the GNN Quatsino Sound -> Ladysmith proxy from the analytical workaround to solved FHOPS
  Phase I after FHOPS P13 landed.
- Solved results: **8.125 / 9.203 / 11.360 CAD/m3** at 100/75/50% utilisation; the analytical
  cross-check matches to the cent.
- Corrected the GNN adapter fixed-cost basis: truck fixed cost uses actual loading/unloading days,
  and barge fixed cost uses the full voyage occupancy.
- Solved voyage: departure day 1, cargo arrival day 5, occupancy 8 days, demand day 8.
- Published legacy screen unchanged; the proxy remains diagnostic and not a quote.
- P7.1 is `pr-open` in PR #41. The P7 close-out report is queued at
  `notes/reports/p7-closeout.md`; no release, tag, or published transport switch is authorized.
