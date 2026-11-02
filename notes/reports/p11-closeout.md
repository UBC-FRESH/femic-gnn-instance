# Phase close-out report: P11 CWH inventory diagnostic and forest-condition handoff

Phase: P11 CWH inventory diagnostic and forest-condition handoff
Parent issue: #74
Pull request: #76, `feature/p11-cwh-inventory-diagnostic` into `main`
Evidence head: `c5d6061`, the commit that adds the diagnostic, report, docs, and roadmap entry
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #76, and delete the branch `feature/p11-cwh-inventory-diagnostic`.
2. Close child issue #75 with a closeout comment that cites the merge commit.
3. Close parent issue #74 with a closeout comment that cites the merge commit.
4. Launch P12 "GNN point-cloud inventory feasibility" only if the maintainer wants to
   continue the inventory track: create its parent and child issues, branch from `main`,
   and start with a bounded coverage/plot audit. If not, leave the phase unstarted.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Use the validated GNN bundle unchanged | `femic lidar inspect` on `lidarbc-1b7b79757e98cfe5` / `2026.10.0-gnn-10m` passed in the diagnostic run; no bundle file changed | met |
| Reproducible feature extraction and card application | `pipeline/cwh_inventory_diagnostic.py`; run output in `notes/reports/p11-cwh-inventory-diagnostic.summary.json` | met |
| Explicit range filtering with retained and dropped counts | height 21,666 retained / 473 dropped; BA and volume 21,995 retained / 144 dropped | met |
| Record prediction summaries, fragment/block/area coverage, VRI comparison, and limits | `notes/reports/p11-cwh-inventory-diagnostic.md`; summary JSON | met |
| No curve, THLB, AAC, target, schedule, matrix, or release change | The change set adds config, a pipeline entry point, a report, and docs only; no runtime/model artifact is tracked | met |
| Dashboard green on the phase head | `python scripts/dashboard.py` -> OVERALL: GREEN at `c5d6061`; rerun after the report commit | met with the stated limit that the report commit's run is the CI run below |

## 2. Workflow compliance

- Parent issue before the branch: issue #74 was created before the branch; child issue
  #75 was created immediately after and linked as a sub-issue.
- Branch from `main`: `feature/p11-cwh-inventory-diagnostic` was created from
  `origin/main` at `ee0e7a3`.
- Commit messages that start with task IDs: one implementation commit, `c5d6061`
  (`P11.1 ...`), and the report commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `c5d6061`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #75 remains open until the merge is
  approved, per the workflow.
- Approval gates: the maintainer's `plan and go` instruction was taken as approval to
  activate P11 and start P11.1. Merge, branch deletion, and issue closure remain
  gated on approval of this report.
- The pipeline entry point is in `pipeline/`, which the repository contract validates
  by execution rather than by the strict `scripts/` coverage gates. The run evidence is
  in the report and summary JSON.

## 3. Gate evidence

At `c5d6061`, before this report was added:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.08
format              GREEN       0.09
types               GREEN       4.49
tests               GREEN       7.95
validator           GREEN       0.28
docs                GREEN       2.18

OVERALL: GREEN. Every gate passed.
```

The dashboard is rerun after the report commit and before the approval request.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| pending | report commit | pending | The report commit's CI run is posted on pull request #76 before approval. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The diagnostic writes outputs under `build/`, so the raw tables are not tracked | The repository ignores `build/`, `data/lidar/`, and `runtime/` | The small summary JSON and the report tables are tracked; the command reproduces the raw tables |
| The CWH cards are copied into the instance | The instance is standalone first and should not depend on a parent FEMIC checkout | The card hashes and source are recorded in the report and config |

## 6. Next phase

Recommended default: **P12 GNN point-cloud inventory feasibility**, only if the
inventory track continues.

Goal: decide whether the GNN AOI has enough public FAIB plots and LidarBC point-cloud
coverage to justify a GNN-specific first-return inventory pilot.

Tasks:
- P12.1 Audit GNN-area FAIB plots and LidarBC point-cloud coverage, and write a
  go/no-go report. Child issue to be created on approval.
- P12.2 If the audit is a go, materialize one bounded block or watershed of point
  clouds and derive first-return metrics with the TSA 23 runbook.

Acceptance: the audit reports plot counts, acquisition years, spatial clustering, and
coverage; the decision is explicit; no model, curve, THLB, AAC, or release value changes.

Reason for the default: the current CWH diagnostic is a transfer check, not a GNN
calibration. The next defensible step is a coverage/plot audit, not a refit or a
model-wide claim.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
