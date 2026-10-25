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
| P1 Validation and hardening | #1 | `feature/p1-validation-hardening` | active |
| P2 Release and hand-off | TBD | `feature/p2-release` | planned |

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
Status: active

Goal: harden the prototype with reviewed boundary inputs, better ground-plot
evidence, an explicit SI/origin decision, and a documented THLB/AAC status. Do
not tune curves to the derived AAC.

- [ ] P1.1 Confirm the proposed SOI boundary and public-output plan (#10)
  - [ ] Record the GNN review outcome or the blocking question.
  - [ ] Keep the public site labelled prototype until confirmed.
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
- [ ] P1.6 Make the UI/docs release gate and close out P1 (#15)
  - [ ] Confirm the UI and docs caveats.
  - [ ] Queue the P1 close-out report.

Acceptance criteria:

- The boundary and public-output review is recorded or explicitly blocked.
- The GNN-area ground-plot evidence is expanded or the limitation is stated with counts.
- The TSA 46 SI/origin issue is linked and its GNN consequence is recorded.
- The THLB/AAC status is decided and labelled.
- The decade-10 miss has a cause or a recorded unresolved state.
- No curve or AAC target is changed to fit the benchmark.

## Phase 2: Release and hand-off

Parent issue: TBD
Branch: `feature/p2-release`
Status: planned

Goal: release the prototype only after the P1 gates and a separate approval.

- [ ] P2.1 Write release notes and the known-gaps list
  - [ ] State the proposed boundary, derived THLB/AAC, and validation limits.
  - [ ] List the GNN review outcome.
- [ ] P2.2 Tag, publish, and verify from a clean checkout
  - [ ] Obtain approval for the tag, release, and any settings change.
  - [ ] Verify the published docs and model artifacts.

Acceptance criteria:

- The release notes carry the non-legal and proposed-boundary labels.
- The tag, release, and settings changes were each approved separately.
- A clean checkout reproduces the documented verification.

## Detailed Next Steps Notes

1. P0 is complete: PR #9 merged as `f9a11c5`; dashboard and CI were green.
2. P1 is active on `feature/p1-validation-hardening`; child issues #10-#15 are linked to parent #1.
3. Start with P1.1: prepare the boundary/public-output review packet. Do not claim GNN confirmation.
4. P1.2-P1.5 follow; no curve or target tuning.
