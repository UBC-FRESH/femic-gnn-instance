# Phase close-out report: P17 Fit pipeline validation against the TSA 23 card

Phase: P17 Fit pipeline validation against the TSA 23 card
Parent issue: #94
Pull request: #96, `feature/p17-fit-validation-tsa23` into `main`
Evidence head: `1e9fda3`, the commit that adds the fixture, regression test, report, and docs
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #96, and delete the branch `feature/p17-fit-validation-tsa23`.
2. Close child issue #95 with a closeout comment that cites the merge commit.
3. Close parent issue #94 with a closeout comment that cites the merge commit.
4. Do not create a new model phase. The fit pipeline is validated against a published
   card and is pinned.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Public fixture with provenance | `tests/fixtures/inv01_tsa23_training.csv` + README | met |
| Reproduce published coefficients and scale | Height, BA, volume all match to machine precision | met |
| Reproduce LOOCV RMSE | 0.68848957 / 4.41421558 / 20.66578728 vs cards rounded 0.688 / 4.414 / 20.666 | met |
| Regression test | `tests/test_fit_inventory_cards_tsa23.py`; 1 passed | met |
| TSA 23 / GNN boundary stated | Validation report and docs | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #94 was created before the branch; child
  issue #95 was created immediately after and linked as a sub-issue.
- Branch from `main`: `feature/p17-fit-validation-tsa23` was created from
  `origin/main` at `f7d9dfb`.
- Commit messages that start with task IDs: `1e9fda3` (`P17.1 ...`) and the report
  commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `8246c2b`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #95 remains open until the merge is
  approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the validation; merge,
  branch deletion, and issue closure wait for approval of this report.
- P16 was corrected from `active` to `complete` in the roadmap.

## 3. Gate evidence

At `1e9fda3`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.08
format              GREEN       0.09
types               GREEN       4.61
tests               GREEN      11.26
validator           GREEN       0.37
docs                GREEN        1.71

OVERALL: GREEN. Every gate passed.
```

The regression test asserts the three published card coefficient sets, scales, and
LOOCV RMSE.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| 41424386729 | `2b4abfe` | success | Quality gates, Green dashboard summary, and Pre-commit parity passed. The only later change is this CI-table refresh. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| RMSE differs in the last decimals | The published cards round to three decimals | The test uses a strict tolerance against the unrounded pipeline value and the report shows the rounded card values |
| The fixture is the 14-plot TSA 23 pilot | It is the only published training table available | Recorded as a TSA 23 IDF validation, not a GNN calibration |

## 6. Next phase

Recommended default: **no new phase** until the private upload arrives.

The fit pipeline is validated against a published card; the next event is Ken's LAZ
upload.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
