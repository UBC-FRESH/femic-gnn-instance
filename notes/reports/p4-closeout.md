# Phase close-out report: P4 FHOPS-native marine transport

Phase: P4 FHOPS-native marine transport
Parent issue: #30
Pull request: #32, `feature/p4-fhops-marine` into `main`
Evidence head: `34ebaad`, the head that the gates and CI run below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #32, and delete the branch `feature/p4-fhops-marine`.
2. Close task #31 and parent issue #30 with a closeout comment that cites the merge commit.
3. Keep the published economic screen on the legacy transport path. Queue a bounded data task for actual GNN barge terminals, road/water distances, and current carrier/terminal quotes before any switch to the FHOPS path as the published base.
4. Do not create a release, tag, or sustainable label from P4.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| The FHOPS marine fixture solves from the adapter. | `python pipeline/fhops_marine_transport.py --out runtime/p4/fhops_marine_cost.csv`; 3/3 optimal. | met |
| The adapter reports water volume, barge trips, drayage, barge variable, terminal handling, fixed dispatch, total, and cost per m3. | `runtime/p4/fhops_marine_cost.csv`; base 2,250 m3, 1 trip, 13,725 CAD, 6.100 CAD/m3. | met |
| The screens can select `fhops-marine` and still reproduce legacy. | Legacy full-THLB 88.0/95.5/96.8 exactly; FHOPS 90.2/95.8/97.0. | met |
| FHOPS commit, scenario, volume basis, and data status are recorded. | `config/cost_revenue/transport/fhops_marine.yaml`; `notes/reference/fhops-marine-transport.md`. | met |
| No sustainable, profitable, or current-quote claim is added. | Docs and notes label the fixture synthetic and diagnostic. | met |
| Dashboard and validator are green. | `dashboard.py` GREEN on six gates; `check_workflow.py` 0/0. | met |

## 2. Workflow compliance

- Parent issue before the branch: #30 created, then #31, then `feature/p4-fhops-marine`.
- Branch from `main`: `7103af5`.
- Commit messages that start with task IDs: `34ebaad` (P4.1).
- Gates for each commit: section 3.
- Roadmap and changelog in step: `34ebaad` updates both.
- Child issues closed with closeout evidence: queued; #31 closes after merge.
- Approval gates: issue and branch creation only; no settings, tag, release, or visibility change.

## 3. Gate evidence

`34ebaad`:

- `python scripts/dashboard.py`: GREEN (lint, format, types, tests, validator, docs).
- `python scripts/check_workflow.py`: 0 errors, 0 warnings.
- `python -m sphinx -b html docs _build/html -W`: build succeeded.
- `python -m py_compile` on the three changed pipeline entry points: clean.
- FHOPS adapter: low/base/high cases optimal at 5.642/6.100/7.097 CAD/m3.
- Legacy full-THLB reproduction: 88.0/95.5/96.8; FHOPS sensitivity: 90.2/95.8/97.0.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40223670308` | `34ebaad` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The adapter adds truck and barge fixed dispatch cost outside FHOPS Phase I. | Phase I charges variable, handling, and trip cost; Phase II charges fixed cost. The transport cost needs the fixed component. | Added and labelled `contract_fixed_cost_cad`; documented in the adapter and note. |
| The FHOPS fixture is synthetic, not a GNN terminal inventory. | The GNN instance has no actual barge terminals, road network, or water distances. | Kept the path opt-in; published screen remains legacy; recorded the data gap. |
| Legacy remains the default screen path. | The FHOPS fixture is not current-quote calibrated; switching the headline would imply unsupported precision. | Added `--transport fhops-marine` and a separate sensitivity table. |
| Phase II/III barge scheduling is not the cost basis. | The required transport output is a cost, and Phase I exposes the components; Phase II is a daily scheduling model. | Recorded as a limit; no schedule claim. |

## 6. Next phase

No model phase is activated by this report. The next bounded step is data collection:

- actual GNN barge terminals and origin/destination ports;
- road and water distances;
- current carrier, barge, and terminal quotes;
- observed barge utilisation and seasonality.

Only after those inputs exist should the published screen switch from legacy to FHOPS marine. The FHOPS adapter and sensitivity remain available in the meantime. Any release or sustainable-label change needs a separate approval.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
