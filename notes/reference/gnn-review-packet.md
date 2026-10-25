# GNN boundary and public-output review packet

Date prepared: 2026-10-25
Status: prepared for review. Not sent. No GNN confirmation has been received.
Owner: UBC-FRESH
Related: P1.1 (issue #10), P1 parent #1, `UBC-FRESH/femic#341`

## Purpose

Ask GNN to review two things before the prototype is treated as public or
operational evidence:

1. The proposed Statement of Intent boundary used as the model AOI.
2. The public-output plan for the prototype model.

This packet is a draft. It does not claim that GNN has reviewed or approved
either item.

## Boundary used

- Source service: `https://maps.gov.bc.ca/arcgis/rest/services/whse/bcgw_pub_reg_legal_and_admin_boundaries/MapServer/1`
- Layer: First Nation Statement of Intent Boundaries BC
- Feature: `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`
- Query: `NAME LIKE '%Gwa%'`, `outSR=3005`, GeoJSON
- Local files: `data/source/aoi/gnn_soi.gpkg`, `data/source/aoi/gnn_full.gpkg`
- Provenance: `data/source/aoi/gnn_aoi.json` and `notes/reference/aoi.md`

This is the **proposed** SOI polygon. It is not a final treaty boundary or a
legal title determination. The BC Treaty Commission states that the SOI map is
under review.

| Intersection | Area |
| --- | ---: |
| GNN SOI total | 703,417.95 ha |
| GNN AOI inside TSA 46/47 | 682,155.05 ha |
| TSA 46 overlap | 292,930.08 ha |
| TSA 47 overlap | 389,226.32 ha |
| Outside both TSAs | 21,262.91 ha |

The forest model uses the union of the TSA 46/47 intersections. The outside-both
portion is mostly ocean and other non-forest area and is excluded from the
model AOI.

## Prototype outputs

| Output | Current state |
| --- | --- |
| Public repository | `https://github.com/UBC-FRESH/femic-gnn-instance` |
| Public docs | `https://ubc-fresh.github.io/femic-gnn-instance/` |
| Local web UI | loopback only, port 8019; not a public deployment |
| Model matrix | local and gitignored under `runtime/` |
| Derived calibrated THLB | 52,984.42 ha |
| Derived annual AAC | 252,636.75 m3/yr |
| Opening-first benchmark | 9/10 decades met; decade 10 is 781.4 m3 below |
| Ground-plot sample | 34 rows / 10 sites; too sparse for an accuracy conclusion |
| AUs | 39 TSA-prefixed model AUs; reporting crosswalk only |

The THLB and AAC are derived from the TSA 46/47 base models. They are not legal
determinations. The public docs already carry that caveat.

## Review questions

1. Is the proposed SOI polygon acceptable as the prototype model AOI?
2. Are there areas inside the polygon that should be excluded or added for this
   prototype, such as reserves, private land, cultural areas, or ocean?
3. Is publication of the current docs and model results acceptable? Which
   outputs, if any, should remain internal?
4. Are the proposed-boundary and derived-THLB/AAC labels adequate, or is there
   preferred wording?
5. Is there a GNN-preferred boundary dataset or authority we should use instead
   of the BCGW SOI layer?
6. Who should review future updates, and what acknowledgement should the docs
   carry?

## Proposed handling of the response

- Record the response in `notes/reference/gnn-review-packet.md` and link it from
  the docs.
- If the boundary changes, rebuild the AOI and model only after the change is
  documented.
- Keep the public site labelled **prototype** until written confirmation is
  recorded.
- Do not treat silence or informal feedback as confirmation.
- Do not change curves or the derived AAC as part of the boundary review.

## Draft cover note

> We have built a prototype FEMIC/ws4 model for the TSA 46/47 portions of the
> proposed GNN Statement of Intent area. Before treating it as public or
> operational evidence, we would like to confirm the boundary and the
> public-output plan with you. The model currently uses the BCGW proposed SOI
> polygon, publishes only prototype results with explicit non-legal caveats, and
> has a sparse ground-plot sample. We are not asking for a treaty or title
> decision. We are asking whether this boundary and these outputs are appropriate
> for a prototype, and what should change before wider use.
