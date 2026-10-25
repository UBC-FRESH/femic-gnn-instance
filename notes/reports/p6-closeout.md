# Phase close-out report: P6 Quatsino Sound to Ladysmith public-route proxy

Phase: P6 Quatsino Sound to Ladysmith public-route proxy
Parent issue: #36
Pull request: #38, `feature/p6-marine-proxy` into `main`
Evidence head: `2383346`, the head that the gates and CI run below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: queued for approval. Not merged.

## Recommendation

Approve these actions:

1. Squash-merge pull request #38, and delete the branch `feature/p6-marine-proxy`.
2. Close task #37 and parent #36 with a closeout comment that cites the merge commit.
3. Keep the published transport base on legacy CLEWs/FFCM.
4. Keep the Quatsino-Ladysmith proxy as a diagnostic comparison only.
5. Track the multi-day Phase I gap at `UBC-FRESH/fhops#196`.
6. Request current terminal, vessel, road, and carrier/terminal data before any published switch.
7. Do not create a release, tag, or sustainable label from P6.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Public route and historical terminal evidence recorded. | Seaspan Log Barging 101; TFL 6 1999/2000; `notes/reference/gnn-marine-proxy.md`. | met |
| GNN-specific proxy scenario added and run. | `config/cost_revenue/transport/fhops_marine_quatsino_ladysmith/`; 3 cases. | met |
| Assumptions labelled. | Config `public_route_assumption_rates`; assumption table in the note. | met |
| Proxy not presented as solved Phase I. | Status `analytical_proxy`; FHOPS #196 limitation. | met |
| Published screen remains legacy. | Only docs/notes changed; no published screen output. | met |
| No current-quote or sustainable claim. | Proxy note and config explicitly reject both. | met |
| Dashboard, validator, docs pass. | GREEN, 0/0, clean Sphinx build. | met |

## 2. Workflow compliance

- Parent issue before the branch: #36 created, then #37, then `feature/p6-marine-proxy`.
- Branch from `main`: `419060b`.
- Commit messages that start with task IDs: `2383346` (P6.1).
- Gates for each commit: section 3.
- Roadmap and changelog in step: `2383346`.
- Child issues closed with closeout evidence: queued; #37 closes after merge.
- Approval gates: issue and branch creation only; no settings, tag, release, or visibility change.

## 3. Gate evidence

`2383346`:

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- `python -m sphinx -b html docs _build/html -W`: build succeeded.
- P4 API fixture still solves: 5.642/6.100/7.097 CAD/m3.
- P6 proxy cases: 8.125/9.203/11.360 CAD/m3.
- FHOPS #196 opened for the multi-day Phase I gap.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40228344644` | `2383346` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| Phase I could not solve the proxy voyage. | The 3,955-minute barge cycle exceeds the 510-minute daily fleet capacity; adding eight barges would fake the fleet. | Used an analytical calculation from the FHOPS marine lane contract and opened FHOPS #196. |
| Proxy uses assumed rates and capacity. | Current carrier/terminal data and vessel confirmation are not public. | Labelled `public_route_assumption_rates`; kept out of the published base. |
| Route distance is an approximation. | No public navigation route or survey was available. | Used documented waypoints and labelled it a distance check, not a navigation route. |

## 6. Next phase

No model phase is activated. The next steps are:

- resolve or track FHOPS #196 for multi-day marine cycles;
- obtain current terminal, vessel, road, and carrier/terminal data;
- decide whether the proxy should become the published base only after those inputs are reviewed.

The legacy CLEWs/FFCM path remains the published comparison. Any release or sustainable-label change needs separate approval.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
