# Phase close-out report: P16 Private LiDAR fit pipeline

Phase: P16 Private LiDAR fit pipeline
Parent issue: #91
Pull request: #93, `feature/p16-private-lidar-fit` into `main`
Evidence head: `ddab6d1`, the commit that adds the fit pipeline, test, runbook, and docs
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #93, and delete the branch `feature/p16-private-lidar-fit`.
2. Close child issue #92 with a closeout comment that cites the merge commit.
3. Close parent issue #91 with a closeout comment that cites the merge commit.
4. Do not run a real fit until the private upload arrives and the P14 coverage review
   shows which plots it covers.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Plot/feature matching or plot-feature input | `match_features` and `--plot-features` | met |
| Three pre-registered forms | Height identity, BA log, volume log | met |
| LOOCV, spatial-cluster, temporal metrics | `fit_summary.json` in the synthetic test | met |
| Coefficient-stability card guard | `sign_changes`; cards refused unless `--force-cards` | met |
| Cards use `femic.inventory.als.model.v1` and research caveats | Card test and `card_for` | met |
| Synthetic test without private data | 12 plots, 4 clusters; 1 passed | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN at `ddab6d1` | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #91 was created before the branch; child
  issue #92 was created immediately after and linked as a sub-issue.
- Branch from `main`: `feature/p16-private-lidar-fit` was created from `origin/main`
  at `9402e12`.
- Commit messages that start with task IDs: `ddab6d1` (`P16.1 ...`) and the report
  commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `ddab6d1`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #92 remains open until the merge is
  approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the pipeline work; merge,
  branch deletion, and issue closure wait for approval of this report.
- P15 was corrected from `active` to `complete` in the roadmap.

## 3. Gate evidence

At `ddab6d1`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.07
format              GREEN       0.07
types               GREEN       0.31
tests               GREEN      10.20
validator           GREEN       0.29
docs                GREEN       0.65

OVERALL: GREEN. Every gate passed.
```

Synthetic test: 12 plots, 4 clusters, three cards, LOOCV/spatial/temporal metrics,
and a stable-sign check.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| pending | report commit | pending | The report commit's CI run is posted on pull request #93 before approval. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The pipeline has not run on real data | The private upload is pending | The synthetic end-to-end test covers the code path; the runbook is ready |
| Nearest-cell matching is not plot-support extraction | A 25 m cell is not an 11.28 m plot | The runbook prefers a plot-level feature table for the real fit |
| Eight plots may produce unstable coefficients | Small, clustered sample | The pipeline reports sign changes and refuses cards unless forced |

## 6. Next phase

Recommended default: **no new phase** until the private upload arrives.

When it arrives:
1. run the P14 ingest kit;
2. build plot-level features;
3. run `pipeline/fit_inventory_cards.py` without `--write-cards` first;
4. review stability and holdout metrics;
5. write cards only if the signs are stable, then apply the P15 publication gate.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
