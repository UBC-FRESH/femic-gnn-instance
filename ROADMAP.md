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
| P3 Operability, cost, and net revenue | #22 | `feature/p3-operability-cost-revenue` | active |

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
Status: active

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
- [ ] P3.3 Build grade/sort decomposition and the price deck (#25)
  - [ ] Define the sort/grade taxonomy.
  - [ ] Build a recovery matrix with provenance.
  - [ ] Build the price deck with date and source.
  - [ ] Run a sensitivity case.
- [ ] P3.4 Implement FHOPS harvest, haul, and barge cost estimates (#26)
  - [ ] Install FHOPS and validate a sample scenario.
  - [ ] Build the block/system cost bridge.
  - [ ] Add haul and barge assumptions.
  - [ ] Produce a cost table with provenance.
- [ ] P3.5 Integrate net revenue and define the sustainable gate (#27)
  - [ ] Add net revenue outputs.
  - [ ] Add the operability and financial gate.
  - [ ] Run base and sensitivity cases.
  - [ ] Record pass/fail per decade.
- [ ] P3.6 Validate, document, and close out P3 (#28)
  - [ ] Validate cost/revenue coverage.
  - [ ] Update docs and release caveat.
  - [ ] Write and post the P3 close-out.

Acceptance criteria:

- Every scheduled block has an explicit operability class, harvest system, landing/access assumption, and cost record.
- Cable and helicopter blocks are identified and costed, not hidden in an average.
- Haul and barge costs are explicit and sourced.
- Volume is decomposed into species/grade/sort assortments with a documented price deck.
- The scenario reports gross revenue, harvest cost, haul/barge cost, net revenue, and NPV.
- A "sustainable" label requires the operability and financial gates, not just volume.
- The current release is clearly marked volume-only until those gates pass.

## Detailed Next Steps Notes

1. P0-P2 are complete; `v0.1.0-prototype` is a volume-only pre-release.
2. P3 is active on `feature/p3-operability-cost-revenue`; parent #22 and child #23-#28 are linked.
3. P3.1 audit is complete: FHOPS is the harvest-cost engine, but price/barge/operability data and a contract are still missing.
4. P3.2-P3.6 follow; no "sustainable" label until the operability and financial gates pass.
5. Do not invent prices, slopes, barge rates, or recovery assumptions.
