# Inherited TSA 46 SI/origin issue

Date: 2026-10-25
Status: linked to the base-model owner; no GNN curve change.
Base issue: `UBC-FRESH/femic#343`
GNN task: `UBC-FRESH/femic-gnn-instance#12` (P1.3)

## What is known

TSA 46 height validation found a conservative bias concentrated in CWH_HW H.
The checkpoint SI is 16.3 m while observed immature/harvested stands are at
23.0-26.0 m. A holdout managed-SI test reduced height bias from -1.61 m to
-0.23 m and MAE from 1.86 m to 1.46 m.

The cause is largely the SI input, not the TIPSY curve shape. A single AU median
SI includes the full THLB, while the observed managed stands are on better
sites.

## GNN exposure

TSA 46 contributes 18,411.68 ha of derived THLB, or **34.7%** of the GNN total.

| AU | Stratum | SI | THLB ha | GNN THLB share |
| --- | --- | --- | ---: | ---: |
| 4603000 | CWH_CW | H | 7,346.9 | 13.9% |
| 4602000 | CWH_CW | M | 3,736.6 | 7.1% |
| 4603001 | CWH_HW | H | 2,805.2 | 5.3% |
| 4603003 | CWH_YC | H | 1,686.9 | 3.2% |

The strongest height evidence is for CWH_HW H. The larger CWH_CW H cell is not
yet demonstrated to have the same SI attribution bias. Do not generalize the
same correction to every TSA 46 AU.

## Decision

- Keep TSA-prefixed AUs; do not merge model AUs.
- Do not switch the GNN model to managed-SI curves until the base-model owner
  records an origin-separated SI decision.
- Do not tune curves or the AAC to compensate.
- If the base model changes, rebuild the GNN model from the new TSA 46 bundle
  and rerun the benchmark.
- Record the base-model issue as an open dependency, not a closed GNN fix.

This follows ADR 0003 (keep TSA-prefixed AUs) and ADR 0004 (no AAC tuning).

## Files

- `UBC-FRESH/femic#343` (base-model issue)
- `external/femic-tsa46-instance/notes/reference/tipsy-validation.md` (evidence)
- `config/tsr/gnn_au/gnn_au_area.csv` (GNN exposure)
- `notes/reference/au-harmonization.md` (AU decision)
