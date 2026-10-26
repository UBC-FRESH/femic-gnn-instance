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
11. No release change or sustainable label is authorized by P4-P9.
