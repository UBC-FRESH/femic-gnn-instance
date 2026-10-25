# Phase close-out report: P7 Solved multi-day marine transport

Phase: P7 Solved multi-day marine transport
Parent issue: #39
Pull request: #41, `feature/p7-solved-marine` into `main`
Evidence head: `a4cff2c`, the head that the gates and CI run below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: queued for approval. Not merged.

## Recommendation

Approve these actions:

1. Squash-merge pull request #41, and delete the branch `feature/p7-solved-marine`.
2. Close task #40 and parent #39 with a closeout comment that cites the merge commit.
3. Keep the Quatsino -> Ladysmith proxy as a diagnostic comparison; keep legacy CLEWs/FFCM as the published screen.
4. Do not create a release, tag, or sustainable label from P7.
5. Keep current terminal/vessel/rate data as the next data requirement.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Config uses `mode: solve`. | `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith.yaml`. | met |
| All three cases optimal. | 10,000/7,500/5,000 m3 solved cases. | met |
| Solved/analytical comparison documented. | 8.125/9.203/11.360 both paths; `notes/reference/gnn-marine-proxy.md`. | met |
| Fixed-cost basis corrected. | Truck fixed uses loading/unloading days; barge fixed uses occupancy. | met |
| Published legacy screen unchanged. | No screen output or published default changed. | met |
| No current-quote or sustainable claim. | Proxy remains `public_route_assumption_rates`. | met |
| Gates. | Dashboard GREEN, validator 0/0, Sphinx clean, CI. | met |

## 2. Workflow compliance

- Parent issue before branch: #39, then #40, then `feature/p7-solved-marine`.
- Branch from `main`: `fa1d280`.
- Commit message starts with task ID: `a4cff2c` (P7.1).
- Roadmap, proxy note, transport notes, README, and changelog updated.
- Approval gates: issue and branch creation only; no settings, tag, release, or visibility change.

## 3. Gate evidence

`a4cff2c`:

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- `python -m sphinx -b html docs _build/html -W`: build succeeded.
- Adapter solved cases: 8.125/9.203/11.360 CAD/m3.
- Analytical cross-check matches to the cent.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40240793154` | `a4cff2c` | success | Quality gates, Pre-commit parity, and Green dashboard summary pass. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| Earlier analytical path differed from solved by fixed cost. | The adapter charged truck fixed cost for the full eight-day horizon. | Corrected to actual truck loading/unloading days; solved and analytical match. |
| Proxy uses assumed capacity/rates. | Current terminal/vessel/quotes are not public. | Kept `public_route_assumption_rates`; not the published base. |

## 6. Next phase

No phase is activated. The next work is data:

- confirmed terminal/operator and destination;
- current vessel/capacity and utilisation;
- current carrier and terminal rates;
- actual road/water distances.

Only after those inputs are reviewed should the published GNN transport base switch from legacy to solved FHOPS marine.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
