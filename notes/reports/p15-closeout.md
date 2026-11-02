# Phase close-out report: P15 Private LiDAR dry run and fit pre-registration

Phase: P15 Private LiDAR dry run and fit pre-registration
Parent issue: #87
Pull request: #90, `feature/p15-private-lidar-dry-run` into `main`
Evidence head: `d1df3cd`, the commit that adds the dry run, fit plan, and planning entries
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #90, and delete the branch `feature/p15-private-lidar-dry-run`.
2. Close child issues #88 and #89 with closeout comments that cite the merge commit.
3. Close parent issue #87 with a closeout comment that cites the merge commit.
4. Do not fit a model until the private upload arrives and the P14 coverage review shows
   which plots it covers.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Synthetic LAS/DEM dry run produces first-return features | 7 cells with `Lhmean`, `Lhcv`, `Lhp95`, `CC2m`, and return counts | met |
| FEMIC version requirement recorded | Runbook names `origin/main` at `03ca3a2`; local checkout lacks the command | met |
| Fit plan names LOOCV, spatial clusters, and temporal check | `notes/reports/p15-fit-preregistration.md` | met |
| Derived-public products explicit under ADR 0007 | Fit plan lists public and private products and the partner-review gate | met |
| No real private LAZ read and no model fit | The change set is reports, docs, and planning only | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN at `d1df3cd` | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #87 was created before the branch; child
  issues #88 and #89 were created immediately after and linked as sub-issues.
- Branch from `main`: `feature/p15-private-lidar-dry-run` was created from
  `origin/main` at `e338821`.
- Commit messages that start with task IDs: `d1df3cd` (`P15.1/P15.2 ...`) and the
  report commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `d1df3cd`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #88 and #89 remain open until the merge
  is approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the dry run and
  pre-registration; merge, branch deletion, and issue closure wait for approval.
- P14 was corrected from `active` to `complete` in the roadmap.

## 3. Gate evidence

At `d1df3cd`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.08
format              GREEN       0.09
types               GREEN       5.00
tests               GREEN      10.31
validator           GREEN       0.31
docs                GREEN       1.86

OVERALL: GREEN. Every gate passed.
```

Dry-run output:

```text
rows: 7
columns: fragment_id, x_center, y_center, source_tile, Lhmean, Lhcv, Lhp95,
         CC2m, all_first_returns, above2m_returns, grid_size_m
Lhmean 10.0, Lhcv 0.0, Lhp95 10.05, CC2m 100 in populated cells
```

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| 41416494142 | `9f3d49f` | success | Quality gates, Green dashboard summary, and Pre-commit parity passed. The only later change is this CI-table refresh. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The local FEMIC checkout lacks the point-cloud feature command | It is on an older branch | The runbook uses `origin/main` at `03ca3a2` via `PYTHONPATH` |
| The dry run uses a flat synthetic DEM and 12 points | No private data exists yet | Recorded as a chain test, not a terrain or density test |
| Eight plots cannot support an operational card | The public plot sample is too small and clustered | The fit plan marks operational use as unavailable |

## 6. Next phase

Recommended default: **no new model phase** until the private upload arrives.

When it arrives:
1. run the P14 ingest kit;
2. review coverage and which of the 8 plots are included;
3. run the first-return features over the covered area;
4. fit only if at least 6 plots are covered, with the pre-registered holdouts;
5. publish only reviewed derived products.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
