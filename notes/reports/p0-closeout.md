# Phase close-out report: P0 Bootstrap and workflow retrofit

Phase: P0 Bootstrap and workflow retrofit
Parent issue: #2
Pull request: #9, `feature/p0-bootstrap` into `main`
Evidence head: `c23eb54`, the code head that the gates and CI runs below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: approved by the maintainer on 2026-10-25. Merge queued.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back
each result.

1. Squash-merge pull request #9, and delete the branch `feature/p0-bootstrap`.
2. Post closeout comments on child issues #3 through #8 and close them.
3. Close parent issue #2 with a closeout comment that cites the merge commit.
4. Launch P1: create `feature/p1-validation-hardening`, set P0 to `complete` and P1 to `active` in `ROADMAP.md`, create the P1 child issues as sub-issues, and start P1.1.
5. After the GNN merge, update the `femic` submodule pointer and comment on `femic#341`. That pointer update follows the `femic` review and merge rules, not this PR.

Settings changes, each with its exact command. Each one runs only after its own
approval.

- None in P0. Pages was enabled before this close-out existed; it is disclosed as
  a deviation, not repeated here.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Workflow contract and quality gates exist | `AGENTS.md`, `CONTRIBUTING.md`, `CHANGE_LOG.md`, `notes/`, `docs/llms.txt`, `scripts/check_workflow.py`, `scripts/dashboard.py`, `tests/`, `.github/workflows/ci.yml` | met |
| `python scripts/check_workflow.py` reports 0 errors | 0 errors, 0 warnings | met |
| `python scripts/dashboard.py` is green | All six gates green | met |
| Docs build with warnings as errors | Docs gate and CI Quality gates pass | met |
| CI passes on the phase branch | Run `40169934846`, all three jobs pass | met |
| Model, curves, THLB, AAC, and derived benchmark unchanged | `git diff ec08555..c23eb54` changes process, docs, and entry-point paths only; no config values changed except generated-path comments | met |
| Issue #1 reconciled as planned P1 | Issue #1 retitled `P1: Validation and hardening`, labelled `phase`, body rewritten | met |
| P0 child issues linked to #2 | Sub-issues #3, #4, #5, #6, #7, #8 | met |
| P0 close-out report queued and not merged | This report; PR #9 open | met |
| Pre-retrofit prototype decisions recorded as ADRs | ADRs 0001-0005 | met |
| Changelog reconstructs the prototype history | `CHANGE_LOG.md` retrospective entry and P0 entries | met |
| Model artifacts stay out of Git | `runtime/`, `output/`, `data/*.feather`, and bundles are ignored | met |

## 2. Workflow compliance

- **Parent issue before the branch:** parent #2 was created at
  `2026-10-25T06:35:21Z`; branch `feature/p0-bootstrap` was created after that.
- **Branch from `main`:** `feature/p0-bootstrap` starts at `ec08555`.
- **Commit messages start with task IDs:** `c23eb54`
  `P0.1-P0.5 retrofit the GNN instance workflow`; the report commit starts
  `P0.6`.
- **Gates for each commit:** section 3. The integrated code commit is green; the
  docs-only report commit is covered by the PR's CI run.
- **Roadmap and changelog in step:** `ROADMAP.md` is `pr-open` with every P0
  task checked; `CHANGE_LOG.md` has the retrospective and P0 entries.
- **Child issues:** #3 through #8 remain open. Closeout comments are posted with
  this report; closure is recommended after the merge.
- **Approval gates:** no tag, release, visibility, branch-protection, or Pages
  setting was changed in P0. Pages was enabled earlier, outside a close-out;
  section 5 records it.

## 3. Gate evidence

On `c23eb54`:

```text
GATE                STATUS
lint                GREEN
format              GREEN
types               GREEN
tests               GREEN
validator           GREEN
docs                GREEN

OVERALL: GREEN
```

`python scripts/check_workflow.py` reports `0 error(s), 0 warning(s)`.

The tests gate runs the full copied workflow suite, including the validator,
dashboard, CLI, property, and docstring tests. The docs gate runs
`sphinx-build -b html docs _build/html -W -q`.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40169934846` | `c23eb54` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass |

The report-only commit moves the head. Its CI run is posted on PR #9 before the
approval request is treated as current.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The prototype was built directly on `main` with no phase branch, issue tree, ADRs, changelog, dashboard, or close-out | The workflow retrofit started after the prototype | The retrospective changelog entry records the history; P0 adds the missing surfaces; the model is unchanged |
| P0.1-P0.5 share one commit | The seed's gates only turn green when the full workflow surface set exists; committing each task alone would leave red commits | `c23eb54` cites P0.1-P0.5; this report discloses the integration |
| Pages was enabled through the API before a workflow close-out | The earlier prototype work treated the maintainer's "go" as approval without a recorded report item | Disclosed here; no further settings change is requested in P0 |
| Issue #1 was created as an ad hoc Phase 1 issue before the workflow retrofit | It was created as a forward-looking issue, not as a phase parent | Reconciled by retitling, relabelling, and rewriting its body as the planned P1 parent |
| The report commit moves the evidence head | The report must be committed to be reviewed | The PR comment records the report commit and its CI run; the report is not treated as approved until that run is green |

## 6. Next phase

**P1 Validation and hardening** is planned with parent issue #1 and branch
`feature/p1-validation-hardening`.

Recommended tasks and defaults:

- `P1.1` Confirm the proposed SOI boundary and public-output plan with GNN.
  Default: keep the public site labelled prototype until confirmed.
- `P1.2` Expand GNN-area ground-plot validation. Default: use public FAIB plots
  and state the sample size before making an accuracy claim.
- `P1.3` Resolve the TSA 46 SI/origin accuracy issue with the base-model owner.
  Default: link the base-model work; do not merge AUs or tune curves.
- `P1.4` Decide the derived THLB/AAC status. Default: keep both labelled
  non-legal and require a reviewed netdown before operational use.
- `P1.5` Diagnose the decade-10 miss without curve tuning. Default: test
  schedule and seed sensitivity only.
- `P1.6` Make the UI/docs release gate and close out P1. Default: no release
  until P1.1-P1.4 are recorded.

P1 child issues are created on activation, not before. The first bounded move is
P1.1, because the boundary and public-output review is the external gate.

## 7. Decision

- [x] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
