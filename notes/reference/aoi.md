# GNN AOI provenance

Date: 2026-10-25

## Boundary

- Source service: `https://maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_reg_legal_and_admin_boundaries/MapServer/1`
- Layer: First Nation Statement of Intent Boundaries BC
- Feature: `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`
- Query: `NAME LIKE '%Gwa%'`, EPSG:3005, GeoJSON
- Stored at: `data/source/aoi/gnn_soi.gpkg`

This is the **proposed Statement of Intent boundary**, not a final treaty
boundary or a legal title determination. The BC Treaty Commission page states
that the SOI map is under review. Confirm with GNN before public or operational
use.

## AOI construction

`gnn_full.gpkg` is the intersection of the SOI polygon with the union of the
TSA 46 and TSA 47 boundaries. The 3.0% of the SOI outside both TSAs is ocean or
otherwise outside the base model extents and is excluded.

| Item | Area |
| --- | ---: |
| SOI total | 703,417.95 ha |
| TSA 46 overlap | 292,930.08 ha |
| TSA 47 overlap | 389,226.32 ha |
| AOI union | 682,155.05 ha |
| Outside both | 21,262.91 ha |

## Next decisions

- custom FEMIC case code and run profile;
- AU harmonization (`CWH_FDC`/`CWH_H`/`MH_H` vs `CWH_FD`/`MH_HM`);
- derived THLB and non-legal benchmark;
- GNN review and public-repo approval.
