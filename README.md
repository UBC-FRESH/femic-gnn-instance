# FEMIC GNN Instance

Public prototype: https://github.com/UBC-FRESH/femic-gnn-instance  
Registered in `femic` as `external/femic-gnn-instance`.

Local bootstrap for a third FEMIC/ws4 model covering the
Gwa'sala-'Nakwaxda'xw Nations (GNN) traditional territory. The model is the
union of the TSA 46 and TSA 47 portions of the proposed GNN Statement of Intent
boundary.

Status: **local AOI bootstrap only**. No public repository, model build, or
Pages site exists yet. The boundary is the proposed Statement of Intent
polygon, not a final treaty boundary or legal title determination. Confirm the
boundary and public-output plan with GNN before release.

## Prototype result

- Combined calibrated THLB: **52,984.42 ha**
- Derived annual AAC: **252,636.75 m3/yr** (not legal)
- Opening-first: 3,158 openings, 5,618 blocks, 39,558.5 ha
- 100% 5-40 ha patches
- 9/10 decades met; decade 10 is 781.4 m3 below the derived band

See `notes/reference/model-build.md`.

## AOI

- `data/source/aoi/gnn_soi.gpkg` — proposed GNN SOI polygon, EPSG:3005.
- `data/source/aoi/gnn_full.gpkg` — SOI clipped to the TSA 46/47 union.
- `data/source/aoi/gnn_aoi.json` — area and provenance summary.

| Item | Area |
| --- | ---: |
| GNN SOI total | 703,417.95 ha |
| GNN AOI inside TSA 46/47 | 682,155.05 ha |
| TSA 46 overlap | 292,930.08 ha |
| TSA 47 overlap | 389,226.32 ha |
| Outside both TSAs | 21,262.91 ha |

Source: BCGW `WHSE_LEGAL_AND_ADMIN_BOUNDARIES.QSOI_BC_REGIONS`,
feature `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`.

## Dependencies

- TSA 46 and TSA 47 base models (P1.7) are merged and stable.
- A GNN-specific AU harmonization decision.
- A derived THLB/AAC benchmark, clearly labelled non-legal.
- GNN review of the proposed boundary and any public output.

Tracking issue: `UBC-FRESH/femic#341`.
