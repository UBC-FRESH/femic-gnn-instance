# Phase close-out report: P2 Release and hand-off

Phase: P2 Release and hand-off
Parent issue: #17
Pull request: #20, `feature/p2-release` into `main`
Evidence head: `49fa20b`, the code head that the gates and CI runs below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: approved by the maintainer. Release execution queued.

## Recommendation

The maintainer has directed the prototype release to proceed; no external review
is being sought. Carry out these actions in order, and read back each result.

1. Squash-merge pull request #20, and delete `feature/p2-release`.
2. Tag the merge commit `v0.1.0-prototype` and publish a GitHub **pre-release**.
3. Verify Pages, `llms.txt`, and a clean checkout.
4. Close child #19 and parent #17 with the release evidence.
5. Set P2 to `complete` in `ROADMAP.md` and record the release in `CHANGE_LOG.md`.
6. Update the `femic` submodule pointer to the release merge.

No settings change beyond the pre-release and the already-enabled Pages is
requested.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| P2.1 release notes and known gaps | `notes/releases/v0.1.0-prototype.md`, `docs/release.rst` | met |
| Prototype / pre-release labels | Release notes, docs page, README, and `CITATION.cff` version `0.1.0` | met |
| Boundary caveat | Proposed SOI polygon; P1.1 deferred; no confirmation claimed | met |
| THLB/AAC caveat | Derived and non-legal; ADR 0006 | met |
| Known gaps | Sparse ground plots, TSA 46 SI dependency, decade-10 end-effect, TSA-prefixed AUs | met |
| No model change | `git diff a3af911..49fa20b` changes notes, docs, citation, and README only | met |
| Dashboard and validator | 6/6 green; 0 errors, 0 warnings | met |
| CI | Run `40172281409`, all three jobs pass | met |
| P2.2 tag and publish | Executes after the merge; evidence is posted on #17 | pending until execution |

## 2. Workflow compliance

- **Parent issue before the branch:** P2 parent #17 was created before `feature/p2-release` work.
- **Branch from `main`:** `feature/p2-release`, based on `a3af911`.
- **Commit messages start with task IDs:** `848c691` (P2.1 activation), `c66fbb5` (P2.1), `0cbfcd3` (P2.2), `49fa20b` (P2.2), and the report commit (P2.2).
- **Gates for each commit:** section 3.
- **Roadmap and changelog in step:** P2 is `pr-open`; P2.1 checked; P2.2 pending release; changelog has the P2 entries.
- **Child issues:** #18 closed; #19 closes with the release; parent #17 closes after the release.
- **Approval gates:** the maintainer directed the prototype release; no external review is being sought. P1.1 remains deferred.

## 3. Gate evidence

On `49fa20b`:

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
| `40172281409` | `49fa20b` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass |

The report-only commit moves the head. Its CI run is posted on PR #20 before
the tag.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| No external boundary review | The maintainer directed that no review will be sought at this time | P1.1 is closed as deferred; the proposed-boundary and non-legal labels remain |
| P2.2 executes after the merge | A tag must point to the main merge commit | The release evidence is posted on #17 and in the changelog after verification |
| The report-only commit moves the head | The report must be committed to be reviewed | The PR comment records the report commit and its CI run |

## 6. Post-release state

- The release is `v0.1.0-prototype`, explicitly a pre-release.
- Public docs and `llms.txt` are the public surface.
- The model remains a prototype; operational use requires a reviewed GNN netdown.
- The TSA 46 SI dependency remains open at `UBC-FRESH/femic#343`.
- No further phase is activated. Maintenance continues under `ROADMAP.md` and the issue tracker.

## 7. Decision

- [x] Approve as written. The maintainer directed the prototype release to proceed.
- [ ] Approve with the changes stated here: <changes>.
