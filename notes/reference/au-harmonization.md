# GNN AU harmonization decision

Date: 2026-10-25
Status: model AUs stay TSA-prefixed; reporting crosswalk only.

## Question

Should the GNN model merge the TSA 46 and TSA 47 AUs that share a nominal
stratum and SI level?

## What is in the model

- 39 AUs in the combined bundle.
- 37 AUs have clipped stand area; two TSA 46 CWH_FDC AUs have no rows.
- The model keeps TSA-prefixed AU ids (46xxxxx / 47xxxxx).

The AU area/THLB table is `config/tsr/gnn_au/gnn_au_area.csv`. The largest
cells are:

| AU | TSA | Stratum | SI | THLB ha | THLB share |
| --- | ---: | --- | --- | ---: | ---: |
| 4702001 | 47 | CWH_CW | M | 10,744.5 | 20.3% |
| 4703001 | 47 | CWH_CW | H | 7,495.8 | 14.1% |
| 4603000 | 46 | CWH_CW | H | 7,346.9 | 13.9% |
| 4701001 | 47 | CWH_CW | L | 6,493.2 | 12.3% |
| 4602000 | 46 | CWH_CW | M | 3,736.6 | 7.1% |

CWH_CW alone is about **67.6%** of the derived THLB.

## Curve test

For nominal matches, the TSA 46 and TSA 47 curves are not interchangeable.
Example volume at age 100:

| Reporting group | Curve | TSA 46 | TSA 47 | Delta |
| --- | --- | ---: | ---: | ---: |
| CWH_CW H | untreated | 85.5 | 584.6 | -85.4% |
| CWH_CW H | treated | 379.7 | 604.9 | -37.2% |
| CWH_HW H | untreated | 539.2 | 807.5 | -33.2% |
| CWH_HW H | treated | 471.5 | 936.5 | -49.7% |
| CWH_FD H | untreated | 495.0 | 718.8 | -31.1% |
| CWH_FD H | treated | 643.3 | 965.1 | -33.3% |
| MH_HM H | untreated | 191.2 | 242.2 | -21.1% |

Full comparison: `config/tsr/gnn_au/gnn_au_curve_comparison.csv`.

The differences are large. Merging by nominal stratum/SI would require choosing
one curve and would hide the provenance of the other. That is not acceptable
without evidence that the curves should be equal.

## Decision

1. **Keep TSA-prefixed AUs in the model.** This preserves the TSA-specific curve
   and SI provenance.
2. **Add a reporting crosswalk only.** `gnn_au_reporting_crosswalk.csv` maps each
   model AU to a reporting group (`CWH_FDC` -> `CWH_FD`, `MH_H` -> `MH_HM`).
3. **Do not merge curves or rebuild for harmonization.** A reporting group is
   not a model AU.
4. **Flag the SI/curve issue.** TSA 46 validation already found that checkpoint
   SI understates managed-stand SI (16.3 m vs observed 23.0 m in the dominant
   CWH_HW H cell). The GNN chunk inherits that issue. It is a base-model
   accuracy question, not a reason to merge AUs.

## Consequence

No GNN model rebuild is needed for AU harmonization. The next accuracy work is
SI/origin validation and more ground plots, not AU merging.
