# Phase close-out report: P12 GNN point-cloud inventory feasibility

Phase: P12 GNN point-cloud inventory feasibility
Parent issue: #77
Pull Request: #79, `feature/p12-pointcloud-feasibility` into `main`
Evidence head: `ccf9dd5`, the commit that adds the audit, report, docs, and planning entries
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #79, and delete the branch `feature/p12-pointcloud-feasibility`.
2. Close child issue #78 with a closeout comment that cites the merge commit.
3. Close parent issue #77 with a closeout comment that cites the merge commit.
4. Do not launch a GNN inventory refit phase. The audit is a no-go; the next step is
   data acquisition, not model work. Add the point-cloud request to the existing GNN
   partner-data request instead.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Plot count, BEC composition, and recent-plot count | 24 plots (22 CWH, 2 MH); 8 since 2018 | met |
| Point-cloud tile count, years, footprint, and AOI share | 755 tiles (2019/2023/2024); 7,486.8 ha; 1.10% of 682,155 ha | met |
| Plot-to-tile overlap and nearest distances | 0 plots inside a tile; nearest recent 32.7 km, median 38.1 km, max 56.2 km | met |
| Explicit go/no-go and next acquisition step | No-go; acquire point clouds over the recent plots or add plots inside the footprint | met |
| No point-cloud download, card fit, or model change | The change set adds one pipeline script, reports, docs, and planning entries | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN at `ccf9dd5` | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #77 was created before the branch; child
  issue #78 was created immediately after and linked as a sub-issue.
- Branch from `main`: `feature/p12-pointcloud-feasibility` was created from
  `origin/main` at `316c7d0`.
- Commit messages that start with task IDs: `ccf9dd5` (`P12.1 ...`) and the report
  commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `ccf9dd5`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #78 remains open until the merge is
  approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the audit phase; merge,
  branch deletion, and issue closure wait for approval of this report.
- The P11 phase section was corrected from `active` to `complete` in the same
  change set, matching the merged P11 tracker state.

## 3. Gate evidence

At `ccf9dd5`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.12
format              GREEN       0.21
types               GREEN       0.35
tests               GREEN      10.10
validator           GREEN       0.56
docs                GREEN       1.69

OVERALL: GREEN. Every gate passed.
```

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| pending | report commit | pending | The report commit's CI run is posted on pull request #79 before approval. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The P11 roadmap section still said `active` after P11 merged | The P11 merge did not update its phase section status | Corrected to `complete` in this phase |
| The audit used tile bounding boxes, not valid-pixel coverage | No point clouds were downloaded | Recorded as an upper-bound limit in the report |

## 6. Next phase

Recommended default: **no new model phase**. The audit is a no-go.

The next step is data acquisition:
- Request LidarBC or partner point clouds over the 8 recent FAIB plots (or all 24).
- Or identify recent plots inside the existing 1.10% point-cloud footprint.

Reason: a local fit without co-located plots and point clouds would be a transfer
claim, not a GNN calibration.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
