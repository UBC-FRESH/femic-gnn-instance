# Phase close-out report: P8 Solved-proxy full-THLB sensitivity

Phase: P8 Solved-proxy full-THLB sensitivity
Parent issue: #42
Pull request: #44, `feature/p8-proxy-sensitivity` into `main`
Evidence head: `6885e2a`, the head that the gates and CI run below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: queued for approval. Not merged.

## Recommendation

Approve these actions:

1. Squash-merge pull request #44, and delete the branch `feature/p8-proxy-sensitivity`.
2. Close task #43 and parent #42 with a closeout comment that cites the merge commit.
3. Keep the published GNN transport base on legacy CLEWs/FFCM.
4. Keep the solved proxy as a diagnostic sensitivity only.
5. Do not create a release, tag, or sustainable label from P8.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Metadata identifies the P7 proxy correctly. | `public_route_assumption_rates` in screen output. | met |
| Separate full-THLB output written. | `runtime/p8/full_thlb_screening_proxy_solved.csv` (local). | met |
| Legacy/API/proxy comparison documented. | 88.0/95.5/96.8; 90.2/95.8/97.0; 89.1/95.7/96.8. | met |
| Published legacy screen unchanged. | No published output or default changed. | met |
| No current-quote or sustainable claim. | Proxy remains assumption-labelled. | met |
| Gates. | Dashboard, validator, docs, CI. | met |

## 2. Workflow compliance

- Parent issue before branch: #42, then #43, then `feature/p8-proxy-sensitivity`.
- Branch from `main`: `987a2fe`.
- Commit message starts with task ID: `6885e2a` (P8.1).
- Roadmap, proxy note, changelog, and screen metadata updated.
- Approval gates: issue and branch creation only; no settings, tag, release, or visibility change.

## 3. Gate evidence

`6885e2a`:

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- `python -m sphinx -b html docs _build/html -W`: build succeeded.
- Full-THLB proxy run: 89.1% low / 95.7% base / 96.8% high.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40241500588` | `6885e2a` | success | Quality gates, Pre-commit parity, and Green dashboard summary pass. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| Proxy sensitivity is close to legacy. | Assumed rates and route basis. | Documented; not used to switch the base. |
| Proxy metadata was hardcoded. | Earlier API-only screen path. | Now read from the selected FHOPS config. |

## 6. Next phase

No phase is activated. The next work is current data:

- confirmed terminal/vessel/operator;
- actual road/water distances;
- current carrier and terminal rates;
- observed utilisation.

Only after those inputs are reviewed should the published GNN transport base switch from legacy to solved FHOPS marine.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
