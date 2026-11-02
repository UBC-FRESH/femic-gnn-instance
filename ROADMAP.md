# FEMIC GNN Instance Roadmap

This roadmap is the plan of record and the issue tracker map for the GNN
instance. Keep it in step with the GitHub issues, `CHANGE_LOG.md`, and `notes/`.
`scripts/check_workflow.py` parses the phase headers, status lines, and
checkboxes below, so keep their format.

Every phase starts as `planned` with `Parent issue: TBD`. Activate a phase only
after its parent issue exists and the maintainer approves it.

## Issue Tracker Map

| Phase | Parent issue | Branch | Status |
| --- | --- | --- | --- |
| P0 Bootstrap and workflow retrofit | #2 | `feature/p0-bootstrap` | complete |
| P1 Validation and hardening | #1 | `feature/p1-validation-hardening` | complete |
| P2 Release and hand-off | #17 | `feature/p2-release` | complete |
| P3 Operability, cost, and net revenue | #22 | `feature/p3-operability-cost-revenue` | complete |
| P4 FHOPS-native marine transport | #30 | `feature/p4-fhops-marine` | complete |
| P5 GNN marine geography and terminal data | #33 | `feature/p5-marine-data` | complete |
| P6 Quatsino Sound to Ladysmith public-route proxy | #36 | `feature/p6-marine-proxy` | complete |
| P7 Solved multi-day marine transport | #39 | `feature/p7-solved-marine` | complete |
| P8 Solved-proxy full-THLB sensitivity | #42 | `feature/p8-proxy-sensitivity` | complete |
| P9 LiDAR-derived indicators | #45 | `feature/p9-lidar-indicators` | complete |
| P10 Documentation and provenance refresh | #49 | `feature/p10-docs-refresh` | complete |
| P11 CWH inventory diagnostic and forest-condition handoff | #74 | `feature/p11-cwh-inventory-diagnostic` | complete |
| P12 GNN point-cloud inventory feasibility | #77 | `feature/p12-pointcloud-feasibility` | complete |
| P13 GNN point-cloud acquisition request | #80 | `feature/p13-pointcloud-acquisition-request` | complete |
| P14 Private LiDAR ingest readiness | #83 | `feature/p14-private-lidar-ingest` | complete |
| P15 Private LiDAR dry run and fit pre-registration | #87 | `feature/p15-private-lidar-dry-run` | complete |
| P16 Private LiDAR fit pipeline | #91 | `feature/p16-private-lidar-fit` | active |

## Lifecycle Map

| Stage | Phases | Exit criteria |
| --- | --- | --- |
| Bootstrap | P0 | Workflow surfaces, issue tree, ADRs, changelog, and gates are in place; the prototype is unchanged |
| Validation and hardening | P1 | Boundary review, ground-plot evidence, SI/origin decision, THLB/AAC decision, and release gate are recorded |
| Release and hand-off | P2 | Release notes, approval, and a clean-checkout verification are complete |

## Conventions

- A phase is `P<n>`. A task is `P<n>.<m>`. A subtask is a checklist item inside the task's issue body. Three levels at most.
- Status values are `planned`, `active`, `pr-open`, `complete`, and `deferred`.
- A phase becomes `complete` only after its pull request merges to `main` and its parent issue closes.
- `scripts/` holds workflow tooling. `pipeline/` holds model build and analysis entry points.
- The model is a prototype. The boundary is the proposed GNN Statement of Intent polygon, and the THLB and AAC are derived, non-legal values.

## Phase 0: Bootstrap and workflow retrofit

Parent issue: #2
Branch: `feature/p0-bootstrap`
Status: complete

Goal: bring the GNN instance into the UBC-FRESH dev workflow without changing
the prototype model, and queue a reviewable close-out.

- [x] P0.1 Add the workflow contract and quality gates (#3)
  - [x] Add `AGENTS.md`, `CONTRIBUTING.md`, and `CHANGE_LOG.md`.
  - [x] Add the notes index, ADR template, and close-out template.
  - [x] Add the validator, dashboard, tests, and CI.
  - [x] Add `docs/llms.txt` and the API reference pages.
- [x] P0.2 Retrofit the roadmap and GitHub issue tree (#4)
  - [x] Add phase metadata, unique task IDs, and acceptance criteria.
  - [x] Reconcile issue `#1` as the planned P1 parent.
  - [x] Link the P0 child issues to parent `#2`.
- [x] P0.3 Record the prototype decisions as ADRs (#5)
  - [x] Record the proposed boundary and derived THLB/AAC.
  - [x] Record the TSA-prefixed AU decision.
  - [x] Record the no-AAC-tuning rule.
  - [x] Record the workflow/pipeline separation.
- [x] P0.4 Separate pipeline scripts from workflow scripts (#6)
  - [x] Move the domain entry points to `pipeline/`.
  - [x] Update the build-script paths.
  - [x] Update docs and notes references.
- [x] P0.5 Reconstruct the changelog and docs index (#7)
  - [x] Reconstruct the pre-retrofit prototype entry.
  - [x] Add the P0 entry.
  - [x] Add `docs/llms.txt` and API pages.
  - [x] Correct the README status and reading paths.
- [x] P0.6 Verify with the dashboard and CI, then queue the close-out (#8)
  - [x] Run the dashboard, validator, and docs build.
  - [x] Open the phase pull request and confirm CI.
  - [x] Write and post the P0 close-out report.

Acceptance criteria:

- `python scripts/check_workflow.py` reports 0 errors.
- `python scripts/dashboard.py` is green.
- `sphinx-build -b html docs _build/html -W` is green.
- CI passes on the phase branch.
- The model, curves, THLB, AAC, and derived benchmark are unchanged.
- Issue `#1` is reconciled as the planned P1 parent.
- The P0 close-out report is queued and not merged.

## Phase 1: Validation and hardening

Parent issue: #1
Branch: `feature/p1-validation-hardening`
Status: complete

Goal: harden the prototype with reviewed boundary inputs, better ground-plot
evidence, an explicit SI/origin decision, and a documented THLB/AAC status. Do
not tune curves to the derived AAC.

- [x] P1.1 Confirm the proposed SOI boundary and public-output plan (#10)
  - [x] Record the review outcome or the blocking question. Outcome: deferred by the maintainer; no external review is being sought.
  - [x] Keep the public site labelled prototype. The proposed-boundary and derived/non-legal labels remain.
  - Note: deferred, not confirmed. The packet is prepared and retained; no GNN confirmation is claimed.
- [x] P1.2 Expand GNN-area ground-plot validation (#11)
  - [x] Filter public plots to the GNN AOI.
  - [x] Report sample size, source, and bias by type.
  - [x] State whether the evidence supports an accuracy conclusion.
- [x] P1.3 Resolve the TSA 46 SI/origin accuracy issue with the base-model owner (#12)
  - [x] Link the base-model issue.
  - [x] Record the GNN consequence for the dominant CWH_CW H cell.
  - [x] Do not merge AUs to hide the difference.
- [x] P1.4 Decide the derived THLB/AAC status (#13)
  - [x] Keep the derived values labelled non-legal.
  - [x] Decide whether a reviewed netdown is required before release.
- [x] P1.5 Diagnose the decade-10 schedule miss without curve tuning (#14)
  - [x] Test schedule/seed sensitivity only.
  - [x] Record whether the miss is capacity, ordering, or data.
- [x] P1.6 Make the UI/docs release gate and close out P1 (#15)
  - [x] Confirm the UI and docs caveats.
  - [x] Queue the P1 close-out report.

Acceptance criteria:

- The boundary and public-output review is recorded or explicitly blocked.
- The GNN-area ground-plot evidence is expanded or the limitation is stated with counts.
- The TSA 46 SI/origin issue is linked and its GNN consequence is recorded.
- The THLB/AAC status is decided and labelled.
- The decade-10 miss has a cause or a recorded unresolved state.
- No curve or AAC target is changed to fit the benchmark.

## Phase 2: Release and hand-off

Parent issue: #17
Branch: `feature/p2-release`
Status: complete

Goal: release the prototype only after the P1 gates and a separate approval.

- [x] P2.1 Write release notes and the known-gaps list (#18)
  - [x] State the proposed boundary, derived THLB/AAC, and validation limits.
  - [x] List the known gaps and deferred review.
- [x] P2.2 Tag, publish, and verify from a clean checkout (#19)
  - [x] Tag and publish a pre-release.
  - [x] Verify the published docs and a clean checkout.

Acceptance criteria:

- The release notes carry the non-legal and proposed-boundary labels.
- The tag, release, and settings changes were each approved separately.
- A clean checkout reproduces the documented verification.

## Phase 3: Operability, cost, and net revenue

Parent issue: #22
Branch: `feature/p3-operability-cost-revenue`
Status: complete

Goal: make block operability, harvest cost, haul/barge cost, grade/sort
revenue, and net revenue first-class. A scenario may not be labelled
"sustainable" unless it is operable and financially assessed.

- [x] P3.1 Audit operability and cost/revenue data (#23)
  - [x] Audit FHOPS capabilities and gaps.
  - [x] Audit GNN block attributes.
  - [x] Audit public terrain/access/barge data.
  - [x] Audit price/sort data.
  - [x] Write the gap list.
- [x] P3.2 Define the per-block-per-treatment cost/revenue contract (#24)
  - [x] Write the contract schema.
  - [x] Add a synthetic contract fixture.
  - [x] Record the ws4/FHOPS boundary.
- [x] P3.3 Build grade/sort decomposition and the price deck (#25)
  - [x] Define the sort/grade taxonomy.
  - [x] Build a recovery matrix with provenance.
  - [x] Build the price deck with date and source.
  - [x] Run a sensitivity case.
  - Note: met with limits; second-growth cypress is a proxy and recovery is an assumption.
- [x] P3.4 Implement FHOPS harvest, haul, and barge cost estimates (#26)
  - [x] Install FHOPS and validate a sample scenario.
  - [x] Build the block/system cost bridge.
  - [x] Add haul and barge assumptions.
  - [x] Produce a cost table with provenance.
  - Note: met with limits; FHOPS hauling is truck-only (#187) and barge remains a legacy diagnostic rate.
- [x] P3.5 Integrate net revenue and define the sustainable gate (#27)
  - [x] Add net revenue outputs.
  - [x] Add the operability and financial gate.
  - [x] Run base and sensitivity cases.
  - [x] Record the full-THLB screening result; decade-level financial gate deferred.
  - Note: diagnostic screen, not a per-decade financial schedule.
- [x] P3.6 Validate, document, and close out P3 (#28)
  - [x] Validate cost/revenue coverage.
  - [x] Update docs and release caveat.
  - [x] Write and post the P3 close-out.

Acceptance criteria:

- Every scheduled block has an explicit operability class, harvest system, landing/access assumption, and cost record.
- Cable and helicopter blocks are identified and costed, not hidden in an average.
- Haul and barge costs are explicit and sourced.
- Volume is decomposed into species/grade/sort assortments with a documented price deck.
- The scenario reports gross revenue, harvest cost, haul/barge cost, net revenue, and NPV.
- A "sustainable" label requires the operability and financial gates, not just volume.
- The current release is clearly marked volume-only until those gates pass.

## Phase 4: FHOPS-native marine transport

Parent issue: #30
Branch: `feature/p4-fhops-marine`
Status: complete

Goal: replace the legacy barge constant as the only transport path with a
solved FHOPS Phase I marine transport adapter, while keeping the legacy path
and the published screen reproducible. The FHOPS fixture is an upstream
Sunshine Coast -> Howe Sound API test, not the GNN geography, terminal inventory,
or a current quote.

- [x] P4.1 Wire FHOPS marine transport into the GNN cost pipeline (#31)
  - [x] Add the FHOPS marine scenario bundle and provenance.
  - [x] Add the phase I adapter and fixed-dispatch accounting.
  - [x] Add low/base/high utilisation cases.
  - [x] Add opt-in screen paths and retain legacy.
  - [x] Run the adapter and full-THLB sensitivity.
  - [x] Update docs, changelog, and close out the task.

Acceptance criteria:

- The FHOPS marine fixture solves from the adapter.
- The adapter reports water volume, barge trips, drayage, barge variable,
  terminal handling, fixed dispatch, total, and cost per m3.
- The screens can select `fhops-marine` and still reproduce legacy.
- FHOPS commit, scenario, volume basis, and data status are recorded.
- No sustainable, profitable, or current-quote claim is added.
- Dashboard and validator are green.

Closeout requirement: a P4 report with the FHOPS commit, solved cases, screen
sensitivity, provenance, limits, and the next recommendation. The maintainer
approves before merge.

## Phase 5: GNN marine geography and terminal data

Parent issue: #33
Branch: `feature/p5-marine-data`
Status: complete

Goal: establish the actual GNN marine geography and correct the upstream FHOPS
Sunshine Coast -> Howe Sound fixture caveat. Record candidate public terminals
and missing external data without inventing locations, distances, or quotes.

- [x] P5.1 Correct the marine fixture geography and audit candidate GNN terminals (#34)
  - [x] Add a GNN marine geography reference note.
  - [x] Record candidate public infrastructure and uncertainty.
  - [x] Record missing terminal/route/quote data.
  - [x] Correct the fixture labels in config, adapter, notes, and docs.
  - [x] Run dashboard, validator, and docs.

Acceptance criteria:

- The GNN AOI geography and fixture mismatch are documented.
- Public infrastructure is labelled candidate, not a confirmed log-barge terminal.
- The fixture is labelled an API/cost-path test, not a GNN transport estimate.
- The published legacy screen is unchanged.
- No invented terminal, route, rate, or sustainable claim is added.

Closeout requirement: a P5 report with geography evidence, candidate-terminal
sources, missing-data list, and the next decision. The maintainer approves
before merge. P5 does not authorize a GNN-specific scenario or a transport
switch.

## Phase 6: Quatsino Sound to Ladysmith public-route proxy

Parent issue: #36
Branch: `feature/p6-marine-proxy`
Status: complete

Goal: build a labelled GNN-specific marine proxy using the public Quatsino
Sound -> Ladysmith Harbour log-barge route. Capacity, road legs, terminal
handling, and rates are explicit assumptions; the proxy is not a quote and not
the published base.

- [x] P6.1 Build the Quatsino Sound -> Ladysmith public-route proxy (#37)
  - [x] Add the scenario bundle and config.
  - [x] Record the public route and assumption table.
  - [x] Run the proxy cases.
  - [x] Compare with the P4 API fixture.
  - [x] Update docs/notes and the roadmap/changelog.
  - [x] Run dashboard, validator, and docs.

Acceptance criteria:

- The proxy scenario validates and the adapter solves all cases.
- The note distinguishes public route evidence from assumed rates/capacity.
- The proxy is clearly not the published base.
- No current-quote or sustainable claim is added.
- FHOPS Phase I multi-day limitation is recorded upstream.

Closeout requirement: a P6 report with the public route evidence, assumptions,
solved cases, comparison, FHOPS #196 limitation, and next decision. The
maintainer approves before merge.

## Phase 7: Solved multi-day marine transport

Parent issue: #39
Branch: `feature/p7-solved-marine`
Status: complete

Goal: switch the GNN Quatsino Sound -> Ladysmith proxy from the analytical
workaround to solved FHOPS Phase I now that FHOPS P13 supports multi-day
voyages, compare both paths, and keep the published legacy screen unchanged.

- [x] P7.1 Switch the GNN proxy to solved FHOPS Phase I (#40)
  - [x] Change the proxy config to `mode: solve`.
  - [x] Run the three utilisation cases.
  - [x] Compare solved and analytical components.
  - [x] Update docs, notes, roadmap, and changelog.
  - [x] Run dashboard, validator, and docs.

Acceptance criteria:

- All three solved cases are optimal.
- Solved and analytical costs are compared and documented.
- The published legacy screen is unchanged.
- No current-quote or sustainable claim is added.

Closeout requirement: a P7 report with the solved/analytical comparison,
provenance, and remaining data limits. The maintainer approves before merge.

## Phase 8: Solved-proxy full-THLB sensitivity

Parent issue: #42
Branch: `feature/p8-proxy-sensitivity`
Status: complete

Goal: run the solved Quatsino proxy through the full-THLB screen, carry its
`public_route_assumption_rates` metadata, and compare it with the legacy and P4
API paths without switching the published base.

- [x] P8.1 Run and document the solved-proxy full-THLB sensitivity (#43)
  - [x] Add config-derived transport metadata.
  - [x] Run the solved-proxy full-THLB screen.
  - [x] Compare legacy, API, and proxy shares.
  - [x] Update docs/notes/changelog.
  - [x] Run dashboard, validator, and docs.

Acceptance criteria:

- Proxy output identifies `public_route_assumption_rates`.
- The separate sensitivity output is written locally.
- Legacy, API, and proxy shares are documented.
- The published legacy screen remains unchanged.
- No current-quote or sustainable claim is added.

Closeout requirement: a P8 report with the comparison, provenance, limits, and
next decision. The maintainer approves before merge.

## Phase 9: LiDAR-derived indicators

Parent issue: #45
Branch: `feature/p9-lidar-indicators`
Status: complete

Goal: consume the merged FEMIC LiDAR producer and WS4 LiDAR consumer to add
reviewed `lidar_*` indicators to the GNN compiled dataset, without changing
curves, THLB, AAC, or making a model-improvement claim.

- [x] P9.1 Audit and integrate GNN AOI LiDAR indicators (#46)
  - [x] Count LidarBC coverage and payload size for the GNN AOI.
  - [x] Build the explicit GNN strategic-grid terrain/canopy products.
  - [x] Package and pin the FEMIC bundle; register it in the GNN dataset.
  - [x] Map and integrate the fields into the GNN fragments/blocks.
  - [x] Document the fields, coverage gaps, and reprojection/resampling.
  - [x] Run the GNN workflow, WS4 validation, and close-out checks.
- [x] P9.2 Public-data terrain and canopy indicators (#48)
  - [x] Add a batch Terrarium zoom 12 block/fragment sampler.
  - [x] Aggregate and join the existing VRI checkpoint fields.
  - [x] Validate the public proxies against the 181-fragment LiDAR pilot.
  - [x] Integrate `terrain_*` and `vri_*`; keep `lidar_*` pilot-only.
  - [x] Document source, resolution, gaps, and no-imputation rules.

Acceptance criteria:

- The GNN AOI LiDAR coverage audit is recorded.
- The FEMIC bundle validates and the WS4 registration/validation passes.
- The `lidar_*` fields are present in the GNN compiled dataset and documented.
- Coverage gaps are explicit; no field, biomass, or biodiversity accuracy claim
  is added.
- Public-data proxy fields are present or gaps are explicit; LiDAR remains
  pilot-only.
- Curves, THLB, AAC, and the existing benchmark are unchanged.
- The release remains volume-only.

Closeout requirement: a P9 report with tile counts, payload size, CRS and
resolution choices, field list, coverage gaps, validation output, and the next
decision. The maintainer approves before merge.

## Phase 10: Documentation and provenance refresh

Parent issue: #49
Branch: `feature/p10-docs-refresh`
Status: complete

Goal: make the public documentation and repository record match P9 without
changing the model, curves, THLB, AAC, scenarios, data, or release label.

- [x] P10.1 Refresh public docs and P9 provenance (#50)
  - [x] Add the indicators/provenance page.
  - [x] Correct stale status, terrain, and release claims.
  - [x] Document the optional P9 rebuild path and limits.
  - [x] Update the docs index and agent index.
  - [x] Track the partner data request note.
  - [x] Run the dashboard and docs build.

Acceptance criteria:

- A reader can tell what is model-wide, pilot-only, validated, and unused.
- The P9 scripts and prerequisites are documented.
- The release remains volume-only and the P9 fields remain descriptive.
- The dashboard and docs gates pass.

## Phase 11: CWH inventory diagnostic and forest-condition handoff

Parent issue: #74
Branch: `feature/p11-cwh-inventory-diagnostic`
Status: complete

Goal: apply the published FEMIC CWH INV-01 cards to the existing bounded GNN
LiDAR pilot as a report-only diagnostic, and publish the coverage, predictions,
VRI comparison, and limits without changing the model, curves, THLB, AAC,
schedule, targets, or release label.

- [x] P11.1 Run and publish the GNN CWH inventory diagnostic (#75)
  - [x] Pin the three CWH cards and bundle in `config/inventory/cwh_pilot.yaml`.
  - [x] Add the reproducible pipeline entry point.
  - [x] Derive the 25 m features and apply the three cards with explicit range filtering.
  - [x] Record the fragment join, VRI comparison, and limits.
  - [x] Publish the report-only forest-condition card.
  - [x] Add the report and docs page.
  - [x] Update the roadmap and changelog.
  - [x] Run the dashboard and queue the phase pull request.

Acceptance criteria:

- The validated bundle is used unchanged.
- Retained and dropped cells are recorded for every card.
- The report labels the VRI comparison descriptive and states the 14-plot CWH limits.
- No curve, THLB, AAC, target, schedule, matrix, or release value changes.
- The dashboard is green.

## Phase 12: GNN point-cloud inventory feasibility

Parent issue: #77
Branch: `feature/p12-pointcloud-feasibility`
Status: complete

Goal: decide whether the GNN AOI has enough public FAIB plots and LidarBC
point-cloud coverage to justify a GNN-specific first-return inventory pilot, and
publish a go/no-go audit without acquiring data or changing the model.

- [x] P12.1 Audit GNN-area FAIB plots and LidarBC point-cloud coverage (#78)
  - [x] Summarize the FAIB plots in the GNN AOI.
  - [x] Summarize the point-cloud tiles and footprint.
  - [x] Measure plot-to-point-cloud overlap and nearest distances.
  - [x] Publish the go/no-go report and machine-readable summary.
  - [x] Update the inventory-pilot page, roadmap, and changelog.
  - [x] Run the dashboard and queue the phase pull request.

Acceptance criteria:

- The report records plot counts, BEC composition, recent plots, tile years,
  footprint, and AOI share.
- The report records the overlap count and nearest-plot distances.
- The decision is explicit and names the missing acquisition or plot evidence.
- No point cloud is downloaded, no card is fit, and no model value changes.
- The dashboard is green.

## Phase 13: GNN point-cloud acquisition request

Parent issue: #80
Branch: `feature/p13-pointcloud-acquisition-request`
Status: complete

Goal: turn the P12 no-go result into a concrete acquisition request for GNN-area
point clouds over the recent FAIB plots, without downloading data or changing the
model.

- [x] P13.1 Publish the GNN point-cloud acquisition request (#81)
  - [x] Extend the feasibility script with the request table.
  - [x] Generate the 24-plot request table and 8 recent flags.
  - [x] Write the partner-facing memo.
  - [x] Link the request from the docs and partner note.
  - [x] Update the roadmap/changelog and queue the PR.

Acceptance criteria:

- The request table covers 24 plots, flags 8 recent, and records nearest-tile distance.
- Each row has a 2 km EPSG:3005 bbox and area.
- The memo states the current gap and what acquisition would unblock.
- No point cloud is downloaded, no card is fit, and no model value changes.
- The dashboard is green.

## Phase 14: Private LiDAR ingest readiness

Parent issue: #83
Branch: `feature/p14-private-lidar-ingest`
Status: complete

Goal: make the pending private GNN LiDAR upload turnkey and auditable, and clarify
that the P13 public/partner request is a fallback for plots the private upload does
not cover.

- [x] P14.1 Add the private LiDAR ingest and verification kit (#84)
  - [x] Add the read-only ingest script and runbook.
  - [x] Add the synthetic LAS/GeoJSON/request fixture test.
  - [x] Record the private-raw/public-derived governance decision.
  - [x] Run the test and dashboard.
  - [x] Queue the phase pull request.
- [x] P14.2 Clarify the P13 request for the pending private upload (#85)
  - [x] Update the P13 memo.
  - [x] Update the partner data request note.
  - [x] Record the empty-collection check.
  - [x] Queue the phase pull request.

Acceptance criteria:

- The ingest kit runs read-only and writes a private summary plus an optional public
  summary and tile index.
- It reports manifest status, optional hash mismatches, CRS, bounds, points, density,
  AOI coverage, and P13 plot coverage.
- The synthetic test passes without private data.
- The P13 memo and partner note state the private upload is pending and the public
  request is a fallback.
- The dashboard is green.

## Phase 15: Private LiDAR dry run and fit pre-registration

Parent issue: #87
Branch: `feature/p15-private-lidar-dry-run`
Status: complete

Goal: prove the first-return feature step on a synthetic LAS/DEM and pre-register the
fit, holdout, and derived-public product plan before the private upload arrives.

- [x] P15.1 Run the synthetic private LiDAR dry run (#88)
  - [x] Build the synthetic LAS/DEM fixture.
  - [x] Run the first-return feature extraction.
  - [x] Record the output and FEMIC version requirement.
  - [x] Update the ingest runbook.
  - [x] Queue the phase pull request.
- [x] P15.2 Pre-register the fit, holdout, and derived-public products (#89)
  - [x] Write the fit and holdout plan.
  - [x] Write the derived-public product manifest.
  - [x] Link the plan from the inventory-pilot page.
  - [x] Queue the phase pull request.

Acceptance criteria:

- The dry run produces a non-empty feature table with the INV-01 predictors.
- The report records the command and the FEMIC version requirement.
- The fit plan names LOOCV, spatial-cluster, and temporal checks.
- The derived-public product list is explicit and consistent with ADR 0007.
- No real private LAZ is read and no model is fit.
- The dashboard is green.

## Phase 16: Private LiDAR fit pipeline

Parent issue: #91
Branch: `feature/p16-private-lidar-fit`
Status: active

Goal: implement the pre-registered fit and holdout pipeline with a synthetic
end-to-end test before the private upload arrives.

- [x] P16.1 Add the private LiDAR fit pipeline and synthetic test (#92)
  - [x] Add the fit pipeline.
  - [x] Add the synthetic end-to-end test.
  - [x] Add the runbook and report.
  - [x] Update the pipeline index and docs.
  - [x] Run the test and dashboard.
  - [x] Queue the phase pull request.

Acceptance criteria:

- The pipeline matches plots to features or accepts a plot-feature table.
- It fits the three pre-registered forms and reports LOOCV, spatial-cluster, and
  optional temporal metrics.
- It refuses cards on coefficient sign changes unless forced.
- Cards use `femic.inventory.als.model.v1` and research-only caveats.
- The synthetic test passes without private data.
- The dashboard is green.

## Post-P10 economics and access evidence

Status: complete

The published base remains the volume-only prototype. The following work created
candidate and diagnostic evidence only:

- [x] Block-level direct-revenue screen (#58, merged #59)
- [x] Negative-block removal diagnostic (#60, merged #61)
- [x] Positive-block candidate schedule (#62, merged #63)
- [x] Block revenue review map (#64, merged #63)
- [x] Candidate shared-cost headroom (#65, merged #66)
- [x] Public access exposure (#67, merged #68)
- [x] Candidate risk register (#70, merged #71)

Reports: `notes/reports/block-level-revenue-screen.md`,
`block-exclusion-scenario.md`, `positive-block-schedule.md`,
`shared-cost-headroom.md`, `access-exposure.md`, and
`candidate-risk-register.md`.

No model, curve, THLB, AAC, target, or benchmark change was made.

## Detailed Next Steps Notes

1. P0-P2 are complete; `v0.1.0-prototype` is a volume-only pre-release.
2. P3 is complete as a **diagnostic** operability/cost/revenue screen, not a release.
3. Full-THLB legacy screening: 95.5% positive base, 88.0-96.8% range; class-average costs, coarse DEM, provisional recovery, legacy transport.
4. FHOPS #187 is resolved. The P4 API fixture is Sunshine Coast -> Howe Sound; it is not a GNN route and is no longer presented as a GNN transport sensitivity in public docs.
5. P4 is complete as a diagnostic transport integration. The published screen remains the legacy comparison.
6. P5 is complete: the GNN AOI is northern Vancouver Island, while the FHOPS fixture is Sunshine Coast -> Howe Sound. The fixture is an API test, not a GNN route. Candidate terminals and missing quote data are recorded without inventing data.
7. P6 is complete: the public Quatsino Sound -> Ladysmith route proxy is diagnostic only. Cases are 8.125/9.203/11.360 CAD/m3 at 100/75/50% utilisation, with assumed capacity and rates.
8. P7 is complete: the proxy now runs as a solved FHOPS Phase I case after FHOPS P13; solved and analytical results match. The published screen remains legacy; current terminal/rate data is still required.
9. P8 is complete: the solved proxy full-THLB sensitivity is 89.1% low / 95.7% base / 96.8% high, versus legacy 88.0/95.5/96.8 and the P4 API 90.2/95.8/97.0. It is diagnostic only.
10. P9 is **complete** (merged as `612a9c5`): the reviewed `lidar_*` fields are integrated as a **bounded southern pilot** (181 direct fragments, 184 blocks, 978.63 ha), not a GNN-wide layer. See `notes/reports/p9-lidar-indicators.md`. P9.2 (#48) is the public-data fallback: Terrarium zoom 12 and VRI are integrated as **descriptive proxies**; validation against the LiDAR pilot is weak (Terrarium slope bias -13.66 points, MAE 13.97; VRI height MAE 4.09 m), so they are not promoted into operability thresholds. See `notes/reports/p9.2-public-data-indicators.md`. This is a data/feature integration, not a model-improvement claim.
11. No release change or sustainable label is authorized by P4-P10.
12. Post-P10 diagnostics are complete: block screen, removal test, positive candidate schedule, headroom, access exposure, and risk register. The base schedule and benchmark remain unchanged. Shared-cost, carrier, recovery, price, and field data are still required.
13. P11 is complete: the published CWH INV-01 cards were applied to the bounded GNN LiDAR pilot as a report-only diagnostic. The 25 m feature table has 22,139 cells; after range filtering, height retains 21,666 cells and BA/volume retain 21,995 cells. The joined footprint is 181 fragments / 181 blocks / 1,317.8 ha by cell area. Fragment-level VRI comparison is weak (height bias +3.56 m, RMSE 5.90 m, correlation -0.027; volume bias +57.82 m3/ha, RMSE 284.99, correlation -0.062), so the cards are not a GNN calibration and do not enter the model. See `notes/reports/p11-cwh-inventory-diagnostic.md`.
14. P12 is complete: the GNN point-cloud feasibility audit is a **no-go** for a local first-return pilot from current public data. The AOI has 24 FAIB plots (22 CWH, 2 MH) and 8 since 2018, but 755 point-cloud tiles cover only 1.10% of the AOI and no plot falls inside a tile; the nearest recent plot is 32.7 km away. See `notes/reports/p12-pointcloud-inventory-feasibility.md`. A local fit needs point clouds over the recent plots, or recent plots inside the existing footprint.
15. P13 is complete: the GNN point-cloud acquisition request covers the 24 FAIB plots in the AOI (8 recent, 16 secondary), with 2 km EPSG:3005 request bboxes. The recent-plot union is 8,661.3 ha; all plots union 17,613.9 ha. Nearest recent tile gap: 32.7 km. See `notes/reports/p13-pointcloud-acquisition-request.md`.
16. P14 is complete: the private LiDAR ingest kit is ready in `pipeline/ingest_private_lidar.py`, with a private/public output split under ADR 0007. The P13 request is a fallback for plots the pending private upload does not cover. The Globus `/incoming/` and `/manifests/` directories were empty on 2026-11-02.
17. P15 is complete: the synthetic point-cloud dry run produces 7 first-return cells with `Lhmean`, `Lhcv`, `Lhp95`, and `CC2m`; the fit plan pre-registers LOOCV, four spatial clusters, and a 2022/2023 temporal check. The installed local FEMIC lacks `inventory-pointcloud-features`; use `origin/main` or newer. See `notes/reports/p15-private-lidar-dry-run.md` and `notes/reports/p15-fit-preregistration.md`.
18. P16 is active: `pipeline/fit_inventory_cards.py` implements the P15 fit forms, LOOCV, spatial clusters, temporal transfer, coefficient-stability checks, and optional FEMIC cards. The synthetic test covers 12 plots in four clusters. See `notes/reports/p16-fit-pipeline.md`.
