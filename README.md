# FEMIC GNN Instance

- Public prototype: https://github.com/UBC-FRESH/femic-gnn-instance
- Documentation: https://ubc-fresh.github.io/femic-gnn-instance/
- Registered in `femic` as `external/femic-gnn-instance`.

A third FEMIC/ws4 model covering the Gwa'sala-'Nakwaxda'xw Nations (GNN)
traditional territory, built from the TSA 46 and TSA 47 portions of the
proposed GNN Statement of Intent boundary.

## Status

Prototype release `v0.1.0-prototype` is available. The prototype and its diagnostic/descriptive data layers are in place. Bounded LiDAR and public terrain/VRI indicators are **descriptive only**. `ROADMAP.md` records the project status, and the model remains a **prototype**, not a legal or operational release.

> **Volume-only caveat:** This release does not contain a validated operability, cost, or net revenue model. A diagnostic economic screen and descriptive terrain/VRI indicators exist, but the release label remains volume-only. It is not a "sustainable harvest level" and it is not financially assessed.

> **Warning:** The boundary is the **proposed GNN Statement of Intent** polygon,
> not a final treaty boundary or a legal title determination. Confirm the
> boundary and the public-output plan with GNN before operational use. The THLB
> and AAC are derived prototype values, not legal determinations.

## Economic screening (diagnostic)

Full derived THLB: **95.5% positive** in the base screening case (88.0-96.8% across price/recovery). It uses class-average full-system costs, coarse DEM centroid terrain, provisional recovery, and legacy transport. The 30 m Terrarium/VRI fields are not used in this screen, and the 10 m LiDAR pilot is not model-wide. A separate FHOPS marine API test is available with `--transport fhops-marine`; its fixture is Sunshine Coast -> Howe Sound, not the northern Vancouver Island GNN geography, so it is not a GNN transport estimate. An internal public-route proxy uses Quatsino Sound -> Ladysmith Harbour; it now runs as a solved FHOPS Phase I case, is diagnostic only, and is not the published base. Neither result is sustainable or financially calibrated.

## Terrain and indicator evidence

The indicator work added two distinct things:

- **Model-wide descriptive proxies:** AWS Terrarium zoom 12 terrain at 30 m and VRI stand fields, with source and coverage flags.
- **A bounded LiDAR pilot:** 181 direct fragments / 184 blocks / 979 ha, 10 m LidarBC products. It is not a GNN-wide layer.

The public proxies failed validation for absolute operability use: Terrarium mean slope is biased **-13.66 points** against the LiDAR pilot, and VRI height has low spatial correlation with CHM. Do not use these fields for ground/cable/heli thresholds or CHM claims. See the [indicator documentation](https://ubc-fresh.github.io/femic-gnn-instance/indicators.html).

## Prototype result

- Combined calibrated THLB: **53.0 thousand ha**
- Derived annual AAC: **252,637 m3/yr** (not legal)
- Opening-first: 3,158 openings, 5,618 blocks, 39.6 thousand ha
- 100% 5-40 ha patches
- All 10 decades within 0.04% of the derived target band
- GNN-area ground-plot sample: 34 rows / 10 sites, too sparse for an accuracy conclusion
- AUs: 39 TSA-prefixed; TSA 46/47 curves are not interchangeable

See `notes/reference/model-build.md`, `notes/reference/validation.md`, and
`notes/reference/au-harmonization.md`.

## Project record

`ROADMAP.md`, `CHANGE_LOG.md`, and the notes record status and decisions. The
agent operating contract is in `AGENTS.md`. Read `AGENTS.md` and `ROADMAP.md`
before changing anything.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
pre-commit install
python scripts/dashboard.py
```

## Repository map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Operating contract for coding agents |
| `ROADMAP.md` | Plan of record and issue tracker map |
| `CHANGE_LOG.md` | Dated narrative of changes |
| `docs/` | Documentation site |
| `notes/` | ADRs, reference notes, plans, and close-out reports |
| `scripts/` | Workflow tooling: validator and green dashboard |
| `pipeline/` | Model build and analysis entry points |
| `config/` | Run profiles, targets, and patch accounts |
| `data/source/` | AOI source polygons and provenance |
| `tests/` | Workflow tooling tests |
| `serve_gnn_calibrated.sh` | Loopback web UI launcher |

## Build

```bash
pipeline/build_gnn_model.sh
./serve_gnn_calibrated.sh
```

The build script expects the base instances at `../femic-tsa46-instance` and
`../femic-tsa47-instance`. Runtime outputs are gitignored.

Indicator fields are **not** run by `build_gnn_model.sh`. See the [indicator documentation](https://ubc-fresh.github.io/femic-gnn-instance/indicators.html) and
`pipeline/README.md` for the optional FEMIC/WS4 build path and the 5.5 GiB
LidarBC materialization boundary.

## AOI

- `data/source/aoi/gnn_soi.gpkg` — proposed GNN SOI polygon, EPSG:3005.
- `data/source/aoi/gnn_full.gpkg` — SOI clipped to the TSA 46/47 union.
- `data/source/aoi/gnn_aoi.json` — area and provenance summary.

| Item | Area (thousand ha) |
| --- | ---: |
| GNN SOI total | 703.4 |
| GNN AOI inside TSA 46/47 | 682.2 |
| TSA 46 overlap | 292.9 |
| TSA 47 overlap | 389.2 |
| Outside both TSAs | 21.3 |

Source: BCGW `WHSE_LEGAL_AND_ADMIN_BOUNDARIES.QSOI_BC_REGIONS`,
feature `Gwa'Sala-'Nakwaxda'xw Nation (proposed)`.

## Dependencies

- TSA 46 and TSA 47 base models are merged and stable.
- A TSA-prefixed AU decision and a reporting-only crosswalk.
- A derived THLB/AAC benchmark, clearly labelled non-legal.
- GNN review of the proposed boundary and any public output.
- Optional terrain/canopy indicators: the FEMIC LiDAR producer and WS4
  consumer, including the multi-track block fix. The indicator fields are
  descriptive, not a release gate.

Tracking issue: `UBC-FRESH/femic#341`.
