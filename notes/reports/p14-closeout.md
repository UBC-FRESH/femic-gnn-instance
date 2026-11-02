# Phase close-out report: P14 Private LiDAR ingest readiness

Phase: P14 Private LiDAR ingest readiness
Parent issue: #83
Pull request: #86, `feature/p14-private-lidar-ingest` into `main`
Evidence head: `45ef56a`, the commit that adds the ingest kit, governance decision, runbook, and request clarification
Report commit: the commit that refreshes this report. Its CI run is posted on the pull request.
Date: 2026-11-02
Status: queued for approval. Not merged.

## Recommendation

Approve these actions. The agent carries them out in this order, and reads back each result.

1. Squash-merge pull request #86, and delete the branch `feature/p14-private-lidar-ingest`.
2. Close child issues #84 and #85 with closeout comments that cite the merge commit.
3. Close parent issue #83 with a closeout comment that cites the merge commit.
4. Do not create a new model phase until the private upload arrives and the coverage
   review shows which plots it covers.

Settings changes, each with its exact command. Each one runs only after its own approval.

- None.

## 1. Objectives and acceptance

| Criterion | Evidence | Status |
| --- | --- | --- |
| Read-only ingest kit with private/public outputs | `pipeline/ingest_private_lidar.py`; private summary and optional redacted public summary/tile index | met |
| Manifest status and optional hash mismatches | `manifest_status`; synthetic test covers a valid manifest and a mismatch | met |
| CRS, bounds, point count, density | Header-only records; synthetic LAS test | met |
| AOI and P13 plot coverage | `coverage_summary`; test reports 1 high-priority plot covered | met |
| Synthetic test without private data | `tests/test_ingest_private_lidar.py`; 2 passed | met |
| P13 memo and partner note state the private upload is pending | `notes/reports/p13-pointcloud-acquisition-request.md`; `notes/gnn-partner-data-request.md` | met |
| Dashboard green | `python scripts/dashboard.py` -> OVERALL: GREEN at `45ef56a` | met |

## 2. Workflow compliance

- Parent issue before the branch: issue #83 was created before the branch; child
  issues #84 and #85 were created immediately after and linked as sub-issues.
- Branch from `main`: `feature/p14-private-lidar-ingest` was created from
  `origin/main` at `fdc949b`.
- Commit messages that start with task IDs: `45ef56a` (`P14.1/P14.2 ...`) and the
  report commit.
- Gates for each commit: section 3.
- Roadmap and changelog in step: both were changed in `45ef56a`; the report commit
  only adds this report.
- Child issues closed with closeout evidence: #84 and #85 remain open until the merge
  is approved, per the workflow.
- Approval gates: the maintainer's `go` instruction approved the ingest readiness
  work; merge, branch deletion, and issue closure wait for approval of this report.
- P13 was corrected from `active` to `complete` in the roadmap.

## 3. Gate evidence

At `45ef56a`:

```text
GATE                STATUS   SECONDS
lint                GREEN       0.07
format              GREEN       0.08
types               GREEN       0.22
tests               GREEN       9.67
validator           GREEN       0.32
docs                GREEN       1.89

OVERALL: GREEN. Every gate passed.
```

The synthetic test covers a valid drop, manifest hash check, P13 high-priority
coverage, public redaction, and a hash mismatch.

## 4. CI evidence

| Run ID | Head commit | Conclusion | Notes |
| --- | --- | --- | --- |
| pending | report commit | pending | The report commit's CI run is posted on pull request #86 before approval. |

## 5. Deviations

| Deviation | Cause | Remedy |
| --- | --- | --- |
| The ingest kit has not run on the real private data | The Globus `/incoming/` and `/manifests/` directories were empty | The synthetic test proves the path; the runbook is ready for the first real drop |
| Full SHA-256 verification is opt-in | Hashing 2 TB is expensive | The runbook uses a structural check first and the full hash check after transfer completion |
| Unknown CRS skips coverage | A file without a parsable CRS cannot be transformed to EPSG:3005 | The summary flags untransformed tiles and reports zero footprint for them |

## 6. Next phase

Recommended default: **no new model phase** until the private upload arrives.

When it arrives:
1. run the ingest kit and review the private summary;
2. check manifests, CRS, density, and P13 plot coverage;
3. derive DEM/DSM/CHM and first-return metrics for covered plots;
4. publish only reviewed derived products under ADR 0007.

## 7. Decision

- [ ] Approve as written.
- [ ] Approve with the changes stated here: <changes>.
