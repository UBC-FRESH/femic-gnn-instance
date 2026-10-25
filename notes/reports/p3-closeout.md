# Phase close-out report: P3 Diagnostic operability, cost, and net revenue

Phase: P3 Diagnostic operability, cost, and net revenue
Parent issue: #22
Pull request: #29, `feature/p3-operability-cost-revenue` into `main`
Evidence head: `cb906f5`, the code head that the gates and CI runs below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: approved by the maintainer as a diagnostic phase. Merge queued. Not a release.

## Recommendation

1. Squash-merge pull request #29, and delete `feature/p3-operability-cost-revenue`.
2. Close child issues #25, #26, #27, and #28 with closeout comments that cite the merge commit.
3. Close parent #22.
4. Keep `UBC-FRESH/fhops#187` open for marine/barge hauling support.
5. Keep the public release **volume-only**. Do not change the sustainable label.
6. Do not activate a P4 until current quotes, observed recovery, finer terrain, and solved FHOPS systems are available.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| P3.1 operability/cost/revenue audit | `notes/reference/operability-cost-revenue.md`; FHOPS/barge/price gap list | met |
| P3.2 cost/revenue contract | `docs/cost-revenue-contract.rst`; synthetic fixture | met |
| P3.3 grade/sort and price deck | local reviewed BC deck; hash recorded; recovery matrix; cypress proxy | met with stated limits |
| P3.4 FHOPS harvest/haul/barge costs | full-system registry costs; 40/stratified pilots; CLEWs barge/truck evidence; FHOPS #187 | met with stated limits |
| P3.5 net revenue and sustainable gate | full-THLB screen: 95.5% base, 88.0-96.8%; gate defined | met with stated limits |
| P3.6 validate/document/close-out | docs page, release caveat, this report | met |
| Model/curve/AAC unchanged | no model, curve, target, THLB, or AAC edits | met |
| Dashboard/validator | 6/6 green; 0 errors, 0 warnings | met |
| CI | run `40219295693`, all three jobs pass | met |

## 2. Workflow compliance

- Parent issue #22 existed before the phase branch.
- Branch `feature/p3-operability-cost-revenue` from `main`.
- Commit messages start with task IDs: P3.1-P3.6.
- Roadmap and changelog are in step: P3 is `pr-open`; tasks checked with limits.
- Child issues #23/#24 were closed earlier; #25-#28 close with this report.
- No settings changes; Pages was already enabled. FHOPS #187 is an upstream issue, not a GNN release.
- Approval: the maintainer directed P3 to close as a diagnostic phase.

## 3. Gate evidence

On `cb906f5`:

```text
GATE                STATUS
lint                GREEN
format              GREEN
types               GREEN
tests               GREEN
validator           GREEN
docs                GREEN

OVERALL: GREEN
```

`python scripts/check_workflow.py` reports `0 error(s), 0 warning(s)`.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| `40219295693` | `cb906f5` | success | Quality gates, Pre-commit parity, Green dashboard summary |

The report-only commit moves the head. Its CI run is posted on PR #29 before the
merge.

## 5. Deviations and limits

| Limit | Cause | Consequence |
| --- | --- | --- |
| Class-average full-system costs | Only three blocks were costed through the registry bottleneck | Full-THLB costs are not per-block FHOPS solves |
| Coarse centroid DEM | Zoom 11 terrain; no LiDAR | Operability classes are screening, not a geotechnical survey |
| Provisional recovery | No observed GNN cruise/mill recovery | Net revenue range is assumption-driven |
| Cypress proxy | No second-growth cypress price | Revenue for cypress is uncertain |
| Legacy transport | No current carrier/terminal quotes; FHOPS barge support missing (#187) | Barge/truck costs are diagnostic |
| No decade-level financial gate | The P3 output is a THLB screen, not a solved financial schedule | The gate is defined but not applied to a per-decade financial plan |

These limits are why P3 is a diagnostic phase, not a sustainable release.

## 6. Next phase

No P4 is activated. The next work is data-driven:

- current barge/truck/terminal quotes,
- observed grade/sort recovery for the GNN area,
- second-growth cypress or an accepted proxy,
- actual road/water distances and port/landing data,
- finer DEM/LiDAR,
- solved FHOPS shift scenarios for ground, cable, and helicopter systems.

FHOPS barge support remains upstream issue #187.

## 7. Decision

- [x] Approve as written. The maintainer directed the diagnostic close-out.
- [ ] Approve with the changes stated here: <changes>.
