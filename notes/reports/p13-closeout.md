# Phase close-out report: P13 GNN point-cloud acquisition request

Phase: P13 GNN point-cloud acquisition request
Parent issue: #80
Pull request: #82, `feature/p13-pointcloud-acquisition-request` into `main`
Evidence head: `6d23ba1`, the commit that adds the request table, memo, docs, and planning entries
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #82, and delete the branch `feature/p13-pointcloud-acquisition-request`.
2. Close child issue #81 with a closeout comment that cites the merge commit.
3. Close parent issue #80 with a closeout comment that cites the merge commit.
4. Do not create a new model phase. Send the request package to the GNN partner
   channel and wait for a time-matched point-cloud response.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Request table covers 24 plots and flags 8 recent | `p13-gnn-pointcloud-acquisition-request.csv`: 24 rows, 8 `high` | met |
| Each row has a 2 km EPSG:3005 bbox and area | 20 columns including `request_bbox_*` and `request_bbox_area_ha` | met |
| Memo states the current gap and what acquisition unblocks | `notes/reports/p13-pointcloud-acquisition-request.md` | met |
| Linked from docs and partner note | `docs/inventory-pilot.rst`; `notes/gnn-partner-data-request.md` | met |
| No point cloud downloaded, no card fit, no model change | The change set is one pipeline script, CSV, memo, docs, and planning | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN at `6d23ba1` | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #80 was created before the branch; child
  issue #81 was created immediately after and linked as a sub-issue.
- Branch from `main`: `feature/p13-pointcloud-acquisition-request` was created from
  `origin/main` at `a65d62b`.
- Commit messages that start with task IDs: `6d23ba1` (`P13.1 ...`) and the report
  commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `6d23ba1`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #81 remains open until the merge is
  approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the request package;
  merge, branch deletion, and issue closure wait for approval of this report.
- P12 was corrected from `active` to `complete` in the roadmap.

## 3. Gate evidence

At `6d23ba1`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.08
format              GREEN       0.08
types               GREEN       5.05
tests               GREEN       6.94
validator           GREEN       0.35
docs                GREEN       1.81

OVERALL: GREEN. Every gate passed.
```

Request result:

```text
24 plots; 8 high priority, 16 secondary
recent-plot request union: 8,661.3 ha
all-plot request union: 17,613.9 ha
nearest recent existing tile: 32.7 km
```

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| pending | report commit | pending | The report commit's CI run is posted on pull request #82 before approval. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The request is a package, not an acquisition | No partner or LidarBC commitment exists | The memo says no point cloud was requested, downloaded, or processed |
| The 2 km bbox is an acquisition footprint | It is not a density or quality guarantee | Recorded as a limit in the memo |

## 6. Next phase

Recommended default: **no new model phase**.

Send the request package to the GNN partner channel. The next technical step is a
time-matched point-cloud pilot only after the data arrive.

Reason: the P12 no-go is a data gap, not a model gap.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
