# Phase close-out report: P1 Validation and hardening

Phase: P1 Validation and hardening
Parent issue: #1
Pull request: #16, `feature/p1-validation-hardening` into `main`
Evidence head: `d648423`, the code head that the gates and CI runs below cover
Report commit: the commit that adds this report. Its CI run is posted on the pull request.
Date: 2026-10-25
Status: approved by the maintainer on 2026-10-25. No external review will be sought at this time. Merge queued.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back
each result.

1. Squash-merge pull request #16, and delete the branch `feature/p1-validation-hardening`.
2. Close child issue #15 with a closeout comment that cites the merge commit.
3. Close issue #10 as **deferred by the maintainer**. No external review is being sought at this time. The packet remains available; no confirmation is claimed.
4. Launch P2 Release and hand-off after the P1 merge.
5. Keep the proposed-boundary and derived/non-legal labels on every public output.

Settings changes, each with its exact command. Each one runs only after its own
approval.

- None in P1.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| P1.1 boundary and public-output review | Packet prepared at `notes/reference/gnn-review-packet.md`; public page `docs/review.rst`; **not sent**; issue #10 to close as deferred | **deferred by the maintainer** — no external review at this time; no confirmation claimed |
| P1.2 expand ground-plot evidence | Inventory: 51 sites; PSP 24 sites (17 PSP_R, 7 PSP_G); PSP check 55 observations / 12 sites; non-PSP matched 34 rows / 10 sites | met with a stated limit: still too sparse for a managed-curve conclusion |
| P1.3 TSA 46 SI/origin dependency | Base issue `UBC-FRESH/femic#343`; GNN note `notes/reference/si-origin.md`; TSA 46 = 34.7% of THLB; no AU merge or curve switch | met; base issue remains open |
| P1.4 derived THLB/AAC status | ADR 0006: prototype-only release condition; operational use needs a reviewed netdown | met |
| P1.5 decade-10 diagnostic | `notes/reference/decade10-diagnostic.md`; band-floor run still low; last period has 866 blocks; 522 openings drop after year 90 | met: horizon/age-structure end-effect |
| P1.6 UI/docs release gate and close-out | Built docs carry proposed/derived labels; UI loopback-only; this report | met |
| No model/curve/target change | `git diff f9a11c5..d648423` is docs, notes, config inventories, and pipeline helper only; no curve or target values changed | met |
| Dashboard and validator | 6/6 green; 0 errors, 0 warnings | met |
| CI | Run `40171639796`, all three jobs pass | met |

## 2. Workflow compliance

- **Parent issue before the branch:** P1 parent #1 was reconciled at P0; the P1 branch was created from `main` at `f9a11c5` after P0 merged.
- **Branch from `main`:** `feature/p1-validation-hardening`, based on `f9a11c5`.
- **Commit messages start with task IDs:** `7c56416` (P1.1), `e5cea11` (P1.2), `b8e128a` (P1.3), `26aa09f` (P1.4), `c95926f` (P1.5), `d648423` (P1.6), and the report commit (P1.6).
- **Gates for each commit:** section 3.
- **Roadmap and changelog in step:** P1 is `pr-open`; P1.2-P1.6 checked; P1.1 deferred with a note; changelog has each P1 entry.
- **Child issues:** #11-#14 closed; #15 closed at P1 close-out; #10 closes as deferred by the maintainer.
- **Approval gates:** no tag, release, visibility, branch-protection, or Pages setting changed in P1.

## 3. Gate evidence

On `d648423`:

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
| `40171639796` | `d648423` | success | Quality gates, Pre-commit parity, and Green dashboard summary all pass |

The report-only commit moves the head. Its CI run is posted on PR #16 before the
approval request is treated as current.

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| P1.1 is not confirmed | The maintainer directed that no external review will be sought at this time; the packet is prepared but not sent | P1.1 is closed as deferred; no confirmation is claimed; the prototype labels remain |
| P1 closes with a deferred task | The maintainer directed that no external review will be sought | The close-out marks P1.1 deferred and proceeds to P2 with the labels intact |
| The base TSA 46 SI issue remains open | It belongs to the base-model owner | Link is recorded in #12 and `UBC-FRESH/femic#343`; no GNN curve switch |
| The report commit moves the evidence head | The report must be committed to be reviewed | PR comment records the report commit and its CI run |
| The PSP sample is not a managed benchmark | PSP_R is experimental and PSP_G natural; median age 101 | Reported as a limitation, not as managed-curve validation |

## 6. Next phase

**P2 Release and hand-off** starts after the P1 merge. The maintainer is the
decision-maker; no external review is being sought at this time.

P2 tasks:

- P2.1 Write release notes and the known-gaps list, with the proposed-boundary,
  derived-THLB/AAC, and validation limits.
- P2.2 Tag, publish, and verify from a clean checkout. Keep the release labelled
  a prototype and carry the non-legal boundary/AAC caveats.

No tag, release, or settings change happens without the maintainer's direction;
the maintainer has directed the phase to proceed.

## 7. Decision

- [x] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
