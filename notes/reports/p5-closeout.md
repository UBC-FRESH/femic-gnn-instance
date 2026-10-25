# Phase close-out report: P5 GNN marine geography and terminal data

Phase: P5 GNN marine geography and terminal data
Parent issue: #33
Pull request: #35, `feature/p5-marine-data` into `main`
Evidence head: `26cafbb`, the head that the gates and CI run below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: queued for approval. Not merged.

## Recommendation

Approve these actions:

1. Squash-merge pull request #35, and delete the branch `feature/p5-marine-data`.
2. Close task #34 and parent #33 with a closeout comment that cites the merge commit.
3. Keep the published transport base on legacy CLEWs/FFCM.
4. Request the missing terminal, route, and carrier/terminal quote data before building a GNN-specific FHOPS scenario.
5. Do not create a release, tag, or sustainable label from P5.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| GNN AOI geography and fixture mismatch documented. | `notes/reference/gnn-marine-geography.md`; centroid 51.185 N, -127.408 W; fixture 80 km water leg. | met |
| Public infrastructure labelled candidate, not confirmed. | Port Hardy, Port McNeill, Beaver Cove, Coal Harbour, Alert Bay, Port Alice; sources and "does not prove" column. | met |
| Fixture labelled API/cost-path test, not GNN estimate. | Config `upstream_fhops_fixture_api_test`; adapter, notes, README, docs corrected. | met |
| Published legacy screen unchanged. | No screening result changed; FHOPS table removed from public page. | met |
| No invented terminal, distance, rate, or sustainable claim. | Straight-line distances labelled non-cost; quotes listed missing. | met |
| Dashboard, validator, docs pass. | GREEN, 0/0, clean Sphinx build. | met |

## 2. Workflow compliance

- Parent issue before the branch: #33 created, then #34, then `feature/p5-marine-data`.
- Branch from `main`: `17972f4`.
- Commit messages that start with task IDs: `26cafbb` (P5.1).
- Gates for each commit: section 3.
- Roadmap and changelog in step: `26cafbb`.
- Child issues closed with closeout evidence: queued; #34 closes after merge.
- Approval gates: issue and branch creation only; no settings, tag, release, or visibility change.

## 3. Gate evidence

`26cafbb`:

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- `python -m sphinx -b html docs _build/html -W`: build succeeded.
- Adapter: 3/3 API fixture cases optimal.
- `screen_net_revenue.py --transport fhops-marine`: runs with `upstream_fhops_fixture_api_test` status.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40226913389` | `26cafbb` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| P4's FHOPS sensitivity was described as representative of the GNN case. | The upstream FHOPS fixture uses Sunshine Coast -> Howe Sound; the GNN AOI is northern Vancouver Island. | Corrected labels and removed the full-THLB FHOPS table from the public screening page. |
| Candidate terminals are not confirmed log-barge terminals. | Public harbour/industrial evidence does not establish log handling, ownership, capacity, or rates. | Labelled every candidate and recorded the missing evidence. |
| No GNN-specific FHOPS scenario was built. | Terminal, route, and quote data are missing; inventing them would violate the evidence rule. | Stopped at the data audit and kept the API fixture as a code-path test. |

## 6. Next phase

No model phase is activated. The next step is data supply, not a new scenario:

- GNN/maintainer confirms origin terminal(s) and destination.
- Road and water route distances.
- Barge type, capacity, load/unload time, and utilisation.
- Current carrier and terminal rates.
- Seasonality and availability.

Only after those inputs exist should a GNN-specific FHOPS scenario and a published transport switch be considered. Any release or sustainable-label change needs separate approval.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
